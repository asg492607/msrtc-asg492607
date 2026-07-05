export interface PassengerInput {
  seatId: string;
  seatNumber: string;
  name: string;
  age: string;
  gender: 'MALE' | 'FEMALE' | 'OTHER' | '';
}

export interface ContactDetailsInput {
  email: string;
  mobile: string;
}

export interface CreateBookingRequest {
  tripId: string;
  passengers: PassengerInput[];
  contact: ContactDetailsInput;
}
