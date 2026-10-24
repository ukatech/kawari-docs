# コールバック

華和梨が情報のやり取りのため、特別扱いするエントリを「システムエントリ」と呼びます。このうち、幾つかのエントリは呼び出す際の仕組みが、他のエントリとまったく違います。この節では、このシステムエントリの中でも特異な、「コールバックエントリ」を説明します。

コールバックエントリとは、本体がイベント、NOTIFYを通知してきた際、最初に評価するエントリです。通常のエントリを評価する場合、エントリ中の文を一つランダムに選び、その文の評価結果をエントリの評価結果とします。一方、コールバックエントリが本体から呼ばれた場合、コールバックエントリ中の**すべての文を添え字順に**評価し、**すべての評価結果を結合したもの**を本体に返します。仮に、`System.Callback.OnGET`エントリが、次のような内容だったとします。

```
System.Callback.OnGET : \0
System.Callback.OnGET : \s[0]
System.Callback.OnGET : 阿。
System.Callback.OnGET : \1
System.Callback.OnGET : \s[10]
System.Callback.OnGET : 吽。
System.Callback.OnGET : \e
```

もしこのコールバックエントリが本体から呼ばれたとすると、本体に返すスクリプトは次のようになります。

```
\0\s[0]阿。\1\s[10]吽。\e
```

この結果は、KISコマンドの[get](../kis/get.md)を使い、次のように書いた結果と等価です。コールバックエントリは、**コールバックエントリをgetで評価した結果を本体に返す**と考えて下さい。

```
get System.Callback.OnGET
```

このコールバックエントリの動作は、主にミドルウェアの記述を簡素化する際に有効でしょう。ミドルウェアは`OnSecondChange`イベント等で、多数の独立した機能を動作させることがあります。従来、この独立動作する機能を追加したい場合、必然的にミドルウェアを書き換える必要がありました。しかし、今回からは`System.Callback.*`エントリに、追加機能を呼ぶ文を追加するだけで大丈夫です。

次に、華和梨の使う全コールバックエントリを示します。

| エントリ | 呼ばれるとき |
|---|---|
| **SHIORI/3.0** |  |
| `System.Callback.OnGET` | GET |
| `System.Callback.OnNOTIFY` | NOTIFY |
| **SHIORI/2.x** |  |
| `System.Callback.OnEvent` | SHIORI/2.2 イベント応答、GET Sentenceのみ |
| `System.Callback.OnGetSentence` | SHIORI/2.3b コミュニケート |
| `System.Callback.OnGetStatus` | ステータス取得 |
| `System.Callback.OnResource` | SHIORI/2.5リソース取得 |
| **SAORI/1.0** |  |
| `System.Callback.OnSaoriExecute` | SAORIモジュールとして呼ばれた |
| **共通** |  |
| `System.Callback.OnUnload` | 切り離しイベント(華和梨が発行) |
| `System.Callback.OnRequest` | その他全てのリクエスト(NOTIFY SHIORI/2.x、TRANSLATE SHIORI/2.x等) |

## System.Callback.OnRequest

このうち`System.Callback.OnRequest`は、少し変わっているので解説します。このコールバックエントリは、他のコールバックエントリに該当しなかった、全ての本体からのコールで呼ばれます。具体的にはNOTIFY SHIORI/2.x、TRANSLATE SHIORI/2.6、TEACH SHIORI/2.4等が該当します。あまり使用しない呼び出しや、将来の本体仕様変更に備えたエントリです。

どのような呼び出しが来たかを知るためには、`System.Request`エントリを参照します。このエントリに、本体のコール種類を示す文字列である、「TEACH」や「NOTIFY OtherGhostName」等が格納されます。また、詳しくは次の節で解説しますが、本体が渡したヘッダは、`System.Request.*`エントリ群に格納されます。また、本体への応答ヘッダは、`System.Response.*`エントリ群に書き込みます。処理状態を示すステータスコードは、`System.Response`エントリに書き込みます。どのようなヘッダが来るか、どのようなヘッダを返すか、どのようなステータスコードを返すかについては、[SHIORI/3.0 仕様書](https://ukatech.shillest.net/ukadoc-spec/spec/shiori3/)などの本体の仕様書を参照して下さい。

一例として、TEACH SHIORI/2.4を簡易的に処理するスクリプトを示します。TEACH SHIORI/2.4は、Wordヘッダに教えた単語が来ます。応答の際は、Sentenceヘッダに書きます。処理が成功したら、ステータスコードとして200を発行します。これをスクリプトにすると、次のようになります。

```
System.Callback.OnRequest : $(
    if $[ ${System.Request} == "TEACH" ] $(
        setstr @Word ${System.Request.Word};
        pushstr TeachWord ${@Word};
        setstr System.Response.Sentence \0\s[0]${@Word}ね。\e;
        setstr System.Response 200;
    );
  )
```
