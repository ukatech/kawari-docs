# pushstr

**Category:** 辞書操作

## 書式

```
$(pushstr エントリ1 文字列1)
```

## 戻り値

なし

## 解説

エントリ1の末尾に文字列1を追加する。adddictstrと同義。

エントリ名の指定には、[辞書操作コマンド共通の書式](dictcommon.md)を利用できる。

## 使用例

```
=kis
# npwエントリに「田中真紀子」を追加
pushstr npw 田中真紀子;

# nameエントリにnpwエントリ中の単語を追加
pushstr name ${npw}

# Actエントリに文字列「${normal}」を追加
pushstr Act "${normal}";

# 次の行を実行すると、「${normal}」を返す。
echo ${Act};
=end
```
