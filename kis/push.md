# push

**Category:** 辞書操作

## 書式

```
$(push エントリ1 単語1)
```

## 戻り値

なし

## 解説

エントリ1の末尾に単語1を追加する。adddictと同義。

エントリ名の指定には、[辞書操作コマンド共通の書式](dictcommon.md)を利用できる。

## 使用例

```
=kis
# npwエントリに「田中真紀子」を追加
push npw 田中真紀子;

# nameエントリにnpwエントリ中の単語を追加
push name ${npw}

# Actエントリに単語「${normal}」を追加
push Act "${normal}";

# 次の行を実行すると、normalエントリの中を単語を呼び出す
echo ${Act};
=end
```
