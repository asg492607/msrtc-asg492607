import React from 'react';
import { View, Text, StatusBar } from 'react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuthStore } from './src/store/useAuthStore';
import { LoginScreen } from './src/screens/auth/LoginScreen';
import { DutyScreen } from './src/screens/duty/DutyScreen';
import { ValidateScreen } from './src/screens/validate/ValidateScreen';
import { TrackingScreen } from './src/screens/tracking/TrackingScreen';
import { ManifestScreen } from './src/screens/manifest/ManifestScreen';
import { useState } from 'react';
import { TouchableOpacity, StyleSheet } from 'react-native';

const queryClient = new QueryClient();

function MainApp() {
  const [activeTab, setActiveTab] = useState<'duty' | 'validate' | 'manifest' | 'tracking'>('duty');

  const tabs = [
    { key: 'duty', label: 'Duty', icon: '📋' },
    { key: 'validate', label: 'Validate', icon: '📷' },
    { key: 'manifest', label: 'Manifest', icon: '👥' },
    { key: 'tracking', label: 'Tracking', icon: '📍' },
  ] as const;

  return (
    <View style={{ flex: 1 }}>
      <View style={{ flex: 1 }}>
        {activeTab === 'duty' && <DutyScreen />}
        {activeTab === 'validate' && <ValidateScreen />}
        {activeTab === 'manifest' && <ManifestScreen />}
        {activeTab === 'tracking' && <TrackingScreen />}
      </View>
      <View style={tabStyles.bar}>
        {tabs.map(tab => (
          <TouchableOpacity key={tab.key} style={tabStyles.tab} onPress={() => setActiveTab(tab.key)}>
            <Text style={tabStyles.icon}>{tab.icon}</Text>
            <Text style={[tabStyles.label, activeTab === tab.key && tabStyles.activeLabel]}>{tab.label}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}

const tabStyles = StyleSheet.create({
  bar: { flexDirection: 'row', backgroundColor: '#fff', borderTopWidth: 1, borderTopColor: '#eee', paddingBottom: 20, paddingTop: 8 },
  tab: { flex: 1, alignItems: 'center' },
  icon: { fontSize: 22 },
  label: { fontSize: 11, color: '#999', marginTop: 2 },
  activeLabel: { color: '#0053A0', fontWeight: '700' },
});

export default function App() {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated);
  return (
    <QueryClientProvider client={queryClient}>
      <StatusBar barStyle="light-content" />
      {isAuthenticated ? <MainApp /> : <LoginScreen />}
    </QueryClientProvider>
  );
}
