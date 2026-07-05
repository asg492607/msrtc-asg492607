"use client";
import { useState } from 'react';

const INCIDENTS = [
  { id:'INC-1042', type:'Road Accident', bus:'MH-01-AB-4521', location:'NH-48, Khopoli', severity:'CRITICAL', status:'OPEN', time:'09:12', assignedTo:'Regional Manager, Mumbai', sla:'2h' },
  { id:'INC-1041', type:'Bus Breakdown', bus:'MH-09-CD-1234', location:'Nashik Bypass', severity:'HIGH', status:'IN_PROGRESS', time:'08:44', assignedTo:'Nashik Depot', sla:'4h' },
  { id:'INC-1040', type:'Passenger Complaint', bus:'MH-01-EF-9012', location:'Dadar ST Stand', severity:'MEDIUM', status:'IN_PROGRESS', time:'08:20', assignedTo:'Customer Care', sla:'24h' },
  { id:'INC-1039', type:'Fuel Theft', bus:'MH-14-GH-3456', location:'Aurangabad Depot', severity:'HIGH', status:'OPEN', time:'07:55', assignedTo:'Vigilance Team', sla:'8h' },
  { id:'INC-1038', type:'Fire Alarm Trigger', bus:'MH-06-IJ-7890', location:'Kolhapur ST', severity:'CRITICAL', status:'RESOLVED', time:'06:30', assignedTo:'Fire Dept / Depot', sla:'1h' },
];

const SBADGE: Record<string,string> = { CRITICAL:'badge-red', HIGH:'badge-yellow', MEDIUM:'badge-blue', LOW:'badge-muted' };
const STBADGE: Record<string,string> = { OPEN:'badge-red', IN_PROGRESS:'badge-yellow', RESOLVED:'badge-green', CLOSED:'badge-muted' };

export default function IncidentsPage() {
  const [filter, setFilter] = useState('ALL');
  const filtered = filter === 'ALL' ? INCIDENTS : INCIDENTS.filter(i => i.status === filter);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Incident Management</h1>
          <p className="page-subtitle">{INCIDENTS.filter(i=>i.status==='OPEN').length} open · {INCIDENTS.filter(i=>i.severity==='CRITICAL').length} critical</p>
        </div>
        <button className="btn btn-danger">🚨 Raise Incident</button>
      </div>

      {INCIDENTS.filter(i=>i.severity==='CRITICAL'&&i.status!=='RESOLVED').length > 0 && (
        <div style={{background:'hsl(4,80%,12%)',border:'1px solid hsl(4,80%,30%)',borderRadius:8,padding:'0.85rem 1rem',marginBottom:'1.25rem',display:'flex',gap:12,alignItems:'center'}}>
          <span style={{fontSize:20}}>⛔</span>
          <span style={{color:'var(--hq-danger)',fontWeight:700}}>
            {INCIDENTS.filter(i=>i.severity==='CRITICAL'&&i.status!=='RESOLVED').length} CRITICAL incident(s) require immediate attention.
          </span>
        </div>
      )}

      <div className="card">
        <div className="toolbar">
          {['ALL','OPEN','IN_PROGRESS','RESOLVED'].map(s=>(
            <button key={s} className="btn btn-sm" style={{background:filter===s?'var(--hq-danger)':'var(--hq-surface2)',color:filter===s?'#fff':'var(--hq-text)',border:'1px solid var(--hq-border)'}} onClick={()=>setFilter(s)}>{s.replace('_',' ')}</button>
          ))}
        </div>
        <table>
          <thead><tr><th>ID</th><th>Type</th><th>Bus</th><th>Location</th><th>Severity</th><th>Status</th><th>Reported</th><th>Assigned To</th><th>SLA</th><th>Action</th></tr></thead>
          <tbody>
            {filtered.map(i=>(
              <tr key={i.id}>
                <td style={{fontWeight:700,fontFamily:'monospace',fontSize:'0.8rem'}}>{i.id}</td>
                <td style={{fontWeight:600,fontSize:'0.83rem'}}>{i.type}</td>
                <td style={{fontFamily:'monospace',fontSize:'0.78rem'}}>{i.bus}</td>
                <td style={{fontSize:'0.82rem',color:'var(--hq-muted)'}}>{i.location}</td>
                <td><span className={`badge ${SBADGE[i.severity]}`}>{i.severity}</span></td>
                <td><span className={`badge ${STBADGE[i.status]}`}>{i.status.replace('_',' ')}</span></td>
                <td style={{fontSize:'0.8rem',color:'var(--hq-muted)'}}>{i.time}</td>
                <td style={{fontSize:'0.8rem'}}>{i.assignedTo}</td>
                <td style={{fontSize:'0.8rem',color:'var(--hq-warn)'}}>SLA: {i.sla}</td>
                <td><button className="btn btn-sm btn-primary">View</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
