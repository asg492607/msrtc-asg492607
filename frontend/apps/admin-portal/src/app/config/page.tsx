"use client";
import { useState } from 'react';

const CONFIGS = [
  { key:'BOOKING_LOCK_TIMEOUT_MINUTES', value:'10', env:'production', description:'Minutes a seat lock is held before expiry', type:'INTEGER' },
  { key:'OTP_EXPIRY_SECONDS', value:'300', env:'production', description:'OTP validity period in seconds', type:'INTEGER' },
  { key:'MAX_SEATS_PER_BOOKING', value:'6', env:'production', description:'Maximum seats a single user can book per trip', type:'INTEGER' },
  { key:'PAYMENT_TIMEOUT_SECONDS', value:'900', env:'production', description:'Payment gateway session timeout', type:'INTEGER' },
  { key:'GPS_UPDATE_INTERVAL_SECONDS', value:'15', env:'production', description:'Interval between GPS location pushes from conductor app', type:'INTEGER' },
  { key:'PARCEL_MAX_WEIGHT_KG', value:'50', env:'production', description:'Maximum parcel weight allowed per booking', type:'INTEGER' },
  { key:'SUPPORT_EMAIL', value:'support@msrtc.gov.in', env:'production', description:'Passenger-facing support email address', type:'STRING' },
  { key:'CANCELLATION_WINDOW_HOURS', value:'4', env:'production', description:'Hours before departure within which cancellation is allowed', type:'INTEGER' },
];

export default function ConfigPage() {
  const [configs, setConfigs] = useState(CONFIGS);
  const [editing, setEditing] = useState<string|null>(null);
  const [editVal, setEditVal] = useState('');

  const startEdit = (key: string, val: string) => { setEditing(key); setEditVal(val); };
  const save = (key: string) => {
    setConfigs(prev => prev.map(c => c.key===key ? {...c, value:editVal} : c));
    setEditing(null);
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Configuration Management</h1>
        <p className="page-subtitle">Runtime platform settings · All changes are audit-logged</p>
      </div>

      <div className="admin-warn">⚠️ Changes to production configuration values take effect within 30 seconds across all services. No restart required.</div>

      <div className="card">
        <table>
          <thead><tr><th>Config Key</th><th>Value</th><th>Type</th><th>Environment</th><th>Description</th><th>Action</th></tr></thead>
          <tbody>
            {configs.map(c => (
              <tr key={c.key}>
                <td className="mono" style={{fontWeight:700,fontSize:'0.78rem'}}>{c.key}</td>
                <td>
                  {editing===c.key
                    ? <div style={{display:'flex',gap:6}}>
                        <input value={editVal} onChange={e=>setEditVal(e.target.value)} style={{padding:'4px 8px',border:'1px solid var(--adm-primary)',borderRadius:4,fontSize:'0.85rem',width:120}} autoFocus />
                        <button className="btn btn-sm btn-primary" onClick={()=>save(c.key)}>Save</button>
                        <button className="btn btn-sm btn-ghost" onClick={()=>setEditing(null)}>✕</button>
                      </div>
                    : <code style={{background:'var(--adm-surface2)',padding:'3px 8px',borderRadius:4,fontSize:'0.82rem',fontFamily:'monospace',fontWeight:700}}>{c.value}</code>
                  }
                </td>
                <td><span className="badge badge-muted">{c.type}</span></td>
                <td><span className="badge badge-success">{c.env}</span></td>
                <td style={{fontSize:'0.8rem',color:'var(--adm-muted)',maxWidth:250}}>{c.description}</td>
                <td><button className="btn btn-sm btn-ghost" onClick={()=>startEdit(c.key, c.value)}>Edit</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
