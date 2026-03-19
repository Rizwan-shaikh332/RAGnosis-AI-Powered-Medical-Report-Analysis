import React, { useState, useEffect } from 'react';
import {
    View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert, ActivityIndicator
} from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { MaterialIcons, FontAwesome5 } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { COLORS } from '../constants/theme';
import { BASE_URL } from './ChatScreen';

const HEALTH_METRICS = {
    hemoglobin: { label: 'Hemoglobin', unit: 'g/dL', normal: { min: 12, max: 17 }, icon: '🩸' },
    glucose: { label: 'Blood Glucose', unit: 'mg/dL', normal: { min: 70, max: 100 }, icon: '🍬' },
    cholesterol: { label: 'Total Cholesterol', unit: 'mg/dL', normal: { min: 100, max: 200 }, icon: '❤️' },
    triglycerides: { label: 'Triglycerides', unit: 'mg/dL', normal: { min: 0, max: 150 }, icon: '🔥' },
    hdl: { label: 'HDL (Good)', unit: 'mg/dL', normal: { min: 60, max: 999 }, icon: '⬆️' },
    ldl: { label: 'LDL (Bad)', unit: 'mg/dL', normal: { min: 0, max: 100 }, icon: '⬇️' },
    wbc: { label: 'White Blood Cells', unit: 'k/µL', normal: { min: 4.5, max: 11 }, icon: '🛡️' },
    rbc: { label: 'Red Blood Cells', unit: 'M/µL', normal: { min: 4.0, max: 5.5 }, icon: '⭕' },
    platelets: { label: 'Platelets', unit: 'k/µL', normal: { min: 150, max: 400 }, icon: '🩹' },
    creatinine: { label: 'Creatinine', unit: 'mg/dL', normal: { min: 0.5, max: 1.2 }, icon: '🫘' },
    urea: { label: 'Blood Urea', unit: 'mg/dL', normal: { min: 7, max: 20 }, icon: '💧' },
    sgpt: { label: 'SGPT (ALT)', unit: 'U/L', normal: { min: 7, max: 56 }, icon: '🧬' },
    sgot: { label: 'SGOT (AST)', unit: 'U/L', normal: { min: 10, max: 40 }, icon: '🧫' },
    tsh: { label: 'TSH (Thyroid)', unit: 'mIU/L', normal: { min: 0.4, max: 4.0 }, icon: '🦋' },
    systolic_bp: { label: 'Systolic BP', unit: 'mmHg', normal: { min: 90, max: 120 }, icon: '💓' },
    diastolic_bp: { label: 'Diastolic BP', unit: 'mmHg', normal: { min: 60, max: 80 }, icon: '💗' },
};

function getHealthStatus(value, range) {
    if (value < range.min) return 'low';
    if (value > range.max) return 'high';
    return 'normal';
}

function HealthScoreCard({ score, normalCount, totalMetrics }) {
    const getScoreLevel = (s) => {
        if (s >= 80) return { text: 'Excellent', color: COLORS.success };
        if (s >= 60) return { text: 'Good', color: COLORS.primary };
        if (s >= 40) return { text: 'Fair', color: COLORS.yellow };
        return { text: 'Needs Attention', color: COLORS.danger };
    };

    const level = getScoreLevel(score);

    return (
        <View style={[s.scoreCard, { borderLeftColor: level.color, borderLeftWidth: 4 }]}>
            <Text style={s.scoreTitle}>📊 Overall Health Score</Text>
            <Text style={[s.scoreValue, { color: level.color }]}>{score}%</Text>
            <Text style={[s.scoreLevel, { color: level.color }]}>{level.text}</Text>
            <Text style={s.scoreDetail}>
                {normalCount} out of {totalMetrics} metrics normal
            </Text>
        </View>
    );
}

function MetricCard({ metric, value, status }) {
    const statusColor = status === 'low' ? COLORS.yellow : status === 'high' ? COLORS.danger : COLORS.success;
    const statusText = status === 'low' ? '↓ LOW' : status === 'high' ? '↑ HIGH' : '✓ NORMAL';

    return (
        <View style={[s.metricCard, status !== 'normal' && { borderLeftColor: statusColor, borderLeftWidth: 3 }]}>
            <View style={s.metricHeader}>
                <View>
                    <Text style={[s.metricLabel, status !== 'normal' && { color: statusColor }]}>
                        {metric.icon} {metric.label}
                    </Text>
                    <Text style={s.metricRange}>
                        Normal: {metric.normal.min}–{metric.normal.max} {metric.unit}
                    </Text>
                </View>
                <View style={s.metricValue}>
                    <Text style={[s.value, { color: statusColor }]}>{value}</Text>
                    <Text style={s.unit}>{metric.unit}</Text>
                </View>
            </View>
            <Text style={[s.status, { color: statusColor }]}>{statusText}</Text>
        </View>
    );
}

export default function HealthScreen() {
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);

    useEffect(() => {
        fetchReports();
    }, []);

    const fetchReports = async () => {
        try {
            const token = await SecureStore.getItemAsync('auth_token');
            if (!token) {
                Alert.alert('Error', 'Please login first');
                return;
            }

            const response = await fetch(`${BASE_URL}/api/reports/`, {
                headers: { Authorization: `Bearer ${token}` }
            });

            if (!response.ok) throw new Error('Failed to fetch reports');

            const data = await response.json();
            setReports(data.reports || []);
        } catch (error) {
            console.error('Error fetching reports:', error);
            Alert.alert('Error', 'Failed to load health data');
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    const onRefresh = async () => {
        setRefreshing(true);
        await fetchReports();
    };

    if (loading) {
        return (
            <View style={[s.root, { justifyContent: 'center', alignItems: 'center' }]}>
                <ActivityIndicator size="large" color={COLORS.primary} />
            </View>
        );
    }

    if (reports.length === 0) {
        return (
            <ScrollView style={s.root} contentContainerStyle={s.emptyContainer}>
                <View style={s.emptyState}>
                    <Text style={s.emptyIcon}>📋</Text>
                    <Text style={s.emptyTitle}>No Health Records Yet</Text>
                    <Text style={s.emptyText}>
                        Upload your first medical report to see your health metrics and recommendations
                    </Text>
                    <TouchableOpacity style={s.uploadButton}>
                        <MaterialIcons name="cloud-upload" size={20} color="#fff" />
                        <Text style={s.uploadButtonText}>Upload Report</Text>
                    </TouchableOpacity>
                </View>
            </ScrollView>
        );
    }

    // Calculate health score
    let totalMetrics = 0;
    let normalCount = 0;
    const abnormalMetrics = [];
    const normalMetrics = [];

    reports.forEach(report => {
        if (report.metrics && typeof report.metrics === 'object') {
            Object.entries(report.metrics).forEach(([key, value]) => {
                if (HEALTH_METRICS[key] && value != null) {
                    totalMetrics++;
                    const status = getHealthStatus(value, HEALTH_METRICS[key].normal);
                    const metric = { key, ...HEALTH_METRICS[key], value, status };

                    if (status === 'normal') {
                        normalCount++;
                        normalMetrics.push(metric);
                    } else {
                        abnormalMetrics.push(metric);
                    }
                }
            });
        }
    });

    const healthScore = totalMetrics > 0 ? Math.round((normalCount / totalMetrics) * 100) : 0;

    // Get recommendations
    const allRecommendations = [];
    reports.forEach(report => {
        if (report.recommendations && Array.isArray(report.recommendations)) {
            report.recommendations.forEach(rec => {
                if (!allRecommendations.find(r => r === rec)) {
                    allRecommendations.push(rec);
                }
            });
        }
    });

    return (
        <ScrollView
            style={s.root}
            contentContainerStyle={s.scroll}
            scrollEventThrottle={16}
            refreshing={refreshing}
            onRefresh={onRefresh}
        >
            {/* Header */}
            <View style={s.header}>
                <Text style={s.title}>💚 Your Health</Text>
                <Text style={s.subtitle}>Track your health metrics</Text>
            </View>

            {/* Health Score */}
            <HealthScoreCard score={healthScore} normalCount={normalCount} totalMetrics={totalMetrics} />

            {/* Latest Metrics Section */}
            {reports[0]?.metrics && (
                <View style={s.section}>
                    <Text style={s.sectionTitle}>
                        {abnormalMetrics.length > 0 ? '⚠️ Values Needing Attention' : '✅ Latest Metrics'}
                    </Text>
                    {abnormalMetrics.length > 0 && (
                        <View>
                            {abnormalMetrics.map(m => (
                                <MetricCard key={m.key} metric={m} value={m.value} status={m.status} />
                            ))}
                        </View>
                    )}

                    {normalMetrics.length > 0 && (
                        <View style={{ marginTop: 12 }}>
                            <Text style={s.subSectionTitle}>✅ Normal Values</Text>
                            {normalMetrics.slice(0, 5).map(m => (
                                <MetricCard key={m.key} metric={m} value={m.value} status={m.status} />
                            ))}
                        </View>
                    )}
                </View>
            )}

            {/* Recommendations */}
            {allRecommendations.length > 0 && (
                <View style={s.section}>
                    <Text style={s.sectionTitle}>💡 What You Need To Do</Text>
                    <View style={s.recommendationList}>
                        {allRecommendations.slice(0, 8).map((rec, i) => (
                            <View key={i} style={s.recommendationItem}>
                                <Text style={s.recommendationBullet}>→</Text>
                                <Text style={s.recommendationText}>{rec}</Text>
                            </View>
                        ))}
                        {allRecommendations.length > 8 && (
                            <Text style={s.moreRecommendations}>
                                ... and {allRecommendations.length - 8} more recommendations
                            </Text>
                        )}
                    </View>
                </View>
            )}

            {/* Report Info */}
            <View style={s.section}>
                <Text style={s.sectionTitle}>📋 Report Info</Text>
                <View style={s.infoCard}>
                    <View style={s.infoRow}>
                        <MaterialIcons name="today" size={18} color={COLORS.primary} />
                        <View style={{ flex: 1, marginLeft: 12 }}>
                            <Text style={s.infoLabel}>Latest Report</Text>
                            <Text style={s.infoValue}>
                                {new Date(reports[0].uploaded_at).toLocaleDateString('en-US', {
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric'
                                })}
                            </Text>
                        </View>
                    </View>
                    <View style={s.divider} />
                    <View style={s.infoRow}>
                        <MaterialIcons name="assessment" size={18} color={COLORS.primary} />
                        <View style={{ flex: 1, marginLeft: 12 }}>
                            <Text style={s.infoLabel}>Total Reports</Text>
                            <Text style={s.infoValue}>{reports.length}</Text>
                        </View>
                    </View>
                </View>
            </View>

            {/* Disclaimer */}
            <View style={s.disclaimer}>
                <MaterialIcons name="info" size={16} color={COLORS.yellow} />
                <Text style={s.disclaimerText}>
                    RAGnosis uses AI for preliminary analysis only. Always consult a qualified healthcare provider for diagnosis and treatment.
                </Text>
            </View>
        </ScrollView>
    );
}

const s = StyleSheet.create({
    root: { flex: 1, backgroundColor: COLORS.bg },
    scroll: { paddingHorizontal: 16, paddingBottom: 40 },
    emptyContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', paddingBottom: 40 },
    emptyState: { alignItems: 'center', paddingHorizontal: 20 },
    emptyIcon: { fontSize: 60, marginBottom: 12 },
    emptyTitle: { fontSize: 18, fontWeight: '900', color: COLORS.textPrimary, marginBottom: 8 },
    emptyText: { fontSize: 13, color: COLORS.textMuted, textAlign: 'center', marginBottom: 20 },
    uploadButton: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: COLORS.primary,
        paddingHorizontal: 20,
        paddingVertical: 12,
        borderRadius: 8,
        gap: 8
    },
    uploadButtonText: { color: '#fff', fontWeight: '600', fontSize: 14 },

    header: { marginTop: 16, marginBottom: 24 },
    title: { fontSize: 28, fontWeight: '900', color: COLORS.textPrimary },
    subtitle: { fontSize: 13, color: COLORS.textMuted, marginTop: 4 },

    scoreCard: {
        backgroundColor: COLORS.card,
        padding: 18,
        borderRadius: 12,
        borderColor: COLORS.border,
        borderWidth: 1,
        marginBottom: 24
    },
    scoreTitle: { fontSize: 12, color: COLORS.textMuted, marginBottom: 8 },
    scoreValue: { fontSize: 40, fontWeight: '900', lineHeight: 44 },
    scoreLevel: { fontSize: 16, fontWeight: '700', marginTop: 4 },
    scoreDetail: { fontSize: 12, color: COLORS.textMuted, marginTop: 8 },

    section: { marginBottom: 24 },
    sectionTitle: { fontSize: 16, fontWeight: '700', color: COLORS.textPrimary, marginBottom: 12 },
    subSectionTitle: { fontSize: 13, fontWeight: '600', color: COLORS.success, marginBottom: 12 },

    metricCard: {
        backgroundColor: COLORS.card,
        padding: 14,
        borderRadius: 10,
        borderColor: COLORS.border,
        borderWidth: 1,
        marginBottom: 10
    },
    metricHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
    metricLabel: { fontSize: 13, fontWeight: '600', color: COLORS.textPrimary, marginBottom: 4 },
    metricRange: { fontSize: 11, color: COLORS.textMuted },
    metricValue: { alignItems: 'flex-end' },
    value: { fontSize: 20, fontWeight: '900' },
    unit: { fontSize: 10, color: COLORS.textMuted },
    status: { fontSize: 11, fontWeight: '700', marginTop: 8 },

    recommendationList: { backgroundColor: COLORS.card, padding: 14, borderRadius: 10, borderColor: COLORS.border, borderWidth: 1 },
    recommendationItem: { flexDirection: 'row', alignItems: 'flex-start', marginBottom: 12, gap: 8 },
    recommendationBullet: { fontSize: 14, color: COLORS.primary, fontWeight: '900', width: 16 },
    recommendationText: { flex: 1, fontSize: 12, color: COLORS.textSecondary, lineHeight: 18 },
    moreRecommendations: { fontSize: 11, color: COLORS.textMuted, fontStyle: 'italic', marginTop: 8 },

    infoCard: { backgroundColor: COLORS.card, borderRadius: 10, borderColor: COLORS.border, borderWidth: 1, overflow: 'hidden' },
    infoRow: { flexDirection: 'row', alignItems: 'center', padding: 14 },
    divider: { height: 1, backgroundColor: COLORS.border },
    infoLabel: { fontSize: 12, color: COLORS.textMuted },
    infoValue: { fontSize: 13, fontWeight: '700', color: COLORS.textPrimary, marginTop: 2 },

    disclaimer: {
        flexDirection: 'row',
        backgroundColor: 'rgba(245, 158, 11, 0.15)',
        borderColor: COLORS.yellow,
        borderWidth: 1,
        borderRadius: 10,
        padding: 12,
        alignItems: 'flex-start',
        gap: 8,
        marginTop: 8,
        marginBottom: 24
    },
    disclaimerText: { flex: 1, fontSize: 11, color: COLORS.textMuted, lineHeight: 16 }
});
