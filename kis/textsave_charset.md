# textsave_charset

**Category:** ファイル操作

## 書式

```
$(textsave_charset ファイル名 文字コード エントリ1 [エントリ2..])
```

## 戻り値

なし

## 解説

[textsave](textsave.md)と同じだが、書き出す文字コードを指定する。文字コードの名前は[`textload_charset`](textload_charset.md)と同じ(autoは指定できない)。BOMは付けない。

文字コードに無い文字は「?」になる。未知の文字コードを指定したときや、実行環境が対応していない文字コードのときは、エラーになりテキストファイル1は上書きされない。

## 使用例

```
=kis
textsave_charset highscore.dat EUC-JP タイトル保持者名一覧;
# highscore.datに、「タイトル保持者名一覧」エントリの内容をEUC-JPで保存
=end
```
