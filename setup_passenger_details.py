import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\passenger-web"

dirs = [
    "src/features/booking/components",
    "src/features/booking/api",
    "src/features/booking/types",
    "src/features/booking/hooks",
    "src/features/booking/schemas",
    "src/app/booking/passenger"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. Types & Schemas
types_ts = """export interface PassengerInput {
  seatId: string;
  seatNumber: string;
  name: string;
  age: string;
  gender: 'MALE' | 'FEMALE' | 'OTHER' | '';
}

export interface ContactDetailsInput {
  email: string;
  mobile: string;
}

export interface CreateBookingRequest {
  tripId: string;
  passengers: PassengerInput[];
  contact: ContactDetailsInput;
}
"""
with open(os.path.join(base_dir, "src/features/booking/types/index.ts"), "w", encoding="utf-8") as f: f.write(types_ts)

schema_ts = """import { PassengerInput, ContactDetailsInput } from '../types';

export const validatePassenger = (p: PassengerInput): string | null => {
  if (!p.name || p.name.length < 3) return "Name must be at least 3 characters";
  const ageNum = parseInt(p.age, 10);
  if (isNaN(ageNum) || ageNum < 1 || ageNum > 120) return "Age must be between 1 and 120";
  if (!p.gender) return "Please select a gender";
  return null;
};

export const validateContact = (c: ContactDetailsInput): string | null => {
  if (!c.mobile || c.mobile.length !== 10 || !/^\d+$/.test(c.mobile)) return "Mobile must be 10 digits";
  if (!c.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(c.email)) return "Invalid email address";
  return null;
};
"""
with open(os.path.join(base_dir, "src/features/booking/schemas/validation.ts"), "w", encoding="utf-8") as f: f.write(schema_ts)


# 2. Mock API extension
client_path = os.path.join(base_dir, "src/lib/api/client.ts")
with open(client_path, "r", encoding="utf-8") as f:
    client_content = f.read()

# Add booking mock to client
booking_mock = """
  booking: {
    createBooking: async (data: any) => {
      console.log('Creating pending booking', data);
      await new Promise(r => setTimeout(r, 1000));
      // Simulate backend validation or success
      return { success: true, bookingId: `BKG-${Math.floor(Math.random() * 1000000)}` };
    }
  },
"""
client_content = client_content.replace("  auth: {", booking_mock + "  auth: {")
with open(client_path, "w", encoding="utf-8") as f: f.write(client_content)


# 3. Hooks
hook_ts = """import { useMutation } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';
import { CreateBookingRequest } from '../types';

export function useBooking() {
  return useMutation({
    mutationFn: (data: CreateBookingRequest) => apiClient.booking.createBooking(data),
  });
}
"""
with open(os.path.join(base_dir, "src/features/booking/hooks/useBooking.ts"), "w", encoding="utf-8") as f: f.write(hook_ts)


# 4. Components
pass_form_tsx = """import { PassengerInput } from '../types';
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
"""
with open(os.path.join(base_dir, "src/features/booking/components/PassengerForm.tsx"), "w", encoding="utf-8") as f: f.write(pass_form_tsx)

contact_tsx = """import { ContactDetailsInput } from '../types';
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
"""
with open(os.path.join(base_dir, "src/features/booking/components/ContactDetails.tsx"), "w", encoding="utf-8") as f: f.write(contact_tsx)


summary_tsx = """export function BookingSummary({ 
  passengers, 
  onProceed, 
  isPending, 
  isValid 
}: { 
  passengers: any[], 
  onProceed: () => void, 
  isPending: boolean, 
  isValid: boolean 
}) {
  const baseFare = passengers.length * 500; // Mock fare
  const tax = baseFare * 0.05;
  const total = baseFare + tax;

  return (
    <div style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', position: 'sticky', top: '100px' }}>
      <h3 style={{ borderBottom: '1px solid #eee', paddingBottom: '0.5rem', marginBottom: '1rem' }}>Booking Summary</h3>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
        <span>Base Fare ({passengers.length} x ₹500)</span>
        <span>₹{baseFare}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
        <span>Taxes (5%)</span>
        <span>₹{tax}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold', fontSize: '1.2rem', marginTop: '1rem', borderTop: '1px solid #eee', paddingTop: '1rem' }}>
        <span>Total Payable</span>
        <span style={{ color: 'var(--color-primary)' }}>₹{total}</span>
      </div>
      <button 
        onClick={onProceed} 
        disabled={!isValid || isPending}
        className="btn-primary" 
        style={{ width: '100%', marginTop: '1.5rem', opacity: (!isValid || isPending) ? 0.5 : 1 }}
      >
        {isPending ? 'Processing...' : 'Proceed to Payment'}
      </button>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/features/booking/components/BookingSummary.tsx"), "w", encoding="utf-8") as f: f.write(summary_tsx)


# 5. Page
page_tsx = """'use client';
import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { PassengerForm } from '../../../features/booking/components/PassengerForm';
import { ContactDetails } from '../../../features/booking/components/ContactDetails';
import { BookingSummary } from '../../../features/booking/components/BookingSummary';
import { useBooking } from '../../../features/booking/hooks/useBooking';
import { PassengerInput, ContactDetailsInput } from '../../../features/booking/types';
import { validatePassenger, validateContact } from '../../../features/booking/schemas/validation';
import { Timer } from '../../../features/seats/components/Timer';

export default function PassengerDetailsPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const tripId = searchParams.get('tripId') || 'TRIP-MOCK';
  
  // Mock seats that were locked in the previous step
  // In a real app, this would come from a Zustand store or React Query
  const mockLockedSeats = [
    { seatId: 'S-1-1', seatNumber: '1' },
    { seatId: 'S-1-2', seatNumber: '2' }
  ];

  const [passengers, setPassengers] = useState<PassengerInput[]>(
    mockLockedSeats.map(s => ({ seatId: s.seatId, seatNumber: s.seatNumber, name: '', age: '', gender: '' }))
  );
  
  const [contact, setContact] = useState<ContactDetailsInput>({ email: '', mobile: '' });
  
  // Timer expires in 5 minutes from page load for this demo
  const [expiresAt] = useState(Date.now() + 5 * 60 * 1000); 
  const [isExpired, setIsExpired] = useState(false);

  const { mutateAsync: createBooking, isPending } = useBooking();

  const handlePassengerChange = (idx: number, field: keyof PassengerInput, val: string) => {
    const updated = [...passengers];
    updated[idx] = { ...updated[idx], [field]: val };
    setPassengers(updated);
  };

  const handleContactChange = (field: keyof ContactDetailsInput, val: string) => {
    setContact({ ...contact, [field]: val });
  };

  const isFormValid = 
    passengers.every(p => validatePassenger(p) === null) && 
    validateContact(contact) === null &&
    !isExpired;

  const handleProceed = async () => {
    try {
      const res = await createBooking({ tripId, passengers, contact });
      // Redirect to Payment Gateway simulation
      router.push(`/booking/payment?bookingId=${res.bookingId}`);
    } catch (e) {
      alert("Failed to create booking.");
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Passenger Details</h1>
        {!isExpired ? (
          <Timer expiresAt={expiresAt} onExpire={() => setIsExpired(true)} />
        ) : (
          <div style={{ color: 'red', fontWeight: 'bold' }}>Reservation Expired. Please restart.</div>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem', alignItems: 'start', opacity: isExpired ? 0.5 : 1, pointerEvents: isExpired ? 'none' : 'auto' }}>
        <div>
          <PassengerForm passengers={passengers} onChange={handlePassengerChange} />
          <ContactDetails contact={contact} onChange={handleContactChange} />
        </div>
        <BookingSummary 
          passengers={passengers} 
          onProceed={handleProceed} 
          isPending={isPending} 
          isValid={isFormValid} 
        />
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/booking/passenger/page.tsx"), "w", encoding="utf-8") as f: f.write(page_tsx)

print("Passenger Details flow scaffolded successfully.")
