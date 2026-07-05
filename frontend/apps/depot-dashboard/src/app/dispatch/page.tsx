"use client";
import { useState } from 'react';

const TRIPS = [
  { id: 'T-101', route: 'Mumbai → Pune', bus: 'MH-01-AB-1234', platform: 'P-3', dep: '07:30', status: 'DEPARTED', pax: 42, cap: 52, driver: 'Rajesh Kumar', conductor: 'Anil Patil' },
  { id: 'T-102', route: 'Mumbai → Nashik', bus: 'MH-01-CD-5678', platform: 'P-7', dep: '08:00', status: 'ON_TIME', pax: 38, cap: 52, driver: 'Suresh More', conductor: 'Dinesh Jadhav' },
  { id: 'T-103', route: 'Mumbai → Aurangabad', bus: 'MH-01-EF-9012', platform: 'P-1', dep: '08:30', status: 'DELAYED', pax: 51, cap: 52, driver: 'Manoj Desai', conductor: 'Priya Nair' },
  { id: 'T-104', route: 'Mumbai → Kolhapur', bus: 'MH-01-GH-3456', platform: 'P-5', dep: '09:00', status: 'ON_TIME', pax: 29, cap: 40, driver: 'Vijay Shinde', conductor: 'Suman Deshpande' },
  { id: 'T-105', route: 'Mumbai → Solapur', bus: 'MH-01-IJ-7890', platform: 'P-2', dep: '09:30', status: 'ON_TIME', pax: 44, cap: 52, driver: 'Ramesh Pawar', conductor: 'Kavita Mali' },
  { id: 'T-106', route: 'Mumbai → Nagpur', bus: 'MH-01-KL-1122', platform: 'P-9', dep: '10:00', status: 'CANCELLED', pax: 0, cap: 52, driver: '—', conductor: '—' },
];

const BADGE: Record<string, string> = { ON_TIME: 'badge-success', DEPARTED: 'badge-info', DELAYED: 'badge-warn', CANCELLED: 'badge-danger', ARRIVED: 'badge-neutral' };

export default function DispatchPage() {
  const [filter, setFilter] = useState('ALL');

  const filtered = filter === 'ALL' ? TRIPS : TRIPS.filter(t => t.status === filter);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Dispatch Board</h1>
        <p className="page-subtitle">Live departure management · Mumbai Central Depot</p>
      </div>

      <div className="card">
        <div className="toolbar">
          <span style={{ fontWeight: 700, fontSize: '0.95rem' }}>Filter:</span>
          {['ALL','ON_TIME','DELAYED','DEPARTED','CANCELLED'].map(s => (
            <button key={s} className={`btn btn-sm ${filter === s ? 'btn-primary' : ''}`} style={{ background: filter === s ? 'var(--depot-primary)' : '#eee', color: filter === s ? '#fff' : '#555' }} onClick={() => setFilter(s)}>{s.replace('_',' ')}</button>
          ))}
        </div>
        <table>
          <thead><tr><th>Trip ID</th><th>Route</th><th>Bus</th><th>Platform</th><th>Departure</th><th>Pax</th><th>Driver</th><th>Conductor</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            {filtered.map(t => (
              <tr key={t.id}>
                <td style={{ fontWeight: 700 }}>{t.id}</td>
                <td>{t.route}</td>
                <td style={{ fontFamily: 'monospace', fontSize: '0.82rem' }}>{t.bus}</td>
                <td style={{ fontWeight: 700, color: 'var(--depot-primary)' }}>{t.platform}</td>
                <td>{t.dep}</td>
                <td><span style={{ color: t.pax / t.cap > 0.9 ? 'var(--depot-danger)' : 'inherit' }}>{t.pax}/{t.cap}</span></td>
                <td style={{ fontSize: '0.83rem' }}>{t.driver}</td>
                <td style={{ fontSize: '0.83rem' }}>{t.conductor}</td>
                <td><span className={`badge ${BADGE[t.status] || 'badge-neutral'}`}>{t.status}</span></td>
                <td><button className="btn btn-sm btn-primary" style={{ opacity: t.status === 'CANCELLED' ? 0.4 : 1 }}>Manage</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
