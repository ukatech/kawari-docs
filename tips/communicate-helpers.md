# コミュニケートコマンドの改善

華和梨Phase 8のコミュニケートコマンド群は、原始的コマンドばかりで、Phase 7.3.1より使いにくい部分があります。キーワードを動的に拡張できる反面、エントリ名を大量に消費します。そこで、あえてキーワードを従来同様に固定にすることで、記述を容易にする方法を考えました。

```
=kis
# 第1引数: 登録する対象のエントリ
# 第2引数: 登録するデータを記録したエントリ
function regist_communicate $(
    # 引数が2以外の場合終了
    if $[ $(size @arg) != 3 ] $(return);
    # 登録すべきデータがなければ終了
    if $[ $(size $@arg[2]) == 0 ] $(return);
    # 登録対象にデータ登録数を設定
    if $[ $(size $@arg[1]) == 0 ] $(setstr $@arg[1].size 0);

    setstr @pos 0;
    setstr @segment 0;
    # メインルーチン
    while $[ ${@segment} < $(size $@arg[2]) ] $(
        # キーワード、応答分部分の特定
        setstr @segment $(find $@arg[2] "//" ${@pos});
        if $[ ${@segment} == -1 ] $(return);
        setstr @keypos $(find $@arg[2] "-" ${@pos});
        if $[ ${@keypos} == -1 ] $(return);
        if $[ ${@keypos} > ${@segment} ] $(return);
        if $[ ${@keypos}+1 >= ${@segment} ] $(return);

        # communicate用エントリに登録
        # キーワード
        setstr @i ${@pos};
        while $[ ${@i} < ${@keypos} ] $(
            push $@arg[1].${$@arg[1].size}.keyword $(getcode $@arg[2][${@i}]);
            inc @i;
        );
        # 応答文
        setstr @i $[ ${@keypos}+1 ];
        while $[ ${@i} < ${@segment} ] $(
            push $@arg[1].${$@arg[1].size}.answer $(getcode $@arg[2][${@i}]);
            inc @i;
        );

        # communicateエントリに登録
        push $@arg[1] (
            "$(if $(xargs "
            $@arg[1]
            "."
            ${$@arg[1].size}
            ".keyword matchall ${System.Request.Reference1}) "
            $@arg[1]
            "."
            ${$@arg[1].size}".answer)"
        );

        # インクリメント
        inc $@arg[1].size;
        setstr @pos $[ ${@segment}+1 ];
    );
);


# 第1引数: 登録する対象のエントリ
# 第2引数: 登録するデータを記録したエントリ
function regist_communicate_to $(
    # 引数が2以外の場合終了
    if $[ $(size @arg) != 3 ] $(return);
    # 登録すべきデータがなければ終了
    if $[ $(size $@arg[2]) == 0 ] $(return);
    # 登録対象にデータ登録数を設定
    if $[ $(size $@arg[1]) == 0 ] $(setstr $@arg[1].size 0);

    setstr @pos 0;
    setstr @segment 0;
    # メインルーチン
    while $[ ${@segment} < $(size $@arg[2]) ] $(
        # ゴースト名部分の特定
        setstr @segment $(find $@arg[2] "//" ${@pos});
        if $[ ${@segment} == -1 ] $(return);
        setstr @ghostpos $(find $@arg[2] "-" ${@pos});
        if $[ ${@ghostpos} == -1 ] $(return);
        if $[ ${@ghostpos} > ${@segment} ] $(return);
        if $[ ${@ghostpos}+1 >= ${@segment} ] $(return);

        # communicate用エントリに登録
        # ゴースト名
        setstr @i ${@pos};
        while $[ ${@i} < ${@ghostpos} ] $(
            push $@arg[1].${$@arg[1].size}.ghost $(getcode $@arg[2][${@i}]);
            inc @i;
        );

        # キーワード、応答分部分の特定
        setstr @pos $[ ${@ghostpos}+1 ];
        setstr @keypos $(find $@arg[2] "-" ${@pos});
        if $[ ${@keypos} == -1 ] $(return);
        if $[ ${@keypos} > ${@segment} ] $(return);
        if $[ ${@keypos}+1 >= ${@segment} ] $(return);

        # communicate用エントリに登録
        # キーワード
        setstr @i ${@pos};
        while $[ ${@i} < ${@keypos} ] $(
            push $@arg[1].${$@arg[1].size}.keyword $(getcode $@arg[2][${@i}]);
            inc @i;
        );
        # 応答文
        setstr @i $[ ${@keypos}+1 ];
        while $[ ${@i} < ${@segment} ] $(
            push $@arg[1].${$@arg[1].size}.answer $(getcode $@arg[2][${@i}]);
            inc @i;
        );

        # communicateエントリに登録
        push $@arg[1] (
            "$(if $[ $(find "
            $@arg[1]
            "."
            ${$@arg[1].size}
            ".ghost ${System.Request.Reference0}) >= 0 && $(xargs "
            $@arg[1]
            "."
            ${$@arg[1].size}
            ".keyword matchall ${System.Request.Reference1}) ] "
            $@arg[1]
            "."
            ${$@arg[1].size}".answer)"
        );

        # インクリメント
        inc $@arg[1].size;
        setstr @pos $[ ${@segment}+1 ];
    );
);
=end
```

以上で定義した`regist_communicate`は、次のように使います。まず、あるエントリ(仮に`data1`とする)に、次のような単語を登録します。

```
data1 (
    今日, 天気, 良い,
    -,
    \0\s[5]そうだね。どこかにお出かけしたいね。\e,
    \0\s[0]こんな日は、外に遊びに行きたいな。\e,
    \0\s[4]こんな日に限って、仕事が一杯なの…\e,
    //
  )
```

その後、実際に`communicate`コマンドに登録するエントリを、仮に`com`とすると、

```
=kis
regist_communicate com data1;
=end
```

このように記述します。すると、`com`以下の次のようなエントリ群に、`data1`エントリの内容が展開されます。

```
com : $(if $(xargs com.0.keyword matchall ${System.Request.Reference1}) com.0.answer)
com.0.keyword : 今日 , 天気 , 良い
com.0.answer : \0\s[5]そうだね。どこかにお出かけしたいね。\e
com.0.answer : \0\s[0]こんな日は、外に遊びに行きたいな。\e
com.0.answer : \0\s[4]こんな日に限って、仕事が一杯なの…\e
com.size : 1
```

なお、上記の展開結果を確認したい場合、`regist_communicate`を実行後、次のようなスクリプトを実行してください。`saved.txt`に展開結果が記録されています。

```
=kis
clear temp;
listtree temp com;
xargs temp save saved.txt;
=end
```

`regist_communicate`で読み込むエントリの形式ですが、最初の「-」までの単語は、「キーワード」になります。Reference1の文章に上記キーワードがすべて存在すると、「-」以降の文章のうち、一つが応答文として選ばれます。一つの応答の組み合わせの最後には、「//」を置いて区切りとして下さい。「//」以降は、また別の応答を書くことが出来ます。

```
data2 (
    キーワード1,
    -,
    応答文1,
    //,
    キーワード2,
    -,
    応答文2,
    //
  )
```

これらの応答は、`com`エントリを`communicate`コマンドを通じて、`OnCommunicate`イベントに登録登録することで機能します。

```
reply.OnCommunicate : $(communicate com)
```

一方、`regist_communicate_to`コマンドは、さらに反応するゴースト名も指定できるよう、機能拡張したものです。最初の「-」までの単語が反応するゴースト名で、ここに列挙したゴーストのうち、いずれかが呼びかけた場合に反応します。最初の「-」から次の「-」までがキーワード、2番目の「-」以降は返す文章です。`regist_communicate`コマンドと同様、キーワード・応答文の組み合わせの最後に、「//」を置いて下さい。

```
data3 (
    毒子,サンバーレイン,
    -,
    メタル,
    -,
    \0\s[5]今度、いいアルバム紹介してね。\e,
    \0\s[0]デスとゴアってどう違うの？\e,
    //
  )

=kis
regist_communicate_to com data3;
=end
```

ゴーストの判定は`communicate`を2段重ねにして、`regist_communicate`のみを使う方法もあります。使い勝手の良い方を選んで使ってください。

```
# com.毒子エントリには、対毒子用文章をregist_communicateで登録
# com.陽子エントリには、対陽子用文章をregist_communicateで登録
com : $(
    if $[ ${System.Request.Reference0} == "毒子" ]
        com.毒子
    );
  )

com : $(
    if $[ ${System.Request.Reference0} == "陽子" ]
        com.陽子
    );
  )

reply.OnCommunicate : $(communicate com ${com.unknown})
```

なお、このスクリプトはゴーストに組み込んで使っても構いませんし、幸水を使って事前に変換する為に利用しても大丈夫です。
