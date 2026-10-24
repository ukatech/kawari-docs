# toupper

**Category:** 文字列操作

## 書式

```
$(toupper 文字列1 ...)
```

## 戻り値

文字列中のアルファベット小文字を大文字に置換した結果

## 解説

文字列中のアルファベット小文字を大文字に置換する。半角文字のみに作用する。

## 使用例

```
=kis
toupper ABC def;
# 「ABC DEF」が返る

toupper ｘｙｚ xyz;
# 「ｘｙｚ XYZ」が返る
=end
```
