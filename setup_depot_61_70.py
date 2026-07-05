import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\depot-dashboard"

dirs = [
    "src/app/dashboard",
    "src/app/dispatch",
    "src/app/fleet",
    "src/app/crew",
    "src/app/maintenance",
    "src/app/operations",
    "src/app/inventory",
    "src/app/finance",
    "src/app/compliance",
    "src/app/login",
    "src/components/ui",
    "src/components/charts",
    "src/features/dispatch",
    "src/features/fleet",
    "src/features/crew",
    "src/lib/api",
    "src/store",
    "src/types",
    "src/styles",
    "public"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# ============================================================
# TASK 61 — Scaffold, package.json, tsconfig, globals.css
# ============================================================

pkg = {
  "name": "depot-dashboard",
  "version": "1.0.0",
  "private": True,
  "scripts": {
    "dev": "next dev --port 3001",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "14.2.3",
    "react": "^18",
    "react-dom": "^18",
    "@tanstack/react-query": "^5.0.0",
    "zustand": "^4.5.0",
    "recharts": "^2.12.0"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18"
  }
}
with open(os.path.join(base_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg, f, indent=2)

tsconfig = {
  "compilerOptions": {
    "lib": ["dom","dom.iterable","esnext"],
    "allowJs": True, "skipLibCheck": True, "strict": True,
    "noEmit": True, "esModuleInterop": True, "module": "esnext",
    "moduleResolution": "bundler", "resolveJsonModule": True,
    "isolatedModules": True, "jsx": "preserve", "incremental": True,
    "plugins": [{"name": "next"}],
    "paths": {"@/*": ["./src/*"]}
  },
  "include": ["next-env.d.ts","**/*.ts","**/*.tsx",".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
with open(os.path.join(base_dir, "tsconfig.json"), "w", encoding="utf-8") as f:
    json.dump(tsconfig, f, indent=2)

next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {};
export default nextConfig;
"""
with open(os.path.join(base_dir, "next.config.mjs"), "w", encoding="utf-8") as f: f.write(next_config)

# Global CSS — Depot theme: dark navy sidebar, clean whites
globals_css = """:root {
  --depot-primary: hsl(215, 90%, 32%);
  --depot-accent:  hsl(38, 100%, 50%);
  --depot-bg:      hsl(220, 20%, 97%);
  --depot-surface: hsl(0, 0%, 100%);
  --depot-sidebar: hsl(220, 40%, 14%);
  --depot-text:    hsl(220, 20%, 18%);
  --depot-muted:   hsl(220, 10%, 52%);
  --depot-success: hsl(142, 60%, 40%);
  --depot-warn:    hsl(38, 100%, 48%);
  --depot-danger:  hsl(4, 80%, 52%);
  --radius: 10px;
  --shadow: 0 2px 12px rgba(0,0,0,0.07);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--depot-bg);
  color: var(--depot-text);
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 240px;
  background: var(--depot-sidebar);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 0;
  position: fixed;
  top: 0; left: 0; bottom: 0;
  z-index: 100;
}
.sidebar-logo {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.sidebar-logo .brand { font-size: 1.3rem; font-weight: 900; color: #fff; letter-spacing: 1px; }
.sidebar-logo .depot-name { font-size: 0.75rem; color: rgba(255,255,255,0.5); margin-top: 2px; }
.sidebar-nav { flex: 1; padding: 1rem 0; }
.nav-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.7rem 1.5rem;
  color: rgba(255,255,255,0.65);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.15s;
  border-left: 3px solid transparent;
}
.nav-item:hover, .nav-item.active {
  background: rgba(255,255,255,0.07);
  color: #fff;
  border-left-color: var(--depot-accent);
}
.nav-icon { font-size: 1.1rem; width: 20px; text-align: center; }

/* Main content */
.main-content { margin-left: 240px; flex: 1; padding: 2rem; }
.page-header { margin-bottom: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 800; color: var(--depot-text); }
.page-subtitle { color: var(--depot-muted); font-size: 0.9rem; margin-top: 2px; }

/* KPI Cards */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.kpi-card {
  background: var(--depot-surface);
  border-radius: var(--radius);
  padding: 1.25rem;
  box-shadow: var(--shadow);
}
.kpi-label { font-size: 0.8rem; font-weight: 600; color: var(--depot-muted); text-transform: uppercase; letter-spacing: 0.5px; }
.kpi-value { font-size: 2rem; font-weight: 900; color: var(--depot-text); margin-top: 4px; }
.kpi-delta { font-size: 0.8rem; margin-top: 4px; }
.kpi-delta.up { color: var(--depot-success); }
.kpi-delta.down { color: var(--depot-danger); }

/* Cards & Tables */
.card {
  background: var(--depot-surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.25rem;
  margin-bottom: 1.25rem;
}
.card-title { font-size: 1rem; font-weight: 700; margin-bottom: 1rem; color: var(--depot-text); }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }

table { width: 100%; border-collapse: collapse; }
th { background: var(--depot-bg); font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--depot-muted); padding: 0.6rem 0.8rem; text-align: left; }
td { padding: 0.75rem 0.8rem; border-bottom: 1px solid var(--depot-bg); font-size: 0.88rem; vertical-align: middle; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: hsl(215, 90%, 97%); }

/* Badges */
.badge { display: inline-block; padding: 0.2rem 0.55rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }
.badge-success { background: hsl(142,60%,92%); color: var(--depot-success); }
.badge-warn    { background: hsl(38,100%,92%); color: var(--depot-warn); }
.badge-danger  { background: hsl(4,80%,94%);   color: var(--depot-danger); }
.badge-info    { background: hsl(215,90%,92%);  color: var(--depot-primary); }
.badge-neutral { background: hsl(0,0%,92%);     color: #555; }

/* Buttons */
.btn { padding: 0.5rem 1rem; border-radius: 6px; border: none; cursor: pointer; font-size: 0.85rem; font-weight: 600; transition: all 0.15s; }
.btn-primary { background: var(--depot-primary); color: #fff; }
.btn-primary:hover { background: hsl(215,90%,26%); transform: translateY(-1px); }
.btn-sm { padding: 0.3rem 0.7rem; font-size: 0.78rem; }

/* Search & Filters */
.toolbar { display: flex; gap: 0.75rem; margin-bottom: 1rem; align-items: center; flex-wrap: wrap; }
.search-input { padding: 0.5rem 0.85rem; border: 1px solid #ddd; border-radius: 6px; font-size: 0.88rem; min-width: 220px; outline: none; }
.search-input:focus { border-color: var(--depot-primary); }
select.filter { padding: 0.5rem 0.85rem; border: 1px solid #ddd; border-radius: 6px; font-size: 0.88rem; background: #fff; cursor: pointer; }

/* Status dots */
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 6px; }
.dot-green { background: var(--depot-success); }
.dot-orange { background: var(--depot-warn); }
.dot-red { background: var(--depot-danger); }
.dot-grey { background: #ccc; }

/* Progress bar */
.progress-bar { height: 6px; background: #eee; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 3px; background: var(--depot-primary); transition: width 0.3s; }
"""
with open(os.path.join(base_dir, "src/styles/depot.css"), "w", encoding="utf-8") as f: f.write(globals_css)

# Types
types_ts = """export interface Bus {
  id: string; busNumber: string; type: string;
  status: 'OPERATIONAL' | 'IN_MAINTENANCE' | 'BREAKDOWN' | 'IDLE';
  driver?: string; conductor?: string; route?: string;
  lastService: string; nextServiceDue: string; kmToday: number;
  fuelLevel: number;
}

export interface TripEntry {
  tripId: string; route: string; busNumber: string;
  departure: string; arrival: string;
  status: 'ON_TIME' | 'DELAYED' | 'DEPARTED' | 'ARRIVED' | 'CANCELLED';
  passengerCount: number; capacity: number;
}

export interface CrewMember {
  id: string; name: string; role: 'DRIVER' | 'CONDUCTOR';
  employeeId: string; phone: string; shift: string;
  status: 'ON_DUTY' | 'OFF_DUTY' | 'LEAVE' | 'AVAILABLE';
  assignedBus?: string; assignedRoute?: string;
}

export interface MaintenanceJob {
  id: string; busNumber: string; type: string;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  status: 'OPEN' | 'IN_PROGRESS' | 'COMPLETED';
  mechanic?: string; openedAt: string; estimatedCompletion: string;
}

export interface SparePart {
  id: string; name: string; partNumber: string;
  stock: number; minStock: number; unit: string; unitPrice: number;
}
"""
with open(os.path.join(base_dir, "src/types/index.ts"), "w", encoding="utf-8") as f: f.write(types_ts)

# Sidebar component
sidebar_tsx = """'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const NAV_ITEMS = [
  { href: '/dashboard', icon: '📊', label: 'Dashboard' },
  { href: '/dispatch', icon: '🚌', label: 'Dispatch Board' },
  { href: '/fleet', icon: '🚍', label: 'Fleet Status' },
  { href: '/crew', icon: '👥', label: 'Crew Roster' },
  { href: '/maintenance', icon: '🔧', label: 'Maintenance' },
  { href: '/operations', icon: '🗺️', label: 'Live Operations' },
  { href: '/inventory', icon: '📦', label: 'Inventory' },
  { href: '/finance', icon: '💰', label: 'Finance' },
  { href: '/compliance', icon: '📋', label: 'Compliance' },
];

export function Sidebar() {
  const path = usePathname();
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="brand">MSRTC</div>
        <div className="depot-name">Mumbai Central Depot</div>
      </div>
      <nav className="sidebar-nav">
        {NAV_ITEMS.map(item => (
          <Link key={item.href} href={item.href} className={`nav-item ${path.startsWith(item.href) ? 'active' : ''}`}>
            <span className="nav-icon">{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>
      <div style={{ padding: '1rem 1.5rem', borderTop: '1px solid rgba(255,255,255,0.08)' }}>
        <div style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.4)' }}>Depot Manager</div>
        <div style={{ fontSize: '0.85rem', color: '#fff', marginTop: '2px', fontWeight: '600' }}>Ramesh Pawar</div>
      </div>
    </aside>
  );
}
"""
with open(os.path.join(base_dir, "src/components/ui/Sidebar.tsx"), "w", encoding="utf-8") as f: f.write(sidebar_tsx)

# Root Layout
layout_tsx = """import '@/styles/depot.css';
import { Sidebar } from '@/components/ui/Sidebar';

export const metadata = {
  title: 'MSRTC Depot Dashboard',
  description: 'Fleet operations and management for Mumbai Central Depot',
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

# Root redirect
root_page = """import { redirect } from 'next/navigation';
export default function Root() { redirect('/dashboard'); }
"""
with open(os.path.join(base_dir, "src/app/page.tsx"), "w", encoding="utf-8") as f: f.write(root_page)

# ============================================================
# TASK 62 — DASHBOARD (KPI overview)
# ============================================================
dashboard_page = """export default function DashboardPage() {
  const kpis = [
    { label: 'Fleet Active', value: '47', delta: '+3 from yesterday', dir: 'up' },
    { label: 'In Maintenance', value: '8', delta: '-2 resolved today', dir: 'up' },
    { label: "Today's Revenue", value: '₹4.2L', delta: '+8% vs last week', dir: 'up' },
    { label: 'On-Time Departures', value: '91%', delta: '-2% from target', dir: 'down' },
  ];

  const recentTrips = [
    { id: 'T-101', route: 'Mumbai → Pune', bus: 'MH-01-AB-1234', dep: '07:30', status: 'DEPARTED', pax: 42 },
    { id: 'T-102', route: 'Mumbai → Nashik', bus: 'MH-01-CD-5678', dep: '08:00', status: 'ON_TIME', pax: 38 },
    { id: 'T-103', route: 'Mumbai → Aurangabad', bus: 'MH-01-EF-9012', dep: '08:30', status: 'DELAYED', pax: 51 },
    { id: 'T-104', route: 'Mumbai → Kolhapur', bus: 'MH-01-GH-3456', dep: '09:00', status: 'ON_TIME', pax: 29 },
  ];

  const statusBadge = (s: string) => {
    const map: Record<string, string> = {
      DEPARTED: 'badge-info', ON_TIME: 'badge-success', DELAYED: 'badge-warn', CANCELLED: 'badge-danger'
    };
    return map[s] || 'badge-neutral';
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Depot Dashboard</h1>
        <p className="page-subtitle">Mumbai Central Depot · {new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
      </div>

      <div className="kpi-grid">
        {kpis.map(k => (
          <div key={k.label} className="kpi-card">
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value">{k.value}</div>
            <div className={`kpi-delta ${k.dir}`}>{k.delta}</div>
          </div>
        ))}
      </div>

      <div className="two-col">
        <div className="card">
          <div className="card-title">Today's Departures</div>
          <table>
            <thead><tr><th>Trip</th><th>Route</th><th>Bus</th><th>Dep</th><th>Pax</th><th>Status</th></tr></thead>
            <tbody>
              {recentTrips.map(t => (
                <tr key={t.id}>
                  <td style={{ fontWeight: 700 }}>{t.id}</td>
                  <td>{t.route}</td>
                  <td style={{ fontFamily: 'monospace' }}>{t.bus}</td>
                  <td>{t.dep}</td>
                  <td>{t.pax}</td>
                  <td><span className={`badge ${statusBadge(t.status)}`}>{t.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card">
          <div className="card-title">Fleet Health Snapshot</div>
          {[
            { label: 'Operational', val: 47, total: 62, color: 'var(--depot-success)' },
            { label: 'In Maintenance', val: 8, total: 62, color: 'var(--depot-warn)' },
            { label: 'Breakdown', val: 4, total: 62, color: 'var(--depot-danger)' },
            { label: 'Idle / Reserve', val: 3, total: 62, color: '#ccc' },
          ].map(b => (
            <div key={b.label} style={{ marginBottom: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--depot-muted)' }}>{b.label}</span>
                <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>{b.val}/{b.total}</span>
              </div>
              <div className="progress-bar"><div className="progress-fill" style={{ width: `${(b.val/b.total*100).toFixed(0)}%`, background: b.color }} /></div>
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
# TASK 62 — DISPATCH BOARD
# ============================================================
dispatch_page = """"use client";
import { useState } from 'react';

const TRIPS = [
  { id: 'T-101', route: 'Mumbai → Pune', bus: 'MH-01-AB-1234', platform: 'P-3', dep: '07:30', status: 'DEPARTED', pax: 42, cap: 52, driver: 'Rajesh Kumar', conductor: 'Anil Patil' },
  { id: 'T-102', route: 'Mumbai → Nashik', bus: 'MH-01-CD-5678', platform: 'P-7', dep: '08:00', status: 'ON_TIME', pax: 38, cap: 52, driver: 'Suresh More', conductor: 'Dinesh Jadhav' },
  { id: 'T-103', route: 'Mumbai → Aurangabad', bus: 'MH-01-EF-9012', platform: 'P-1', dep: '08:30', status: 'DELAYED', pax: 51, cap: 52, driver: 'Manoj Desai', conductor: 'Priya Nair' },
  { id: 'T-104', route: 'Mumbai → Kolhapur', bus: 'MH-01-GH-3456', platform: 'P-5', dep: '09:00', status: 'ON_TIME', pax: 29, cap: 40, driver: 'Vijay Shinde', conductor: 'Suman Deshpande' },
  { id: 'T-105', route: 'Mumbai → Solapur', bus: 'MH-01-IJ-7890', platform: 'P-2', dep: '09:30', status: 'ON_TIME', pax: 44, cap: 52, driver: 'Ramesh Pawar', conductor: 'Kavita Mali' },
  { id: 'T-106', route: 'Mumbai → Nagpur', bus: 'MH-01-KL-1122', platform: 'P-9', dep: '10:00', status: 'CANCELLED', pax: 0, cap: 52, driver: '—', conductor: '—' },
];

const BADGE: Record<string, string> = { ON_TIME: 'badge-success', DEPARTED: 'badge-info', DELAYED: 'badge-warn', CANCELLED: 'badge-danger', ARRIVED: 'badge-neutral' };

export default function DispatchPage() {
  const [filter, setFilter] = useState('ALL');

  const filtered = filter === 'ALL' ? TRIPS : TRIPS.filter(t => t.status === filter);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Dispatch Board</h1>
        <p className="page-subtitle">Live departure management · Mumbai Central Depot</p>
      </div>

      <div className="card">
        <div className="toolbar">
          <span style={{ fontWeight: 700, fontSize: '0.95rem' }}>Filter:</span>
          {['ALL','ON_TIME','DELAYED','DEPARTED','CANCELLED'].map(s => (
            <button key={s} className={`btn btn-sm ${filter === s ? 'btn-primary' : ''}`} style={{ background: filter === s ? 'var(--depot-primary)' : '#eee', color: filter === s ? '#fff' : '#555' }} onClick={() => setFilter(s)}>{s.replace('_',' ')}</button>
          ))}
        </div>
        <table>
          <thead><tr><th>Trip ID</th><th>Route</th><th>Bus</th><th>Platform</th><th>Departure</th><th>Pax</th><th>Driver</th><th>Conductor</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            {filtered.map(t => (
              <tr key={t.id}>
                <td style={{ fontWeight: 700 }}>{t.id}</td>
                <td>{t.route}</td>
                <td style={{ fontFamily: 'monospace', fontSize: '0.82rem' }}>{t.bus}</td>
                <td style={{ fontWeight: 700, color: 'var(--depot-primary)' }}>{t.platform}</td>
                <td>{t.dep}</td>
                <td><span style={{ color: t.pax / t.cap > 0.9 ? 'var(--depot-danger)' : 'inherit' }}>{t.pax}/{t.cap}</span></td>
                <td style={{ fontSize: '0.83rem' }}>{t.driver}</td>
                <td style={{ fontSize: '0.83rem' }}>{t.conductor}</td>
                <td><span className={`badge ${BADGE[t.status] || 'badge-neutral'}`}>{t.status}</span></td>
                <td><button className="btn btn-sm btn-primary" style={{ opacity: t.status === 'CANCELLED' ? 0.4 : 1 }}>Manage</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/dispatch/page.tsx"), "w", encoding="utf-8") as f: f.write(dispatch_page)

# ============================================================
# TASK 63 — FLEET MANAGEMENT
# ============================================================
fleet_page = """"use client";
import { useState } from 'react';

const FLEET = [
  { id: 'B01', busNumber: 'MH-01-AB-1234', type: 'Shivneri AC', status: 'OPERATIONAL', driver: 'Rajesh Kumar', route: 'Mumbai-Pune', kmToday: 312, fuelLevel: 78, lastService: '2026-06-01', nextServiceDue: '2026-09-01' },
  { id: 'B02', busNumber: 'MH-01-CD-5678', type: 'Shivshahi', status: 'OPERATIONAL', driver: 'Suresh More', route: 'Mumbai-Nashik', kmToday: 187, fuelLevel: 55, lastService: '2026-05-15', nextServiceDue: '2026-08-15' },
  { id: 'B03', busNumber: 'MH-01-EF-9012', type: 'Ordinary', status: 'IN_MAINTENANCE', driver: '—', route: '—', kmToday: 0, fuelLevel: 30, lastService: '2026-04-20', nextServiceDue: '2026-07-20' },
  { id: 'B04', busNumber: 'MH-01-GH-3456', type: 'Hirkani', status: 'OPERATIONAL', driver: 'Vijay Shinde', route: 'Mumbai-Kolhapur', kmToday: 410, fuelLevel: 62, lastService: '2026-06-10', nextServiceDue: '2026-09-10' },
  { id: 'B05', busNumber: 'MH-01-IJ-7890', type: 'Shivneri AC', status: 'BREAKDOWN', driver: '—', route: '—', kmToday: 45, fuelLevel: 20, lastService: '2026-05-01', nextServiceDue: '2026-08-01' },
  { id: 'B06', busNumber: 'MH-01-KL-1122', type: 'Ordinary', status: 'IDLE', driver: '—', route: '—', kmToday: 0, fuelLevel: 90, lastService: '2026-06-20', nextServiceDue: '2026-09-20' },
];

const SBADGE: Record<string, string> = { OPERATIONAL: 'badge-success', IN_MAINTENANCE: 'badge-warn', BREAKDOWN: 'badge-danger', IDLE: 'badge-neutral' };

export default function FleetPage() {
  const [search, setSearch] = useState('');
  const filtered = FLEET.filter(b => b.busNumber.toLowerCase().includes(search.toLowerCase()) || b.type.toLowerCase().includes(search.toLowerCase()));
  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Fleet Management</h1>
        <p className="page-subtitle">62 buses registered · Mumbai Central Depot</p>
      </div>

      <div className="kpi-grid">
        {[{ label:'Operational',val:'47',c:'var(--depot-success)'},{label:'In Maintenance',val:'8',c:'var(--depot-warn)'},{label:'Breakdown',val:'4',c:'var(--depot-danger)'},{label:'Idle/Reserve',val:'3',c:'var(--depot-muted)'}].map(k => (
          <div key={k.label} className="kpi-card" style={{ borderTop: `3px solid ${k.c}` }}>
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value" style={{ color: k.c }}>{k.val}</div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="toolbar">
          <input className="search-input" placeholder="Search bus number or type..." value={search} onChange={e => setSearch(e.target.value)} />
          <button className="btn btn-primary">+ Add Bus</button>
        </div>
        <table>
          <thead><tr><th>Bus Number</th><th>Type</th><th>Status</th><th>Driver</th><th>Route</th><th>KM Today</th><th>Fuel %</th><th>Next Service</th><th>Action</th></tr></thead>
          <tbody>
            {filtered.map(b => (
              <tr key={b.id}>
                <td style={{ fontWeight: 700, fontFamily: 'monospace' }}>{b.busNumber}</td>
                <td>{b.type}</td>
                <td><span className={`badge ${SBADGE[b.status]}`}>{b.status.replace('_',' ')}</span></td>
                <td style={{ fontSize: '0.83rem' }}>{b.driver}</td>
                <td style={{ fontSize: '0.83rem' }}>{b.route}</td>
                <td>{b.kmToday} km</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <div className="progress-bar" style={{ width: 60 }}><div className="progress-fill" style={{ width: `${b.fuelLevel}%`, background: b.fuelLevel < 25 ? 'var(--depot-danger)' : 'var(--depot-primary)' }} /></div>
                    <span style={{ fontSize: '0.8rem' }}>{b.fuelLevel}%</span>
                  </div>
                </td>
                <td style={{ fontSize: '0.82rem', color: new Date(b.nextServiceDue) < new Date() ? 'var(--depot-danger)' : 'inherit', fontWeight: new Date(b.nextServiceDue) < new Date() ? 700 : 400 }}>{b.nextServiceDue}</td>
                <td><button className="btn btn-sm btn-primary">Details</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/fleet/page.tsx"), "w", encoding="utf-8") as f: f.write(fleet_page)

# ============================================================
# TASK 64 — CREW ASSIGNMENT
# ============================================================
crew_page = """"use client";
import { useState } from 'react';

const CREW = [
  { id:'C01', name:'Rajesh Kumar', role:'DRIVER', employeeId:'EMP-1001', phone:'9876500001', shift:'Morning', status:'ON_DUTY', assignedBus:'MH-01-AB-1234', assignedRoute:'Mumbai-Pune' },
  { id:'C02', name:'Anil Patil', role:'CONDUCTOR', employeeId:'EMP-2001', phone:'9876500002', shift:'Morning', status:'ON_DUTY', assignedBus:'MH-01-AB-1234', assignedRoute:'Mumbai-Pune' },
  { id:'C03', name:'Suresh More', role:'DRIVER', employeeId:'EMP-1002', phone:'9876500003', shift:'Morning', status:'ON_DUTY', assignedBus:'MH-01-CD-5678', assignedRoute:'Mumbai-Nashik' },
  { id:'C04', name:'Priya Nair', role:'CONDUCTOR', employeeId:'EMP-2002', phone:'9876500004', shift:'Afternoon', status:'AVAILABLE', assignedBus:'', assignedRoute:'' },
  { id:'C05', name:'Vijay Shinde', role:'DRIVER', employeeId:'EMP-1003', phone:'9876500005', shift:'Night', status:'OFF_DUTY', assignedBus:'', assignedRoute:'' },
  { id:'C06', name:'Kavita Mali', role:'CONDUCTOR', employeeId:'EMP-2003', phone:'9876500006', shift:'Morning', status:'LEAVE', assignedBus:'', assignedRoute:'' },
];

const SBADGE: Record<string,string> = { ON_DUTY:'badge-success', AVAILABLE:'badge-info', OFF_DUTY:'badge-neutral', LEAVE:'badge-warn' };

export default function CrewPage() {
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('ALL');
  const filtered = CREW.filter(c =>
    (filter === 'ALL' || c.status === filter) &&
    (c.name.toLowerCase().includes(search.toLowerCase()) || c.employeeId.includes(search))
  );
  const available = CREW.filter(c => c.status === 'AVAILABLE').length;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Crew Roster</h1>
        <p className="page-subtitle">{CREW.length} staff registered · {available} available for assignment</p>
      </div>

      <div className="kpi-grid">
        {[{label:'On Duty',val:CREW.filter(c=>c.status==='ON_DUTY').length,c:'var(--depot-success)'},
          {label:'Available',val:CREW.filter(c=>c.status==='AVAILABLE').length,c:'var(--depot-primary)'},
          {label:'Off Duty',val:CREW.filter(c=>c.status==='OFF_DUTY').length,c:'var(--depot-muted)'},
          {label:'On Leave',val:CREW.filter(c=>c.status==='LEAVE').length,c:'var(--depot-warn)'}].map(k=>(
          <div key={k.label} className="kpi-card" style={{borderTop:`3px solid ${k.c}`}}>
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value" style={{color:k.c}}>{k.val}</div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="toolbar">
          <input className="search-input" placeholder="Search name or employee ID..." value={search} onChange={e=>setSearch(e.target.value)} />
          <select className="filter" value={filter} onChange={e=>setFilter(e.target.value)}>
            <option value="ALL">All Status</option>
            <option value="ON_DUTY">On Duty</option>
            <option value="AVAILABLE">Available</option>
            <option value="OFF_DUTY">Off Duty</option>
            <option value="LEAVE">On Leave</option>
          </select>
          <button className="btn btn-primary">+ Add Staff</button>
        </div>
        <table>
          <thead><tr><th>Name</th><th>Employee ID</th><th>Role</th><th>Shift</th><th>Status</th><th>Assigned Bus</th><th>Route</th><th>Action</th></tr></thead>
          <tbody>
            {filtered.map(c => (
              <tr key={c.id}>
                <td style={{fontWeight:700}}>{c.name}</td>
                <td style={{fontFamily:'monospace',fontSize:'0.82rem'}}>{c.employeeId}</td>
                <td><span className={`badge ${c.role==='DRIVER'?'badge-info':'badge-neutral'}`}>{c.role}</span></td>
                <td>{c.shift}</td>
                <td><span className={`badge ${SBADGE[c.status]}`}>{c.status.replace('_',' ')}</span></td>
                <td style={{fontFamily:'monospace',fontSize:'0.82rem'}}>{c.assignedBus || '—'}</td>
                <td style={{fontSize:'0.82rem'}}>{c.assignedRoute || '—'}</td>
                <td><button className="btn btn-sm btn-primary" disabled={c.status!=='AVAILABLE'} style={{opacity:c.status!=='AVAILABLE'?0.4:1}}>Assign</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/crew/page.tsx"), "w", encoding="utf-8") as f: f.write(crew_page)

# ============================================================
# TASK 65 — MAINTENANCE INTEGRATION
# ============================================================
maintenance_page = """"use client";
import { useState } from 'react';

const JOBS = [
  { id:'JOB-001', busNumber:'MH-01-EF-9012', type:'Engine Overhaul', priority:'HIGH', status:'IN_PROGRESS', mechanic:'Ganesh Kamble', openedAt:'2026-07-01', estimatedCompletion:'2026-07-07', notes:'Cylinder head replacement required' },
  { id:'JOB-002', busNumber:'MH-01-IJ-7890', type:'Brake System Failure', priority:'HIGH', status:'OPEN', mechanic:'', openedAt:'2026-07-05', estimatedCompletion:'2026-07-06', notes:'Brake fluid leak, urgent fix required' },
  { id:'JOB-003', busNumber:'MH-01-MN-4567', type:'AC Service', priority:'MEDIUM', status:'COMPLETED', mechanic:'Ramesh Kale', openedAt:'2026-07-03', estimatedCompletion:'2026-07-04', notes:'Filter cleaned and refrigerant topped' },
  { id:'JOB-004', busNumber:'MH-01-OP-8901', type:'Tyre Replacement', priority:'LOW', status:'OPEN', mechanic:'', openedAt:'2026-07-05', estimatedCompletion:'2026-07-06', notes:'Front two tyres worn beyond limit' },
  { id:'JOB-005', busNumber:'MH-01-QR-2345', type:'Scheduled 10,000 km Service', priority:'MEDIUM', status:'IN_PROGRESS', mechanic:'Sunil More', openedAt:'2026-07-04', estimatedCompletion:'2026-07-05', notes:'Oil change, filter replacement' },
];

const PBADGE: Record<string,string> = { HIGH:'badge-danger', MEDIUM:'badge-warn', LOW:'badge-info' };
const SBADGE: Record<string,string> = { OPEN:'badge-warn', IN_PROGRESS:'badge-info', COMPLETED:'badge-success' };

export default function MaintenancePage() {
  const [filter, setFilter] = useState('ALL');
  const filtered = filter === 'ALL' ? JOBS : JOBS.filter(j => j.status === filter);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Maintenance</h1>
        <p className="page-subtitle">Active job cards and service tracking</p>
      </div>

      <div className="kpi-grid">
        {[{label:'Open Jobs',val:JOBS.filter(j=>j.status==='OPEN').length,c:'var(--depot-warn)'},
          {label:'In Progress',val:JOBS.filter(j=>j.status==='IN_PROGRESS').length,c:'var(--depot-primary)'},
          {label:'Completed Today',val:JOBS.filter(j=>j.status==='COMPLETED').length,c:'var(--depot-success)'},
          {label:'High Priority',val:JOBS.filter(j=>j.priority==='HIGH').length,c:'var(--depot-danger)'}].map(k=>(
          <div key={k.label} className="kpi-card" style={{borderTop:`3px solid ${k.c}`}}>
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value" style={{color:k.c}}>{k.val}</div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="toolbar">
          {['ALL','OPEN','IN_PROGRESS','COMPLETED'].map(s=>(
            <button key={s} className="btn btn-sm" style={{background:filter===s?'var(--depot-primary)':'#eee',color:filter===s?'#fff':'#555'}} onClick={()=>setFilter(s)}>{s.replace('_',' ')}</button>
          ))}
          <button className="btn btn-primary" style={{marginLeft:'auto'}}>+ New Job Card</button>
        </div>
        <table>
          <thead><tr><th>Job ID</th><th>Bus</th><th>Type</th><th>Priority</th><th>Status</th><th>Mechanic</th><th>Opened</th><th>ETA</th><th>Notes</th></tr></thead>
          <tbody>
            {filtered.map(j=>(
              <tr key={j.id}>
                <td style={{fontWeight:700}}>{j.id}</td>
                <td style={{fontFamily:'monospace',fontSize:'0.82rem'}}>{j.busNumber}</td>
                <td>{j.type}</td>
                <td><span className={`badge ${PBADGE[j.priority]}`}>{j.priority}</span></td>
                <td><span className={`badge ${SBADGE[j.status]}`}>{j.status.replace('_',' ')}</span></td>
                <td style={{fontSize:'0.83rem'}}>{j.mechanic || <span style={{color:'var(--depot-warn)'}}>Unassigned</span>}</td>
                <td style={{fontSize:'0.82rem'}}>{j.openedAt}</td>
                <td style={{fontSize:'0.82rem',color:new Date(j.estimatedCompletion)<new Date()?'var(--depot-danger)':'inherit'}}>{j.estimatedCompletion}</td>
                <td style={{fontSize:'0.8rem',color:'var(--depot-muted)',maxWidth:160}} title={j.notes}>{j.notes.slice(0,40)}…</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/maintenance/page.tsx"), "w", encoding="utf-8") as f: f.write(maintenance_page)

# ============================================================
# TASK 66 — LIVE OPERATIONS (Map placeholder)
# ============================================================
ops_page = """export default function OperationsPage() {
  const buses = [
    { id:'B01', bus:'MH-01-AB-1234', route:'Mumbai → Pune', driver:'Rajesh Kumar', lat:18.9200, lng:73.1100, speed:72, status:'ON_TIME', lastUpdate:'30s ago' },
    { id:'B02', bus:'MH-01-CD-5678', route:'Mumbai → Nashik', driver:'Suresh More', lat:19.6500, lng:73.7600, speed:65, status:'DELAYED', lastUpdate:'45s ago' },
    { id:'B03', bus:'MH-01-GH-3456', route:'Mumbai → Kolhapur', driver:'Vijay Shinde', lat:17.6800, lng:74.2400, speed:58, status:'ON_TIME', lastUpdate:'20s ago' },
  ];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Live Operations</h1>
        <p className="page-subtitle">Real-time fleet tracking · {buses.length} active buses</p>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'1fr 380px',gap:'1.25rem'}}>
        <div className="card" style={{minHeight:480,display:'flex',alignItems:'center',justifyContent:'center',background:'linear-gradient(135deg,hsl(215,60%,12%),hsl(215,40%,20%))',borderRadius:10}}>
          <div style={{textAlign:'center',color:'rgba(255,255,255,0.7)'}}>
            <div style={{fontSize:48,marginBottom:12}}>🗺️</div>
            <div style={{fontSize:'1rem',fontWeight:700,color:'#fff'}}>Maharashtra Fleet Map</div>
            <div style={{fontSize:'0.85rem',marginTop:6}}>Leaflet/Mapbox integration</div>
            <div style={{marginTop:16,display:'flex',gap:8,justifyContent:'center',flexWrap:'wrap'}}>
              {buses.map(b=>(
                <div key={b.id} style={{background:'rgba(255,255,255,0.12)',borderRadius:6,padding:'6px 12px',fontSize:'0.78rem',fontWeight:600,color:'#fff'}}>
                  📍 {b.bus}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div>
          <div className="card-title" style={{marginBottom:12}}>Active Buses</div>
          {buses.map(b=>(
            <div key={b.id} className="card" style={{marginBottom:12,borderLeft:`4px solid ${b.status==='ON_TIME'?'var(--depot-success)':'var(--depot-warn)'}`}}>
              <div style={{display:'flex',justifyContent:'space-between',marginBottom:6}}>
                <span style={{fontWeight:700,fontFamily:'monospace',fontSize:'0.85rem'}}>{b.bus}</span>
                <span className={`badge ${b.status==='ON_TIME'?'badge-success':'badge-warn'}`}>{b.status.replace('_',' ')}</span>
              </div>
              <div style={{fontSize:'0.83rem',color:'var(--depot-muted)',marginBottom:4}}>{b.route}</div>
              <div style={{fontSize:'0.8rem',color:'var(--depot-muted)'}}>Driver: {b.driver} · {b.speed} km/h</div>
              <div style={{fontSize:'0.78rem',color:'#aaa',marginTop:4}}>Updated {b.lastUpdate}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/operations/page.tsx"), "w", encoding="utf-8") as f: f.write(ops_page)

# ============================================================
# TASK 67 — INVENTORY & SPARE PARTS
# ============================================================
inventory_page = """"use client";
import { useState } from 'react';

const PARTS = [
  { id:'P001', name:'Engine Oil Filter', partNumber:'EF-4501', stock:48, minStock:20, unit:'pcs', unitPrice:320 },
  { id:'P002', name:'Brake Pad Set', partNumber:'BP-2200', stock:12, minStock:15, unit:'sets', unitPrice:1800 },
  { id:'P003', name:'AC Refrigerant R134a', partNumber:'AC-R134', stock:8, minStock:10, unit:'cans', unitPrice:650 },
  { id:'P004', name:'Windshield Wiper Blade', partNumber:'WW-550', stock:35, minStock:20, unit:'pcs', unitPrice:180 },
  { id:'P005', name:'Bus Tyre 11R22.5', partNumber:'TY-1122', stock:6, minStock:10, unit:'pcs', unitPrice:12500 },
  { id:'P006', name:'Headlight Bulb 24V', partNumber:'HL-24V', stock:22, minStock:10, unit:'pcs', unitPrice:290 },
];

export default function InventoryPage() {
  const [search, setSearch] = useState('');
  const filtered = PARTS.filter(p => p.name.toLowerCase().includes(search.toLowerCase()) || p.partNumber.includes(search));
  const lowStock = PARTS.filter(p => p.stock < p.minStock).length;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Inventory & Spare Parts</h1>
        <p className="page-subtitle">{PARTS.length} SKUs · {lowStock} items below minimum stock</p>
      </div>

      {lowStock > 0 && (
        <div style={{background:'hsl(38,100%,94%)',border:'1px solid hsl(38,100%,75%)',borderRadius:8,padding:'0.75rem 1rem',marginBottom:'1.25rem',display:'flex',gap:8,alignItems:'center'}}>
          <span>⚠️</span>
          <span style={{fontWeight:600,color:'hsl(38,100%,30%)'}}>{lowStock} item(s) below minimum stock level. Raise purchase orders.</span>
        </div>
      )}

      <div className="card">
        <div className="toolbar">
          <input className="search-input" placeholder="Search part name or number..." value={search} onChange={e=>setSearch(e.target.value)} />
          <button className="btn btn-primary">+ Raise PO</button>
        </div>
        <table>
          <thead><tr><th>Part Name</th><th>Part No.</th><th>Stock</th><th>Min Stock</th><th>Unit</th><th>Unit Price</th><th>Stock Value</th><th>Status</th></tr></thead>
          <tbody>
            {filtered.map(p=>(
              <tr key={p.id}>
                <td style={{fontWeight:600}}>{p.name}</td>
                <td style={{fontFamily:'monospace',fontSize:'0.82rem'}}>{p.partNumber}</td>
                <td style={{fontWeight:700,color:p.stock<p.minStock?'var(--depot-danger)':'var(--depot-success)'}}>{p.stock}</td>
                <td style={{color:'var(--depot-muted)'}}>{p.minStock}</td>
                <td>{p.unit}</td>
                <td>₹{p.unitPrice.toLocaleString()}</td>
                <td>₹{(p.stock*p.unitPrice).toLocaleString()}</td>
                <td><span className={`badge ${p.stock<p.minStock?'badge-danger':'badge-success'}`}>{p.stock<p.minStock?'Low Stock':'Adequate'}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/inventory/page.tsx"), "w", encoding="utf-8") as f: f.write(inventory_page)

# ============================================================
# TASK 68 — FINANCE & REVENUE
# ============================================================
finance_page = """export default function FinancePage() {
  const weeklyRevenue = [
    { day: 'Mon', revenue: 185000, target: 200000 },
    { day: 'Tue', revenue: 212000, target: 200000 },
    { day: 'Wed', revenue: 198000, target: 200000 },
    { day: 'Thu', revenue: 225000, target: 200000 },
    { day: 'Fri', revenue: 241000, target: 200000 },
    { day: 'Sat', revenue: 310000, target: 250000 },
    { day: 'Sun', revenue: 295000, target: 250000 },
  ];

  const routes = [
    { route: 'Mumbai → Pune', trips: 12, revenue: 88400, pax: 496, load: 79 },
    { route: 'Mumbai → Nashik', trips: 8, revenue: 52800, pax: 312, load: 72 },
    { route: 'Mumbai → Aurangabad', trips: 6, revenue: 61200, pax: 228, load: 88 },
    { route: 'Mumbai → Kolhapur', trips: 4, revenue: 44800, pax: 168, load: 65 },
    { route: 'Mumbai → Solapur', trips: 5, revenue: 53500, pax: 210, load: 74 },
  ];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Finance & Revenue</h1>
        <p className="page-subtitle">Depot earnings and route profitability</p>
      </div>

      <div className="kpi-grid">
        {[{label:"Today's Revenue",val:'₹4,20,000',d:'+8%'},{label:'Weekly Revenue',val:'₹16,60,000',d:'+5%'},{label:'Avg Load Factor',val:'76%',d:'-2%'},{label:'Collection Efficiency',val:'98.4%',d:'+0.2%'}].map(k=>(
          <div key={k.label} className="kpi-card">
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value">{k.val}</div>
            <div className="kpi-delta up">{k.d} vs last week</div>
          </div>
        ))}
      </div>

      <div className="two-col">
        <div className="card">
          <div className="card-title">Weekly Revenue vs Target</div>
          <div style={{display:'flex',flexDirection:'column',gap:8}}>
            {weeklyRevenue.map(d=>(
              <div key={d.day}>
                <div style={{display:'flex',justifyContent:'space-between',marginBottom:3}}>
                  <span style={{fontSize:'0.82rem',fontWeight:600,width:30}}>{d.day}</span>
                  <span style={{fontSize:'0.82rem',color:'var(--depot-muted)'}}>₹{(d.revenue/1000).toFixed(0)}K / ₹{(d.target/1000).toFixed(0)}K</span>
                </div>
                <div className="progress-bar">
                  <div className="progress-fill" style={{width:`${Math.min(100,(d.revenue/d.target*100)).toFixed(0)}%`,background:d.revenue>=d.target?'var(--depot-success)':'var(--depot-warn)'}} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <div className="card-title">Route Revenue Breakdown</div>
          <table>
            <thead><tr><th>Route</th><th>Trips</th><th>Revenue</th><th>Load</th></tr></thead>
            <tbody>
              {routes.map(r=>(
                <tr key={r.route}>
                  <td style={{fontSize:'0.82rem'}}>{r.route}</td>
                  <td>{r.trips}</td>
                  <td style={{fontWeight:700}}>₹{r.revenue.toLocaleString()}</td>
                  <td><span className={`badge ${r.load>80?'badge-success':r.load>60?'badge-warn':'badge-danger'}`}>{r.load}%</span></td>
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
# TASK 69 — COMPLIANCE & DOCUMENTATION
# ============================================================
compliance_page = """"use client";
import { useState } from 'react';

const CERTS = [
  { id:'C01', busNumber:'MH-01-AB-1234', type:'Fitness Certificate', issueDate:'2025-07-01', expiryDate:'2026-07-01', status:'EXPIRING_SOON', authority:'RTO Mumbai' },
  { id:'C02', busNumber:'MH-01-CD-5678', type:'Permit Certificate', issueDate:'2025-06-15', expiryDate:'2027-06-15', status:'VALID', authority:'MSRTC HQ' },
  { id:'C03', busNumber:'MH-01-EF-9012', type:'Pollution Under Control', issueDate:'2026-01-10', expiryDate:'2026-07-10', status:'EXPIRED', authority:'MPCB' },
  { id:'C04', busNumber:'MH-01-GH-3456', type:'Insurance', issueDate:'2026-01-01', expiryDate:'2026-12-31', status:'VALID', authority:'National Insurance' },
  { id:'C05', busNumber:'MH-01-IJ-7890', type:'Fitness Certificate', issueDate:'2024-07-01', expiryDate:'2025-07-01', status:'EXPIRED', authority:'RTO Mumbai' },
];

const SBADGE: Record<string,string> = { VALID:'badge-success', EXPIRING_SOON:'badge-warn', EXPIRED:'badge-danger' };

export default function CompliancePage() {
  const expired = CERTS.filter(c=>c.status==='EXPIRED').length;
  const expiring = CERTS.filter(c=>c.status==='EXPIRING_SOON').length;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Compliance & Documentation</h1>
        <p className="page-subtitle">Certificates, permits and regulatory compliance</p>
      </div>

      {(expired > 0 || expiring > 0) && (
        <div style={{background:'hsl(4,80%,95%)',border:'1px solid hsl(4,80%,80%)',borderRadius:8,padding:'0.75rem 1rem',marginBottom:'1.25rem'}}>
          ⛔ <strong>{expired} expired</strong> and <strong>{expiring} expiring soon</strong> — Immediate action required to avoid regulatory penalties.
        </div>
      )}

      <div className="kpi-grid">
        {[{label:'Total Certificates',val:CERTS.length},{label:'Valid',val:CERTS.filter(c=>c.status==='VALID').length},{label:'Expiring (30 days)',val:expiring},{label:'Expired',val:expired}].map(k=>(
          <div key={k.label} className="kpi-card"><div className="kpi-label">{k.label}</div><div className="kpi-value">{k.val}</div></div>
        ))}
      </div>

      <div className="card">
        <div className="card-title">Certificate Registry</div>
        <table>
          <thead><tr><th>Bus</th><th>Certificate Type</th><th>Issued</th><th>Expiry</th><th>Authority</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            {CERTS.map(c=>(
              <tr key={c.id}>
                <td style={{fontFamily:'monospace',fontSize:'0.82rem'}}>{c.busNumber}</td>
                <td>{c.type}</td>
                <td style={{fontSize:'0.82rem'}}>{c.issueDate}</td>
                <td style={{fontSize:'0.82rem',fontWeight:c.status!=='VALID'?700:400,color:c.status==='EXPIRED'?'var(--depot-danger)':c.status==='EXPIRING_SOON'?'var(--depot-warn)':'inherit'}}>{c.expiryDate}</td>
                <td style={{fontSize:'0.82rem'}}>{c.authority}</td>
                <td><span className={`badge ${SBADGE[c.status]}`}>{c.status.replace('_',' ')}</span></td>
                <td><button className="btn btn-sm btn-primary">Renew</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/compliance/page.tsx"), "w", encoding="utf-8") as f: f.write(compliance_page)

print("Tasks 61-70: Depot Dashboard (Next.js) scaffolded successfully.")
