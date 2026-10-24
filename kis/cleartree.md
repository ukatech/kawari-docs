# cleartree

**Category:** 辞書操作

## 書式

```
$(cleartree エントリ1)
```

## 戻り値

なし

## 解説

「エントリ1.」で名前が始まるエントリの内容を全て削除する。例えば「エントリ1.a」、「エントリ1.b」というエントリがあったとすると、これらの内容が削除される。

## 使用例

```
ghost1.name : まゆら
ghost1.shiori : 華和梨
ghost1.shiori.phase : 7.3.1
ghost1.author : 夢蛍
ghost1.shell : サンタ,着せ替え,白,夏服

=kis
cleartree ghost1;
=end
# 上記エントリの内容は全て削除される
```
