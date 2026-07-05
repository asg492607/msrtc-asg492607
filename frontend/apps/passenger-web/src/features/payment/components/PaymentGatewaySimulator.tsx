'use client';
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
