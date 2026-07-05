'use client';
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
