# continue

**Category:** 構文コマンド

## 書式

```
$(continue)
```

## 戻り値

なし

## 解説

loop、until、while、foreach等のループ構文中で、現在のループ処理を終了し、次のループ処理に入る

## 使用例

```
# dataエントリの単語で「ゴースト」を含む単語のみdata2エントリにコピー
$(
  loop $(size data) $(
      setstr @count ${-1};
      echo $data[${@count}];
      if $[ $data[${@count} !~ "ゴースト" ] $(
          continue;
      );
      pushstr data2 $data[${@count}];
  );
)
```
