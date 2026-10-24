# adddictstr

**Category:** 辞書操作

## 書式

```
$(adddictstr エントリ1 文字列1)
```

## 戻り値

なし

## 解説

エントリ1に文字列1を追加する。adddictとの違いは、追加したものが必ず置換ブロックではなく、文字列になる点である。

エントリ名の指定には、[辞書操作コマンド共通の書式](dictcommon.md)を利用できる。

## 使用例

```
=kis
# npwエントリに「田中真紀子」を追加
adddictstr npw 田中真紀子;

# nameエントリにnpwエントリ中の単語を追加
adddictstr name ${npw}

# Actエントリに文字列「${normal}」を追加
adddictstr Act "${normal}";

# 次の行を実行すると、「${normal}」を返す。
echo ${Act};
=end
```
