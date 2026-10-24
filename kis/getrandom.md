# getrandom

**Category:** 辞書操作

## 書式

```
$(getrandom エントリ1 単語1)
```

## 戻り値

エントリ1の単語のいずれか、または単語1

## 解説

エントリ1の単語をランダムに1つ選択し、評価結果を返す。エントリ1に単語が無かった場合、単語1を返す。機能はentryとまったく同じである。

## 使用例

```
=kis
getrandom "npw";
# ${npw}と同じ

getrandom "message."$(rand 3);
# ${message.0}から${message.2}のどれかと同じ

getrandom "System.OtherGhost" ${myname};
# ${System.OtherGhost}と同じ
# 結果が空の場合は、${myname}の戻り値が返る
=end
```
