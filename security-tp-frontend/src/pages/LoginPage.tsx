import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Login } from '../components/Login';
import { Register } from '../components/Register';

export function LoginPage() {
  const [activeTab, setActiveTab] = useState<'login' | 'register'>('login');
  const navigate = useNavigate();

  const handleLoginSuccess = () => {
    navigate('/dashboard');
  };

  const handleRegisterSuccess = () => {
    // Optionally switch to login tab after successful registration
    setActiveTab('login');
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <h1>Security Training Platform</h1>
          <p className="auth-subtitle">Welcome back! Please login to continue</p>
        </div>
        
        <div className="auth-tabs">
          <div 
            className={`auth-tab ${activeTab === 'login' ? 'active' : ''}`}
            onClick={() => setActiveTab('login')}
          >
            Login
          </div>
          <div 
            className={`auth-tab ${activeTab === 'register' ? 'active' : ''}`}
            onClick={() => setActiveTab('register')}
          >
            Register
          </div>
        </div>
        
        <div className="auth-forms">
          {activeTab === 'login' ? (
            <Login onLoginSuccess={handleLoginSuccess} />
          ) : (
            <Register onSuccess={handleRegisterSuccess} />
          )}
        </div>
        
        <div className="auth-footer">
          <p>By using our platform, you agree to our Terms of Service and Privacy Policy</p>
        </div>
      </div>
    </div>
  );
}
