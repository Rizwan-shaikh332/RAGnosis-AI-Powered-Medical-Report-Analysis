import React, { useState, useCallback } from 'react';
import {
    View, Text, FlatList, StyleSheet, TouchableOpacity,
    RefreshControl, ActivityIndicator
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import api from '../api/client';
import { COLORS } from '../constants/theme';

const TYPE_COLORS = {
    'Blood / CBC Report': '#ef4444',
    'Lipid Panel Report': '#f59e0b',
    'Diabetes / Glucose Report': '#10b981',
    'Kidney Function Report': '#22d3ee',
    'Liver Function Report': '#a78bfa',
    'Thyroid Report': '#fb923c',
    'Blood Pressure': '#60a5fa',
    'Radiology Report': '#94a3b8',
};

export default function ReportsScreen({ navigation }) {
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refresh, setRefresh] = useState(false);

    const load = useCallback(async () => {
        try {
            const res = await api.get('/reports/');
            setReports(res.data.reports || []);
        } catch (_) { }
        setLoading(false);
        setRefresh(false);
    }, []);

    useFocusEffect(useCallback(() => { load(); }, [load]));

    const openReport = async (id) => {
        try {
            const res = await api.get(`/reports/${id}`);
            navigation.navigate('ReportDetail', { report: res.data });
        } catch (_) { }
    };

    if (loading) return (
        <View style={[s.root, { justifyContent: 'center', alignItems: 'center' }]}>
            <ActivityIndicator color={COLORS.primary} size="large" />
        </View>
    );

    const renderItem = ({ item: r }) => {
        const color = TYPE_COLORS[r.report_type] || COLORS.primary;
        const mCount = Object.keys(r.metrics || {}).length;
        return (
            <TouchableOpacity style={s.row} onPress={() => openReport(r._id)} activeOpacity={0.75}>
                <View style={[s.dot, { backgroundColor: color + '22', borderColor: color }]}>
                    <Ionicons name="document-text" size={18} color={color} />
                </View>
                <View style={{ flex: 1 }}>
                    <Text style={s.name} numberOfLines={1}>{r.original_name}</Text>
                    <View style={s.meta}>
                        <Text style={s.type}>{r.report_type}</Text>
                        {mCount > 0 && <Text style={s.metrics}>{mCount} metrics</Text>}
                    </View>
                </View>
                <Text style={s.date}>{new Date(r.uploaded_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' })}</Text>
                <Ionicons name="chevron-forward" size={16} color={COLORS.textMuted} />
            </TouchableOpacity>
        );
    };

    return (
        <View style={s.root}>
            <View style={s.header}>
                <Text style={s.heading}>My Reports</Text>
                <View style={s.countBadge}><Text style={s.countText}>{reports.length}</Text></View>
            </View>
            <FlatList
                data={reports}
                keyExtractor={r => r._id}
                renderItem={renderItem}
                contentContainerStyle={{ padding: 16, paddingBottom: 40 }}
                refreshControl={<RefreshControl refreshing={refresh}
                    onRefresh={() => { setRefresh(true); load(); }} colors={[COLORS.primary]} />}
                ListEmptyComponent={
                    <View style={s.empty}>
                        <Text style={{ fontSize: 48 }}>📋</Text>
                        <Text style={s.emptyText}>No reports yet{'\n'}Go to Upload tab to add one!</Text>
                    </View>
                }
                ItemSeparatorComponent={() => <View style={s.sep} />}
            />
        </View>
    );
}

const s = StyleSheet.create({
    root: { flex: 1, backgroundColor: COLORS.bg },
    header: { flexDirection: 'row', alignItems: 'center', gap: 10, padding: 20, paddingBottom: 8 },
    heading: { color: COLORS.textPrimary, fontSize: 22, fontWeight: '800', flex: 1 },
    countBadge: { backgroundColor: COLORS.primaryLight, paddingHorizontal: 10, paddingVertical: 4, borderRadius: 100 },
    countText: { color: COLORS.primary, fontWeight: '700' },
    row: {
        flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: COLORS.card,
        borderRadius: 16, padding: 14, borderWidth: 1, borderColor: COLORS.border
    },
    dot: { width: 42, height: 42, borderRadius: 12, borderWidth: 1, alignItems: 'center', justifyContent: 'center' },
    name: { color: COLORS.textPrimary, fontWeight: '600', fontSize: 14, marginBottom: 4 },
    meta: { flexDirection: 'row', gap: 8, alignItems: 'center' },
    type: { color: COLORS.textSecond, fontSize: 11 },
    metrics: {
        backgroundColor: COLORS.primaryLight, color: COLORS.primary,
        paddingHorizontal: 6, paddingVertical: 1, borderRadius: 6, fontSize: 10, fontWeight: '700'
    },
    date: { color: COLORS.textMuted, fontSize: 11 },
    sep: { height: 8 },
    empty: { alignItems: 'center', paddingTop: 80, gap: 10 },
    emptyText: { color: COLORS.textSecond, textAlign: 'center', fontSize: 14, lineHeight: 22 },
});
