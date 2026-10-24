# コミュニケート

他のゴーストに話し掛ける時は、`Reference0`に話し掛けたいゴースト名をセットして、トークを返します。`ReferenceN`(Nは0以上の整数)を返すには、`System.Response.ReferenceN`エントリに単語をセットします。なお、`System.Response`で始まるエントリは、コールバックごとに毎回内容が消去されます。

```
sentence : (
    $(setstr System.Response.Reference0 毒子)
    \0\s[0]おーい、毒子さん、聞こえるかーい。
    \1\s[11]やめとけ、アレは偽毒子だ。変な注射されるぞ。\e
  )
```

こうして話し掛けられたゴーストには、`OnCommunicate`がやってきます。SHIORI/3.0から、コミュニケートはイベントの一種になりました。

```
# 「会話」エントリの全内容を評価し、戻り値の一つをエントリ名として
# エントリ呼び出し
# 戻り値がなければ、communicate.unknownエントリを呼ぶ
reply.OnCommunicate : $(communicate 会話 ${communicate.unknown})
```

自分から話し掛けるときと同様、話し掛けるゴースト名を`Reference0`に設定して下さい。

なお、コミュニケート用コマンドは、ユーザ定義コマンドで使いやすいようラッピングするのが得策ですが、ここでは一番素直に書いた場合を例示します。

コミュニケートの基本的書き方は、次のようになります。

1. 反応するキーワードを書いたエントリを作る。キーワード群1個につきエントリ一個とする。仮にkeyとする。

1. キーワード群に対応する、返事を書いたエントリを作る。これもキーワード群1個につきエントリ1個とする。仮にanswerとする。

1. `communicate`コマンドで束ねるエントリを、仮に`com`とする。

1. キーワード、返事を`com`エントリに登録する時は、

   ```
   com : $(
       if $(xargs key matchall ${System.Request.Reference1})
           answer
     )
   ```

   と書く。

1. `OnCommunicate`イベントで、

   ```
   $(communicate com)
   ```

   と書く。

以上をまとめた例を挙げます。

```
# 例えば「あなたの名前は何？」に反応する
com.key.1 : あなた , 名前 , 何？
com.answer.1 : (
    \0\s[0]私の名前は${myname}です。\s[5]あなたは？\e
    $(setstr System.Response.Reference0 $(Reference 0))
  )
com.answer.1 : \0\s[4]うー。\1\s[10]すまん、こいつ今機嫌が悪くてな\e
com.answer.1 : \0\s[8]…。\1\s[10]無視かよ。\e
com : $(
    if $(xargs com.key.1 matchall $(Reference 1))
        com.answer.1
  )

# 「胸が無い」と言われるとキれる
com.key.2 : 胸 , 無い
com.answer.2 : \0\s[25]…。\1\s[11]俺が時間を稼ぐ、早く逃げろ！\e
com : $(
    if $(xargs com.key.2 matchall $(Reference 1))
        com.answer.2
  )

# 複数のゴーストの呼びかけに応じる例
# 「うにゅぼんで一緒に遊ぼう」等に反応する
com.key.3 : うにゅぼん , 一緒 , 遊ぼう
com.answer.3 : (
    \0\s[5]うん！じゃ、私は「${installedghost}」使うよ。\e
    $(setstr System.Response.Reference0 $(Reference 0))
  )
# 反応するゴースト名一覧
com.ghost.3  : 黒姉 , まゆら , さくら , せりこ
com.ghost.3  : 毒子 , あると , 奈留 , 安子
# findを使い、反応するべきゴーストかどうか判定
com : $(
    if $[ $(find com.ghost.3 $(Reference 0)) >= 0 &&
     $(xargs com.key.3 matchall $(Reference 1)) ]
        com.answer.3
  )

# あるゴーストに自分の名前を呼ばれたときに反応
com.key.4 : ${myname}
com.answer.4 : \0\s[5]……$(Reference 0)様！\e$(setstr FlagMode happy)
com.ghost.4 : まゆら
com : $(
    if $[ $(Reference 0) == ${com.ghost.4} &&
     $(xargs com.key.4 matchall $(Reference 1)) ]
        com.answer.4
  )

# キーワード外の反応文
com.unknown : \0\s[4]ごめん、よく分かんない。\e
com.unknown : \0\s[8]なプー。\1\s[10]…。\e
com.unknown : (
    \0\s[0]…それから？\e
    $(setstr System.Response.Reference0 $(Reference 0))
  )

# コミュニケートイベントでcomエントリを登録
reply.OnCommunicate : $(communicate com ${com.unknown})
```
