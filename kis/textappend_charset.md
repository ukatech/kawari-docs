# textappend_charset

**Category:** ファイル操作

## 書式

```
$(textappend_charset ファイル名 文字コード エントリ1 [エントリ2..])
```

## 戻り値

なし

## 解説

[textappend](textappend.md)と同じだが、追記する文字コードを指定する。それ以外は[`textsave_charset`](textsave_charset.md)と同じ。既存のファイルの文字コードとは無関係に指定の文字コードで追記するので、異なる文字コードを指定すると1つのファイル内に文字コードが混在する。
