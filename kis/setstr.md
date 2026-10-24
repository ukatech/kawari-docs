# setstr

**Category:** 辞書操作

## 書式

```
$(setstr エントリ1 文字列1)
```

## 戻り値

なし

## 解説

エントリ1の内容を削除してから、文字列1を登録する。setとの違いは、追加したものが必ず置換ブロックではなく、文字列になる点である。

エントリ名の指定には、[辞書操作コマンド共通の書式](dictcommon.md)を利用できる。

## 使用例

```
dummy : 1
angry : 怒ってるゾ！

=kis
setstr mode 1;
# modeエントリの内容は「1」だけになる

setstr mody ${dummy};
# modeエントリの内容は${dummy}＝「1」になる

setstr emotion "${angry}";
# emotionエントリの内容は文字列「${angry}」になる

echo ${emotion};
# 「${angry}」を返す

=end
```
