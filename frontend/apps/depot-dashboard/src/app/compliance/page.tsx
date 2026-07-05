"use client";
import { useState } from 'react';

const CERTS = [
  { id:'C01', busNumber:'MH-01-AB-1234', type:'Fitness Certificate', issueDate:'2025-07-01', expiryDate:'2026-07-01', status:'EXPIRING_SOON', authority:'RTO Mumbai' },
  { id:'C02', busNumber:'MH-01-CD-5678', type:'Permit Certificate', issueDate:'2025-06-15', expiryDate:'2027-06-15', status:'VALID', authority:'MSRTC HQ' },
  { id:'C03', busNumber:'MH-01-EF-9012', type:'Pollution Under Control', issueDate:'2026-01-10', expiryDate:'2026-07-10', status:'EXPIRED', authority:'MPCB' },
  { id:'C04', busNumber:'MH-01-GH-3456', type:'Insurance', issueDate:'2026-01-01', expiryDate:'2026-12-31', status:'VALID', authority:'National Insurance' },
  { id:'C05', busNumber:'MH-01-IJ-7890', type:'Fitness Certificate', issueDate:'2024-07-01', expiryDate:'2025-07-01', status:'EXPIRED', authority:'RTO Mumbai' },
];

const SBADGE: Record<string,string> = { VALID:'badge-success', EXPIRING_SOON:'badge-warn', EXPIRED:'badge-danger' };

export default function CompliancePage() {
  const expired = CERTS.filter(c=>c.status==='EXPIRED').length;
  const expiring = CERTS.filter(c=>c.status==='EXPIRING_SOON').length;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Compliance & Documentation</h1>
        <p className="page-subtitle">Certificates, permits and regulatory compliance</p>
      </div>

      {(expired > 0 || expiring > 0) && (
        <div style={{background:'hsl(4,80%,95%)',border:'1px solid hsl(4,80%,80%)',borderRadius:8,padding:'0.75rem 1rem',marginBottom:'1.25rem'}}>
          ⛔ <strong>{expired} expired</strong> and <strong>{expiring} expiring soon</strong> — Immediate action required to avoid regulatory penalties.
        </div>
      )}

      <div className="kpi-grid">
        {[{label:'Total Certificates',val:CERTS.length},{label:'Valid',val:CERTS.filter(c=>c.status==='VALID').length},{label:'Expiring (30 days)',val:expiring},{label:'Expired',val:expired}].map(k=>(
          <div key={k.label} className="kpi-card"><div className="kpi-label">{k.label}</div><div className="kpi-value">{k.val}</div></div>
        ))}
      </div>

      <div className="card">
        <div className="card-title">Certificate Registry</div>
        <table>
          <thead><tr><th>Bus</th><th>Certificate Type</th><th>Issued</th><th>Expiry</th><th>Authority</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            {CERTS.map(c=>(
              <tr key={c.id}>
                <td style={{fontFamily:'monospace',fontSize:'0.82rem'}}>{c.busNumber}</td>
                <td>{c.type}</td>
                <td style={{fontSize:'0.82rem'}}>{c.issueDate}</td>
                <td style={{fontSize:'0.82rem',fontWeight:c.status!=='VALID'?700:400,color:c.status==='EXPIRED'?'var(--depot-danger)':c.status==='EXPIRING_SOON'?'var(--depot-warn)':'inherit'}}>{c.expiryDate}</td>
                <td style={{fontSize:'0.82rem'}}>{c.authority}</td>
                <td><span className={`badge ${SBADGE[c.status]}`}>{c.status.replace('_',' ')}</span></td>
                <td><button className="btn btn-sm btn-primary">Renew</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
