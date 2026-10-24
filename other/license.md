# 華和梨のライセンスについて

## ライセンス

華和梨はフリーソフトウェアであり、いわゆる修正BSDライセンス(FreeBSDスタイルのもの)に基づいて再配布可能です。

ライセンスは以下になります。

```
Copyright (C) 2001-2015 KAWARI Development Team
(Meister(original works)/Nie/Nise-Meister/Sato/Shino/Suikyo)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer
   as the first lines of this file unmodified.

2. Redistributions in  binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
```

[氷鉋悦子さんによる日本語訳](http://openlab.etl.go.jp/freesoft/BSD-j.htm)(参考)をもとにした日本語訳は以下です。

> Copyright (C) 2001-2015 KAWARI Development Team
>
> (Meister(original works)/Nie/Nise-Meister/Sato/Shino/Suikyo)
>
> All rights reserved.
>
> 改変を加える場合も、加えない場合も、ソースとバイナリー形式での再配布、使用は、下記の条件を満たした場合に許諾される。
>
> 1. ソースコードでの再配布物には、必ず上記の著作権表示、この条件リスト、および以下の免責事項を、改変せずにこのファイルの最初の数行に入れなければならない。
> 1. バイナリー形式での再配布は、必ず上記の著作権表示、この条件リスト、以下の免責事項の複製をドキュメンテーション内、あるいは配布と共にパッケージに入れられて提供される他の物の中に入れなければならない。
>
> 著作者は直接的、非直接的、偶発的、特殊な、典型的、あるいは必然のいかなる場合においても、いかなる損害に一切責任は負わない。その損害は以下の内容も含み、しかもそれに限定されない。代用となる物やサービスの調達、効果・データ・利益の低下、商取引の障害、また、どのような責務の論理においても、それが契約に関するものであろうと、厳格な責務であろうと、不正行為（不注意やその他の場合も含む）であろうと、このソフトウェアを使用することによって生じるそれらの損害の、一切の責任から著作者は免れている。たとえ事前にそれらすべての損害への可能性が示唆されていた場合においても同様である。

## ゴーストの再配布について

[華和梨公式配布サイト](https://github.com/ukatech/kawari/releases)より配布されているパッケージについては、MTライブラリのものを含め、ver licenseコマンドで全ライセンス条文を見ることができます。

よって、**`shiori.dll`を含めた`.nar`や`.zip`を普通に再配布(Webページで公開など)して構いません。**華和梨のパッケージからshiori.dllだけを抜き出して同梱した状態で、ゴーストのパッケージ(.narや.zip)を公開することができます。公開に際して、華和梨ソースコードの再配布や、独自に書いたKISスクリプトなどの公開は必要ありません。

また、添付したサンプルのスクリプトと辞書については、改変の有無に関わらず、自由に使用、再配布できます。サンプルのスクリプトと辞書の使用、再配布に際して、暗号化解除やライセンス表示は必要ありません。

## パッチの採用について

修正BSDライセンスへの統一に伴い、パッチについても修正BSD、もしくは再配布制限無しに近いものを優先的に受け付けることにしました。GPLのパッチの取り込みは限りなく不可能です。LGPLのものは検討が必要ですが、できれば修正BSDにしていただけるとありがたいです。すみません。

## 華和梨の改造について

ライセンス文をパッケージに同梱、もしくはバイナリに直接含めることにより、改造した華和梨のバイナリを、ソースを公開せずに公開、ゴーストに用いることも可能です。ただし機能拡張については、SAORIという共通拡張方式を用いて華和梨外部に実現することを強く推奨します。
