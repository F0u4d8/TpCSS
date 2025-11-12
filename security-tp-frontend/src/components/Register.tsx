import { useState, type FormEvent } from 'react';
import { AuthService } from '../services/auth.service';

interface RegisterProps {
  onSuccess?: () => void;
}

export function Register({ onSuccess }: RegisterProps) {
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [username, setUsername] = useState('');

const [message, setMessage] = useState('');
const [isLoading, setIsLoading] = useState(false);

const handleSubmit = async (e: FormEvent) => {
e.preventDefault();
setMessage('');
setIsLoading(true);


try {
  await AuthService.register({ username, email, password });
  setMessage('✅ Registration successful! You can now login.');
  setUsername('');
  setEmail('');
  setPassword('');
  onSuccess?.();
} catch (error: any) {
  setMessage(`❌ ${error.message}`);
} finally {
  setIsLoading(false);
}
};

return (
<div className="form-container">
  <h2>Register</h2>
  <form onSubmit={handleSubmit}>
    <div className="form-group">
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
        disabled={isLoading}
      />
    </div>

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
      {isLoading ? 'Registering...' : 'Register'}
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