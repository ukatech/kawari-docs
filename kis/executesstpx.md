# executesstpx

**Category:** 本体との連携

## 書式

```
executesstpx 追加データ格納エントリ コマンド [ 引数 引数 ... ]
```

## 戻り値

応答の追加データの1行目(executesstpと同じ)

## 解説

[executesstp](executesstp.md)と同じだが、追加データの全行を、指定したエントリに1行1単語で格納する(エントリはいったん空になる)。`GetNames`のように複数行を返すコマンド向け。行数は`size`コマンドで得られる。

## 使用例

```
=kis
executesstpx names GetNames;
# namesエントリにインストール済みのゴースト名が入る
=end
```
