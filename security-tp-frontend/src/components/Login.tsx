import { useState, type FormEvent } from 'react';
import { useAuthStore } from '../stores/authStore';
import { AuthService } from '../services/auth.service';
interface LoginProps {
onLoginSuccess?: () => void;
}
export function Login({ onLoginSuccess }: LoginProps) {
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [message, setMessage] = useState('');
const [isLoading, setIsLoading] = useState(false);
const { setUser, setError } = useAuthStore();
const handleSubmit = async (e: FormEvent) => {
e.preventDefault();
setMessage('');
setIsLoading(true);
try {
const response = await AuthService.login({ email, password });
setUser(response.user);
setMessage('✅ Login successful!');
if (onLoginSuccess) {
onLoginSuccess();

}
} catch (error: any) {
setError(error.message);
setMessage(`❌ ${error.message}`);
} finally {
setIsLoading(false);
}
};
return (
<div className="form-container">
  <h2>Login</h2>
  <form onSubmit={handleSubmit}>
    <div className="form-group">
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        disabled={isLoading}
      />
    </div>
    <div className="form-group">
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        disabled={isLoading}
      />
    </div>
    <button type="submit" disabled={isLoading}>
      {isLoading ? 'Logging in...' : 'Login'}
    </button>
  </form>
  {message && <p className="message" style={{ 
    backgroundColor: message.startsWith('❌') ? '#f8d7da' : '#d4edda',
    color: message.startsWith('❌') ? '#721c24' : '#155724',
    border: message.startsWith('❌') ? '1px solid #f5c6cb' : '1px solid #c3e6cb'
  }}>{message}</p>}
</div>
);
}