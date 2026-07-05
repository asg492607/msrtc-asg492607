export default function FleetPage() {
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
