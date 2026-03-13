import React, { useState, useEffect } from 'react';
import {
    View, Text, StyleSheet, TouchableOpacity, Alert, ScrollView
} from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { COLORS } from '../constants/theme';

export default function ProfileScreen() {
    const navigation = useNavigation();
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');

    useEffect(() => {
        SecureStore.getItemAsync('user_name').then(n => n && setName(n));
        SecureStore.getItemAsync('user_email').then(e => e && setEmail(e));
    }, []);

    const handleLogout = () => {
        Alert.alert('Logout', 'Are you sure you want to logout?', [
            { text: 'Cancel', style: 'cancel' },
            {
                text: 'Logout', style: 'destructive', onPress: async () => {
                    await SecureStore.deleteItemAsync('auth_token');
                    await SecureStore.deleteItemAsync('user_name');
                    await SecureStore.deleteItemAsync('user_email');
                    await SecureStore.deleteItemAsync('user_id');
                    // Navigate to Login — App.js listener will pick up the missing token
                    navigation.reset({ index: 0, routes: [{ name: 'Login' }] });
                }
            }
        ]);
    };

    const items = [
        { icon: 'person-outline', label: 'Name', value: name || 'Not set' },
        { icon: 'mail-outline', label: 'Email', value: email || 'Not set' },
        { icon: 'shield-checkmark-outline', label: 'Data Security', value: 'Encrypted & Private' },
        { icon: 'information-circle-outline', label: 'App Version', value: '1.0.0' },
    ];

    return (
        <ScrollView style={s.root} contentContainerStyle={s.scroll}>
            {/* Avatar */}
            <View style={s.avatarSection}>
                <View style={s.avatar}>
                    <Text style={s.avatarText}>{name?.charAt(0)?.toUpperCase() || 'U'}</Text>
                </View>
                <Text style={s.displayName}>{name || 'RAGnosis User'}</Text>
                <Text style={s.displayEmail}>{email}</Text>
            </View>

            {/* Info rows */}
            <View style={s.card}>
                {items.map((item, i) => (
                    <View key={item.label} style={[s.row, i < items.length - 1 && s.rowBorder]}>
                        <View style={s.rowIcon}>
                            <Ionicons name={item.icon} size={18} color={COLORS.primary} />
                        </View>
                        <View style={{ flex: 1 }}>
                            <Text style={s.rowLabel}>{item.label}</Text>
                            <Text style={s.rowValue}>{item.value}</Text>
                        </View>
                    </View>
                ))}
            </View>

            {/* Disclaimer */}
            <View style={s.disclaimerCard}>
                <Ionicons name="information-circle-outline" size={16} color={COLORS.yellow} />
                <Text style={s.disclaimerText}>
                    RAGnosis uses AI for preliminary analysis only. Always consult a qualified healthcare provider for diagnosis and treatment.
                </Text>
            </View>

            {/* Logout */}
            <TouchableOpacity style={s.logoutBtn} onPress={handleLogout}>
                <Ionicons name="log-out-outline" size={18} color="#ef4444" />
                <Text style={s.logoutText}>Logout</Text>
            </TouchableOpacity>
        </ScrollView>
    );
}

const s = StyleSheet.create({
    root: { flex: 1, backgroundColor: COLORS.bg },
    scroll: { padding: 20, paddingBottom: 40 },
    avatarSection: { alignItems: 'center', marginBottom: 24 },
    avatar: {
        width: 80, height: 80, borderRadius: 40, backgroundColor: COLORS.primary,
        alignItems: 'center', justifyContent: 'center', marginBottom: 10
    },
    avatarText: { color: '#fff', fontSize: 36, fontWeight: '900' },
    displayName: { color: COLORS.textPrimary, fontWeight: '800', fontSize: 20 },
    displayEmail: { color: COLORS.textMuted, fontSize: 13, marginTop: 4 },
    card: {
        backgroundColor: COLORS.card, borderRadius: 16, borderWidth: 1,
        borderColor: COLORS.border, marginBottom: 16, overflow: 'hidden'
    },
    row: { flexDirection: 'row', alignItems: 'center', gap: 12, padding: 14 },
    rowBorder: { borderBottomWidth: 1, borderBottomColor: COLORS.border },
    rowIcon: {
        width: 36, height: 36, backgroundColor: COLORS.primaryLight, borderRadius: 10,
        alignItems: 'center', justifyContent: 'center'
    },
    rowLabel: { color: COLORS.textMuted, fontSize: 11 },
    rowValue: { color: COLORS.textPrimary, fontWeight: '600', fontSize: 14 },
    disclaimerCard: {
        backgroundColor: 'rgba(251,191,36,0.08)', borderRadius: 14, borderWidth: 1,
        borderColor: '#f59e0b33', padding: 14, flexDirection: 'row', gap: 8, marginBottom: 16
    },
    disclaimerText: { color: COLORS.textMuted, fontSize: 12, flex: 1, lineHeight: 18 },
    logoutBtn: {
        flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 10,
        backgroundColor: 'rgba(239,68,68,0.1)', borderRadius: 14, padding: 16,
        borderWidth: 1, borderColor: 'rgba(239,68,68,0.3)'
    },
    logoutText: { color: '#ef4444', fontWeight: '700', fontSize: 15 },
});
