# eval

**Category:** 補助機能

## 書式

```
$(eval 単語1 ...)
```

## 戻り値

デコード結果

## 解説

与えられた全引数中の`${}`、`$()`等を再度再帰的に評価し、展開結果を返す。再帰的評価を行う以外はechoと同じ。

## 使用例

```
kawari     : 華和梨
nise       : 偽
shiori     : 栞
niseshiori : ${nise}${shiori}

=kis
eval "理夢の偽AIは${kawari}です";
# 「理夢の偽AIは華和梨です」が返る

eval "奈留の偽AIは${niseshiori}です";
# 「奈留の偽AIは偽栞です」が返る
=end
```

**参考**

```
=kis
echo "奈留の偽AIは${niseshiori}です";
# 「奈留の偽AIは${niseshiori}です」が返る
=end
```
