# filename

**Category:** ファイル操作

## 書式

```
$(filename パス名)
```

## 戻り値

ファイル名

## 解説

与えられたパス名をcncpathで正規化し、ファイル名部分を抽出して返す。

## 使用例

```
=kis
# ここではMS Windows上のオリジナル華和梨を想定している

# "POWERPNT.EXE"が返る
filename "C:/Program Files/Microsoft Office/Office/POWERPNT.EXE"
=end
```
