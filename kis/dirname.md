# dirname

**Category:** ファイル操作

## 書式

```
$(dirname パス名)
```

## 戻り値

正規化したディレクトリ名

## 解説

与えられたパス名をcncpathで正規化し、ディレクトリ名部分を抽出して返す。

## 使用例

```
=kis
# ここではMS Windows上のオリジナル華和梨を想定している

# "C:\Program Files\Microsoft Office\Office"が返る
dirname "C:/Program Files/Microsoft Office/Office/POWERPNT.EXE"
=end
```
