import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\passenger-web"

dirs = [
    "src/features/seats/components",
    "src/features/seats/api",
    "src/features/seats/types",
    "src/features/seats/hooks",
    "src/app/booking/seats"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. Types
types_ts = """export type SeatStatus = 'AVAILABLE' | 'BOOKED' | 'LOCKED' | 'SELECTED' | 'LADIES_ONLY';

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
"""
with open(os.path.join(base_dir, "src/features/seats/types/index.ts"), "w", encoding="utf-8") as f: f.write(types_ts)


# 2. Mock API extension
client_path = os.path.join(base_dir, "src/lib/api/client.ts")
with open(client_path, "r", encoding="utf-8") as f:
    client_content = f.read()

# Add seats mock to client
seats_mock = """
  seats: {
    getLayout: async (tripId: string) => {
      console.log('Fetching layout for', tripId);
      await new Promise(r => setTimeout(r, 500));
      // Generate a mock 2x2 layout (4 columns: [Seat, Seat, Aisle, Seat, Seat])
      // We will model the aisle as empty space in the component, so columns 1,2 and 4,5
      const mockSeats = [];
      let seatCounter = 1;
      for(let r=1; r<=10; r++) {
         for(let c of [1,2, 4,5]) {
            let status = 'AVAILABLE';
            if(r === 1 && c === 1) status = 'BOOKED';
            if(r === 2 && c === 4) status = 'LOCKED';
            if(r === 3 && c === 1) status = 'LADIES_ONLY';
            
            mockSeats.push({
              id: `S-${r}-${c}`,
              row: r, col: c,
              status,
              fare: 500,
              number: `${seatCounter++}`
            });
         }
      }
      return { tripId, rows: 10, cols: 5, seats: mockSeats };
    },
    lockSeats: async (tripId: string, seatIds: string[]) => {
      console.log('Attempting Redis Lock for', seatIds);
      await new Promise(r => setTimeout(r, 800));
      // Simulate 10% chance of 409 Conflict (someone else locked it)
      if (Math.random() > 0.9) {
         throw new Error("409_CONFLICT: One or more seats are no longer available.");
      }
      return { success: true, expiresAt: Date.now() + 10 * 60 * 1000 };
    }
  },
"""
client_content = client_content.replace("  auth: {", seats_mock + "  auth: {")
with open(client_path, "w", encoding="utf-8") as f: f.write(client_content)


# 3. Hooks
layout_hook = """import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';
import { SeatLayout } from '../types';

export function useSeatLayout(tripId: string) {
  return useQuery<SeatLayout>({
    queryKey: ['seats', tripId],
    queryFn: () => apiClient.seats.getLayout(tripId),
    enabled: !!tripId,
    refetchInterval: 5000, // Poll every 5s for live availability
  });
}
"""
with open(os.path.join(base_dir, "src/features/seats/hooks/useSeatLayout.ts"), "w", encoding="utf-8") as f: f.write(layout_hook)

lock_hook = """import { useMutation } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';

export function useSeatLock() {
  return useMutation({
    mutationFn: (data: { tripId: string, seatIds: string[] }) => 
      apiClient.seats.lockSeats(data.tripId, data.seatIds),
  });
}
"""
with open(os.path.join(base_dir, "src/features/seats/hooks/useSeatLock.ts"), "w", encoding="utf-8") as f: f.write(lock_hook)


# 4. Components
timer_tsx = """'use client';
import { useState, useEffect } from 'react';

export function Timer({ expiresAt, onExpire }: { expiresAt: number, onExpire: () => void }) {
  const [timeLeft, setTimeLeft] = useState(Math.max(0, expiresAt - Date.now()));

  useEffect(() => {
    if (timeLeft <= 0) {
      onExpire();
      return;
    }
    const interval = setInterval(() => {
      const remaining = Math.max(0, expiresAt - Date.now());
      setTimeLeft(remaining);
      if (remaining <= 0) onExpire();
    }, 1000);
    return () => clearInterval(interval);
  }, [expiresAt, onExpire, timeLeft]);

  const minutes = Math.floor(timeLeft / 60000);
  const seconds = Math.floor((timeLeft % 60000) / 1000);
  const isWarning = timeLeft < 120000; // < 2 minutes

  if (timeLeft <= 0) return null;

  return (
    <div style={{ padding: '0.5rem 1rem', background: isWarning ? '#fce8e6' : '#e8f0fe', color: isWarning ? '#c5221f' : '#1967d2', borderRadius: '8px', fontWeight: 'bold', display: 'inline-block' }}>
      Time to complete booking: {minutes}:{seconds.toString().padStart(2, '0')}
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/features/seats/components/Timer.tsx"), "w", encoding="utf-8") as f: f.write(timer_tsx)

fare_tsx = """import { Seat } from '../types';
export function FareSummary({ selectedSeats, onProceed, isLocking }: { selectedSeats: Seat[], onProceed: () => void, isLocking: boolean }) {
  const totalFare = selectedSeats.reduce((sum, seat) => sum + seat.fare, 0);

  return (
    <div style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', position: 'sticky', top: '100px' }}>
      <h3 style={{ borderBottom: '1px solid #eee', paddingBottom: '0.5rem', marginBottom: '1rem' }}>Fare Summary</h3>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
        <span>Selected Seats ({selectedSeats.length})</span>
        <span>{selectedSeats.map(s => s.number).join(', ')}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold', fontSize: '1.2rem', marginTop: '1rem', borderTop: '1px solid #eee', paddingTop: '1rem' }}>
        <span>Total Payable</span>
        <span style={{ color: 'var(--color-primary)' }}>₹{totalFare}</span>
      </div>
      <button 
        onClick={onProceed} 
        disabled={selectedSeats.length === 0 || isLocking}
        className="btn-primary" 
        style={{ width: '100%', marginTop: '1.5rem', opacity: selectedSeats.length === 0 ? 0.5 : 1 }}
      >
        {isLocking ? 'Locking Seats...' : 'Proceed to Book'}
      </button>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/features/seats/components/FareSummary.tsx"), "w", encoding="utf-8") as f: f.write(fare_tsx)

map_tsx = """'use client';
import { SeatLayout, Seat } from '../types';

export function SeatMap({ layout, selectedSeatIds, onToggleSeat }: { layout: SeatLayout, selectedSeatIds: string[], onToggleSeat: (seat: Seat) => void }) {
  
  const getSeatStyle = (seat: Seat) => {
    const isSelected = selectedSeatIds.includes(seat.id);
    let bg = '#fff';
    let border = '1px solid #ccc';
    let cursor = 'pointer';

    if (isSelected) {
      bg = 'var(--color-primary)'; color = 'white'; border = '1px solid var(--color-primary-dark)';
    } else if (seat.status === 'BOOKED' || seat.status === 'LOCKED') {
      bg = '#eee'; color = '#aaa'; cursor = 'not-allowed'; border = '1px solid #ddd';
    } else if (seat.status === 'LADIES_ONLY') {
      bg = '#fce4ec'; color = '#c2185b'; border = '1px solid #f48fb1';
    }

    return { backgroundColor: bg, border, cursor, padding: '0.5rem', borderRadius: '4px', textAlign: 'center' as const, width: '40px', height: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.9rem', fontWeight: 'bold', color: isSelected ? 'white' : 'inherit' };
  };

  const rows = Array.from({ length: layout.rows }, (_, i) => i + 1);

  return (
    <div style={{ background: '#fafafa', padding: '2rem', borderRadius: '12px', border: '1px solid #eee' }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 40px)', gap: '10px', justifyContent: 'center' }}>
        {rows.map(row => (
           <React.Fragment key={row}>
             {[1,2,3,4,5].map(col => {
                if (col === 3) return <div key={`aisle-${row}`} style={{ width: '40px' }} />; // Aisle
                const seat = layout.seats.find(s => s.row === row && s.col === col);
                if (!seat) return <div key={`empty-${row}-${col}`} style={{ width: '40px' }} />;
                
                return (
                  <div 
                    key={seat.id} 
                    style={getSeatStyle(seat)}
                    onClick={() => {
                       if (seat.status === 'AVAILABLE' || seat.status === 'LADIES_ONLY') {
                           onToggleSeat(seat);
                       }
                    }}
                  >
                    {seat.number}
                  </div>
                );
             })}
           </React.Fragment>
        ))}
      </div>
    </div>
  );
}
import React from 'react';
"""
with open(os.path.join(base_dir, "src/features/seats/components/SeatMap.tsx"), "w", encoding="utf-8") as f: f.write(map_tsx)


# 5. Page
page_tsx = """'use client';
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
        <SeatMap layout={layout} selectedSeatIds={selectedSeats.map(s => s.id)} onToggleSeat={handleToggleSeat} />
        <FareSummary selectedSeats={selectedSeats} onProceed={handleProceed} isLocking={lockMutation.isPending} />
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/booking/seats/page.tsx"), "w", encoding="utf-8") as f: f.write(page_tsx)

print("Seat Selection flow scaffolded successfully.")
