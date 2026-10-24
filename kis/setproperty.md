# setproperty

**Category:** 本体との連携

## 書式

```
setproperty プロパティ名 値
```

## 戻り値

なし

## 解説

本体のプロパティシステムに値を設定する(Phase 9.0.0 β2以降)。本体にSSTPの`EXECUTE`で`SetProperty`を送る。送り先や条件は[getproperty](getproperty.md)と同じ。応答コードは`System.SSTP.ResponseCode`に入る。値を空にはできない(SSPは空の値を受け取らず、400になる)。

## 使用例

```
# オーナードローメニューの「シェル」から、masterシェルを隠す
sentence : $(setproperty "currentghost.shelllist(master).menu" hidden)
```
