export default function MonitoringPage() {
  const dashboards = [
    { name:'Platform Overview', tool:'Grafana', url:'http://grafana.internal/d/platform', desc:'Golden signals (latency, traffic, errors, saturation)', status:'LIVE' },
    { name:'Distributed Tracing', tool:'Jaeger', url:'http://jaeger.internal', desc:'End-to-end request traces across all microservices', status:'LIVE' },
    { name:'Log Analytics', tool:'Loki / Grafana', url:'http://grafana.internal/d/logs', desc:'Centralised log aggregation from all pods', status:'LIVE' },
    { name:'Kubernetes Cluster', tool:'Grafana', url:'http://grafana.internal/d/k8s', desc:'Node health, pod restarts, resource utilisation', status:'LIVE' },
    { name:'Kafka Lag Monitor', tool:'Grafana', url:'http://grafana.internal/d/kafka', desc:'Consumer group lag per topic', status:'LIVE' },
    { name:'SLO Dashboard', tool:'Grafana', url:'http://grafana.internal/d/slo', desc:'Service Level Objectives and error budget burn rates', status:'LIVE' },
  ];

  const alerts = [
    { rule:'SeatService P95 > 150ms', severity:'WARNING', firing:true, since:'1h 22m' },
    { rule:'KafkaTopic seat.locks consumer lag > 200', severity:'WARNING', firing:true, since:'45m' },
    { rule:'PaymentService error rate > 1%', severity:'CRITICAL', firing:false, since:'—' },
    { rule:'Any pod CrashLoopBackOff', severity:'CRITICAL', firing:false, since:'—' },
    { rule:'Redis memory > 80%', severity:'WARNING', firing:false, since:'—' },
  ];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Monitoring & Observability</h1>
        <p className="page-subtitle">OpenTelemetry · Prometheus · Loki · Jaeger · Grafana</p>
      </div>

      <div className="two-col">
        <div className="card">
          <div className="card-title">Observability Dashboards</div>
          {dashboards.map(d => (
            <div key={d.name} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'10px 0',borderBottom:'1px solid var(--adm-border)'}}>
              <div>
                <div style={{fontWeight:700,fontSize:'0.88rem'}}>{d.name}</div>
                <div style={{fontSize:'0.75rem',color:'var(--adm-muted)',marginTop:2}}>{d.tool} · {d.desc}</div>
              </div>
              <div style={{display:'flex',gap:8,alignItems:'center'}}>
                <span className="badge badge-success">● {d.status}</span>
                <a href={d.url} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-ghost">Open ↗</a>
              </div>
            </div>
          ))}
        </div>

        <div className="card">
          <div className="card-title">Active Alert Rules</div>
          {alerts.map(a => (
            <div key={a.rule} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'10px 0',borderBottom:'1px solid var(--adm-border)'}}>
              <div style={{flex:1}}>
                <div style={{fontSize:'0.83rem',fontWeight:600,color:a.firing?'var(--adm-danger)':'inherit'}}>{a.rule}</div>
                {a.firing && <div style={{fontSize:'0.72rem',color:'var(--adm-danger)',marginTop:2}}>🔴 FIRING · {a.since}</div>}
              </div>
              <span className={`badge ${a.severity==='CRITICAL'?'badge-danger':'badge-warn'}`}>{a.severity}</span>
            </div>
          ))}
          <div style={{marginTop:12,display:'flex',gap:8}}>
            <button className="btn btn-sm btn-ghost">View All Rules</button>
            <button className="btn btn-sm btn-primary">Create Rule</button>
          </div>
        </div>
      </div>
    </div>
  );
}
