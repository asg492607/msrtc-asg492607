import React, { useState, useEffect, useRef } from 'react';
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
