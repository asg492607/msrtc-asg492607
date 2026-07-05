export function BookingSummary({ 
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
