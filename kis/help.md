# help

**Category:** その他

## 書式

```
$(help コマンド名)
$(help)
```

## 戻り値

リファレンスまたはコマンド一覧

## 解説

コマンドが指定された場合は、リファレンスを返す。

コマンドが指定されない場合は、使用可能なコマンドの一覧を返す。

戻り値は"幸水"での出力を前提にしている。

## 使用例

**例("幸水"での実行例)**

```
echo-mode > $(help help)
help
syntax  : help Command1
return  : help message
comment : return online help of KIS commnad (for Kosui use)
echo-mode > $(help)
Command list :
        echo
        set
    (・・・中略・・・)
        escape
echo-mode >
```
