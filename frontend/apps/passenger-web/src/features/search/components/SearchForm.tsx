'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export function SearchForm({ defaultSource = '', defaultDestination = '', defaultDate = '' }) {
  const [source, setSource] = useState(defaultSource);
  const [destination, setDestination] = useState(defaultDestination);
  const [date, setDate] = useState(defaultDate);
  const router = useRouter();

  const handleSwap = () => {
    setSource(destination);
    setDestination(source);
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (source && destination && date) {
      router.push(`/search?source=${source}&destination=${destination}&date=${date}`);
    }
  };

  return (
    <form onSubmit={handleSearch} className="search-box" style={{ display: 'flex', gap: '1rem', alignItems: 'center', background: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
      <input value={source} onChange={e=>setSource(e.target.value)} placeholder="Leaving From" required style={{ padding: '0.75rem', border: '1px solid #ddd', borderRadius: '8px' }} />
      <button type="button" onClick={handleSwap} style={{ background: '#eee', border: 'none', padding: '0.5rem 1rem', borderRadius: '8px', cursor: 'pointer' }}>⇄</button>
      <input value={destination} onChange={e=>setDestination(e.target.value)} placeholder="Going To" required style={{ padding: '0.75rem', border: '1px solid #ddd', borderRadius: '8px' }} />
      <input type="date" value={date} onChange={e=>setDate(e.target.value)} required style={{ padding: '0.75rem', border: '1px solid #ddd', borderRadius: '8px' }} />
      <button type="submit" className="btn-primary">Search Buses</button>
    </form>
  );
}
