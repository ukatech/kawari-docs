# callsaori

**Category:** SAORI

## 書式

```
callsaori エイリアス [ 引数 引数 ... ]
```

## 戻り値

SAORIの戻り値(Result)

## 解説

戻り値が一つのSAORIを呼び出す。

Phase 9.0.0以降、リクエストの文字コードはUTF-8から始める。ロード直後のGET Versionの応答にCharsetがあれば、以後その文字コードで送り、なければ以後`Shift_JIS`で送る(古いSAORI互換)。応答はそのCharsetに従って解釈し、Charsetがなければ、`Shift_JIS`で送った場合は`Shift_JIS`、そうでなければ自動判定する。応答に有効なCharsetがあれば、次回からその文字コードで送る。

**SAORI over DirectSSTP** (Phase 9.0.0 β2以降、Windows (SSP 2.9.13以降)とninixのみ):本体に内蔵されたモジュール(`internal_crypto`、`internal_data`、`internal_random`など)を、DLLなしのSAORIとして呼べる。SAORI/1.0の要求をDLLではなく本体へDirect SSTPで送る。

- エイリアスの登録は、`saoriregist`に、実体のないDLLの名前を`internal_`で始まる名前で指定する(フォルダは問わない)。本体が互換機能を内蔵するSAORI(houchi、clipcopy、textcopy、`saori_ip`、`saori_cpuid`、mciaudio、cpuusage、httpc、string、hanayu)も、DLLが無ければ本体の機能を呼ぶ。DLLの実体があるときは、これまでどおりDLLとして読む。
- 登録しなくても、`internal_`で始まるモジュール名をそのままエイリアスにして呼べる。初めて呼ぶとき、本体の`internal_system`の`ListModules`で内蔵モジュールの一覧を確かめ、一覧にあれば自動で登録する。
- 1つ目の引数が関数名、2つ目以降がその関数の引数と`--オプション=値`。詳細は[SAORI over DirectSSTP](https://ssp.shillest.net/ukadoc/manual/spec_saori_ex.html)を参照。
- 本体のウィンドウは、本体からのNOTIFY`hwnd`で知る。それより前は呼べない。
- 常にUTF-8で送る。引数に改行は書けない(送らずに失敗)。空の引数も位置として数える。
- Direct SSTPは常にLocalとして扱われるため、SecurityLevelがlocal以外のリクエストの処理からは呼ばない。
- 本体の応答を最大30秒待つ。時間のかかる処理は、モジュール側の`--async=識別子`で非同期にする。

## 使用例

```
sentence : \0\s[0]ここのOSは$(callsaori cpuid os.name)ね。\e

# 登録なしで、本体のモジュールを呼ぶ
sentence : $(callsaori internal_crypto Digest sha256 abc)
```
