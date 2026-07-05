import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\passenger-web"

dirs = [
    "src/app/tracking",
    "src/app/passes",
    "src/app/parcels",
    "src/app/complaints",
    "src/app/notifications",
    "src/app/profile",
    "src/app/bookings",
    "src/features/tracking/components",
    "src/features/passes/components",
    "src/features/parcels/components",
    "src/features/complaints/components",
    "src/features/profile/components",
    "src/features/bookings/components",
]
for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# Extend API client
client_path = os.path.join(base_dir, "src/lib/api/client.ts")
with open(client_path, "r", encoding="utf-8") as f:
    client = f.read()

extra_apis = """
  tracking: {
    getBusPosition: async (tripId: string) => {
      await new Promise(r => setTimeout(r, 400));
      return {
        tripId, lat: 18.5204 + (Math.random() - 0.5) * 0.08,
        lng: 73.8567 + (Math.random() - 0.5) * 0.08,
        speed: Math.floor(Math.random() * 40) + 40,
        eta: `${Math.floor(Math.random() * 30) + 5} min`,
        nextStop: 'Pune Station', status: 'ON_TIME'
      };
    }
  },
  passes: {
    list: async () => {
      await new Promise(r => setTimeout(r, 300));
      return [
        { id:'PSS-001', type:'MONTHLY', route:'Mumbai-Pune', validFrom:'2026-07-01', validUntil:'2026-07-31', status:'ACTIVE', pnr:'PASS001', tripsUsed:12, tripsAllowed:60 },
        { id:'PSS-002', type:'QUARTERLY', route:'Mumbai-Nashik', validFrom:'2026-04-01', validUntil:'2026-06-30', status:'EXPIRED', pnr:'PASS002', tripsUsed:60, tripsAllowed:180 },
      ];
    },
    purchase: async (data: any) => {
      await new Promise(r => setTimeout(r, 800));
      return { success: true, passId: `PSS-${Date.now()}`, pnr: `PASS${Date.now()}` };
    }
  },
  parcels: {
    list: async () => {
      await new Promise(r => setTimeout(r, 300));
      return [
        { id:'PCL-001', from:'Mumbai', to:'Pune', weight:'5kg', status:'DELIVERED', trackingId:'TRK-12345', bookedOn:'2026-07-01', deliveredOn:'2026-07-02' },
        { id:'PCL-002', from:'Mumbai', to:'Nashik', weight:'2kg', status:'IN_TRANSIT', trackingId:'TRK-67890', bookedOn:'2026-07-04', deliveredOn:null },
      ];
    },
    book: async (data: any) => {
      await new Promise(r => setTimeout(r, 700));
      return { success: true, trackingId: `TRK-${Math.floor(Math.random()*99999)}`, fare: 120 };
    }
  },
  complaints: {
    list: async () => {
      await new Promise(r => setTimeout(r, 300));
      return [
        { id:'CMP-001', subject:'AC not working', type:'ONBOARD', status:'RESOLVED', createdAt:'2026-06-20', resolvedAt:'2026-06-21', response:'We apologize for the inconvenience. The issue has been fixed.' },
        { id:'CMP-002', subject:'Driver was rude', type:'CONDUCT', status:'UNDER_REVIEW', createdAt:'2026-07-03', resolvedAt:null, response:null },
      ];
    },
    submit: async (data: any) => {
      await new Promise(r => setTimeout(r, 600));
      return { success: true, complaintId: `CMP-${Date.now()}` };
    }
  },
  bookings: {
    history: async () => {
      await new Promise(r => setTimeout(r, 500));
      return [
        { id:'BKG-001', pnr:'PNR10001', route:'Mumbai → Pune', date:'2026-07-05', seats:['14','15'], passengers:['Amit Desai','Priya Desai'], fare:1050, status:'CONFIRMED', canCancel:true },
        { id:'BKG-002', pnr:'PNR10002', route:'Mumbai → Nashik', date:'2026-06-28', seats:['3'], passengers:['Amit Desai'], fare:520, status:'COMPLETED', canCancel:false },
        { id:'BKG-003', pnr:'PNR10003', route:'Mumbai → Kolhapur', date:'2026-06-15', seats:['22'], passengers:['Amit Desai'], fare:840, status:'CANCELLED', canCancel:false },
      ];
    },
    cancel: async (bookingId: string) => {
      await new Promise(r => setTimeout(r, 600));
      return { success: true, refundAmount: 945, refundEta: '5-7 business days' };
    }
  },
  profile: {
    get: async () => {
      await new Promise(r => setTimeout(r, 300));
      return { name:'Amit Desai', email:'amit.desai@gmail.com', phone:'9876543210', dob:'1990-05-15', gender:'MALE' };
    },
    update: async (data: any) => {
      await new Promise(r => setTimeout(r, 500));
      return { success: true };
    }
  },
"""

client = client.replace("  auth: {", extra_apis + "  auth: {")
with open(client_path, "w", encoding="utf-8") as f: f.write(client)


# ============================================================
# TASK 91 — Live GPS Bus Tracking Page
# ============================================================
tracking_page = """'use client';
import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { apiClient } from '../../lib/api/client';

export default function TrackingPage() {
  const params = useSearchParams();
  const tripId = params.get('tripId') || 'TRIP-MOCK-001';
  const [pos, setPos] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    const poll = async () => {
      const data = await apiClient.tracking.getBusPosition(tripId);
      setPos(data);
      setHistory(prev => [{ ...data, time: new Date().toLocaleTimeString() }, ...prev.slice(0, 4)]);
    };
    poll();
    const id = setInterval(poll, 10000);
    return () => clearInterval(id);
  }, [tripId]);

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '2rem' }}>
      <h1 style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: 6 }}>Live Bus Tracking</h1>
      <p style={{ color: '#777', marginBottom: '1.5rem' }}>Trip: {tripId} · Updates every 10s</p>

      {/* Map Placeholder */}
      <div style={{ background: 'linear-gradient(135deg, #0f172a, #1e3a5f)', borderRadius: 16, height: 280, display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.5rem', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', inset: 0, background: 'radial-gradient(circle at 40% 50%, rgba(66,153,225,0.2) 0%, transparent 60%)' }} />
        <div style={{ textAlign: 'center', zIndex: 1 }}>
          <div style={{ fontSize: 48, marginBottom: 8 }}>📍</div>
          <div style={{ color: '#fff', fontWeight: 700, fontSize: '1rem' }}>Maharashtra Live Map</div>
          <div style={{ color: 'rgba(255,255,255,0.55)', fontSize: '0.82rem', marginTop: 4 }}>Leaflet.js · v1 API: GET /v1/fleet/positions/{tripId}</div>
          {pos && (
            <div style={{ marginTop: 12, background: 'rgba(255,255,255,0.1)', borderRadius: 8, padding: '8px 16px', color: '#fff', fontSize: '0.82rem', fontFamily: 'monospace' }}>
              {pos.lat.toFixed(5)}, {pos.lng.toFixed(5)}
            </div>
          )}
        </div>
      </div>

      {pos && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
          {[
            { label: 'Current Speed', value: `${pos.speed} km/h`, icon: '⚡' },
            { label: 'ETA to Next Stop', value: pos.eta, icon: '⏱️' },
            { label: 'Next Stop', value: pos.nextStop, icon: '🚏' },
          ].map(s => (
            <div key={s.label} style={{ background: '#fff', borderRadius: 12, padding: '1rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)', textAlign: 'center' }}>
              <div style={{ fontSize: 24, marginBottom: 6 }}>{s.icon}</div>
              <div style={{ fontWeight: 800, fontSize: '1.1rem', color: '#0053A0' }}>{s.value}</div>
              <div style={{ fontSize: '0.75rem', color: '#999', marginTop: 2 }}>{s.label}</div>
            </div>
          ))}
        </div>
      )}

      <div style={{ background: '#fff', borderRadius: 12, padding: '1.25rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)' }}>
        <h3 style={{ fontWeight: 700, marginBottom: 12, fontSize: '0.95rem' }}>Position History</h3>
        {history.length === 0 ? <p style={{ color: '#aaa', fontSize: '0.85rem' }}>Waiting for GPS data…</p> : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead><tr>{['Time','Latitude','Longitude','Speed'].map(h => <th key={h} style={{ textAlign: 'left', padding: '6px 8px', fontSize: '0.75rem', color: '#999', fontWeight: 700, textTransform: 'uppercase', borderBottom: '1px solid #eee' }}>{h}</th>)}</tr></thead>
            <tbody>
              {history.map((p, i) => (
                <tr key={i} style={{ fontSize: '0.83rem' }}>
                  <td style={{ padding: '6px 8px', fontFamily: 'monospace' }}>{p.time}</td>
                  <td style={{ padding: '6px 8px', fontFamily: 'monospace' }}>{p.lat.toFixed(5)}</td>
                  <td style={{ padding: '6px 8px', fontFamily: 'monospace' }}>{p.lng.toFixed(5)}</td>
                  <td style={{ padding: '6px 8px' }}>{p.speed} km/h</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/tracking/page.tsx"), "w", encoding="utf-8") as f: f.write(tracking_page)


# ============================================================
# TASK 92 — Pass Management
# ============================================================
passes_page = """'use client';
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
"""
with open(os.path.join(base_dir, "src/app/passes/page.tsx"), "w", encoding="utf-8") as f: f.write(passes_page)


# ============================================================
# TASK 93 — Parcel Booking
# ============================================================
parcels_page = """'use client';
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
"""
with open(os.path.join(base_dir, "src/app/parcels/page.tsx"), "w", encoding="utf-8") as f: f.write(parcels_page)


# ============================================================
# TASK 94 — Complaints & Feedback
# ============================================================
complaints_page = """'use client';
import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '../../lib/api/client';

export default function ComplaintsPage() {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ type: 'ONBOARD', subject: '', description: '', pnr: '' });
  const [submitted, setSubmitted] = useState<any>(null);

  const { data: complaints, isLoading, refetch } = useQuery({ queryKey: ['complaints'], queryFn: apiClient.complaints.list });
  const { mutateAsync: submit, isPending } = useMutation({ mutationFn: apiClient.complaints.submit });

  const handleSubmit = async () => {
    const res = await submit(form);
    setSubmitted(res);
    setShowForm(false);
    setForm({ type: 'ONBOARD', subject: '', description: '', pnr: '' });
    refetch();
  };

  const STATUS_STYLE: Record<string, any> = {
    RESOLVED: { bg: '#e6f4ea', color: '#137333' },
    UNDER_REVIEW: { bg: '#fff3cd', color: '#856404' },
    OPEN: { bg: '#fce8e6', color: '#c5221f' }
  };

  if (isLoading) return <div style={{ padding: '4rem', textAlign: 'center' }}>Loading…</div>;

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800 }}>Complaints & Feedback</h1>
          <p style={{ color: '#777', marginTop: 4 }}>We value your experience and work to resolve all issues.</p>
        </div>
        <button onClick={() => setShowForm(true)} style={{ background: '#ea4335', color: '#fff', border: 'none', borderRadius: 8, padding: '0.6rem 1.2rem', fontWeight: 700, cursor: 'pointer' }}>+ Raise Complaint</button>
      </div>

      {submitted && (
        <div style={{ background: '#e6f4ea', border: '1px solid #34a853', borderRadius: 10, padding: '1rem', marginBottom: '1.5rem' }}>
          ✅ Complaint <strong>{submitted.complaintId}</strong> raised. We will respond within 48 hours.
        </div>
      )}

      {showForm && (
        <div style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', marginBottom: '1.5rem', boxShadow: '0 2px 12px rgba(0,0,0,0.1)' }}>
          <h3 style={{ marginBottom: '1rem' }}>New Complaint</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div>
                <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>Category</label>
                <select value={form.type} onChange={e => setForm({ ...form, type: e.target.value })} style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: 6 }}>
                  <option value="ONBOARD">Onboard Experience</option>
                  <option value="CONDUCT">Staff Conduct</option>
                  <option value="BOOKING">Booking Issue</option>
                  <option value="REFUND">Refund Delay</option>
                  <option value="OTHER">Other</option>
                </select>
              </div>
              <div>
                <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>PNR (if applicable)</label>
                <input value={form.pnr} onChange={e => setForm({ ...form, pnr: e.target.value })} placeholder="PNR12345" style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: 6 }} />
              </div>
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>Subject</label>
              <input value={form.subject} onChange={e => setForm({ ...form, subject: e.target.value })} placeholder="Brief description" style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: 6 }} />
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>Detailed Description</label>
              <textarea value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} rows={4} placeholder="Describe the issue in detail…" style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: 6, resize: 'vertical' }} />
            </div>
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <button onClick={handleSubmit} disabled={isPending || !form.subject} style={{ background: '#ea4335', color: '#fff', border: 'none', borderRadius: 8, padding: '0.6rem 1.5rem', fontWeight: 700, cursor: 'pointer', opacity: (!form.subject || isPending) ? 0.5 : 1 }}>{isPending ? 'Submitting…' : 'Submit Complaint'}</button>
            <button onClick={() => setShowForm(false)} style={{ background: '#eee', color: '#333', border: 'none', borderRadius: 8, padding: '0.6rem 1rem', fontWeight: 700, cursor: 'pointer' }}>Cancel</button>
          </div>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {complaints?.map((c: any) => (
          <div key={c.id} style={{ background: '#fff', borderRadius: 12, padding: '1.25rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <div style={{ fontWeight: 700 }}>{c.subject}</div>
              <span style={{ background: STATUS_STYLE[c.status]?.bg, color: STATUS_STYLE[c.status]?.color, padding: '3px 10px', borderRadius: 20, fontSize: '0.75rem', fontWeight: 700 }}>{c.status.replace('_', ' ')}</span>
            </div>
            <div style={{ fontSize: '0.82rem', color: '#999' }}>{c.type} · {c.createdAt} · {c.id}</div>
            {c.response && <div style={{ marginTop: 8, padding: '8px 12px', background: '#f0f4ff', borderRadius: 8, fontSize: '0.82rem', color: '#0053A0', borderLeft: '3px solid #0053A0' }}>📣 {c.response}</div>}
          </div>
        ))}
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/complaints/page.tsx"), "w", encoding="utf-8") as f: f.write(complaints_page)


# ============================================================
# TASK 96 — Profile & Settings  (95 = notifications prefs, inside profile)
# ============================================================
profile_page = """'use client';
import { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '../../lib/api/client';

export default function ProfilePage() {
  const [saved, setSaved] = useState(false);
  const [notifPrefs, setNotifPrefs] = useState({ email: true, sms: true, push: false, promotions: false });

  const { data: profile, isLoading } = useQuery({ queryKey: ['profile'], queryFn: apiClient.profile.get });
  const { mutateAsync: update, isPending } = useMutation({ mutationFn: apiClient.profile.update });
  const [form, setForm] = useState({ name: '', email: '', phone: '' });

  useEffect(() => { if (profile) setForm({ name: profile.name, email: profile.email, phone: profile.phone }); }, [profile]);

  const handleSave = async () => {
    await update(form);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  if (isLoading) return <div style={{ padding: '4rem', textAlign: 'center' }}>Loading profile…</div>;

  return (
    <div style={{ maxWidth: 760, margin: '0 auto', padding: '2rem' }}>
      <h1 style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: '1.5rem' }}>Profile & Settings</h1>

      {saved && <div style={{ background: '#e6f4ea', border: '1px solid #34a853', borderRadius: 8, padding: '0.75rem 1rem', marginBottom: '1.5rem', color: '#137333', fontWeight: 600 }}>✅ Profile updated successfully!</div>}

      {/* Profile */}
      <div style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)', marginBottom: '1.25rem' }}>
        <h3 style={{ fontWeight: 700, marginBottom: '1rem', fontSize: '1rem' }}>Personal Information</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
          {[{ key: 'name', label: 'Full Name', type: 'text' }, { key: 'email', label: 'Email Address', type: 'email' }, { key: 'phone', label: 'Mobile Number', type: 'tel' }].map(f => (
            <div key={f.key} style={{ gridColumn: f.key === 'name' ? '1 / -1' : 'auto' }}>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>{f.label}</label>
              <input type={f.type} value={(form as any)[f.key]} onChange={e => setForm({ ...form, [f.key]: e.target.value })} style={{ width: '100%', padding: '0.55rem 0.85rem', border: '1px solid #ddd', borderRadius: 8, fontSize: '0.9rem' }} />
            </div>
          ))}
        </div>
        <button onClick={handleSave} disabled={isPending} style={{ background: '#0053A0', color: '#fff', border: 'none', borderRadius: 8, padding: '0.55rem 1.5rem', fontWeight: 700, cursor: 'pointer', opacity: isPending ? 0.5 : 1 }}>{isPending ? 'Saving…' : 'Save Changes'}</button>
      </div>

      {/* Task 95 — Notification Preferences */}
      <div style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)', marginBottom: '1.25rem' }}>
        <h3 style={{ fontWeight: 700, marginBottom: '1rem', fontSize: '1rem' }}>Notification Preferences</h3>
        {[
          { key: 'email', label: 'Email Notifications', desc: 'Booking confirmations, tickets, receipts' },
          { key: 'sms', label: 'SMS Alerts', desc: 'OTPs, departure reminders, delays' },
          { key: 'push', label: 'Push Notifications', desc: 'Real-time updates via browser/app' },
          { key: 'promotions', label: 'Promotional Offers', desc: 'Discounts, new routes, seasonal offers' },
        ].map(n => (
          <div key={n.key} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.75rem 0', borderBottom: '1px solid #f0f0f0' }}>
            <div>
              <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{n.label}</div>
              <div style={{ fontSize: '0.78rem', color: '#999', marginTop: 2 }}>{n.desc}</div>
            </div>
            <label style={{ position: 'relative', display: 'inline-block', width: 40, height: 22 }}>
              <input type="checkbox" checked={(notifPrefs as any)[n.key]} onChange={e => setNotifPrefs({ ...notifPrefs, [n.key]: e.target.checked })} style={{ opacity: 0, width: 0, height: 0 }} />
              <span onClick={() => setNotifPrefs(p => ({ ...p, [n.key]: !(p as any)[n.key] }))} style={{ position: 'absolute', cursor: 'pointer', inset: 0, background: (notifPrefs as any)[n.key] ? '#0053A0' : '#ccc', borderRadius: 22, transition: '0.2s' }}>
                <span style={{ position: 'absolute', width: 16, height: 16, left: (notifPrefs as any)[n.key] ? 21 : 3, top: 3, background: '#fff', borderRadius: '50%', transition: '0.2s' }} />
              </span>
            </label>
          </div>
        ))}
      </div>

      {/* Security */}
      <div style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)' }}>
        <h3 style={{ fontWeight: 700, marginBottom: '1rem', fontSize: '1rem' }}>Security</h3>
        <button style={{ background: '#eee', color: '#333', border: 'none', borderRadius: 8, padding: '0.55rem 1.2rem', fontWeight: 700, cursor: 'pointer', marginRight: 8 }}>Change Password</button>
        <button style={{ background: '#fce8e6', color: '#c5221f', border: 'none', borderRadius: 8, padding: '0.55rem 1.2rem', fontWeight: 700, cursor: 'pointer' }}>Delete Account</button>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/profile/page.tsx"), "w", encoding="utf-8") as f: f.write(profile_page)


# ============================================================
# TASK 97 — Booking History & Cancellation
# ============================================================
bookings_page = """'use client';
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
"""
with open(os.path.join(base_dir, "src/app/bookings/page.tsx"), "w", encoding="utf-8") as f: f.write(bookings_page)


# ============================================================
# Update global nav to add new links
# ============================================================
nav_tsx = """// Navigation items for the Passenger Web app header/sidebar
export const NAV_LINKS = [
  { href: '/', label: 'Home', icon: '🏠' },
  { href: '/bookings', label: 'My Bookings', icon: '🎫' },
  { href: '/passes', label: 'Passes', icon: '🪪' },
  { href: '/parcels', label: 'Parcels', icon: '📦' },
  { href: '/tracking', label: 'Track Bus', icon: '📍' },
  { href: '/complaints', label: 'Complaints', icon: '📋' },
  { href: '/profile', label: 'Profile', icon: '👤' },
];
"""
with open(os.path.join(base_dir, "src/lib/nav.ts"), "w", encoding="utf-8") as f: f.write(nav_tsx)


print("Tasks 91-97: Passenger Web features scaffolded successfully.")
