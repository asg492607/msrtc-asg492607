// Offline SQLite cache simulation using in-memory storage
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
