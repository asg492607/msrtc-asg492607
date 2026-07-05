export default function AIPage() {
  const insights = [
    { category:'Demand Forecasting', insight:'Predicted 22% surge in Mumbai-Pune travel on 2026-07-10 (public holiday). Recommend deploying 40 additional Shivneri buses.', confidence:'94%', impact:'HIGH', action:'Deploy Additional Fleet' },
    { category:'Predictive Maintenance', insight:'Bus MH-09-CD-4521 shows engine vibration pattern consistent with bearing failure. Predicted failure within 8-12 days.', confidence:'87%', impact:'HIGH', action:'Schedule Inspection' },
    { category:'Revenue Optimization', insight:'Nashik-Aurangabad route shows 62% empty seats on Tuesdays. Recommend dynamic pricing reduction of 15% to improve load factor.', confidence:'79%', impact:'MEDIUM', action:'Adjust Pricing' },
    { category:'Fuel Efficiency', insight:'Drivers on NH-48 corridor show 8% higher fuel consumption than benchmark. Eco-driving training recommended for 34 drivers.', confidence:'91%', impact:'MEDIUM', action:'Schedule Training' },
    { category:'Passenger Experience', insight:'Complaint volume for Konkan division increased 28% this month, primarily about AC failures. 6 specific buses identified.', confidence:'99%', impact:'MEDIUM', action:'Prioritize Repairs' },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">AI Insights</h1>
          <p className="page-subtitle">Machine learning recommendations · Updated every 6 hours</p>
        </div>
        <div className="live-badge"><span style={{color:'var(--hq-accent)'}}>🤖</span> AI Engine Active</div>
      </div>

      <div className="kpi-grid">
        {[{l:'Insights Generated',v:'142',c:'blue'},{l:'High Impact Actions',v:'12',c:'red'},{l:'Avg Confidence',v:'88.4%',c:'green'},{l:'Est. Savings (Monthly)',v:'₹42L',c:'green'}].map(k=>(
          <div key={k.l} className={`kpi-card ${k.c}`}><div className="kpi-label">{k.l}</div><div className="kpi-value">{k.v}</div></div>
        ))}
      </div>

      <div style={{display:'flex',flexDirection:'column',gap:'1rem'}}>
        {insights.map((ins,i) => (
          <div key={i} className="card" style={{borderLeft:`3px solid ${ins.impact==='HIGH'?'var(--hq-danger)':'var(--hq-warn)'}`}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',marginBottom:8}}>
              <div>
                <span className="badge badge-blue" style={{marginRight:8}}>{ins.category}</span>
                <span className="badge badge-muted">Confidence: {ins.confidence}</span>
              </div>
              <span className={`badge ${ins.impact==='HIGH'?'badge-red':'badge-yellow'}`}>{ins.impact} IMPACT</span>
            </div>
            <p style={{fontSize:'0.88rem',color:'var(--hq-text)',lineHeight:1.6,marginBottom:12}}>{ins.insight}</p>
            <button className="btn btn-primary btn-sm">{ins.action}</button>
          </div>
        ))}
      </div>
    </div>
  );
}
