'use client';
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
