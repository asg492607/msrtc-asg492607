"use client";
import { useState } from 'react';

const JOBS = [
  { id:'JOB-001', busNumber:'MH-01-EF-9012', type:'Engine Overhaul', priority:'HIGH', status:'IN_PROGRESS', mechanic:'Ganesh Kamble', openedAt:'2026-07-01', estimatedCompletion:'2026-07-07', notes:'Cylinder head replacement required' },
  { id:'JOB-002', busNumber:'MH-01-IJ-7890', type:'Brake System Failure', priority:'HIGH', status:'OPEN', mechanic:'', openedAt:'2026-07-05', estimatedCompletion:'2026-07-06', notes:'Brake fluid leak, urgent fix required' },
  { id:'JOB-003', busNumber:'MH-01-MN-4567', type:'AC Service', priority:'MEDIUM', status:'COMPLETED', mechanic:'Ramesh Kale', openedAt:'2026-07-03', estimatedCompletion:'2026-07-04', notes:'Filter cleaned and refrigerant topped' },
  { id:'JOB-004', busNumber:'MH-01-OP-8901', type:'Tyre Replacement', priority:'LOW', status:'OPEN', mechanic:'', openedAt:'2026-07-05', estimatedCompletion:'2026-07-06', notes:'Front two tyres worn beyond limit' },
  { id:'JOB-005', busNumber:'MH-01-QR-2345', type:'Scheduled 10,000 km Service', priority:'MEDIUM', status:'IN_PROGRESS', mechanic:'Sunil More', openedAt:'2026-07-04', estimatedCompletion:'2026-07-05', notes:'Oil change, filter replacement' },
];

const PBADGE: Record<string,string> = { HIGH:'badge-danger', MEDIUM:'badge-warn', LOW:'badge-info' };
const SBADGE: Record<string,string> = { OPEN:'badge-warn', IN_PROGRESS:'badge-info', COMPLETED:'badge-success' };

export default function MaintenancePage() {
  const [filter, setFilter] = useState('ALL');
  const filtered = filter === 'ALL' ? JOBS : JOBS.filter(j => j.status === filter);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Maintenance</h1>
        <p className="page-subtitle">Active job cards and service tracking</p>
      </div>

      <div className="kpi-grid">
        {[{label:'Open Jobs',val:JOBS.filter(j=>j.status==='OPEN').length,c:'var(--depot-warn)'},
          {label:'In Progress',val:JOBS.filter(j=>j.status==='IN_PROGRESS').length,c:'var(--depot-primary)'},
          {label:'Completed Today',val:JOBS.filter(j=>j.status==='COMPLETED').length,c:'var(--depot-success)'},
          {label:'High Priority',val:JOBS.filter(j=>j.priority==='HIGH').length,c:'var(--depot-danger)'}].map(k=>(
          <div key={k.label} className="kpi-card" style={{borderTop:`3px solid ${k.c}`}}>
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value" style={{color:k.c}}>{k.val}</div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="toolbar">
          {['ALL','OPEN','IN_PROGRESS','COMPLETED'].map(s=>(
            <button key={s} className="btn btn-sm" style={{background:filter===s?'var(--depot-primary)':'#eee',color:filter===s?'#fff':'#555'}} onClick={()=>setFilter(s)}>{s.replace('_',' ')}</button>
          ))}
          <button className="btn btn-primary" style={{marginLeft:'auto'}}>+ New Job Card</button>
        </div>
        <table>
          <thead><tr><th>Job ID</th><th>Bus</th><th>Type</th><th>Priority</th><th>Status</th><th>Mechanic</th><th>Opened</th><th>ETA</th><th>Notes</th></tr></thead>
          <tbody>
            {filtered.map(j=>(
              <tr key={j.id}>
                <td style={{fontWeight:700}}>{j.id}</td>
                <td style={{fontFamily:'monospace',fontSize:'0.82rem'}}>{j.busNumber}</td>
                <td>{j.type}</td>
                <td><span className={`badge ${PBADGE[j.priority]}`}>{j.priority}</span></td>
                <td><span className={`badge ${SBADGE[j.status]}`}>{j.status.replace('_',' ')}</span></td>
                <td style={{fontSize:'0.83rem'}}>{j.mechanic || <span style={{color:'var(--depot-warn)'}}>Unassigned</span>}</td>
                <td style={{fontSize:'0.82rem'}}>{j.openedAt}</td>
                <td style={{fontSize:'0.82rem',color:new Date(j.estimatedCompletion)<new Date()?'var(--depot-danger)':'inherit'}}>{j.estimatedCompletion}</td>
                <td style={{fontSize:'0.8rem',color:'var(--depot-muted)',maxWidth:160}} title={j.notes}>{j.notes.slice(0,40)}…</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
