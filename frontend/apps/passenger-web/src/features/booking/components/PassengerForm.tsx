import { PassengerInput } from '../types';
import { validatePassenger } from '../schemas/validation';

export function PassengerForm({ 
  passengers, 
  onChange 
}: { 
  passengers: PassengerInput[], 
  onChange: (idx: number, field: keyof PassengerInput, val: string) => void 
}) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {passengers.map((p, idx) => {
         const error = validatePassenger(p);
         const isDirty = p.name !== '' || p.age !== '' || p.gender !== '';
         return (
           <div key={p.seatId} style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', border: '1px solid #ddd' }}>
             <h4 style={{ marginBottom: '1rem', color: 'var(--color-primary)' }}>Passenger {idx + 1} (Seat {p.seatNumber})</h4>
             <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
               <input value={p.name} onChange={e => onChange(idx, 'name', e.target.value)} placeholder="Full Name" className="form-input" />
               <input type="number" value={p.age} onChange={e => onChange(idx, 'age', e.target.value)} placeholder="Age" className="form-input" />
               <select value={p.gender} onChange={e => onChange(idx, 'gender', e.target.value)} className="form-input">
                 <option value="">Select Gender</option>
                 <option value="MALE">Male</option>
                 <option value="FEMALE">Female</option>
                 <option value="OTHER">Other</option>
               </select>
             </div>
             {isDirty && error && <p style={{ color: 'red', fontSize: '0.85rem', marginTop: '0.5rem' }}>{error}</p>}
           </div>
         );
      })}
    </div>
  );
}
