# join

**Category:** 文字列操作

## 書式

```
$(join エントリ1 区切り文字)
```

## 戻り値

結合後の文字列

## 解説

エントリ1の内容を、区切り文字を間に挟んで順に結合して返す。結合の際、エントリ1の内容は順に評価される。

区切り文字は省略可能で、省略した場合はヌル文字「""」をした場合と同じ。

## 使用例

```
path : WINDOWS, SYSTEM32, drivers, etc
=kis
join path "\\";
# 「WINDOWS\SYSTEM32\drivers\etc」が返る
=end
```
