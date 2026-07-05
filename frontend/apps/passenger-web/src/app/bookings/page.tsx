'use client';
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../lib/api/client';

export default function BookingsPage() {
  const qc = useQueryClient();
  const [cancelInfo, setCancelInfo] = useState<any>(null);
  const { data: bookings, isLoading } = useQuery({ queryKey: ['bookings'], queryFn: apiClient.bookings.history });
  const { mutateAsync: cancel, isPending } = useMutation({
    mutationFn: apiClient.bookings.cancel,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['bookings'] }); }
  });

  const handleCancel = async (id: string) => {
    if (!confirm('Are you sure you want to cancel this booking? Refund will be processed within 5-7 business days.')) return;
    const res = await cancel(id);
    setCancelInfo(res);
  };

  const STATUS_COLORS: Record<string, string> = { CONFIRMED: '#0053A0', COMPLETED: '#34a853', CANCELLED: '#ea4335' };

  if (isLoading) return <div style={{ padding: '4rem', textAlign: 'center' }}>Loading bookings…</div>;

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '2rem' }}>
      <h1 style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: 6 }}>Booking History</h1>
      <p style={{ color: '#777', marginBottom: '1.5rem' }}>All your past and upcoming trips</p>

      {cancelInfo && (
        <div style={{ background: '#fff3cd', border: '1px solid #fbbc04', borderRadius: 10, padding: '1rem', marginBottom: '1.5rem' }}>
          ✅ Booking cancelled. Refund of <strong>₹{cancelInfo.refundAmount}</strong> will be processed in <strong>{cancelInfo.refundEta}</strong>.
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {bookings?.map((b: any) => (
          <div key={b.id} style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)', borderLeft: `4px solid ${STATUS_COLORS[b.status]}` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 }}>
              <div>
                <div style={{ fontWeight: 800, fontSize: '1.05rem', marginBottom: 2 }}>{b.route}</div>
                <div style={{ fontSize: '0.82rem', color: '#777' }}>📅 {b.date} · 💺 Seats: {b.seats.join(', ')} · PNR: <strong>{b.pnr}</strong></div>
              </div>
              <span style={{ background: STATUS_COLORS[b.status] + '18', color: STATUS_COLORS[b.status], padding: '3px 12px', borderRadius: 20, fontSize: '0.75rem', fontWeight: 800 }}>{b.status}</span>
            </div>
            <div style={{ fontSize: '0.82rem', color: '#555', marginBottom: 12 }}>Passengers: {b.passengers.join(' · ')}</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ fontWeight: 800, color: '#0053A0', fontSize: '1.1rem' }}>₹{b.fare}</div>
              <div style={{ display: 'flex', gap: 8 }}>
                <button style={{ background: '#eee', color: '#333', border: 'none', borderRadius: 8, padding: '0.4rem 1rem', fontWeight: 700, cursor: 'pointer', fontSize: '0.82rem' }}>🎫 View Ticket</button>
                {b.canCancel && (
                  <button onClick={() => handleCancel(b.id)} disabled={isPending} style={{ background: '#fce8e6', color: '#c5221f', border: 'none', borderRadius: 8, padding: '0.4rem 1rem', fontWeight: 700, cursor: 'pointer', fontSize: '0.82rem', opacity: isPending ? 0.5 : 1 }}>✕ Cancel</button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
