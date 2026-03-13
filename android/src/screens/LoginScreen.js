import React, { useState } from 'react';
import {
    View, Text, TextInput, TouchableOpacity, StyleSheet,
    ScrollView, Alert, ActivityIndicator, KeyboardAvoidingView, Platform
} from 'react-native';
import * as SecureStore from 'expo-secure-store';
import api from '../api/client';
import { COLORS } from '../constants/theme';

export default function LoginScreen({ navigation, route }) {
    const [identifier, setIdentifier] = useState(''); // email or mobile
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const onLogin = route.params?.onLogin;

    const handleLogin = async () => {
        if (!identifier.trim() || !password) { Alert.alert('Error', 'Please fill all fields'); return; }
        setLoading(true);
        try {
            // Backend expects { identifier, password } — works for both email and mobile
            const res = await api.post('/auth/login', { identifier: identifier.trim(), password });
            await SecureStore.setItemAsync('auth_token', res.data.token);
            await SecureStore.setItemAsync('user_id', res.data.user?.id || '');
            await SecureStore.setItemAsync('user_name', res.data.user?.name || 'User');
            await SecureStore.setItemAsync('user_email', res.data.user?.email || '');
            onLogin?.();
        } catch (err) {
            Alert.alert('Login Failed', err.response?.data?.error || 'Check credentials and try again');
        } finally {
            setLoading(false);
        }
    };

    return (
        <KeyboardAvoidingView style={s.root} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
            <ScrollView contentContainerStyle={s.container} keyboardShouldPersistTaps="handled">
                <View style={s.logoRow}>
                    <View style={s.logoBox}><Text style={s.logoLetter}>R</Text></View>
                    <Text style={s.appName}>RAGnosis</Text>
                </View>
                <Text style={s.subtitle}>AI-Powered Medical Report Analysis</Text>

                <View style={s.card}>
                    <Text style={s.title}>Welcome Back 👋</Text>

                    <Text style={s.label}>Email or Mobile Number</Text>
                    <TextInput style={s.input} value={identifier} onChangeText={setIdentifier}
                        placeholder="doctor@hospital.com or 9876543210" placeholderTextColor={COLORS.textMuted}
                        keyboardType="email-address" autoCapitalize="none" />

                    <Text style={s.label}>Password</Text>
                    <TextInput style={s.input} value={password} onChangeText={setPassword}
                        placeholder="••••••••" placeholderTextColor={COLORS.textMuted}
                        secureTextEntry />

                    <TouchableOpacity style={s.btn} onPress={handleLogin} disabled={loading}>
                        {loading ? <ActivityIndicator color="#fff" /> : <Text style={s.btnText}>Login</Text>}
                    </TouchableOpacity>

                    <TouchableOpacity style={s.secondaryBtn} onPress={() => navigation.navigate('Register', { onLogin })}>
                        <Text style={s.secondaryText}>Don't have an account? <Text style={{ color: COLORS.primary }}>Register</Text></Text>
                    </TouchableOpacity>
                </View>
                <Text style={s.disclaimer}>🔒 Your medical data is encrypted and secure</Text>
            </ScrollView>
        </KeyboardAvoidingView>
    );
}

const s = StyleSheet.create({
    root: { flex: 1, backgroundColor: COLORS.bg },
    container: { flexGrow: 1, padding: 24, justifyContent: 'center' },
    logoRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', marginBottom: 8 },
    logoBox: {
        width: 44, height: 44, backgroundColor: COLORS.primary, borderRadius: 12,
        alignItems: 'center', justifyContent: 'center', marginRight: 10
    },
    logoLetter: { color: '#fff', fontWeight: '900', fontSize: 22 },
    appName: { color: COLORS.textPrimary, fontSize: 28, fontWeight: '800' },
    subtitle: { color: COLORS.textSecond, textAlign: 'center', marginBottom: 32, fontSize: 13 },
    card: {
        backgroundColor: COLORS.card, borderRadius: 20, padding: 24,
        borderWidth: 1, borderColor: COLORS.border
    },
    title: { color: COLORS.textPrimary, fontSize: 20, fontWeight: '800', marginBottom: 20 },
    label: { color: COLORS.textSecond, fontSize: 13, marginBottom: 6, marginTop: 12 },
    input: {
        backgroundColor: COLORS.bg, borderWidth: 1, borderColor: COLORS.border,
        borderRadius: 12, padding: 14, color: COLORS.textPrimary, fontSize: 15
    },
    btn: {
        backgroundColor: COLORS.primary, borderRadius: 12, padding: 16,
        alignItems: 'center', marginTop: 24
    },
    btnText: { color: '#fff', fontWeight: '800', fontSize: 16 },
    secondaryBtn: { alignItems: 'center', marginTop: 16, padding: 8 },
    secondaryText: { color: COLORS.textSecond, fontSize: 14 },
    disclaimer: { color: COLORS.textMuted, textAlign: 'center', fontSize: 11, marginTop: 24 },
});
