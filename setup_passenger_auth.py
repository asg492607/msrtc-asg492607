import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\passenger-web"

dirs = [
    "src/features/auth/components",
    "src/store",
    "src/lib/auth",
    "src/types",
    "src/app/login",
    "src/app/profile"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. Types
types_ts = """export interface User {
  id: string;
  phone: string;
  name?: string;
  roles: string[];
}
"""
with open(os.path.join(base_dir, "src/types/auth.ts"), "w", encoding="utf-8") as f: f.write(types_ts)

# 2. Zustand Store
store_ts = """import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User } from '../types/auth';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (user, token) => set({ user, token, isAuthenticated: true }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
    }),
    {
      name: 'msrtc-auth-storage', // saves to localStorage
    }
  )
);
"""
with open(os.path.join(base_dir, "src/store/useAuthStore.ts"), "w", encoding="utf-8") as f: f.write(store_ts)

# 3. API Interceptor / Client Update
client_ts = """import { useAuthStore } from '../../store/useAuthStore';

// Mock implementation of the generated SDK client with Auth Injection
export const apiClient = {
  getHeaders: () => {
    const token = useAuthStore.getState().token;
    return {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    };
  },

  routes: {
    search: async (from: string, to: string, date: string) => {
      console.log('Searching routes', from, to, date, 'Headers:', apiClient.getHeaders());
      return [];
    }
  },
  
  auth: {
    login: async (phone: string, otp: string) => {
      console.log('Verifying OTP', phone, otp);
      // Simulate backend response
      if (otp === '1234') {
         return {
           token: 'mock-jwt-token-xyz',
           user: { id: 'u1', phone, roles: ['PASSENGER'] }
         };
      }
      throw new Error("Invalid OTP");
    }
  }
};
"""
with open(os.path.join(base_dir, "src/lib/api/client.ts"), "w", encoding="utf-8") as f: f.write(client_ts)

# 4. Auth Feature Component (LoginForm)
login_tsx = """'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '../../../store/useAuthStore';
import { apiClient } from '../../../lib/api/client';

export function LoginForm() {
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState(1);
  const [error, setError] = useState('');
  
  const login = useAuthStore((state) => state.login);
  const router = useRouter();

  const handleSendOtp = (e: React.FormEvent) => {
    e.preventDefault();
    if (phone.length === 10) setStep(2);
  };

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await apiClient.auth.login(phone, otp);
      login(res.user, res.token);
      router.push('/profile'); // Redirect on success
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="auth-form-container" style={{ padding: '2rem', maxWidth: '400px', margin: '0 auto', background: 'white', borderRadius: '16px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
      <h2 style={{ marginBottom: '1.5rem', color: 'var(--color-primary)' }}>Sign In</h2>
      {error && <p style={{ color: 'red', marginBottom: '1rem' }}>{error}</p>}
      
      {step === 1 ? (
        <form onSubmit={handleSendOtp}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>Phone Number</label>
            <input type="tel" value={phone} onChange={e => setPhone(e.target.value)} placeholder="10-digit number" required className="form-input" style={{ width: '100%', padding: '0.75rem', borderRadius: '8px', border: '1px solid #ccc' }} />
          </div>
          <button type="submit" className="btn-primary" style={{ width: '100%' }}>Send OTP (Use 1234)</button>
        </form>
      ) : (
        <form onSubmit={handleVerifyOtp}>
           <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>Enter OTP</label>
            <input type="text" value={otp} onChange={e => setOtp(e.target.value)} placeholder="1234" required className="form-input" style={{ width: '100%', padding: '0.75rem', borderRadius: '8px', border: '1px solid #ccc' }} />
          </div>
          <button type="submit" className="btn-primary" style={{ width: '100%' }}>Verify & Login</button>
        </form>
      )}
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/features/auth/components/LoginForm.tsx"), "w", encoding="utf-8") as f: f.write(login_tsx)

# 5. Pages
page_login = """import { LoginForm } from '../../features/auth/components/LoginForm';

export default function LoginPage() {
  return (
    <div style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--color-background)' }}>
      <LoginForm />
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/login/page.tsx"), "w", encoding="utf-8") as f: f.write(page_login)

page_profile = """'use client';
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
"""
with open(os.path.join(base_dir, "src/app/profile/page.tsx"), "w", encoding="utf-8") as f: f.write(page_profile)


print("Auth flow scaffolded successfully.")
