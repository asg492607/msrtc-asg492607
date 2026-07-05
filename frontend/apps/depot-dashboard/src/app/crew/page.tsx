"use client";
import { useState } from 'react';

const CREW = [
  { id:'C01', name:'Rajesh Kumar', role:'DRIVER', employeeId:'EMP-1001', phone:'9876500001', shift:'Morning', status:'ON_DUTY', assignedBus:'MH-01-AB-1234', assignedRoute:'Mumbai-Pune' },
  { id:'C02', name:'Anil Patil', role:'CONDUCTOR', employeeId:'EMP-2001', phone:'9876500002', shift:'Morning', status:'ON_DUTY', assignedBus:'MH-01-AB-1234', assignedRoute:'Mumbai-Pune' },
  { id:'C03', name:'Suresh More', role:'DRIVER', employeeId:'EMP-1002', phone:'9876500003', shift:'Morning', status:'ON_DUTY', assignedBus:'MH-01-CD-5678', assignedRoute:'Mumbai-Nashik' },
  { id:'C04', name:'Priya Nair', role:'CONDUCTOR', employeeId:'EMP-2002', phone:'9876500004', shift:'Afternoon', status:'AVAILABLE', assignedBus:'', assignedRoute:'' },
  { id:'C05', name:'Vijay Shinde', role:'DRIVER', employeeId:'EMP-1003', phone:'9876500005', shift:'Night', status:'OFF_DUTY', assignedBus:'', assignedRoute:'' },
  { id:'C06', name:'Kavita Mali', role:'CONDUCTOR', employeeId:'EMP-2003', phone:'9876500006', shift:'Morning', status:'LEAVE', assignedBus:'', assignedRoute:'' },
];

const SBADGE: Record<string,string> = { ON_DUTY:'badge-success', AVAILABLE:'badge-info', OFF_DUTY:'badge-neutral', LEAVE:'badge-warn' };

export default function CrewPage() {
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('ALL');
  const filtered = CREW.filter(c =>
    (filter === 'ALL' || c.status === filter) &&
    (c.name.toLowerCase().includes(search.toLowerCase()) || c.employeeId.includes(search))
  );
  const available = CREW.filter(c => c.status === 'AVAILABLE').length;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Crew Roster</h1>
        <p className="page-subtitle">{CREW.length} staff registered · {available} available for assignment</p>
      </div>

      <div className="kpi-grid">
        {[{label:'On Duty',val:CREW.filter(c=>c.status==='ON_DUTY').length,c:'var(--depot-success)'},
          {label:'Available',val:CREW.filter(c=>c.status==='AVAILABLE').length,c:'var(--depot-primary)'},
          {label:'Off Duty',val:CREW.filter(c=>c.status==='OFF_DUTY').length,c:'var(--depot-muted)'},
          {label:'On Leave',val:CREW.filter(c=>c.status==='LEAVE').length,c:'var(--depot-warn)'}].map(k=>(
          <div key={k.label} className="kpi-card" style={{borderTop:`3px solid ${k.c}`}}>
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value" style={{color:k.c}}>{k.val}</div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="toolbar">
          <input className="search-input" placeholder="Search name or employee ID..." value={search} onChange={e=>setSearch(e.target.value)} />
          <select className="filter" value={filter} onChange={e=>setFilter(e.target.value)}>
            <option value="ALL">All Status</option>
            <option value="ON_DUTY">On Duty</option>
            <option value="AVAILABLE">Available</option>
            <option value="OFF_DUTY">Off Duty</option>
            <option value="LEAVE">On Leave</option>
          </select>
          <button className="btn btn-primary">+ Add Staff</button>
        </div>
        <table>
          <thead><tr><th>Name</th><th>Employee ID</th><th>Role</th><th>Shift</th><th>Status</th><th>Assigned Bus</th><th>Route</th><th>Action</th></tr></thead>
          <tbody>
            {filtered.map(c => (
              <tr key={c.id}>
                <td style={{fontWeight:700}}>{c.name}</td>
                <td style={{fontFamily:'monospace',fontSize:'0.82rem'}}>{c.employeeId}</td>
                <td><span className={`badge ${c.role==='DRIVER'?'badge-info':'badge-neutral'}`}>{c.role}</span></td>
                <td>{c.shift}</td>
                <td><span className={`badge ${SBADGE[c.status]}`}>{c.status.replace('_',' ')}</span></td>
                <td style={{fontFamily:'monospace',fontSize:'0.82rem'}}>{c.assignedBus || '—'}</td>
                <td style={{fontSize:'0.82rem'}}>{c.assignedRoute || '—'}</td>
                <td><button className="btn btn-sm btn-primary" disabled={c.status!=='AVAILABLE'} style={{opacity:c.status!=='AVAILABLE'?0.4:1}}>Assign</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
