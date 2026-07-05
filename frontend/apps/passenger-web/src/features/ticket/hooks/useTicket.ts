import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';

export function useTicket(pnr: string) {
  return useQuery({
    queryKey: ['ticket', pnr],
    queryFn: () => apiClient.ticket.get(pnr),
    enabled: !!pnr,
  });
}
