"use client";
import { useState } from 'react';

const TENANTS = [
  { id:'T01', name:'Maharashtra HQ', slug:'hq', plan:'ENTERPRISE', users:284, status:'ACTIVE', region:'Statewide', created:'2024-01-01', features:['ai_insights','live_tracking','advanced_reports'] },
  { id:'T02', name:'Mumbai Division', slug:'mumbai', plan:'ENTERPRISE', users:6420, status:'ACTIVE', region:'Mumbai', created:'2024-01-15', features:['live_tracking','dispatch_board'] },
  { id:'T03', name:'Pune Division', slug:'pune', plan:'PROFESSIONAL', users:3180, status:'ACTIVE', region:'Pune', created:'2024-02-01', features:['live_tracking'] },
  { id:'T04', name:'Konkan Division', slug:'konkan', plan:'PROFESSIONAL', users:1240, status:'PROVISIONING', region:'Konkan', created:'2026-07-05', features:[] },
  { id:'T05', name:'Developer Sandbox', slug:'sandbox', plan:'FREE', users:8, status:'ACTIVE', region:'N/A', created:'2025-03-10', features:[] },
];

const PLAN_BADGE: Record<string,string> = { ENTERPRISE:'badge-purple', PROFESSIONAL:'badge-primary', FREE:'badge-muted' };
const ST_BADGE: Record<string,string> = { ACTIVE:'badge-success', PROVISIONING:'badge-warn', SUSPENDED:'badge-danger' };

export default function TenantsPage() {
  const [selected, setSelected] = useState<typeof TENANTS[0]|null>(null);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Tenant Management</h1>
        <p className="page-subtitle">{TENANTS.length} tenants · Multi-tenancy isolation enabled</p>
      </div>

      <div className="admin-warn">⚠️ Each tenant is fully isolated at the database row-level. Configuration changes take effect within 60 seconds via cache invalidation.</div>

      <div className="two-col">
        <div className="card" style={{marginBottom:0}}>
          <div className="card-title">Tenants <button className="btn btn-sm btn-primary">+ Provision Tenant</button></div>
          <table>
            <thead><tr><th>Name</th><th>Slug</th><th>Plan</th><th>Users</th><th>Status</th><th>Action</th></tr></thead>
            <tbody>
              {TENANTS.map(t => (
                <tr key={t.id} style={{cursor:'pointer',background:selected?.id===t.id?'hsl(250,30%,97%)':'inherit'}} onClick={()=>setSelected(t)}>
                  <td style={{fontWeight:700}}>{t.name}</td>
                  <td className="mono" style={{fontSize:'0.78rem'}}>{t.slug}</td>
                  <td><span className={`badge ${PLAN_BADGE[t.plan]}`}>{t.plan}</span></td>
                  <td>{t.users.toLocaleString()}</td>
                  <td><span className={`badge ${ST_BADGE[t.status]}`}>{t.status}</span></td>
                  <td><button className="btn btn-sm btn-ghost">Configure</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card" style={{marginBottom:0}}>
          <div className="card-title">Tenant Details</div>
          {selected ? (
            <div style={{display:'flex',flexDirection:'column',gap:12}}>
              <div><div style={{fontSize:'0.72rem',color:'var(--adm-muted)',fontWeight:700,marginBottom:2}}>TENANT NAME</div><div style={{fontWeight:800,fontSize:'1.1rem'}}>{selected.name}</div></div>
              <div><div style={{fontSize:'0.72rem',color:'var(--adm-muted)',fontWeight:700,marginBottom:2}}>SLUG</div><div className="mono">{selected.slug}</div></div>
              <div><div style={{fontSize:'0.72rem',color:'var(--adm-muted)',fontWeight:700,marginBottom:2}}>REGION</div><div>{selected.region}</div></div>
              <div><div style={{fontSize:'0.72rem',color:'var(--adm-muted)',fontWeight:700,marginBottom:2}}>CREATED</div><div>{selected.created}</div></div>
              <div>
                <div style={{fontSize:'0.72rem',color:'var(--adm-muted)',fontWeight:700,marginBottom:6}}>ENABLED FEATURES</div>
                {selected.features.length > 0
                  ? selected.features.map(f=><span key={f} className="badge badge-success" style={{marginRight:4}}>{f.replace(/_/g,' ')}</span>)
                  : <span style={{fontSize:'0.82rem',color:'var(--adm-muted)'}}>No extra features enabled</span>
                }
              </div>
              <div style={{display:'flex',gap:8,marginTop:8}}>
                <button className="btn btn-primary btn-sm">Edit Config</button>
                <button className="btn btn-danger btn-sm">Suspend</button>
              </div>
            </div>
          ) : <div style={{color:'var(--adm-muted)',fontSize:'0.85rem',textAlign:'center',padding:'2rem 0'}}>← Select a tenant to view details</div>}
        </div>
      </div>
    </div>
  );
}
