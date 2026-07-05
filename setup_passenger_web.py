import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\frontend\apps\passenger-web"

dirs = [
    "src/app",
    "src/components",
    "src/lib/api",
    "src/styles",
    "public"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# package.json
pkg_json = {
  "name": "passenger-web",
  "version": "1.0.0",
  "private": True,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.2.3",
    "react": "^18",
    "react-dom": "^18"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18"
  }
}
with open(os.path.join(base_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg_json, f, indent=2)

# tsconfig.json
tsconfig = {
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": True,
    "skipLibCheck": True,
    "strict": True,
    "noEmit": True,
    "esModuleInterop": True,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": True,
    "isolatedModules": True,
    "jsx": "preserve",
    "incremental": True,
    "plugins": [{"name": "next"}],
    "paths": {"@/*": ["./src/*"]}
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
with open(os.path.join(base_dir, "tsconfig.json"), "w", encoding="utf-8") as f:
    json.dump(tsconfig, f, indent=2)

# next.config.mjs
next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {};
export default nextConfig;
"""
with open(os.path.join(base_dir, "next.config.mjs"), "w", encoding="utf-8") as f: f.write(next_config)

# src/app/layout.tsx
layout = """import './globals.css';
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
"""
with open(os.path.join(base_dir, "src/app/layout.tsx"), "w", encoding="utf-8") as f: f.write(layout)

# src/app/page.tsx
page = """export default function Home() {
  return (
    <div className="hero">
      <div className="hero-content">
        <h1>Your Journey Starts Here</h1>
        <p>Premium transit across Maharashtra. Book your seat today.</p>
        <div className="search-box">
          <input type="text" placeholder="From (e.g., Mumbai)" />
          <input type="text" placeholder="To (e.g., Pune)" />
          <input type="date" />
          <button className="btn-primary">Search Buses</button>
        </div>
      </div>
    </div>
  );
}
"""
with open(os.path.join(base_dir, "src/app/page.tsx"), "w", encoding="utf-8") as f: f.write(page)

# src/app/globals.css
css = """:root {
  --color-primary: hsl(210, 100%, 50%); /* Vibrant Blue */
  --color-primary-dark: hsl(210, 100%, 40%);
  --color-background: hsl(0, 0%, 98%);
  --color-surface: hsl(0, 0%, 100%);
  --color-text: hsl(220, 20%, 20%);
  --color-text-light: hsl(220, 20%, 40%);
  --font-sans: var(--font-inter), system-ui, sans-serif;
  --transition-speed: 0.2s;
}

body {
  margin: 0;
  font-family: var(--font-sans);
  background-color: var(--color-background);
  color: var(--color-text);
  line-height: 1.5;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header */
.header {
  background-color: var(--color-surface);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  font-weight: 800;
  font-size: 1.5rem;
  color: var(--color-primary);
  letter-spacing: -0.5px;
}

.header nav a {
  margin-left: 2rem;
  text-decoration: none;
  color: var(--color-text);
  font-weight: 500;
  transition: color var(--transition-speed);
}

.header nav a:hover {
  color: var(--color-primary);
}

/* Main Content */
main {
  flex: 1;
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, hsl(210, 100%, 95%), hsl(210, 50%, 90%));
  padding: 6rem 2rem;
  text-align: center;
}

.hero h1 {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  letter-spacing: -1px;
  color: var(--color-text);
}

.hero p {
  font-size: 1.2rem;
  color: var(--color-text-light);
  margin-bottom: 3rem;
}

/* Search Box */
.search-box {
  background: var(--color-surface);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  display: inline-flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
}

.search-box input {
  padding: 0.75rem 1rem;
  border: 1px solid hsl(0, 0%, 80%);
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  outline: none;
  transition: border-color var(--transition-speed);
}

.search-box input:focus {
  border-color: var(--color-primary);
}

/* Buttons */
.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color var(--transition-speed), transform var(--transition-speed);
}

.btn-primary:hover {
  background-color: var(--color-primary-dark);
  transform: translateY(-1px);
}

.btn-primary:active {
  transform: translateY(0);
}

/* Footer */
footer {
  text-align: center;
  padding: 2rem;
  background-color: var(--color-surface);
  color: var(--color-text-light);
  font-size: 0.9rem;
  border-top: 1px solid hsl(0, 0%, 90%);
}
"""
with open(os.path.join(base_dir, "src/app/globals.css"), "w", encoding="utf-8") as f: f.write(css)

# src/lib/api/client.ts
client_ts = """// Mock implementation of the generated SDK client
export const apiClient = {
  routes: {
    search: async (from: string, to: string, date: string) => {
      // In reality, this calls: fetch('https://api.msrtc.gov.in/v1/routes?from=...')
      console.log('Searching routes', from, to, date);
      return [];
    }
  },
  auth: {
    login: async (phone: string) => {
      console.log('Requesting OTP', phone);
      return { success: true };
    }
  }
};
"""
with open(os.path.join(base_dir, "src/lib/api/client.ts"), "w", encoding="utf-8") as f: f.write(client_ts)

print("Passenger Web app scaffolded successfully.")
