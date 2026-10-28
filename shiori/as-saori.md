# SAORIモジュールとしての華和梨

華和梨はSHIORI規格の準AIモジュールですが、同時にSAORI規格モジュールでもあります。SAORIモジュールとして使うと、

- 華和梨Phase 7から移行する際、新旧スクリプトを同時に使える
- 他の栞を使用している場合でも、華和梨の欲しい機能だけを使える

といったメリットがあります。

華和梨をSAORIとして使うとき、次の3つのことに注意します。

## 引数の受け取り

華和梨がSAORIとして呼ばれた時、`System.Callback.OnSaoriExecute`エントリを評価します。他のコールバックエントリと同様、所属する全ての単語を評価します。この時、SAORIモジュールに与えられた引数は、`System.Request.*`以下、`System.Request.Argument0`、`System.Request.Argument1`等のエントリに存在します。

引数が何個あるか等を知りたい場合、listtreeコマンドを使い、

```
listtree arguments System.Request
```

として、argumentsエントリを調べると知ることが出来ます。

## 戻り値の引渡し

戻り値を返したい時はコミュニケートと同様、`System.Response.*`エントリ群を使います。SAORI規格に従って、戻り値は、`System.Response.Result`に書き込みます。以下、`System.Response.Value0`、`System.Response.Value1`、`System.Response.Value2`等のエントリに補助情報を書き込みます。

## ステータス

戻り値を返すには、実はこれだけでは不十分です。`System.Resopose`エントリに、ステータスを書き込む必要があります。このステータスコードを見て、SAORIモジュールを呼び出した側は処理の成功/失敗を判断する為、必須情報です。主なステータスコードは次の通りです。

| ステータス | 意味 |
|---|---|
| 200 | 引数を正しく理解し、戻り値を書き込んだ |
| 204 | 引数は正しく理解したが、戻り値がない |
| 400(省略時デフォルト) | 理解できない引数が来た |

なお、`System.Callback.OnSaoriExecute`の評価結果は、ステータスと無関係です。この点が他のコールバックエントリと違いますので、注意が必要です

```
System.Callback.OnSaoriExecute : $(
    if $[ ${System.Request.Argument0} == "処理1" ] $(
        SAORI処理1;
    ) else if $[ ${System.Request.Argument0} == "処理2" ] $(
        SAORI処理2;
    );
  )

# SAORI処理をわざわざ関数にする必然性はないのだが…
# 新機軸に見慣れて貰うために、あえて関数で記述した。
# 普通にエントリとして書いても何の問題もない。
# 引数はSystem.Request.*に存在し、関数の引数として与える必要がないから。

=kis
function SAORI処理1 $(
    if $[ ${System.Request.Argument1} == "貢物" ] $(
        # Resultのみ返す例
        setstr System.Response.Result "うむ、よろしい！";
        setstr System.Response 200;
    ) else $(
        # ResultとValue*を併用する例
        setstr System.Response.Result "貢物はどうした！";
        setstr System.Response.Value0 "文句";
        setstr System.Response.Value1 "不満";
        setstr System.Response.Value2 $(date %y%m%d);
        setstr System.Response 200;
    );
);

function SAORI処理2 $(
    if $[ ${System.Request.Argument1} == "1" ] $(
        # Resultなしだが正常終了の例
        setstr System.Response 204;
    ) else $(
        # 異常終了の例
        setstr System.Response 400;
    );
);
=end
```
