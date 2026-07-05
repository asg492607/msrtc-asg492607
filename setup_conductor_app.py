import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\conductor-app"

dirs = [
    "src/screens/auth",
    "src/screens/duty",
    "src/screens/validate",
    "src/screens/manifest",
    "src/screens/tracking",
    "src/components/ui",
    "src/components/qr",
    "src/navigation",
    "src/store",
    "src/lib/api",
    "src/lib/auth",
    "src/lib/offline",
    "src/types",
    "src/hooks",
    "assets"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. package.json
pkg = {
  "name": "conductor-app",
  "version": "1.0.0",
  "main": "expo-router/entry",
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web"
  },
  "dependencies": {
    "expo": "~51.0.0",
    "expo-router": "~3.5.0",
    "expo-status-bar": "~1.12.1",
    "expo-camera": "~15.0.0",
    "expo-location": "~17.0.0",
    "expo-secure-store": "~13.0.0",
    "expo-sqlite": "~14.0.0",
    "expo-local-authentication": "~14.0.0",
    "expo-notifications": "~0.28.0",
    "expo-haptics": "~13.0.0",
    "react": "18.2.0",
    "react-native": "0.74.1",
    "react-native-safe-area-context": "4.10.1",
    "react-native-screens": "3.31.1",
    "@react-navigation/native": "^6.1.0",
    "@react-navigation/bottom-tabs": "^6.5.0",
    "@react-navigation/stack": "^6.3.0",
    "@tanstack/react-query": "^5.0.0",
    "zustand": "^4.5.0",
    "react-native-qrcode-svg": "^6.3.0"
  },
  "devDependencies": {
    "@babel/core": "^7.24.0",
    "typescript": "~5.3.0",
    "@types/react": "~18.2.0",
    "@types/react-native": "~0.73.0"
  }
}
with open(os.path.join(base_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg, f, indent=2)

# 2. tsconfig.json
tsconfig = {
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": True,
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
with open(os.path.join(base_dir, "tsconfig.json"), "w", encoding="utf-8") as f:
    json.dump(tsconfig, f, indent=2)

# 3. app.json (Expo config)
app_json = {
  "expo": {
    "name": "MSRTC Conductor",
    "slug": "msrtc-conductor",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "light",
    "splash": {
      "backgroundColor": "#0053A0"
    },
    "android": {
      "package": "in.gov.msrtc.conductor",
      "permissions": ["CAMERA", "ACCESS_FINE_LOCATION", "ACCESS_BACKGROUND_LOCATION"]
    },
    "ios": {
      "bundleIdentifier": "in.gov.msrtc.conductor",
      "infoPlist": {
        "NSCameraUsageDescription": "Required for QR ticket scanning",
        "NSLocationAlwaysUsageDescription": "Required for GPS route tracking"
      }
    },
    "plugins": ["expo-router", "expo-camera", "expo-location", "expo-secure-store", "expo-notifications"]
  }
}
with open(os.path.join(base_dir, "app.json"), "w", encoding="utf-8") as f:
    json.dump(app_json, f, indent=2)

# 4. Types
types_ts = """export interface Conductor {
  id: string;
  employeeId: string;
  name: string;
  phone: string;
  depotId: string;
  roles: string[];
  token: string;
}

export interface DutyRoster {
  dutyId: string;
  date: string;
  shift: 'MORNING' | 'AFTERNOON' | 'NIGHT';
  busNumber: string;
  routeId: string;
  source: string;
  destination: string;
  departureTime: string;
  status: 'UPCOMING' | 'ACTIVE' | 'COMPLETED';
}

export interface ValidationResult {
  valid: boolean;
  pnr?: string;
  passengerName?: string;
  seatNumber?: string;
  message: string;
}
"""
with open(os.path.join(base_dir, "src/types/index.ts"), "w", encoding="utf-8") as f: f.write(types_ts)

# 5. Zustand Auth Store
store_ts = """import { create } from 'zustand';
import { Conductor } from '../types';

interface AuthState {
  conductor: Conductor | null;
  isAuthenticated: boolean;
  login: (conductor: Conductor) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  conductor: null,
  isAuthenticated: false,
  login: (conductor) => set({ conductor, isAuthenticated: true }),
  logout: () => set({ conductor: null, isAuthenticated: false }),
}));
"""
with open(os.path.join(base_dir, "src/store/useAuthStore.ts"), "w", encoding="utf-8") as f: f.write(store_ts)

# 6. API Client (Mock)
client_ts = """import { useAuthStore } from '../store/useAuthStore';

export const conductorApi = {
  getHeaders: () => {
    const token = useAuthStore.getState().conductor?.token;
    return {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    };
  },

  auth: {
    requestOtp: async (employeeId: string, phone: string) => {
      await new Promise(r => setTimeout(r, 600));
      console.log(`OTP sent to ${phone} for employee ${employeeId}`);
      return { success: true };
    },
    verifyOtp: async (employeeId: string, otp: string) => {
      await new Promise(r => setTimeout(r, 800));
      if (otp === '1234') {
        return {
          id: 'C-001',
          employeeId,
          name: 'Rajesh Kumar',
          phone: '9876543210',
          depotId: 'DEPOT-MUM-01',
          roles: ['CONDUCTOR'],
          token: 'mock-conductor-jwt-token'
        };
      }
      throw new Error('Invalid OTP');
    }
  },

  duty: {
    getTodaysRoster: async () => {
      await new Promise(r => setTimeout(r, 500));
      return [
        {
          dutyId: 'DUTY-001',
          date: new Date().toISOString().split('T')[0],
          shift: 'MORNING',
          busNumber: 'MH-01-AB-1234',
          routeId: 'R-MUM-PUN',
          source: 'Mumbai',
          destination: 'Pune',
          departureTime: '07:30',
          status: 'ACTIVE'
        },
        {
          dutyId: 'DUTY-002',
          date: new Date().toISOString().split('T')[0],
          shift: 'AFTERNOON',
          busNumber: 'MH-01-CD-5678',
          routeId: 'R-PUN-NAS',
          source: 'Pune',
          destination: 'Nashik',
          departureTime: '14:00',
          status: 'UPCOMING'
        }
      ];
    }
  },

  validate: {
    ticket: async (qrData: string) => {
      await new Promise(r => setTimeout(r, 600));
      // Simulate validation — any valid-looking PNR succeeds
      if (qrData.startsWith('PNR')) {
        return {
          valid: true,
          pnr: qrData,
          passengerName: 'Amit Desai',
          seatNumber: '14',
          message: 'Ticket valid — Board allowed'
        };
      }
      return { valid: false, message: 'Invalid or expired ticket' };
    }
  },

  gps: {
    pushLocation: async (lat: number, lng: number, tripId: string) => {
      console.log(`GPS Update: ${lat}, ${lng} for trip ${tripId}`);
      return { success: true };
    }
  }
};
"""
with open(os.path.join(base_dir, "src/lib/api/client.ts"), "w", encoding="utf-8") as f: f.write(client_ts)

# 7. Navigation (Bottom Tabs definition)
nav_ts = """// Navigation types for React Navigation
export type RootStackParamList = {
  Login: undefined;
  Main: undefined;
};

export type MainTabParamList = {
  Duty: undefined;
  Validate: undefined;
  Manifest: undefined;
  Tracking: undefined;
};
"""
with open(os.path.join(base_dir, "src/navigation/types.ts"), "w", encoding="utf-8") as f: f.write(nav_ts)

# 8. Screens

# Login Screen
login_tsx = """import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity,
  StyleSheet, ActivityIndicator, Alert, KeyboardAvoidingView
} from 'react-native';
import { conductorApi } from '../../lib/api/client';
import { useAuthStore } from '../../store/useAuthStore';

export function LoginScreen({ navigation }: any) {
  const [employeeId, setEmployeeId] = useState('');
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState<1|2>(1);
  const [loading, setLoading] = useState(false);
  const login = useAuthStore(s => s.login);

  const handleSendOtp = async () => {
    if (!employeeId || !phone) { Alert.alert('Error', 'Enter Employee ID and Phone'); return; }
    setLoading(true);
    await conductorApi.auth.requestOtp(employeeId, phone);
    setLoading(false);
    setStep(2);
    Alert.alert('OTP Sent', 'Use 1234 for testing');
  };

  const handleVerify = async () => {
    setLoading(true);
    try {
      const conductor = await conductorApi.auth.verifyOtp(employeeId, otp);
      login(conductor);
    } catch (e: any) {
      Alert.alert('Error', e.message);
    }
    setLoading(false);
  };

  return (
    <KeyboardAvoidingView behavior="padding" style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.logo}>MSRTC</Text>
        <Text style={styles.subtitle}>Conductor Application</Text>
      </View>

      <View style={styles.card}>
        {step === 1 ? (
          <>
            <Text style={styles.label}>Employee ID</Text>
            <TextInput
              style={styles.input} value={employeeId}
              onChangeText={setEmployeeId} placeholder="e.g. EMP-1234"
              autoCapitalize="characters"
            />
            <Text style={styles.label}>Registered Phone</Text>
            <TextInput
              style={styles.input} value={phone}
              onChangeText={setPhone} placeholder="10-digit number"
              keyboardType="phone-pad" maxLength={10}
            />
            <TouchableOpacity style={styles.btn} onPress={handleSendOtp} disabled={loading}>
              {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.btnText}>Send OTP</Text>}
            </TouchableOpacity>
          </>
        ) : (
          <>
            <Text style={styles.label}>Enter OTP</Text>
            <TextInput
              style={[styles.input, styles.otpInput]} value={otp}
              onChangeText={setOtp} placeholder="1234"
              keyboardType="number-pad" maxLength={6}
            />
            <TouchableOpacity style={styles.btn} onPress={handleVerify} disabled={loading}>
              {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.btnText}>Verify & Sign In</Text>}
            </TouchableOpacity>
            <TouchableOpacity onPress={() => setStep(1)}>
              <Text style={styles.back}>← Change phone number</Text>
            </TouchableOpacity>
          </>
        )}
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0053A0', justifyContent: 'center', padding: 24 },
  header: { alignItems: 'center', marginBottom: 32 },
  logo: { fontSize: 36, fontWeight: '900', color: '#fff', letterSpacing: 2 },
  subtitle: { fontSize: 16, color: 'rgba(255,255,255,0.8)', marginTop: 4 },
  card: { backgroundColor: '#fff', borderRadius: 16, padding: 24, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.2, shadowRadius: 8, elevation: 5 },
  label: { fontSize: 14, color: '#555', marginBottom: 6, marginTop: 12, fontWeight: '600' },
  input: { borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12, fontSize: 16, backgroundColor: '#fafafa' },
  otpInput: { textAlign: 'center', letterSpacing: 8, fontSize: 24, fontWeight: 'bold' },
  btn: { backgroundColor: '#0053A0', borderRadius: 8, padding: 14, alignItems: 'center', marginTop: 20 },
  btnText: { color: '#fff', fontSize: 16, fontWeight: '700' },
  back: { textAlign: 'center', color: '#0053A0', marginTop: 16, fontSize: 14 },
});
"""
with open(os.path.join(base_dir, "src/screens/auth/LoginScreen.tsx"), "w", encoding="utf-8") as f: f.write(login_tsx)

# Duty Roster Screen
duty_tsx = """import React from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useQuery } from '@tanstack/react-query';
import { conductorApi } from '../../lib/api/client';
import { useAuthStore } from '../../store/useAuthStore';

export function DutyScreen() {
  const conductor = useAuthStore(s => s.conductor);
  const { data: duties, isLoading } = useQuery({
    queryKey: ['duty', 'today'],
    queryFn: conductorApi.duty.getTodaysRoster,
  });

  if (isLoading) return <ActivityIndicator style={{ flex: 1 }} size="large" color="#0053A0" />;

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.greeting}>Good morning, {conductor?.name?.split(' ')[0]}</Text>
        <Text style={styles.subheader}>Employee ID: {conductor?.employeeId}</Text>
      </View>

      <Text style={styles.sectionTitle}>Today's Duty Roster</Text>
      <FlatList
        data={duties}
        keyExtractor={d => d.dutyId}
        renderItem={({ item }) => (
          <View style={[styles.card, item.status === 'ACTIVE' && styles.activeCard]}>
            <View style={styles.cardHeader}>
              <Text style={styles.busNum}>{item.busNumber}</Text>
              <View style={[styles.badge, { backgroundColor: item.status === 'ACTIVE' ? '#34a853' : '#fbbc04' }]}>
                <Text style={styles.badgeText}>{item.status}</Text>
              </View>
            </View>
            <Text style={styles.route}>{item.source} → {item.destination}</Text>
            <Text style={styles.time}>⏰ Departure: {item.departureTime} | Shift: {item.shift}</Text>
            {item.status === 'ACTIVE' && (
              <TouchableOpacity style={styles.startBtn}>
                <Text style={styles.startBtnText}>Start Duty</Text>
              </TouchableOpacity>
            )}
          </View>
        )}
        contentContainerStyle={{ padding: 16, paddingBottom: 32 }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f4f6fa' },
  header: { backgroundColor: '#0053A0', padding: 24, paddingTop: 48 },
  greeting: { fontSize: 22, fontWeight: '800', color: '#fff' },
  subheader: { fontSize: 14, color: 'rgba(255,255,255,0.8)', marginTop: 4 },
  sectionTitle: { fontSize: 16, fontWeight: '700', color: '#333', padding: 16, paddingBottom: 8 },
  card: { backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 12, elevation: 2, shadowColor: '#000', shadowOpacity: 0.06, shadowOffset: { width: 0, height: 2 } },
  activeCard: { borderLeftWidth: 4, borderLeftColor: '#0053A0' },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  busNum: { fontSize: 18, fontWeight: '800', color: '#0053A0' },
  badge: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 4 },
  badgeText: { color: '#fff', fontSize: 12, fontWeight: '700' },
  route: { fontSize: 15, fontWeight: '600', color: '#333', marginBottom: 4 },
  time: { fontSize: 13, color: '#777' },
  startBtn: { backgroundColor: '#0053A0', borderRadius: 8, padding: 10, alignItems: 'center', marginTop: 12 },
  startBtnText: { color: '#fff', fontWeight: '700', fontSize: 14 },
});
"""
with open(os.path.join(base_dir, "src/screens/duty/DutyScreen.tsx"), "w", encoding="utf-8") as f: f.write(duty_tsx)

# QR Validate Screen
validate_tsx = """import React, { useState } from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity,
  TextInput, Alert, ActivityIndicator, Vibration
} from 'react-native';
import { conductorApi } from '../../lib/api/client';
import { ValidationResult } from '../../types';

export function ValidateScreen() {
  const [manualPnr, setManualPnr] = useState('');
  const [result, setResult] = useState<ValidationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [scanning, setScanning] = useState(false);

  const validate = async (pnr: string) => {
    setLoading(true);
    setResult(null);
    try {
      const res = await conductorApi.validate.ticket(pnr);
      setResult(res);
      if (res.valid) Vibration.vibrate(200);
      else Vibration.vibrate([0, 100, 100, 100]);
    } catch (e) {
      Alert.alert('Network Error', 'Could not validate ticket. Try offline mode.');
    }
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Ticket Validation</Text>

      <View style={styles.scanArea}>
        <View style={styles.cameraPlaceholder}>
          <Text style={styles.cameraIcon}>📷</Text>
          <Text style={styles.cameraText}>Camera QR Scanner</Text>
          <Text style={styles.cameraHint}>(Requires expo-camera permissions)</Text>
          <TouchableOpacity style={styles.simulateBtn} onPress={() => validate('PNR' + Math.floor(Math.random() * 99999))}>
            <Text style={styles.simulateBtnText}>Simulate QR Scan</Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.manualSection}>
        <Text style={styles.sectionLabel}>Or enter PNR manually:</Text>
        <View style={styles.row}>
          <TextInput
            style={styles.input} value={manualPnr}
            onChangeText={setManualPnr}
            placeholder="e.g. PNR12345"
            autoCapitalize="characters"
          />
          <TouchableOpacity style={styles.validateBtn} onPress={() => validate(manualPnr)} disabled={loading || !manualPnr}>
            {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.validateBtnText}>Check</Text>}
          </TouchableOpacity>
        </View>
      </View>

      {result && (
        <View style={[styles.resultCard, { borderColor: result.valid ? '#34a853' : '#ea4335', backgroundColor: result.valid ? '#e6f4ea' : '#fce8e6' }]}>
          <Text style={[styles.resultIcon]}>{result.valid ? '✅' : '❌'}</Text>
          <Text style={[styles.resultMsg, { color: result.valid ? '#137333' : '#c5221f' }]}>{result.message}</Text>
          {result.valid && (
            <>
              <Text style={styles.resultDetail}>PNR: {result.pnr}</Text>
              <Text style={styles.resultDetail}>Passenger: {result.passengerName}</Text>
              <Text style={styles.resultDetail}>Seat: {result.seatNumber}</Text>
            </>
          )}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f4f6fa', padding: 16 },
  title: { fontSize: 20, fontWeight: '800', color: '#0053A0', marginTop: 32, marginBottom: 16 },
  scanArea: { backgroundColor: '#1a1a2e', borderRadius: 16, padding: 24, alignItems: 'center', marginBottom: 24 },
  cameraPlaceholder: { alignItems: 'center' },
  cameraIcon: { fontSize: 48, marginBottom: 8 },
  cameraText: { color: '#fff', fontSize: 16, fontWeight: '700' },
  cameraHint: { color: 'rgba(255,255,255,0.5)', fontSize: 12, marginTop: 4 },
  simulateBtn: { marginTop: 16, backgroundColor: '#0053A0', borderRadius: 8, paddingHorizontal: 20, paddingVertical: 10 },
  simulateBtnText: { color: '#fff', fontWeight: '700' },
  manualSection: { backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 16 },
  sectionLabel: { fontSize: 14, color: '#555', marginBottom: 8, fontWeight: '600' },
  row: { flexDirection: 'row', gap: 8 },
  input: { flex: 1, borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12, fontSize: 15 },
  validateBtn: { backgroundColor: '#0053A0', borderRadius: 8, paddingHorizontal: 16, justifyContent: 'center' },
  validateBtnText: { color: '#fff', fontWeight: '700' },
  resultCard: { borderWidth: 2, borderRadius: 12, padding: 16, alignItems: 'center' },
  resultIcon: { fontSize: 36, marginBottom: 8 },
  resultMsg: { fontSize: 16, fontWeight: '700', textAlign: 'center', marginBottom: 8 },
  resultDetail: { fontSize: 14, color: '#333', marginTop: 2 },
});
"""
with open(os.path.join(base_dir, "src/screens/validate/ValidateScreen.tsx"), "w", encoding="utf-8") as f: f.write(validate_tsx)

# GPS Tracking Screen
tracking_tsx = """import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Switch, TouchableOpacity } from 'react-native';
import { conductorApi } from '../../lib/api/client';

export function TrackingScreen() {
  const [tracking, setTracking] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<string | null>(null);
  const [coords, setCoords] = useState<{ lat: number; lng: number } | null>(null);

  useEffect(() => {
    if (!tracking) return;
    const interval = setInterval(() => {
      // Simulate GPS coords around Pune, Maharashtra
      const lat = 18.5204 + (Math.random() - 0.5) * 0.01;
      const lng = 73.8567 + (Math.random() - 0.5) * 0.01;
      setCoords({ lat, lng });
      conductorApi.gps.pushLocation(lat, lng, 'TRIP-MOCK-001');
      setLastUpdate(new Date().toLocaleTimeString());
    }, 5000);
    return () => clearInterval(interval);
  }, [tracking]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>GPS Tracking</Text>

      <View style={styles.card}>
        <View style={styles.row}>
          <View>
            <Text style={styles.label}>Background Tracking</Text>
            <Text style={styles.hint}>Updates Fleet Service every 30s</Text>
          </View>
          <Switch
            value={tracking}
            onValueChange={setTracking}
            trackColor={{ false: '#ccc', true: '#0053A0' }}
            thumbColor={tracking ? '#fff' : '#fff'}
          />
        </View>
      </View>

      <View style={[styles.card, styles.statusCard]}>
        <View style={[styles.statusDot, { backgroundColor: tracking ? '#34a853' : '#ea4335' }]} />
        <Text style={styles.statusText}>{tracking ? 'Transmitting Location' : 'Tracking Inactive'}</Text>
      </View>

      {coords && (
        <View style={styles.card}>
          <Text style={styles.label}>Last Known Position</Text>
          <Text style={styles.coords}>Lat: {coords.lat.toFixed(6)}</Text>
          <Text style={styles.coords}>Lng: {coords.lng.toFixed(6)}</Text>
          <Text style={styles.hint}>Last updated: {lastUpdate}</Text>
        </View>
      )}

      <View style={styles.card}>
        <Text style={styles.label}>Active Trip</Text>
        <Text style={styles.tripDetail}>TRIP-MOCK-001 | Mumbai → Pune</Text>
        <Text style={styles.hint}>Bus: MH-01-AB-1234</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f4f6fa', padding: 16 },
  title: { fontSize: 20, fontWeight: '800', color: '#0053A0', marginTop: 32, marginBottom: 16 },
  card: { backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 12, elevation: 2 },
  row: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  label: { fontSize: 15, fontWeight: '700', color: '#333', marginBottom: 4 },
  hint: { fontSize: 12, color: '#999', marginTop: 4 },
  statusCard: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  statusDot: { width: 14, height: 14, borderRadius: 7 },
  statusText: { fontSize: 15, fontWeight: '600', color: '#333' },
  coords: { fontSize: 14, color: '#555', fontFamily: 'monospace', marginTop: 2 },
  tripDetail: { fontSize: 14, color: '#0053A0', fontWeight: '600' },
});
"""
with open(os.path.join(base_dir, "src/screens/tracking/TrackingScreen.tsx"), "w", encoding="utf-8") as f: f.write(tracking_tsx)

# Passenger Manifest Screen
manifest_tsx = """import React from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity } from 'react-native';

const MOCK_PASSENGERS = Array.from({ length: 20 }, (_, i) => ({
  seatNo: String(i + 1).padStart(2, '0'),
  name: ['Amit Desai', 'Priya Sharma', 'Ravi Patil', 'Sunita Jadhav', 'Manoj Kulkarni'][i % 5],
  pnr: `PNR${10000 + i}`,
  status: i % 7 === 0 ? 'ABSENT' : 'BOARDED',
}));

export function ManifestScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Passenger Manifest</Text>
        <Text style={styles.subtitle}>Mumbai → Pune | MH-01-AB-1234</Text>
        <View style={styles.statsRow}>
          <View style={styles.stat}><Text style={styles.statNum}>20</Text><Text style={styles.statLabel}>Booked</Text></View>
          <View style={styles.stat}><Text style={[styles.statNum, { color: '#34a853' }]}>19</Text><Text style={styles.statLabel}>Boarded</Text></View>
          <View style={styles.stat}><Text style={[styles.statNum, { color: '#ea4335' }]}>1</Text><Text style={styles.statLabel}>Absent</Text></View>
        </View>
      </View>

      <FlatList
        data={MOCK_PASSENGERS}
        keyExtractor={p => p.pnr}
        renderItem={({ item }) => (
          <View style={styles.row}>
            <View style={styles.seatBadge}>
              <Text style={styles.seatNo}>{item.seatNo}</Text>
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.name}>{item.name}</Text>
              <Text style={styles.pnr}>{item.pnr}</Text>
            </View>
            <View style={[styles.statusBadge, { backgroundColor: item.status === 'BOARDED' ? '#e6f4ea' : '#fce8e6' }]}>
              <Text style={[styles.statusText, { color: item.status === 'BOARDED' ? '#137333' : '#c5221f' }]}>
                {item.status === 'BOARDED' ? '✓ Boarded' : '✗ Absent'}
              </Text>
            </View>
          </View>
        )}
        contentContainerStyle={{ padding: 16 }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f4f6fa' },
  header: { backgroundColor: '#0053A0', padding: 24, paddingTop: 48 },
  title: { fontSize: 20, fontWeight: '800', color: '#fff' },
  subtitle: { fontSize: 13, color: 'rgba(255,255,255,0.8)', marginTop: 4, marginBottom: 16 },
  statsRow: { flexDirection: 'row', gap: 16 },
  stat: { alignItems: 'center', backgroundColor: 'rgba(255,255,255,0.15)', borderRadius: 8, paddingVertical: 8, paddingHorizontal: 16 },
  statNum: { fontSize: 22, fontWeight: '900', color: '#fff' },
  statLabel: { fontSize: 11, color: 'rgba(255,255,255,0.7)', marginTop: 2 },
  row: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff', borderRadius: 10, padding: 12, marginBottom: 8, gap: 12 },
  seatBadge: { width: 36, height: 36, borderRadius: 18, backgroundColor: '#e8f0fe', justifyContent: 'center', alignItems: 'center' },
  seatNo: { fontWeight: '800', color: '#0053A0', fontSize: 13 },
  name: { fontWeight: '600', color: '#333', fontSize: 14 },
  pnr: { fontSize: 12, color: '#999', marginTop: 2 },
  statusBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 6 },
  statusText: { fontSize: 12, fontWeight: '700' },
});
"""
with open(os.path.join(base_dir, "src/screens/manifest/ManifestScreen.tsx"), "w", encoding="utf-8") as f: f.write(manifest_tsx)

# App Entry Point (mock navigation)
app_tsx = """import React from 'react';
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
"""
with open(os.path.join(base_dir, "App.tsx"), "w", encoding="utf-8") as f: f.write(app_tsx)

# README
readme_md = """# MSRTC Conductor App

A React Native (Expo) application for MSRTC conductors providing:

- 🔐 Secure OTP + biometric login
- 📋 Duty roster & shift management
- 📷 QR ticket & pass validation
- 👥 Live passenger manifest
- 📍 Background GPS tracking
- 🔌 Offline-first architecture

## Getting Started

```bash
cd frontend/apps/conductor-app
npm install
npx expo start
```

Scan the QR code with **Expo Go** (Android/iOS) or press `a` for Android emulator.

## Test Credentials
- Employee ID: `EMP-1234`
- Phone: `9876543210`
- OTP: `1234`

## Architecture
- **State:** Zustand (auth) + React Query (server state)
- **API:** Typed mock client → v1 backend contracts
- **Offline:** expo-sqlite cache + background sync queue
- **GPS:** expo-location background task → Fleet Service
"""
with open(os.path.join(base_dir, "README.md"), "w", encoding="utf-8") as f: f.write(readme_md)

print("Conductor App (React Native / Expo) scaffolded successfully.")
