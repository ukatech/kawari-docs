このリポジトリは伺かの SHIORI「華和梨（KAWARI）」のマニュアル（Markdown）です。
華和梨本体のソースは `../kawari`（`build/src`）にあります。
`../yaya-docs`（YAYA のマニュアル）と `../satori-docs`（里々の仕様書）の構成を手本にしています。

もとは `../kawari/document/` の HTML（`index.html` `start.html` `users.html` `kis_reference.html` など）で、これを記述要素ごとの Markdown に書き直したものです。`../kawari/document/` は廃止して削除したので、このリポジトリが華和梨マニュアルの正本です。更新履歴（`other/changelog.md`）も、版を上げるたびにここへ書きます。

## 書式

- UTF-8、LF
- コマンドページ（`kis/*.md`）は既存ページの見出し構成（書式 / 戻り値 / 解説 / 使用例）に合わせる。ファイル名はコマンド名（`?` だけは Windows のファイル名に使えないので `randomselect.md`）
- 対応バージョンは `Phase 9.0.0以降` のように書く。変更履歴が必要なときは解説の中に書く
- リンクは相対パスで `.md` まで書く（例: `[set](set.md)`、`[式](05-expressions.md#演算式)`）。見出しへのアンカーは GitHub と同じく日本語の見出しをそのまま使う
- 華和梨の記法は半角のまま書く（`${エントリ}` `$(echo hi)` `$[ 1 + 1 ]`）。コードブロックの言語指定はしない
- 見出しに番号は付けない（順序はファイル名の番号と `oldstyle/menu.yml` で決める）
- 名前に `_` を含むコマンド（`match_at` `regex_replace` など）は、コードスパンで囲む。コードスパンの外にある `_名前_` は `scripts/prepare_site.py` が警告する

## ページを追加・改名したとき

- `oldstyle/menu.yml` に加える。サイトの階層（左のメニュー・パンくずリスト・節の索引ページ）は、すべてこのファイルから作られ、並びもここで決まる。載っていないページがあると、ビルドが止まる（KIS コマンドの 1 コマンド 1 ファイルのページと、`grammar/` などの章のファイルは、まとめたページが載っていればビルドは通る。章はメニューにも並べてあるので、足したら加える）
- コマンドなら `kis/index.md` の「### 分類」の表に 1 回だけ載せ、ページの `**Category:**` 行を分類名と合わせる。サイトではこの分類ごとに 1 ページにまとめるため、載せ忘れや食い違いは `scripts/prepare_site.py` が止める。新しい分類を作ったら `prepare_site.py` の `GROUP_PAGES` にページ名（英字。コマンド名と重ならないもの）も加え、`oldstyle/menu.yml` にそのページ（`kis/<ページ名>.md`）を載せる
- 辞書操作の共通事項（`kis/dictcommon.md`）と正規表現の共通仕様（`kis/regex.md`）は、表ではなく本文の行からリンクする（分類ページの先頭に置かれる）
- `grammar/` `migration/` `spec/` は、章ごとのファイル（`NN-名前.md`、番号順）をサイトでは 1 ページにまとめる。章を足すときは番号を振り、`oldstyle/menu.yml` に加える
- 公開済みのページを改名したら、`scripts/prepare_site.py` の `REDIRECTS` に旧パスと新パスを加える（旧 URL に転送用の HTML を置く）
- 新しいディレクトリを作ったら、`scripts/prepare_site.py` の `DIRS`（または `MERGED_DIRS`）に加え、`oldstyle/menu.yml` に載せる

## 書き方の勘所

- 動作を書き換えるときは、`kosui` で実際に動かして確かめる（`../kawari` の `CLAUDE.md` に、ビルドとテストの手順がある）。例の出力は、実機で出たものを書く
- 辞書やスクリプトの例は、`=kis` ～ `=end` の中に書く文と、辞書定義ゾーンに書く文を取り違えない。`echo-mode > ` で始まる行は、幸水に入力した例と、その出力
- 構文コマンド（`if` `while` など）は引数を使うときに展開し、関数コマンドは引数を先に展開する。この違いは繰り返し説明する
- `document/` の HTML 由来の文面は、古い版（Phase 8.2.x）の記述が残っている。Phase 9 の変更（文字コード、`date` / `mktime` の 64bit、診断コード、`kosui --check` など）は、該当するページに反映する。変更は `../kawari/document/changelog.txt`（本リポジトリの `other/changelog.md`）が一次資料

## GitHub Pages

`main` に push すると GitHub Actions（`.github/workflows/pages.yml`）が `oldstyle/build.py` と `oldstyle/check.py` を走らせ、https://ukatech.shillest.net/kawari-docs/（リポジトリにカスタムドメインが設定されている。`ukatech.github.io/kawari-docs/` はここへ転送される）に公開する。ビルドは自前（Zensical・MkDocs は使わない。以前の Zensical 版は `old-zensical` ブランチに残してある。里々マニュアル `../satori-docs` の `oldstyle/` を移したもの）で、リンク切れ・アンカー切れがあると失敗する。ビルドの仕組みは [`oldstyle/README.md`](oldstyle/README.md)。原稿を書くうえで知っておくことは次のとおり。

- サイトの見た目と構造は、PukiWiki 1.5 の標準スキンを模している。上にヘッダ（左に 50x50 に縮めたアイコン、ページ名、その下にパンくずリスト。右上に検索欄と翻訳ボタン）、左に目次（`#menubar`）、右に本文（`#body`）。wiki の道具（ナビゲータ・ツールバー・最終更新・フッタ）は無い。HTML は HTML5 で、ヘッダ（区切りの横線まで）はスクロールしても画面の上端に残り、左のメニューはその下に残る（yaya-docs と同じ）。幅が 767px 以下ではヘッダは残さず、左のメニューはハンバーガーボタンで開く引き出しに畳む。JavaScript は検索（`search.js`）・翻訳ボタン（`translate.js`）・狭い画面のメニュー（`menu.js`）だけ
- ページの H1 は、本文ではなくヘッダのページ名（wiki の `h1.title`）になる。本文の見出しは H2 が帯、H3 が枠、H4 が左の太線（wiki と同じ）
- ページの URL は、Zensical 版と同じディレクトリ形式（`kosui/launch/` など）。外部からのリンクを切らないため、変えない。`file://` ではディレクトリのリンクが `index.html` を開かないので、手元では `python -m http.server -d _site` で見る
- 原稿はリポジトリ直下にあるため、`scripts/prepare_site.py` が `_site_src/` に写してからビルドする。その際 `INDEX.md` は `index.md`（トップページ）になり、`INDEX.md` へのリンクも書き換えられる。原稿内のリンク（`../kis/set.md` や `05-expressions.md#演算式` など）は、ビルドが出力先の相対パスに書き換える。行き先が無ければビルドが止まる
- コマンド（`kis/`）は、サイトでは `kis/index.md` の分類ごとの 1 ページ（`kis/dictionary/`、`kis/strings/` など）にまとめて出す。`index.md` 自体は手書きのまま 1 ページで出す。`grammar/` `migration/` `spec/` も、それぞれ 1 ページ（`grammar/` など）にまとめる。原稿は 1 ファイル 1 ページのまま書き、リンクも `../kis/set.md` や `05-expressions.md#演算式` と従来どおり書く（`prepare_site.py` がまとめたページの見出しへのリンクに書き換える。リンク先の見出しが無いとエラーで止まる）
- まとめた元ページの URL（`kis/set/` など）には、移動先へ飛ばすだけの HTML を `prepare_site.py` が置く。まとめたページでは、コマンド名（`dictcommon` と `regex` は、その節）が H2、コマンドの中の節（書式・戻り値など）が H4 で、見出しの id は `set`（ファイル名）、`set-書式` の形になる
- 各ページの先頭（最初の H2 の前）に、wiki の `#contents` にあたる目次を `oldstyle/build.py` が付ける（H2・H3 が 3 つ以上あるページ。トップページは H2 だけ）。まとめたページの目次はコマンド名だけになる。見出しの末尾の `†` は、その見出しへのリンク（wiki と同じ）
- サイトの階層の元は `oldstyle/menu.yml`（wiki の MenuBar に当たる、手で選んだ一覧。書き方はファイルの先頭に書いてある）ひとつだけ。左のメニュー、上のパンくずリスト、節の索引ページ（`startup/` `other/`）が、同じ木から作られる。最上位の項目は左のメニューで見出しになる。`index: startup/` と書いた項目には、下の項目を並べるだけの索引ページを、ビルドが自動で作る（原稿は無い。サイトには生の `index.md` も置かれる）。原稿のパスや `#見出し` が違う、載っていないページがある、とビルドが止まる
- `llms.txt`（AI エージェント向けの探し方の案内。`INDEX.md` と各ディレクトリの入口だけを書く）はサイトのルートに置かれる。ページごとの一覧は載せないので、ページを足しても直さなくてよい。ディレクトリを足したときは「構成」に 1 行足す
- 生の Markdown 原稿（`README.md` と `CLAUDE.md` 以外の `.md`）は、リポジトリと同じパスでサイトにも置かれる（`prepare_site.py` が `_raw/` に写し、ビルドが出力に重ねる）。`llms.txt` や `INDEX.md` の相対リンクは、このおかげでサイト上でも辿れる
- Markdown の拡張は `tables` `admonition` `attr_list` `md_in_html` `mdx_truly_sane_lists` `pymdownx.superfences` `toc`。見出しのアンカーは GitHub と同じく日本語のまま（`pymdownx.slugs.slugify(case='lower')`）で、`prepare_site.py` のリンク書き換えと同じ変換
- GitHub では表示できても Python-Markdown では崩れる書き方がある。段落の直後に空行なしで続くリストや表は `prepare_site.py` が空行を補うので、原稿は GitHub 向けのままでよい。表の中のコードスパンの `|` は GitHub 向けに `\|` と書く（`prepare_site.py` がサイト用に `|` へ戻す）。2 スペース字下げの入れ子リストは mdx_truly_sane_lists で扱える
- `${エントリ}` や `$(echo hi)` のような記法は、本文に書くときもコードスパンで囲む（囲まないと、`_` や `*` が強調として解釈される）
- 注意書きは `!!! note "タイトル"` / `!!! warning "タイトル"`（admonition）で書く
- 見た目は `oldstyle/static/style.css`（wiki の `skin/pukiwiki.css` の規則のうち使う分。寸法は wiki のまま。色はヘッダのアイコン（黒）に合わせて、wiki の青系の配色を灰色（ほんの少し青み）にしてある。リンクは彩度を落とした青 `#2e5a92`、訪問済みのリンクは彩度を落とした紫 `#6a4c8c`。note の青系の枠、warning の赤系の枠、検索語の強調の黄色は、色に意味があるので wiki に倣う。決め方は `style.css` の先頭に書いてある）。字は普通のゴシック（丸ゴシックにはしない）。ダークモードは無い。ヘッダのアイコンと favicon は `assets/logo.png`（300x300 の画像を 50x50 で表示）
- OGP / Twitter カードのタグは `oldstyle/build.py` が全ページに出す。ページごとのタイトル・説明・画像（1200x630 の PNG）は `build.py` の `OGP` に、ページの URL（`other/changelog/` のように末尾が `/`。トップは空文字）をキーにして書く（今は設定なし）
- 検索は、ビルド時に作る `search-index.js`（節ごとの本文）を、`search.js` が空白区切りの語の AND で部分一致検索する。ヘッダの検索欄に打ち込むとドロップダウンが出て、Enter で `search/?q=` に全件が並ぶ
- ヘッダに翻訳ボタンがある（`oldstyle/static/translate.js`。見た目は `style.css` の `.ukadoc-translate`）。ブラウザ組み込みの Translator API（Chrome 138 以降のデスクトップ版など）で、本文・左のメニュー・ページ名とパンくずリストを日本語から英語・中国語（繁体 `zh-Hant`・簡体 `zh`）へ機械翻訳する。API が無いブラウザではボタンを出さない。訳すのは日本語を含む文だけで、`code` `pre` `kbd` と `translate="no"` の中は訳さない。文はブロック（`p` `li` `td` など）の中の連なりを単位にまとめて訳し、リンク・太字・コードスパンは印（`<x1/>` `<a2>…</a2>`）に置き換えて訳してから元の要素へ戻す（印が崩れた文は断片ごとの訳に切り替える）。訳したくない語は原稿で `<span translate="no">…</span>` と囲める。読める程度の品質でよいとしている
- `sitemap.xml` と `404.html` もビルドが作る。404.html のリンクは、どの深さで開かれるかわからないので、サイトのルートからの絶対パス（`/kawari-docs/…`）

手元で確認するとき（`_site_src/` `_site/` `_raw/` は `.gitignore` 済み）:

```sh
pip install -r requirements.txt
python oldstyle/build.py    # prepare_site.py で _site_src/ を作り、_site/ に出力する（--no-prepare で作り直さない）
python oldstyle/check.py    # 出力のリンク切れ・アンカー切れ・画像の切れ・検索の索引の URL を調べる（エラーが 0 件であること）
python -m http.server -d _site    # http://127.0.0.1:8000/ でプレビュー
```
