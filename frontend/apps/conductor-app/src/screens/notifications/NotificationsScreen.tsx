import React, { useState } from 'react';
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
