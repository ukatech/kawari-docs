# expr, test消滅

exprコマンド、testコマンドは削除され、新たに「演算式」が書けるようになりました。演算式は`$[ ～ ]`という書式になります。基本的にはexprの機能を引き継いだものです。

幸水の表記で演算式をいくつか示します：

```
echo-mode > $[4*(10+2)]
48
echo-mode > $[${npw.special}||${npw}]
龍太郎
echo-mode > $["伺か"=~"何か"]
false
```

演算式中では、以前のexprやtestが持っていた全ての演算記号に限らず、常識的な演算記号は全て使えます。testの持っていた、-gtや-ltと言った演算子はなくなり、exprのように文字列と数値は自動判別されるようになりました。

```
# 従来
event.OnMusicPlay: $(if $([ ${freeze} -eq 0 ]) ${OnMusicPlay1})

# Phase 8
event.OnMusicPlay: $(if $[${freeze}==0] ${OnMusicPlay1})
# こう書くこともできます
event.OnMusicPlay: $(if $[!${freeze}] ${OnMusicPlay1})
```

`$[ ～ ]`の中では自由に空白・改行を入れられます。空白が全く無くてもかまいません。

`( ～ )`によるグルーピングができます。exprでは、閉じかっこのみクォートが必須という仕様でしたが、演算式では普通に式が書けます。

ただし、exprの`'|'、'&'`は、それぞれ、`'||'、'&&'`になりました。比較などに**文字列を使う場合は、必ずクォートしなければならなくなりました。** exprの持っていたsubstr, lengthなどの演算機能(サブコマンド)は、独立したKISコマンドとして再定義されました。

数値についてはexpr, testと同様、**整数しか使えません。**また、**数値と見なせるものは強制的に数値扱いになります。**どうしても文字列として比較を行いたい場合は、KISのcompareコマンドを使ってください。

```
# 従来
OnMusicPlay1: $(if $([ $(expr substr ${system.Reference0} 2 6) != "Buffer" ]) ${OnMusicPlay2})

# Phase 8
OnMusicPlay1: $(if $[$(substr ${system.Reference0} 2 6)!="Buffer"] ${OnMusicPlay2})
```
