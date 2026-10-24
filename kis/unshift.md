# unshift

**Category:** 辞書操作

## 書式

```
$(unshift エントリ1 単語1)
```

## 戻り値

なし

## 解説

エントリ1の先頭に単語1を挿入する。

## 使用例

```
ghosts : まゆら,理夢,毒子,白子,美耳,陽子
任意 : さくら

=kis
get ghosts;
# 「まゆら理夢毒子白子美耳陽子」を返す

unshift ghosts "${任意}";

get ghosts;
# 「さくらまゆら理夢毒子白子美耳陽子」を返す
=end
```
