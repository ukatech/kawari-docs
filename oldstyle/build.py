r"""華和梨マニュアルのサイトを作る（PukiWiki 1.5 の標準スキンの見た目を模した、自前の静的サイトのビルド。
里々マニュアル（satori-docs）の oldstyle/ を移したもの）。

    python oldstyle/build.py              # scripts/prepare_site.py で _site_src/ を作り、_site/ に出力する
    python oldstyle/build.py --no-prepare # _site_src/ を作り直さない

原稿（Markdown）→ HTML → wiki の構造（ヘッダ・本文の #body・左の #menubar）に組む。HTML は HTML5。
ページの URL は Zensical 版と同じ（kosui/launch/ のようにディレクトリ。外部からのリンクを切らないため）。
詳しくは oldstyle/README.md。
"""
import argparse
import copy
import json
import os
import posixpath
import re
import shutil
import string
import sys
from urllib.parse import urlsplit

import lxml.html
import markdown
import yaml
from lxml import etree
from pymdownx.slugs import slugify

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import prepare_site  # noqa: E402

SRC = prepare_site.OUT                  # 原稿の写し（_site_src/）
RAW = prepare_site.RAW                  # 生の Markdown 原稿の写し（_raw/）
OUT = os.path.join(ROOT, '_site')
STATIC = os.path.join(HERE, 'static')
SITE_URL = prepare_site.SITE_URL
SITE_PATH = urlsplit(SITE_URL).path     # /kawari-docs/（404.html のように、どの深さで開かれるかわからないページが使う）
SITE_NAME = '華和梨マニュアル'
SITE_DESCRIPTION = '伺かの SHIORI「華和梨（KAWARI）」のマニュアル'

# ページごとの OGP / Twitter カード。キーはページの URL（トップは ''）、image は SITE_URL からの相対パス（1200x630）
# 例: 'other/changelog/': {'title': '…', 'description': '…', 'image': 'assets/….png'}
OGP = {}

MD_EXTENSIONS = ['tables', 'admonition', 'attr_list', 'md_in_html', 'mdx_truly_sane_lists', 'pymdownx.superfences', 'toc']
MD_CONFIG = {
    'toc': {
        # GitHub と同じく日本語の見出しをそのままアンカーにする（prepare_site.py の heading_slug と同じ変換）
        'slugify': slugify(case='lower'),
        # PukiWiki と同じ、見出しの末尾の †（その見出しへのリンク）
        'permalink': '†',
        'permalink_class': 'anchor_super',
        'permalink_title': 'この見出しへのリンク',
    },
}

errors = []


def error(msg):
    errors.append(msg)
    print(f'エラー: {msg}', file=sys.stderr)


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path) or OUT, exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


# ---------------------------------------------------------------- URL

def page_url(md):
    """原稿（_site_src/ からのパス）のページの URL（サイトのルートから。トップは ''、末尾は /）"""
    if md == 'index.md':
        return ''
    stem = md[:-len('.md')]
    if posixpath.basename(stem) == 'index':
        return posixpath.dirname(stem) + '/'
    return stem + '/'


def rel_url(from_url, to_url):
    """ページ from_url から、ページ to_url へのリンク。from_url が None なら、サイトのルートからの絶対パス"""
    if from_url is None:
        return SITE_PATH + to_url
    r = posixpath.relpath(to_url.rstrip('/') or '.', from_url.rstrip('/') or '.')
    return './' if r == '.' else r + '/'


def rel_file(from_url, path):
    """ページ from_url から、サイトのルートからの path（画像・添付ファイルなど）へのパス"""
    if from_url is None:
        return SITE_PATH + path
    return posixpath.relpath(path, from_url.rstrip('/') or '.')


def root_of(url):
    return rel_url(url, '')


# ---------------------------------------------------------------- メニューと章立て（menu.yml）

MENU_FILE = os.path.join(HERE, 'menu.yml')
INDEX_SLUG = re.compile(r'^[a-z0-9][a-z0-9-]*(/[a-z0-9][a-z0-9-]*)*/$')
GENERATED = {}      # 自動で作る索引ページ: 原稿のパス（startup/index.md など）→ その節の Node
GENERATED_LIST = '.generated'   # 前のビルドで作った索引ページの記録（--no-prepare で消し残さないため）
PLACED = {}         # 原稿のパス → 章立て（パンくずリスト）での位置の Node


def plain(text):
    # 見出しの Markdown 記法（コード・リンク・{#id} など）を除いた文字
    text = re.sub(r'\{[#:][^}]*\}', '', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text).replace('`', '')
    return text.strip()


def h1_line(md):
    for line in read(os.path.join(SRC, md)).split('\n'):
        if line.startswith('# '):
            return line[2:]
    error(f'{md} に H1 が無い')
    return md


def h1_of(md):
    return plain(h1_line(md))


def md_escape(text):
    """索引ページ（生成する Markdown）の題に書く、メニューの題の記号を Markdown として効かなくする"""
    return re.sub(r'([\\`*_\[\]<>])', r'\\\1', text)


class Node:
    """menu.yml の 1 項目。左のメニュー・パンくずリスト・索引ページの元"""

    def __init__(self, title, parent=None, title_md=None):
        self.title = title
        self.title_md = title_md if title_md is not None else md_escape(title)   # 索引ページのリンクの文字（Markdown）
        self.parent = parent
        self.children = []      # children:（左のメニューに出る）
        self.listed = []        # list: のディレクトリのページ（左のメニューには出さず、索引ページとパンくずリストにだけ使う）
        self.list_dirs = []
        self.target = None      # 行き先（原稿のパス, フラグメント）
        self.ext = None         # 外部のページの URL
        self.md = None          # この項目がパンくずリストでの位置になる原稿（フラグメントの無い、ページそのもの）


def menu_target(spec, where):
    """menu.yml の page: に書いた原稿のパス（`INDEX.md#見出し`、まとめた元ページの `kis/set.md` も可）の行き先（原稿のパス, フラグメント）"""
    path, _, frag = spec.partition('#')
    path = 'index.md' if path == 'INDEX.md' else path
    if path in MD_PAGES:
        return path, frag
    if path in prepare_site.MERGED:
        page, prefix = prepare_site.MERGED[path]
        return page, prepare_site.FRAGMENTS.get((path, frag), prefix) if frag else prefix
    error(f'{where}: page: {spec} の原稿が無い')
    return None


def load_menu():
    """oldstyle/menu.yml の menu: を読んで、Node の木にする。
    各項目は title:（必須）、page:（原稿）か index:（自動で作る索引ページの URL）か url:（外部）、children:（下の項目）、list:（ディレクトリ）"""
    with open(MENU_FILE, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    root = Node(SITE_NAME)

    def parse(items, parent, where):
        for i, it in enumerate(items or []):
            here = f'menu.yml {where}[{i}]'
            if not isinstance(it, dict) or not it.get('title'):
                error(f'{here}: title: が無い')
                continue
            node = Node(str(it['title']), parent)
            parent.children.append(node)
            if sum(k in it for k in ('page', 'index', 'url')) > 1:
                error(f'{here}: page: index: url: は 1 つしか書けない')
            if it.get('page'):
                node.target = menu_target(it['page'], here)
                if node.target and not node.target[1] and node.target[0] in MD_PAGES:
                    node.md = node.target[0]
            elif it.get('index'):
                slug = str(it['index'])
                md = slug + 'index.md'
                if not INDEX_SLUG.match(slug):
                    error(f'{here}: index: {slug} は startup/ のように、小文字の英数字とハイフンの名前で、末尾を / にして書く')
                elif md in MD_PAGES or md in GENERATED:
                    error(f'{here}: index: {slug} は、ほかのページと重なる')
                else:
                    GENERATED[md] = node
                    node.md = md
                    node.target = (md, '')
            elif it.get('url'):
                node.ext = str(it['url'])
            lists = it.get('list') or []
            node.list_dirs = [lists] if isinstance(lists, str) else list(lists)
            parse(it.get('children'), node, f'{where}[{i}]')

    parse(data.get('menu'), root, 'menu')
    return root


def walk(node):
    for c in node.children:
        yield c
        yield from walk(c)


def list_pages(rel_dir, where):
    """list: のディレクトリのページ（原稿のパス）。ディレクトリに .nav.yml があれば、その並びを先に、残りは H1 の順"""
    if not os.path.isdir(os.path.join(SRC, rel_dir)):
        error(f'{where}: list: {rel_dir} のディレクトリが無い')
        return []
    mds = [f'{rel_dir}/{n}' for n in os.listdir(os.path.join(SRC, rel_dir)) if n.endswith('.md') and n != 'index.md']
    order = []
    nav = os.path.join(SRC, rel_dir, '.nav.yml')
    if os.path.exists(nav):
        with open(nav, encoding='utf-8') as f:
            order = [f'{rel_dir}/{e}' for e in yaml.safe_load(f)['nav'] if isinstance(e, str)]
    first = [m for m in order if m in mds]
    return first + sorted((m for m in mds if m not in first), key=h1_of)


def place_pages(root):
    """章立てでの位置を決める。ページは最初に出てきた項目の下に置く（同じページが何度か載っていてもよい）。
    list: のページは、menu.yml のどこにも載っていないものだけが、その項目の下に加わる"""
    for n in walk(root):
        if n.md and n.md not in PLACED:
            PLACED[n.md] = n
    for n in walk(root):
        for d in n.list_dirs:
            for md in list_pages(d, f'menu.yml 「{n.title}」'):
                if md not in PLACED:
                    c = Node(h1_of(md), n, title_md=h1_line(md).strip())
                    c.target = (md, '')
                    c.md = md
                    n.listed.append(c)
                    PLACED[md] = c
    for md in sorted(MD_PAGES | set(GENERATED)):
        if md not in PLACED:
            error(f'{md} が menu.yml に無い（children: に書くか、list: のディレクトリに入れる）')
    for n in walk(root):
        if not n.md and not n.ext and any(d.md for d in walk(n)):
            error(f'menu.yml 「{n.title}」: 下にページがあるのに、page: も index: も無い（索引ページを作るなら index: を書く）')


def index_markdown(node):
    """自動で作る索引ページの原稿。menu.yml の children: と、list: のページを並べるだけ"""
    base = posixpath.dirname(node.md)
    lines = [f'# {node.title_md}', '']
    for c in node.children + node.listed:
        if c.ext:
            link = c.ext
        elif c.target:
            md, frag = c.target
            link = posixpath.relpath(md, base) + ('#' + frag if frag else '')
        else:
            link = None
        lines.append(f'- [{c.title_md}]({link})' if link else f'- {c.title_md}')
    return '\n'.join(lines) + '\n'


def cleanup_generated():
    """前のビルドで作った索引ページを消す（--no-prepare のとき、_site_src/ に残っている）"""
    record = os.path.join(SRC, GENERATED_LIST)
    if not os.path.exists(record):
        return
    with open(record, encoding='utf-8') as f:
        for md in json.load(f):
            for base in (SRC, RAW):
                if os.path.exists(os.path.join(base, md)):
                    os.remove(os.path.join(base, md))
    os.remove(record)


def write_generated():
    """索引ページの原稿を _site_src/ と _raw/（生の原稿としてサイトにも置く）に書く"""
    for md, node in GENERATED.items():
        text = index_markdown(node)
        for base in (SRC, RAW):
            path = os.path.join(base, md)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(text)
    with open(os.path.join(SRC, GENERATED_LIST), 'w', encoding='utf-8') as f:
        json.dump(sorted(GENERATED), f)


def node_href(node, from_url):
    if node.ext:
        return node.ext
    if node.target:
        md, frag = node.target
        return rel_url(from_url, page_url(md)) + ('#' + frag if frag else '')
    return None


def menu_html(root, current_md, from_url):
    """左のメニュー。PukiWiki の MenuBar と同じく、最上位の項目は見出し（h4）、その下の children: は入れ子の ul にして、
    下の階層まで常に全部出す。下の項目の無い最上位の項目は、見出しにせず 1 行のリンクにする"""
    def label_of(n):
        label = esc(n.title)
        link = node_href(n, from_url)
        if link:
            cur = ' aria-current="page"' if current_md is not None and n.target and n.target == (current_md, '') else ''
            ext = ' class="external"' if n.ext else ''     # サイトの外へ飛ぶリンクは、CSS で印（↗）を付ける
            label = f'<a href="{esc(link)}"{ext}{cur}>{label}</a>'
        return label

    def ul(nodes):
        return '<ul>\n' + '\n'.join(li(c) for c in nodes) + '\n</ul>'

    def li(n):
        sub = '\n' + ul(n.children) + '\n' if n.children else ''
        return f'<li>{label_of(n)}{sub}</li>'

    out = []
    for n in root.children:
        if n.children:
            out.append(f'<h4>{label_of(n)}</h4>\n{ul(n.children)}')
        else:
            out.append(f'<p class="menu-item">{label_of(n)}</p>')
    return '\n'.join(out)


def breadcrumb_html(md, from_url, last=None):
    """パンくずリスト。md の章立てでの位置を、上の項目から順にたどる（PukiWiki の「Top(FrontPage)」と同じく、トップページでも出す）。
    md が None のページ（検索・404）は、last の題を最後に付ける"""
    chain = []
    n = PLACED.get(md)
    while n is not None and n.parent is not None:
        chain.append(n)
        n = n.parent
    chain.reverse()
    chain = [n for n in chain if n.md != 'index.md']
    items = []
    if md == 'index.md':
        items.append('<li>トップ</li>')
    else:
        items.append(f'<li><a href="{rel_url(from_url, "")}">トップ</a></li>')
        for n in chain:
            link = node_href(n, from_url) if n.md != md else None
            items.append(f'<li><a href="{esc(link)}">{esc(n.title)}</a></li>' if link else f'<li>{esc(n.title)}</li>')
        if last:
            items.append(f'<li>{esc(last)}</li>')
    return '<nav id="breadcrumb" aria-label="パンくずリスト">\n<ul>\n' + '\n'.join(items) + '\n</ul>\n</nav>\n'


# ---------------------------------------------------------------- Markdown → HTML

def resolve(src, href_):
    """原稿 src（_site_src/ からのパス）の中のリンク href の行き先。(行き先のパス, フラグメント) か None（外部・ページ内）"""
    if not href_ or href_.startswith(('#', '/', 'mailto:', 'tel:', 'javascript:')) or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', href_):
        return None
    path, _, frag = href_.partition('#')
    return posixpath.normpath(posixpath.join(posixpath.dirname(src), path)), frag


def rewrite_links(tree, src, from_url):
    for a in tree.iter('a'):
        r = resolve(src, a.get('href'))
        if not r:
            continue
        t, frag = r
        frag = '#' + frag if frag else ''
        if t in MD_PAGES:
            a.set('href', rel_url(from_url, page_url(t)) + frag)
        elif os.path.exists(os.path.join(RAW, t)) and t.endswith('.md'):
            # ページにならない生の原稿（サイトにも原稿のまま置かれる）
            a.set('href', rel_file(from_url, t) + frag)
        elif os.path.isfile(os.path.join(SRC, t)):
            a.set('href', rel_file(from_url, t) + frag)
        elif posixpath.join(t, 'index.md') in MD_PAGES:
            # startup/ のようなディレクトリへのリンクは、そのディレクトリの索引ページへ（GitHub ではファイルの一覧になる）
            a.set('href', rel_url(from_url, page_url(posixpath.join(t, 'index.md'))) + frag)
        else:
            error(f'{src}: リンク先 {a.get("href")} が無い')
    for img in tree.iter('img'):
        r = resolve(src, img.get('src'))
        if not r:
            continue
        if os.path.isfile(os.path.join(SRC, r[0])):
            img.set('src', rel_file(from_url, r[0]))
            img.set('loading', 'lazy')
        else:
            error(f'{src}: 画像 {img.get("src")} が無い')


def text_of(el):
    return re.sub(r'\s+', ' ', el.text_content()).strip()


def heading_text(el):
    """見出しの文字（末尾の † のリンクは除く）"""
    c = copy.deepcopy(el)
    for a in c.xpath('.//a[@class="anchor_super"]'):
        a.drop_tree()
    return text_of(c)


def nested_list(items):
    """[(見出しの深さ, リンクの HTML)] を、深さで入れ子にした ul にする"""
    out = ['<ul>']
    i = 0
    while i < len(items):
        level, link = items[i]
        i += 1
        sub = []
        while i < len(items) and items[i][0] > level:
            sub.append(items[i])
            i += 1
        out.append(f'<li>{link}{nested_list(sub) if sub else ""}</li>')
    out.append('</ul>')
    return '\n'.join(out)


def add_contents(tree, levels):
    """ページの先頭の目次（PukiWiki の div.contents）。最初の見出しの前に置く"""
    heads = [h for h in tree.iter('h2', 'h3') if h.get('id') and int(h.tag[1]) in levels]
    if len(heads) < 3:
        return
    items = [(int(h.tag[1]), f'<a href="#{esc(h.get("id"))}">{esc(heading_text(h))}</a>') for h in heads]
    box = lxml.html.fragment_fromstring('<div class="contents">\n' + nested_list(items) + '\n</div>')
    heads[0].addprevious(box)


def mark_index_grid(tree):
    """索引ページの長い一覧（ul）に class を付ける。CSS で 3 列のグリッド（狭いと 1 列）にする"""
    for ul in tree.findall('ul'):
        if len(ul) >= 9:
            ul.set('class', 'index-grid')


def render(md, from_url):
    text = read(os.path.join(SRC, md))
    html = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG, output_format='html').convert(text)
    tree = lxml.html.fragment_fromstring(html, create_parent='div')
    rewrite_links(tree, md, from_url)
    add_contents(tree, (2,) if md == 'index.md' else (2, 3))
    if md in GENERATED:
        mark_index_grid(tree)
    return tree


def inner_html(tree):
    out = (tree.text or '')
    out = esc(out) if out.strip() else ''
    for c in tree:
        out += etree.tostring(c, method='html', encoding='unicode')
    return out


def description_of(tree):
    for p in tree.iter('p'):
        t = text_of(p)
        if t:
            return t[:110] + ('…' if len(t) > 110 else '')
    return SITE_DESCRIPTION


def search_entries(tree, label, url):
    """検索の索引の行: [ページの名前, 節の題, サイトのルートからの URL, 本文]。節は H1〜H3 の区切り"""
    entries = []
    title, frag, buf = label, '', []

    def flush():
        text = ' '.join(buf).strip()
        if text or title:
            entries.append([label, title, url + ('#' + frag if frag else ''), re.sub(r'\s+', ' ', text)])

    for el in tree:
        if not isinstance(el.tag, str):
            continue
        if el.tag in ('h1', 'h2', 'h3'):
            flush()
            buf = []
            title = heading_text(el)
            frag = el.get('id', '')
        elif 'contents' not in (el.get('class') or '').split():
            buf.append(text_of(el).replace('†', ''))   # 節の中の見出し（H4 など）の † は、本文に混ぜない
    flush()
    return entries


# ---------------------------------------------------------------- 出力

def head_extra(url, page_title, description):
    """canonical・OGP・Twitter カード"""
    ogp = OGP.get(url, {})
    title = ogp.get('title', f'{page_title} - {SITE_NAME}' if url else SITE_NAME)
    description = ogp.get('description', description)
    full = SITE_URL + url
    out = f'<link rel="canonical" href="{esc(full)}">\n'
    out += (f'<meta property="og:type" content="{"article" if url else "website"}">\n'
            f'<meta property="og:site_name" content="{esc(SITE_NAME)}">\n'
            f'<meta property="og:title" content="{esc(title)}">\n'
            f'<meta property="og:description" content="{esc(description)}">\n'
            f'<meta property="og:url" content="{esc(full)}">\n'
            '<meta property="og:locale" content="ja_JP">\n')
    if 'image' in ogp:
        image = esc(SITE_URL + ogp['image'])
        out += (f'<meta property="og:image" content="{image}">\n<meta property="og:image:width" content="1200">\n'
                f'<meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">\n'
                f'<meta name="twitter:image" content="{image}">\n')
    else:
        out += '<meta name="twitter:card" content="summary">\n'
    out += f'<meta name="twitter:title" content="{esc(title)}">\n<meta name="twitter:description" content="{esc(description)}">\n'
    return out


def build_pages(root):
    if errors:
        return None
    template = string.Template(read(os.path.join(HERE, 'templates', 'page.html')))
    index = []
    pages = sorted(MD_PAGES)
    for md in pages:
        node = PLACED[md]
        url = page_url(md)
        tree = render(md, url)
        page_title, h1_id = take_title(tree, node.title)
        description = f'{node.title}の一覧' if md in GENERATED else description_of(tree)
        head = head_extra(url, page_title, description)
        content = inner_html(tree)
        write(posixpath.join(url, 'index.html'), template.substitute(
            title=esc(page_title if not url else f'{page_title} - {SITE_NAME}'), description=esc(description), head=head,
            root=root_of(url), home=rel_url(url, ''), body_attr='', **title_fields(page_title, h1_id),
            breadcrumb=breadcrumb_html(md, url), menu=menu_html(root, md, url), content=content))
        if md not in GENERATED:     # 自動で作る索引ページは、題の一覧でしかないので、検索の対象にしない
            index.extend(search_entries(tree, node.title, url))
    build_search_page(root, template)
    build_404(root, template)
    write('search-index.js', 'window.KAWARI_INDEX=' + json.dumps(index, ensure_ascii=False, separators=(',', ':')) + ';\n')
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          ''.join(f'<url><loc>{esc(SITE_URL + page_url(md))}</loc></url>\n' for md in pages) + '</urlset>\n')
    return pages


def take_title(tree, fallback):
    """本文の H1 を取り出して、ヘッダのページ名（PukiWiki の h1.title）にする。(題の文字, H1 の id)。
    H1 の id は、ヘッダの h1 に移す（#題 へのリンクを切らないため）"""
    h1 = tree.find('h1')
    if h1 is None:
        return fallback, None
    title, h1_id = heading_text(h1), h1.get('id')
    h1.drop_tree()
    return title, h1_id


def title_fields(page_title, h1_id=None):
    """page.html のヘッダのページ名"""
    return dict(page_title=esc(page_title), h1_attr=f' id="{esc(h1_id)}"' if h1_id else '')


def build_search_page(root, template):
    url = 'search/'
    content = ('<form id="search-form" action="./">\n<p><input id="search-q" name="q" type="search" size="30" autocomplete="off"> '
               '<button type="submit">検索</button></p>\n</form>\n<div id="search-results"></div>\n')
    write(url + 'index.html', template.substitute(
        title=esc(f'検索 - {SITE_NAME}'), description=esc(f'{SITE_NAME}の内部検索'), head='<meta name="robots" content="noindex">\n',
        root=root_of(url), home=rel_url(url, ''), body_attr='', **title_fields('検索'), breadcrumb=breadcrumb_html(None, url, last='検索'),
        menu=menu_html(root, None, url), content=content))


def build_404(root, template):
    # どの深さの URL で開かれるかわからないので、リンクはサイトのルートからの絶対パス（SITE_PATH）にする
    content = '<p>お探しのページは、移動したか、無くなったようです。左のメニューか、上の検索欄から探してください。</p>\n'
    write('404.html', template.substitute(
        title=esc(f'ページが見つかりません - {SITE_NAME}'), description='ページが見つかりません', head='<meta name="robots" content="noindex">\n',
        root=SITE_PATH, home=SITE_PATH, body_attr='', **title_fields('ページが見つかりません'), breadcrumb=breadcrumb_html(None, None),
        menu=menu_html(root, None, None), content=content))


def copy_static():
    """静的ファイル（CSS・JS・ヘッダの画像）、_site_src/ の .md 以外（assets/・attachment/・llms.txt・転送 HTML）、
    生の Markdown 原稿（llms.txt や INDEX.md の相対リンクを、サイト上でも辿れるようにする）を出力に置く"""
    shutil.copytree(STATIC, OUT, dirs_exist_ok=True)
    for base, _, names in os.walk(SRC):
        for name in names:
            if name.endswith('.md') or name in ('.nav.yml', GENERATED_LIST):
                continue
            rel = os.path.relpath(os.path.join(base, name), SRC)
            dst = os.path.join(OUT, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(os.path.join(base, name), dst)
    shutil.copytree(RAW, OUT, dirs_exist_ok=True)


MD_PAGES = set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-prepare', action='store_true', help='_site_src/ を作り直さない')
    args = ap.parse_args()
    if not args.no_prepare:
        prepare_site.main()
    cleanup_generated()
    for base, _, names in os.walk(SRC):
        for name in names:
            if name.endswith('.md'):
                MD_PAGES.add(os.path.relpath(os.path.join(base, name), SRC).replace(os.sep, '/'))
    if args.no_prepare:
        # まとめた元ページ（kis/set.md など）の行き先の表は、prepare_site.main() が作る。menu.yml が使うので、ここでも作る
        for d in prepare_site.GROUP_PAGES:
            prepare_site.register_groups(d, prepare_site.read_groups(d))
        for d in prepare_site.MERGED_DIRS:
            prepare_site.register_merged(d)
    root = load_menu()
    place_pages(root)
    if errors:
        sys.exit(f'ビルドに失敗: エラー {len(errors)} 件')
    write_generated()
    MD_PAGES.update(GENERATED)
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    copy_static()
    pages = build_pages(root)
    if pages is None or errors:
        sys.exit(f'ビルドに失敗: エラー {len(errors)} 件')
    print(f'{len(pages)} ページを {os.path.relpath(OUT)} に出力した')


if __name__ == '__main__':
    main()
