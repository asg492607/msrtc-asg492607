"use client";
import { useState } from 'react';

const ALERTS = [
  { id:'ALT-001', type:'CRITICAL', icon:'🚨', title:'Accident on NH-48', desc:'Bus MH-01-AB-4521 involved in road accident near Khopoli. Emergency services deployed.', time:'9 min ago', acked: false },
  { id:'ALT-002', type:'HIGH', icon:'⚠️', title:'Breakdown — Nashik Bypass', desc:'Bus MH-09-CD-1234 stopped due to engine failure. Replacement bus dispatched.', time:'21 min ago', acked: false },
  { id:'ALT-003', type:'HIGH', icon:'⛽', title:'Fuel Shortage — Aurangabad Depot', desc:'Fuel stock at 18% capacity. Tanker ETA: 4 hours.', time:'45 min ago', acked: true },
  { id:'ALT-004', type:'MEDIUM', icon:'🕐', title:'High Delay Rate — Konkan Division', desc:'Average delay exceeding 22 minutes on 6 routes. Traffic congestion reported.', time:'1h ago', acked: true },
  { id:'ALT-005', type:'LOW', icon:'ℹ️', title:'Scheduled Maintenance Reminder', desc:'8 buses due for 10,000km service this week at Mumbai Central Depot.', time:'2h ago', acked: true },
];

const ACOLORS: Record<string,string> = {
  CRITICAL:'hsl(4,80%,12%)', HIGH:'hsl(38,100%,10%)', MEDIUM:'hsl(210,100%,10%)', LOW:'var(--hq-surface2)'
};
const ABORDERS: Record<string,string> = {
  CRITICAL:'var(--hq-danger)', HIGH:'var(--hq-warn)', MEDIUM:'var(--hq-primary)', LOW:'var(--hq-border)'
};

export default function AlertsPage() {
  const [alerts, setAlerts] = useState(ALERTS);
  const ack = (id: string) => setAlerts(prev => prev.map(a => a.id===id?{...a,acked:true}:a));

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Alert Center</h1>
          <p className="page-subtitle">{alerts.filter(a=>!a.acked).length} unacknowledged · {alerts.filter(a=>a.type==='CRITICAL').length} critical</p>
        </div>
        <button className="btn btn-ghost">Mark All Read</button>
      </div>

      <div style={{display:'flex',flexDirection:'column',gap:'0.85rem'}}>
        {alerts.map(a => (
          <div key={a.id} style={{background:ACOLORS[a.type],border:`1px solid ${ABORDERS[a.type]}`,borderRadius:10,padding:'1rem 1.25rem',display:'flex',gap:'1rem',alignItems:'flex-start',opacity:a.acked?0.6:1}}>
            <span style={{fontSize:24,marginTop:2}}>{a.icon}</span>
            <div style={{flex:1}}>
              <div style={{display:'flex',justifyContent:'space-between',marginBottom:4}}>
                <span style={{fontWeight:700,fontSize:'0.92rem'}}>{a.title}</span>
                <span style={{fontSize:'0.75rem',color:'var(--hq-muted)'}}>{a.time}</span>
              </div>
              <p style={{fontSize:'0.83rem',color:'var(--hq-muted)',lineHeight:1.5}}>{a.desc}</p>
            </div>
            {!a.acked && (
              <button className="btn btn-sm btn-ghost" onClick={()=>ack(a.id)} style={{whiteSpace:'nowrap'}}>Acknowledge</button>
            )}
            {a.acked && <span style={{fontSize:'0.75rem',color:'var(--hq-success)',whiteSpace:'nowrap',marginTop:4}}>✓ Acked</span>}
          </div>
        ))}
      </div>
    </div>
  );
}
