export default function AdminDashboardPage() {
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
