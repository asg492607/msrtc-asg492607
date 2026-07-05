import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\passenger-web"

dirs = [
    "src/features/search/components",
    "src/features/search/api",
    "src/features/search/types",
    "src/app/search",
    "src/providers"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. Update package.json to include React Query
pkg_path = os.path.join(base_dir, "package.json")
with open(pkg_path, "r", encoding="utf-8") as f:
    pkg = json.load(f)
pkg["dependencies"]["@tanstack/react-query"] = "^5.0.0"
with open(pkg_path, "w", encoding="utf-8") as f:
    json.dump(pkg, f, indent=2)

# 2. QueryProvider
provider_tsx = """'use client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export default function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
"""
with open(os.path.join(base_dir, "src/providers/QueryProvider.tsx"), "w", encoding="utf-8") as f: f.write(provider_tsx)

# 3. Update Layout
layout_tsx = """import './globals.css';
import { Inter } from 'next/font/google';
import Providers from '../providers/QueryProvider';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata = {
  title: 'MSRTC Passenger Portal',
  description: 'Book tickets, track buses, and manage your journeys.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body>
        <Providers>
          <header className="header">
            <div className="logo">MSRTC</div>
            <nav>
              <a href="/">Home</a>
              <a href="/search">Book</a>
              <a href="/profile">Profile</a>
              <a href="/login">Login</a>
            </nav>
          </header>
          <main>{children}</main>
          <footer>
            <p>&copy; 2026 Maharashtra State Road Transport Corporation</p>
          </footer>
        </Providers>
      </body>
    </html>
  );
}
"""
with open(os.path.join(base_dir, "src/app/layout.tsx"), "w", encoding="utf-8") as f: f.write(layout_tsx)

# 4. Search Types
types_ts = """export interface Trip {
  id: string;
  routeId: string;
  source: string;
  destination: string;
  departureTime: string; // ISO String
  arrivalTime: string;   // ISO String
  durationMinutes: number;
  busType: 'Shivneri' | 'Shivshahi' | 'Ordinary' | 'Hirkani';
  availableSeats: number;
  baseFare: number;
  liveStatus: 'ON_TIME' | 'DELAYED';
}
"""
with open(os.path.join(base_dir, "src/features/search/types/index.ts"), "w", encoding="utf-8") as f: f.write(types_ts)

# 5. Search Hooks & API Update
client_path = os.path.join(base_dir, "src/lib/api/client.ts")
with open(client_path, "r", encoding="utf-8") as f:
    client_content = f.read()

client_content = client_content.replace(
"""  routes: {
    search: async (from: string, to: string, date: string) => {
      console.log('Searching routes', from, to, date, 'Headers:', apiClient.getHeaders());
      return [];
    }
  },""",
"""  routes: {
    search: async (from: string, to: string, date: string): Promise<any[]> => {
      console.log('Searching routes', from, to, date, 'Headers:', apiClient.getHeaders());
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 800));
      return [
        {
          id: 'TRIP-101', routeId: 'R-MUM-PUN', source: from, destination: to,
          departureTime: '2026-07-10T08:00:00Z', arrivalTime: '2026-07-10T11:30:00Z', durationMinutes: 210,
          busType: 'Shivneri', availableSeats: 12, baseFare: 550, liveStatus: 'ON_TIME'
        },
        {
          id: 'TRIP-102', routeId: 'R-MUM-PUN', source: from, destination: to,
          departureTime: '2026-07-10T09:15:00Z', arrivalTime: '2026-07-10T13:00:00Z', durationMinutes: 225,
          busType: 'Shivshahi', availableSeats: 30, baseFare: 350, liveStatus: 'DELAYED'
        }
      ];
    }
  },"""
)
with open(client_path, "w", encoding="utf-8") as f: f.write(client_content)


hook_ts = """import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';
import { Trip } from '../types';

export function useRouteSearch(source: string, destination: string, date: string) {
  return useQuery<Trip[]>({
    queryKey: ['routes', source, destination, date],
    queryFn: () => apiClient.routes.search(source, destination, date),
    enabled: !!source && !!destination && !!date,
    staleTime: 60 * 1000, // Cache for 1 minute to avoid spamming the backend
  });
}
"""
with open(os.path.join(base_dir, "src/features/search/api/useRouteSearch.ts"), "w", encoding="utf-8") as f: f.write(hook_ts)

# 6. Components
form_tsx = """'use client';
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
"""
with open(os.path.join(base_dir, "src/features/search/components/SearchForm.tsx"), "w", encoding="utf-8") as f: f.write(form_tsx)

card_tsx = """import { Trip } from '../types';
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
"""
with open(os.path.join(base_dir, "src/features/search/components/TripCard.tsx"), "w", encoding="utf-8") as f: f.write(card_tsx)


# 7. Pages
home_tsx = """import { SearchForm } from '../../features/search/components/SearchForm';

export default function Home() {
  return (
    <div className="hero" style={{ minHeight: '80vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <h1 style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '1rem' }}>Your Journey Starts Here</h1>
      <p style={{ fontSize: '1.2rem', marginBottom: '2rem', color: '#555' }}>Premium transit across Maharashtra. Book your seat today.</p>
      <SearchForm />
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/page.tsx"), "w", encoding="utf-8") as f: f.write(home_tsx)


search_page_tsx = """'use client';
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
"""
with open(os.path.join(base_dir, "src/app/search/page.tsx"), "w", encoding="utf-8") as f: f.write(search_page_tsx)

print("Route Search flow scaffolded successfully.")
