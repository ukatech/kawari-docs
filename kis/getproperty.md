# getproperty

**Category:** 本体との連携

## 書式

```
getproperty プロパティ名 [ 既定値 ]
```

## 戻り値

プロパティの値。取得できなかったときは既定値(省略時は空文字列)

## 解説

本体(SSPなど)のプロパティシステムから値を取得する(Phase 9.0.0 β2以降)。本体にSSTPの`EXECUTE`で`GetProperty`を送る。プロパティ名の仕様は、本体のドキュメント(SSPならUKADOCのプロパティシステム)を参照。

応答コードが200のときだけ値を返し、それ以外は既定値を返す。存在しないプロパティ(204)、本体のウィンドウがまだ分からないとき、本体が5秒以内に応答しなかったときも既定値になる。応答コードは`System.SSTP.ResponseCode`で確かめられる([executesstp](executesstp.md)を参照)。

送り先は、本体からのNOTIFY`hwnd`で知るので、Windowsでは本体がSHIORI/3.0でNOTIFYを送る環境で使える。ninixではFMOからUNIXソケットを探す。SecurityLevelがlocal以外のリクエストの処理からは送らない。

## 使用例

```
sentence : 現在のゴーストは$(getproperty currentghost.name 不明)です。
```
