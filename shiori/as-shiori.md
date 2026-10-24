# 栞としての華和梨

栞サブシステムの仕事は一見複雑ですが、要約すれば、「本体の通知してきたIDから、相応しい応答を割り出して本体に返す」ことです。華和梨Phase 8はPhase 7までと比べると、こうした栞の仕事を、使用者により「生のまま」見せています。

代表的な例はイベント応答です。華和梨Phase 8はイベント応答、リソース文字列の要求、NOTIFY処理の呼び分けを、KISを使って書く必要があります。本体が通知してきたID(=イベント名、リソース名)は、`System.Request.ID`エントリに入っています。これを使って呼び分けます。

華和梨Phase 7.3.1と同じ名前でイベントエントリ、リソース文字列エントリを使いたい場合、`System.Callback.OnGET`エントリに次のように書きます。

```
# GET SHIORI/3.0への応答
# イベント、リソース文字列、コミュニケート、etc…
# イベントは「event.<イベント名>」、
# リソースは「Resourece.<リソース名>」というエントリを呼ぶ
System.Callback.OnGET: $(
    if $[ $(match_at ${System.Request.ID} On) ]
        ${event.${System.Request.ID}}
    else $(
        ${resource.${System.Request.ID}}
  )
```

この例では、例えばマウスのダブルクリックイベントが来た時、`event.OnMouseDoubleClick`エントリを呼びます。また、例えばさくら側の「おすすめURL」の要求があった場合、`${resource.sakura.recommendsites}`の評価結果を返します。

しかし、SHIORI/3.0ではイベントとリソース文字列要求は、本体からの通知形式に差がありません。そこで、エントリ名を従来から変更する代わりに、記述を簡素化することが出来ます。この場合、次のように書きます。

```
# GET SHIORI/3.0への応答
# イベント、リソース文字列、コミュニケート、etc…
# 「reply.<要求されている処理名>」というエントリを呼ぶ
System.Callback.OnGET : ${reply.${System.Request.ID}}
```

この例では、例えばマウスのダブルクリックイベントが来た時、`reply.OnMouseDoubleClick`エントリを呼びます。また、例えばさくら側の「おすすめURL」の要求があった場合、`${reply.sakura.recommendsites}`の評価結果を返します。

最後に、NOTIFYの処理の呼び分け触れます。NOTIFYの形式はイベント・リソース文字列要求のGETの場合と、ほとんど差がありません。

```
# NOTIFY SHIORI/3.0の処理
# HWnd通知、他のゴースト通知、インストール済みゴースト通知、etc…
# 「notify.<通知された情報名>」というエントリを呼ぶ
System.Callback.OnNOTIFY : ${notify.${System.Request.ID}}
```

例えば他に起動中のゴーストの名前がNOTIFYされた場合、`notify.otherghostnameエントリを呼びます。`

ミドルウェアを使わずに華和梨を使う場合、こうした記述が必ず必要です。しかし、多くのミドルウェアでは、こうした低レベル(よりプログラムに密着した)の記述が、既にパッケージ化されています。何らかの事情が無い限り、こうしたミドルウェアの使用をおすすめします。
