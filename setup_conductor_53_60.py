import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\conductor-app"

dirs = [
    "src/screens/duty",
    "src/screens/validate",
    "src/screens/manifest",
    "src/screens/tracking",
    "src/screens/notifications",
    "src/screens/offline",
    "src/components/ui",
    "src/lib/offline",
    "src/hooks",
]
for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# =============================================================
# TASK 53 — Duty Roster & Full Shift Management
# =============================================================
duty_full_tsx = """import React, { useState } from 'react';
import {
  View, Text, FlatList, StyleSheet,
  TouchableOpacity, ActivityIndicator, Alert, ScrollView
} from 'react-native';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { conductorApi } from '../../lib/api/client';
import { useAuthStore } from '../../store/useAuthStore';
import { DutyRoster } from '../../types';

export function DutyScreen() {
  const conductor = useAuthStore(s => s.conductor);
  const qc = useQueryClient();
  const [activeDuty, setActiveDuty] = useState<DutyRoster | null>(null);
  const [dutyLog, setDutyLog] = useState<string[]>([]);

  const { data: duties, isLoading } = useQuery({
    queryKey: ['duty', 'today'],
    queryFn: conductorApi.duty.getTodaysRoster,
  });

  const startDuty = (duty: DutyRoster) => {
    setActiveDuty(duty);
    setDutyLog(prev => [...prev, `${new Date().toLocaleTimeString()} — Duty STARTED: ${duty.source} → ${duty.destination}`]);
    Alert.alert('Duty Started', `Bus ${duty.busNumber} | ${duty.source} → ${duty.destination}`);
  };

  const endDuty = () => {
    if (!activeDuty) return;
    Alert.alert('End Duty', 'Are you sure you want to end this duty?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'End Duty', style: 'destructive', onPress: () => {
          setDutyLog(prev => [...prev, `${new Date().toLocaleTimeString()} — Duty ENDED: ${activeDuty.source} → ${activeDuty.destination}`]);
          setActiveDuty(null);
          qc.invalidateQueries({ queryKey: ['duty'] });
        }
      }
    ]);
  };

  if (isLoading) return <ActivityIndicator style={{ flex: 1 }} size="large" color="#0053A0" />;

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.greeting}>Good morning, {conductor?.name?.split(' ')[0]}</Text>
        <Text style={styles.subheader}>Depot: {conductor?.depotId}</Text>
      </View>

      {activeDuty && (
        <View style={styles.activeBanner}>
          <View>
            <Text style={styles.activeBannerLabel}>🟢 Active Duty</Text>
            <Text style={styles.activeBannerRoute}>{activeDuty.source} → {activeDuty.destination}</Text>
            <Text style={styles.activeBannerBus}>{activeDuty.busNumber} | Departure: {activeDuty.departureTime}</Text>
          </View>
          <TouchableOpacity style={styles.endBtn} onPress={endDuty}>
            <Text style={styles.endBtnText}>End</Text>
          </TouchableOpacity>
        </View>
      )}

      <Text style={styles.sectionTitle}>Today's Roster</Text>
      {duties?.map(duty => (
        <View key={duty.dutyId} style={[styles.card, duty.status === 'ACTIVE' && styles.activeCard]}>
          <View style={styles.cardHeader}>
            <Text style={styles.busNum}>{duty.busNumber}</Text>
            <View style={[styles.badge, { backgroundColor: duty.status === 'ACTIVE' ? '#34a853' : duty.status === 'COMPLETED' ? '#999' : '#fbbc04' }]}>
              <Text style={styles.badgeText}>{duty.status}</Text>
            </View>
          </View>
          <Text style={styles.route}>{duty.source} → {duty.destination}</Text>
          <Text style={styles.time}>⏰ {duty.departureTime} | 🕐 {duty.shift} SHIFT</Text>
          {duty.status === 'UPCOMING' && !activeDuty && (
            <TouchableOpacity style={styles.startBtn} onPress={() => startDuty(duty)}>
              <Text style={styles.startBtnText}>Start Duty</Text>
            </TouchableOpacity>
          )}
        </View>
      ))}

      {dutyLog.length > 0 && (
        <View style={styles.logCard}>
          <Text style={styles.logTitle}>Shift Activity Log</Text>
          {dutyLog.map((entry, i) => (
            <Text key={i} style={styles.logEntry}>• {entry}</Text>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f4f6fa' },
  header: { backgroundColor: '#0053A0', padding: 24, paddingTop: 48 },
  greeting: { fontSize: 22, fontWeight: '800', color: '#fff' },
  subheader: { fontSize: 13, color: 'rgba(255,255,255,0.8)', marginTop: 4 },
  activeBanner: { backgroundColor: '#e6f4ea', margin: 16, padding: 16, borderRadius: 12, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', borderLeftWidth: 4, borderLeftColor: '#34a853' },
  activeBannerLabel: { fontSize: 13, color: '#137333', fontWeight: '700', marginBottom: 4 },
  activeBannerRoute: { fontSize: 15, fontWeight: '700', color: '#1a1a1a' },
  activeBannerBus: { fontSize: 12, color: '#555', marginTop: 2 },
  endBtn: { backgroundColor: '#ea4335', borderRadius: 8, paddingHorizontal: 16, paddingVertical: 8 },
  endBtnText: { color: '#fff', fontWeight: '700' },
  sectionTitle: { fontSize: 15, fontWeight: '700', color: '#333', padding: 16, paddingBottom: 8 },
  card: { backgroundColor: '#fff', borderRadius: 12, padding: 16, marginHorizontal: 16, marginBottom: 12, elevation: 2 },
  activeCard: { borderLeftWidth: 4, borderLeftColor: '#0053A0' },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  busNum: { fontSize: 18, fontWeight: '800', color: '#0053A0' },
  badge: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 4 },
  badgeText: { color: '#fff', fontSize: 11, fontWeight: '700' },
  route: { fontSize: 15, fontWeight: '600', color: '#333', marginBottom: 4 },
  time: { fontSize: 12, color: '#777' },
  startBtn: { backgroundColor: '#0053A0', borderRadius: 8, padding: 10, alignItems: 'center', marginTop: 12 },
  startBtnText: { color: '#fff', fontWeight: '700', fontSize: 14 },
  logCard: { backgroundColor: '#fff', borderRadius: 12, margin: 16, padding: 16 },
  logTitle: { fontWeight: '700', color: '#333', marginBottom: 8 },
  logEntry: { fontSize: 12, color: '#555', marginBottom: 4, fontFamily: 'monospace' },
});
"""
with open(os.path.join(base_dir, "src/screens/duty/DutyScreen.tsx"), "w", encoding="utf-8") as f: f.write(duty_full_tsx)


# =============================================================
# TASK 54 — Enhanced QR Ticket Validation
# TASK 55 — Pass Validation
# Combined into ValidateScreen with tabs
# =============================================================
validate_tabs_tsx = """import React, { useState } from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity,
  TextInput, Alert, ActivityIndicator, Vibration, ScrollView
} from 'react-native';
import { conductorApi } from '../../lib/api/client';
import { ValidationResult } from '../../types';
import { offlineCache } from '../../lib/offline/cache';

type Tab = 'ticket' | 'pass';

export function ValidateScreen() {
  const [tab, setTab] = useState<Tab>('ticket');
  const [input, setInput] = useState('');
  const [result, setResult] = useState<ValidationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<ValidationResult[]>([]);

  const validate = async (value: string, type: Tab) => {
    if (!value) return;
    setLoading(true);
    setResult(null);
    try {
      const res = type === 'ticket'
        ? await conductorApi.validate.ticket(value)
        : await conductorApi.validate.pass(value);
      setResult(res);
      setHistory(prev => [res, ...prev.slice(0, 4)]);
      // Cache for offline reference
      offlineCache.saveValidation(value, res);
      Vibration.vibrate(res.valid ? 200 : [0, 100, 100, 100]);
    } catch (e) {
      // Offline fallback
      const cached = offlineCache.getValidation(value);
      if (cached) {
        setResult({ ...cached, message: cached.message + ' (Offline cached)' });
        Alert.alert('Offline Mode', 'Validated using cached data.');
      } else {
        Alert.alert('Network Error', 'Cannot validate. No cached data available.');
      }
    }
    setLoading(false);
    setInput('');
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.pageTitle}>Validation Center</Text>

      {/* Tab Switch */}
      <View style={styles.tabs}>
        <TouchableOpacity style={[styles.tab, tab === 'ticket' && styles.activeTab]} onPress={() => { setTab('ticket'); setResult(null); }}>
          <Text style={[styles.tabText, tab === 'ticket' && styles.activeTabText]}>🎫 Ticket</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.tab, tab === 'pass' && styles.activeTab]} onPress={() => { setTab('pass'); setResult(null); }}>
          <Text style={[styles.tabText, tab === 'pass' && styles.activeTabText]}>🪪 Pass</Text>
        </TouchableOpacity>
      </View>

      {/* Camera Area */}
      <View style={styles.scanArea}>
        <Text style={styles.cameraIcon}>📷</Text>
        <Text style={styles.cameraText}>Point camera at {tab === 'ticket' ? 'Ticket QR' : 'Pass QR'}</Text>
        <TouchableOpacity style={styles.simulateBtn} onPress={() => validate(tab === 'ticket' ? `PNR${Math.floor(Math.random() * 99999)}` : `PASS-MUM-${Math.floor(Math.random() * 9999)}`, tab)}>
          <Text style={styles.simulateBtnText}>Simulate {tab === 'ticket' ? 'Ticket' : 'Pass'} Scan</Text>
        </TouchableOpacity>
      </View>

      {/* Manual Input */}
      <View style={styles.manualCard}>
        <Text style={styles.sectionLabel}>Manual Entry</Text>
        <View style={styles.row}>
          <TextInput
            style={styles.input} value={input} onChangeText={setInput}
            placeholder={tab === 'ticket' ? 'PNR123456' : 'PASS-MUM-1234'}
            autoCapitalize="characters"
          />
          <TouchableOpacity style={styles.checkBtn} onPress={() => validate(input, tab)} disabled={loading || !input}>
            {loading ? <ActivityIndicator color="#fff" size="small" /> : <Text style={styles.checkBtnText}>✓</Text>}
          </TouchableOpacity>
        </View>
      </View>

      {/* Result */}
      {result && (
        <View style={[styles.resultCard, { borderColor: result.valid ? '#34a853' : '#ea4335', backgroundColor: result.valid ? '#e6f4ea' : '#fce8e6' }]}>
          <Text style={styles.resultIcon}>{result.valid ? '✅' : '❌'}</Text>
          <Text style={[styles.resultMsg, { color: result.valid ? '#137333' : '#c5221f' }]}>{result.message}</Text>
          {result.valid && (
            <View style={styles.resultDetails}>
              {result.pnr && <Text style={styles.resultDetail}>PNR: {result.pnr}</Text>}
              {result.passId && <Text style={styles.resultDetail}>Pass ID: {result.passId}</Text>}
              {result.passengerName && <Text style={styles.resultDetail}>Passenger: {result.passengerName}</Text>}
              {result.seatNumber && <Text style={styles.resultDetail}>Seat: {result.seatNumber}</Text>}
              {result.validUntil && <Text style={styles.resultDetail}>Valid Until: {result.validUntil}</Text>}
            </View>
          )}
        </View>
      )}

      {/* Recent History */}
      {history.length > 0 && (
        <View style={styles.historyCard}>
          <Text style={styles.sectionLabel}>Recent Scans</Text>
          {history.map((h, i) => (
            <View key={i} style={styles.historyRow}>
              <Text>{h.valid ? '✅' : '❌'}</Text>
              <Text style={styles.historyText} numberOfLines={1}>{h.pnr || h.passId || '—'} | {h.passengerName || 'Unknown'}</Text>
            </View>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f4f6fa' },
  pageTitle: { fontSize: 20, fontWeight: '800', color: '#0053A0', padding: 16, paddingTop: 48, paddingBottom: 8 },
  tabs: { flexDirection: 'row', marginHorizontal: 16, backgroundColor: '#e8eaf0', borderRadius: 10, padding: 4, marginBottom: 12 },
  tab: { flex: 1, paddingVertical: 8, alignItems: 'center', borderRadius: 8 },
  activeTab: { backgroundColor: '#fff', shadowColor: '#000', shadowOpacity: 0.1, shadowRadius: 4, elevation: 2 },
  tabText: { fontSize: 14, color: '#999', fontWeight: '600' },
  activeTabText: { color: '#0053A0' },
  scanArea: { backgroundColor: '#1a1a2e', borderRadius: 16, margin: 16, padding: 24, alignItems: 'center' },
  cameraIcon: { fontSize: 48, marginBottom: 8 },
  cameraText: { color: '#fff', fontSize: 14, fontWeight: '600' },
  simulateBtn: { marginTop: 14, backgroundColor: '#0053A0', borderRadius: 8, paddingHorizontal: 20, paddingVertical: 10 },
  simulateBtnText: { color: '#fff', fontWeight: '700', fontSize: 13 },
  manualCard: { backgroundColor: '#fff', borderRadius: 12, margin: 16, marginTop: 0, padding: 16 },
  sectionLabel: { fontSize: 14, fontWeight: '700', color: '#555', marginBottom: 8 },
  row: { flexDirection: 'row', gap: 8 },
  input: { flex: 1, borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12, fontSize: 14 },
  checkBtn: { backgroundColor: '#0053A0', borderRadius: 8, width: 48, alignItems: 'center', justifyContent: 'center' },
  checkBtnText: { color: '#fff', fontSize: 20, fontWeight: '700' },
  resultCard: { borderWidth: 2, borderRadius: 12, margin: 16, marginTop: 0, padding: 16, alignItems: 'center' },
  resultIcon: { fontSize: 40, marginBottom: 8 },
  resultMsg: { fontSize: 15, fontWeight: '700', textAlign: 'center', marginBottom: 8 },
  resultDetails: { width: '100%', gap: 4 },
  resultDetail: { fontSize: 13, color: '#333' },
  historyCard: { backgroundColor: '#fff', borderRadius: 12, margin: 16, marginTop: 0, padding: 16 },
  historyRow: { flexDirection: 'row', alignItems: 'center', gap: 8, paddingVertical: 6, borderBottomWidth: 1, borderBottomColor: '#f0f0f0' },
  historyText: { flex: 1, fontSize: 13, color: '#555' },
});
"""
with open(os.path.join(base_dir, "src/screens/validate/ValidateScreen.tsx"), "w", encoding="utf-8") as f: f.write(validate_tabs_tsx)


# =============================================================
# TASK 56 — Full Passenger Manifest with Mark Absent/Present
# =============================================================
manifest_full_tsx = """import React, { useState, useMemo } from 'react';
import {
  View, Text, FlatList, StyleSheet, TouchableOpacity,
  TextInput, Alert
} from 'react-native';

const INITIAL_PASSENGERS = Array.from({ length: 28 }, (_, i) => ({
  seatNo: String(i + 1).padStart(2, '0'),
  name: ['Amit Desai', 'Priya Sharma', 'Ravi Patil', 'Sunita Jadhav', 'Manoj Kulkarni', 'Deepa Nair', 'Vijay More'][i % 7],
  pnr: `PNR${10000 + i}`,
  status: (i === 5 || i === 17) ? 'ABSENT' : 'BOARDED' as 'BOARDED' | 'ABSENT',
  concession: i % 9 === 0 ? 'SR_CITIZEN' : i % 12 === 0 ? 'STUDENT' : null,
}));

export function ManifestScreen() {
  const [passengers, setPassengers] = useState(INITIAL_PASSENGERS);
  const [search, setSearch] = useState('');

  const filtered = useMemo(() =>
    passengers.filter(p =>
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      p.pnr.includes(search) ||
      p.seatNo.includes(search)
    ), [passengers, search]);

  const boarded = passengers.filter(p => p.status === 'BOARDED').length;
  const absent = passengers.filter(p => p.status === 'ABSENT').length;

  const toggleStatus = (pnr: string) => {
    setPassengers(prev => prev.map(p =>
      p.pnr === pnr ? { ...p, status: p.status === 'BOARDED' ? 'ABSENT' : 'BOARDED' } : p
    ));
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Passenger Manifest</Text>
        <Text style={styles.subtitle}>Mumbai → Pune | MH-01-AB-1234</Text>
        <View style={styles.statsRow}>
          <View style={styles.stat}><Text style={styles.statNum}>{passengers.length}</Text><Text style={styles.statLabel}>Total</Text></View>
          <View style={styles.stat}><Text style={[styles.statNum, { color: '#8fff8f' }]}>{boarded}</Text><Text style={styles.statLabel}>Boarded</Text></View>
          <View style={styles.stat}><Text style={[styles.statNum, { color: '#ff8f8f' }]}>{absent}</Text><Text style={styles.statLabel}>Absent</Text></View>
        </View>
      </View>

      <View style={styles.searchRow}>
        <TextInput style={styles.searchInput} value={search} onChangeText={setSearch} placeholder="Search name, PNR or seat..." />
      </View>

      <FlatList
        data={filtered}
        keyExtractor={p => p.pnr}
        renderItem={({ item }) => (
          <View style={styles.row}>
            <View style={[styles.seatBadge, { backgroundColor: item.status === 'BOARDED' ? '#e8f0fe' : '#fce8e6' }]}>
              <Text style={[styles.seatNo, { color: item.status === 'BOARDED' ? '#0053A0' : '#c5221f' }]}>{item.seatNo}</Text>
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.name}>{item.name}</Text>
              <Text style={styles.pnr}>{item.pnr}{item.concession ? ` · ${item.concession.replace('_', ' ')}` : ''}</Text>
            </View>
            <TouchableOpacity
              style={[styles.toggleBtn, { backgroundColor: item.status === 'BOARDED' ? '#e6f4ea' : '#fce8e6' }]}
              onPress={() => toggleStatus(item.pnr)}
            >
              <Text style={[styles.toggleText, { color: item.status === 'BOARDED' ? '#137333' : '#c5221f' }]}>
                {item.status === 'BOARDED' ? '✓' : '✗'}
              </Text>
            </TouchableOpacity>
          </View>
        )}
        contentContainerStyle={{ padding: 12, paddingBottom: 32 }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f4f6fa' },
  header: { backgroundColor: '#0053A0', padding: 24, paddingTop: 48 },
  title: { fontSize: 20, fontWeight: '800', color: '#fff' },
  subtitle: { fontSize: 12, color: 'rgba(255,255,255,0.8)', marginTop: 4, marginBottom: 14 },
  statsRow: { flexDirection: 'row', gap: 12 },
  stat: { alignItems: 'center', backgroundColor: 'rgba(255,255,255,0.15)', borderRadius: 8, paddingVertical: 8, paddingHorizontal: 14 },
  statNum: { fontSize: 20, fontWeight: '900', color: '#fff' },
  statLabel: { fontSize: 10, color: 'rgba(255,255,255,0.7)', marginTop: 2 },
  searchRow: { padding: 12 },
  searchInput: { backgroundColor: '#fff', borderRadius: 10, padding: 12, fontSize: 14, borderWidth: 1, borderColor: '#ddd' },
  row: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff', borderRadius: 10, padding: 12, marginBottom: 6, gap: 10 },
  seatBadge: { width: 38, height: 38, borderRadius: 19, justifyContent: 'center', alignItems: 'center' },
  seatNo: { fontWeight: '800', fontSize: 13 },
  name: { fontWeight: '600', color: '#333', fontSize: 14 },
  pnr: { fontSize: 11, color: '#999', marginTop: 1 },
  toggleBtn: { width: 36, height: 36, borderRadius: 18, justifyContent: 'center', alignItems: 'center' },
  toggleText: { fontSize: 18, fontWeight: '700' },
});
"""
with open(os.path.join(base_dir, "src/screens/manifest/ManifestScreen.tsx"), "w", encoding="utf-8") as f: f.write(manifest_full_tsx)


# =============================================================
# TASK 57 — GPS Background Tracking (Enhanced)
# =============================================================
tracking_full_tsx = """import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, Switch, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { conductorApi } from '../../lib/api/client';

interface GPSPoint { lat: number; lng: number; time: string; accuracy: number; }

export function TrackingScreen() {
  const [tracking, setTracking] = useState(false);
  const [coords, setCoords] = useState<GPSPoint | null>(null);
  const [log, setLog] = useState<GPSPoint[]>([]);
  const [pushCount, setPushCount] = useState(0);
  const intervalRef = useRef<any>(null);

  const ACTIVE_TRIP = { id: 'TRIP-MUM-PUN-001', route: 'Mumbai → Pune', bus: 'MH-01-AB-1234' };

  const startTracking = () => {
    setTracking(true);
    intervalRef.current = setInterval(() => {
      const lat = 18.5204 + (Math.random() - 0.5) * 0.05;
      const lng = 73.8567 + (Math.random() - 0.5) * 0.05;
      const accuracy = Math.floor(Math.random() * 8) + 3;
      const point: GPSPoint = { lat, lng, time: new Date().toLocaleTimeString(), accuracy };
      setCoords(point);
      setLog(prev => [point, ...prev.slice(0, 9)]);
      setPushCount(prev => prev + 1);
      conductorApi.gps.pushLocation(lat, lng, ACTIVE_TRIP.id);
    }, 5000);
  };

  const stopTracking = () => {
    setTracking(false);
    if (intervalRef.current) clearInterval(intervalRef.current);
  };

  useEffect(() => () => { if (intervalRef.current) clearInterval(intervalRef.current); }, []);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.pageTitle}>GPS Tracking</Text>

      <View style={styles.tripCard}>
        <Text style={styles.tripLabel}>Active Trip</Text>
        <Text style={styles.tripRoute}>{ACTIVE_TRIP.route}</Text>
        <Text style={styles.tripBus}>{ACTIVE_TRIP.bus} · {ACTIVE_TRIP.id}</Text>
      </View>

      <View style={styles.card}>
        <View style={styles.row}>
          <View>
            <Text style={styles.label}>Background Tracking</Text>
            <Text style={styles.hint}>Pushes to Fleet Service every 30s</Text>
          </View>
          <Switch value={tracking} onValueChange={v => v ? startTracking() : stopTracking()} trackColor={{ false: '#ccc', true: '#0053A0' }} thumbColor="#fff" />
        </View>
      </View>

      <View style={[styles.statusCard, { borderColor: tracking ? '#34a853' : '#ddd' }]}>
        <View style={[styles.dot, { backgroundColor: tracking ? '#34a853' : '#ccc' }]} />
        <View>
          <Text style={styles.statusText}>{tracking ? 'Transmitting' : 'Inactive'}</Text>
          <Text style={styles.hint}>{pushCount} updates sent this session</Text>
        </View>
      </View>

      {coords && (
        <View style={styles.card}>
          <Text style={styles.label}>Current Position</Text>
          <Text style={styles.coord}>Lat: {coords.lat.toFixed(6)}</Text>
          <Text style={styles.coord}>Lng: {coords.lng.toFixed(6)}</Text>
          <Text style={styles.coord}>Accuracy: ±{coords.accuracy}m</Text>
          <Text style={styles.hint}>Updated: {coords.time}</Text>
        </View>
      )}

      {log.length > 0 && (
        <View style={styles.card}>
          <Text style={styles.label}>Location History (Session)</Text>
          {log.map((p, i) => (
            <View key={i} style={styles.logRow}>
              <Text style={styles.logTime}>{p.time}</Text>
              <Text style={styles.logCoord}>{p.lat.toFixed(4)}, {p.lng.toFixed(4)}</Text>
            </View>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f4f6fa' },
  pageTitle: { fontSize: 20, fontWeight: '800', color: '#0053A0', padding: 16, paddingTop: 48, paddingBottom: 8 },
  tripCard: { backgroundColor: '#0053A0', margin: 16, borderRadius: 12, padding: 16 },
  tripLabel: { fontSize: 12, color: 'rgba(255,255,255,0.7)', marginBottom: 4 },
  tripRoute: { fontSize: 18, fontWeight: '800', color: '#fff' },
  tripBus: { fontSize: 12, color: 'rgba(255,255,255,0.8)', marginTop: 4 },
  card: { backgroundColor: '#fff', borderRadius: 12, margin: 16, marginTop: 0, padding: 16 },
  row: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  label: { fontSize: 15, fontWeight: '700', color: '#333', marginBottom: 4 },
  hint: { fontSize: 12, color: '#999' },
  statusCard: { flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: '#fff', borderRadius: 12, margin: 16, marginTop: 0, padding: 16, borderWidth: 2 },
  dot: { width: 14, height: 14, borderRadius: 7 },
  statusText: { fontSize: 15, fontWeight: '700', color: '#333' },
  coord: { fontSize: 13, color: '#555', fontFamily: 'monospace', marginTop: 2 },
  logRow: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 4, borderBottomWidth: 1, borderBottomColor: '#f0f0f0' },
  logTime: { fontSize: 12, color: '#999', width: 70 },
  logCoord: { fontSize: 12, color: '#555', fontFamily: 'monospace' },
});
"""
with open(os.path.join(base_dir, "src/screens/tracking/TrackingScreen.tsx"), "w", encoding="utf-8") as f: f.write(tracking_full_tsx)


# =============================================================
# TASK 58 — Offline Cache Utility
# =============================================================
cache_ts = """// Offline SQLite cache simulation using in-memory storage
// In production, this uses expo-sqlite for persistent storage

const cache: Record<string, any> = {};

export const offlineCache = {
  saveValidation: (key: string, result: any) => {
    cache[`validation_${key}`] = { ...result, cachedAt: new Date().toISOString() };
  },
  getValidation: (key: string) => cache[`validation_${key}`] || null,

  saveDutyRoster: (data: any[]) => {
    cache['duty_roster'] = { data, cachedAt: new Date().toISOString() };
  },
  getDutyRoster: () => cache['duty_roster']?.data || null,

  queueGpsUpdate: (lat: number, lng: number, tripId: string) => {
    if (!cache['gps_queue']) cache['gps_queue'] = [];
    cache['gps_queue'].push({ lat, lng, tripId, timestamp: Date.now() });
  },
  flushGpsQueue: () => {
    const q = cache['gps_queue'] || [];
    cache['gps_queue'] = [];
    return q;
  },
};
"""
with open(os.path.join(base_dir, "src/lib/offline/cache.ts"), "w", encoding="utf-8") as f: f.write(cache_ts)


# =============================================================
# TASK 59 — Notifications Screen
# =============================================================
notif_tsx = """import React, { useState } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity } from 'react-native';

type NotifType = 'DUTY_CHANGE' | 'INCIDENT' | 'SYSTEM' | 'DISPATCH';

interface Notification {
  id: string;
  type: NotifType;
  title: string;
  body: string;
  time: string;
  read: boolean;
}

const MOCK_NOTIFS: Notification[] = [
  { id: 'N1', type: 'DUTY_CHANGE', title: 'Duty Reassigned', body: 'Your afternoon duty bus has changed to MH-01-EF-9012. Please check the roster.', time: '10:30 AM', read: false },
  { id: 'N2', type: 'INCIDENT', title: 'Accident Alert', body: 'Minor accident reported on NH-48 near Khopoli. Expect 20-min delay.', time: '9:15 AM', read: false },
  { id: 'N3', type: 'DISPATCH', title: 'Platform Change', body: 'Your bus departs from Platform 7 instead of Platform 3.', time: '8:45 AM', read: true },
  { id: 'N4', type: 'SYSTEM', title: 'App Update Available', body: 'Version 1.2.0 is available with offline sync improvements.', time: 'Yesterday', read: true },
];

const typeColors: Record<NotifType, string> = {
  DUTY_CHANGE: '#fbbc04',
  INCIDENT: '#ea4335',
  DISPATCH: '#0053A0',
  SYSTEM: '#34a853',
};

const typeIcons: Record<NotifType, string> = {
  DUTY_CHANGE: '🔄',
  INCIDENT: '⚠️',
  DISPATCH: '🚌',
  SYSTEM: '⚙️',
};

export function NotificationsScreen() {
  const [notifs, setNotifs] = useState(MOCK_NOTIFS);

  const markAllRead = () => setNotifs(prev => prev.map(n => ({ ...n, read: true })));
  const unreadCount = notifs.filter(n => !n.read).length;

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Notifications</Text>
        {unreadCount > 0 && (
          <TouchableOpacity onPress={markAllRead}>
            <Text style={styles.markAll}>Mark all read ({unreadCount})</Text>
          </TouchableOpacity>
        )}
      </View>

      <FlatList
        data={notifs}
        keyExtractor={n => n.id}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={[styles.card, !item.read && styles.unreadCard]}
            onPress={() => setNotifs(prev => prev.map(n => n.id === item.id ? { ...n, read: true } : n))}
          >
            <View style={[styles.iconBadge, { backgroundColor: typeColors[item.type] }]}>
              <Text style={styles.icon}>{typeIcons[item.type]}</Text>
            </View>
            <View style={{ flex: 1 }}>
              <View style={styles.cardHeader}>
                <Text style={styles.cardTitle}>{item.title}</Text>
                {!item.read && <View style={styles.unreadDot} />}
              </View>
              <Text style={styles.cardBody} numberOfLines={2}>{item.body}</Text>
              <Text style={styles.cardTime}>{item.time}</Text>
            </View>
          </TouchableOpacity>
        )}
        contentContainerStyle={{ padding: 12, paddingBottom: 32 }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f4f6fa' },
  header: { backgroundColor: '#0053A0', padding: 24, paddingTop: 48, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  title: { fontSize: 20, fontWeight: '800', color: '#fff' },
  markAll: { fontSize: 13, color: 'rgba(255,255,255,0.85)', textDecorationLine: 'underline' },
  card: { flexDirection: 'row', backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 8, gap: 12, elevation: 1 },
  unreadCard: { borderLeftWidth: 3, borderLeftColor: '#0053A0', backgroundColor: '#f0f4ff' },
  iconBadge: { width: 40, height: 40, borderRadius: 20, justifyContent: 'center', alignItems: 'center' },
  icon: { fontSize: 18 },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 },
  cardTitle: { fontWeight: '700', color: '#1a1a1a', fontSize: 14 },
  unreadDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: '#0053A0' },
  cardBody: { fontSize: 13, color: '#666', lineHeight: 18 },
  cardTime: { fontSize: 11, color: '#aaa', marginTop: 4 },
});
"""
with open(os.path.join(base_dir, "src/screens/notifications/NotificationsScreen.tsx"), "w", encoding="utf-8") as f: f.write(notif_tsx)


# =============================================================
# TASK 60 — Update API Client with Pass Validation
#           + Update App.tsx with 5-tab navigation + notifications
# =============================================================

# Update API client with pass validation
client_path = os.path.join(base_dir, "src/lib/api/client.ts")
with open(client_path, "r", encoding="utf-8") as f:
    client = f.read()

client = client.replace(
    "    ticket: async (qrData: string) => {",
    """    pass: async (passId: string) => {
      await new Promise(r => setTimeout(r, 500));
      if (passId.startsWith('PASS')) {
        return {
          valid: true,
          passId,
          passengerName: 'Suresh Pawar',
          validUntil: '2026-07-31',
          message: 'Monthly Pass valid — Board allowed'
        };
      }
      return { valid: false, message: 'Invalid or expired pass' };
    },

    ticket: async (qrData: string) => {"""
)
with open(client_path, "w", encoding="utf-8") as f: f.write(client)

# Update types to include passId and validUntil
types_path = os.path.join(base_dir, "src/types/index.ts")
with open(types_path, "r", encoding="utf-8") as f:
    types = f.read()

types = types.replace(
    "  message: string;\n}",
    "  message: string;\n  passId?: string;\n  validUntil?: string;\n}"
)
with open(types_path, "w", encoding="utf-8") as f: f.write(types)

# Update App.tsx with 5 tabs including Notifications
app_tsx = """import React, { useState } from 'react';
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
"""
with open(os.path.join(base_dir, "App.tsx"), "w", encoding="utf-8") as f: f.write(app_tsx)

print("Tasks 53-60: Conductor App complete — All screens, offline cache, and 5-tab navigation done.")
