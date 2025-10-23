import { useNavigate } from 'react-router-dom';
import { Login } from '../components/Login';
import { Register } from '../components/Register';

export function LoginPage() {
  const navigate = useNavigate();

  const handleLoginSuccess = () => {
    navigate('/dashboard');
  };

  return (
    <div className="page">
      <div className="auth-forms">
        <Register />
        <Login onLoginSuccess={handleLoginSuccess} />
      </div>
    </div>
  );
}
