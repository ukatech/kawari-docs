# SAORIモジュール呼び出し

SAORIモジュールを呼び出す時は、`callsaori`コマンド、`callsaorix`コマンドを使います。`callsaori`コマンド、`callsaorix`コマンドは、先に定義した「エイリアス」でSAORIモジュールを呼びます。仮に、`music.dll`というSAORIモジュールを、「音楽」というエイリアスで使用宣言したとします。

```
saoriregist music.dll 音楽
```

このSAORIモジュールの機能が指定した音楽ファイルの再生だとしたら、再生する音楽ファイル名を指定するのが普通でしょう。この場合、SAORIモジュールに再生するファイル名を伝える必要があります。話の都合上、`music.dll`は

- 第1引数が「play」で再生開始、「stop」で再生停止
- 第2引数が再生開始時は再生するファイル名、停止時は無し

という仕様だとします。

この`music.dll`で、「`technopolis.mid`」という音楽ファイルを再生したい場合、

```
callsaori 音楽 play technopolis.mid
```

と書きます。`callsaori`コマンドのエイリアスより後ろの引数は、SAORIモジュールに引数として渡します。

`callsaorix`コマンドは、SAORIモジュールが戻り値以外に、様々な情報を送ってくるタイプの場合に使用します。仮に、先ほどの`music.dll`が「play」を指示した場合、次のような情報を送ってくるとします。

- Result:再生に成功したら「OK」
- Value0:音楽ファイルのタイトル
- Value1:音楽ファイルのアーティスト
- Value2:音楽ファイルの演奏時間(mm:ss形式)

では、`callsaorix`を使って、音楽ファイル「`Truth21c.mid`」を再生します。エイリアスは`callsaori`コマンド、`callsaorix`コマンドに共通で使えます。

```
callsaorix 音楽 music.info play Truth21c.mid
```

ここで、エイリアスのすぐ後ろの「`music.info`」は、SAORIモジュールが送ってきた情報を記録する際の、基準となるエントリの名前です。このエントリの名前は自由に決められます。上の例の場合、次のようなエントリに情報を書き込みます。

- music.info.Value0: "TRUTH(21C Remix)"
- music.info.Value1: "T-SQUARE plus"
- music.info.Value2: "05:30"
- music.info.size: "3"
- music.info: "SAORI/1.0 200 OK"

sizeはValueが何個あるかを示します。

`callsaori`、`callsaorix`はともに戻り値を返す関数コマンドです。戻り値はSAORIモジュールの返した`Result`ヘッダです。
