'use client';
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
