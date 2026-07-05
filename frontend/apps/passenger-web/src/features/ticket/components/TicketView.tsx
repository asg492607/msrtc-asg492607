import { QRCodeSVG } from 'qrcode.react';

export function TicketView({ ticket }: { ticket: any }) {
  return (
    <div style={{ background: 'white', maxWidth: '600px', margin: '2rem auto', borderRadius: '16px', overflow: 'hidden', boxShadow: '0 10px 30px rgba(0,0,0,0.1)' }}>
      <div style={{ background: 'var(--color-primary)', color: 'white', padding: '2rem', textAlign: 'center' }}>
        <h2 style={{ margin: 0 }}>E-Ticket Confirmed</h2>
        <p style={{ opacity: 0.8, margin: '0.5rem 0 0 0' }}>Show this ticket to the conductor</p>
      </div>
      
      <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px dashed #ccc', paddingBottom: '1.5rem' }}>
          <div>
            <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem' }}>PNR Number</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold', letterSpacing: '1px' }}>{ticket.pnr}</div>
          </div>
          <QRCodeSVG value={ticket.pnr} size={80} />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div>
            <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem' }}>From</div>
            <div style={{ fontWeight: 'bold' }}>{ticket.source}</div>
          </div>
          <div>
            <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem' }}>To</div>
            <div style={{ fontWeight: 'bold' }}>{ticket.destination}</div>
          </div>
          <div>
            <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem' }}>Departure</div>
            <div style={{ fontWeight: 'bold' }}>{new Date(ticket.departureTime).toLocaleString()}</div>
          </div>
          <div>
             <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem' }}>Bus Type</div>
             <div style={{ fontWeight: 'bold' }}>{ticket.busType}</div>
          </div>
        </div>

        <div style={{ background: '#f5f7fa', padding: '1rem', borderRadius: '8px' }}>
          <div style={{ color: 'var(--color-text-light)', fontSize: '0.9rem', marginBottom: '0.5rem' }}>Passengers & Seats</div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold' }}>
            <span>{ticket.passengers.map((p:any) => p.name).join(', ')}</span>
            <span style={{ color: 'var(--color-primary)' }}>Seats: {ticket.seats.join(', ')}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
