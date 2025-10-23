import { useState, type FormEvent } from 'react';
import { AuthService } from '../services/auth.service';

interface RegisterProps {
onSuccess?: () => void;
}

export function Register({ onSuccess }: RegisterProps) {
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [message, setMessage] = useState('');
const [isLoading, setIsLoading] = useState(false);

const handleSubmit = async (e: FormEvent) => {
e.preventDefault();
setMessage('');
setIsLoading(true);


try {
  await AuthService.register({ email, password });
  setMessage('✅ Registration successful! You can now login.');
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
{message && <p className="message">{message}</p>}
</div>
);
}