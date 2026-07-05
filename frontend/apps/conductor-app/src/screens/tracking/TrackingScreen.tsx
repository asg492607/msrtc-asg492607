import React, { useState, useEffect } from 'react';
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
