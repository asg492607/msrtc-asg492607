import { useMutation } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';
import { CreateBookingRequest } from '../types';

export function useBooking() {
  return useMutation({
    mutationFn: (data: CreateBookingRequest) => apiClient.booking.createBooking(data),
  });
}
