export const CacheKeys = {
  AUTH_OTP: (mobile: string) => `auth:otp:${mobile}`,
  AUTH_REFRESH: (userId: string) => `auth:refresh:${userId}`,
  BOOKING_SEARCH: (hash: string) => `booking:search:${hash}`,
  SEAT_LOCK: (tripId: string, seatNo: string) => `seat:lock:${tripId}:${seatNo}`,
  GPS_BUS: (vehicleId: string) => `gps:bus:${vehicleId}`,
  HQ_KPI_TODAY: 'hq:kpi:today',
  FINANCE_SUMMARY: (date: string) => `finance:summary:${date}`,
  NOTIFICATION_RATE: (userId: string) => `notification:rate:${userId}`,
};
