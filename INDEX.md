# 華和梨マニュアル

伺か（ukagaka）の SHIORI「華和梨（KAWARI）」のマニュアルです。華和梨の辞書の書き方、インラインスクリプト（KIS）のコマンド、コンソール版の幸水、仕様書をまとめています。

*To hack, or not to be... That is the Program!!*

<p align="center"><img src="assets/logo.png" width="300" height="300" alt='MULTI PURPOSE SHIORI SYSTEM "KAWARI"'></p>

> 「ですくとっぷ戦線ニ異常アリ」 — *"SOMETHING IS WRONG WITH THE DESKTOP FRONT."* （[ストーリー](other/story.md)）

間違いやわかりにくいところを見つけたら、[整備班BTS](https://bts.shillest.net/)（報告フォーム）で教えてください。GitHub に慣れている方は、[Issues](https://github.com/ukatech/kawari-docs/issues) や Pull Request でも構いません。

## ダウンロード・ソース

- [華和梨のリポジトリ（kawari）](https://github.com/ukatech/kawari)
- [ダウンロード（GitHub Releases）](https://github.com/ukatech/kawari/releases)

## はじめての方へ

- 華和梨って何？ → [華和梨とは](startup/what-is-kawari.md)
- はじめて華和梨でゴーストを作りたい → [導入ガイド](startup/getting-started.md)
- 華和梨 8（8.2.x）を使っていて Phase 9 に移りたい → [華和梨 8 から Phase 9 への乗り換え](migration/00-from-phase8.md)（`shiori.dll` を差し替えるだけで動きます）
- 華和梨 7 以前を使っていた → [移行ガイド](migration/01-overview.md)

## 調べたいとき

- 辞書の書き方を知りたい → [文法](grammar/01-dictionary-files.md)
- イベントや SAORI の扱いを知りたい → [SHIORI/SAORI インターフェース](shiori/index.md)
- KIS のコマンドを調べたい → [KIS リファレンス](kis/index.md)
- 幸水で動作確認・デバッグをしたい → [幸水](kosui/index.md)
- 機能を組むサンプルが見たい → [ヒント集](tips/index.md)
- エラーメッセージを調べたい → [エラーメッセージ一覧](other/error-messages.md)

ページ上部の検索窓からも探せます。

## 配布条件

本プログラムはフリーソフトウェアであり、修正BSDライセンスに基づいて再配布可能です。詳しくは[ライセンス](other/license.md)を御覧下さい。

---

## はじめに (startup/)

| ファイル | 内容 |
|---------|------|
| [what-is-kawari.md](startup/what-is-kawari.md) | 華和梨とは |
| [getting-started.md](startup/getting-started.md) | 導入ガイド（Getting Started） |

---

## 文法 (grammar/)

ユーザーズマニュアルにあたる、辞書の書き方の解説です。

| ファイル | 内容 |
|---------|------|
| [00-introduction.md](grammar/00-introduction.md) | ユーザーズマニュアルの読み方 |
| [01-dictionary-files.md](grammar/01-dictionary-files.md) | 辞書ファイル（コメント・セキュリティレベル・暗号化辞書） |
| [02-entry-definition.md](grammar/02-entry-definition.md) | エントリ定義（文と文字列・クォート文字列・ブロック・複数行対応） |
| [03-substitution.md](grammar/03-substitution.md) | 置換とエントリ呼び出しと実行 |
| [04-entry-call-variations.md](grammar/04-entry-call-variations.md) | エントリ呼び出しのバリエーション（集合演算式・エントリ配列呼び出し・履歴参照・一時エントリ） |
| [05-expressions.md](grammar/05-expressions.md) | 演算式 |
| [06-inline-script.md](grammar/06-inline-script.md) | インラインスクリプト（構文コマンドと関数コマンド・if・ユーザ定義コマンド） |

---

## SHIORI/SAORI インターフェース (shiori/)

| ファイル | 内容 |
|---------|------|
| [index.md](shiori/index.md) | SHIORI/SAORI インターフェース |
| [callbacks.md](shiori/callbacks.md) | コールバック |
| [system-entries.md](shiori/system-entries.md) | その他のシステムエントリ |
| [as-shiori.md](shiori/as-shiori.md) | 栞としての華和梨 |
| [as-saori.md](shiori/as-saori.md) | SAORI モジュールとしての華和梨 |
| [saori-register.md](shiori/saori-register.md) | SAORI モジュールの使用宣言 |
| [saori-call.md](shiori/saori-call.md) | SAORI モジュール呼び出し |
| [events.md](shiori/events.md) | イベント |
| [communicate.md](shiori/communicate.md) | コミュニケート |
| [random-talk.md](shiori/random-talk.md) | 自発トーク |

---

## KIS コマンド (kis/)

コマンドは 1 コマンド 1 ファイルです。サイトでは分類ごとのページにまとまって表示されます。一覧は [kis/index.md](kis/index.md) にあります。

| 分類 | 内容 |
|------|------|
| 構文コマンド | `if` `foreach` `loop` `while` `until` `function` `lambda` など |
| 辞書操作 | `set` `adddict` `get` `size` `copy` など（[共通事項](kis/dictcommon.md)） |
| ファイル操作 | `save` `load` `textload` `readdir` など |
| カウンタ | `inc` `dec` |
| 文字列操作 | `length` `substr` `sub` `split` `join` など |
| 正規表現 | `regex_match` `regex_replace` など（[共通の仕様](kis/regex.md)） |
| SAORI | `saoriregist` `callsaori` など |
| 本体との連携 | `getproperty` `setproperty` `executesstp` など |
| コミュニケート機能 | `communicate` `matchall` |
| 出力 | `echo` `escape` `encode_entryname` |
| 補助機能 | `entry` `eval` `xargs` など |
| その他 | `date` `mktime` `rand` `loglevel` `securitylevel` など |

---

## 幸水 (kosui/)

| ファイル | 内容 |
|---------|------|
| [index.md](kosui/index.md) | 幸水（kosui）とは |
| [launch.md](kosui/launch.md) | 起動方法（オプション・各モード） |
| [check-mode.md](kosui/check-mode.md) | 検査モード（`--check`） |
| [operation.md](kosui/operation.md) | 操作方法と終了方法 |
| [debugging.md](kosui/debugging.md) | 幸水を使ったデバッグの指針 |

---

## ヒント集 (tips/)

| ファイル | 内容 |
|---------|------|
| [index.md](tips/index.md) | ヒント集の一覧 |
| [pseudo-kawari-ini.md](tips/pseudo-kawari-ini.md) | 疑似 kawari.ini |
| [story-talk.md](tips/story-talk.md) | ストーリートーク |
| [non-overlap-call.md](tips/non-overlap-call.md) | エントリの重複回避呼び出し |
| [sequential-call.md](tips/sequential-call.md) | エントリの順序呼び出し |
| [communicate-helpers.md](tips/communicate-helpers.md) | コミュニケートコマンドの改善 |
| [char-type.md](tips/char-type.md) | 簡易文字種判別 |
| [notify-handling.md](tips/notify-handling.md) | SHIORI/3.0 NOTIFY 処理 |
| [debug-support.md](tips/debug-support.md) | デバッグ支援スクリプト |

---

## 移行ガイド (migration/)

| ファイル | 内容 |
|---------|------|
| [00-from-phase8.md](migration/00-from-phase8.md) | 華和梨 8 から Phase 9 への乗り換え |
| [01-overview.md](migration/01-overview.md) | Phase 7 以前からの移行ガイド |
| [02-kawari-ini.md](migration/02-kawari-ini.md) | kawari.ini 消滅 |
| [03-system-entries.md](migration/03-system-entries.md) | システムエントリ整理/イベントエントリ統合 |
| [04-match-entries.md](migration/04-match-entries.md) | マッチエントリ消滅 |
| [05-piro.md](migration/05-piro.md) | 内蔵 piro 消滅 |
| [06-history-reference.md](migration/06-history-reference.md) | 履歴参照ルールが小変更 |
| [07-expr-test.md](migration/07-expr-test.md) | expr, test 消滅 |
| [08-if-syntax.md](migration/08-if-syntax.md) | if 文の文法変更 |
| [09-enumerate.md](migration/09-enumerate.md) | enumerate 消滅 |
| [10-get-set.md](migration/10-get-set.md) | get/set の動作変更 |
| [11-other-commands.md](migration/11-other-commands.md) | その他の KIS コマンドの変更 |
| [12-multiline.md](migration/12-multiline.md) | 複数行対応 |

---

## 仕様書 (spec/)

華和梨ハッカー、ミドルウェアベンダ、互換系・KIS 開発者向けの仕様書です。

| ファイル | 内容 |
|---------|------|
| [00-introduction.md](spec/00-introduction.md) | KIS プログラミングリファレンス（はじめに） |
| [01-what-is-kawari.md](spec/01-what-is-kawari.md) | 華和梨とは何か？ |
| [02-semantics.md](spec/02-semantics.md) | 華和梨言語仕様 |
| [03-syntax.md](spec/03-syntax.md) | 華和梨文法 |
| [04-external-interfaces.md](spec/04-external-interfaces.md) | 外部インターフェース |
| [05-roadmap.md](spec/05-roadmap.md) | ロードマップ |
| [06-bnf.md](spec/06-bnf.md) | 文法仕様（EBNF） |

---

## その他 (other/)

| ファイル | 内容 |
|---------|------|
| [error-messages.md](other/error-messages.md) | エラーメッセージ一覧 |
| [license.md](other/license.md) | 華和梨のライセンスについて |
| [source-overview.md](other/source-overview.md) | 華和梨ソース概略 |
| [adding-kis-commands.md](other/adding-kis-commands.md) | インラインスクリプトの追加方法 |
| [changelog.md](other/changelog.md) | 更新履歴（ChangeLog） |
| [story.md](other/story.md) | ストーリー（STORY） |

---

## 関連リンク

- [華和梨公式配布サイト（GitHub）](https://ukatech.github.io/kawari/)
- [「あれ以外の何か以外の何か」掲示板](http://hpcgi1.nifty.com/creative-s/meister/wforum.cgi)
- [華和梨を使い倒す？](http://homepage1.nifty.com/creative-s/kawarisp/)

華和梨開発チーム: NAKAUE.T (Meister)、偽Meister (夢乃)、さとー、酔狂、さくらのにえ
