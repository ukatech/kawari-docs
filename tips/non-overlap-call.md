# エントリの重複回避呼び出し

通常のエントリ呼び出し(`${hoge}`)は、単語をランダムに選んで返します。しかし、同じ文章で同じエントリ呼び出しを複数使った場合、それぞれが異なることを保証しません。これが気になる場合、まず次のようなスクリプトを用意します。

```
# エントリからランダムに単語を重複せずに呼び出す
# 第1引数 : エントリ名
# 戻り値  : エントリ内の単語
# 備考    : 「エントリ名.buffer」というエントリを占有する
=kis
function  GetWordRandom $(
    if $[ $(size @arg) != 2] $(return);
    if $[ $(size $@arg[1].buffer) == 0 ] $(copy $@arg[1] $@arg[1].buffer);

    setstr @pos $(rand $(size $@arg[1].buffer));
    get $@arg[1].buffer[${@pos}];
    clear $@arg[1].buffer[${@pos}];
);
=end

# 指定エントリを単語重複せず呼び出すエントリ化する
# 第1引数 : エントリ名
# 戻り値  : なし
# 備考    : 「エントリ名.backup」、「エントリ名.backup.buffer」という
#           エントリを占有する
=kis
function Nonoverlap $(
    if $[ $(size $@arg[1].backup) == 0 ] $(copy $@arg[1] $@arg[1].backup);
    set $@arg[1] "$(GetWordRandom "$@arg[1]".backup)";
    writeprotect $@arg[1];
    writeprotect $@arg[1].backup;
);
=end
```

そして、次のように書きます。

```
# 「人名」エントリを重複回避して呼ぶよう指定する
=kis
Nonoverlap 人名;
=end
```

すると、単に`${人名}`と呼ぶだけで、エントリ内の単語をすべて使うまで、同じ単語を呼ばなくなります。単語を呼ぶ順序は、通常通りランダムです。

この記述をすると、指定したエントリに単語の追加が出来なくなります。指定する際は、辞書の読み込みがすべて完了した時点で、`Nonoverlap`を実行すると良いでしょう。
