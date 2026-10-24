# size

**Category:** 辞書操作

## 書式

```
$(size エントリ1)
```

## 戻り値

単語数

## 解説

エントリ1中の単語数を返す。

## 使用例

```
理夢 : 理夢
ninni.angels,famous.ghosts : 奈留, せりこ, まゆら, ${理夢}
dark.sisters,famous.ghosts : 毒子, 花ちゃん, サンバーレイン, ${理夢}

=kis
size dark.sisters;
# 4が返る

size famous.ghosts;
# 8が返る
=end
```
