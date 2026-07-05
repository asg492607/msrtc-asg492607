export default function DashboardPage() {
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
