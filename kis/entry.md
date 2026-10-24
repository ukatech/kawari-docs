# entry

**Category:** 補助機能

## 書式

```
$(entry エントリ名 単語1)
```

## 戻り値

`${エントリ名}`の結果、または単語1

## 解説

エントリからランダムに単語を選び、評価する。指定したエントリが空の場合、単語1を返す。単語1は省略可能。省略した時に指定したエントリが空の場合、空文字を返す。

evalでも同様のことが可能だが、entryの方が負荷が軽い。

## 使用例

```
=kis
entry "npw";
# ${npw}と同じ

entry "message."$(rand 3);
# ${message.0}から${message.2}のどれか

entry "system.OtherGhost" ${myname};
# ${system.OtherGhost}と同じ
# 空の場合は${myname}の戻り値が返る
=end
```
