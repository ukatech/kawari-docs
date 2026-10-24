# echo

**Category:** 出力

## 書式

```
$(echo 単語1 ...)
```

## 戻り値

全引数を空白文字で接続したもの

## 解説

与えられた全引数を、空白文字で区切って返す。

## 使用例

```
=kis
echo 1 2 3 4 5;
# 「1 2 3 4 5」が返る

setstr test1 "TEST";
echo ${test1};
# 「TEST」が返る
=end
```
