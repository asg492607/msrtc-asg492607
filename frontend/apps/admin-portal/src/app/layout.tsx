import '@/styles/admin.css';
import { Sidebar } from '@/components/ui/Sidebar';

export const metadata = {
  title: 'MSRTC Admin Portal',
  description: 'Platform administration, IAM, tenants, feature flags and compliance',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Sidebar />
        <div className="main-content">
          <div className="page-body">{children}</div>
        </div>
      </body>
    </html>
  );
}
