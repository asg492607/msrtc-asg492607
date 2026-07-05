'use client';
import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { apiClient } from '../../lib/api/client';

export default function TrackingPage() {
  const params = useSearchParams();
  const tripId = params.get('tripId') || 'TRIP-MOCK-001';
  const [pos, setPos] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    const poll = async () => {
      const data = await apiClient.tracking.getBusPosition(tripId);
      setPos(data);
      setHistory(prev => [{ ...data, time: new Date().toLocaleTimeString() }, ...prev.slice(0, 4)]);
    };
    poll();
    const id = setInterval(poll, 10000);
    return () => clearInterval(id);
  }, [tripId]);

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '2rem' }}>
      <h1 style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: 6 }}>Live Bus Tracking</h1>
      <p style={{ color: '#777', marginBottom: '1.5rem' }}>Trip: {tripId} · Updates every 10s</p>

      {/* Map Placeholder */}
      <div style={{ background: 'linear-gradient(135deg, #0f172a, #1e3a5f)', borderRadius: 16, height: 280, display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.5rem', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', inset: 0, background: 'radial-gradient(circle at 40% 50%, rgba(66,153,225,0.2) 0%, transparent 60%)' }} />
        <div style={{ textAlign: 'center', zIndex: 1 }}>
          <div style={{ fontSize: 48, marginBottom: 8 }}>📍</div>
          <div style={{ color: '#fff', fontWeight: 700, fontSize: '1rem' }}>Maharashtra Live Map</div>
          <div style={{ color: 'rgba(255,255,255,0.55)', fontSize: '0.82rem', marginTop: 4 }}>Leaflet.js · v1 API: GET /v1/fleet/positions/{tripId}</div>
          {pos && (
            <div style={{ marginTop: 12, background: 'rgba(255,255,255,0.1)', borderRadius: 8, padding: '8px 16px', color: '#fff', fontSize: '0.82rem', fontFamily: 'monospace' }}>
              {pos.lat.toFixed(5)}, {pos.lng.toFixed(5)}
            </div>
          )}
        </div>
      </div>

      {pos && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
          {[
            { label: 'Current Speed', value: `${pos.speed} km/h`, icon: '⚡' },
            { label: 'ETA to Next Stop', value: pos.eta, icon: '⏱️' },
            { label: 'Next Stop', value: pos.nextStop, icon: '🚏' },
          ].map(s => (
            <div key={s.label} style={{ background: '#fff', borderRadius: 12, padding: '1rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)', textAlign: 'center' }}>
              <div style={{ fontSize: 24, marginBottom: 6 }}>{s.icon}</div>
              <div style={{ fontWeight: 800, fontSize: '1.1rem', color: '#0053A0' }}>{s.value}</div>
              <div style={{ fontSize: '0.75rem', color: '#999', marginTop: 2 }}>{s.label}</div>
            </div>
          ))}
        </div>
      )}

      <div style={{ background: '#fff', borderRadius: 12, padding: '1.25rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)' }}>
        <h3 style={{ fontWeight: 700, marginBottom: 12, fontSize: '0.95rem' }}>Position History</h3>
        {history.length === 0 ? <p style={{ color: '#aaa', fontSize: '0.85rem' }}>Waiting for GPS data…</p> : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead><tr>{['Time','Latitude','Longitude','Speed'].map(h => <th key={h} style={{ textAlign: 'left', padding: '6px 8px', fontSize: '0.75rem', color: '#999', fontWeight: 700, textTransform: 'uppercase', borderBottom: '1px solid #eee' }}>{h}</th>)}</tr></thead>
            <tbody>
              {history.map((p, i) => (
                <tr key={i} style={{ fontSize: '0.83rem' }}>
                  <td style={{ padding: '6px 8px', fontFamily: 'monospace' }}>{p.time}</td>
                  <td style={{ padding: '6px 8px', fontFamily: 'monospace' }}>{p.lat.toFixed(5)}</td>
                  <td style={{ padding: '6px 8px', fontFamily: 'monospace' }}>{p.lng.toFixed(5)}</td>
                  <td style={{ padding: '6px 8px' }}>{p.speed} km/h</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
