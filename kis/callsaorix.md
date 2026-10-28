# callsaorix

**Category:** SAORI

## 書式

```
callsaorix エイリアス 戻り値格納エントリ [ 引数 引数 ... ]
```

## 戻り値

SAORI呼び出し結果(Result)

## 解説

複数の戻り値を持つSAORIを呼び出し、結果を得る。SAORIの戻り値はValue\[数値\]ヘッダに格納されているが、これを、「`指定エントリ.Value[数値]`」エントリに格納する。また、「`指定エントリ.size`」に、得られた戻り値(Value)の数を返す。

## 使用例

```
# tmizu氏作のwmove.dllを使い、キャラクタの立ち位置を取得する
=kis
function getposition $(
  # 引数1 : 0=Sakura、1=Kero
  # 引数2 : 戻り値返却用エントリ名
  if $[ $@arg[1] == 0 ] $(
    setstr @characterHWnd $System.HWnd.shell[0];
  ) else if $[ $@arg[1] == 1 ] $(
    setstr @characterHWnd $System.HWnd.shell[1];
  ) else $(
    return "";
  );

  callsaorix wmove $@arg[2] GET_POSITION ${@characterHWnd};
);
=end
```
