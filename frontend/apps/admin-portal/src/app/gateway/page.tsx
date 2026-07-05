"use client";
import { useState } from 'react';

const SERVICES = [
  { name:'auth-service', url:'http://auth-svc:8080', version:'v1.4.2', status:'HEALTHY', rateLimit:'500/min', latency:'12ms', requests:'84.2K/day' },
  { name:'booking-service', url:'http://booking-svc:8081', version:'v1.3.0', status:'HEALTHY', rateLimit:'1000/min', latency:'34ms', requests:'42.1K/day' },
  { name:'seat-service', url:'http://seat-svc:8082', version:'v1.2.1', status:'DEGRADED', rateLimit:'2000/min', latency:'180ms', requests:'38.4K/day' },
  { name:'payment-service', url:'http://payment-svc:8083', version:'v1.1.5', status:'HEALTHY', rateLimit:'200/min', latency:'28ms', requests:'12.8K/day' },
  { name:'ticket-service', url:'http://ticket-svc:8084', version:'v1.0.8', status:'HEALTHY', rateLimit:'500/min', latency:'19ms', requests:'11.2K/day' },
  { name:'notification-service', url:'http://notif-svc:8085', version:'v1.2.0', status:'HEALTHY', rateLimit:'5000/min', latency:'8ms', requests:'128.4K/day' },
];

const ST_BADGE: Record<string,string> = { HEALTHY:'badge-success', DEGRADED:'badge-warn', DOWN:'badge-danger' };

export default function GatewayPage() {
  const [search, setSearch] = useState('');
  const filtered = SERVICES.filter(s => s.name.includes(search));

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">API Gateway & Service Registry</h1>
        <p className="page-subtitle">Kong Gateway · {SERVICES.length} registered services</p>
      </div>

      <div className="kpi-grid">
        {[{l:'Total Requests Today',v:'317K'},{l:'Avg Latency',v:'47ms'},{l:'Error Rate',v:'0.08%'},{l:'Services Healthy',v:`${SERVICES.filter(s=>s.status==='HEALTHY').length}/${SERVICES.length}`}].map(k=>(
          <div key={k.l} className="kpi-card"><div className="kpi-label">{k.l}</div><div className="kpi-value">{k.v}</div></div>
        ))}
      </div>

      <div className="card">
        <div className="toolbar">
          <input className="search-input" placeholder="Search service name..." value={search} onChange={e=>setSearch(e.target.value)} />
          <button className="btn btn-primary" style={{marginLeft:'auto'}}>+ Register Service</button>
        </div>
        <table>
          <thead><tr><th>Service</th><th>Internal URL</th><th>Version</th><th>Status</th><th>Rate Limit</th><th>P50 Latency</th><th>Requests/Day</th><th>Actions</th></tr></thead>
          <tbody>
            {filtered.map(s => (
              <tr key={s.name}>
                <td style={{fontWeight:700}} className="mono">{s.name}</td>
                <td className="mono" style={{fontSize:'0.75rem',color:'var(--adm-muted)'}}>{s.url}</td>
                <td><span className="badge badge-muted">{s.version}</span></td>
                <td><span className={`badge ${ST_BADGE[s.status]}`}>{s.status}</span></td>
                <td className="mono" style={{fontSize:'0.82rem'}}>{s.rateLimit}</td>
                <td style={{color:parseInt(s.latency)>100?'var(--adm-danger)':'inherit',fontWeight:parseInt(s.latency)>100?700:400}} className="mono">{s.latency}</td>
                <td style={{fontSize:'0.82rem'}}>{s.requests}</td>
                <td style={{display:'flex',gap:4}}>
                  <button className="btn btn-sm btn-ghost">Config</button>
                  <button className="btn btn-sm btn-ghost">Logs</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
