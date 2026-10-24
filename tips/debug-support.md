# デバッグ支援スクリプト

ゴーストを作る際、試行錯誤によるデバッグ作業は避けられません。しかし、その為にいちいち本体を立ち上げるのは、あまり効率が良くありません。その点、幸水を使ったデバッグは効率が良いですが、イベント処理やNOTIFY処理のデバッグを行おうとすると、少し工夫が必要です。

そこで、コールバックエントリの処理動作と、本体との入出力ヘッダをエミュレートするスクリプトを作りました。自由に望みのイベント、NOTIFYをエミュレートし、結果をログに出力できます。全てKISで記述していますので、幸水だけでゴーストのデバッグが出来ます。

```
=kis
# debugOnGET…GETのデバッグ
#
# 第1引数: イベント名、リソース名
# 第2引数以降: Reference[x]
function debugOnGET $(
    # IDがなければ終了
    if $[ $(size @arg) < 2 ] $(return);

    # ヘッダのお掃除
    cleartree System.Request;

    # ヘッダセット
    setstr System.Request GET;
    setstr System.Request.ID $@arg[1];

    clear @arg[0];
    setstr @arg[0] OnGET;
    xargs @arg debugCallback;
);

# debugOnNOTIFY…NOTIFYのデバッグ
#
# 第1引数: notifyされた情報名
# 第2引数以降: Reference[x]
function debugOnNOTIFY $(
    # IDがなければ終了
    if $[ $(size @arg) < 2 ] $(return);

    # ヘッダのお掃除
    cleartree System.Request;

    # ヘッダセット
    setstr System.Request NOTIFY;
    setstr System.Request.ID $@arg[1];

    clear @arg[0];
    setstr @arg[0] OnNOTIFY;
    xargs @arg debugCallback;
);

# debugCallback…コールバックエントリデバッグ用共通関数
#
# 第1引数: コールバックエントリ(OnGET、OnNOTIFY)
# 第2引数以降: Reference[x]
# 備考: リクエストヘッダはこの関数を呼ぶ前にセットすること
function debugCallback $(
    # IDがなければ終了
    if $[ $(size @arg) < 2 ] $(return);

    # ヘッダのお掃除
    cleartree System.Response;

    # 共通ヘッダセッド
    setstr System.Request.Sender Kosui;
    setstr System.Request.SecurityLevel local;
    setstr System.Request.Charset Shift_JIS;
    setstr @pos 2;
    loop $[ $(size @arg)-2 ] $(
        setstr System.Request.Reference$[${@pos}-2] $@arg[${@pos}];
        inc @pos;
    );

    # クエリー開始宣言
    logprint "[SHIORI/SAORI Emulator] Query sequence begin.";

    # リクエストの表示
    printRequestHeaders;

    # コールバック
    if $(size System.Callback.$@arg[1]) $(
        setstr @Value $(get System.Callback.$@arg[1]);
        if $(length ${@Value}) $(setstr System.Response.Value ${@Value});
    );

    # 応答の表示
    printResponseHeaders;

    # クエリー終了宣言
    logprint "[SHIORI/SAORI Emulator] Query sequence end.";

    #ヘッダの後片付け
    cleartree System.Request;
    cleartree System.Response;
);

# リクエストヘッダの表示
function printRequestHeaders $(
    logprint "---------------------- REQUEST";
    logprint ${System.Request} "SHIORI/3.0";

    listtree @Headers System.Request;
    if $(size @Headers) $(
        foreach @h @Headers $(
            if $[ ${@h} != "System.Request" ] $(
                logprint $(substr ${@h} 15)":" ${${@h}};
            );
        );
    );
    logprint;
);

# 応答ヘッダの表示
function printResponseHeaders $(
    logprint "---------------------- RESPONSE";
    if $(size System.Response.Value) $(
        logprint "SHIORI/3.0 200 OK";
    ) else $(
        logprint "SHIORI/3.0 204 No Content";
    );

    listtree @Headers System.Response;
    if $(size @Headers) $(
        foreach @h @Headers $(
            if $[ ${@h} != "System.Response" ] $(
                logprint $(substr ${@h} 16)":" ${${@h}};
            );
        );
    );
    logprint;
);
=end
```

このスクリプトを幸水からロードし、次のようにコマンドモードで入力すると、「OnSecondChangeイベント、連続起動15時間目、見切れ・重なり無し、トークは出力される状態」がエミュレートできます。

```
debugOnGET OnSecondChange 15 0 0 1
```

また、次のように入力すると、「インストールされているゴーストはさくら、まゆら、双葉、毒子」のNOTIFYをエミュレートします。

```
debugOnNOTIFY installedghostname さくら まゆら 双葉 毒子
```

実際は、さらにこのコマンドを使ってスクリプトを組み、長時間起動時の加速試験等を行うと便利でしょう。次の例は、1時間分のOnSecondChangeとOnMinuteChangeを送り、加速耐久試験を行うスクリプトです。トーク途中で選択肢を出した場合、サーフィス復帰を考慮していませんが、普通はこれで十分だと思います。

```
=kis
# Hourエントリに起動何時間目か記憶させる
loop 60 $(
    debugOnGET OnMinuteChange ${Hour} 0 0 1;
    loop 60 $(
        debugOnGET OnSecondChange ${Hour} 0 0 1;
    );
);
=end
```
