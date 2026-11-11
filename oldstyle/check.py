r"""出力（_site/）の内部リンク・アンカー・画像・スクリプト・CSS・フォームの宛先・検索の索引の切れを調べる（旧 zensical build --strict の代わり）。

    python oldstyle/check.py

エラーは出力 HTML のパスで出る。見つかれば終了コード 1。外部リンク（http: など）は見ない。
"""
import json
import os
import posixpath
import re
import sys
from urllib.parse import unquote, urlsplit

import lxml.html

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
SITE = os.path.join(ROOT, '_site')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import prepare_site  # noqa: E402

SITE_PATH = urlsplit(prepare_site.SITE_URL).path   # /kawari-docs/（404.html が使う、ルートからの絶対パス）
EXTERNAL = re.compile(r'^(?:[A-Za-z][A-Za-z0-9+.-]*:|//)')


def main():
    if not os.path.isdir(SITE):
        sys.exit('_site/ が無い。先に python oldstyle/build.py を実行する')
    pages = {}
    for base, _, names in os.walk(SITE):
        for name in names:
            if name.endswith('.html'):
                rel = os.path.relpath(os.path.join(base, name), SITE).replace(os.sep, '/')
                tree = lxml.html.parse(os.path.join(base, name)).getroot()
                ids = {e.get('id') for e in tree.iter() if isinstance(e.tag, str) and e.get('id')}
                ids |= {e.get('name') for e in tree.iter('a') if e.get('name')}
                pages[rel] = (tree, ids)
    errors = 0

    def resolve(rel, ref):
        """ページ rel の中の参照 ref の行き先 (サイト内のパス, フラグメント)。サイト外なら None"""
        if not ref or EXTERNAL.match(ref):
            return None
        path, _, frag = ref.partition('#')
        if path.startswith(SITE_PATH):
            target = path[len(SITE_PATH):]                   # 404.html のようにルートからの絶対パスで書いたもの
        elif path.startswith('/'):
            return None
        elif path:
            target = posixpath.normpath(posixpath.join(posixpath.dirname(rel), unquote(path)))
        else:
            target = rel
        if target in ('', '.') or target.endswith('/'):
            target = posixpath.join(target if target != '.' else '', 'index.html')
        if os.path.isdir(os.path.join(SITE, target)):
            target = posixpath.join(target, 'index.html')
        return target, frag

    def verify(where, ref, label):
        nonlocal errors
        r = resolve(where, ref)
        if r is None:
            return
        target, frag = r
        if not os.path.exists(os.path.join(SITE, target)):
            print(f'{where}: {label} {ref} の行き先が無い')
            errors += 1
        elif frag and target in pages and unquote(frag) not in pages[target][1]:
            print(f'{where}: {ref} のアンカーが無い')
            errors += 1

    for rel, (tree, _) in sorted(pages.items()):
        for e in tree.iter():
            if not isinstance(e.tag, str):
                continue
            if e.tag in ('a', 'link') and e.get('href') is not None:
                verify(rel, e.get('href'), f'<{e.tag}>')
            elif e.tag in ('img', 'script', 'source') and e.get('src') is not None:
                verify(rel, e.get('src'), f'<{e.tag}>')
            elif e.tag == 'form' and e.get('action') is not None:
                verify(rel, e.get('action'), '<form>')
    # 検索の索引（search-index.js）の URL は、サイトのルートからの相対パス。search.js がルートの接頭辞を付けて使う
    index_path = os.path.join(SITE, 'search-index.js')
    if os.path.exists(index_path):
        with open(index_path, encoding='utf-8') as f:
            body = f.read()
        entries = json.loads(body[body.index('=') + 1:].rstrip().rstrip(';'))
        for _, _, url, _ in entries:
            verify('search-index.js', url, '索引の URL')
        print(f'検索の索引 {len(entries)} 件の URL を調べた')
    else:
        print('search-index.js が無い')
        errors += 1
    print(f'{len(pages)} ページを調べた。エラー {errors} 件')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
