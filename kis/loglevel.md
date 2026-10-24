# loglevel

**Category:** その他

## 書式

```
$(loglevel キーワードの列挙)
```

## 戻り値

なし

## 解説

ログに出力する内容を決める。引数に列挙したキーワードに対応する内容が出力されるようになる。キーワードには以下がある。デフォルトではquietだが、現在、一部のログが設定を無視して出力されてしまう既知のバグあり。

| キーワード | 出力する内容 |
|---|---|
| error | エラー |
| warning | 警告 |
| info | 動作情報 |
| decl | 空エントリへの読み出しアクセス |
| paranoia | 上記全て＋非常に詳しい動作情報 |
| baseevents | 基本イベント |
| timeevents | 時刻(秒、分)イベント |
| rscevents | リソース問い合わせイベント |
| quiet | 明確にログを禁止する |

## 使用例

```
=kis
# 通常デバッグ時には、これで十分
loglevel error warning info baseevents;

# まぁ、一度ぐらいは試してみてもいいです
# 間違っても配布版でこれをやらないように
loglevel paranoia baseevents;
=end
```
