# pop

**Category:** 辞書操作

## 書式

```
$(pop エントリ1)
```

## 戻り値

エントリ1の末尾の単語

## 解説

エントリ1の末尾にある単語を削除し、それを返す。エントリ1に単語が無ければ、空文字列を返す。

## 使用例

```
PASOPIA : パソピア7
oldmachine : PC9801,X68k,MSX2,PC8801,X1,PC8001,${PASOPIA}

=kis
foreach @pc oldmachine $(echo " "${@pc});
# 「 PC9801 X68k MSX2 PC8801 X1 PC8001 パソピア7」を返す

pop oldmachine;
# 「パソピア7」を返す

foreach @pc oldmachine $(echo " "${@pc});
# 「 PC9801 X68k MSX2 PC8801 X1 PC8001」を返す
=end
```
