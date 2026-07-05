'use client';
import { useParams } from 'next/navigation';
import { useTicket } from '../../../../features/ticket/hooks/useTicket';
import { TicketView } from '../../../../features/ticket/components/TicketView';

export default function TicketPage() {
  const params = useParams();
  const pnr = params.pnr as string;
  const { data: ticket, isLoading } = useTicket(pnr);

  if (isLoading || !ticket) return <div style={{ padding: '4rem', textAlign: 'center' }}>Generating Digital Ticket...</div>;

  return (
    <div style={{ padding: '2rem' }}>
       <TicketView ticket={ticket} />
       
       <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button className="btn-primary" onClick={() => window.print()} style={{ background: '#333' }}>Download PDF</button>
       </div>
    </div>
  );
}
