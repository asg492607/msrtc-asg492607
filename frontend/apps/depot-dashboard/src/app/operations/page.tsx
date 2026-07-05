export default function OperationsPage() {
  const buses = [
    { id:'B01', bus:'MH-01-AB-1234', route:'Mumbai → Pune', driver:'Rajesh Kumar', lat:18.9200, lng:73.1100, speed:72, status:'ON_TIME', lastUpdate:'30s ago' },
    { id:'B02', bus:'MH-01-CD-5678', route:'Mumbai → Nashik', driver:'Suresh More', lat:19.6500, lng:73.7600, speed:65, status:'DELAYED', lastUpdate:'45s ago' },
    { id:'B03', bus:'MH-01-GH-3456', route:'Mumbai → Kolhapur', driver:'Vijay Shinde', lat:17.6800, lng:74.2400, speed:58, status:'ON_TIME', lastUpdate:'20s ago' },
  ];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Live Operations</h1>
        <p className="page-subtitle">Real-time fleet tracking · {buses.length} active buses</p>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'1fr 380px',gap:'1.25rem'}}>
        <div className="card" style={{minHeight:480,display:'flex',alignItems:'center',justifyContent:'center',background:'linear-gradient(135deg,hsl(215,60%,12%),hsl(215,40%,20%))',borderRadius:10}}>
          <div style={{textAlign:'center',color:'rgba(255,255,255,0.7)'}}>
            <div style={{fontSize:48,marginBottom:12}}>🗺️</div>
            <div style={{fontSize:'1rem',fontWeight:700,color:'#fff'}}>Maharashtra Fleet Map</div>
            <div style={{fontSize:'0.85rem',marginTop:6}}>Leaflet/Mapbox integration</div>
            <div style={{marginTop:16,display:'flex',gap:8,justifyContent:'center',flexWrap:'wrap'}}>
              {buses.map(b=>(
                <div key={b.id} style={{background:'rgba(255,255,255,0.12)',borderRadius:6,padding:'6px 12px',fontSize:'0.78rem',fontWeight:600,color:'#fff'}}>
                  📍 {b.bus}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div>
          <div className="card-title" style={{marginBottom:12}}>Active Buses</div>
          {buses.map(b=>(
            <div key={b.id} className="card" style={{marginBottom:12,borderLeft:`4px solid ${b.status==='ON_TIME'?'var(--depot-success)':'var(--depot-warn)'}`}}>
              <div style={{display:'flex',justifyContent:'space-between',marginBottom:6}}>
                <span style={{fontWeight:700,fontFamily:'monospace',fontSize:'0.85rem'}}>{b.bus}</span>
                <span className={`badge ${b.status==='ON_TIME'?'badge-success':'badge-warn'}`}>{b.status.replace('_',' ')}</span>
              </div>
              <div style={{fontSize:'0.83rem',color:'var(--depot-muted)',marginBottom:4}}>{b.route}</div>
              <div style={{fontSize:'0.8rem',color:'var(--depot-muted)'}}>Driver: {b.driver} · {b.speed} km/h</div>
              <div style={{fontSize:'0.78rem',color:'#aaa',marginTop:4}}>Updated {b.lastUpdate}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
