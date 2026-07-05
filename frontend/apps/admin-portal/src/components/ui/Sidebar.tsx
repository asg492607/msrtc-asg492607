'use client';
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
