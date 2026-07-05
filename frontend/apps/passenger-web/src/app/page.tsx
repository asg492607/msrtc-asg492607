import { SearchForm } from '../../features/search/components/SearchForm';

export default function Home() {
  return (
    <div className="hero" style={{ minHeight: '80vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <h1 style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '1rem' }}>Your Journey Starts Here</h1>
      <p style={{ fontSize: '1.2rem', marginBottom: '2rem', color: '#555' }}>Premium transit across Maharashtra. Book your seat today.</p>
      <SearchForm />
    </div>
  );
}
