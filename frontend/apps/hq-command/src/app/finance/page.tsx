export default function FinancePage() {
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
