import React, { useState } from 'react';
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
