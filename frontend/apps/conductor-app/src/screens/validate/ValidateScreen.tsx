import React, { useState } from 'react';
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
