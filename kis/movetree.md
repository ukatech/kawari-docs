# movetree

**Category:** 辞書操作

## 書式

```
$(movetree エントリ1 エントリ2)
```

## 戻り値

なし

## 解説

「エントリ1.」で名前が始まるエントリの構造を、エントリ2に移す。例えば「エントリ1.a」、「エントリ1.b」というエントリがあったとすると、それぞれの内容を「エントリ2.a」、「エントリ2.b」エントリにコピーする。その後エントリ1.a、エントリ1.b等を削除する。

## 使用例

```
ghost1.name : まゆら
ghost1.shiori : 華和梨
ghost1.shiori.phase : 7.3.1
ghost1.author : 夢蛍
ghost1.shell : サンタ,着せ替え,白,夏服

=kis
movetree ghost1 ghost2;
=end
# 「ghost2.」で始まるエントリの内容が、次のようになる
# ghost2.name : まゆら
# ghost2.shiori : 華和梨
# ghost2.shiori.phase : 7.3.1
# ghost2.author : 夢蛍
# ghost2.shell : サンタ,着せ替え,白,夏服
```
