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
- 見出しに番号は付けない（順序はファイル名の番号と `.nav.yml` で決める）
- 名前に `_` を含むコマンド（`match_at` `regex_replace` など）は、コードスパンで囲む。コードスパンの外にある `_名前_` は `scripts/prepare_site.py` が警告する

## ページを追加・改名したとき

- `INDEX.md` の該当する表に追加する
- コマンドなら `kis/index.md` の「### 分類」の表に 1 回だけ載せ、ページの `**Category:**` 行を分類名と合わせる。サイトではこの分類ごとに 1 ページにまとめるため、載せ忘れや食い違いは `scripts/prepare_site.py` が止める。新しい分類を作ったら `prepare_site.py` の `GROUP_PAGES` にページ名（英字。コマンド名と重ならないもの）も加える
- 辞書操作の共通事項（`kis/dictcommon.md`）と正規表現の共通仕様（`kis/regex.md`）は、表ではなく本文の行からリンクする（分類ページの先頭に置かれる）
- `grammar/` `migration/` `spec/` は、章ごとのファイル（`NN-名前.md`、番号順）をサイトでは 1 ページにまとめる。章を足すときは番号を振り、`INDEX.md` に加える
- 公開済みのページを改名したら、`scripts/prepare_site.py` の `REDIRECTS` に旧パスと新パスを加える（旧 URL に転送用の HTML を置く。Zensical は mkdocs-redirects を使えないため）
- 新しいディレクトリを作ったら、`.nav.yml` の `nav` と `scripts/prepare_site.py` の `DIRS`（または `MERGED_DIRS`）に加える。ディレクトリ内の並びは、そのディレクトリの `.nav.yml` で決める

## 書き方の勘所

- 動作を書き換えるときは、`kosui` で実際に動かして確かめる（`../kawari` の `CLAUDE.md` に、ビルドとテストの手順がある）。例の出力は、実機で出たものを書く
- 辞書やスクリプトの例は、`=kis` ～ `=end` の中に書く文と、辞書定義ゾーンに書く文を取り違えない。`echo-mode > ` で始まる行は、幸水に入力した例と、その出力
- 構文コマンド（`if` `while` など）は引数を使うときに展開し、関数コマンドは引数を先に展開する。この違いは繰り返し説明する
- `document/` の HTML 由来の文面は、古い版（Phase 8.2.x）の記述が残っている。Phase 9 の変更（文字コード、`date` / `mktime` の 64bit、診断コード、`kosui --check` など）は、該当するページに反映する。変更は `../kawari/document/changelog.txt`（本リポジトリの `other/changelog.md`）が一次資料

## GitHub Pages

`main` に push すると GitHub Actions（`.github/workflows/pages.yml`）が Zensical（Material for MkDocs の後継。Material テーマ互換）でビルドし、https://ukatech.shillest.net/kawari-docs/（リポジトリにカスタムドメインが設定されている。`ukatech.github.io/kawari-docs/` はここへ転送される）に公開する。ビルドは `zensical build --strict` で、リンク切れ・アンカー切れがあると失敗する。

- 原稿はリポジトリ直下にあるため、`scripts/prepare_site.py` が `_site_src/` に写してからビルドする。その際 `INDEX.md` は `index.md`（トップページ）になり、`INDEX.md` へのリンクも書き換えられる
- コマンド（`kis/`）は、サイトでは `kis/index.md` の分類ごとの 1 ページ（`kis/dictionary/`、`kis/strings/` など）にまとめて出す。`index.md` 自体は手書きのまま 1 ページで出す。`grammar/` `migration/` `spec/` も、それぞれ 1 ページ（`grammar/` など）にまとめる。原稿は 1 ファイル 1 ページのまま書き、リンクも `../kis/set.md` や `05-expressions.md#演算式` と従来どおり書く（`prepare_site.py` がまとめたページの見出しへのリンクに書き換える。リンク先の見出しが無いとエラーで止まる）
- まとめた元ページの URL（`kis/set/` など）には、移動先へ飛ばすだけの HTML を `prepare_site.py` が置く。まとめたページでは、コマンド名（`dictcommon` と `regex` は、その節）が H2、コマンドの中の節（書式・戻り値など）が H4 で、見出しの id は `set`（ファイル名）、`set-書式` の形になる。右の目次は `toc_depth: 3` によりコマンド名だけになる
- `llms.txt`（AI エージェント向けの探し方の案内。`INDEX.md` と各ディレクトリの入口だけを書く）はサイトのルートに置かれる。ページごとの一覧は載せないので、ページを足しても直さなくてよい。ディレクトリを足したときは「構成」に 1 行足す
- 生の Markdown 原稿（`README.md` と `CLAUDE.md` 以外の `.md`）は、リポジトリと同じパスでサイトにも置かれる。`scripts/prepare_site.py` が `_raw/` に写し、workflow がビルド後に `_site` へ重ねる（zensical は `.md` をページにしてしまうので、`_site_src/` には置けない）。`llms.txt` や `INDEX.md` の相対リンクは、このおかげでサイト上でも辿れる
- 設定は `mkdocs.yml` をそのまま読ませている。左メニューの章立ては `.nav.yml`（mkdocs-awesome-nav）、各ページの名前は H1 から決まる
- ヘッダの色は `mkdocs.yml` の `theme.palette` の `primary`（現在は black）で決まる。ロゴと favicon は `assets/logo.png`（`../kawari/document/images/logo.png` と同じもの）
- GitHub では表示できても MkDocs（Python-Markdown）では崩れる書き方がある。段落の直後に空行なしで続くリストや表は `prepare_site.py` が空行を補うので、原稿は GitHub 向けのままでよい。表の中のコードスパンの `|` は GitHub 向けに `\|` と書く（`prepare_site.py` がサイト用に `|` へ戻す）。2 スペース字下げの入れ子リストは mdx_truly_sane_lists で扱える
- `${エントリ}` や `$(echo hi)` のような記法は、本文に書くときもコードスパンで囲む（囲まないと、`_` や `*` が強調として解釈される）
- 注意書きは `!!! note "タイトル"` / `!!! warning "タイトル"`（admonition）で書く
- Zensical は 0.0.x の版を固定している（`requirements.txt`）。Material for MkDocs は 2026-11-05 にサポート終了のため移行した（MkDocs 2.0 はプラグインや Material テーマと互換性が無い）
- Zensical のテンプレートは MiniJinja で、`page.file` や `page.is_homepage` が無い。`overrides/main.html` はページの URL（`page.url`）で判定し、ページ別の OGP は `extra.ogp` に URL をキーにして書く（今は設定なし）
- 見た目は `theme.variant: classic` で従来のまま。Zensical の既定は新デザインの modern

手元で確認するとき（`_site_src/` と `_site/` は `.gitignore` 済み）:

```sh
pip install -r requirements.txt
python scripts/prepare_site.py
zensical build --strict    # 警告（リンク切れ・アンカー切れ）が出ないことを確認する
zensical serve             # http://127.0.0.1:8000/kawari-docs/ でプレビュー
```
