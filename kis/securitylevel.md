# securitylevel

**Category:** その他

## 書式

```
$(securitylevel レベル指定)
```

## 戻り値

なし

## 解説

セキュリティレベルを指定する。以下の値を設定できる。

| 値 | 意味 |
|---|---|
| 0 / low | 全てのイベントを許可する。 |
| 1 / middle | 外部からやってきたイベントを禁止。 |
| 2 / high | 当面は1(middle)と同じ。 |
| 3 / ultrahigh | 明確にローカルマシン発行と記されたイベントのみ許可。 |

なお、securitylevelコマンドは、ゴースト初期化中のみ、一回だけ実行可能である。

## 使用例

```
=kis
# 低レベルに設定
securitylevel low;
=end
```
