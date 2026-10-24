# savecrypt

**Category:** ファイル操作

## 書式

```
$(savecrypt ファイル名 エントリ名1 ... )
```

## 戻り値

なし

## 解説

ファイルにエントリ内容を暗号化華和梨辞書形式でセーブする。指定ファイルの以前の内容は消去し、指定エントリ群の内容でファイルを上書きする。

Phase 9.0.0以降、暗号化前の内容はUTF-8(BOMあり)で出力される。このため、savecryptで保存した辞書は、Phase 8.2.9以前の華和梨では正しく読めない。

## 使用例

```
=kis
savecrypt dict-flag.txt flag1 flag2 flag3;
# flag1、flag2、flag3エントリをdict-flag.txtに暗号化して保存
=end
```
