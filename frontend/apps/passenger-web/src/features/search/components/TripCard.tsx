import { Trip } from '../types';
import { useRouter } from 'next/navigation';

export function TripCard({ trip }: { trip: Trip }) {
  const router = useRouter();

  const handleSelect = () => {
    // Navigate to Seat Selection milestone
    router.push(`/booking/seats?tripId=${trip.id}`);
  };

  const depDate = new Date(trip.departureTime);
  const arrDate = new Date(trip.arrivalTime);

  return (
    <div style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div>
        <div style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>{depDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} - {arrDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
        <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem', marginBottom: '0.5rem' }}>{trip.durationMinutes} mins • {trip.busType}</div>
        <div style={{ display: 'inline-block', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold', backgroundColor: trip.liveStatus === 'ON_TIME' ? '#e6f4ea' : '#fce8e6', color: trip.liveStatus === 'ON_TIME' ? '#137333' : '#c5221f' }}>
          {trip.liveStatus === 'ON_TIME' ? 'On Time' : 'Delayed'}
        </div>
      </div>
      
      <div style={{ textAlign: 'right' }}>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--color-primary)' }}>₹{trip.baseFare}</div>
        <div style={{ fontSize: '0.9rem', color: trip.availableSeats < 5 ? 'red' : 'green', marginBottom: '0.5rem' }}>{trip.availableSeats} Seats Left</div>
        <button onClick={handleSelect} className="btn-primary">Select Seats</button>
      </div>
    </div>
  );
}
