# urllist

**Category:** 補助機能

## 書式

```
$(urllist サイト名1 URL1 バナーURL1 ... サイト名n URLn バナーURLn)
```

## 戻り値

- サイト名1\[1\]URL1\[1\]バナーURL1\[2\]...サイト名n\[1\]URLn\[1\]バナーURLn\[2\]
- ※\[1\]はバイト値1、\[2\]はバイト値2

## 解説

SHIORI/2.5規格に従い、「おすすめリスト」を生成する。引数の数は必ず3の倍数になること。

仕切り線はサイト名に「-」を渡す。

## 使用例

```
futaba : "http://futaba.mikage.to/"
kawari : "http://meister-d-i.hoops.ne.jp/"

# さくら側のおすすめサイトのリスト
resource.sakura.recommendsites : $(
  urllist "ふたばみかげ" ${futaba} ${futaba}"banner.png"
  "何か以外の何か" ${kawari} ${kawari}"banner.png"
)

# うにゅう側のおすすめサイトのリスト
resource.kero.recommendsites : (
  $(urllist "ふたばみかげ" "http://futaba.mikage.to/" "banner.png")
  $(urllist "-" "-" "-")
  $(urllist "何か以外の何か" "http://meister-d-i.hoops.ne.jp/" "banner.png")
)
# サイトごとにurllistコマンドを分けて書くことも出来る
# 仕切り線の場合でも、ダミーのURLとバナーURLを与える必要がある
```
