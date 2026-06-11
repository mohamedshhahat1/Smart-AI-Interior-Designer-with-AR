# Smart Interior AI Mobile

Flutter client for Smart AI Interior Designer with AR.

## API configuration

Development defaults are:

- Android emulator: `http://10.0.2.2:8000/api/v1`
- Web, iOS simulator, Windows, macOS, Linux: `http://localhost:8000/api/v1`

Physical devices and release builds must provide a reachable HTTPS endpoint:

```powershell
flutter run --dart-define=API_BASE_URL=https://api.example.com/api/v1
```

Debug Android builds allow cleartext HTTP for local development. The main
manifest does not enable cleartext traffic, so production deployments should
use HTTPS.

## Android release signing

Release tasks require `android/key.properties` with `storeFile`,
`storePassword`, `keyAlias`, and `keyPassword`. Release builds fail rather than
silently using the debug key when this file is missing.

## Verification

```powershell
flutter pub get
flutter analyze
flutter test
flutter build apk --debug --dart-define=API_BASE_URL=https://example.invalid/api/v1
```
