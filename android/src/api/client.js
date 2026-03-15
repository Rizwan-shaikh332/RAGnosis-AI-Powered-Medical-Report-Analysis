import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

// ─────────────────────────────────────────────────────────────────────────────
//  IMPORTANT: Change this to your backend IP when testing on a real device.
//  If using Android emulator:  http://10.0.2.2:5000
//  If using Expo Go on Wi-Fi:  http://<YOUR_LAN_IP>:5000  (e.g. 192.168.1.5)
// ─────────────────────────────────────────────────────────────────────────────
export const BASE_URL = 'http://172.20.10.7:5000';

const api = axios.create({
    baseURL: `${BASE_URL}/api`,
    timeout: 120000,
});

// Inject Bearer token automatically on every request
api.interceptors.request.use(async (config) => {
    try {
        const token = await SecureStore.getItemAsync('auth_token');
        if (token) config.headers.Authorization = `Bearer ${token}`;
    } catch (_) { }
    return config;
});

export default api;
