'use client';
import { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '../../lib/api/client';

export default function ProfilePage() {
  const [saved, setSaved] = useState(false);
  const [notifPrefs, setNotifPrefs] = useState({ email: true, sms: true, push: false, promotions: false });

  const { data: profile, isLoading } = useQuery({ queryKey: ['profile'], queryFn: apiClient.profile.get });
  const { mutateAsync: update, isPending } = useMutation({ mutationFn: apiClient.profile.update });
  const [form, setForm] = useState({ name: '', email: '', phone: '' });

  useEffect(() => { if (profile) setForm({ name: profile.name, email: profile.email, phone: profile.phone }); }, [profile]);

  const handleSave = async () => {
    await update(form);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  if (isLoading) return <div style={{ padding: '4rem', textAlign: 'center' }}>Loading profile…</div>;

  return (
    <div style={{ maxWidth: 760, margin: '0 auto', padding: '2rem' }}>
      <h1 style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: '1.5rem' }}>Profile & Settings</h1>

      {saved && <div style={{ background: '#e6f4ea', border: '1px solid #34a853', borderRadius: 8, padding: '0.75rem 1rem', marginBottom: '1.5rem', color: '#137333', fontWeight: 600 }}>✅ Profile updated successfully!</div>}

      {/* Profile */}
      <div style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)', marginBottom: '1.25rem' }}>
        <h3 style={{ fontWeight: 700, marginBottom: '1rem', fontSize: '1rem' }}>Personal Information</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
          {[{ key: 'name', label: 'Full Name', type: 'text' }, { key: 'email', label: 'Email Address', type: 'email' }, { key: 'phone', label: 'Mobile Number', type: 'tel' }].map(f => (
            <div key={f.key} style={{ gridColumn: f.key === 'name' ? '1 / -1' : 'auto' }}>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>{f.label}</label>
              <input type={f.type} value={(form as any)[f.key]} onChange={e => setForm({ ...form, [f.key]: e.target.value })} style={{ width: '100%', padding: '0.55rem 0.85rem', border: '1px solid #ddd', borderRadius: 8, fontSize: '0.9rem' }} />
            </div>
          ))}
        </div>
        <button onClick={handleSave} disabled={isPending} style={{ background: '#0053A0', color: '#fff', border: 'none', borderRadius: 8, padding: '0.55rem 1.5rem', fontWeight: 700, cursor: 'pointer', opacity: isPending ? 0.5 : 1 }}>{isPending ? 'Saving…' : 'Save Changes'}</button>
      </div>

      {/* Task 95 — Notification Preferences */}
      <div style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)', marginBottom: '1.25rem' }}>
        <h3 style={{ fontWeight: 700, marginBottom: '1rem', fontSize: '1rem' }}>Notification Preferences</h3>
        {[
          { key: 'email', label: 'Email Notifications', desc: 'Booking confirmations, tickets, receipts' },
          { key: 'sms', label: 'SMS Alerts', desc: 'OTPs, departure reminders, delays' },
          { key: 'push', label: 'Push Notifications', desc: 'Real-time updates via browser/app' },
          { key: 'promotions', label: 'Promotional Offers', desc: 'Discounts, new routes, seasonal offers' },
        ].map(n => (
          <div key={n.key} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.75rem 0', borderBottom: '1px solid #f0f0f0' }}>
            <div>
              <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{n.label}</div>
              <div style={{ fontSize: '0.78rem', color: '#999', marginTop: 2 }}>{n.desc}</div>
            </div>
            <label style={{ position: 'relative', display: 'inline-block', width: 40, height: 22 }}>
              <input type="checkbox" checked={(notifPrefs as any)[n.key]} onChange={e => setNotifPrefs({ ...notifPrefs, [n.key]: e.target.checked })} style={{ opacity: 0, width: 0, height: 0 }} />
              <span onClick={() => setNotifPrefs(p => ({ ...p, [n.key]: !(p as any)[n.key] }))} style={{ position: 'absolute', cursor: 'pointer', inset: 0, background: (notifPrefs as any)[n.key] ? '#0053A0' : '#ccc', borderRadius: 22, transition: '0.2s' }}>
                <span style={{ position: 'absolute', width: 16, height: 16, left: (notifPrefs as any)[n.key] ? 21 : 3, top: 3, background: '#fff', borderRadius: '50%', transition: '0.2s' }} />
              </span>
            </label>
          </div>
        ))}
      </div>

      {/* Security */}
      <div style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)' }}>
        <h3 style={{ fontWeight: 700, marginBottom: '1rem', fontSize: '1rem' }}>Security</h3>
        <button style={{ background: '#eee', color: '#333', border: 'none', borderRadius: 8, padding: '0.55rem 1.2rem', fontWeight: 700, cursor: 'pointer', marginRight: 8 }}>Change Password</button>
        <button style={{ background: '#fce8e6', color: '#c5221f', border: 'none', borderRadius: 8, padding: '0.55rem 1.2rem', fontWeight: 700, cursor: 'pointer' }}>Delete Account</button>
      </div>
    </div>
  );
}
