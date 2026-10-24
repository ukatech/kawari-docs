# listtree

**Category:** 辞書操作

## 書式

```
$(listtree エントリ1 エントリ2)
```

## 戻り値

なし

## 解説

「エントリ2.」で名前が始まるエントリ名一覧を、エントリ1に追加する。エントリ2に「.」を指定すると、全エントリ名一覧を取得できる。

## 使用例

```
=kis
listtree SHIORI System.Request;
# SHIORIエントリに、本体からのリクエストヘッダ一覧を追加する

listree Entries .;
# 全エントリ名をEntriesエントリに追加。主に今は亡き対GET Status用
```
