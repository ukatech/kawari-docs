# 簡易文字種判別

関数を作っていると、英大文字、英小文字、数字等、文字の種類を判別したくなることがよくあります。精度は今ひとつですが、比較的簡単に判別する関数が作れるので、次に示します。

```
# 判別に用いる文字テーブル
asciichar : "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
asciichar : "abcdefghijklmnopqrstuvwxyz_"
asciichar : "+-0123456789."
asciichar : "-^\!\"#$%&'()=|@[;:],./`{+*}<>?_"
=kis
writeprotect asciichar;
=end

# 文字種判別のテンプレートとなる関数
=kis
function ischaracters $(
    setstr @pos 0;

    while $[ ${@pos} < $(length $@arg[1]) ] $(
        setstr @char $(char_at $@arg[1] ${@pos});
        if $[ $@arg[2] !~ ${@char} ] $(
            return 0;
        );
        inc @pos;
    );
    return 1;
);
# 英大文字だけの文字列ならば真
function isupper     $(ischaracters $@arg[1] $asciichar[0]);
# 英小文字だけの文字列ならば真
function islower     $(ischaracters $@arg[1] $asciichar[1]);
# 数字だけなら真
function isnumerical $(ischaracters $@arg[1] $asciichar[2]);
# アルファベットだけの文字列ならば真
function isalpha     $(ischaracters $@arg[1] $(get asciichar[0..1]));
# アルファベットと数字だけの文字列ならば真
function isalnum     $(ischaracters $@arg[1] $(get asciichar[0..2]));
=end
```

これらの関数は、次のように使います。

```
string1 : alphabet
string2 : P2P
string3 : 12345

=kis
isupper ${string1};
# 0が返る
islower ${string1};
# 1が返る
isalnum ${string2};
# 1が返る
isnumerilac ${string1}${string3};
# 0が返る
=end
```
