"use client";
import { useState } from 'react';

const AUDIT_LOGS = [
  { id:'AUD-5021', actor:'admin@msrtc.gov', action:'ROLE_ASSIGNED', resource:'User:U004', detail:'Role CONDUCTOR added to Rajesh Kumar', ip:'10.0.0.1', time:'2026-07-05 09:42:11', severity:'INFO' },
  { id:'AUD-5020', actor:'sunetra@msrtc.gov', action:'FEATURE_FLAG_TOGGLED', resource:'Flag:GPS_V2', detail:'GPS_TRACKING_V2 enabled in production (rollout: 75%)', ip:'10.0.0.8', time:'2026-07-05 09:31:00', severity:'WARN' },
  { id:'AUD-5019', actor:'sys-provisioner', action:'TENANT_CREATED', resource:'Tenant:konkan', detail:'New tenant Konkan Division provisioned (plan: PROFESSIONAL)', ip:'10.0.1.10', time:'2026-07-05 09:12:44', severity:'INFO' },
  { id:'AUD-5018', actor:'security-bot', action:'LOGIN_FAILED_BLOCKED', resource:'Auth', detail:'IP 203.0.113.42 blocked after 5 failed attempts', ip:'203.0.113.42', time:'2026-07-05 07:15:32', severity:'CRITICAL' },
  { id:'AUD-5017', actor:'admin@msrtc.gov', action:'RATE_LIMIT_UPDATED', resource:'Service:booking-service', detail:'Rate limit changed 500→1000 rpm', ip:'10.0.0.1', time:'2026-07-04 18:22:00', severity:'WARN' },
  { id:'AUD-5016', actor:'admin@msrtc.gov', action:'USER_SUSPENDED', resource:'User:test@example.com', detail:'User suspended for policy violation', ip:'10.0.0.1', time:'2026-07-04 16:10:05', severity:'WARN' },
];

const SEV_BADGE: Record<string,string> = { INFO:'badge-muted', WARN:'badge-warn', CRITICAL:'badge-danger' };

export default function AuditPage() {
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('ALL');
  const filtered = AUDIT_LOGS.filter(l =>
    (filter==='ALL' || l.severity===filter) &&
    (l.actor.includes(search) || l.action.includes(search) || l.detail.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Audit Trail</h1>
        <p className="page-subtitle">Immutable log of all administrative actions · Retained 7 years</p>
      </div>

      <div className="card">
        <div className="toolbar">
          <input className="search-input" placeholder="Search actor, action or detail..." value={search} onChange={e=>setSearch(e.target.value)} />
          <select className="filter" value={filter} onChange={e=>setFilter(e.target.value)}>
            <option value="ALL">All Severity</option>
            <option value="CRITICAL">Critical</option>
            <option value="WARN">Warning</option>
            <option value="INFO">Info</option>
          </select>
          <button className="btn btn-ghost" style={{marginLeft:'auto'}}>⬇ Export CSV</button>
        </div>
        <table>
          <thead><tr><th>Log ID</th><th>Actor</th><th>Action</th><th>Resource</th><th>Detail</th><th>Source IP</th><th>Timestamp</th><th>Severity</th></tr></thead>
          <tbody>
            {filtered.map(l => (
              <tr key={l.id}>
                <td className="mono" style={{fontSize:'0.75rem',fontWeight:700}}>{l.id}</td>
                <td className="mono" style={{fontSize:'0.78rem'}}>{l.actor}</td>
                <td className="mono" style={{fontSize:'0.75rem',fontWeight:700,color:'var(--adm-primary)'}}>{l.action}</td>
                <td className="mono" style={{fontSize:'0.75rem'}}>{l.resource}</td>
                <td style={{fontSize:'0.8rem',color:'var(--adm-muted)',maxWidth:200}}>{l.detail}</td>
                <td className="mono" style={{fontSize:'0.75rem'}}>{l.ip}</td>
                <td className="mono" style={{fontSize:'0.75rem',color:'var(--adm-muted)'}}>{l.time}</td>
                <td><span className={`badge ${SEV_BADGE[l.severity]}`}>{l.severity}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
