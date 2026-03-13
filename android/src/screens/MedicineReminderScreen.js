import React, { useState, useEffect, useCallback } from 'react';
import {
    View, Text, StyleSheet, TouchableOpacity, ScrollView,
    TextInput, Modal, Alert, Switch, RefreshControl,
    KeyboardAvoidingView, Platform, ActivityIndicator
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Notifications from 'expo-notifications';
import api from '../api/client';
import { COLORS } from '../constants/theme';

// ── Notification configuration ────────────────────────────────────────────────
Notifications.setNotificationHandler({
    handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: false,
    }),
});

async function requestNotificationPermissions() {
    const { status: existing } = await Notifications.getPermissionsAsync();
    if (existing === 'granted') return true;
    const { status } = await Notifications.requestPermissionsAsync();
    return status === 'granted';
}

async function scheduleReminderNotifications(reminderId, medicineName, dosage, times) {
    const granted = await requestNotificationPermissions();
    if (!granted) {
        Alert.alert('Permission Denied', 'Enable notifications in Settings to receive medicine reminders.');
        return [];
    }

    const scheduleIds = [];
    for (const t of times) {
        const id = await Notifications.scheduleNotificationAsync({
            content: {
                title: `💊 Medicine Reminder`,
                body: `Time to take ${medicineName}${dosage ? ` — ${dosage}` : ''}`,
                data: { reminderId, medicineName },
                sound: true,
            },
            trigger: {
                type: Notifications.SchedulableTriggerInputTypes.DAILY,
                hour: t.hour,
                minute: t.minute,
            },
        });
        scheduleIds.push(id);
    }
    return scheduleIds;
}

async function cancelReminderNotifications(notifIds = []) {
    for (const id of notifIds) {
        try { await Notifications.cancelScheduledNotificationAsync(id); } catch (_) { }
    }
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function pad(n) { return String(n).padStart(2, '0'); }
function timeLabel(h, m) {
    const suffix = h < 12 ? 'AM' : 'PM';
    const hour = h % 12 === 0 ? 12 : h % 12;
    return `${pad(hour)}:${pad(m)} ${suffix}`;
}

// ── Local notification IDs stored per reminder (in memory) ───────────────────
const notifMap = {}; // { reminderId: [notifId1, notifId2] }

// ── Main component ────────────────────────────────────────────────────────────
export default function MedicineReminderScreen() {
    const [reminders, setReminders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);

    // Form state
    const [medName, setMedName] = useState('');
    const [dosage, setDosage] = useState('');
    const [notes, setNotes] = useState('');
    const [hour, setHour] = useState('8');
    const [minute, setMinute] = useState('0');
    const [saving, setSaving] = useState(false);

    const load = useCallback(async () => {
        try {
            const res = await api.get('/reminders/');
            setReminders(res.data.reminders || []);
        } catch (_) { }
        setLoading(false);
        setRefreshing(false);
    }, []);

    useEffect(() => {
        load();
        requestNotificationPermissions();
    }, [load]);

    // Schedule notifications for all active reminders on mount
    useEffect(() => {
        reminders.forEach(async (r) => {
            if (r.active && !notifMap[r._id]) {
                const ids = await scheduleReminderNotifications(r._id, r.medicine_name, r.dosage, r.times);
                notifMap[r._id] = ids;
            }
        });
    }, [reminders]);

    const openAddModal = () => {
        setMedName(''); setDosage(''); setNotes(''); setHour('8'); setMinute('0');
        setModalVisible(true);
    };

    const handleSave = async () => {
        if (!medName.trim()) { Alert.alert('Error', 'Medicine name is required'); return; }
        const h = parseInt(hour, 10);
        const m = parseInt(minute, 10);
        if (isNaN(h) || h < 0 || h > 23) { Alert.alert('Error', 'Hour must be 0-23'); return; }
        if (isNaN(m) || m < 0 || m > 59) { Alert.alert('Error', 'Minute must be 0-59'); return; }

        setSaving(true);
        try {
            const times = [{ hour: h, minute: m, label: timeLabel(h, m) }];
            const res = await api.post('/reminders/', {
                medicine_name: medName.trim(),
                dosage: dosage.trim(),
                notes: notes.trim(),
                times,
                frequency: 'daily',
            });
            const rid = res.data.reminder_id;
            // Schedule local notification
            const ids = await scheduleReminderNotifications(rid, medName.trim(), dosage.trim(), times);
            notifMap[rid] = ids;
            setModalVisible(false);
            await load();
            Alert.alert('✅ Reminder Set!', `You'll be reminded to take ${medName.trim()} at ${timeLabel(h, m)} every day.`);
        } catch (err) {
            Alert.alert('Error', err.response?.data?.error || 'Could not save reminder');
        } finally {
            setSaving(false);
        }
    };

    const handleDelete = (reminder) => {
        Alert.alert('Delete Reminder', `Remove reminder for ${reminder.medicine_name}?`, [
            { text: 'Cancel', style: 'cancel' },
            {
                text: 'Delete', style: 'destructive', onPress: async () => {
                    try {
                        await api.delete(`/reminders/${reminder._id}`);
                        await cancelReminderNotifications(notifMap[reminder._id] || []);
                        delete notifMap[reminder._id];
                        setReminders(prev => prev.filter(r => r._id !== reminder._id));
                    } catch (_) {
                        Alert.alert('Error', 'Could not delete reminder');
                    }
                }
            }
        ]);
    };

    const handleToggle = async (reminder) => {
        const newActive = !reminder.active;
        try {
            await api.put(`/reminders/${reminder._id}`, { active: newActive });
            if (newActive) {
                const ids = await scheduleReminderNotifications(
                    reminder._id, reminder.medicine_name, reminder.dosage, reminder.times
                );
                notifMap[reminder._id] = ids;
            } else {
                await cancelReminderNotifications(notifMap[reminder._id] || []);
                notifMap[reminder._id] = [];
            }
            setReminders(prev => prev.map(r => r._id === reminder._id ? { ...r, active: newActive } : r));
        } catch (_) {
            Alert.alert('Error', 'Could not update reminder');
        }
    };

    if (loading) return (
        <View style={[s.root, { justifyContent: 'center', alignItems: 'center' }]}>
            <ActivityIndicator color={COLORS.primary} size="large" />
        </View>
    );

    return (
        <View style={s.root}>
            {/* Header */}
            <View style={s.header}>
                <View>
                    <Text style={s.headerTitle}>Medicine Reminders 💊</Text>
                    <Text style={s.headerSub}>Daily dose tracker</Text>
                </View>
                <TouchableOpacity style={s.addBtn} onPress={openAddModal}>
                    <Ionicons name="add" size={22} color="#fff" />
                </TouchableOpacity>
            </View>

            <ScrollView style={s.list} contentContainerStyle={{ padding: 16, paddingBottom: 40 }}
                refreshControl={<RefreshControl refreshing={refreshing}
                    onRefresh={() => { setRefreshing(true); load(); }} colors={[COLORS.primary]} />}>

                {reminders.length === 0 ? (
                    <View style={s.empty}>
                        <Text style={{ fontSize: 52 }}>💊</Text>
                        <Text style={s.emptyTitle}>No reminders yet</Text>
                        <Text style={s.emptyText}>Tap + to add your first medicine reminder. Get daily notifications at your chosen time.</Text>
                        <TouchableOpacity style={s.emptyBtn} onPress={openAddModal}>
                            <Text style={s.emptyBtnText}>Add Medicine</Text>
                        </TouchableOpacity>
                    </View>
                ) : reminders.map(r => (
                    <View key={r._id} style={[s.card, !r.active && s.cardInactive]}>
                        <View style={s.cardTop}>
                            <View style={[s.pillIcon, { backgroundColor: r.active ? COLORS.primaryLight : 'rgba(100,100,100,0.15)' }]}>
                                <Ionicons name="medkit" size={20} color={r.active ? COLORS.primary : COLORS.textMuted} />
                            </View>
                            <View style={{ flex: 1 }}>
                                <Text style={[s.medName, !r.active && { color: COLORS.textMuted }]}>{r.medicine_name}</Text>
                                {r.dosage ? <Text style={s.dosage}>{r.dosage}</Text> : null}
                            </View>
                            <Switch
                                value={r.active}
                                onValueChange={() => handleToggle(r)}
                                trackColor={{ false: COLORS.border, true: COLORS.primaryLight }}
                                thumbColor={r.active ? COLORS.primary : COLORS.textMuted}
                            />
                            <TouchableOpacity style={s.deleteBtn} onPress={() => handleDelete(r)}>
                                <Ionicons name="trash-outline" size={18} color={COLORS.red} />
                            </TouchableOpacity>
                        </View>

                        {/* Times */}
                        <View style={s.timesRow}>
                            {(r.times || []).map((t, i) => (
                                <View key={i} style={[s.timeBadge, { backgroundColor: r.active ? 'rgba(124,58,237,0.18)' : 'rgba(100,100,100,0.1)' }]}>
                                    <Ionicons name="alarm-outline" size={12} color={r.active ? COLORS.primary : COLORS.textMuted} />
                                    <Text style={[s.timeText, { color: r.active ? COLORS.primary : COLORS.textMuted }]}>{t.label}</Text>
                                </View>
                            ))}
                        </View>

                        {r.notes ? (
                            <Text style={s.notes}>📝 {r.notes}</Text>
                        ) : null}

                        <View style={s.cardFooter}>
                            <Ionicons name={r.active ? 'notifications' : 'notifications-off'} size={12}
                                color={r.active ? COLORS.green : COLORS.textMuted} />
                            <Text style={[s.statusText, { color: r.active ? COLORS.green : COLORS.textMuted }]}>
                                {r.active ? 'Active — reminders ON' : 'Inactive — reminders OFF'}
                            </Text>
                        </View>
                    </View>
                ))}
            </ScrollView>

            {/* Add Medicine Modal */}
            <Modal visible={modalVisible} animationType="slide" transparent onRequestClose={() => setModalVisible(false)}>
                <KeyboardAvoidingView style={s.modalOverlay} behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
                    <View style={s.modalCard}>
                        <View style={s.modalHeader}>
                            <Text style={s.modalTitle}>Add Medicine 💊</Text>
                            <TouchableOpacity onPress={() => setModalVisible(false)}>
                                <Ionicons name="close" size={24} color={COLORS.textSecond} />
                            </TouchableOpacity>
                        </View>

                        <ScrollView showsVerticalScrollIndicator={false} keyboardShouldPersistTaps="handled">
                            <Text style={s.label}>Medicine Name *</Text>
                            <TextInput style={s.input} value={medName} onChangeText={setMedName}
                                placeholder="e.g. Metformin, Amlodipine..." placeholderTextColor={COLORS.textMuted} />

                            <Text style={s.label}>Dosage</Text>
                            <TextInput style={s.input} value={dosage} onChangeText={setDosage}
                                placeholder="e.g. 500mg, 1 tablet" placeholderTextColor={COLORS.textMuted} />

                            <Text style={s.label}>Reminder Time</Text>
                            <View style={s.timeRow}>
                                <View style={s.timeInputWrap}>
                                    <Text style={s.timeInputLabel}>Hour (0–23)</Text>
                                    <TextInput style={[s.input, s.timeInput]} value={hour} onChangeText={setHour}
                                        keyboardType="number-pad" maxLength={2} />
                                </View>
                                <Text style={s.timeSep}>:</Text>
                                <View style={s.timeInputWrap}>
                                    <Text style={s.timeInputLabel}>Minute (0–59)</Text>
                                    <TextInput style={[s.input, s.timeInput]} value={minute} onChangeText={setMinute}
                                        keyboardType="number-pad" maxLength={2} />
                                </View>
                                <View style={s.previewWrap}>
                                    <Text style={s.previewTime}>
                                        {timeLabel(parseInt(hour, 10) || 0, parseInt(minute, 10) || 0)}
                                    </Text>
                                </View>
                            </View>

                            {/* Quick time presets */}
                            <View style={s.presetsRow}>
                                {[
                                    { label: '7 AM', h: 7, m: 0 }, { label: '12 PM', h: 12, m: 0 },
                                    { label: '2 PM', h: 14, m: 0 }, { label: '8 PM', h: 20, m: 0 },
                                    { label: '10 PM', h: 22, m: 0 },
                                ].map(p => (
                                    <TouchableOpacity key={p.label} style={s.preset}
                                        onPress={() => { setHour(String(p.h)); setMinute(String(p.m)); }}>
                                        <Text style={s.presetText}>{p.label}</Text>
                                    </TouchableOpacity>
                                ))}
                            </View>

                            <Text style={s.label}>Notes (optional)</Text>
                            <TextInput style={[s.input, { minHeight: 60, textAlignVertical: 'top' }]}
                                value={notes} onChangeText={setNotes}
                                placeholder="e.g. Take with food, avoid alcohol"
                                placeholderTextColor={COLORS.textMuted} multiline />

                            <TouchableOpacity style={[s.saveBtn, saving && { opacity: 0.7 }]}
                                onPress={handleSave} disabled={saving}>
                                {saving
                                    ? <ActivityIndicator color="#fff" />
                                    : <>
                                        <Ionicons name="alarm" size={18} color="#fff" />
                                        <Text style={s.saveBtnText}>Set Reminder</Text>
                                    </>
                                }
                            </TouchableOpacity>
                        </ScrollView>
                    </View>
                </KeyboardAvoidingView>
            </Modal>
        </View>
    );
}

const s = StyleSheet.create({
    root: { flex: 1, backgroundColor: COLORS.bg },
    header: {
        flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
        paddingHorizontal: 20, paddingTop: 20, paddingBottom: 12,
    },
    headerTitle: { color: COLORS.textPrimary, fontSize: 20, fontWeight: '800' },
    headerSub: { color: COLORS.textMuted, fontSize: 12, marginTop: 2 },
    addBtn: {
        width: 44, height: 44, borderRadius: 22, backgroundColor: COLORS.primary,
        alignItems: 'center', justifyContent: 'center',
    },
    list: { flex: 1 },
    empty: { alignItems: 'center', paddingTop: 60, gap: 10 },
    emptyTitle: { color: COLORS.textPrimary, fontSize: 20, fontWeight: '700' },
    emptyText: { color: COLORS.textSecond, textAlign: 'center', fontSize: 14, lineHeight: 20, paddingHorizontal: 20 },
    emptyBtn: {
        backgroundColor: COLORS.primary, paddingHorizontal: 24, paddingVertical: 14,
        borderRadius: 14, marginTop: 10
    },
    emptyBtnText: { color: '#fff', fontWeight: '700', fontSize: 15 },
    card: {
        backgroundColor: COLORS.card, borderRadius: 18, padding: 16, marginBottom: 12,
        borderWidth: 1, borderColor: COLORS.border
    },
    cardInactive: { opacity: 0.6 },
    cardTop: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 10 },
    pillIcon: { width: 40, height: 40, borderRadius: 12, alignItems: 'center', justifyContent: 'center' },
    medName: { color: COLORS.textPrimary, fontWeight: '700', fontSize: 16 },
    dosage: { color: COLORS.textMuted, fontSize: 12, marginTop: 2 },
    deleteBtn: { padding: 6 },
    timesRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 8 },
    timeBadge: {
        flexDirection: 'row', alignItems: 'center', gap: 4,
        paddingHorizontal: 10, paddingVertical: 5, borderRadius: 10
    },
    timeText: { fontSize: 12, fontWeight: '600' },
    notes: { color: COLORS.textSecond, fontSize: 12, marginBottom: 8, lineHeight: 18 },
    cardFooter: { flexDirection: 'row', alignItems: 'center', gap: 6 },
    statusText: { fontSize: 11, fontWeight: '600' },

    // Modal
    modalOverlay: {
        flex: 1, backgroundColor: 'rgba(0,0,0,0.7)',
        justifyContent: 'flex-end'
    },
    modalCard: {
        backgroundColor: COLORS.card, borderTopLeftRadius: 28, borderTopRightRadius: 28,
        padding: 24, paddingBottom: 40, maxHeight: '92%',
    },
    modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
    modalTitle: { color: COLORS.textPrimary, fontSize: 20, fontWeight: '800' },
    label: { color: COLORS.textSecond, fontSize: 13, marginBottom: 6, marginTop: 14 },
    input: {
        backgroundColor: COLORS.bg, borderWidth: 1, borderColor: COLORS.border,
        borderRadius: 12, padding: 14, color: COLORS.textPrimary, fontSize: 15
    },
    timeRow: { flexDirection: 'row', alignItems: 'flex-end', gap: 10 },
    timeInputWrap: { flex: 1 },
    timeInputLabel: { color: COLORS.textMuted, fontSize: 11, marginBottom: 4 },
    timeInput: { textAlign: 'center', fontSize: 22, fontWeight: '700' },
    timeSep: { color: COLORS.textPrimary, fontSize: 28, fontWeight: '900', paddingBottom: 8 },
    previewWrap: {
        flex: 1, backgroundColor: COLORS.primaryLight, borderRadius: 12,
        alignItems: 'center', justifyContent: 'center', paddingVertical: 14
    },
    previewTime: { color: COLORS.primary, fontWeight: '800', fontSize: 18 },
    presetsRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 10 },
    preset: {
        backgroundColor: COLORS.bg, borderWidth: 1, borderColor: COLORS.border,
        paddingHorizontal: 12, paddingVertical: 8, borderRadius: 10
    },
    presetText: { color: COLORS.textSecond, fontSize: 13, fontWeight: '600' },
    saveBtn: {
        backgroundColor: COLORS.primary, borderRadius: 14, padding: 16,
        alignItems: 'center', flexDirection: 'row', justifyContent: 'center', gap: 8, marginTop: 24
    },
    saveBtnText: { color: '#fff', fontWeight: '800', fontSize: 16 },
});
