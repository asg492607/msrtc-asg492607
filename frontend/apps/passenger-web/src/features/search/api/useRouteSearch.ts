import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';
import { Trip } from '../types';

export function useRouteSearch(source: string, destination: string, date: string) {
  return useQuery<Trip[]>({
    queryKey: ['routes', source, destination, date],
    queryFn: () => apiClient.routes.search(source, destination, date),
    enabled: !!source && !!destination && !!date,
    staleTime: 60 * 1000, // Cache for 1 minute to avoid spamming the backend
  });
}
