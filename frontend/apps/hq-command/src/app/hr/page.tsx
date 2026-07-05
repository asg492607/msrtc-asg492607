export default function HRPage() {
  const staffByCategory = [
    { role:'Drivers',total:12400,present:11820,onLeave:340,absent:240 },
    { role:'Conductors',total:11800,present:11210,onLeave:310,absent:280 },
    { role:'Mechanics',total:3200,present:3050,onLeave:90,absent:60 },
    { role:'Admin Staff',total:4600,present:4390,onLeave:140,absent:70 },
  ];

  const pendingItems = [
    { item:'Driving License Renewals Due', count: 142, urgency: 'HIGH' },
    { item:'Medical Fitness Certificates Expiring', count: 89, urgency: 'HIGH' },
    { item:'Uniform Allowance Pending', count: 2340, urgency: 'MEDIUM' },
    { item:'Provident Fund Disputes', count: 28, urgency: 'LOW' },
    { item:'Promotion Backlogs', count: 66, urgency: 'MEDIUM' },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Workforce Analytics</h1>
          <p className="page-subtitle">32,000 employees across Maharashtra</p>
        </div>
      </div>

      <div className="kpi-grid">
        {[{l:'Total Employees',v:'32,000',c:'blue'},{l:'Present Today',v:'30,470',c:'green'},{l:'On Leave',v:'880',c:'yellow'},{l:'Attrition Rate (YTD)',v:'2.4%',c:'red'}].map(k=>(
          <div key={k.l} className={`kpi-card ${k.c}`}><div className="kpi-label">{k.l}</div><div className="kpi-value">{k.v}</div></div>
        ))}
      </div>

      <div className="two-col">
        <div className="card">
          <div className="card-title">Attendance by Category</div>
          {staffByCategory.map(s => (
            <div key={s.role} style={{marginBottom:16}}>
              <div style={{display:'flex',justifyContent:'space-between',marginBottom:4}}>
                <span style={{fontWeight:700,fontSize:'0.85rem'}}>{s.role}</span>
                <span style={{fontSize:'0.78rem',color:'var(--hq-muted)'}}>{s.present.toLocaleString()}/{s.total.toLocaleString()} present</span>
              </div>
              <div className="progress-bar" style={{height:10}}>
                <div className="progress-fill" style={{width:`${(s.present/s.total*100).toFixed(0)}%`,background:'var(--hq-success)'}} />
              </div>
              <div style={{display:'flex',gap:12,marginTop:4,fontSize:'0.72rem',color:'var(--hq-muted)'}}>
                <span style={{color:'var(--hq-warn)'}}>On leave: {s.onLeave}</span>
                <span style={{color:'var(--hq-danger)'}}>Absent: {s.absent}</span>
              </div>
            </div>
          ))}
        </div>

        <div className="card">
          <div className="card-title">Pending HR Actions</div>
          {pendingItems.map(p => (
            <div key={p.item} style={{display:'flex',justifyContent:'space-between',alignItems:'center',paddingBottom:10,marginBottom:10,borderBottom:'1px solid var(--hq-border)'}}>
              <div>
                <div style={{fontSize:'0.83rem',fontWeight:600}}>{p.item}</div>
              </div>
              <div style={{display:'flex',gap:8,alignItems:'center'}}>
                <span style={{fontSize:'1rem',fontWeight:800,color:p.urgency==='HIGH'?'var(--hq-danger)':p.urgency==='MEDIUM'?'var(--hq-warn)':'var(--hq-muted)'}}>{p.count}</span>
                <span className={`badge ${p.urgency==='HIGH'?'badge-red':p.urgency==='MEDIUM'?'badge-yellow':'badge-muted'}`}>{p.urgency}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
