"use client";
import { useState } from 'react';

export default function PlatformPage() {
  const [maintenanceMode, setMaintenanceMode] = useState(false);
  const [cacheClearing, setCacheClearing] = useState(false);

  const clearCache = async () => {
    setCacheClearing(true);
    await new Promise(r => setTimeout(r, 1500));
    setCacheClearing(false);
    alert('Redis cache cleared successfully (12,481 keys evicted)');
  };

  const kafkaTopics = [
    { topic:'booking.events', partitions:12, msgs:'84.2K/hr', lag:0, status:'HEALTHY' },
    { topic:'payment.events', partitions:6, msgs:'12.1K/hr', lag:0, status:'HEALTHY' },
    { topic:'seat.locks', partitions:24, msgs:'142K/hr', lag:241, status:'LAG_DETECTED' },
    { topic:'gps.updates', partitions:48, msgs:'1.2M/hr', lag:0, status:'HEALTHY' },
    { topic:'notifications.email', partitions:4, msgs:'8.4K/hr', lag:0, status:'HEALTHY' },
  ];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Platform Operations</h1>
        <p className="page-subtitle">System controls, Kafka monitoring, cache management</p>
      </div>

      <div className="two-col">
        <div className="card">
          <div className="card-title">System Controls</div>
          <div style={{display:'flex',flexDirection:'column',gap:16}}>

            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'12px 0',borderBottom:'1px solid var(--adm-border)'}}>
              <div>
                <div style={{fontWeight:700}}>Maintenance Mode</div>
                <div style={{fontSize:'0.78rem',color:'var(--adm-muted)'}}>Shows maintenance page to all passengers</div>
              </div>
              <label className="toggle">
                <input type="checkbox" checked={maintenanceMode} onChange={e=>setMaintenanceMode(e.target.checked)} />
                <span className="toggle-slider"></span>
              </label>
            </div>

            {maintenanceMode && (
              <div style={{background:'hsl(4,78%,94%)',border:'1px solid hsl(4,78%,80%)',borderRadius:8,padding:'10px 12px',fontSize:'0.82rem',color:'var(--adm-danger)',fontWeight:600}}>
                ⛔ MAINTENANCE MODE ACTIVE — Passengers are seeing the maintenance page
              </div>
            )}

            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'12px 0',borderBottom:'1px solid var(--adm-border)'}}>
              <div>
                <div style={{fontWeight:700}}>Clear Redis Cache</div>
                <div style={{fontSize:'0.78rem',color:'var(--adm-muted)'}}>Evicts all cached data (seat availability, sessions)</div>
              </div>
              <button className="btn btn-sm btn-danger" onClick={clearCache} disabled={cacheClearing}>
                {cacheClearing ? '⟳ Clearing…' : '🗑 Clear Cache'}
              </button>
            </div>

            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'12px 0'}}>
              <div>
                <div style={{fontWeight:700}}>Force Deploy Restart</div>
                <div style={{fontSize:'0.78rem',color:'var(--adm-muted)'}}>Rolling restart of all Kubernetes pods</div>
              </div>
              <button className="btn btn-sm btn-danger">↺ Rolling Restart</button>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">Kafka Topics</div>
          <table>
            <thead><tr><th>Topic</th><th>Msgs/hr</th><th>Consumer Lag</th><th>Status</th></tr></thead>
            <tbody>
              {kafkaTopics.map(t=>(
                <tr key={t.topic}>
                  <td className="mono" style={{fontSize:'0.78rem',fontWeight:600}}>{t.topic}</td>
                  <td style={{fontSize:'0.82rem'}}>{t.msgs}</td>
                  <td style={{fontWeight:t.lag>0?700:400,color:t.lag>0?'var(--adm-danger)':'var(--adm-success)'}}>{t.lag > 0 ? `⚠ ${t.lag}` : '0'}</td>
                  <td><span className={`badge ${t.status==='HEALTHY'?'badge-success':'badge-danger'}`}>{t.status.replace('_',' ')}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
