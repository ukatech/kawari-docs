# KIS リファレンス

## 概要

華和梨インラインスクリプト(KIS : Kawari Inline Script)は、華和梨の辞書ファイル中で使用できる簡易言語です。インラインスクリプトを使用することにより、華和梨実行中に辞書へ単語を追加したり、本体から通知されるイベントに応じた処理を行ったりすることができます。

## 書式

インラインスクリプトは、単語中に「`$(～)`」で囲んで記述します。一つの「`$(～)`」で囲まれた塊を、「インラインスクリプトブロック」と呼びます。一つのブロックの中には、複数の文を記述できます。文と文の間は「`;`」(セミコロン)で区切ります。一つの文は、一つのコマンドと零個以上の引数から構成されます。コマンド、セミコロン、各引数の間は、それぞれ一つ以上の空白で区切ります。

```
インラインスクリプト:
  ブロック

ブロック:
  $(文)
  $(文 ; 文 ; …)

文:
  コマンド名 引数1 引数2 …
```

## 評価、戻り値、真偽の判定

ブロックがイベント呼び出し、発話要求等を通じて華和梨に解釈されることを、「評価」と呼びます。ブロックは評価されると、「戻り値」を返します。戻り値は一つの文字列で、どのような戻り値を返すかはコマンドによって異なります。コマンドによっては、つねに「""」(空文字列)を返すこともあります。

ブロックが複数の文から成る場合、ブロックの戻り値は、ブロック中の全ての文の戻り値を順に繋げたものです。なお、ブロックから戻り値を返したくない場合、[silent](silent.md)コマンドを使用すれば抑制できます。

華和梨が戻り値を評価し、ブール代数における「真」か「偽」かを判定する際、次のような基準で判定します。

- 空文字列「""」、文字列「"0"」、文字列「"false"」ならば「偽」
- 「偽」以外ならば「真」("ほげ"、"1"、"true"、" "(空白)...)

この真偽の判定は、後述する構文コマンド、関数コマンド問わず共通です。コマンドを独自に追加する場合、真偽の判定はこの基準に合わせて下さい。

## コマンドの種類

コマンドは大きく分けて、[if](if.md)コマンドや[while](while.md)コマンドのような「構文コマンド」と、[adddict](adddict.md)コマンドや[date](date.md)コマンドのような「関数コマンド」の二つに分類できます。構文コマンドは与えられた条件の真偽に従い、処理の流れを制御します。一方、関数コマンドは与えられた引数に従い、実際の処理を行います。[注1](#構文コマンドと関数コマンドの違い) [注2](#インラインスクリプトに渡される引数の数)

混同する恐れの無い場合、構文コマンドは「構文」、関数コマンドは単に「コマンド」と呼ぶことがあります。

## 構文コマンドと関数コマンドの違い

構文と関数の、実用上最も重要な違いは、

- 構文の評価は引数評価以前に行われる
- 関数の評価は引数評価以後に行われる

という点です。引数評価以前は、引数は「`${npw}`」や「`$(echo Hello)`」等の「書いたまま」の状態です。一方、引数評価以後は、引数は展開されて、「カルロス・ゴーン」や「Hello」等の「文字列だけ」の状態となります。引数が通常の文字列だけである場合はさほど問題になりませんが、引数に[set](set.md)コマンド等の、戻り値よりも機能が目的となるコマンドがあった場合、この差が意味を持つことになります。

```
true : 真です。$(set tmp OK)
# 下記の二つは、表示上は恐らく同じ結果だが…
$(entry true ${cond})      # true文はcondが不成立でも実行されてしまう。
$(if ${cond} else ${true}) # true文はcondが不成立なら実行されない。
```

## インラインスクリプトに渡される引数の数

コマンドに引数を与える時、エントリ呼び出しで与える場合を考えます。

```
$(echo $(entry ${EntryName}) "Hello")
```

このケースで、EntryNameエントリに何もセットされていない場合を考えます。この場合、echoコマンドの第1引数は""で、第2引数が「Hello」になります。第1引数が「Hello」ということはありません。インラインスクリプトに渡される引数の数と位置は、エントリ解釈の前に確定します。

## コマンド一覧

### 構文コマンド

| コマンド | 説明 |
|---|---|
| [`if`](if.md) | 条件判断 |
| [`foreach`](foreach.md) | 指定エントリ中のすべての単語に対しコマンド実行 |
| [`loop`](loop.md) | 指定回数ループ |
| [`silent`](silent.md) | ブロックの出力を抑制 |
| [`until`](until.md) | 条件が成立するまでループ |
| [`while`](while.md) | 条件が成立している間ループ |
| [`break`](break.md) | ループからの脱出 |
| [`continue`](continue.md) | ループ先頭に戻る |
| [`NULL`](NULL.md) | 空文字列 |
| [`?`](randomselect.md) | ランダム選択 |
| [`function`](function.md) | 関数定義 |
| [`lambda`](lambda.md) | 無名関数の定義 |
| [`rmfunc`](rmfunc.md) | ユーザ定義関数の削除 |
| [`return`](return.md) | 関数からの脱出 |

### 辞書操作

辞書操作コマンドに共通の特徴は、[辞書操作コマンド共通事項](dictcommon.md)を参照してください。

| コマンド | 説明 |
|---|---|
| [`set`](set.md) | エントリに単語をセット |
| [`setstr`](setstr.md) | エントリに文字列をセット |
| [`adddict`](adddict.md) | エントリに単語を追加 |
| [`adddictstr`](adddictstr.md) | エントリに文字列を追加 |
| [`push`](push.md) | エントリに単語を追加 |
| [`pushstr`](pushstr.md) | エントリに文字列を追加 |
| [`unshift`](unshift.md) | エントリの先頭に単語を挿入 |
| [`unshiftstr`](unshiftstr.md) | エントリの先頭に文字列を挿入 |
| [`insert`](insert.md) | エントリ内の指定した位置に単語を挿入 |
| [`insertstr`](insertstr.md) | エントリ内の指定した位置に文字列を挿入 |
| [`get`](get.md) | エントリ中の単語を得る |
| [`getcode`](getcode.md) | エントリを評価せずに参照 |
| [`getrandom`](getrandom.md) | エントリ中のいずれかの単語を得る |
| [`pop`](pop.md) | エントリ最後尾の単語を返し、エントリから削除 |
| [`popcode`](popcode.md) | エントリ最後尾の単語を評価せずに返し、エントリから削除 |
| [`shift`](shift.md) | エントリ先頭の単語を返し、エントリから削除 |
| [`shiftcode`](shiftcode.md) | エントリ先頭の単語を評価せずに返し、エントリから削除 |
| [`clear`](clear.md) | エントリから単語を削除 |
| [`cleartree`](cleartree.md) | エントリツリーから単語を削除 |
| [`size`](size.md) | エントリ中の単語数を数える |
| [`find`](find.md) | エントリ中の単語の最初の位置を得る |
| [`rfind`](rfind.md) | エントリ中の単語の最後の位置を得る |
| [`copy`](copy.md) | エントリ内容のコピー |
| [`copytree`](copytree.md) | エントリ内容をエントリ構造ごとコピー |
| [`move`](move.md) | エントリ内容の移動 |
| [`movetree`](movetree.md) | エントリ内容をエントリ構造ごと移動 |
| [`listsub`](listsub.md) | サブエントリのリストを得る |
| [`listtree`](listtree.md) | エントリツリー全体のリストを得る |
| [`writeprotect`](writeprotect.md) | エントリを書き込み不可にする |

### ファイル操作

| コマンド | 説明 |
|---|---|
| [`save`](save.md) | エントリをファイルに保存 |
| [`savecrypt`](savecrypt.md) | エントリをファイルに暗号化して保存 |
| [`load`](load.md) | 華和梨形式辞書ファイルを読み込む |
| [`textload`](textload.md) | テキストファイルを読み込む |
| [`textappend`](textappend.md) | テキストファイルを追記 |
| [`textsave`](textsave.md) | テキストファイルを保存 |
| [`textload_charset`](textload_charset.md) | 文字コードを指定してテキストファイルを読み込む |
| [`textappend_charset`](textappend_charset.md) | 文字コードを指定してテキストファイルを追記 |
| [`textsave_charset`](textsave_charset.md) | 文字コードを指定してテキストファイルを保存 |
| [`readdir`](readdir.md) | ディレクトリを読み込む |
| [`cncpath`](cncpath.md) | パス名をシステムで使えるようにする |
| [`dirname`](dirname.md) | パス名からディレクトリ名部分を切り出す |
| [`filename`](filename.md) | パス名からファイル名部分を切り出す |
| [`isexist`](isexist.md) | 指定ファイルが存在するか判定する |
| [`isdir`](isdir.md) | 指定ファイルがディレクトリか判定する |
| [`isfile`](isfile.md) | 指定ファイルが通常ファイルか判定する |

### カウンタ

| コマンド | 説明 |
|---|---|
| [`dec`](dec.md) | 指定エントリの単語を数字と見なし減算する |
| [`inc`](inc.md) | 指定エントリの単語を数字と見なし加算する |

### 文字列操作

| コマンド | 説明 |
|---|---|
| [`length`](length.md) | 文字列の長さを得る |
| [`match`](match.md) | ある部分文字列が現れる最初の位置を得る |
| [`rmatch`](rmatch.md) | ある部分文字列が現れる最後の位置を得る |
| [`match_at`](match_at.md) | ある部分文字列が指定位置に存在するか否か判定する |
| [`substr`](substr.md) | 部分文字列を得る |
| [`char_at`](char_at.md) | 指定位置の文字を得る |
| [`sub`](sub.md) | マッチする最初の文字列を置き換える |
| [`gsub`](gsub.md) | マッチする全ての文字列を置き換える |
| [`rsub`](rsub.md) | マッチする最後尾の文字列を置き換える |
| [`tr`](tr.md) | 文字を置き換える |
| [`reverse`](reverse.md) | 文字列を逆順にする |
| [`tolower`](tolower.md) | アルファベットを小文字にする |
| [`toupper`](toupper.md) | アルファベットを大文字にする |
| [`chr`](chr.md) | 指定した文字コードの一文字を返す |
| [`split`](split.md) | 文字列を区切り文字で分解 |
| [`join`](join.md) | 区切り文字で文字列を結合 |
| [`compare`](compare.md) | 文字列を比較する |

### 正規表現

正規表現コマンド共通の仕様(パターン・オプション・サブルーチン呼び出し)は、[正規表現コマンド共通の仕様](regex.md)を参照してください。

| コマンド | 説明 |
|---|---|
| [`regex_match`](regex_match.md) | 正規表現にマッチするか調べる |
| [`regex_find`](regex_find.md) | 正規表現にマッチする最初の位置を得る |
| [`regex_findall`](regex_findall.md) | 正規表現にマッチする部分すべてをエントリに格納する |
| [`regex_count`](regex_count.md) | 正規表現にマッチする個数を数える |
| [`regex_replace`](regex_replace.md) | マッチする全ての部分を正規表現で置き換える |
| [`regex_replace_first`](regex_replace_first.md) | マッチする最初の部分だけを正規表現で置き換える |
| [`regex_erase`](regex_erase.md) | マッチする全ての部分を削除する |
| [`regex_erase_first`](regex_erase_first.md) | マッチする最初の部分だけを削除する |
| [`regex_split`](regex_split.md) | 正規表現にマッチする部分で文字列を分解する |
| [`regex_escape`](regex_escape.md) | 正規表現の特殊文字をエスケープする |

### SAORI

| コマンド | 説明 |
|---|---|
| [`saoriregist`](saoriregist.md) | SAORIを登録する |
| [`saorierase`](saorierase.md) | SAORIの登録を解除する |
| [`saorilist`](saorilist.md) | 登録中のSAORI一覧を返す |
| [`callsaori`](callsaori.md) | 登録したSAORIを呼び出す |
| [`callsaorix`](callsaorix.md) | 登録したSAORIを呼び出す(高機能版) |

### 本体との連携

| コマンド | 説明 |
|---|---|
| [`getproperty`](getproperty.md) | 本体のプロパティシステムから値を取得する |
| [`setproperty`](setproperty.md) | 本体のプロパティシステムに値を設定する |
| [`executesstp`](executesstp.md) | 本体にSSTPのEXECUTEを送る |
| [`executesstpx`](executesstpx.md) | 本体にSSTPのEXECUTEを送る(追加データをエントリに格納) |

### コミュニケート機能

| コマンド | 説明 |
|---|---|
| [`communicate`](communicate.md) | あるエントリの全ての単語を評価し、値から一つをランダムで選ぶ |
| [`matchall`](matchall.md) | 全てのキーワードに対してマッチング |

### 出力

| コマンド | 説明 |
|---|---|
| [`echo`](echo.md) | 引数を空白文字で接続して返す |
| [`encode_entryname`](encode_entryname.md) | エントリ名に使用できる名前に変換 |
| [`escape`](escape.md) | 引数内のさくらスクリプトをエスケープする |

### 補助機能

| コマンド | 説明 |
|---|---|
| [`entry`](entry.md) | エントリを呼び出す |
| [`entrycount`](entrycount.md) | エントリ総数を返す |
| [`eval`](eval.md) | 単語を再評価 |
| [`urllist`](urllist.md) | SHIORI/2.5形式のおすすめリストを出力する |
| [`wordcount`](wordcount.md) | 単語総数を返す |
| [`xargs`](xargs.md) | 引数を展開して実行する |

### その他

| コマンド | 説明 |
|---|---|
| [`rccharset`](rccharset.md) | メッセージ文字セット設定 |
| [`date`](date.md) | 日時を指定フォーマットで返す |
| [`mktime`](mktime.md) | 日時を通算経過秒数に変換する |
| [`getenv`](getenv.md) | 環境変数の内容を返す |
| [`help`](help.md) | KISコマンドオンラインヘルプ |
| [`logfile`](logfile.md) | ログファイルを指定する |
| [`loglevel`](loglevel.md) | ログに取る種類を決める |
| [`logprint`](logprint.md) | ログに出力する |
| [`debugger`](debugger.md) | 幸水デバッガのON/OFF |
| [`rand`](rand.md) | ランダムな整数を返す |
| [`srand`](srand.md) | 乱数の種を設定する |
| [`securitylevel`](securitylevel.md) | セキュリティレベルの指定 |
| [`ver`](ver.md) | バージョン番号取得 |
