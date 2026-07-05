export default function FinancePage() {
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
