# textload

**Category:** ファイル操作

## 書式

```
$(textload エントリ1 テキストファイル1)
```

## 戻り値

なし

## 解説

テキストファイル1の内容を読み込む。

ファイルの1行目はエントリ1の一つ目の単語、2行目はエントリ1の二つ目の単語となる。行末の改行コードは、削除してからエントリに格納する。

Phase 9.0.0以降、ファイルの文字コード(UTF-8または`Shift_JIS`)は自動判定される。

## 使用例

```
=kis
textload poem mypoem.txt;
# poemエントリにファイル'mypoem.txt'を読み込む

echo \0$(set @i 0 ; loop $(size poem) $(get poem[${@i}] ; inc @i))\e;
# ファイルmypoem.txtの内容を読み込み、さくら側バルーンで内容を表示する
=end
```
