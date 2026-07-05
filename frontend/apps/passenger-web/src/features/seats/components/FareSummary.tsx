import { Seat } from '../types';
export function FareSummary({ selectedSeats, onProceed, isLocking }: { selectedSeats: Seat[], onProceed: () => void, isLocking: boolean }) {
  const totalFare = selectedSeats.reduce((sum, seat) => sum + seat.fare, 0);

  return (
    <div style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', position: 'sticky', top: '100px' }}>
      <h3 style={{ borderBottom: '1px solid #eee', paddingBottom: '0.5rem', marginBottom: '1rem' }}>Fare Summary</h3>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
        <span>Selected Seats ({selectedSeats.length})</span>
        <span>{selectedSeats.map(s => s.number).join(', ')}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold', fontSize: '1.2rem', marginTop: '1rem', borderTop: '1px solid #eee', paddingTop: '1rem' }}>
        <span>Total Payable</span>
        <span style={{ color: 'var(--color-primary)' }}>₹{totalFare}</span>
      </div>
      <button 
        onClick={onProceed} 
        disabled={selectedSeats.length === 0 || isLocking}
        className="btn-primary" 
        style={{ width: '100%', marginTop: '1.5rem', opacity: selectedSeats.length === 0 ? 0.5 : 1 }}
      >
        {isLocking ? 'Locking Seats...' : 'Proceed to Book'}
      </button>
    </div>
  );
}
