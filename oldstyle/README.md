# oldstyle: PukiWiki の見た目を模した静的サイト

PukiWiki 1.5 の標準スキン（`skin/pukiwiki.css`。見出しの字間・左のメニューの幅 18em などの手直しを加えたもの）の見た目と構造を（色は、wiki の青系の配色を灰色（ほんの少し青み）にしたもの）、このリポジトリの Markdown 原稿から再現する自前のビルド。里々マニュアル（`../satori-docs` の `oldstyle/`）を移したもので、仕組みは同じ。Zensical・MkDocs は使わない（以前の Zensical 版は `old-zensical` ブランチ）。見た目だけを真似て、HTML は HTML5。wiki の道具（ナビゲータの編集・差分・一覧などのリンク、ツールバー、最終更新、最新の 10 件、フッタ）は載せない。ヘッダのページの URL の代わりにパンくずリストを出し、右上に検索欄と翻訳ボタンを足している。

```sh
python oldstyle/build.py              # scripts/prepare_site.py で _site_src/ を作り、_site/ に出力する
python oldstyle/build.py --no-prepare # _site_src/ を作り直さない
python oldstyle/check.py              # _site/ の内部リンク（ファイル・アンカー・画像・スクリプト・フォーム・検索の索引）を調べる
python -m http.server -d _site        # プレビュー（ディレクトリ形式の URL なので、file:// では見られない）
```

必要なもの: `pip install -r requirements.txt`（`Markdown` `pymdown-extensions` `mdx_truly_sane_lists` `lxml` `PyYAML`）。

## 作り

| 場所 | 内容 |
|---|---|
| `build.py` | `menu.yml` から階層（左のメニュー・パンくずリスト・索引ページ）を作り、原稿 → HTML → wiki の構造に組む。リンク・画像のパスは出力先からの相対パスに書き換え、行き先が無ければエラーで止まる。`search-index.js` `sitemap.xml` `404.html` `search/` も作る |
| `static/` | `style.css`（wiki の `skin/pukiwiki.css` の規則のうち使う分）、`menu.js`（狭い画面のメニューの引き出しと、ヘッダの高さの測定）、`search.js`（サイト内検索）、`translate.js`（ブラウザ組み込みの Translator API による翻訳ボタン）。ビルドで出力のルートにそのまま置く。ヘッダのアイコンと favicon は `../assets/logo.png`（300x300 の画像を 50x50 で表示） |
| `menu.yml` | サイトの階層の定義（wiki の MenuBar に当たる）。`title:` と `page:`（原稿のパス。`INDEX.md#見出し` や、まとめた元の `grammar/05-expressions.md` や `kis/set.md` も可）か `index:`（自動で作る索引ページの URL）か `url:`、入れ子の `children:`、メニューに出さないページを下に置く `list:`。書き方はファイルの先頭 |
| `templates/page.html` | 1 ページの HTML5 の枠（`$title` などを `string.Template` で埋める） |
| `check.py` | 出力のリンク・アンカー・画像・フォームの宛先・検索の索引の URL の検査（旧 `zensical build --strict` の代わり。CI でも走る） |
| `../scripts/prepare_site.py` | 原稿を `_site_src/` に写して整える（KIS コマンドの分類ごとの束ね、文法・移行ガイド・仕様書の束ね、転送 HTML、空行補い、`_raw/`） |

## ページの構造

```
body[data-root]
  header#header     … a#site-logo（img#logo。50x50 のアイコン、左に float）、#search（検索欄 + 翻訳ボタン。右に float）、
                      #site-title（h1.title = ページ名、nav#breadcrumb）、hr.full_hr（ヘッダと一緒に上端に残す）
  div#contents      … flex。HTML では本文が先で、order で左右を入れ替える（wiki と同じ）
    main#body       … 本文（先頭に div.contents の目次）
    nav#menubar     … 左のメニュー（menu.yml の最上位の項目が h4、その下の children: が入れ子の ul。いま開いているページは太字）
```

- ページの URL は、Zensical 版と同じディレクトリ形式（`kosui/launch/` など）。リンクと静的ファイルのパスは、ページの深さに応じた相対パス（`../../style.css` など）。`<body data-root>` が、サイトのルートへの相対パス
- 原稿の H1 は本文から取り除いて、ヘッダの `h1.title` にする（H1 の id もそちらへ移す）。本文の見出しは H2 が帯、H3 が枠、H4 が左の太線で、wiki の `*` `**` `***` と同じ見た目
- ヘッダ（`#header`）と左のメニュー（`#menubar`）は `position: sticky` で、スクロールしてもヘッダは画面の上端に、メニューはその下に残る（yaya-docs と同じ）。ヘッダの高さはパンくずリストの折り返しで変わるので、`menu.js` が測って CSS の `--header-h` に入れる（メニューの位置と、`#` アンカーで飛んだ見出しの `scroll-padding-top` に使う）。メニューが画面より長いときは、メニューの中だけをスクロールする
- 幅が 767px 以下（wiki と同じ）では、ヘッダは上端に残さず、検索欄はページ名の上に回り、メニューは畳む。検索欄の左に `menu.js` がボタン（ハンバーガー）を置き、押すとヘッダの下からメニューが引き出し（ドロワー）として出る（暗幕・Esc・メニューの中のリンクで閉じる。yaya-docs と同じ）。`menu.js` は head で同期に読み込み、`<html>` に `js-drawer` を付ける。CSS はこのときだけメニューを畳むので、JavaScript が動かなければ、従来どおり本文 → メニューの縦並びになる。幅の広い表と `pre` は、その中だけを横にスクロールする
- 階層の元は menu.yml だけ。パンくずリストは、そのページが menu.yml で最初に出てくる項目から、親をたどって作る。ページが menu.yml のどこにも（`children:` にも `list:` にも）載っていないと、ビルドが止まる
- `index:` を書いた項目の索引ページ（`startup/` `other/`）は、ビルドが `children:` と `list:` のページを並べた Markdown を `_site_src/` と `_raw/` に書いて作る（`_site_src/.generated` に記録し、`--no-prepare` のときの消し残しを防ぐ）。検索の索引には入れない。9 件以上の一覧は、`ul.index-grid` として 3 列のグリッドにする
- 見出しの末尾の `†` は、その見出しへのリンク。ページ先頭の `div.contents` は、H2・H3 の目次
- OGP は `build.py` の `OGP`（今はページ別の設定なし）
- 翻訳ボタン（`translate.js`）は、`#search` の中に置かれる。訳す範囲は `#site-title`（ページ名・パンくずリスト）、`#body`、`#menubar`
