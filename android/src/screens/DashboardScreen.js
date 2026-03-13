import React, { useState, useEffect, useCallback } from 'react';
import {
    View, Text, ScrollView, StyleSheet, TouchableOpacity,
    RefreshControl, ActivityIndicator
} from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { Ionicons } from '@expo/vector-icons';
import api from '../api/client';
import { COLORS } from '../constants/theme';

export default function DashboardScreen() {
    const [reports, setReports] = useState([]);
    const [name, setName] = useState('User');
    const [loading, setLoading] = useState(true);
    const [refresh, setRefresh] = useState(false);

    const load = useCallback(async () => {
        try {
            const n = await SecureStore.getItemAsync('user_name');
            if (n) setName(n);
            const res = await api.get('/reports/');
            setReports(res.data.reports || []);
        } catch (_) { }
        setLoading(false);
        setRefresh(false);
    }, []);

    useEffect(() => { load(); }, [load]);

    const elevated = reports.reduce((a, r) => {
        const m = r.metrics || {};
        return a + Object.keys(m).length;
    }, 0);

    const cards = [
        { icon: 'document-text', label: 'Total Reports', value: reports.length, color: COLORS.primary },
        { icon: 'trending-up', label: 'Metrics Tracked', value: elevated, color: COLORS.green },
        {
            icon: 'time', label: 'Last Upload',
            value: reports[0]
                ? new Date(reports[0].uploaded_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' })
                : '—',
            color: COLORS.cyan
        },
    ];

    if (loading) return (
        <View style={[s.root, { justifyContent: 'center', alignItems: 'center' }]}>
            <ActivityIndicator color={COLORS.primary} size="large" />
        </View>
    );

    return (
        <ScrollView style={s.root} contentContainerStyle={s.scroll}
            refreshControl={<RefreshControl refreshing={refresh}
                onRefresh={() => { setRefresh(true); load(); }} colors={[COLORS.primary]} />}>

            {/* Header */}
            <View style={s.header}>
                <View>
                    <Text style={s.greeting}>Good day,</Text>
                    <Text style={s.name}>{name} 👋</Text>
                </View>
                <View style={s.logoBox}><Text style={s.logoLetter}>R</Text></View>
            </View>

            {/* Stat cards */}
            <View style={s.cardRow}>
                {cards.map(c => (
                    <View key={c.label} style={[s.statCard, { borderColor: c.color }]}>
                        <Ionicons name={c.icon} size={22} color={c.color} />
                        <Text style={[s.statValue, { color: c.color }]}>{c.value}</Text>
                        <Text style={s.statLabel}>{c.label}</Text>
                    </View>
                ))}
            </View>

            {/* Recent reports */}
            <Text style={s.section}>Recent Reports</Text>
            {reports.slice(0, 5).map(r => (
                <View key={r._id} style={s.reportRow}>
                    <View style={[s.iconCircle, { backgroundColor: COLORS.primaryLight }]}>
                        <Ionicons name="document-text" size={18} color={COLORS.primary} />
                    </View>
                    <View style={{ flex: 1 }}>
                        <Text style={s.reportName} numberOfLines={1}>{r.original_name}</Text>
                        <Text style={s.reportDate}>{new Date(r.uploaded_at).toLocaleDateString('en-IN')}</Text>
                    </View>
                    <View style={s.typeBadge}><Text style={s.typeBadgeText}>{r.report_type?.split('/')[0]}</Text></View>
                </View>
            ))}
            {reports.length === 0 && (
                <View style={s.empty}>
                    <Text style={{ fontSize: 36 }}>📋</Text>
                    <Text style={s.emptyText}>No reports yet. Upload one to get started!</Text>
                </View>
            )}

            <View style={s.disclaimer}>
                <Ionicons name="information-circle-outline" size={14} color={COLORS.textMuted} />
                <Text style={s.disclaimerText}> RAGnosis uses AI for preliminary analysis only. Always consult a doctor.</Text>
            </View>
        </ScrollView>
    );
}

const s = StyleSheet.create({
    root: { flex: 1, backgroundColor: COLORS.bg },
    scroll: { padding: 20, paddingBottom: 40 },
    header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 },
    greeting: { color: COLORS.textSecond, fontSize: 13 },
    name: { color: COLORS.textPrimary, fontSize: 22, fontWeight: '800' },
    logoBox: { width: 40, height: 40, backgroundColor: COLORS.primary, borderRadius: 10, alignItems: 'center', justifyContent: 'center' },
    logoLetter: { color: '#fff', fontWeight: '900', fontSize: 18 },
    cardRow: { flexDirection: 'row', gap: 10, marginBottom: 28 },
    statCard: {
        flex: 1, backgroundColor: COLORS.card, borderRadius: 16, padding: 14,
        borderWidth: 1, alignItems: 'center', gap: 6
    },
    statValue: { fontSize: 22, fontWeight: '900' },
    statLabel: { color: COLORS.textMuted, fontSize: 10, textAlign: 'center' },
    section: { color: COLORS.textPrimary, fontWeight: '700', fontSize: 16, marginBottom: 12 },
    reportRow: {
        flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: COLORS.card,
        borderRadius: 14, padding: 14, marginBottom: 10, borderWidth: 1, borderColor: COLORS.border
    },
    iconCircle: { width: 40, height: 40, borderRadius: 10, alignItems: 'center', justifyContent: 'center' },
    reportName: { color: COLORS.textPrimary, fontWeight: '600', fontSize: 14 },
    reportDate: { color: COLORS.textMuted, fontSize: 11, marginTop: 2 },
    typeBadge: { backgroundColor: COLORS.primaryLight, paddingHorizontal: 8, paddingVertical: 4, borderRadius: 8 },
    typeBadgeText: { color: COLORS.primary, fontSize: 10, fontWeight: '700' },
    empty: { alignItems: 'center', padding: 40, gap: 8 },
    emptyText: { color: COLORS.textSecond, textAlign: 'center', fontSize: 14 },
    disclaimer: {
        flexDirection: 'row', alignItems: 'center', marginTop: 20, paddingTop: 16,
        borderTopWidth: 1, borderTopColor: COLORS.border
    },
    disclaimerText: { color: COLORS.textMuted, fontSize: 11, flex: 1 },
});
