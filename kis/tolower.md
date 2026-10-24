# tolower

**Category:** 文字列操作

## 書式

```
$(tolower 文字列1 ...)
```

## 戻り値

文字列中のアルファベット大文字を小文字に置換した結果

## 解説

文字列中のアルファベット大文字を小文字に置換する。半角文字のみに作用する。

## 使用例

```
=kis
tolower ABC def;
# 「abc def」が返る

tolower ＸＹＺ XYZ;
# 「ＸＹＺ xyz」が返る
=end
```
