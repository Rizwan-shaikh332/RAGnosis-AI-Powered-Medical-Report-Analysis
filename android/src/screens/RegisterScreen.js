import React, { useState, useContext } from 'react';
import {
    View, Text, TextInput, TouchableOpacity, StyleSheet,
    ScrollView, Alert, ActivityIndicator, KeyboardAvoidingView, Platform
} from 'react-native';
import * as SecureStore from 'expo-secure-store';
import api from '../api/client';
import { COLORS } from '../constants/theme';
import { AuthContext } from '../../App';

const GENDERS = ['Male', 'Female', 'Other'];

export default function RegisterScreen({ navigation }) {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [mobile, setMobile] = useState('');
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [heightInches, setHeightInches] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const { setLoggedIn } = useContext(AuthContext);

    const handleRegister = async () => {
        if (!name.trim() || !email.trim() || !password || !mobile.trim() || !age || !gender || !heightInches) {
            Alert.alert('Error', 'Please fill all fields'); return;
        }
        if (password.length < 6) { Alert.alert('Error', 'Password must be at least 6 characters'); return; }
        if (!/^\d{10}$/.test(mobile.trim())) { Alert.alert('Error', 'Mobile number must be 10 digits'); return; }
        setLoading(true);
        try {
            const res = await api.post('/auth/register', {
                name: name.trim(),
                email: email.trim(),
                password,
                mobile: mobile.trim(),
                age: parseInt(age, 10),
                gender,
                height_inches: parseFloat(heightInches),
            });
            await SecureStore.setItemAsync('auth_token', res.data.token);
            await SecureStore.setItemAsync('user_name', name.trim());
            await SecureStore.setItemAsync('user_email', email.trim());
            await SecureStore.setItemAsync('user_id', res.data.user?.id || '');
            setLoggedIn(true);
        } catch (err) {
            Alert.alert('Registration Failed', err.response?.data?.error || 'Please try again');
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

                <View style={s.card}>
                    <Text style={s.title}>Create Account 🏥</Text>

                    <Text style={s.label}>Full Name</Text>
                    <TextInput style={s.input} value={name} onChangeText={setName}
                        placeholder="Dr. Rizwan Shaikh" placeholderTextColor={COLORS.textMuted} />

                    <Text style={s.label}>Email</Text>
                    <TextInput style={s.input} value={email} onChangeText={setEmail}
                        placeholder="doctor@hospital.com" placeholderTextColor={COLORS.textMuted}
                        keyboardType="email-address" autoCapitalize="none" />

                    <Text style={s.label}>Mobile Number (10 digits)</Text>
                    <TextInput style={s.input} value={mobile} onChangeText={setMobile}
                        placeholder="9876543210" placeholderTextColor={COLORS.textMuted}
                        keyboardType="phone-pad" maxLength={10} />

                    <View style={s.row2}>
                        <View style={{ flex: 1 }}>
                            <Text style={s.label}>Age</Text>
                            <TextInput style={s.input} value={age} onChangeText={setAge}
                                placeholder="25" placeholderTextColor={COLORS.textMuted}
                                keyboardType="number-pad" />
                        </View>
                        <View style={{ width: 12 }} />
                        <View style={{ flex: 1 }}>
                            <Text style={s.label}>Height (inches)</Text>
                            <TextInput style={s.input} value={heightInches} onChangeText={setHeightInches}
                                placeholder="65" placeholderTextColor={COLORS.textMuted}
                                keyboardType="decimal-pad" />
                        </View>
                    </View>

                    <Text style={s.label}>Gender</Text>
                    <View style={s.genderRow}>
                        {GENDERS.map(g => (
                            <TouchableOpacity key={g} style={[s.genderBtn, gender === g && s.genderBtnActive]}
                                onPress={() => setGender(g)}>
                                <Text style={[s.genderText, gender === g && s.genderTextActive]}>{g}</Text>
                            </TouchableOpacity>
                        ))}
                    </View>

                    <Text style={s.label}>Password</Text>
                    <TextInput style={s.input} value={password} onChangeText={setPassword}
                        placeholder="Min. 6 characters" placeholderTextColor={COLORS.textMuted}
                        secureTextEntry />

                    <TouchableOpacity style={s.btn} onPress={handleRegister} disabled={loading}>
                        {loading ? <ActivityIndicator color="#fff" /> : <Text style={s.btnText}>Create Account</Text>}
                    </TouchableOpacity>

                    <TouchableOpacity style={s.secondaryBtn} onPress={() => navigation.navigate('Login')}>
                        <Text style={s.secondaryText}>Already have an account? <Text style={{ color: COLORS.primary }}>Login</Text></Text>
                    </TouchableOpacity>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
}

const s = StyleSheet.create({
    root: { flex: 1, backgroundColor: COLORS.bg },
    container: { flexGrow: 1, padding: 24, paddingVertical: 40 },
    logoRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', marginBottom: 24 },
    logoBox: {
        width: 44, height: 44, backgroundColor: COLORS.primary, borderRadius: 12,
        alignItems: 'center', justifyContent: 'center', marginRight: 10
    },
    logoLetter: { color: '#fff', fontWeight: '900', fontSize: 22 },
    appName: { color: COLORS.textPrimary, fontSize: 28, fontWeight: '800' },
    card: { backgroundColor: COLORS.card, borderRadius: 20, padding: 24, borderWidth: 1, borderColor: COLORS.border },
    title: { color: COLORS.textPrimary, fontSize: 20, fontWeight: '800', marginBottom: 20 },
    label: { color: COLORS.textSecond, fontSize: 13, marginBottom: 6, marginTop: 12 },
    input: {
        backgroundColor: COLORS.bg, borderWidth: 1, borderColor: COLORS.border,
        borderRadius: 12, padding: 14, color: COLORS.textPrimary, fontSize: 15
    },
    row2: { flexDirection: 'row' },
    genderRow: { flexDirection: 'row', gap: 10 },
    genderBtn: {
        flex: 1, borderWidth: 1, borderColor: COLORS.border, borderRadius: 12,
        padding: 12, alignItems: 'center', backgroundColor: COLORS.bg
    },
    genderBtnActive: { borderColor: COLORS.primary, backgroundColor: COLORS.primaryLight },
    genderText: { color: COLORS.textSecond, fontWeight: '600' },
    genderTextActive: { color: COLORS.primary },
    btn: { backgroundColor: COLORS.primary, borderRadius: 12, padding: 16, alignItems: 'center', marginTop: 24 },
    btnText: { color: '#fff', fontWeight: '800', fontSize: 16 },
    secondaryBtn: { alignItems: 'center', marginTop: 16, padding: 8 },
    secondaryText: { color: COLORS.textSecond, fontSize: 14 },
});
