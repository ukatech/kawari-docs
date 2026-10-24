# clear

**Category:** 辞書操作

## 書式

```
$(clear エントリ1)
```

## 戻り値

なし

## 解説

エントリ1から単語を削除する。

エントリ名の指定には、[辞書操作コマンド共通の書式](dictcommon.md)を利用できる。

## 使用例

```
test1 : word1, word2, word3

=kis
foreach @word test1 $(echo ${@word})
# 「word1word2word3」を返す

clear test1;
# test1エントリの内容を全て消去

foreach @word test1 $(echo ${@word})
# 何も返さない
=end
```
