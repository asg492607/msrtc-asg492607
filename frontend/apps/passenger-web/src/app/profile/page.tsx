'use client';
import { useAuthStore } from '../../store/useAuthStore';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function ProfilePage() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const router = useRouter();

  // Route Guard Pattern
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated || !user) return null;

  return (
    <div style={{ padding: '4rem 2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Welcome back, {user.phone}</h1>
      <p>Role: {user.roles.join(', ')}</p>
      <button onClick={() => { logout(); router.push('/'); }} className="btn-primary" style={{ marginTop: '2rem', backgroundColor: 'red' }}>Logout</button>
    </div>
  );
}
