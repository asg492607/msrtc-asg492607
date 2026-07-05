import '@/styles/hq.css';
import { Sidebar } from '@/components/ui/Sidebar';

export const metadata = {
  title: 'MSRTC HQ Command Center',
  description: 'Executive command center for Maharashtra State Road Transport Corporation',
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
