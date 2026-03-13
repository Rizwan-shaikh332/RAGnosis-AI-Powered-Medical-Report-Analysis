import React, { useMemo } from 'react';
import {
    View, Text, ScrollView, StyleSheet
} from 'react-native';
import { COLORS, METRIC_CATALOG, getMetricStatus } from '../constants/theme';

const STATUS_LABEL = { high: 'HIGH ↑', low: 'LOW ↓', normal: 'NORMAL ✓' };
const STATUS_COLOR = { high: '#ef4444', low: '#f59e0b', normal: '#10b981' };

function MetricBar({ info }) {
    const c = STATUS_COLOR[info.status] || '#8b949e';
    const barWidth = 220;
    const markerX = (info.pct / 100) * barWidth;
    const loX = (info.loPct / 100) * barWidth;
    const hiX = (info.hiPct / 100) * barWidth;
    const zoneW = Math.max(0, hiX - loX);

    return (
        <View style={mb.card}>
            <View style={mb.headerRow}>
                <Text style={mb.label}>{info.label}</Text>
                <View style={[mb.chip, { backgroundColor: c + '22', borderColor: c }]}>
                    <Text style={[mb.chipText, { color: c }]}>{STATUS_LABEL[info.status]}</Text>
                </View>
            </View>
            <View style={mb.valueRow}>
                <Text style={[mb.value, { color: c }]}>{info.value}</Text>
                <Text style={mb.unit}> {info.unit}</Text>
                <Text style={mb.range}>  Normal: {info.normal_range}</Text>
            </View>
            {/* Range bar */}
            <View style={[mb.track, { width: barWidth }]}>
                <View style={[mb.zone, { left: loX, width: zoneW }]} />
                <View style={[mb.marker, { left: Math.max(0, Math.min(barWidth - 8, markerX - 4)), backgroundColor: c }]} />
            </View>
            <View style={[mb.trackLabels, { width: barWidth }]}>
                <Text style={mb.trackLabel}>Low</Text>
                <Text style={mb.trackLabel}>High</Text>
            </View>
        </View>
    );
}

const mb = StyleSheet.create({
    card: { backgroundColor: COLORS.card, borderRadius: 14, padding: 14, borderWidth: 1, borderColor: COLORS.border, marginBottom: 10 },
    headerRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 },
    label: { color: COLORS.textPrimary, fontWeight: '700', fontSize: 14 },
    chip: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: 8, borderWidth: 1 },
    chipText: { fontSize: 10, fontWeight: '800' },
    valueRow: { flexDirection: 'row', alignItems: 'baseline', marginBottom: 10 },
    value: { fontWeight: '900', fontSize: 22 },
    unit: { color: COLORS.textMuted, fontSize: 12 },
    range: { color: COLORS.textMuted, fontSize: 10 },
    track: { height: 8, backgroundColor: COLORS.bg, borderRadius: 4, marginBottom: 2, overflow: 'hidden', position: 'relative' },
    zone: { position: 'absolute', height: '100%', backgroundColor: '#10b981', opacity: 0.35, borderRadius: 4 },
    marker: { position: 'absolute', width: 8, height: 8, borderRadius: 4, top: 0 },
    trackLabels: { flexDirection: 'row', justifyContent: 'space-between' },
    trackLabel: { color: COLORS.textMuted, fontSize: 9 },
});

export default function ReportDetailScreen({ route }) {
    const report = route.params?.report || {};
    const metrics = report.metrics || {};

    const recs = useMemo(() =>
        Object.entries(metrics)
            .map(([k, v]) => getMetricStatus(k, v))
            .filter(Boolean),
        [metrics]);

    const elevated = recs.filter(r => r.status === 'high');
    const belowNorm = recs.filter(r => r.status === 'low');
    const normal = recs.filter(r => r.status === 'normal');

    return (
        <ScrollView style={s.root} contentContainerStyle={s.scroll}>
            {/* Header */}
            <Text style={s.filename} numberOfLines={1}>{report.original_name}</Text>
            <View style={s.badgeRow}>
                <Text style={s.typeBadge}>{report.report_type}</Text>
                {elevated.length > 0 && (
                    <Text style={[s.statusBadge, { backgroundColor: 'rgba(239,68,68,0.15)', color: '#ef4444' }]}>
                        ⬆ {elevated.length} Elevated
                    </Text>
                )}
            </View>

            {/* Status summary boxes */}
            <View style={s.boxRow}>
                <View style={[s.box, { borderColor: '#ef4444' }]}>
                    <Text style={[s.boxIcon]}>⬆️</Text>
                    <Text style={[s.boxTitle, { color: '#ef4444' }]}>Elevated</Text>
                    {elevated.length === 0
                        ? <Text style={s.boxNone}>All within range ✓</Text>
                        : elevated.map(r => (
                            <Text key={r.key} style={s.boxItem}>• {r.label} {r.value} {r.unit}</Text>
                        ))}
                </View>
                <View style={[s.box, { borderColor: '#f59e0b' }]}>
                    <Text style={s.boxIcon}>⚠️</Text>
                    <Text style={[s.boxTitle, { color: '#f59e0b' }]}>Below Normal</Text>
                    {belowNorm.length === 0
                        ? <Text style={s.boxNone}>None — all in range ✓</Text>
                        : belowNorm.map(r => (
                            <Text key={r.key} style={s.boxItem}>• {r.label} {r.value} {r.unit}</Text>
                        ))}
                </View>
                <View style={[s.box, { borderColor: '#10b981' }]}>
                    <Text style={s.boxIcon}>✅</Text>
                    <Text style={[s.boxTitle, { color: '#10b981' }]}>Normal</Text>
                    {normal.length === 0
                        ? <Text style={s.boxNone}>—</Text>
                        : normal.map(r => (
                            <Text key={r.key} style={s.boxItem}>• {r.label}</Text>
                        ))}
                </View>
            </View>

            {/* Metric range bars */}
            {recs.length > 0 && (
                <>
                    <Text style={s.section}>📊 Lab Values at a Glance</Text>
                    {recs.map(info => <MetricBar key={info.key} info={info} />)}
                </>
            )}

            {/* AI Summary */}
            <Text style={s.section}>🧠 AI Summary</Text>
            <View style={s.summaryCard}>
                <Text style={s.summaryText}>{report.summary || 'No summary available.'}</Text>
            </View>

            {/* Data table */}
            {recs.length > 0 && (
                <>
                    <Text style={s.section}>📋 Report Data</Text>
                    <View style={s.table}>
                        <View style={s.tableHead}>
                            <Text style={[s.thCell, { flex: 2 }]}>Parameter</Text>
                            <Text style={s.thCell}>Value</Text>
                            <Text style={s.thCell}>Status</Text>
                        </View>
                        {recs.map(r => {
                            const c = STATUS_COLOR[r.status] || '#8b949e';
                            return (
                                <View key={r.key} style={s.tableRow}>
                                    <Text style={[s.tdCell, { flex: 2 }]}>{r.label}</Text>
                                    <Text style={[s.tdCell, { color: c }]}>{r.value} {r.unit}</Text>
                                    <View style={[s.statusChip, { backgroundColor: c + '22' }]}>
                                        <Text style={[s.statusChipText, { color: c }]}>{STATUS_LABEL[r.status]}</Text>
                                    </View>
                                </View>
                            );
                        })}
                    </View>
                </>
            )}

            {recs.length === 0 && (
                <View style={s.noMetrics}>
                    <Text style={{ fontSize: 36 }}>🔬</Text>
                    <Text style={s.noMetricsText}>No metrics extracted. Try re-uploading the report or use a clearer scan.</Text>
                </View>
            )}
        </ScrollView>
    );
}

const s = StyleSheet.create({
    root: { flex: 1, backgroundColor: COLORS.bg },
    scroll: { padding: 16, paddingBottom: 40 },
    filename: { color: COLORS.textPrimary, fontWeight: '800', fontSize: 18, marginBottom: 8 },
    badgeRow: { flexDirection: 'row', gap: 8, marginBottom: 16, flexWrap: 'wrap' },
    typeBadge: {
        backgroundColor: COLORS.primaryLight, color: COLORS.primary,
        paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8, fontWeight: '700', fontSize: 12
    },
    statusBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8, fontWeight: '700', fontSize: 12 },
    boxRow: { flexDirection: 'row', gap: 8, marginBottom: 20 },
    box: { flex: 1, backgroundColor: COLORS.card, borderRadius: 14, borderWidth: 1, padding: 10, gap: 4 },
    boxIcon: { fontSize: 16 },
    boxTitle: { fontWeight: '800', fontSize: 12 },
    boxNone: { color: COLORS.textMuted, fontSize: 10 },
    boxItem: { color: COLORS.textSecond, fontSize: 10 },
    section: { color: COLORS.textPrimary, fontWeight: '700', fontSize: 15, marginBottom: 10, marginTop: 6 },
    summaryCard: {
        backgroundColor: COLORS.card, borderRadius: 14, padding: 14,
        borderWidth: 1, borderColor: COLORS.border, marginBottom: 16
    },
    summaryText: { color: COLORS.textSecond, fontSize: 13, lineHeight: 22 },
    table: { backgroundColor: COLORS.card, borderRadius: 14, borderWidth: 1, borderColor: COLORS.border, overflow: 'hidden' },
    tableHead: { flexDirection: 'row', backgroundColor: 'rgba(124,58,237,0.1)', padding: 10 },
    thCell: { flex: 1, color: COLORS.textMuted, fontWeight: '700', fontSize: 11 },
    tableRow: { flexDirection: 'row', alignItems: 'center', padding: 10, borderTopWidth: 1, borderTopColor: COLORS.border },
    tdCell: { flex: 1, color: COLORS.textPrimary, fontSize: 12 },
    statusChip: { paddingHorizontal: 6, paddingVertical: 2, borderRadius: 6 },
    statusChipText: { fontSize: 9, fontWeight: '800' },
    noMetrics: { alignItems: 'center', gap: 10, padding: 40 },
    noMetricsText: { color: COLORS.textSecond, textAlign: 'center', fontSize: 13, lineHeight: 22 },
});
