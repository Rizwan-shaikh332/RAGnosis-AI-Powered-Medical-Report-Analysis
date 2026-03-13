# RAGnosis Mobile App 📱

A React Native (Expo) Android app for RAGnosis — AI-powered medical report analysis.

---

## ✅ Features
- 🔐 **JWT Login / Register** — same accounts as the web app
- 📤 **Upload Reports** — Pick PDF/image from files or scan directly with camera
- 📊 **Visual Report Detail** — Status boxes, range bars, metric table (same as web)
- 🤖 **AI Chatbot** — Ask questions about your reports using Groq Llama 3
- 📋 **My Reports** — Scrollable list with pull-to-refresh
- 👤 **Profile** — User info + logout

---

## 📋 Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Node.js | ≥ 18 | [nodejs.org](https://nodejs.org) |
| npm | ≥ 9 | Comes with Node |
| Expo Go App | Latest | Install on phone from Play Store |
| Python backend | Running | `python app.py` in `backend/` |

> **No Android Studio needed!** Expo Go lets you run the app instantly on your phone.

---

## 🚀 Quick Start

### 1. Configure Backend URL

Open `android/src/api/client.js` and set `BASE_URL`:

```js
// For Android Emulator (default)
export const BASE_URL = 'http://10.0.2.2:5000';

// For a real phone on the same Wi-Fi network:
export const BASE_URL = 'http://192.168.X.X:5000';  // ← your PC's LAN IP
```

**How to find your LAN IP on Windows:**
```powershell
ipconfig
# Look for "IPv4 Address" under your Wi-Fi adapter
```

Also ensure the backend allows external connections (it already does since Flask binds to `0.0.0.0` when run with `python app.py`).

---

### 2. Install Dependencies

```bash
cd android
npm install
```

---

### 3. Start the Expo Dev Server

```bash
npx expo start
```

This prints a QR code in the terminal.

---

### 4. Run on Your Phone

1. Install **Expo Go** from the Google Play Store
2. Open Expo Go → **Scan QR code**
3. Scan the QR code printed in step 3
4. The app loads on your phone!

---

### 5. Run on Android Emulator (Optional)

If you have Android Studio installed:

```bash
npx expo start --android
```

Or press `a` in the Expo terminal after `npx expo start`.

---

## 🏗 Build a Standalone APK

To generate a real `.apk` file (no Expo Go needed):

```bash
npm install -g eas-cli
eas login
eas build -p android --profile preview
```

After the build completes, download the APK from [expo.dev](https://expo.dev) and install it on your phone.

---

## 📁 Project Structure

```
android/
├── App.js                     # Root navigation (Stack + Tab)
├── app.json                   # Expo config
├── package.json
├── babel.config.js
└── src/
    ├── api/
    │   └── client.js          # Axios + SecureStore auth
    ├── constants/
    │   └── theme.js           # Colors, METRIC_CATALOG, getMetricStatus
    └── screens/
        ├── LoginScreen.js
        ├── RegisterScreen.js
        ├── DashboardScreen.js  # Overview + recent reports
        ├── UploadScreen.js     # Document picker + camera + OOK errors
        ├── ReportsScreen.js    # Reports list
        ├── ReportDetailScreen.js # Status boxes + range bars + table
        ├── ChatScreen.js       # AI Chatbot
        └── ProfileScreen.js    # User info + logout
```

---

## 🔌 API Endpoints Used

| Screen | Method | Endpoint |
|--------|--------|----------|
| Login | POST | `/api/auth/login` |
| Register | POST | `/api/auth/register` |
| Upload | POST | `/api/reports/upload` |
| List Reports | GET | `/api/reports/` |
| Report Detail | GET | `/api/reports/<id>` |
| Chatbot | POST | `/api/chatbot/chat` |

---

## ⚠️ Known Limitations

- PDF rendering inside the app is not embedded (tap to view from reports list)
- iOS is supported by Expo but not tested in this build
- The backend must be reachable from the device's network

---

## 🆘 Troubleshooting

| Problem | Fix |
|---------|-----|
| `Network Error` on login | Check `BASE_URL` in `client.js` — use LAN IP for phone, 10.0.2.2 for emulator |
| App shows blank screen | Run `npx expo start --clear` |
| Camera permission denied | Go to phone Settings → Apps → RAGnosis → Permissions → Camera |
| Backend connection refused | Make sure `python app.py` is running and Windows Firewall allows port 5000 |

---

*Built with Expo 51 · React Navigation 6 · Axios · Expo-Secure-Store*
