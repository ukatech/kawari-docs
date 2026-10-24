# break

**Category:** 構文コマンド

## 書式

```
$(break)
```

## 戻り値

なし

## 解説

loop、until、while、foreach等のループ構文から抜け出す。

## 使用例

```
# dataエントリ内の単語を調べ、「END」だったらループから抜ける
$(
  setstr @count 0;
  loop $(size data) $(
    if $[ $data[${@count}] == "END" ] $(
      break;
    ) else $(
      inc @count;
    );
  );
  get data[${@count}];
)
```
