'use client';
import { Suspense } from 'react';
import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { PassengerForm } from '../../../features/booking/components/PassengerForm';
import { ContactDetails } from '../../../features/booking/components/ContactDetails';
import { BookingSummary } from '../../../features/booking/components/BookingSummary';
import { useBooking } from '../../../features/booking/hooks/useBooking';
import { PassengerInput, ContactDetailsInput } from '../../../features/booking/types';
import { validatePassenger, validateContact } from '../../../features/booking/schemas/validation';
import { Timer } from '../../../features/seats/components/Timer';

function PassengerDetailsPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const tripId = searchParams.get('tripId') || 'TRIP-MOCK';
  
  // Mock seats that were locked in the previous step
  // In a real app, this would come from a Zustand store or React Query
  const mockLockedSeats = [
    { seatId: 'S-1-1', seatNumber: '1' },
    { seatId: 'S-1-2', seatNumber: '2' }
  ];

  const [passengers, setPassengers] = useState<PassengerInput[]>(
    mockLockedSeats.map(s => ({ seatId: s.seatId, seatNumber: s.seatNumber, name: '', age: '', gender: '' }))
  );
  
  const [contact, setContact] = useState<ContactDetailsInput>({ email: '', mobile: '' });
  
  // Timer expires in 5 minutes from page load for this demo
  const [expiresAt] = useState(Date.now() + 5 * 60 * 1000); 
  const [isExpired, setIsExpired] = useState(false);

  const { mutateAsync: createBooking, isPending } = useBooking();

  const handlePassengerChange = (idx: number, field: keyof PassengerInput, val: string) => {
    const updated = [...passengers];
    updated[idx] = { ...updated[idx], [field]: val };
    setPassengers(updated);
  };

  const handleContactChange = (field: keyof ContactDetailsInput, val: string) => {
    setContact({ ...contact, [field]: val });
  };

  const isFormValid = 
    passengers.every(p => validatePassenger(p) === null) && 
    validateContact(contact) === null &&
    !isExpired;

  const handleProceed = async () => {
    try {
      const res = await createBooking({ tripId, passengers, contact });
      // Redirect to Payment Gateway simulation
      router.push(`/booking/payment?bookingId=${res.bookingId}`);
    } catch (e) {
      alert("Failed to create booking.");
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Passenger Details</h1>
        {!isExpired ? (
          <Timer expiresAt={expiresAt} onExpire={() => setIsExpired(true)} />
        ) : (
          <div style={{ color: 'red', fontWeight: 'bold' }}>Reservation Expired. Please restart.</div>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem', alignItems: 'start', opacity: isExpired ? 0.5 : 1, pointerEvents: isExpired ? 'none' : 'auto' }}>
        <div>
          <PassengerForm passengers={passengers} onChange={handlePassengerChange} />
          <ContactDetails contact={contact} onChange={handleContactChange} />
        </div>
        <BookingSummary 
          passengers={passengers} 
          onProceed={handleProceed} 
          isPending={isPending} 
          isValid={isFormValid} 
        />
      </div>
    </div>
  );
}

export default function PassengerDetailsPage() {
  return (
    <Suspense fallback={<div style={{ padding: '2rem' }}>Loading passenger details...</div>}>
      <PassengerDetailsPageContent />
    </Suspense>
  );
}
