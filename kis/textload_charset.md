# textload_charset

**Category:** ファイル操作

## 書式

```
$(textload_charset エントリ1 テキストファイル1 文字コード)
```

## 戻り値

なし

## 解説

[textload](textload.md)と同じだが、テキストファイル1の文字コードを指定して読み込む。

文字コードには次の名前を指定できる(大文字小文字は区別しない)。

| 文字コード | 説明 |
|---|---|
| `Shift_JIS` | `Shift_JIS`(CP932)。SJIS、CP932も可 |
| `UTF-8` | UTF-8。BOMがあれば取り除く |
| `EUC-JP` | EUC-JP |
| `ISO-2022-JP` | ISO-2022-JP(JIS)。JISも可 |
| `EUC-KR` | EUC-KR(Windowsでは949) |
| `GB2312` | GB2312(Windowsでは936。GBKも可) |
| `auto` | UTF-8または`Shift_JIS`を自動判定(textloadと同じ) |

未知の文字コードを指定したときや、実行環境が対応していない文字コードのときは、エラーになりエントリ1は変更されない。

## 使用例

```
=kis
textload_charset poem mypoem.txt EUC-JP;
# poemエントリにEUC-JPのファイル'mypoem.txt'を読み込む
=end
```
