export default function ReportsPage() {
  const reports = [
    { name:'Daily Operations Summary', lastGenerated:'Today 06:00', schedule:'Daily', format:'PDF/Excel', status:'READY' },
    { name:'Weekly Revenue Report', lastGenerated:'2026-06-30', schedule:'Weekly', format:'PDF', status:'READY' },
    { name:'Monthly Fleet Health Report', lastGenerated:'2026-06-01', schedule:'Monthly', format:'PDF/Excel', status:'GENERATING' },
    { name:'Quarterly Financial Statement', lastGenerated:'2026-04-01', schedule:'Quarterly', format:'PDF', status:'READY' },
    { name:'Annual Performance Review', lastGenerated:'2026-04-01', schedule:'Annual', format:'PDF/PPT', status:'READY' },
    { name:'Incident Analysis Report', lastGenerated:'Today 08:00', schedule:'On-Demand', format:'PDF', status:'READY' },
    { name:'Compliance Audit Report', lastGenerated:'2026-07-01', schedule:'Monthly', format:'PDF', status:'READY' },
    { name:'Fuel Efficiency Analysis', lastGenerated:'2026-07-04', schedule:'Weekly', format:'Excel', status:'READY' },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Reports</h1>
          <p className="page-subtitle">Scheduled and on-demand executive reports</p>
        </div>
        <button className="btn btn-primary">+ Generate Report</button>
      </div>

      <div className="card">
        <table>
          <thead><tr><th>Report Name</th><th>Last Generated</th><th>Schedule</th><th>Format</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            {reports.map(r => (
              <tr key={r.name}>
                <td style={{fontWeight:600}}>{r.name}</td>
                <td style={{fontSize:'0.82rem',color:'var(--hq-muted)'}}>{r.lastGenerated}</td>
                <td><span className="badge badge-muted">{r.schedule}</span></td>
                <td style={{fontSize:'0.82rem'}}>{r.format}</td>
                <td><span className={`badge ${r.status==='READY'?'badge-green':'badge-yellow'}`}>{r.status}</span></td>
                <td style={{display:'flex',gap:6}}>
                  <button className="btn btn-sm btn-primary" disabled={r.status!=='READY'} style={{opacity:r.status!=='READY'?0.4:1}}>⬇ Download</button>
                  <button className="btn btn-sm btn-ghost">Schedule</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
