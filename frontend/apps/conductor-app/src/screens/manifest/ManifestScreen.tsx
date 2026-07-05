import React from 'react';
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
