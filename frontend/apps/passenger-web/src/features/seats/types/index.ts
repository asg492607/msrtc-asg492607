export type SeatStatus = 'AVAILABLE' | 'BOOKED' | 'LOCKED' | 'SELECTED' | 'LADIES_ONLY';

export interface Seat {
  id: string;
  row: number;
  col: number;
  status: SeatStatus;
  fare: number;
  number: string;
}

export interface SeatLayout {
  tripId: string;
  rows: number;
  cols: number;
  seats: Seat[];
}
