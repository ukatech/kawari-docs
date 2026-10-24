# isfile

**Category:** ファイル操作

## 書式

```
$(isfile パス名)
```

## 戻り値

パスが通常ファイルならば真、そうでなければ偽

## 解説

与えられたパス名が通常ファイルかどうか判定する。パスが通常ファイルならば真、そうでなければ偽を返す。パスのファイルが存在しない場合の動作は不定である。

## 使用例

```
=kis
# MATERIAのghost\masterフォルダで実行した場合を想定

isfile $(cncpath profile);
# ""が返る
isfile shiori.dll;
# 1が返る
=end
```
