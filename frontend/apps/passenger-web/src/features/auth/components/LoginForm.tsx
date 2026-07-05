'use client';
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
