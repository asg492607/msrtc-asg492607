import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\hq-command"

dirs = [
    "src/app/dashboard", "src/app/map", "src/app/finance",
    "src/app/fleet", "src/app/hr", "src/app/incidents",
    "src/app/ai", "src/app/alerts", "src/app/reports",
    "src/components/ui", "src/styles", "src/types",
    "src/lib/api", "src/store", "public"
]
for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# ============================================================
# TASK 71 — Scaffold, package.json, Dark Theme Design System
# ============================================================
pkg = {
  "name": "hq-command",
  "version": "1.0.0",
  "private": True,
  "scripts": { "dev": "next dev --port 3002", "build": "next build", "start": "next start" },
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

next_config = "/** @type {import('next').NextConfig} */\nconst nextConfig = {};\nexport default nextConfig;\n"
with open(os.path.join(base_dir, "next.config.mjs"), "w", encoding="utf-8") as f: f.write(next_config)

# Dark command-center theme CSS
css = """:root {
  --hq-bg:       hsl(220, 28%, 8%);
  --hq-surface:  hsl(220, 25%, 12%);
  --hq-surface2: hsl(220, 22%, 17%);
  --hq-border:   hsl(220, 20%, 22%);
  --hq-primary:  hsl(210, 100%, 58%);
  --hq-accent:   hsl(165, 80%, 48%);
  --hq-warn:     hsl(38, 100%, 55%);
  --hq-danger:   hsl(4, 80%, 58%);
  --hq-success:  hsl(142, 65%, 48%);
  --hq-text:     hsl(220, 20%, 90%);
  --hq-muted:    hsl(220, 15%, 55%);
  --radius: 10px;
  --glow: 0 0 20px rgba(66,153,225,0.15);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--hq-bg);
  color: var(--hq-text);
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 230px; background: var(--hq-surface);
  border-right: 1px solid var(--hq-border);
  min-height: 100vh; display: flex; flex-direction: column;
  position: fixed; top: 0; left: 0; bottom: 0; z-index: 100;
}
.sidebar-logo { padding: 1.5rem; border-bottom: 1px solid var(--hq-border); }
.logo-badge { background: var(--hq-primary); color: #fff; font-size: 0.7rem; font-weight: 800; padding: 2px 7px; border-radius: 4px; letter-spacing: 1px; }
.logo-title { font-size: 1.1rem; font-weight: 900; color: var(--hq-text); margin-top: 6px; }
.logo-sub { font-size: 0.72rem; color: var(--hq-muted); margin-top: 2px; }

.sidebar-nav { flex: 1; padding: 0.75rem 0; }
.nav-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.65rem 1.25rem; color: var(--hq-muted);
  text-decoration: none; font-size: 0.875rem; font-weight: 500;
  transition: all 0.15s; border-left: 3px solid transparent;
}
.nav-item:hover, .nav-item.active {
  background: var(--hq-surface2); color: var(--hq-text);
  border-left-color: var(--hq-primary);
}
.nav-icon { font-size: 1rem; width: 18px; text-align: center; }

.sidebar-footer { padding: 1rem 1.25rem; border-top: 1px solid var(--hq-border); }
.user-name { font-size: 0.85rem; font-weight: 700; color: var(--hq-text); }
.user-role { font-size: 0.72rem; color: var(--hq-muted); margin-top: 2px; }

/* Main */
.main-content { margin-left: 230px; flex: 1; padding: 1.75rem; }
.page-header { margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: flex-start; }
.page-title { font-size: 1.4rem; font-weight: 800; color: var(--hq-text); }
.page-subtitle { color: var(--hq-muted); font-size: 0.82rem; margin-top: 3px; }
.live-badge { display: flex; align-items: center; gap: 6px; background: var(--hq-surface2); border: 1px solid var(--hq-border); padding: 0.4rem 0.85rem; border-radius: 20px; font-size: 0.78rem; }
.pulse { width: 8px; height: 8px; border-radius: 50%; background: var(--hq-success); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.4;} }

/* KPI */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.25rem; }
.kpi-card {
  background: var(--hq-surface); border: 1px solid var(--hq-border);
  border-radius: var(--radius); padding: 1.25rem;
  box-shadow: var(--glow); position: relative; overflow: hidden;
}
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; }
.kpi-card.blue::before { background: var(--hq-primary); }
.kpi-card.green::before { background: var(--hq-success); }
.kpi-card.yellow::before { background: var(--hq-warn); }
.kpi-card.red::before { background: var(--hq-danger); }
.kpi-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: var(--hq-muted); }
.kpi-value { font-size: 2rem; font-weight: 900; color: var(--hq-text); margin: 6px 0 4px; }
.kpi-delta { font-size: 0.78rem; }
.delta-up { color: var(--hq-success); }
.delta-down { color: var(--hq-danger); }

/* Card */
.card {
  background: var(--hq-surface); border: 1px solid var(--hq-border);
  border-radius: var(--radius); padding: 1.25rem; margin-bottom: 1.25rem;
}
.card-title { font-size: 0.95rem; font-weight: 700; color: var(--hq-text); margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
.three-col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.25rem; }

/* Table */
table { width: 100%; border-collapse: collapse; }
th { background: var(--hq-surface2); font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--hq-muted); padding: 0.65rem 0.85rem; text-align: left; }
td { padding: 0.7rem 0.85rem; border-bottom: 1px solid var(--hq-border); font-size: 0.85rem; vertical-align: middle; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: var(--hq-surface2); }

/* Badge */
.badge { display: inline-block; padding: 0.2rem 0.55rem; border-radius: 20px; font-size: 0.72rem; font-weight: 700; }
.badge-blue    { background: hsl(210,100%,15%); color: var(--hq-primary); border: 1px solid hsl(210,100%,25%); }
.badge-green   { background: hsl(142,65%,10%); color: var(--hq-success); border: 1px solid hsl(142,65%,20%); }
.badge-yellow  { background: hsl(38,100%,12%); color: var(--hq-warn); border: 1px solid hsl(38,100%,22%); }
.badge-red     { background: hsl(4,80%,12%); color: var(--hq-danger); border: 1px solid hsl(4,80%,22%); }
.badge-muted   { background: var(--hq-surface2); color: var(--hq-muted); border: 1px solid var(--hq-border); }

/* Buttons */
.btn { padding: 0.45rem 1rem; border-radius: 6px; border: none; cursor: pointer; font-size: 0.82rem; font-weight: 600; transition: all 0.15s; }
.btn-primary { background: var(--hq-primary); color: #fff; }
.btn-primary:hover { opacity: 0.85; transform: translateY(-1px); }
.btn-sm { padding: 0.3rem 0.65rem; font-size: 0.75rem; }
.btn-danger { background: var(--hq-danger); color: #fff; }
.btn-ghost { background: var(--hq-surface2); color: var(--hq-text); border: 1px solid var(--hq-border); }

/* Progress bar */
.progress-bar { height: 6px; background: var(--hq-surface2); border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }

/* Toolbar */
.toolbar { display: flex; gap: 0.75rem; margin-bottom: 1rem; align-items: center; flex-wrap: wrap; }
.search-input { background: var(--hq-surface2); border: 1px solid var(--hq-border); color: var(--hq-text); padding: 0.45rem 0.85rem; border-radius: 6px; font-size: 0.85rem; min-width: 200px; outline: none; }
.search-input:focus { border-color: var(--hq-primary); }
select.filter { background: var(--hq-surface2); border: 1px solid var(--hq-border); color: var(--hq-text); padding: 0.45rem 0.85rem; border-radius: 6px; font-size: 0.85rem; cursor: pointer; }

/* Stat row */
.stat-row { display: flex; gap: 1rem; flex-wrap: wrap; }
.mini-stat { background: var(--hq-surface2); border-radius: 8px; padding: 0.75rem 1rem; flex: 1; min-width: 100px; }
.mini-stat-val { font-size: 1.4rem; font-weight: 900; color: var(--hq-text); }
.mini-stat-label { font-size: 0.72rem; color: var(--hq-muted); margin-top: 2px; }
"""
with open(os.path.join(base_dir, "src/styles/hq.css"), "w", encoding="utf-8") as f: f.write(css)

# Sidebar Component
sidebar_tsx = """'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const NAV = [
  { href: '/dashboard', icon: '⚡', label: 'Executive Dashboard' },
  { href: '/map',       icon: '🗺️', label: 'Live State Map' },
  { href: '/finance',   icon: '💹', label: 'Finance Analytics' },
  { href: '/fleet',     icon: '🚌', label: 'Fleet Analytics' },
  { href: '/hr',        icon: '👥', label: 'Workforce' },
  { href: '/incidents', icon: '🚨', label: 'Incident Management' },
  { href: '/ai',        icon: '🤖', label: 'AI Insights' },
  { href: '/alerts',    icon: '🔔', label: 'Alert Center' },
  { href: '/reports',   icon: '📊', label: 'Reports' },
];

export function Sidebar() {
  const path = usePathname();
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-badge">HQ</div>
        <div className="logo-title">Command Center</div>
        <div className="logo-sub">Maharashtra State RTC</div>
      </div>
      <nav className="sidebar-nav">
        {NAV.map(n => (
          <Link key={n.href} href={n.href} className={`nav-item ${path.startsWith(n.href) ? 'active' : ''}`}>
            <span className="nav-icon">{n.icon}</span>
            {n.label}
          </Link>
        ))}
      </nav>
      <div className="sidebar-footer">
        <div className="user-name">Sunetra Pawar</div>
        <div className="user-role">Director General, MSRTC</div>
      </div>
    </aside>
  );
}
"""
with open(os.path.join(base_dir, "src/components/ui/Sidebar.tsx"), "w", encoding="utf-8") as f: f.write(sidebar_tsx)

# Root Layout
layout_tsx = """import '@/styles/hq.css';
import { Sidebar } from '@/components/ui/Sidebar';

export const metadata = {
  title: 'MSRTC HQ Command Center',
  description: 'Executive command center for Maharashtra State Road Transport Corporation',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Sidebar />
        <div className="main-content">{children}</div>
      </body>
    </html>
  );
}
"""
with open(os.path.join(base_dir, "src/app/layout.tsx"), "w", encoding="utf-8") as f: f.write(layout_tsx)

with open(os.path.join(base_dir, "src/app/page.tsx"), "w", encoding="utf-8") as f:
    f.write("import { redirect } from 'next/navigation';\nexport default function Root() { redirect('/dashboard'); }\n")

# ============================================================
# TASK 72 — Executive KPI Dashboard
# ============================================================
dashboard_page = """export default function DashboardPage() {
  const kpis = [
    { label: 'Total Fleet', value: '5,840', delta: '+12 this month', dir: 'up', color: 'blue' },
    { label: 'Active Buses', value: '4,921', delta: '84.3% utilisation', dir: 'up', color: 'green' },
    { label: "Today's Revenue", value: '₹3.8Cr', delta: '+11% vs last week', dir: 'up', color: 'green' },
    { label: 'On-Time Rate', value: '88.7%', delta: '-1.3% from target', dir: 'down', color: 'yellow' },
  ];

  const kpis2 = [
    { label: 'Depots Online', value: '244/251', delta: '7 in maintenance', dir: 'down', color: 'yellow' },
    { label: 'Daily Passengers', value: '61.2L', delta: '+4.8% YoY', dir: 'up', color: 'blue' },
    { label: 'CSAT Score', value: '4.2/5', delta: '+0.1 from last month', dir: 'up', color: 'green' },
    { label: 'Open Incidents', value: '14', delta: '-6 from yesterday', dir: 'up', color: 'red' },
  ];

  const divisions = [
    { name: 'Mumbai', fleet: 820, active: 712, revenue: '₹84.2L', otd: '91%' },
    { name: 'Pune', fleet: 640, active: 558, revenue: '₹62.1L', otd: '89%' },
    { name: 'Nashik', fleet: 420, active: 361, revenue: '₹38.4L', otd: '85%' },
    { name: 'Aurangabad', fleet: 380, active: 318, revenue: '₹31.8L', otd: '82%' },
    { name: 'Nagpur', fleet: 510, active: 441, revenue: '₹48.2L', otd: '87%' },
    { name: 'Konkan', fleet: 290, active: 241, revenue: '₹22.6L', otd: '79%' },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Executive Dashboard</h1>
          <p className="page-subtitle">Maharashtra State Road Transport Corporation · Real-time Operations</p>
        </div>
        <div className="live-badge">
          <span className="pulse"></span>
          <span>Live · {new Date().toLocaleTimeString()}</span>
        </div>
      </div>

      <div className="kpi-grid">
        {kpis.map(k => (
          <div key={k.label} className={`kpi-card ${k.color}`}>
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value">{k.value}</div>
            <div className={`kpi-delta ${k.dir === 'up' ? 'delta-up' : 'delta-down'}`}>
              {k.dir === 'up' ? '▲' : '▼'} {k.delta}
            </div>
          </div>
        ))}
      </div>

      <div className="kpi-grid">
        {kpis2.map(k => (
          <div key={k.label} className={`kpi-card ${k.color}`}>
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value">{k.value}</div>
            <div className={`kpi-delta ${k.dir === 'up' ? 'delta-up' : 'delta-down'}`}>
              {k.dir === 'up' ? '▲' : '▼'} {k.delta}
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="card-title">
          Division Performance
          <span style={{fontSize:'0.78rem',color:'var(--hq-muted)'}}>All 6 divisions</span>
        </div>
        <table>
          <thead><tr><th>Division</th><th>Total Fleet</th><th>Active</th><th>Utilisation</th><th>Today Revenue</th><th>On-Time Rate</th></tr></thead>
          <tbody>
            {divisions.map(d => (
              <tr key={d.name}>
                <td style={{fontWeight:700}}>{d.name}</td>
                <td>{d.fleet}</td>
                <td>{d.active}</td>
                <td>
                  <div style={{display:'flex',alignItems:'center',gap:8}}>
                    <div className="progress-bar" style={{width:80}}>
                      <div className="progress-fill" style={{width:`${(d.active/d.fleet*100).toFixed(0)}%`,background:'var(--hq-primary)'}} />
                    </div>
                    <span style={{fontSize:'0.8rem'}}>{(d.active/d.fleet*100).toFixed(1)}%</span>
                  </div>
                </td>
                <td style={{fontWeight:700,color:'var(--hq-accent)'}}>{d.revenue}</td>
                <td><span className={`badge ${parseInt(d.otd)>=90?'badge-green':parseInt(d.otd)>=80?'badge-yellow':'badge-red'}`}>{d.otd}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/dashboard/page.tsx"), "w", encoding="utf-8") as f: f.write(dashboard_page)

# ============================================================
# TASK 73 — Live State Map
# ============================================================
map_page = """export default function MapPage() {
  const heatspots = [
    { region: 'Mumbai Metropolitan', buses: 820, alerts: 2 },
    { region: 'Pune Division', buses: 640, alerts: 1 },
    { region: 'Nashik Division', buses: 420, alerts: 3 },
    { region: 'Aurangabad Division', buses: 380, alerts: 0 },
    { region: 'Nagpur Division', buses: 510, alerts: 1 },
    { region: 'Konkan Division', buses: 290, alerts: 4 },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Live State Map</h1>
          <p className="page-subtitle">Real-time fleet positions across Maharashtra · 4,921 active buses</p>
        </div>
        <div className="live-badge"><span className="pulse"></span>Live GPS Feed</div>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'1fr 300px',gap:'1.25rem'}}>
        <div className="card" style={{minHeight:520,display:'flex',alignItems:'center',justifyContent:'center',background:'linear-gradient(145deg,hsl(220,35%,8%),hsl(220,28%,14%))',position:'relative',overflow:'hidden'}}>
          <div style={{position:'absolute',inset:0,opacity:0.05,backgroundImage:'radial-gradient(circle at 30% 40%, hsl(210,100%,58%) 0%, transparent 50%), radial-gradient(circle at 70% 60%, hsl(165,80%,48%) 0%, transparent 50%)'}} />
          <div style={{textAlign:'center',position:'relative',zIndex:1}}>
            <div style={{fontSize:56,marginBottom:16}}>🗺️</div>
            <div style={{fontSize:'1.1rem',fontWeight:800,color:'var(--hq-text)'}}>Maharashtra Fleet Map</div>
            <div style={{fontSize:'0.82rem',color:'var(--hq-muted)',marginTop:6,marginBottom:20}}>Leaflet / Mapbox GL JS integration · v1 API: GET /v1/fleet/positions</div>
            <div style={{display:'flex',flexWrap:'wrap',gap:8,justifyContent:'center',maxWidth:400}}>
              {['Mumbai','Pune','Nashik','Aurangabad','Nagpur','Amravati','Kolhapur','Solapur','Latur'].map(d => (
                <span key={d} style={{background:'rgba(66,153,225,0.15)',border:'1px solid rgba(66,153,225,0.3)',color:'var(--hq-primary)',padding:'4px 10px',borderRadius:20,fontSize:'0.75rem',fontWeight:600}}>
                  📍 {d}
                </span>
              ))}
            </div>
          </div>
        </div>

        <div>
          <div className="card" style={{marginBottom:'1rem'}}>
            <div className="card-title">Division Status</div>
            {heatspots.map(h => (
              <div key={h.region} style={{marginBottom:12}}>
                <div style={{display:'flex',justifyContent:'space-between',marginBottom:4}}>
                  <span style={{fontSize:'0.82rem',fontWeight:600}}>{h.region}</span>
                  <div style={{display:'flex',gap:6,alignItems:'center'}}>
                    {h.alerts > 0 && <span className="badge badge-red">⚠ {h.alerts}</span>}
                    <span style={{fontSize:'0.78rem',color:'var(--hq-muted)'}}>{h.buses}</span>
                  </div>
                </div>
                <div className="progress-bar">
                  <div className="progress-fill" style={{width:`${(h.buses/820*100).toFixed(0)}%`,background:h.alerts>2?'var(--hq-warn)':'var(--hq-primary)'}} />
                </div>
              </div>
            ))}
          </div>

          <div className="card">
            <div className="card-title">Map Legend</div>
            {[{icon:'🟢',label:'On-Time Bus'},{icon:'🟡',label:'Delayed Bus'},{icon:'🔴',label:'Breakdown'},{icon:'⚪',label:'Depot'},{icon:'🔵',label:'Bus Stop'}].map(l => (
              <div key={l.label} style={{display:'flex',gap:8,alignItems:'center',marginBottom:8,fontSize:'0.82rem',color:'var(--hq-muted)'}}>
                <span>{l.icon}</span>{l.label}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/map/page.tsx"), "w", encoding="utf-8") as f: f.write(map_page)

# ============================================================
# TASK 74 — Finance & Revenue Analytics
# ============================================================
finance_page = """export default function FinancePage() {
  const monthly = [
    { month:'Jan',rev:28.4,exp:19.2},{month:'Feb',rev:31.2,exp:20.1},{month:'Mar',rev:35.8,exp:22.4},
    { month:'Apr',rev:29.6,exp:19.8},{month:'May',rev:33.1,exp:21.2},{month:'Jun',rev:38.4,exp:23.5},
    { month:'Jul',rev:41.2,exp:24.8,current:true},
  ];
  const maxRev = Math.max(...monthly.map(m => m.rev));

  const topRoutes = [
    { route:'Mumbai-Pune',rev:'₹8.4Cr',trips:1240,margin:'34%' },
    { route:'Mumbai-Nashik',rev:'₹5.2Cr',trips:860,margin:'29%' },
    { route:'Pune-Aurangabad',rev:'₹3.8Cr',trips:640,margin:'31%' },
    { route:'Mumbai-Kolhapur',rev:'₹4.1Cr',trips:520,margin:'28%' },
    { route:'Nagpur-Amravati',rev:'₹2.9Cr',trips:480,margin:'33%' },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Finance & Revenue Analytics</h1>
          <p className="page-subtitle">Statewide financial performance · FY 2025-26</p>
        </div>
      </div>

      <div className="kpi-grid">
        {[{l:'Monthly Revenue',v:'₹41.2Cr',d:'▲ 7.3% vs Jun',c:'green'},{l:'Monthly Expenditure',v:'₹24.8Cr',d:'▲ 5.5% vs Jun',c:'yellow'},{l:'Operating Surplus',v:'₹16.4Cr',d:'▲ 10.2% vs Jun',c:'green'},{l:'Cost per KM',v:'₹14.2',d:'▼ 0.8 vs Jun',c:'green'}].map(k=>(
          <div key={k.l} className={`kpi-card ${k.c}`}>
            <div className="kpi-label">{k.l}</div>
            <div className="kpi-value">{k.v}</div>
            <div className="kpi-delta delta-up">{k.d}</div>
          </div>
        ))}
      </div>

      <div className="two-col">
        <div className="card">
          <div className="card-title">Monthly Revenue vs Expenditure (₹Cr)</div>
          <div style={{display:'flex',alignItems:'flex-end',gap:6,height:180,paddingBottom:24,position:'relative'}}>
            {monthly.map(m => (
              <div key={m.month} style={{flex:1,display:'flex',flexDirection:'column',alignItems:'center',gap:2}}>
                <div style={{width:'100%',display:'flex',flexDirection:'column',alignItems:'center',gap:2}}>
                  <div style={{width:'45%',background:'var(--hq-primary)',borderRadius:'3px 3px 0 0',height:`${(m.rev/maxRev)*140}px`,opacity:m.current?1:0.7}} />
                  <div style={{width:'45%',background:'var(--hq-danger)',borderRadius:'3px 3px 0 0',height:`${(m.exp/maxRev)*140}px`,opacity:0.7,marginTop:-2}} />
                </div>
                <span style={{fontSize:'0.7rem',color:'var(--hq-muted)',marginTop:4}}>{m.month}</span>
              </div>
            ))}
          </div>
          <div style={{display:'flex',gap:16,justifyContent:'center',fontSize:'0.75rem',color:'var(--hq-muted)'}}>
            <span><span style={{color:'var(--hq-primary)'}}>■</span> Revenue</span>
            <span><span style={{color:'var(--hq-danger)'}}>■</span> Expenditure</span>
          </div>
        </div>

        <div className="card">
          <div className="card-title">Top Revenue Routes</div>
          <table>
            <thead><tr><th>Route</th><th>Revenue</th><th>Trips</th><th>Margin</th></tr></thead>
            <tbody>
              {topRoutes.map(r => (
                <tr key={r.route}>
                  <td style={{fontSize:'0.82rem'}}>{r.route}</td>
                  <td style={{fontWeight:700,color:'var(--hq-accent)'}}>{r.rev}</td>
                  <td>{r.trips}</td>
                  <td><span className="badge badge-green">{r.margin}</span></td>
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
with open(os.path.join(base_dir, "src/app/finance/page.tsx"), "w", encoding="utf-8") as f: f.write(finance_page)

# ============================================================
# TASK 75 — Fleet Analytics
# ============================================================
fleet_page = """export default function FleetPage() {
  const breakdown = [
    { type:'Shivneri AC',count:840,active:791,avgAge:'3.2y',breakdowns:12 },
    { type:'Shivshahi',count:1240,active:1128,avgAge:'5.1y',breakdowns:28 },
    { type:'Ordinary',count:2100,active:1872,avgAge:'8.4y',breakdowns:71 },
    { type:'Hirkani (Women)',count:420,active:402,avgAge:'4.8y',breakdowns:8 },
    { type:'EV Pilot',count:24,active:24,avgAge:'1.1y',breakdowns:0 },
  ];

  const maintenance = [
    { issue:'Brake System',count:48,severity:'HIGH' },
    { issue:'Engine',count:31,severity:'HIGH' },
    { issue:'AC / Climate',count:66,severity:'MEDIUM' },
    { issue:'Tyres',count:82,severity:'MEDIUM' },
    { issue:'Body / Glass',count:34,severity:'LOW' },
    { issue:'Electrical',count:27,severity:'MEDIUM' },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Fleet Analytics</h1>
          <p className="page-subtitle">5,840 buses across 251 depots statewide</p>
        </div>
      </div>

      <div className="kpi-grid">
        {[{l:'Total Fleet',v:'5,840',c:'blue'},{l:'Utilisation Rate',v:'84.3%',c:'green'},{l:'Avg Fleet Age',v:'6.2 yrs',c:'yellow'},{l:'Breakdown Rate',v:'2.1%',c:'red'}].map(k=>(
          <div key={k.l} className={`kpi-card ${k.c}`}>
            <div className="kpi-label">{k.l}</div>
            <div className="kpi-value">{k.v}</div>
          </div>
        ))}
      </div>

      <div className="two-col">
        <div className="card">
          <div className="card-title">Fleet by Type</div>
          <table>
            <thead><tr><th>Bus Type</th><th>Count</th><th>Active</th><th>Utilisation</th><th>Avg Age</th><th>Breakdowns</th></tr></thead>
            <tbody>
              {breakdown.map(b => (
                <tr key={b.type}>
                  <td style={{fontWeight:600}}>{b.type}</td>
                  <td>{b.count}</td>
                  <td>{b.active}</td>
                  <td>
                    <div style={{display:'flex',alignItems:'center',gap:6}}>
                      <div className="progress-bar" style={{width:60}}>
                        <div className="progress-fill" style={{width:`${(b.active/b.count*100).toFixed(0)}%`,background:(b.active/b.count)>0.9?'var(--hq-success)':'var(--hq-warn)'}} />
                      </div>
                      <span style={{fontSize:'0.78rem'}}>{(b.active/b.count*100).toFixed(0)}%</span>
                    </div>
                  </td>
                  <td>{b.avgAge}</td>
                  <td style={{color:b.breakdowns>20?'var(--hq-danger)':b.breakdowns>5?'var(--hq-warn)':'var(--hq-success)',fontWeight:700}}>{b.breakdowns}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card">
          <div className="card-title">Top Maintenance Issues</div>
          {maintenance.map(m => (
            <div key={m.issue} style={{marginBottom:12}}>
              <div style={{display:'flex',justifyContent:'space-between',marginBottom:4}}>
                <span style={{fontSize:'0.83rem',fontWeight:600}}>{m.issue}</span>
                <div style={{display:'flex',gap:6,alignItems:'center'}}>
                  <span className={`badge ${m.severity==='HIGH'?'badge-red':m.severity==='MEDIUM'?'badge-yellow':'badge-muted'}`}>{m.severity}</span>
                  <span style={{fontSize:'0.78rem',color:'var(--hq-muted)'}}>{m.count} buses</span>
                </div>
              </div>
              <div className="progress-bar">
                <div className="progress-fill" style={{width:`${(m.count/82*100).toFixed(0)}%`,background:m.severity==='HIGH'?'var(--hq-danger)':m.severity==='MEDIUM'?'var(--hq-warn)':'var(--hq-muted)'}} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/fleet/page.tsx"), "w", encoding="utf-8") as f: f.write(fleet_page)

# ============================================================
# TASK 76 — HR & Workforce Analytics
# ============================================================
hr_page = """export default function HRPage() {
  const staffByCategory = [
    { role:'Drivers',total:12400,present:11820,onLeave:340,absent:240 },
    { role:'Conductors',total:11800,present:11210,onLeave:310,absent:280 },
    { role:'Mechanics',total:3200,present:3050,onLeave:90,absent:60 },
    { role:'Admin Staff',total:4600,present:4390,onLeave:140,absent:70 },
  ];

  const pendingItems = [
    { item:'Driving License Renewals Due', count: 142, urgency: 'HIGH' },
    { item:'Medical Fitness Certificates Expiring', count: 89, urgency: 'HIGH' },
    { item:'Uniform Allowance Pending', count: 2340, urgency: 'MEDIUM' },
    { item:'Provident Fund Disputes', count: 28, urgency: 'LOW' },
    { item:'Promotion Backlogs', count: 66, urgency: 'MEDIUM' },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Workforce Analytics</h1>
          <p className="page-subtitle">32,000 employees across Maharashtra</p>
        </div>
      </div>

      <div className="kpi-grid">
        {[{l:'Total Employees',v:'32,000',c:'blue'},{l:'Present Today',v:'30,470',c:'green'},{l:'On Leave',v:'880',c:'yellow'},{l:'Attrition Rate (YTD)',v:'2.4%',c:'red'}].map(k=>(
          <div key={k.l} className={`kpi-card ${k.c}`}><div className="kpi-label">{k.l}</div><div className="kpi-value">{k.v}</div></div>
        ))}
      </div>

      <div className="two-col">
        <div className="card">
          <div className="card-title">Attendance by Category</div>
          {staffByCategory.map(s => (
            <div key={s.role} style={{marginBottom:16}}>
              <div style={{display:'flex',justifyContent:'space-between',marginBottom:4}}>
                <span style={{fontWeight:700,fontSize:'0.85rem'}}>{s.role}</span>
                <span style={{fontSize:'0.78rem',color:'var(--hq-muted)'}}>{s.present.toLocaleString()}/{s.total.toLocaleString()} present</span>
              </div>
              <div className="progress-bar" style={{height:10}}>
                <div className="progress-fill" style={{width:`${(s.present/s.total*100).toFixed(0)}%`,background:'var(--hq-success)'}} />
              </div>
              <div style={{display:'flex',gap:12,marginTop:4,fontSize:'0.72rem',color:'var(--hq-muted)'}}>
                <span style={{color:'var(--hq-warn)'}}>On leave: {s.onLeave}</span>
                <span style={{color:'var(--hq-danger)'}}>Absent: {s.absent}</span>
              </div>
            </div>
          ))}
        </div>

        <div className="card">
          <div className="card-title">Pending HR Actions</div>
          {pendingItems.map(p => (
            <div key={p.item} style={{display:'flex',justifyContent:'space-between',alignItems:'center',paddingBottom:10,marginBottom:10,borderBottom:'1px solid var(--hq-border)'}}>
              <div>
                <div style={{fontSize:'0.83rem',fontWeight:600}}>{p.item}</div>
              </div>
              <div style={{display:'flex',gap:8,alignItems:'center'}}>
                <span style={{fontSize:'1rem',fontWeight:800,color:p.urgency==='HIGH'?'var(--hq-danger)':p.urgency==='MEDIUM'?'var(--hq-warn)':'var(--hq-muted)'}}>{p.count}</span>
                <span className={`badge ${p.urgency==='HIGH'?'badge-red':p.urgency==='MEDIUM'?'badge-yellow':'badge-muted'}`}>{p.urgency}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/hr/page.tsx"), "w", encoding="utf-8") as f: f.write(hr_page)

# ============================================================
# TASK 77 — Incident Management
# ============================================================
incident_page = """"use client";
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
"""
with open(os.path.join(base_dir, "src/app/incidents/page.tsx"), "w", encoding="utf-8") as f: f.write(incident_page)

# ============================================================
# TASK 78 — AI Insights Panel
# ============================================================
ai_page = """export default function AIPage() {
  const insights = [
    { category:'Demand Forecasting', insight:'Predicted 22% surge in Mumbai-Pune travel on 2026-07-10 (public holiday). Recommend deploying 40 additional Shivneri buses.', confidence:'94%', impact:'HIGH', action:'Deploy Additional Fleet' },
    { category:'Predictive Maintenance', insight:'Bus MH-09-CD-4521 shows engine vibration pattern consistent with bearing failure. Predicted failure within 8-12 days.', confidence:'87%', impact:'HIGH', action:'Schedule Inspection' },
    { category:'Revenue Optimization', insight:'Nashik-Aurangabad route shows 62% empty seats on Tuesdays. Recommend dynamic pricing reduction of 15% to improve load factor.', confidence:'79%', impact:'MEDIUM', action:'Adjust Pricing' },
    { category:'Fuel Efficiency', insight:'Drivers on NH-48 corridor show 8% higher fuel consumption than benchmark. Eco-driving training recommended for 34 drivers.', confidence:'91%', impact:'MEDIUM', action:'Schedule Training' },
    { category:'Passenger Experience', insight:'Complaint volume for Konkan division increased 28% this month, primarily about AC failures. 6 specific buses identified.', confidence:'99%', impact:'MEDIUM', action:'Prioritize Repairs' },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">AI Insights</h1>
          <p className="page-subtitle">Machine learning recommendations · Updated every 6 hours</p>
        </div>
        <div className="live-badge"><span style={{color:'var(--hq-accent)'}}>🤖</span> AI Engine Active</div>
      </div>

      <div className="kpi-grid">
        {[{l:'Insights Generated',v:'142',c:'blue'},{l:'High Impact Actions',v:'12',c:'red'},{l:'Avg Confidence',v:'88.4%',c:'green'},{l:'Est. Savings (Monthly)',v:'₹42L',c:'green'}].map(k=>(
          <div key={k.l} className={`kpi-card ${k.c}`}><div className="kpi-label">{k.l}</div><div className="kpi-value">{k.v}</div></div>
        ))}
      </div>

      <div style={{display:'flex',flexDirection:'column',gap:'1rem'}}>
        {insights.map((ins,i) => (
          <div key={i} className="card" style={{borderLeft:`3px solid ${ins.impact==='HIGH'?'var(--hq-danger)':'var(--hq-warn)'}`}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',marginBottom:8}}>
              <div>
                <span className="badge badge-blue" style={{marginRight:8}}>{ins.category}</span>
                <span className="badge badge-muted">Confidence: {ins.confidence}</span>
              </div>
              <span className={`badge ${ins.impact==='HIGH'?'badge-red':'badge-yellow'}`}>{ins.impact} IMPACT</span>
            </div>
            <p style={{fontSize:'0.88rem',color:'var(--hq-text)',lineHeight:1.6,marginBottom:12}}>{ins.insight}</p>
            <button className="btn btn-primary btn-sm">{ins.action}</button>
          </div>
        ))}
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/ai/page.tsx"), "w", encoding="utf-8") as f: f.write(ai_page)

# ============================================================
# TASK 79 — Alert Center
# ============================================================
alerts_page = """"use client";
import { useState } from 'react';

const ALERTS = [
  { id:'ALT-001', type:'CRITICAL', icon:'🚨', title:'Accident on NH-48', desc:'Bus MH-01-AB-4521 involved in road accident near Khopoli. Emergency services deployed.', time:'9 min ago', acked: false },
  { id:'ALT-002', type:'HIGH', icon:'⚠️', title:'Breakdown — Nashik Bypass', desc:'Bus MH-09-CD-1234 stopped due to engine failure. Replacement bus dispatched.', time:'21 min ago', acked: false },
  { id:'ALT-003', type:'HIGH', icon:'⛽', title:'Fuel Shortage — Aurangabad Depot', desc:'Fuel stock at 18% capacity. Tanker ETA: 4 hours.', time:'45 min ago', acked: true },
  { id:'ALT-004', type:'MEDIUM', icon:'🕐', title:'High Delay Rate — Konkan Division', desc:'Average delay exceeding 22 minutes on 6 routes. Traffic congestion reported.', time:'1h ago', acked: true },
  { id:'ALT-005', type:'LOW', icon:'ℹ️', title:'Scheduled Maintenance Reminder', desc:'8 buses due for 10,000km service this week at Mumbai Central Depot.', time:'2h ago', acked: true },
];

const ACOLORS: Record<string,string> = {
  CRITICAL:'hsl(4,80%,12%)', HIGH:'hsl(38,100%,10%)', MEDIUM:'hsl(210,100%,10%)', LOW:'var(--hq-surface2)'
};
const ABORDERS: Record<string,string> = {
  CRITICAL:'var(--hq-danger)', HIGH:'var(--hq-warn)', MEDIUM:'var(--hq-primary)', LOW:'var(--hq-border)'
};

export default function AlertsPage() {
  const [alerts, setAlerts] = useState(ALERTS);
  const ack = (id: string) => setAlerts(prev => prev.map(a => a.id===id?{...a,acked:true}:a));

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Alert Center</h1>
          <p className="page-subtitle">{alerts.filter(a=>!a.acked).length} unacknowledged · {alerts.filter(a=>a.type==='CRITICAL').length} critical</p>
        </div>
        <button className="btn btn-ghost">Mark All Read</button>
      </div>

      <div style={{display:'flex',flexDirection:'column',gap:'0.85rem'}}>
        {alerts.map(a => (
          <div key={a.id} style={{background:ACOLORS[a.type],border:`1px solid ${ABORDERS[a.type]}`,borderRadius:10,padding:'1rem 1.25rem',display:'flex',gap:'1rem',alignItems:'flex-start',opacity:a.acked?0.6:1}}>
            <span style={{fontSize:24,marginTop:2}}>{a.icon}</span>
            <div style={{flex:1}}>
              <div style={{display:'flex',justifyContent:'space-between',marginBottom:4}}>
                <span style={{fontWeight:700,fontSize:'0.92rem'}}>{a.title}</span>
                <span style={{fontSize:'0.75rem',color:'var(--hq-muted)'}}>{a.time}</span>
              </div>
              <p style={{fontSize:'0.83rem',color:'var(--hq-muted)',lineHeight:1.5}}>{a.desc}</p>
            </div>
            {!a.acked && (
              <button className="btn btn-sm btn-ghost" onClick={()=>ack(a.id)} style={{whiteSpace:'nowrap'}}>Acknowledge</button>
            )}
            {a.acked && <span style={{fontSize:'0.75rem',color:'var(--hq-success)',whiteSpace:'nowrap',marginTop:4}}>✓ Acked</span>}
          </div>
        ))}
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/alerts/page.tsx"), "w", encoding="utf-8") as f: f.write(alerts_page)

# ============================================================
# TASK 80 — Reports page (polish / summary)
# ============================================================
reports_page = """export default function ReportsPage() {
  const reports = [
    { name:'Daily Operations Summary', lastGenerated:'Today 06:00', schedule:'Daily', format:'PDF/Excel', status:'READY' },
    { name:'Weekly Revenue Report', lastGenerated:'2026-06-30', schedule:'Weekly', format:'PDF', status:'READY' },
    { name:'Monthly Fleet Health Report', lastGenerated:'2026-06-01', schedule:'Monthly', format:'PDF/Excel', status:'GENERATING' },
    { name:'Quarterly Financial Statement', lastGenerated:'2026-04-01', schedule:'Quarterly', format:'PDF', status:'READY' },
    { name:'Annual Performance Review', lastGenerated:'2026-04-01', schedule:'Annual', format:'PDF/PPT', status:'READY' },
    { name:'Incident Analysis Report', lastGenerated:'Today 08:00', schedule:'On-Demand', format:'PDF', status:'READY' },
    { name:'Compliance Audit Report', lastGenerated:'2026-07-01', schedule:'Monthly', format:'PDF', status:'READY' },
    { name:'Fuel Efficiency Analysis', lastGenerated:'2026-07-04', schedule:'Weekly', format:'Excel', status:'READY' },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Reports</h1>
          <p className="page-subtitle">Scheduled and on-demand executive reports</p>
        </div>
        <button className="btn btn-primary">+ Generate Report</button>
      </div>

      <div className="card">
        <table>
          <thead><tr><th>Report Name</th><th>Last Generated</th><th>Schedule</th><th>Format</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            {reports.map(r => (
              <tr key={r.name}>
                <td style={{fontWeight:600}}>{r.name}</td>
                <td style={{fontSize:'0.82rem',color:'var(--hq-muted)'}}>{r.lastGenerated}</td>
                <td><span className="badge badge-muted">{r.schedule}</span></td>
                <td style={{fontSize:'0.82rem'}}>{r.format}</td>
                <td><span className={`badge ${r.status==='READY'?'badge-green':'badge-yellow'}`}>{r.status}</span></td>
                <td style={{display:'flex',gap:6}}>
                  <button className="btn btn-sm btn-primary" disabled={r.status!=='READY'} style={{opacity:r.status!=='READY'?0.4:1}}>⬇ Download</button>
                  <button className="btn btn-sm btn-ghost">Schedule</button>
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
with open(os.path.join(base_dir, "src/app/reports/page.tsx"), "w", encoding="utf-8") as f: f.write(reports_page)

print("Tasks 71-80: HQ Command Center (Next.js) scaffolded successfully.")
