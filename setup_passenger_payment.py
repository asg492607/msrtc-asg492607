import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\passenger-web"

dirs = [
    "src/features/payment/components",
    "src/features/payment/api",
    "src/features/payment/hooks",
    "src/features/ticket/components",
    "src/features/ticket/hooks",
    "src/app/booking/payment",
    "src/app/booking/ticket/[pnr]"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. Update package.json to include qrcode.react
pkg_path = os.path.join(base_dir, "package.json")
with open(pkg_path, "r", encoding="utf-8") as f:
    pkg = json.load(f)
pkg["dependencies"]["qrcode.react"] = "^3.1.0"
with open(pkg_path, "w", encoding="utf-8") as f:
    json.dump(pkg, f, indent=2)

# 2. Mock API extension
client_path = os.path.join(base_dir, "src/lib/api/client.ts")
with open(client_path, "r", encoding="utf-8") as f:
    client_content = f.read()

payment_ticket_mock = """
  payment: {
    initiate: async (bookingId: string, method: string) => {
      console.log('Initiating payment for', bookingId, method);
      await new Promise(r => setTimeout(r, 500));
      return { paymentIntentId: `PI-${Date.now()}` };
    },
    // Simulating webhook polling
    getStatus: async (bookingId: string) => {
      console.log('Polling payment status for', bookingId);
      // In a real app, this queries the backend which listens to razorpay webhooks
      // For this demo, we use localStorage to mock backend state changes made by the simulator
      const status = localStorage.getItem(`mock_payment_${bookingId}`);
      if (status === 'SUCCESS') return { status: 'CONFIRMED', pnr: `PNR${Math.floor(Math.random()*100000)}` };
      if (status === 'FAILED') return { status: 'FAILED' };
      return { status: 'PENDING' };
    }
  },
  ticket: {
    get: async (pnr: string) => {
      console.log('Fetching ticket', pnr);
      await new Promise(r => setTimeout(r, 500));
      return {
        pnr,
        status: 'CONFIRMED',
        source: 'Mumbai', destination: 'Pune',
        departureTime: '2026-07-10T08:00:00Z',
        busType: 'Shivneri',
        seats: ['1', '2'],
        passengers: [{ name: 'John Doe', age: 30, gender: 'MALE' }]
      };
    }
  },
"""
client_content = client_content.replace("  auth: {", payment_ticket_mock + "  auth: {")
with open(client_path, "w", encoding="utf-8") as f: f.write(client_content)


# 3. Hooks
poll_hook = """import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';

export function usePaymentStatus(bookingId: string, enabled: boolean) {
  return useQuery({
    queryKey: ['paymentStatus', bookingId],
    queryFn: () => apiClient.payment.getStatus(bookingId),
    enabled,
    refetchInterval: (query) => {
       const status = query.state.data?.status;
       return (status === 'CONFIRMED' || status === 'FAILED') ? false : 2000;
    }
  });
}
"""
with open(os.path.join(base_dir, "src/features/payment/hooks/usePaymentStatus.ts"), "w", encoding="utf-8") as f: f.write(poll_hook)

ticket_hook = """import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';

export function useTicket(pnr: string) {
  return useQuery({
    queryKey: ['ticket', pnr],
    queryFn: () => apiClient.ticket.get(pnr),
    enabled: !!pnr,
  });
}
"""
with open(os.path.join(base_dir, "src/features/ticket/hooks/useTicket.ts"), "w", encoding="utf-8") as f: f.write(ticket_hook)


# 4. Payment Components
simulator_tsx = """'use client';
export function PaymentGatewaySimulator({ bookingId, onCancel }: { bookingId: string, onCancel: () => void }) {
  const handleSuccess = () => {
    // Mocking the backend webhook success
    localStorage.setItem(`mock_payment_${bookingId}`, 'SUCCESS');
  };

  const handleFail = () => {
    // Mocking the backend webhook failure
    localStorage.setItem(`mock_payment_${bookingId}`, 'FAILED');
  };

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
      <div style={{ background: 'white', padding: '2rem', borderRadius: '12px', maxWidth: '400px', width: '100%', textAlign: 'center' }}>
        <h2 style={{ marginBottom: '1rem', color: '#333' }}>MSRTC Mock Gateway</h2>
        <p style={{ color: '#666', marginBottom: '2rem' }}>Please complete your payment simulation.</p>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
           <button onClick={handleSuccess} style={{ padding: '1rem', background: '#34a853', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>Simulate SUCCESS</button>
           <button onClick={handleFail} style={{ padding: '1rem', background: '#ea4335', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>Simulate FAILURE</button>
           <button onClick={onCancel} style={{ padding: '1rem', background: '#eee', color: '#333', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>Cancel Payment</button>
        </div>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/features/payment/components/PaymentGatewaySimulator.tsx"), "w", encoding="utf-8") as f: f.write(simulator_tsx)


# 5. Ticket Component
ticket_tsx = """import { QRCodeSVG } from 'qrcode.react';

export function TicketView({ ticket }: { ticket: any }) {
  return (
    <div style={{ background: 'white', maxWidth: '600px', margin: '2rem auto', borderRadius: '16px', overflow: 'hidden', boxShadow: '0 10px 30px rgba(0,0,0,0.1)' }}>
      <div style={{ background: 'var(--color-primary)', color: 'white', padding: '2rem', textAlign: 'center' }}>
        <h2 style={{ margin: 0 }}>E-Ticket Confirmed</h2>
        <p style={{ opacity: 0.8, margin: '0.5rem 0 0 0' }}>Show this ticket to the conductor</p>
      </div>
      
      <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px dashed #ccc', paddingBottom: '1.5rem' }}>
          <div>
            <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem' }}>PNR Number</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold', letterSpacing: '1px' }}>{ticket.pnr}</div>
          </div>
          <QRCodeSVG value={ticket.pnr} size={80} />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div>
            <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem' }}>From</div>
            <div style={{ fontWeight: 'bold' }}>{ticket.source}</div>
          </div>
          <div>
            <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem' }}>To</div>
            <div style={{ fontWeight: 'bold' }}>{ticket.destination}</div>
          </div>
          <div>
            <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem' }}>Departure</div>
            <div style={{ fontWeight: 'bold' }}>{new Date(ticket.departureTime).toLocaleString()}</div>
          </div>
          <div>
             <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem' }}>Bus Type</div>
             <div style={{ fontWeight: 'bold' }}>{ticket.busType}</div>
          </div>
        </div>

        <div style={{ background: '#f5f7fa', padding: '1rem', borderRadius: '8px' }}>
          <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem', marginBottom: '0.5rem' }}>Passengers & Seats</div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold' }}>
            <span>{ticket.passengers.map((p:any) => p.name).join(', ')}</span>
            <span style={{ color: 'var(--color-primary)' }}>Seats: {ticket.seats.join(', ')}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/features/ticket/components/TicketView.tsx"), "w", encoding="utf-8") as f: f.write(ticket_tsx)


# 6. Pages
payment_page_tsx = """'use client';
import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { PaymentGatewaySimulator } from '../../../features/payment/components/PaymentGatewaySimulator';
import { usePaymentStatus } from '../../../features/payment/hooks/usePaymentStatus';

export default function PaymentPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const bookingId = searchParams.get('bookingId') || '';
  
  const [showGateway, setShowGateway] = useState(false);
  
  // React Query Hook that polls the backend when the gateway is open
  const { data: statusData, isError } = usePaymentStatus(bookingId, showGateway);

  useEffect(() => {
    if (statusData?.status === 'CONFIRMED') {
      setShowGateway(false);
      router.push(`/booking/ticket/${statusData.pnr}`);
    }
  }, [statusData, router]);

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '2rem' }}>
      <h1>Payment Integration</h1>
      <p style={{ color: 'var(--color-text-light)', marginBottom: '2rem' }}>Booking Reference: {bookingId}</p>

      {statusData?.status === 'FAILED' && (
        <div style={{ padding: '1rem', background: '#fce8e6', color: '#c5221f', borderRadius: '8px', marginBottom: '2rem' }}>
          Payment Failed! The transaction was declined. You can safely retry before your reservation expires.
        </div>
      )}

      <div style={{ background: 'white', padding: '2rem', borderRadius: '12px', border: '1px solid #ddd' }}>
        <h3 style={{ marginBottom: '1.5rem' }}>Select Payment Method</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
           <label style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '1rem', border: '1px solid #eee', borderRadius: '8px', cursor: 'pointer' }}>
             <input type="radio" name="payment" defaultChecked /> UPI (GPay, PhonePe, Paytm)
           </label>
           <label style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '1rem', border: '1px solid #eee', borderRadius: '8px', cursor: 'pointer' }}>
             <input type="radio" name="payment" /> Credit / Debit Card
           </label>
        </div>

        <button 
          onClick={() => { localStorage.removeItem(`mock_payment_${bookingId}`); setShowGateway(true); }}
          className="btn-primary" 
          style={{ width: '100%', marginTop: '2rem', fontSize: '1.1rem', padding: '1rem' }}
        >
          Pay Now (₹1050)
        </button>
      </div>

      {showGateway && <PaymentGatewaySimulator bookingId={bookingId} onCancel={() => setShowGateway(false)} />}
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/booking/payment/page.tsx"), "w", encoding="utf-8") as f: f.write(payment_page_tsx)


ticket_page_tsx = """'use client';
import { useParams } from 'next/navigation';
import { useTicket } from '../../../../features/ticket/hooks/useTicket';
import { TicketView } from '../../../../features/ticket/components/TicketView';

export default function TicketPage() {
  const params = useParams();
  const pnr = params.pnr as string;
  const { data: ticket, isLoading } = useTicket(pnr);

  if (isLoading || !ticket) return <div style={{ padding: '4rem', textAlign: 'center' }}>Generating Digital Ticket...</div>;

  return (
    <div style={{ padding: '2rem' }}>
       <TicketView ticket={ticket} />
       
       <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button className="btn-primary" onClick={() => window.print()} style={{ background: '#333' }}>Download PDF</button>
       </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/booking/ticket/[pnr]/page.tsx"), "w", encoding="utf-8") as f: f.write(ticket_page_tsx)

print("Payment & Ticketing flow scaffolded successfully.")
