# debugger

**Category:** その他

## 書式

```
$(debugger on)
$(debugger off)
```

## 戻り値

なし

## 解説

起動中のゴーストに、[幸水](../kosui/index.md)からの接続を許すかどうかを決める。引数に「on」を指定すると、接続可能になる。「off」を指定すると接続不可になる。接続可能な場合、`System.Debugger`エントリに「`on`」という文が定義される。

## 使用例

```
=kis
# 幸水にてデバッグ中
debugger on;
=end
```
