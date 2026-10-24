# listsub

**Category:** 辞書操作

## 書式

```
$(listsub エントリ1 エントリ2)
```

## 戻り値

なし

## 解説

「エントリ2.」で名前が始まり、それ以上「.」が含まれないエントリ名の一覧を、エントリ1に追加する。エントリ2に「.」を指定すると、最上位(「.」を全く含まない)エントリ名の一覧が得られる。

## 使用例

```
ghost1.name : まゆら
ghost1.shiori : 華和梨
ghost1.shiori.phase : 7.3.1
ghost1.author : 夢蛍
ghost1.shell : サンタ,着せ替え,白,夏服

=kis
listsub 一覧 ghost1;

getcode 一覧;
# "ghost1.name""ghost1.shiori""ghost1.author""ghsot1.shell"が返る。
```
