# adddict

**Category:** 辞書操作

## 書式

```
$(adddict エントリ1 単語1)
```

## 戻り値

なし

## 解説

エントリ1に単語1を追加する。

エントリ名の指定には、[辞書操作コマンド共通の書式](dictcommon.md)を利用できる。

## 使用例

```
=kis
# npwエントリに「田中真紀子」を追加
adddict npw 田中真紀子;

# nameエントリにnpwエントリ中の単語を追加
adddict name ${npw}

# Actエントリに単語「${normal}」を追加
adddict Act "${normal}";

# 次の行を実行すると、normalエントリの中を単語を呼び出す
echo ${Act};
=end
```
