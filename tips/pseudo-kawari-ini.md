# 疑似kawari.ini

ゴースト定義辞書ファイルを読むのに、いちいちloadコマンドを並べるのは癪だという方は、kawarirc.kisに以下の記述を行うことで、従来のkawari.iniと同じようにdictに辞書ファイル名を書けます。

```
# kawarirc.kis内サンプル
=kis
load kawari.ini;
foreach @f dict $( load ${@f} );
=end
```

```
# kawari.iniサンプル
dict : dict-word.txt
dict : dict-game.txt
```
