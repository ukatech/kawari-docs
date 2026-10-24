# 自発トーク

自発的にトークをするには、`OnSecondChange`イベントを使うのが一般的です。ほぼ毎秒来るこのイベントが発生するたびに内部でカウンタを1ずつ増やし、カウンタが指定の値になったら、`OnSecondChange`でトークを返す、という方法です。

このとき注意が必要なのは、`OnSecondChange`が最小化しているときも発生する、という点です。`OnSecondChange`でトークが捨てられるか否かは、Reference3の1/0で判定できます。

以上を踏まえて、簡単な自発トークをするスクリプトを組んでみます。伝統的理由から、トークは`sentence`エントリにあるものとします。

```
System.Callback.OnGET : ${reply.${System.Request.ID}}

# トーク周期(秒)
# このエントリに指定した時間間隔で発話する
interval : 90

# トークカウンタ
# このカウンタがトーク周期と等しくなったら発話する
talkcounter : 0

# OnSecondChangeイベント
# Reference3が1なら、トークを返しても大丈夫
reply.OnSecondChange : $(
    if ${System.Request.Reference3} $(
        inc talkcounter;
        # カウンタがトーク周期以上になっていたら発話し、
        # カウンタをリセットする
        if $[ ${talkcounter} >= ${interval} ] $(
            entry sentence;
            setstr talkcounter 0;
        );
    );
  )
```
