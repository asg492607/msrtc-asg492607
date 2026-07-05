'use client';
import { Suspense } from 'react';
import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { PaymentGatewaySimulator } from '../../../features/payment/components/PaymentGatewaySimulator';
import { usePaymentStatus } from '../../../features/payment/hooks/usePaymentStatus';

function PaymentPageContent() {
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

export default function PaymentPage() {
  return (
    <Suspense fallback={<div style={{ padding: '2rem' }}>Loading payment details...</div>}>
      <PaymentPageContent />
    </Suspense>
  );
}
