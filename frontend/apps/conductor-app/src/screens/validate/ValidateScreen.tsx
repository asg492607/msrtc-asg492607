import React, { useState } from 'react';
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
