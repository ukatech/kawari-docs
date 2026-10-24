# save

**Category:** ファイル操作

## 書式

```
$(save ファイル名 エントリ名1 ... )
```

## 戻り値

なし

## 解説

ファイルにエントリ内容を華和梨辞書形式でセーブする。指定ファイルの以前の内容は消去し、指定エントリ群の内容でファイルを上書きする。

Phase 9.0.0以降、出力の文字コードはUTF-8(BOMあり)である。Phase 8.2.9以前は`Shift_JIS`で出力していた。

## 使用例

```
=kis
save dict-flag.txt flag1 flag2 flag3;
# flag1、flag2、flag3エントリをdict-flag.txtに保存
=end
```
