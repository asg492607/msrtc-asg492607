import React, { useState } from 'react';
import { View, Text, StatusBar, StyleSheet, TouchableOpacity } from 'react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuthStore } from './src/store/useAuthStore';
import { LoginScreen } from './src/screens/auth/LoginScreen';
import { DutyScreen } from './src/screens/duty/DutyScreen';
import { ValidateScreen } from './src/screens/validate/ValidateScreen';
import { TrackingScreen } from './src/screens/tracking/TrackingScreen';
import { ManifestScreen } from './src/screens/manifest/ManifestScreen';
import { NotificationsScreen } from './src/screens/notifications/NotificationsScreen';

const queryClient = new QueryClient();

const TABS = [
  { key: 'duty', label: 'Duty', icon: '📋' },
  { key: 'validate', label: 'Validate', icon: '📷' },
  { key: 'manifest', label: 'Manifest', icon: '👥' },
  { key: 'tracking', label: 'Tracking', icon: '📍' },
  { key: 'alerts', label: 'Alerts', icon: '🔔' },
] as const;

type TabKey = typeof TABS[number]['key'];

function MainApp() {
  const [activeTab, setActiveTab] = useState<TabKey>('duty');
  const logout = useAuthStore(s => s.logout);

  return (
    <View style={{ flex: 1 }}>
      <View style={{ flex: 1 }}>
        {activeTab === 'duty' && <DutyScreen />}
        {activeTab === 'validate' && <ValidateScreen />}
        {activeTab === 'manifest' && <ManifestScreen />}
        {activeTab === 'tracking' && <TrackingScreen />}
        {activeTab === 'alerts' && <NotificationsScreen />}
      </View>
      <View style={styles.bar}>
        {TABS.map(tab => (
          <TouchableOpacity key={tab.key} style={styles.tab} onPress={() => setActiveTab(tab.key)}>
            <Text style={styles.icon}>{tab.icon}</Text>
            <Text style={[styles.label, activeTab === tab.key && styles.active]}>{tab.label}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  bar: { flexDirection: 'row', backgroundColor: '#fff', borderTopWidth: 1, borderTopColor: '#eee', paddingBottom: 20, paddingTop: 8 },
  tab: { flex: 1, alignItems: 'center' },
  icon: { fontSize: 20 },
  label: { fontSize: 10, color: '#999', marginTop: 2 },
  active: { color: '#0053A0', fontWeight: '700' },
});

export default function App() {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated);
  return (
    <QueryClientProvider client={queryClient}>
      <StatusBar barStyle="light-content" backgroundColor="#0053A0" />
      {isAuthenticated ? <MainApp /> : <LoginScreen />}
    </QueryClientProvider>
  );
}
