# F-03J Launcher3（user app）

AOSP Launcher3 [`android-5.1.1_r4`](https://android.googlesource.com/platform/packages/apps/Launcher3/+/refs/tags/android-5.1.1_r4) をF-03J向けに移植したランチャーです。実機ログに基づき、初回データベース生成時の`AppWidgetHost.deleteHost()`によるnull binderクラッシュを回避し、通常のユーザーアプリとしてビルドします。

## 2つのビルド

両方ともパッケージ名は`com.f03j.launcher`です。同時にはインストールできません。切り替える際は同じアプリを上書きインストールしてください。

| APK | 内容 |
|---|---|
| `F03J-Launcher3-noqsb.apk` | QSBバーを表示せず、QSB用に予約されていた画面上部の余白をWorkspaceに戻します。ホームの一番上の行にもアプリを配置できます。 |
| `F03J-Launcher3-qsb.apk` | 白い角丸検索バーにロゴとマイクを表示します。バーをタップするとAOSP QSBと同じ`SearchManager.INTENT_ACTION_GLOBAL_SEARCH`をGoogleアプリ（`com.google.android.googlequicksearchbox`）宛てに送ります。Googleアプリが見つからない場合は端末の既定`ACTION_WEB_SEARCH`ハンドラーを試します。検索アプリ本体は含めません。 |

どちらのAPKにも添付された端末イラストをランチャーアイコンとして使用しています。縦横比を保ったまま透明余白を入れて、各mipmapサイズへ書き出しています。

## ビルド

`applicationId=com.f03j.launcher`、`minSdkVersion=16`、`targetSdkVersion=22`。JDK 17、Gradle Wrapper 7.5.1、Android SDK Platform 33 / Build Tools 33.0.2を使います。SDK 33はコンパイル用で、Android 13を実行対象にする設定ではありません。依存ライブラリはMaterial Components 1.9.0、AndroidX AppCompat 1.6.1、AndroidX Collection 1.2.0です。

```sh
./gradlew clean assembleNoqsbDebug assembleQsbDebug
```

## インストールと切り替え

WindowsのコマンドプロンプトではAPKのファイル名を選んで実行してください。

```bat
adb install -r F03J-Launcher3-noqsb.apk
adb shell appwidget grantbind --package com.f03j.launcher --user 0
```

QSB版を使う場合は代わりに`F03J-Launcher3-qsb.apk`を指定します。その後、端末のホームアプリ選択／既定ホーム設定で **F-03J Launcher3** を選択してください。QSB版はGoogleアプリが端末にインストールされていることを前提にします。

## 権限・テーマ・クラッシュ対策

APKはAOSP標準テーマを使用します。`BIND_APPWIDGET`等のsignature/system権限は要求しません。実機ログにあった`AppWidgetHost.deleteHost()`の初回起動呼び出しを外し、Widget serviceのstart/stop時にnull binderで起きるNPEはwidget連携だけをスキップするよう処理しています。Widget serviceが使えない場合、ホーム画面自体は起動してもウィジェット機能は使えないことがあります。Widgetのbindは上記のadbコマンドで許可します。

## 出典と検証

QuickSearchBoxの検索バーのタップ方法は[AOSP QuickSearchBox `lollipop-release`](https://android.googlesource.com/platform/packages/apps/QuickSearchBox/+/refs/heads/lollipop-release)

clean build、APK構造・署名・Manifestのprotected permission不在を確認します。実機でのこの版の起動確認はまだです。実機で問題が出た場合は`adb logcat -b crash -d -v threadtime`を採取してissueください。
