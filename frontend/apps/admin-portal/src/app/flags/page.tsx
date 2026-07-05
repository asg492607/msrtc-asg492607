"use client";
import { useState } from 'react';

const INITIAL_FLAGS = [
  { key:'GPS_TRACKING_V2', desc:'Next-gen GPS with 15s intervals and geofencing', env:'production', enabled:true, rollout:100, tenants:'ALL' },
  { key:'AI_DEMAND_FORECAST', desc:'ML-based demand forecasting for route planning', env:'production', enabled:true, rollout:100, tenants:'HQ only' },
  { key:'DYNAMIC_PRICING', desc:'Real-time fare adjustment based on demand and capacity', env:'staging', enabled:false, rollout:0, tenants:'NONE' },
  { key:'QR_V2_VALIDATOR', desc:'Upgraded QR scanner with offline JWT verification', env:'production', enabled:true, rollout:75, tenants:'Mumbai,Pune' },
  { key:'PARCEL_BOOKING_BETA', desc:'New parcel booking flow with tracking', env:'production', enabled:true, rollout:20, tenants:'Mumbai' },
  { key:'LIVE_CHAT_SUPPORT', desc:'In-app live chat with customer support agents', env:'staging', enabled:false, rollout:0, tenants:'NONE' },
  { key:'PASS_SUBSCRIPTION', desc:'Monthly/annual pass subscription self-service', env:'production', enabled:true, rollout:100, tenants:'ALL' },
  { key:'DARK_MODE_UI', desc:'Dark mode for HQ Command Center and Admin Portal', env:'production', enabled:false, rollout:0, tenants:'HQ only' },
];

export default function FlagsPage() {
  const [flags, setFlags] = useState(INITIAL_FLAGS);
  const toggle = (key: string) => setFlags(prev => prev.map(f => f.key===key ? {...f, enabled:!f.enabled} : f));

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Feature Flags</h1>
        <p className="page-subtitle">{flags.filter(f=>f.enabled).length}/{flags.length} flags enabled · Changes propagate in &lt;60s</p>
      </div>

      <div className="admin-warn">⚠️ Production flag changes take effect immediately. Test in staging first. All changes are audit-logged.</div>

      <div className="card">
        <table>
          <thead><tr><th>Flag Key</th><th>Description</th><th>Environment</th><th>Rollout %</th><th>Tenants</th><th>Enabled</th><th>Actions</th></tr></thead>
          <tbody>
            {flags.map(f => (
              <tr key={f.key}>
                <td className="mono" style={{fontWeight:700,fontSize:'0.8rem'}}>{f.key}</td>
                <td style={{fontSize:'0.82rem',color:'var(--adm-muted)',maxWidth:240}}>{f.desc}</td>
                <td><span className={`badge ${f.env==='production'?'badge-success':'badge-warn'}`}>{f.env}</span></td>
                <td>
                  <div style={{display:'flex',alignItems:'center',gap:6}}>
                    <div style={{width:50,height:5,background:'var(--adm-surface2)',borderRadius:3,overflow:'hidden'}}>
                      <div style={{height:'100%',width:`${f.rollout}%`,background:'var(--adm-primary)',borderRadius:3}} />
                    </div>
                    <span style={{fontSize:'0.78rem'}}>{f.rollout}%</span>
                  </div>
                </td>
                <td style={{fontSize:'0.8rem',color:'var(--adm-muted)'}}>{f.tenants}</td>
                <td>
                  <label className="toggle">
                    <input type="checkbox" checked={f.enabled} onChange={()=>toggle(f.key)} />
                    <span className="toggle-slider"></span>
                  </label>
                </td>
                <td style={{display:'flex',gap:4}}>
                  <button className="btn btn-sm btn-ghost">Edit</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
