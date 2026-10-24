# matchall

**Category:** コミュニケート機能

## 書式

```
$(matchall 文字列1 キーワード1 ...)
```

## 戻り値

真または偽

## 解説

キーワードが全て文字列1にあった場合、真を返す。キーワードは1個以上ならば、いくつでも列挙できる。

## 使用例

```
毒子.keyword1 : あらあら , 最近 , 中学生 , 乳

=kis
matchall ${System.Request.Reference1} こんにちは;
# Reference1に「こんにちは」が含まれる場合、真を返す

matchall ${System.Request.Reference1} うにゅう おいしい ？;
# Reference1に「うにゅう」「おいしい」「？」が含まれる場合、真を返す
# 例えば「うにゅうっておいしいの？」と言う文章がきた場合、真を返す

xargs 毒子.keyword1 matchall ${System.Request.Reference1};
# xargsとの合わせ技
# xargsで毒子.keyword1エントリの単語を「matchall..」以降に列挙
# 結果として、毒子.keyword1エントリの単語がすべてReference1に含まれる
# 場合、真を返す
=end
```
