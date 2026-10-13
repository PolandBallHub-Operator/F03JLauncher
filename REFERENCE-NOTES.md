# Theme migration reference notes

- Material Components for Android official getting-started guide: https://m2.material.io/develop/android/docs/getting-started
  - It lists `Theme.MaterialComponents.Light.NoActionBar.Bridge` among available bridge themes.
  - Bridge themes inherit from AppCompat themes and provide Material Components theme attributes.
  - The same guide recommends `AppCompatActivity` (or `AppCompatDelegate`) where AppCompat/Material view inflation is needed.
- AndroidX AppCompat release notes: https://developer.android.com/jetpack/androidx/releases/appcompat
  - AppCompat 1.6.1 was released February 8, 2023.
- AppCompat 1.6.1 Google Maven artifact inspected: https://dl.google.com/dl/android/maven2/androidx/appcompat/appcompat/1.6.1/appcompat-1.6.1.aar
  - Its `META-INF/com/android/build/gradle/aar-metadata.properties` declares `minCompileSdk=33`, so this build must use `compileSdkVersion 33` or later.
- Material Components 1.9.0 Google Maven artifact: https://dl.google.com/dl/android/maven2/com/google/android/material/material/1.9.0/material-1.9.0.aar

F-03J device framework information came from the user-provided `/home/ubuntu/upload/framework-res.apk`: Apktool reports package `android`, `sdkVersion=22`, `versionName=5.1.1-F03J.20190222.100239`. This is user-provided evidence, not a public web source.
