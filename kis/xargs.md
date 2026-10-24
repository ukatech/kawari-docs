# xargs

**Category:** 補助機能

## 書式

```
$(xargs 引数エントリ コマンド1 ...)
```

## 戻り値

コマンド1の実行結果

## 解説

引数エントリの内容を添え字順に展開して、コマンド1の引数として与える。コマンド1の後に書いた引数は、引数エントリの展開内容より前方に付加する。コマンド1の実行結果が戻り値となる。

エントリ名の指定には、[辞書操作コマンド共通の書式](dictcommon.md)を利用できる。

## 使用例

```
SaveEntries : HighScore , Life , 喋り頻度 , 好感度 , 最終更新日

RecommendSites : "伺か" , "http://sakura.mikage.to" , "-"
RecommendSites : "まゆら" , "http://mayura.jp/" , "-"
RecommendSites : "-" , "-" , "-"
RecommendSites : "華和梨" , "http://kawari.sf.net/" , "-"

keyword1 : 華和梨 , SHIORI , ゴースト

=kis
xargs SaveEntries save parameter.txt;
# SaveEntriesの内容を展開してsaveコマンドを実行。
# 「save parameter.txt HighScore Lige 喋り頻度 好感度 最終更新日」
# を実行した場合と等価。

xargs RecommendSites urllist;
# urllistコマンドにRecommendSitesエントリの内容を展開して与える

xargs keyword1 matchall ${System.Request.Reference0};
# keyword1エントリの全ての単語がReference0にマッチしたら真を返す
=end
```
