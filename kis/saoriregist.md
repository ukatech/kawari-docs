# saoriregist

**Category:** SAORI

## 書式

```
$(saoriregist DLLファイル エイリアス [ オプション ] )
```

## 戻り値

なし

## 解説

SAORIモジュールの登録。DLLファイルには、相対パスまたは絶対パスでDLLを指定する。エイリアスは、callsaoriコマンドでSAORIモジュールを呼ぶ際のキーワードを指定する。

オプションには、SAORIモジュールをロードするタイミングを指定する。SAORIの中にはロードに時間のかかるものや、呼ばれない可能性があることも考えられるため、このような調整が可能となっている。タイミングには`"preload", "loadoncall", "noresident"`の3種類があり、それぞれ、「saoriregist時にロード」「最初にcallsaori(x)された時にロード」「callsaori時にロードし、終わったら即アンロード」を意味する。デフォルトはloadoncallである。

Phase 9.0.0以降、SAORIモジュールがloadu(UTF-8のパスを受け取るload)をエクスポートしていれば、UTF-8のパスでloaduを呼ぶ。なければ従来どおりシステムのコードページ(ACP)のパスでloadを呼ぶ。

## 使用例

```
=kis
# saori_cpuid.dllをcpuidとして登録。今すぐロード。
saoriregist modules\saori_cpuid.dll cpuid preload
=end
```
