'use client';
import { useState, useEffect } from 'react';

export function Timer({ expiresAt, onExpire }: { expiresAt: number, onExpire: () => void }) {
  const [timeLeft, setTimeLeft] = useState(Math.max(0, expiresAt - Date.now()));

  useEffect(() => {
    if (timeLeft <= 0) {
      onExpire();
      return;
    }
    const interval = setInterval(() => {
      const remaining = Math.max(0, expiresAt - Date.now());
      setTimeLeft(remaining);
      if (remaining <= 0) onExpire();
    }, 1000);
    return () => clearInterval(interval);
  }, [expiresAt, onExpire, timeLeft]);

  const minutes = Math.floor(timeLeft / 60000);
  const seconds = Math.floor((timeLeft % 60000) / 1000);
  const isWarning = timeLeft < 120000; // < 2 minutes

  if (timeLeft <= 0) return null;

  return (
    <div style={{ padding: '0.5rem 1rem', background: isWarning ? '#fce8e6' : '#e8f0fe', color: isWarning ? '#c5221f' : '#1967d2', borderRadius: '8px', fontWeight: 'bold', display: 'inline-block' }}>
      Time to complete booking: {minutes}:{seconds.toString().padStart(2, '0')}
    </div>
  );
}
