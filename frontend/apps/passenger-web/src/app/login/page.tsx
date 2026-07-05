import { LoginForm } from '../../features/auth/components/LoginForm';

export default function LoginPage() {
  return (
    <div style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--color-background)' }}>
      <LoginForm />
    </div>
  );
}
