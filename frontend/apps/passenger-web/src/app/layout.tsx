import './globals.css';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata = {
  title: 'MSRTC Passenger Portal',
  description: 'Book tickets, track buses, and manage your journeys.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body>
        <header className="header">
          <div className="logo">MSRTC</div>
          <nav>
            <a href="/">Home</a>
            <a href="/search">Book</a>
            <a href="/login">Login</a>
          </nav>
        </header>
        <main>{children}</main>
        <footer>
          <p>&copy; 2026 Maharashtra State Road Transport Corporation</p>
        </footer>
      </body>
    </html>
  );
}
