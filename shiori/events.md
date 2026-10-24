# イベント

イベント通知の際、本体からのReferenceヘッダを華和梨から参照するには、`${System.Request.Reference0}`など、非常に長いエントリ名を記述する必要があります。使ってみると、これは不便です。そこで、コマンドを作って記述を簡単にする場合を考えます。

コマンドを定義する際の注意ですが、スクリプト記述ゾーンで定義して下さい。辞書記述ゾーンのエントリ定義中でコマンドを定義した場合、コマンドの定義は「そのエントリが呼び出されて」初めて機能します。多く場合、コマンドは未定義も同然となります。

では、実際に定義してみます。

```
=kis
# Referenceを返すコマンド "Reference"
function Reference $(
    # 引数がなかった場合、何も返さない
    if $[ $(size @arg) <= 1 ] $(return);

    # System.Request.Reference?エントリの一つ目の単語を得る
    get System.Request.Reference$@arg[1][0];
);
=end
```

この例では、同じReference番号のReferenceヘッダが複数来る場合を想定し、getで0番目のRefernce?を参照しています。
