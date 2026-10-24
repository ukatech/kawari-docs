# エントリの順序呼び出し

エントリ呼び出しの際、呼び出すたびにエントリ内の単語の順序に従って呼び出すことが出来ます。主にストーリー等を記述する際に便利でしょう。次のようなスクリプトを用意してください。

```
# エントリから単語を添え字順に呼び出す
# 第1引数 : エントリ名
# 戻り値  : エントリ内の単語
# 備考    : 「エントリ名.pos」というエントリを占有する
=kis
function  GetWordSequential $(
    if $[ $(size @arg) != 2] $(return);
    if $[ $(size $@arg[1].pos) == 0 ] $(setstr $@arg[1].pos 0);

    get $@arg[1][${$@arg[1].pos}];
    setstr $@arg[1].pos $[ (${$@arg[1].pos}+1) % $(size $@arg[1]) ];
);
=end

# 指定エントリを添え字順に呼び出すエントリ化する
# 第1引数 : エントリ名
# 戻り値  : なし
# 備考    : 「エントリ名.backup」、「エントリ名.backup.pos」という
#           エントリを占有する
=kis
function Sequential $(
    if $[ $(size $@arg[1].backup) == 0 ] $(copy $@arg[1] $@arg[1].backup);
    set $@arg[1] "$(GetWordSequential "$@arg[1]".backup)";
    writeprotect $@arg[1];
    writeprotect $@arg[1].backup;
);
=end
```

そして、次のように書きます。

```
# 「カード」エントリを添え字順に呼ぶよう指定する
=kis
Sequential カード;
=end
```

すると、単に`${カード}`と呼ぶだけで、エントリ内の単語を添え字順に呼びます。一番最後の単語を呼び出すと、先頭に戻ります。

この記述をすると、指定したエントリに単語の追加が出来なくなります。指定する際は、辞書の読み込みがすべて完了した時点で、`Sequential`を実行すると良いでしょう。
