import { ContactDetailsInput } from '../types';
import { validateContact } from '../schemas/validation';

export function ContactDetails({ 
  contact, 
  onChange 
}: { 
  contact: ContactDetailsInput, 
  onChange: (field: keyof ContactDetailsInput, val: string) => void 
}) {
  const error = validateContact(contact);
  const isDirty = contact.email !== '' || contact.mobile !== '';

  return (
    <div style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', border: '1px solid #ddd', marginTop: '1.5rem' }}>
      <h4 style={{ marginBottom: '1rem' }}>Contact Details (For Tickets)</h4>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <input type="email" value={contact.email} onChange={e => onChange('email', e.target.value)} placeholder="Email Address" className="form-input" />
        <input type="tel" value={contact.mobile} onChange={e => onChange('mobile', e.target.value)} placeholder="Mobile Number" className="form-input" />
      </div>
      {isDirty && error && <p style={{ color: 'red', fontSize: '0.85rem', marginTop: '0.5rem' }}>{error}</p>}
    </div>
  );
}
