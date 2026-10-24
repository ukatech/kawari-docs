# set

**Category:** 辞書操作

## 書式

```
$(set エントリ1 単語1)
```

## 戻り値

なし

## 解説

エントリ1の内容を削除してから、単語1を登録する。

エントリ名の指定には、[辞書操作コマンド共通の書式](dictcommon.md)を利用できる。

## 使用例

```
dummy : 1
angry : 怒ってるゾ！

=kis
set mode 1;
# modeエントリの内容は「1」だけになる

set mody ${dummy};
# modeエントリの内容は${dummy}＝「1」になる

set emotion "${angry}";
# emotionエントリの内容は単語「${angry}」になる

echo ${emotion};
# 「怒ってるゾ！」を返す

=end
```
