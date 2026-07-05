import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';

export function usePaymentStatus(bookingId: string, enabled: boolean) {
  return useQuery({
    queryKey: ['paymentStatus', bookingId],
    queryFn: () => apiClient.payment.getStatus(bookingId),
    enabled,
    refetchInterval: (query) => {
       const status = query.state.data?.status;
       return (status === 'CONFIRMED' || status === 'FAILED') ? false : 2000;
    }
  });
}
