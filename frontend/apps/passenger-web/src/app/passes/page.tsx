'use client';
import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '../../lib/api/client';

export default function PassesPage() {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ type: 'MONTHLY', route: '' });

  const { data: passes, isLoading, refetch } = useQuery({ queryKey: ['passes'], queryFn: apiClient.passes.list });
  const { mutateAsync: purchase, isPending } = useMutation({ mutationFn: apiClient.passes.purchase });

  const handlePurchase = async () => {
    await purchase(form);
    setShowForm(false);
    refetch();
    alert('Pass purchased successfully! Check your email for the QR code.');
  };

  if (isLoading) return <div style={{ padding: '4rem', textAlign: 'center' }}>Loading passes…</div>;

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800 }}>My Passes</h1>
          <p style={{ color: '#777', marginTop: 4 }}>Monthly, quarterly & season passes</p>
        </div>
        <button onClick={() => setShowForm(!showForm)} style={{ background: '#0053A0', color: '#fff', border: 'none', borderRadius: 8, padding: '0.6rem 1.2rem', fontWeight: 700, cursor: 'pointer' }}>
          + Buy Pass
        </button>
      </div>

      {showForm && (
        <div style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', marginBottom: '1.5rem', boxShadow: '0 2px 12px rgba(0,0,0,0.1)', border: '1px solid #ddd' }}>
          <h3 style={{ marginBottom: '1rem' }}>Purchase New Pass</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>Pass Type</label>
              <select value={form.type} onChange={e => setForm({ ...form, type: e.target.value })} style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: 6, fontSize: '0.9rem' }}>
                <option value="MONTHLY">Monthly (₹1,800)</option>
                <option value="QUARTERLY">Quarterly (₹4,800)</option>
                <option value="ANNUAL">Annual (₹16,000)</option>
              </select>
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>Route</label>
              <input value={form.route} onChange={e => setForm({ ...form, route: e.target.value })} placeholder="e.g. Mumbai-Pune" style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: 6, fontSize: '0.9rem' }} />
            </div>
          </div>
          <button onClick={handlePurchase} disabled={isPending || !form.route} style={{ background: '#34a853', color: '#fff', border: 'none', borderRadius: 8, padding: '0.6rem 1.5rem', fontWeight: 700, cursor: 'pointer', opacity: (!form.route || isPending) ? 0.5 : 1 }}>
            {isPending ? 'Processing…' : 'Confirm Purchase'}
          </button>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {passes?.map((p: any) => (
          <div key={p.id} style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)', borderLeft: `4px solid ${p.status === 'ACTIVE' ? '#34a853' : '#ccc'}` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 4 }}>
                  <span style={{ fontWeight: 800, fontSize: '1rem' }}>{p.type} PASS</span>
                  <span style={{ background: p.status === 'ACTIVE' ? '#e6f4ea' : '#f0f0f0', color: p.status === 'ACTIVE' ? '#137333' : '#888', padding: '2px 10px', borderRadius: 20, fontSize: '0.75rem', fontWeight: 700 }}>{p.status}</span>
                </div>
                <div style={{ color: '#0053A0', fontWeight: 700 }}>{p.route}</div>
                <div style={{ fontSize: '0.82rem', color: '#999', marginTop: 4 }}>{p.validFrom} → {p.validUntil} · PNR: {p.pnr}</div>
              </div>
              {p.status === 'ACTIVE' && (
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.82rem', color: '#555' }}>Trips Used</div>
                  <div style={{ fontWeight: 800, fontSize: '1.2rem' }}>{p.tripsUsed}/{p.tripsAllowed}</div>
                </div>
              )}
            </div>
            {p.status === 'ACTIVE' && (
              <div style={{ marginTop: 12 }}>
                <div style={{ height: 6, background: '#eee', borderRadius: 3, overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${(p.tripsUsed / p.tripsAllowed * 100).toFixed(0)}%`, background: '#0053A0', borderRadius: 3 }} />
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
