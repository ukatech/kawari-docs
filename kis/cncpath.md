# cncpath

**Category:** ファイル操作

## 書式

```
$(cncpath パス名)
$(cncpath パス名 ファイル名)
```

## 戻り値

正規化したパス名

## 解説

パス区切り記号に'/'と'\\'が混在したパス名を、実装したファイルシステムで適切なパス区切り記号に変換して返す。ファイル名も指定した場合、パスと適切な形で結合して、同じように適切なパス区切り記号で返す。パスとして解釈できない場合、何も返さない。

## 使用例

```
=kis
# ここではMS Windows上のオリジナル華和梨を想定している

# "..\..\unix"が返る
cncpath ../../unix;

# "C:\WINDOWS\SYSTEM"が返る
cncpath C:/WINDOWS\SYSTEM

# "..\..\UNIX\LS.EXE"が返る
cncpath ../../UNIX/ LS.EXE
=end
```
