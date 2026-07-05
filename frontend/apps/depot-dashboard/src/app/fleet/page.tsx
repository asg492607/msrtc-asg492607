"use client";
import { useState } from 'react';

const FLEET = [
  { id: 'B01', busNumber: 'MH-01-AB-1234', type: 'Shivneri AC', status: 'OPERATIONAL', driver: 'Rajesh Kumar', route: 'Mumbai-Pune', kmToday: 312, fuelLevel: 78, lastService: '2026-06-01', nextServiceDue: '2026-09-01' },
  { id: 'B02', busNumber: 'MH-01-CD-5678', type: 'Shivshahi', status: 'OPERATIONAL', driver: 'Suresh More', route: 'Mumbai-Nashik', kmToday: 187, fuelLevel: 55, lastService: '2026-05-15', nextServiceDue: '2026-08-15' },
  { id: 'B03', busNumber: 'MH-01-EF-9012', type: 'Ordinary', status: 'IN_MAINTENANCE', driver: '—', route: '—', kmToday: 0, fuelLevel: 30, lastService: '2026-04-20', nextServiceDue: '2026-07-20' },
  { id: 'B04', busNumber: 'MH-01-GH-3456', type: 'Hirkani', status: 'OPERATIONAL', driver: 'Vijay Shinde', route: 'Mumbai-Kolhapur', kmToday: 410, fuelLevel: 62, lastService: '2026-06-10', nextServiceDue: '2026-09-10' },
  { id: 'B05', busNumber: 'MH-01-IJ-7890', type: 'Shivneri AC', status: 'BREAKDOWN', driver: '—', route: '—', kmToday: 45, fuelLevel: 20, lastService: '2026-05-01', nextServiceDue: '2026-08-01' },
  { id: 'B06', busNumber: 'MH-01-KL-1122', type: 'Ordinary', status: 'IDLE', driver: '—', route: '—', kmToday: 0, fuelLevel: 90, lastService: '2026-06-20', nextServiceDue: '2026-09-20' },
];

const SBADGE: Record<string, string> = { OPERATIONAL: 'badge-success', IN_MAINTENANCE: 'badge-warn', BREAKDOWN: 'badge-danger', IDLE: 'badge-neutral' };

export default function FleetPage() {
  const [search, setSearch] = useState('');
  const filtered = FLEET.filter(b => b.busNumber.toLowerCase().includes(search.toLowerCase()) || b.type.toLowerCase().includes(search.toLowerCase()));
  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Fleet Management</h1>
        <p className="page-subtitle">62 buses registered · Mumbai Central Depot</p>
      </div>

      <div className="kpi-grid">
        {[{ label:'Operational',val:'47',c:'var(--depot-success)'},{label:'In Maintenance',val:'8',c:'var(--depot-warn)'},{label:'Breakdown',val:'4',c:'var(--depot-danger)'},{label:'Idle/Reserve',val:'3',c:'var(--depot-muted)'}].map(k => (
          <div key={k.label} className="kpi-card" style={{ borderTop: `3px solid ${k.c}` }}>
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value" style={{ color: k.c }}>{k.val}</div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="toolbar">
          <input className="search-input" placeholder="Search bus number or type..." value={search} onChange={e => setSearch(e.target.value)} />
          <button className="btn btn-primary">+ Add Bus</button>
        </div>
        <table>
          <thead><tr><th>Bus Number</th><th>Type</th><th>Status</th><th>Driver</th><th>Route</th><th>KM Today</th><th>Fuel %</th><th>Next Service</th><th>Action</th></tr></thead>
          <tbody>
            {filtered.map(b => (
              <tr key={b.id}>
                <td style={{ fontWeight: 700, fontFamily: 'monospace' }}>{b.busNumber}</td>
                <td>{b.type}</td>
                <td><span className={`badge ${SBADGE[b.status]}`}>{b.status.replace('_',' ')}</span></td>
                <td style={{ fontSize: '0.83rem' }}>{b.driver}</td>
                <td style={{ fontSize: '0.83rem' }}>{b.route}</td>
                <td>{b.kmToday} km</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <div className="progress-bar" style={{ width: 60 }}><div className="progress-fill" style={{ width: `${b.fuelLevel}%`, background: b.fuelLevel < 25 ? 'var(--depot-danger)' : 'var(--depot-primary)' }} /></div>
                    <span style={{ fontSize: '0.8rem' }}>{b.fuelLevel}%</span>
                  </div>
                </td>
                <td style={{ fontSize: '0.82rem', color: new Date(b.nextServiceDue) < new Date() ? 'var(--depot-danger)' : 'inherit', fontWeight: new Date(b.nextServiceDue) < new Date() ? 700 : 400 }}>{b.nextServiceDue}</td>
                <td><button className="btn btn-sm btn-primary">Details</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
