# compare

**Category:** 文字列操作

## 書式

```
$(compare 文字列1 文字列2)
```

## 戻り値

-1、0、1のいずれか

## 解説

文字列同士を辞書順序で比較する。文字列1が文字列2より辞書順で後ならば1、文字列1が文字列2より辞書順で前ならば-1、文字列1と文字列2が等しければ0を返す。

Phase 9.0.0以降、比較は`Shift_JIS`のバイト順ではなく、Unicodeのコードポイント順で行われる。ASCII文字のみなら従来と変わらないが、漢字・かな・半角カナの間の順序は変わりうる。(`$[ ]`内の&lt;や\>による文字列比較や、エントリ列挙の順序も同様。)

## 使用例

```
dict : a , aa , b , c , xa , xy , z
word : hello

=kis
setstr @count 0;
loop $(size dict) $(
  if $[ $(compare $dict[${@count}] ${word}) < 1 ] $(
    inc @count;
  ) else $(
    break;
  );
);
insertstr dict[${@count}] ${word};

# compareを使った大小比較の例
# 辞書順にソートしたエントリに対し、添え字0から${word}と比較し、
# ${word}より大きな単語の直前に${word}を挿入している
=end
```
