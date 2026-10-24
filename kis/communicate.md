# communicate

**Category:** コミュニケート機能

## 書式

```
$(communicate エントリ1 単語1)
```

## 戻り値

エントリ1の示すエントリの単語、もしくは単語1

## 解説

エントリ1の単語を全て評価し、戻り値があった単語をランダムに1個選び、これをエントリ名と見なしてエントリ呼び出しの結果を返す。戻り値のあった単語が1つも無い場合、単語1を返す。単語1は省略可能。

エントリ名の指定には、[辞書操作コマンド共通の書式](dictcommon.md)を利用できる。

## 使用例

```
毒子.keyword1 : うむ , ふはははは , 変態
毒子.answer1  : \t\0\s[7]胸のことは言うなっ！\e
毒子.answer1  : \t\0\s[1]…。\e

花ちゃん.keyword1 : どないしたんや , 同じ中学生なのに
花ちゃん.answer1  : \t\0\s[8]あ‥‥\w8あまりじろじろ見んといてな。\e
花ちゃん.answer1  : \t\0\s[1]花ちゃんかて…。\e

match_keys : $(
  if $[ ${System.Request.Reference0} == "毒子" ] $(
    if $(xargs 毒子.keyword1 matchall ${System.Request.Reference1})
      毒子.answer1
  )
)

match_keys : $(
  if $[ ${System.Request.Reference0} == "花ちゃん" ] $(
    if $(xargs 花ちゃん.keyword1 matchall ${System.Request.Reference1})
      花ちゃん.answer1
  )
)

event.OnCommunicate : $(communicate match_keys ${communicate.else})

# コミュニケートコマンド群を用いたコミュニケートの実装例
# OnCommunicateイベントでcommunicateコマンドを使い、イベント反応を
# 記述したmatch_keysエントリを全て評価、戻り値のうち一つを選ぶ
# そして、戻り値をエントリ名と見なしてエントリ呼び出しを行い、それを返す
# 何も無い場合、communicate.elseエントリの単語を返す
```
