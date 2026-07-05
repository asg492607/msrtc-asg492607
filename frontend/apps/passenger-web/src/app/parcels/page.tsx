'use client';
import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '../../lib/api/client';

const STATUS_COLOR: Record<string, string> = {
  DELIVERED: '#34a853', IN_TRANSIT: '#0053A0', PENDING: '#fbbc04', CANCELLED: '#ea4335'
};

export default function ParcelsPage() {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ from: '', to: '', weight: '', description: '' });
  const [confirmation, setConfirmation] = useState<any>(null);

  const { data: parcels, isLoading, refetch } = useQuery({ queryKey: ['parcels'], queryFn: apiClient.parcels.list });
  const { mutateAsync: book, isPending } = useMutation({ mutationFn: apiClient.parcels.book });

  const handleBook = async () => {
    const res = await book(form);
    setConfirmation(res);
    setShowForm(false);
    refetch();
  };

  if (isLoading) return <div style={{ padding: '4rem', textAlign: 'center' }}>Loading parcels…</div>;

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800 }}>Parcel Booking</h1>
          <p style={{ color: '#777', marginTop: 4 }}>Send parcels via MSRTC buses</p>
        </div>
        <button onClick={() => setShowForm(true)} style={{ background: '#0053A0', color: '#fff', border: 'none', borderRadius: 8, padding: '0.6rem 1.2rem', fontWeight: 700, cursor: 'pointer' }}>
          + New Parcel
        </button>
      </div>

      {confirmation && (
        <div style={{ background: '#e6f4ea', border: '1px solid #34a853', borderRadius: 10, padding: '1rem', marginBottom: '1.5rem' }}>
          ✅ <strong>Parcel booked!</strong> Tracking ID: <strong>{confirmation.trackingId}</strong> · Fare: ₹{confirmation.fare}
        </div>
      )}

      {showForm && (
        <div style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', marginBottom: '1.5rem', boxShadow: '0 2px 12px rgba(0,0,0,0.1)' }}>
          <h3 style={{ marginBottom: '1rem' }}>Book Parcel</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
            {[{ key: 'from', label: 'From City', ph: 'Mumbai' }, { key: 'to', label: 'To City', ph: 'Pune' }, { key: 'weight', label: 'Weight (kg)', ph: '5' }, { key: 'description', label: 'Description', ph: 'Household items' }].map(f => (
              <div key={f.key}>
                <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>{f.label}</label>
                <input value={(form as any)[f.key]} onChange={e => setForm({ ...form, [f.key]: e.target.value })} placeholder={f.ph} style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: 6, fontSize: '0.9rem' }} />
              </div>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <button onClick={handleBook} disabled={isPending || !form.from || !form.to || !form.weight} style={{ background: '#0053A0', color: '#fff', border: 'none', borderRadius: 8, padding: '0.6rem 1.5rem', fontWeight: 700, cursor: 'pointer', opacity: (!form.from || !form.to || !form.weight || isPending) ? 0.5 : 1 }}>
              {isPending ? 'Booking…' : 'Book Parcel'}
            </button>
            <button onClick={() => setShowForm(false)} style={{ background: '#eee', color: '#333', border: 'none', borderRadius: 8, padding: '0.6rem 1rem', fontWeight: 700, cursor: 'pointer' }}>Cancel</button>
          </div>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {parcels?.map((p: any) => (
          <div key={p.id} style={{ background: '#fff', borderRadius: 12, padding: '1.25rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontWeight: 700 }}>{p.from} → {p.to} · {p.weight}</div>
              <div style={{ fontSize: '0.82rem', color: '#999', marginTop: 4 }}>Tracking: <span style={{ fontFamily: 'monospace', fontWeight: 700 }}>{p.trackingId}</span> · Booked: {p.bookedOn}</div>
            </div>
            <span style={{ background: STATUS_COLOR[p.status] + '22', color: STATUS_COLOR[p.status], padding: '4px 12px', borderRadius: 20, fontSize: '0.78rem', fontWeight: 800 }}>{p.status.replace('_', ' ')}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
