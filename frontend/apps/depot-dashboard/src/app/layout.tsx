import '@/styles/depot.css';
import { Sidebar } from '@/components/ui/Sidebar';

export const metadata = {
  title: 'MSRTC Depot Dashboard',
  description: 'Fleet operations and management for Mumbai Central Depot',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Sidebar />
        <div className="main-content">{children}</div>
      </body>
    </html>
  );
}
