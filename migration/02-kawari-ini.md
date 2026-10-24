# kawari.ini消滅

kawari.iniは使えなくなりました。華和梨が読み込む全てのファイルは、単一の「華和梨辞書形式」になります。華和梨辞書形式では、「ゾーン切り替え」によって、辞書が読み込まれた瞬間にその場で直接実行されるKIS文を書けるようになっています。つまり、以前kawari.iniでしかできなかったことが、全ての辞書ファイルで可能になりました。

**華和梨Phase8が最初に読むファイルは「kawarirc.kis」になりました。**当然、これも普通の辞書ファイルです。

直接KISを書くゾーンに切り替えるには、そのゾーンを「`=kis`」のみの行と「`=end`」のみの行で囲います。

```
=kis


=end
```

従来の書式をPhase 8の書式で書き直すと以下のようになります。

```
# 従来
dict : dict-dms.txt
include : keeps.ini
adddict : author 偽Meister
set : myname 二葉亭四迷
text : spell necronomicon.txt
debug : log
randomseed : 100
security : 0
```

```
# Phase 8バージョン。
# KIS文を区切るためのセミコロンが必要なことに注意
# =kis ～ =endは、文法的には$( ～ )と全く完全に同じです。
=kis
# 辞書のロード
load dict-dms.txt;
# 全て辞書ファイルなので、loadコマンドのみです。
load keeps.ini;
# 文の追加
adddict author 偽Meister;
# 文のセット
set myname 二葉亭四迷;
# テキストファイルの読み込み(従来のtextloadと引数の順序が逆になっています!)
textload spell necronomicon.txt;
# ログをファイルに書き出します
logfile kawari.log;
## 以下のようにすると、起動時日付つきのファイルに書き出します
# logfile kawari-$(date %Y%m%d%H%M%S).log;
# ログに取るべきイベントや情報の種類を指定します
loglevel error warning info baseevents;
# 乱数の種の指定
srand 100;
# セキュリティレベルの指定(通常は必要ありません)
securitylevel low;
=end
```
