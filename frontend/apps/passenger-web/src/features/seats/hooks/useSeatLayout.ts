import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';
import { SeatLayout } from '../types';

export function useSeatLayout(tripId: string) {
  return useQuery<SeatLayout>({
    queryKey: ['seats', tripId],
    queryFn: () => apiClient.seats.getLayout(tripId) as Promise<SeatLayout>,
    enabled: !!tripId,
    refetchInterval: 5000, // Poll every 5s for live availability
  });
}
