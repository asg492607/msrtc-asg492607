import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\admin-portal"

dirs = [
    "src/app/dashboard", "src/app/users", "src/app/tenants",
    "src/app/flags", "src/app/gateway", "src/app/audit",
    "src/app/platform", "src/app/config", "src/app/monitoring",
    "src/app/login", "src/components/ui", "src/styles",
    "src/types", "src/lib/api", "src/store", "public"
]
for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# ============================================================
# TASK 81 — Scaffold, package.json, Admin Purple Design System
# ============================================================
pkg = {
  "name": "admin-portal",
  "version": "1.0.0",
  "private": True,
  "scripts": { "dev": "next dev --port 3003", "build": "next build", "start": "next start" },
  "dependencies": {
    "next": "14.2.3", "react": "^18", "react-dom": "^18",
    "@tanstack/react-query": "^5.0.0", "zustand": "^4.5.0"
  },
  "devDependencies": {
    "typescript": "^5", "@types/node": "^20",
    "@types/react": "^18", "@types/react-dom": "^18"
  }
}
with open(os.path.join(base_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg, f, indent=2)

tsconfig = {
  "compilerOptions": {
    "lib": ["dom","dom.iterable","esnext"], "allowJs": True,
    "skipLibCheck": True, "strict": True, "noEmit": True,
    "esModuleInterop": True, "module": "esnext",
    "moduleResolution": "bundler", "resolveJsonModule": True,
    "isolatedModules": True, "jsx": "preserve", "incremental": True,
    "plugins": [{"name": "next"}], "paths": {"@/*": ["./src/*"]}
  },
  "include": ["next-env.d.ts","**/*.ts","**/*.tsx",".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
with open(os.path.join(base_dir, "tsconfig.json"), "w", encoding="utf-8") as f:
    json.dump(tsconfig, f, indent=2)

with open(os.path.join(base_dir, "next.config.mjs"), "w", encoding="utf-8") as f:
    f.write("/** @type {import('next').NextConfig} */\nconst nextConfig = {};\nexport default nextConfig;\n")

# Admin theme: clean white + deep indigo/purple — enterprise premium feel
css = """:root {
  --adm-primary:  hsl(250, 84%, 54%);
  --adm-primary2: hsl(250, 84%, 44%);
  --adm-accent:   hsl(280, 70%, 58%);
  --adm-bg:       hsl(250, 20%, 97%);
  --adm-surface:  hsl(0, 0%, 100%);
  --adm-surface2: hsl(250, 25%, 96%);
  --adm-sidebar:  hsl(250, 40%, 10%);
  --adm-border:   hsl(250, 15%, 88%);
  --adm-text:     hsl(250, 20%, 15%);
  --adm-muted:    hsl(250, 12%, 50%);
  --adm-success:  hsl(142, 60%, 42%);
  --adm-warn:     hsl(38, 90%, 50%);
  --adm-danger:   hsl(4, 78%, 54%);
  --adm-info:     hsl(200, 80%, 50%);
  --radius: 10px;
  --shadow: 0 1px 8px rgba(80,40,180,0.07), 0 2px 16px rgba(80,40,180,0.04);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--adm-bg);
  color: var(--adm-text);
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 240px; background: var(--adm-sidebar);
  border-right: 1px solid rgba(255,255,255,0.06);
  min-height: 100vh; display: flex; flex-direction: column;
  position: fixed; top: 0; left: 0; bottom: 0; z-index: 100;
}
.sidebar-logo {
  padding: 1.5rem 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  display: flex; align-items: center; gap: 10px;
}
.logo-icon {
  width: 34px; height: 34px; background: var(--adm-primary);
  border-radius: 8px; display: flex; align-items: center;
  justify-content: center; font-size: 16px;
}
.logo-text .brand { font-size: 1rem; font-weight: 900; color: #fff; }
.logo-text .sub { font-size: 0.7rem; color: rgba(255,255,255,0.45); margin-top: 1px; }

.sidebar-section { padding: 0.6rem 1rem 0.2rem; font-size: 0.65rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.28); }

.sidebar-nav { flex: 1; padding: 0.5rem 0; overflow-y: auto; }
.nav-item {
  display: flex; align-items: center; gap: 0.7rem;
  padding: 0.6rem 1.25rem; color: rgba(255,255,255,0.6);
  text-decoration: none; font-size: 0.85rem; font-weight: 500;
  transition: all 0.15s; border-left: 3px solid transparent; margin: 1px 0;
}
.nav-item:hover { background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.9); }
.nav-item.active { background: rgba(139,92,246,0.2); color: #fff; border-left-color: var(--adm-primary); }
.nav-icon { font-size: 0.95rem; width: 18px; text-align: center; }

.sidebar-footer {
  padding: 1rem 1.25rem; border-top: 1px solid rgba(255,255,255,0.06);
  display: flex; align-items: center; gap: 10px;
}
.avatar { width: 32px; height: 32px; background: var(--adm-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 800; color: #fff; }
.footer-name { font-size: 0.82rem; font-weight: 700; color: #fff; }
.footer-role { font-size: 0.68rem; color: rgba(255,255,255,0.4); }

/* Topbar */
.topbar {
  height: 56px; background: var(--adm-surface);
  border-bottom: 1px solid var(--adm-border);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 1.75rem; margin-bottom: 1.75rem;
  position: sticky; top: 0; z-index: 50;
}
.topbar-title { font-size: 1rem; font-weight: 700; color: var(--adm-text); }
.topbar-actions { display: flex; gap: 0.75rem; align-items: center; }

/* Main */
.main-content { margin-left: 240px; flex: 1; }
.page-body { padding: 0 1.75rem 2rem; }
.page-header { margin-bottom: 1.5rem; }
.page-title { font-size: 1.35rem; font-weight: 800; color: var(--adm-text); }
.page-subtitle { color: var(--adm-muted); font-size: 0.82rem; margin-top: 3px; }

/* Warning banner */
.admin-warn {
  background: hsl(38,90%,95%); border: 1px solid hsl(38,90%,78%);
  border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1.25rem;
  display: flex; gap: 10px; align-items: center;
  font-size: 0.85rem; color: hsl(38,90%,30%);
}

/* KPI */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.25rem; }
.kpi-card {
  background: var(--adm-surface); border: 1px solid var(--adm-border);
  border-radius: var(--radius); padding: 1.2rem; box-shadow: var(--shadow);
}
.kpi-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--adm-muted); }
.kpi-value { font-size: 1.8rem; font-weight: 900; color: var(--adm-text); margin: 5px 0 3px; }
.kpi-sub { font-size: 0.75rem; color: var(--adm-muted); }

/* Card */
.card { background: var(--adm-surface); border: 1px solid var(--adm-border); border-radius: var(--radius); padding: 1.25rem; margin-bottom: 1.25rem; box-shadow: var(--shadow); }
.card-title { font-size: 0.92rem; font-weight: 700; color: var(--adm-text); margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }

/* Table */
table { width: 100%; border-collapse: collapse; }
th { background: var(--adm-surface2); font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--adm-muted); padding: 0.6rem 0.85rem; text-align: left; }
td { padding: 0.72rem 0.85rem; border-bottom: 1px solid var(--adm-border); font-size: 0.85rem; vertical-align: middle; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: hsl(250,30%,98%); }

/* Badge */
.badge { display: inline-flex; align-items: center; gap: 4px; padding: 0.18rem 0.55rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }
.badge-primary { background: hsl(250,84%,94%); color: var(--adm-primary); }
.badge-success { background: hsl(142,60%,92%); color: var(--adm-success); }
.badge-warn    { background: hsl(38,90%,92%);  color: hsl(38,90%,32%); }
.badge-danger  { background: hsl(4,78%,94%);   color: var(--adm-danger); }
.badge-muted   { background: var(--adm-surface2); color: var(--adm-muted); border: 1px solid var(--adm-border); }
.badge-purple  { background: hsl(280,70%,94%); color: var(--adm-accent); }

/* Buttons */
.btn { padding: 0.45rem 1rem; border-radius: 6px; border: none; cursor: pointer; font-size: 0.82rem; font-weight: 600; transition: all 0.15s; display: inline-flex; align-items: center; gap: 5px; }
.btn-primary { background: var(--adm-primary); color: #fff; }
.btn-primary:hover { background: var(--adm-primary2); }
.btn-danger  { background: var(--adm-danger); color: #fff; }
.btn-ghost   { background: var(--adm-surface2); color: var(--adm-text); border: 1px solid var(--adm-border); }
.btn-ghost:hover { background: var(--adm-border); }
.btn-sm { padding: 0.28rem 0.65rem; font-size: 0.75rem; }

/* Toggle switch */
.toggle { position: relative; display: inline-block; width: 40px; height: 22px; }
.toggle input { opacity: 0; width: 0; height: 0; }
.toggle-slider { position: absolute; cursor: pointer; inset: 0; background: #ccc; border-radius: 22px; transition: 0.2s; }
.toggle-slider:before { content:''; position: absolute; width: 16px; height: 16px; left: 3px; top: 3px; background: white; border-radius: 50%; transition: 0.2s; }
input:checked + .toggle-slider { background: var(--adm-primary); }
input:checked + .toggle-slider:before { transform: translateX(18px); }

/* Search */
.toolbar { display: flex; gap: 0.75rem; margin-bottom: 1rem; align-items: center; flex-wrap: wrap; }
.search-input { padding: 0.45rem 0.85rem; border: 1px solid var(--adm-border); border-radius: 6px; font-size: 0.85rem; min-width: 220px; outline: none; background: var(--adm-surface2); color: var(--adm-text); }
.search-input:focus { border-color: var(--adm-primary); background: var(--adm-surface); }
select.filter { padding: 0.45rem 0.85rem; border: 1px solid var(--adm-border); border-radius: 6px; font-size: 0.85rem; background: var(--adm-surface2); color: var(--adm-text); cursor: pointer; outline: none; }

/* Code / Mono */
.mono { font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 0.8rem; }
"""
with open(os.path.join(base_dir, "src/styles/admin.css"), "w", encoding="utf-8") as f: f.write(css)

# Sidebar
sidebar_tsx = """'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const NAV = [
  { section: 'IDENTITY', items: [
    { href: '/dashboard', icon: '🏠', label: 'Dashboard' },
    { href: '/users',     icon: '👤', label: 'Users & RBAC' },
    { href: '/tenants',   icon: '🏢', label: 'Tenants' },
  ]},
  { section: 'PLATFORM', items: [
    { href: '/flags',     icon: '🚩', label: 'Feature Flags' },
    { href: '/gateway',   icon: '🌐', label: 'API Gateway' },
    { href: '/config',    icon: '⚙️', label: 'Configuration' },
    { href: '/platform',  icon: '🛠️', label: 'Platform Ops' },
  ]},
  { section: 'COMPLIANCE', items: [
    { href: '/audit',     icon: '📋', label: 'Audit Trail' },
    { href: '/monitoring',icon: '📊', label: 'Monitoring' },
  ]},
];

export function Sidebar() {
  const path = usePathname();
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">🛡️</div>
        <div className="logo-text">
          <div className="brand">Admin Portal</div>
          <div className="sub">MSRTC Platform</div>
        </div>
      </div>
      <nav className="sidebar-nav">
        {NAV.map(group => (
          <div key={group.section}>
            <div className="sidebar-section">{group.section}</div>
            {group.items.map(n => (
              <Link key={n.href} href={n.href} className={`nav-item ${path.startsWith(n.href) ? 'active' : ''}`}>
                <span className="nav-icon">{n.icon}</span>
                {n.label}
              </Link>
            ))}
          </div>
        ))}
      </nav>
      <div className="sidebar-footer">
        <div className="avatar">SA</div>
        <div>
          <div className="footer-name">Super Admin</div>
          <div className="footer-role">Platform Administrator</div>
        </div>
      </div>
    </aside>
  );
}
"""
with open(os.path.join(base_dir, "src/components/ui/Sidebar.tsx"), "w", encoding="utf-8") as f: f.write(sidebar_tsx)

# Root Layout
layout_tsx = """import '@/styles/admin.css';
import { Sidebar } from '@/components/ui/Sidebar';

export const metadata = {
  title: 'MSRTC Admin Portal',
  description: 'Platform administration, IAM, tenants, feature flags and compliance',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Sidebar />
        <div className="main-content">
          <div className="page-body">{children}</div>
        </div>
      </body>
    </html>
  );
}
"""
with open(os.path.join(base_dir, "src/app/layout.tsx"), "w", encoding="utf-8") as f: f.write(layout_tsx)

with open(os.path.join(base_dir, "src/app/page.tsx"), "w", encoding="utf-8") as f:
    f.write("import { redirect } from 'next/navigation';\nexport default function Root() { redirect('/dashboard'); }\n")

# ============================================================
# TASK 81 — Dashboard
# ============================================================
dashboard_page = """export default function AdminDashboardPage() {
  const kpis = [
    { label: 'Total Users', value: '32,841', sub: '↑ 142 this month' },
    { label: 'Active Tenants', value: '12', sub: '3 division tenants + HQ' },
    { label: 'Feature Flags', value: '48', sub: '31 enabled globally' },
    { label: 'Platform Health', value: '99.7%', sub: 'All services nominal' },
  ];

  const recentActivity = [
    { who: 'admin@msrtc.gov', action: 'Created role DEPOT_SUPERVISOR', when: '2 min ago', severity: 'info' },
    { who: 'sys-provisioner', action: 'Tenant onboarded: Konkan Division', when: '18 min ago', severity: 'success' },
    { who: 'admin@msrtc.gov', action: 'Feature flag GPS_V2 enabled (prod)', when: '1h ago', severity: 'warn' },
    { who: 'security-bot', action: 'Failed login attempt — IP blocked (203.0.113.42)', when: '2h ago', severity: 'danger' },
    { who: 'admin@msrtc.gov', action: 'Rate limit updated: /v1/booking → 1000 rpm', when: '3h ago', severity: 'info' },
  ];

  const services = [
    { name:'Auth Service', status:'HEALTHY', latency:'12ms', uptime:'99.98%' },
    { name:'Booking Service', status:'HEALTHY', latency:'34ms', uptime:'99.92%' },
    { name:'Payment Service', status:'HEALTHY', latency:'28ms', uptime:'99.95%' },
    { name:'Seat Service', status:'DEGRADED', latency:'180ms', uptime:'98.40%' },
    { name:'Notification Service', status:'HEALTHY', latency:'8ms', uptime:'99.99%' },
  ];

  const sevColor: Record<string, string> = { info:'var(--adm-info)', success:'var(--adm-success)', warn:'var(--adm-warn)', danger:'var(--adm-danger)' };
  const svcBadge: Record<string, string> = { HEALTHY:'badge-success', DEGRADED:'badge-warn', DOWN:'badge-danger' };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Admin Dashboard</h1>
        <p className="page-subtitle">Platform overview · Super Admin view</p>
      </div>

      <div className="admin-warn">
        ⚠️ <strong>Seat Service</strong> is currently <strong>DEGRADED</strong>. P95 latency at 180ms — investigate before peak hours.
      </div>

      <div className="kpi-grid">
        {kpis.map(k => (
          <div key={k.label} className="kpi-card">
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value">{k.value}</div>
            <div className="kpi-sub">{k.sub}</div>
          </div>
        ))}
      </div>

      <div className="two-col">
        <div className="card">
          <div className="card-title">Service Health</div>
          <table>
            <thead><tr><th>Service</th><th>Status</th><th>Latency</th><th>Uptime</th></tr></thead>
            <tbody>
              {services.map(s => (
                <tr key={s.name}>
                  <td style={{fontWeight:600}}>{s.name}</td>
                  <td><span className={`badge ${svcBadge[s.status]}`}>{s.status}</span></td>
                  <td className="mono">{s.latency}</td>
                  <td style={{color:parseFloat(s.uptime)<99.5?'var(--adm-danger)':'var(--adm-success)',fontWeight:700}}>{s.uptime}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card">
          <div className="card-title">Recent Admin Activity</div>
          {recentActivity.map((a,i) => (
            <div key={i} style={{display:'flex',gap:10,paddingBottom:10,marginBottom:10,borderBottom:'1px solid var(--adm-border)',alignItems:'flex-start'}}>
              <div style={{width:8,height:8,borderRadius:'50%',background:sevColor[a.severity],marginTop:5,flexShrink:0}} />
              <div style={{flex:1}}>
                <div style={{fontSize:'0.83rem',fontWeight:600}}>{a.action}</div>
                <div style={{fontSize:'0.75rem',color:'var(--adm-muted)',marginTop:2}}>{a.who} · {a.when}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/dashboard/page.tsx"), "w", encoding="utf-8") as f: f.write(dashboard_page)

# ============================================================
# TASK 82 — User & RBAC Management
# ============================================================
users_page = """"use client";
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
"""
with open(os.path.join(base_dir, "src/app/users/page.tsx"), "w", encoding="utf-8") as f: f.write(users_page)

# ============================================================
# TASK 83 — Tenant Management
# ============================================================
tenants_page = """"use client";
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
"""
with open(os.path.join(base_dir, "src/app/tenants/page.tsx"), "w", encoding="utf-8") as f: f.write(tenants_page)

# ============================================================
# TASK 84 — Feature Flags
# ============================================================
flags_page = """"use client";
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
"""
with open(os.path.join(base_dir, "src/app/flags/page.tsx"), "w", encoding="utf-8") as f: f.write(flags_page)

# ============================================================
# TASK 85 — API Gateway & Service Registry
# ============================================================
gateway_page = """"use client";
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
"""
with open(os.path.join(base_dir, "src/app/gateway/page.tsx"), "w", encoding="utf-8") as f: f.write(gateway_page)

# ============================================================
# TASK 86 — Audit Trail
# ============================================================
audit_page = """"use client";
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
"""
with open(os.path.join(base_dir, "src/app/audit/page.tsx"), "w", encoding="utf-8") as f: f.write(audit_page)

# ============================================================
# TASK 87 — Platform Operations Console
# ============================================================
platform_page = """"use client";
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
"""
with open(os.path.join(base_dir, "src/app/platform/page.tsx"), "w", encoding="utf-8") as f: f.write(platform_page)

# ============================================================
# TASK 88 — Configuration Management
# ============================================================
config_page = """"use client";
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
"""
with open(os.path.join(base_dir, "src/app/config/page.tsx"), "w", encoding="utf-8") as f: f.write(config_page)

# ============================================================
# TASK 89 — Monitoring & Observability
# ============================================================
monitoring_page = """export default function MonitoringPage() {
  const dashboards = [
    { name:'Platform Overview', tool:'Grafana', url:'http://grafana.internal/d/platform', desc:'Golden signals (latency, traffic, errors, saturation)', status:'LIVE' },
    { name:'Distributed Tracing', tool:'Jaeger', url:'http://jaeger.internal', desc:'End-to-end request traces across all microservices', status:'LIVE' },
    { name:'Log Analytics', tool:'Loki / Grafana', url:'http://grafana.internal/d/logs', desc:'Centralised log aggregation from all pods', status:'LIVE' },
    { name:'Kubernetes Cluster', tool:'Grafana', url:'http://grafana.internal/d/k8s', desc:'Node health, pod restarts, resource utilisation', status:'LIVE' },
    { name:'Kafka Lag Monitor', tool:'Grafana', url:'http://grafana.internal/d/kafka', desc:'Consumer group lag per topic', status:'LIVE' },
    { name:'SLO Dashboard', tool:'Grafana', url:'http://grafana.internal/d/slo', desc:'Service Level Objectives and error budget burn rates', status:'LIVE' },
  ];

  const alerts = [
    { rule:'SeatService P95 > 150ms', severity:'WARNING', firing:true, since:'1h 22m' },
    { rule:'KafkaTopic seat.locks consumer lag > 200', severity:'WARNING', firing:true, since:'45m' },
    { rule:'PaymentService error rate > 1%', severity:'CRITICAL', firing:false, since:'—' },
    { rule:'Any pod CrashLoopBackOff', severity:'CRITICAL', firing:false, since:'—' },
    { rule:'Redis memory > 80%', severity:'WARNING', firing:false, since:'—' },
  ];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Monitoring & Observability</h1>
        <p className="page-subtitle">OpenTelemetry · Prometheus · Loki · Jaeger · Grafana</p>
      </div>

      <div className="two-col">
        <div className="card">
          <div className="card-title">Observability Dashboards</div>
          {dashboards.map(d => (
            <div key={d.name} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'10px 0',borderBottom:'1px solid var(--adm-border)'}}>
              <div>
                <div style={{fontWeight:700,fontSize:'0.88rem'}}>{d.name}</div>
                <div style={{fontSize:'0.75rem',color:'var(--adm-muted)',marginTop:2}}>{d.tool} · {d.desc}</div>
              </div>
              <div style={{display:'flex',gap:8,alignItems:'center'}}>
                <span className="badge badge-success">● {d.status}</span>
                <a href={d.url} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-ghost">Open ↗</a>
              </div>
            </div>
          ))}
        </div>

        <div className="card">
          <div className="card-title">Active Alert Rules</div>
          {alerts.map(a => (
            <div key={a.rule} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'10px 0',borderBottom:'1px solid var(--adm-border)'}}>
              <div style={{flex:1}}>
                <div style={{fontSize:'0.83rem',fontWeight:600,color:a.firing?'var(--adm-danger)':'inherit'}}>{a.rule}</div>
                {a.firing && <div style={{fontSize:'0.72rem',color:'var(--adm-danger)',marginTop:2}}>🔴 FIRING · {a.since}</div>}
              </div>
              <span className={`badge ${a.severity==='CRITICAL'?'badge-danger':'badge-warn'}`}>{a.severity}</span>
            </div>
          ))}
          <div style={{marginTop:12,display:'flex',gap:8}}>
            <button className="btn btn-sm btn-ghost">View All Rules</button>
            <button className="btn btn-sm btn-primary">Create Rule</button>
          </div>
        </div>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/monitoring/page.tsx"), "w", encoding="utf-8") as f: f.write(monitoring_page)

print("Tasks 81-90: Admin & Enterprise Portal (Next.js) scaffolded successfully.")
