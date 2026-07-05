import { useMutation } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';

export function useSeatLock() {
  return useMutation({
    mutationFn: (data: { tripId: string, seatIds: string[] }) => 
      apiClient.seats.lockSeats(data.tripId, data.seatIds),
  });
}
