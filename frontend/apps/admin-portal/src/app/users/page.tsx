"use client";
import { useState } from 'react';

const ROLES = ['SUPER_ADMIN','HQ_MANAGER','REGIONAL_MANAGER','DEPOT_MANAGER','CONDUCTOR','DRIVER','PASSENGER','API_CLIENT'];
const USERS = [
  { id:'U001', name:'Sunetra Pawar', email:'sunetra@msrtc.gov', roles:['HQ_MANAGER'], tenant:'HQ', status:'ACTIVE', mfa:true, lastLogin:'5 min ago' },
  { id:'U002', name:'Ramesh Pawar', email:'ramesh.d@msrtc.gov', roles:['DEPOT_MANAGER'], tenant:'Mumbai Central', status:'ACTIVE', mfa:true, lastLogin:'1h ago' },
  { id:'U003', name:'API Gateway Bot', email:'apigw@sys.msrtc.gov', roles:['API_CLIENT'], tenant:'System', status:'ACTIVE', mfa:false, lastLogin:'Just now' },
  { id:'U004', name:'Rajesh Kumar', email:'rajesh.k@msrtc.gov', roles:['DRIVER','CONDUCTOR'], tenant:'Mumbai', status:'ACTIVE', mfa:false, lastLogin:'2h ago' },
  { id:'U005', name:'Test Account', email:'test@example.com', roles:['PASSENGER'], tenant:'Public', status:'SUSPENDED', mfa:false, lastLogin:'3 days ago' },
];

export default function UsersPage() {
  const [search, setSearch] = useState('');
  const [filterRole, setFilterRole] = useState('ALL');
  const filtered = USERS.filter(u =>
    (filterRole === 'ALL' || u.roles.includes(filterRole)) &&
    (u.name.toLowerCase().includes(search.toLowerCase()) || u.email.includes(search))
  );

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Users & RBAC</h1>
        <p className="page-subtitle">{USERS.length} users · {ROLES.length} roles defined</p>
      </div>

      <div className="two-col" style={{marginBottom:'1.25rem'}}>
        <div className="card" style={{marginBottom:0}}>
          <div className="card-title">Roles Summary</div>
          <div style={{display:'flex',flexWrap:'wrap',gap:8}}>
            {ROLES.map(r => (
              <div key={r} style={{background:'var(--adm-surface2)',border:'1px solid var(--adm-border)',borderRadius:8,padding:'8px 12px',textAlign:'center',minWidth:120}}>
                <div style={{fontSize:'1.2rem',fontWeight:800,color:'var(--adm-primary)'}}>{USERS.filter(u=>u.roles.includes(r)).length}</div>
                <div style={{fontSize:'0.72rem',color:'var(--adm-muted)',marginTop:2}}>{r.replace(/_/g,' ')}</div>
              </div>
            ))}
          </div>
        </div>
        <div className="card" style={{marginBottom:0}}>
          <div className="card-title">MFA Compliance</div>
          <div style={{display:'flex',alignItems:'center',gap:16}}>
            <div>
              <div style={{fontSize:'2.5rem',fontWeight:900,color:'var(--adm-primary)'}}>{Math.round(USERS.filter(u=>u.mfa).length/USERS.length*100)}%</div>
              <div style={{fontSize:'0.82rem',color:'var(--adm-muted)'}}>Users with MFA enabled</div>
            </div>
            <div style={{flex:1}}>
              <div style={{height:10,background:'var(--adm-surface2)',borderRadius:5,overflow:'hidden'}}>
                <div style={{height:'100%',width:`${Math.round(USERS.filter(u=>u.mfa).length/USERS.length*100)}%`,background:'var(--adm-primary)',borderRadius:5}} />
              </div>
              <div style={{fontSize:'0.75rem',color:'var(--adm-muted)',marginTop:4}}>{USERS.filter(u=>u.mfa).length}/{USERS.length} users</div>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="toolbar">
          <input className="search-input" placeholder="Search name or email..." value={search} onChange={e=>setSearch(e.target.value)} />
          <select className="filter" value={filterRole} onChange={e=>setFilterRole(e.target.value)}>
            <option value="ALL">All Roles</option>
            {ROLES.map(r=><option key={r} value={r}>{r.replace(/_/g,' ')}</option>)}
          </select>
          <button className="btn btn-primary" style={{marginLeft:'auto'}}>+ Invite User</button>
        </div>
        <table>
          <thead><tr><th>Name</th><th>Email</th><th>Roles</th><th>Tenant</th><th>MFA</th><th>Status</th><th>Last Login</th><th>Actions</th></tr></thead>
          <tbody>
            {filtered.map(u => (
              <tr key={u.id}>
                <td style={{fontWeight:700}}>{u.name}</td>
                <td className="mono" style={{fontSize:'0.78rem'}}>{u.email}</td>
                <td>{u.roles.map(r=><span key={r} className="badge badge-primary" style={{marginRight:3}}>{r.replace(/_/g,' ')}</span>)}</td>
                <td style={{fontSize:'0.82rem'}}>{u.tenant}</td>
                <td>{u.mfa ? <span className="badge badge-success">✓ Enabled</span> : <span className="badge badge-warn">✗ Off</span>}</td>
                <td><span className={`badge ${u.status==='ACTIVE'?'badge-success':'badge-danger'}`}>{u.status}</span></td>
                <td style={{fontSize:'0.78rem',color:'var(--adm-muted)'}}>{u.lastLogin}</td>
                <td style={{display:'flex',gap:4}}>
                  <button className="btn btn-sm btn-ghost">Edit</button>
                  <button className="btn btn-sm btn-danger" style={{opacity:u.status==='SUSPENDED'?0.4:1}}>Suspend</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
