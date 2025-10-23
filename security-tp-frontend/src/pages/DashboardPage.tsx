import { Link } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

export function DashboardPage() {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="page">
      <div className="dashboard">
        <h2>✅ Welcome, {user?.email}!</h2>
        <div className="user-info">
          <p><strong>User ID:</strong> {user?.id}</p>
          <p><strong>Email:</strong> {user?.email}</p>
        </div>

        <div className="dashboard-actions">
          <Link to="/profile" className="btn btn-primary">
            View Profile
          </Link>
          <Link to="/users" className="btn btn-secondary">
            View All Users (Mock Admin)
          </Link>
        </div>

        <div className="security-note">
          <h3>⚠️ Security Note (Phase 1):</h3>
          <ul>
            <li>This "session" only exists in your browser (Zustand + localStorage)</li>
            <li>The backend has NO way to verify you're actually logged in</li>
            <li>Try editing localStorage manually and refresh!</li>
            <li>Anyone can access /profile/:id and /users endpoints directly</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
