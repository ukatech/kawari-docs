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

文字コードには次の名前を指定できる。大文字小文字は区別せず、`-` `_` `.` と空白は無視する(`Shift_JIS` `shift-jis` `ShiftJIS`は同じ。YAYAと同じ規則)。

| 文字コード | 説明 |
|---|---|
| `Shift_JIS` | `Shift_JIS`(CP932)。SJIS、CP932も可 |
| `UTF-8` | UTF-8。BOMがあれば取り除く |
| `EUC-JP` | EUC-JP |
| `ISO-2022-JP` | ISO-2022-JP(JIS)。JISも可 |
| `EUC-KR` | EUC-KR(Windowsでは949) |
| `GB2312` | GB2312(Windowsでは936。GBKも可) |
| `Big5` | Big5(Windowsでは950。CP950も可。Phase 9.3.4以降) |
| `ISO-8859-1` | ISO-8859-1。バイトとU+0000～U+00FFを1対1に対応させる(CP1252ではない)。Latin1も可。書き出すときU+00FFを超える文字は「?」になる(Phase 9.3.4以降) |
| `auto` | UTF-8または`Shift_JIS`を自動判定(textloadと同じ) |

未知の文字コードを指定したときや、実行環境が対応していない文字コードのときは、エラーになりエントリ1は変更されない。

## 使用例

```
=kis
textload_charset poem mypoem.txt EUC-JP;
# poemエントリにEUC-JPのファイル'mypoem.txt'を読み込む
=end
```
