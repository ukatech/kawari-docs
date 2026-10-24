# isexist

**Category:** ファイル操作

## 書式

```
$(isexist パス名)
```

## 戻り値

パスが存在すれば真、そうでなければ偽

## 解説

与えられたパス名が存在するかどうか判定する。パスが存在すれば真、そうでなければ偽を返す。

## 使用例

```
=kis
# MATERIAのghost\masterフォルダで実行した場合を想定

isexist $(cncpath profile);
# 1が返る
isexist shiori.dll;
# 1が返る
isexist $(cncpath ..\..\..\..\embryo.exe);
# ""が返る
=end
```
