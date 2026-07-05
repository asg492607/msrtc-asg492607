"use client";
import { useState } from 'react';

const PARTS = [
  { id:'P001', name:'Engine Oil Filter', partNumber:'EF-4501', stock:48, minStock:20, unit:'pcs', unitPrice:320 },
  { id:'P002', name:'Brake Pad Set', partNumber:'BP-2200', stock:12, minStock:15, unit:'sets', unitPrice:1800 },
  { id:'P003', name:'AC Refrigerant R134a', partNumber:'AC-R134', stock:8, minStock:10, unit:'cans', unitPrice:650 },
  { id:'P004', name:'Windshield Wiper Blade', partNumber:'WW-550', stock:35, minStock:20, unit:'pcs', unitPrice:180 },
  { id:'P005', name:'Bus Tyre 11R22.5', partNumber:'TY-1122', stock:6, minStock:10, unit:'pcs', unitPrice:12500 },
  { id:'P006', name:'Headlight Bulb 24V', partNumber:'HL-24V', stock:22, minStock:10, unit:'pcs', unitPrice:290 },
];

export default function InventoryPage() {
  const [search, setSearch] = useState('');
  const filtered = PARTS.filter(p => p.name.toLowerCase().includes(search.toLowerCase()) || p.partNumber.includes(search));
  const lowStock = PARTS.filter(p => p.stock < p.minStock).length;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Inventory & Spare Parts</h1>
        <p className="page-subtitle">{PARTS.length} SKUs · {lowStock} items below minimum stock</p>
      </div>

      {lowStock > 0 && (
        <div style={{background:'hsl(38,100%,94%)',border:'1px solid hsl(38,100%,75%)',borderRadius:8,padding:'0.75rem 1rem',marginBottom:'1.25rem',display:'flex',gap:8,alignItems:'center'}}>
          <span>⚠️</span>
          <span style={{fontWeight:600,color:'hsl(38,100%,30%)'}}>{lowStock} item(s) below minimum stock level. Raise purchase orders.</span>
        </div>
      )}

      <div className="card">
        <div className="toolbar">
          <input className="search-input" placeholder="Search part name or number..." value={search} onChange={e=>setSearch(e.target.value)} />
          <button className="btn btn-primary">+ Raise PO</button>
        </div>
        <table>
          <thead><tr><th>Part Name</th><th>Part No.</th><th>Stock</th><th>Min Stock</th><th>Unit</th><th>Unit Price</th><th>Stock Value</th><th>Status</th></tr></thead>
          <tbody>
            {filtered.map(p=>(
              <tr key={p.id}>
                <td style={{fontWeight:600}}>{p.name}</td>
                <td style={{fontFamily:'monospace',fontSize:'0.82rem'}}>{p.partNumber}</td>
                <td style={{fontWeight:700,color:p.stock<p.minStock?'var(--depot-danger)':'var(--depot-success)'}}>{p.stock}</td>
                <td style={{color:'var(--depot-muted)'}}>{p.minStock}</td>
                <td>{p.unit}</td>
                <td>₹{p.unitPrice.toLocaleString()}</td>
                <td>₹{(p.stock*p.unitPrice).toLocaleString()}</td>
                <td><span className={`badge ${p.stock<p.minStock?'badge-danger':'badge-success'}`}>{p.stock<p.minStock?'Low Stock':'Adequate'}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
