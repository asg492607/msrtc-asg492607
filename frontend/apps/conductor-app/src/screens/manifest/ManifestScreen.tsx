import React, { useState, useMemo } from 'react';
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
