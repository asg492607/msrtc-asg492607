'use client';
import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '../../lib/api/client';

export default function ComplaintsPage() {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ type: 'ONBOARD', subject: '', description: '', pnr: '' });
  const [submitted, setSubmitted] = useState<any>(null);

  const { data: complaints, isLoading, refetch } = useQuery({ queryKey: ['complaints'], queryFn: apiClient.complaints.list });
  const { mutateAsync: submit, isPending } = useMutation({ mutationFn: apiClient.complaints.submit });

  const handleSubmit = async () => {
    const res = await submit(form);
    setSubmitted(res);
    setShowForm(false);
    setForm({ type: 'ONBOARD', subject: '', description: '', pnr: '' });
    refetch();
  };

  const STATUS_STYLE: Record<string, any> = {
    RESOLVED: { bg: '#e6f4ea', color: '#137333' },
    UNDER_REVIEW: { bg: '#fff3cd', color: '#856404' },
    OPEN: { bg: '#fce8e6', color: '#c5221f' }
  };

  if (isLoading) return <div style={{ padding: '4rem', textAlign: 'center' }}>Loading…</div>;

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800 }}>Complaints & Feedback</h1>
          <p style={{ color: '#777', marginTop: 4 }}>We value your experience and work to resolve all issues.</p>
        </div>
        <button onClick={() => setShowForm(true)} style={{ background: '#ea4335', color: '#fff', border: 'none', borderRadius: 8, padding: '0.6rem 1.2rem', fontWeight: 700, cursor: 'pointer' }}>+ Raise Complaint</button>
      </div>

      {submitted && (
        <div style={{ background: '#e6f4ea', border: '1px solid #34a853', borderRadius: 10, padding: '1rem', marginBottom: '1.5rem' }}>
          ✅ Complaint <strong>{submitted.complaintId}</strong> raised. We will respond within 48 hours.
        </div>
      )}

      {showForm && (
        <div style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', marginBottom: '1.5rem', boxShadow: '0 2px 12px rgba(0,0,0,0.1)' }}>
          <h3 style={{ marginBottom: '1rem' }}>New Complaint</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div>
                <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>Category</label>
                <select value={form.type} onChange={e => setForm({ ...form, type: e.target.value })} style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: 6 }}>
                  <option value="ONBOARD">Onboard Experience</option>
                  <option value="CONDUCT">Staff Conduct</option>
                  <option value="BOOKING">Booking Issue</option>
                  <option value="REFUND">Refund Delay</option>
                  <option value="OTHER">Other</option>
                </select>
              </div>
              <div>
                <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>PNR (if applicable)</label>
                <input value={form.pnr} onChange={e => setForm({ ...form, pnr: e.target.value })} placeholder="PNR12345" style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: 6 }} />
              </div>
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>Subject</label>
              <input value={form.subject} onChange={e => setForm({ ...form, subject: e.target.value })} placeholder="Brief description" style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: 6 }} />
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#555', display: 'block', marginBottom: 4 }}>Detailed Description</label>
              <textarea value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} rows={4} placeholder="Describe the issue in detail…" style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: 6, resize: 'vertical' }} />
            </div>
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <button onClick={handleSubmit} disabled={isPending || !form.subject} style={{ background: '#ea4335', color: '#fff', border: 'none', borderRadius: 8, padding: '0.6rem 1.5rem', fontWeight: 700, cursor: 'pointer', opacity: (!form.subject || isPending) ? 0.5 : 1 }}>{isPending ? 'Submitting…' : 'Submit Complaint'}</button>
            <button onClick={() => setShowForm(false)} style={{ background: '#eee', color: '#333', border: 'none', borderRadius: 8, padding: '0.6rem 1rem', fontWeight: 700, cursor: 'pointer' }}>Cancel</button>
          </div>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {complaints?.map((c: any) => (
          <div key={c.id} style={{ background: '#fff', borderRadius: 12, padding: '1.25rem', boxShadow: '0 2px 8px rgba(0,0,0,0.07)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <div style={{ fontWeight: 700 }}>{c.subject}</div>
              <span style={{ background: STATUS_STYLE[c.status]?.bg, color: STATUS_STYLE[c.status]?.color, padding: '3px 10px', borderRadius: 20, fontSize: '0.75rem', fontWeight: 700 }}>{c.status.replace('_', ' ')}</span>
            </div>
            <div style={{ fontSize: '0.82rem', color: '#999' }}>{c.type} · {c.createdAt} · {c.id}</div>
            {c.response && <div style={{ marginTop: 8, padding: '8px 12px', background: '#f0f4ff', borderRadius: 8, fontSize: '0.82rem', color: '#0053A0', borderLeft: '3px solid #0053A0' }}>📣 {c.response}</div>}
          </div>
        ))}
      </div>
    </div>
  );
}
