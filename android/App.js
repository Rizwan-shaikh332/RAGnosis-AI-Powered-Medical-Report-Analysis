import React, { useState, useEffect, createContext } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import * as SecureStore from 'expo-secure-store';
import * as Notifications from 'expo-notifications';
import { StatusBar } from 'expo-status-bar';
import { View, ActivityIndicator } from 'react-native';

import { COLORS } from './src/constants/theme';
import LoginScreen from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import DashboardScreen from './src/screens/DashboardScreen';
import UploadScreen from './src/screens/UploadScreen';
import ReportsScreen from './src/screens/ReportsScreen';
import ReportDetailScreen from './src/screens/ReportDetailScreen';
import ChatScreen from './src/screens/ChatScreen';
import ProfileScreen from './src/screens/ProfileScreen';
import MedicineReminderScreen from './src/screens/MedicineReminderScreen';

// ── Auth context — lets Login/Register call setLoggedIn without route params ──
export const AuthContext = createContext(null);

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

// Configure how notifications appear when app is in foreground
Notifications.setNotificationHandler({
    handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: false,
    }),
});

function MainTabs() {
    return (
        <Tab.Navigator
            screenOptions={({ route }) => ({
                headerShown: false,
                tabBarStyle: {
                    backgroundColor: COLORS.card,
                    borderTopColor: COLORS.border,
                    paddingBottom: 4,
                },
                tabBarActiveTintColor: COLORS.primary,
                tabBarInactiveTintColor: COLORS.textMuted,
                tabBarIcon: ({ focused, color, size }) => {
                    const icons = {
                        Overview: focused ? 'home' : 'home-outline',
                        Upload: focused ? 'cloud-upload' : 'cloud-upload-outline',
                        Reports: focused ? 'document-text' : 'document-text-outline',
                        Chat: focused ? 'chatbubble' : 'chatbubble-outline',
                        Reminders: focused ? 'alarm' : 'alarm-outline',
                        Profile: focused ? 'person' : 'person-outline',
                    };
                    return <Ionicons name={icons[route.name]} size={size} color={color} />;
                },
            })}
        >
            <Tab.Screen name="Overview" component={DashboardScreen} />
            <Tab.Screen name="Upload" component={UploadScreen} />
            <Tab.Screen name="Reports" component={ReportsScreen} />
            <Tab.Screen name="Chat" component={ChatScreen} />
            <Tab.Screen name="Reminders" component={MedicineReminderScreen} />
            <Tab.Screen name="Profile" component={ProfileScreen} />
        </Tab.Navigator>
    );
}

export default function App() {
    const [loggedIn, setLoggedIn] = useState(null); // null = checking

    useEffect(() => {
        // Check auth token
        SecureStore.getItemAsync('auth_token').then(t => setLoggedIn(!!t));

        // Request notification permissions on startup
        Notifications.requestPermissionsAsync().catch(() => { });
    }, []);

    if (loggedIn === null) {
        return (
            <View style={{ flex: 1, backgroundColor: COLORS.bg, justifyContent: 'center', alignItems: 'center' }}>
                <ActivityIndicator color={COLORS.primary} size="large" />
            </View>
        );
    }

    return (
        <AuthContext.Provider value={{ setLoggedIn }}>
            <NavigationContainer>
                <StatusBar style="light" />
                <Stack.Navigator screenOptions={{ headerShown: false }}>
                    {!loggedIn ? (
                        <>
                            <Stack.Screen name="Login" component={LoginScreen} />
                            <Stack.Screen name="Register" component={RegisterScreen} />
                        </>
                    ) : (
                        <>
                            <Stack.Screen name="Main" component={MainTabs} />
                            <Stack.Screen name="ReportDetail" component={ReportDetailScreen}
                                options={{
                                    headerShown: true, title: 'Report Details',
                                    headerStyle: { backgroundColor: COLORS.card },
                                    headerTintColor: COLORS.textPrimary
                                }} />
                        </>
                    )}
                </Stack.Navigator>
            </NavigationContainer>
        </AuthContext.Provider>
    );
}
