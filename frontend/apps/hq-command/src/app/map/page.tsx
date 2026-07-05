export default function MapPage() {
  const heatspots = [
    { region: 'Mumbai Metropolitan', buses: 820, alerts: 2 },
    { region: 'Pune Division', buses: 640, alerts: 1 },
    { region: 'Nashik Division', buses: 420, alerts: 3 },
    { region: 'Aurangabad Division', buses: 380, alerts: 0 },
    { region: 'Nagpur Division', buses: 510, alerts: 1 },
    { region: 'Konkan Division', buses: 290, alerts: 4 },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Live State Map</h1>
          <p className="page-subtitle">Real-time fleet positions across Maharashtra · 4,921 active buses</p>
        </div>
        <div className="live-badge"><span className="pulse"></span>Live GPS Feed</div>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'1fr 300px',gap:'1.25rem'}}>
        <div className="card" style={{minHeight:520,display:'flex',alignItems:'center',justifyContent:'center',background:'linear-gradient(145deg,hsl(220,35%,8%),hsl(220,28%,14%))',position:'relative',overflow:'hidden'}}>
          <div style={{position:'absolute',inset:0,opacity:0.05,backgroundImage:'radial-gradient(circle at 30% 40%, hsl(210,100%,58%) 0%, transparent 50%), radial-gradient(circle at 70% 60%, hsl(165,80%,48%) 0%, transparent 50%)'}} />
          <div style={{textAlign:'center',position:'relative',zIndex:1}}>
            <div style={{fontSize:56,marginBottom:16}}>🗺️</div>
            <div style={{fontSize:'1.1rem',fontWeight:800,color:'var(--hq-text)'}}>Maharashtra Fleet Map</div>
            <div style={{fontSize:'0.82rem',color:'var(--hq-muted)',marginTop:6,marginBottom:20}}>Leaflet / Mapbox GL JS integration · v1 API: GET /v1/fleet/positions</div>
            <div style={{display:'flex',flexWrap:'wrap',gap:8,justifyContent:'center',maxWidth:400}}>
              {['Mumbai','Pune','Nashik','Aurangabad','Nagpur','Amravati','Kolhapur','Solapur','Latur'].map(d => (
                <span key={d} style={{background:'rgba(66,153,225,0.15)',border:'1px solid rgba(66,153,225,0.3)',color:'var(--hq-primary)',padding:'4px 10px',borderRadius:20,fontSize:'0.75rem',fontWeight:600}}>
                  📍 {d}
                </span>
              ))}
            </div>
          </div>
        </div>

        <div>
          <div className="card" style={{marginBottom:'1rem'}}>
            <div className="card-title">Division Status</div>
            {heatspots.map(h => (
              <div key={h.region} style={{marginBottom:12}}>
                <div style={{display:'flex',justifyContent:'space-between',marginBottom:4}}>
                  <span style={{fontSize:'0.82rem',fontWeight:600}}>{h.region}</span>
                  <div style={{display:'flex',gap:6,alignItems:'center'}}>
                    {h.alerts > 0 && <span className="badge badge-red">⚠ {h.alerts}</span>}
                    <span style={{fontSize:'0.78rem',color:'var(--hq-muted)'}}>{h.buses}</span>
                  </div>
                </div>
                <div className="progress-bar">
                  <div className="progress-fill" style={{width:`${(h.buses/820*100).toFixed(0)}%`,background:h.alerts>2?'var(--hq-warn)':'var(--hq-primary)'}} />
                </div>
              </div>
            ))}
          </div>

          <div className="card">
            <div className="card-title">Map Legend</div>
            {[{icon:'🟢',label:'On-Time Bus'},{icon:'🟡',label:'Delayed Bus'},{icon:'🔴',label:'Breakdown'},{icon:'⚪',label:'Depot'},{icon:'🔵',label:'Bus Stop'}].map(l => (
              <div key={l.label} style={{display:'flex',gap:8,alignItems:'center',marginBottom:8,fontSize:'0.82rem',color:'var(--hq-muted)'}}>
                <span>{l.icon}</span>{l.label}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
