'use client';
import { useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useSeatLayout } from '../../../features/seats/hooks/useSeatLayout';
import { useSeatLock } from '../../../features/seats/hooks/useSeatLock';
import { SeatMap } from '../../../features/seats/components/SeatMap';
import { FareSummary } from '../../../features/seats/components/FareSummary';
import { Timer } from '../../../features/seats/components/Timer';
import { Seat } from '../../../features/seats/types';

export default function SeatSelectionPage() {
  const searchParams = useSearchParams();
  const tripId = searchParams.get('tripId') || '';
  const router = useRouter();

  const { data: layout, isLoading } = useSeatLayout(tripId);
  const lockMutation = useSeatLock();
  
  const [selectedSeats, setSelectedSeats] = useState<Seat[]>([]);
  const [lockExpiresAt, setLockExpiresAt] = useState<number | null>(null);
  const [errorMsg, setErrorMsg] = useState('');

  const handleToggleSeat = (seat: Seat) => {
    if (lockExpiresAt) return; // Cannot modify selection after locking
    if (selectedSeats.find(s => s.id === seat.id)) {
      setSelectedSeats(selectedSeats.filter(s => s.id !== seat.id));
    } else {
      if (selectedSeats.length >= 6) {
         setErrorMsg("Maximum 6 seats allowed per booking.");
         return;
      }
      setSelectedSeats([...selectedSeats, seat]);
      setErrorMsg('');
    }
  };

  const handleProceed = async () => {
    if (selectedSeats.length === 0) return;
    try {
      const res = await lockMutation.mutateAsync({ tripId, seatIds: selectedSeats.map(s => s.id) });
      setLockExpiresAt(res.expiresAt);
      setErrorMsg('');
      // In a real app, wait a moment then redirect to Passenger details
      setTimeout(() => router.push(`/booking/passenger?tripId=${tripId}`), 2000);
    } catch (e: any) {
      setErrorMsg(e.message);
      setSelectedSeats([]); // Clear seats so they pick again
    }
  };

  if (isLoading || !layout) return <div style={{ padding: '2rem' }}>Loading seat map...</div>;

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
      <h1 style={{ marginBottom: '1rem' }}>Select Your Seats</h1>
      
      {errorMsg && <div style={{ padding: '1rem', background: '#fce8e6', color: '#c5221f', borderRadius: '8px', marginBottom: '1rem' }}>{errorMsg}</div>}
      
      {lockExpiresAt && (
        <div style={{ marginBottom: '1rem' }}>
           <Timer expiresAt={lockExpiresAt} onExpire={() => { setLockExpiresAt(null); setSelectedSeats([]); setErrorMsg('Reservation time expired. Please select seats again.'); }} />
           <p style={{ color: 'green', fontWeight: 'bold', marginTop: '0.5rem' }}>Seats Locked Successfully! Redirecting to passenger details...</p>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem', alignItems: 'start' }}>
        <SeatMap layout={layout as any} selectedSeatIds={selectedSeats.map(s => s.id)} onToggleSeat={handleToggleSeat} />
        <FareSummary selectedSeats={selectedSeats} onProceed={handleProceed} isLocking={lockMutation.isPending} />
      </div>
    </div>
  );
}
