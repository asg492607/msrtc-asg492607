'use client';
import { useSearchParams } from 'next/navigation';
import { SearchForm } from '../../features/search/components/SearchForm';
import { useRouteSearch } from '../../features/search/api/useRouteSearch';
import { TripCard } from '../../features/search/components/TripCard';

export default function SearchPage() {
  const searchParams = useSearchParams();
  const source = searchParams.get('source') || '';
  const destination = searchParams.get('destination') || '';
  const date = searchParams.get('date') || '';

  const { data: trips, isLoading, isError } = useRouteSearch(source, destination, date);

  return (
    <div style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ marginBottom: '2rem' }}>
        <SearchForm defaultSource={source} defaultDestination={destination} defaultDate={date} />
      </div>

      <h2>Available Buses for {source} to {destination}</h2>
      <p style={{ color: '#666', marginBottom: '2rem' }}>Date: {date}</p>

      {isLoading && <div>Loading trips... (Skeleton Loader Placeholder)</div>}
      {isError && <div style={{ color: 'red' }}>Failed to load trips. Please try again.</div>}
      
      {trips && trips.length === 0 && <div>No buses found for this route.</div>}
      
      {trips && trips.map(trip => (
        <TripCard key={trip.id} trip={trip} />
      ))}
    </div>
  );
}
