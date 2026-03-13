import React, { useState } from 'react';
import {
    View, Text, StyleSheet, TouchableOpacity, ScrollView,
    Alert, ActivityIndicator, Platform
} from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import * as ImagePicker from 'expo-image-picker';
import { Ionicons } from '@expo/vector-icons';
import api from '../api/client';
import { COLORS, METRIC_CATALOG, getMetricStatus } from '../constants/theme';

const STATUS_COLOR = { high: '#ef4444', low: '#f59e0b', normal: '#10b981' };

export default function UploadScreen() {
    const [uploading, setUploading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);  // { type, message }

    const doUpload = async (uri, name, mimeType) => {
        setUploading(true);
        setResult(null);
        setError(null);
        try {
            const formData = new FormData();
            formData.append('file', { uri, name, type: mimeType || 'application/pdf' });
            const res = await api.post('/reports/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            setResult(res.data);
            Alert.alert('✅ Success', 'Report analyzed successfully!');
        } catch (err) {
            const status = err.response?.status;
            const data = err.response?.data || {};
            if (status === 422 && data.error === 'out_of_knowledge_base') {
                setError({ type: 'ook', message: data.message });
            } else if (status === 400 && data.error === 'unreadable') {
                setError({ type: 'unreadable', message: data.message });
            } else {
                Alert.alert('Upload Failed', data.message || 'Please try again');
            }
        } finally {
            setUploading(false);
        }
    };

    const pickDocument = async () => {
        const r = await DocumentPicker.getDocumentAsync({ type: ['application/pdf', 'image/*'] });
        if (!r.canceled && r.assets?.length)
            doUpload(r.assets[0].uri, r.assets[0].name, r.assets[0].mimeType);
    };

    const pickCamera = async () => {
        const perm = await ImagePicker.requestCameraPermissionsAsync();
        if (!perm.granted) { Alert.alert('Permission required', 'Allow camera access.'); return; }
        const r = await ImagePicker.launchCameraAsync({ quality: 0.9, mediaTypes: ImagePicker.MediaTypeOptions.Images });
        if (!r.canceled && r.assets?.length) {
            const uri = r.assets[0].uri;
            const name = 'scan_' + Date.now() + '.jpg';
            doUpload(uri, name, 'image/jpeg');
        }
    };

    return (
        <ScrollView style={s.root} contentContainerStyle={s.scroll}>
            <Text style={s.heading}>Upload Report</Text>
            <Text style={s.sub}>Supported: PDF, JPG, PNG, JPEG — Scans & digital reports</Text>

            {/* Upload buttons */}
            <View style={s.buttonRow}>
                <TouchableOpacity style={[s.uploadBtn, { borderColor: COLORS.primary }]} onPress={pickDocument}>
                    <Ionicons name="document-attach" size={28} color={COLORS.primary} />
                    <Text style={[s.uploadBtnText, { color: COLORS.primary }]}>Choose File (PDF/Image)</Text>
                    <Text style={s.uploadBtnSub}>From Files / Gallery</Text>
                </TouchableOpacity>

                <TouchableOpacity style={[s.uploadBtn, { borderColor: COLORS.cyan }]} onPress={pickCamera}>
                    <Ionicons name="camera" size={28} color={COLORS.cyan} />
                    <Text style={[s.uploadBtnText, { color: COLORS.cyan }]}>Capture Report</Text>
                    <Text style={s.uploadBtnSub}>Use Camera</Text>
                </TouchableOpacity>
            </View>

            {uploading && (
                <View style={s.loadingBox}>
                    <ActivityIndicator color={COLORS.primary} size="large" />
                    <Text style={s.loadingText}>⚙️ AI is analyzing your report…{'\n'}This may take 15–30 seconds</Text>
                </View>
            )}

            {/* OOK Error */}
            {error?.type === 'ook' && (
                <View style={[s.errorCard, { borderColor: '#f59e0b' }]}>
                    <Text style={[s.errorTitle, { color: '#f59e0b' }]}>🔬 Out of Knowledge Base</Text>
                    <Text style={s.errorMsg}>{error.message}</Text>
                    <Text style={s.errorHint}>Supported: CBC · Lipid · LFT · KFT · Thyroid · Diabetes · BP</Text>
                </View>
            )}

            {/* Unreadable Error */}
            {error?.type === 'unreadable' && (
                <View style={[s.errorCard, { borderColor: '#ef4444' }]}>
                    <Text style={[s.errorTitle, { color: '#ef4444' }]}>❌ Could Not Read File</Text>
                    <Text style={s.errorMsg}>{error.message}</Text>
                    <Text style={s.errorHint}>Tip: Use a well-lit, high-resolution scan (≥ 150 DPI)</Text>
                </View>
            )}

            {/* Success result */}
            {result && (
                <View style={s.resultCard}>
                    <View style={s.resultHeader}>
                        <Text style={s.resultBadge}>✅ Analysis Complete</Text>
                        <Text style={s.typeBadge}>{result.report_type}</Text>
                    </View>
                    <Text style={s.sectionTitle}>🧠 AI Summary</Text>
                    <Text style={s.summaryText}>{result.summary}</Text>

                    {result.metrics && Object.keys(result.metrics).length > 0 && (
                        <>
                            <Text style={s.sectionTitle}>📊 Extracted Values</Text>
                            <View style={s.metricsGrid}>
                                {Object.entries(result.metrics).map(([k, v]) => {
                                    const info = getMetricStatus(k, v);
                                    if (!info) return null;
                                    const c = STATUS_COLOR[info.status] || '#8b949e';
                                    return (
                                        <View key={k} style={[s.metricChip, { borderColor: c }]}>
                                            <Text style={s.metricLabel}>{info.label}</Text>
                                            <Text style={[s.metricVal, { color: c }]}>{v}</Text>
                                            <Text style={s.metricUnit}>{info.unit}</Text>
                                        </View>
                                    );
                                })}
                            </View>
                        </>
                    )}
                </View>
            )}
        </ScrollView>
    );
}

const s = StyleSheet.create({
    root: { flex: 1, backgroundColor: COLORS.bg },
    scroll: { padding: 20, paddingBottom: 40 },
    heading: { color: COLORS.textPrimary, fontSize: 22, fontWeight: '800', marginBottom: 6 },
    sub: { color: COLORS.textSecond, fontSize: 13, marginBottom: 24 },
    buttonRow: { gap: 12, marginBottom: 20 },
    uploadBtn: {
        backgroundColor: COLORS.card, borderWidth: 1.5, borderRadius: 18, padding: 20,
        borderStyle: 'dashed', alignItems: 'center', gap: 8
    },
    uploadBtnText: { fontWeight: '700', fontSize: 15 },
    uploadBtnSub: { color: COLORS.textMuted, fontSize: 12 },
    loadingBox: { alignItems: 'center', gap: 12, padding: 24, marginBottom: 16 },
    loadingText: { color: COLORS.textSecond, textAlign: 'center', lineHeight: 22 },
    errorCard: { backgroundColor: COLORS.card, borderWidth: 1, borderRadius: 16, padding: 20, marginBottom: 16 },
    errorTitle: { fontWeight: '800', fontSize: 15, marginBottom: 8 },
    errorMsg: { color: COLORS.textSecond, fontSize: 13, lineHeight: 20, marginBottom: 8 },
    errorHint: { color: COLORS.textMuted, fontSize: 12 },
    resultCard: {
        backgroundColor: COLORS.card, borderRadius: 18, padding: 20,
        borderWidth: 1, borderColor: COLORS.border, marginBottom: 20
    },
    resultHeader: { flexDirection: 'row', gap: 8, marginBottom: 16, flexWrap: 'wrap' },
    resultBadge: {
        backgroundColor: 'rgba(16,185,129,0.15)', color: '#10b981', paddingHorizontal: 10,
        paddingVertical: 4, borderRadius: 8, fontWeight: '700', fontSize: 12
    },
    typeBadge: {
        backgroundColor: COLORS.primaryLight, color: COLORS.primary,
        paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8, fontWeight: '700', fontSize: 12
    },
    sectionTitle: { color: COLORS.textPrimary, fontWeight: '700', fontSize: 14, marginBottom: 10, marginTop: 12 },
    summaryText: { color: COLORS.textSecond, fontSize: 13, lineHeight: 22 },
    metricsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
    metricChip: { backgroundColor: COLORS.bg, borderWidth: 1, borderRadius: 12, padding: 10, minWidth: 100, gap: 2 },
    metricLabel: { color: COLORS.textMuted, fontSize: 10 },
    metricVal: { fontWeight: '800', fontSize: 18 },
    metricUnit: { color: COLORS.textMuted, fontSize: 10 },
});
