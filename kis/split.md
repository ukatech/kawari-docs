# split

**Category:** 文字列操作

## 書式

```
$(split エントリ1 文字列1 区切り文字列1)
```

## 戻り値

なし

## 解説

文字列1を区切り文字列1で分割し、エントリ1に格納する。エントリ1の以前の内容はそのまま残り、新たに格納される文は、エントリ1にpushされる。

区切り文字1は省略可能で、省略した場合は文字列1を文字ごとに分割する。

## 使用例

```
=kis
split string "AA:BB:CC" ":";
# AA、BB、CCに分割

split Header ${System.GhostEx} $(chr 1);
# GhostExヘッダをバイト値1で分割

split Msg "籠の中の鳥" "の";
# 籠、中、鳥に分割

split test "1ch2ch3ch" "ch";
# 1、2、3に分割

split char "世界よ、こんにちは！";
# "世界よ、こんにちは！"を文字ごとに分割
=end
```
