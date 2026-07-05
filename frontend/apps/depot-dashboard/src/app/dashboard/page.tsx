export default function DashboardPage() {
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
