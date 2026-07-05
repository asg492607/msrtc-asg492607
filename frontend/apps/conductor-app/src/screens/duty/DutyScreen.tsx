import React from 'react';
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
