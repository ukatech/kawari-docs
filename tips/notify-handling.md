# SHIORI/3.0 NOTIFY処理

従来華和梨が担当していたNOTIFYの処理は、恐らくどのミドルウェアでも共通して必要だと思います。そこで、基本的なNOTIFY処理のサンプルを示します。このサンプルは、華和梨Phase 7.3.1時代のNOTIFY処理を模した動作をします。また、`Reference`ヘッダの参照に、ユーザーズマニュアルの応用編で定義した`Reference`コマンドを使用しています。

```
# コールバックエントリの設定
System.Callback.OnNOTIFY: ${notify.${System.Request.ID}}

# HWnd通知
# System.Hwnd.shellエントリ…シェル側のHWnd
# System.Hwnd.balloonエントリ…バルーン側のHWnd
notify.hwnd : $(
    split System.Hwnd.shell $(Reference 0) $(chr 1);
    split System.Hwnd.balloon $(Reference 1) $(chr 1);
)

# インストール済みゴースト通知
# System.InstalledGhostエントリにインストール済みゴースト名一覧
notify.installedghostname : $(
    clear System.InstalledGhost;

    setstr @count 0;
    while $(Reference ${@count}) $(
        pushstr System.Installedghost $(Reference ${@count});
        inc @count;
    );
)

# 起動中の他ゴースト通知
# System.OtherGhostエントリ…起動中ゴースト名一覧
# System.OtherGhostExエントリ…起動中ゴースト名＋サーフィス番号一覧
notify.otherghostname : $(
    clear System.OtherGhost;
    clear System.OtherGhostEx;

    setstr @count 0;
    while $(Reference ${@count}) $(
        split @ghost $(Reference ${@count}) $(chr 1);
        pushstr System.OtherGhost $@ghost[0];
        pushstr System.OtherGhostEx $(Reference ${@count});
        inc @count;
    );
)

# ユニークID通知
# System.UniqueIdエントリ…ユニークID
notify.uniqueid : $(setstr System.UniqueId $(Reference 0))
```
