import React, { useState, useRef } from 'react';
import {
    View, Text, FlatList, TextInput, TouchableOpacity,
    StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import api from '../api/client';
import { COLORS } from '../constants/theme';

export default function ChatScreen() {
    const [messages, setMessages] = useState([
        { id: '0', role: 'assistant', text: '👋 Hi! I\'m RAGnosis AI. Ask me anything about your medical reports, lab values, or health.' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const listRef = useRef(null);

    const send = async () => {
        const q = input.trim();
        if (!q || loading) return;
        const userMsg = { id: Date.now().toString(), role: 'user', text: q };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);
        try {
            const res = await api.post('/chat/', { message: q });
            const reply = res.data.response || 'Sorry, I could not process that.';
            setMessages(prev => [...prev, { id: Date.now().toString() + '_r', role: 'assistant', text: reply }]);
        } catch (_) {
            setMessages(prev => [...prev, {
                id: Date.now().toString() + '_e', role: 'assistant',
                text: '⚠️ Could not reach the AI. Check your network connection.'
            }]);
        } finally {
            setLoading(false);
            setTimeout(() => listRef.current?.scrollToEnd({ animated: true }), 100);
        }
    };

    const renderMessage = ({ item: m }) => {
        const isUser = m.role === 'user';
        return (
            <View style={[s.bubble, isUser ? s.userBubble : s.aiBubble]}>
                {!isUser && <Text style={s.aiIcon}>🤖</Text>}
                <Text style={[s.bubbleText, isUser ? s.userText : s.aiText]}>{m.text}</Text>
            </View>
        );
    };

    return (
        <KeyboardAvoidingView style={s.root} behavior={Platform.OS === 'ios' ? 'padding' : 'height'} keyboardVerticalOffset={80}>
            <View style={s.header}>
                <View style={s.headerDot}><Text style={{ fontSize: 18 }}>🤖</Text></View>
                <View>
                    <Text style={s.headerTitle}>AI Chatbot</Text>
                    <Text style={s.headerSub}>Powered by Groq Llama 3</Text>
                </View>
            </View>
            <FlatList
                ref={listRef}
                data={messages}
                keyExtractor={m => m.id}
                renderItem={renderMessage}
                contentContainerStyle={{ padding: 16, paddingBottom: 8 }}
                onContentSizeChange={() => listRef.current?.scrollToEnd({ animated: false })}
            />
            {loading && (
                <View style={s.typingRow}>
                    <ActivityIndicator color={COLORS.primary} size="small" />
                    <Text style={s.typingText}>AI is typing…</Text>
                </View>
            )}
            <View style={s.inputRow}>
                <TextInput
                    style={s.input}
                    value={input}
                    onChangeText={setInput}
                    placeholder="Ask about your reports…"
                    placeholderTextColor={COLORS.textMuted}
                    multiline
                    onSubmitEditing={send}
                    returnKeyType="send"
                />
                <TouchableOpacity style={s.sendBtn} onPress={send} disabled={loading || !input.trim()}>
                    <Ionicons name="send" size={20} color="#fff" />
                </TouchableOpacity>
            </View>
        </KeyboardAvoidingView>
    );
}

const s = StyleSheet.create({
    root: { flex: 1, backgroundColor: COLORS.bg },
    header: {
        flexDirection: 'row', alignItems: 'center', gap: 12, padding: 16,
        borderBottomWidth: 1, borderBottomColor: COLORS.border, backgroundColor: COLORS.card
    },
    headerDot: {
        width: 44, height: 44, backgroundColor: COLORS.primaryLight, borderRadius: 12,
        alignItems: 'center', justifyContent: 'center'
    },
    headerTitle: { color: COLORS.textPrimary, fontWeight: '800', fontSize: 16 },
    headerSub: { color: COLORS.textMuted, fontSize: 11 },
    bubble: { marginBottom: 10, maxWidth: '85%', borderRadius: 16, padding: 12 },
    userBubble: { backgroundColor: COLORS.primary, alignSelf: 'flex-end', borderBottomRightRadius: 4 },
    aiBubble: {
        backgroundColor: COLORS.card, borderWidth: 1, borderColor: COLORS.border,
        alignSelf: 'flex-start', borderBottomLeftRadius: 4, flexDirection: 'row', gap: 8
    },
    aiIcon: { fontSize: 14, marginTop: 2 },
    bubbleText: { fontSize: 14, lineHeight: 20 },
    userText: { color: '#fff' },
    aiText: { color: COLORS.textPrimary, flex: 1 },
    typingRow: { flexDirection: 'row', alignItems: 'center', gap: 8, paddingHorizontal: 16, paddingVertical: 6 },
    typingText: { color: COLORS.textMuted, fontSize: 12 },
    inputRow: {
        flexDirection: 'row', padding: 12, gap: 10, borderTopWidth: 1, borderTopColor: COLORS.border,
        backgroundColor: COLORS.card
    },
    input: {
        flex: 1, backgroundColor: COLORS.bg, borderWidth: 1, borderColor: COLORS.border,
        borderRadius: 12, paddingHorizontal: 14, paddingVertical: 10, color: COLORS.textPrimary,
        fontSize: 14, maxHeight: 100
    },
    sendBtn: {
        width: 44, height: 44, backgroundColor: COLORS.primary, borderRadius: 12,
        alignItems: 'center', justifyContent: 'center', alignSelf: 'flex-end'
    },
});
