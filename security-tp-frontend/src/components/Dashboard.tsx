import { useAuthStore } from '../stores/authStore';

export function Dashboard() {
  const { user, clearAuth } = useAuthStore();

  const handleLogout = () => {
    // ⚠️ Phase 1: Just clear frontend state - backend doesn't know!
    clearAuth();
  };

  return (
    <div className="dashboard">
      <h2>✅ Logged in as: {user?.email}</h2>
      <div className="user-info">
        <p><strong>User ID:</strong> {user?.id}</p>
        <p><strong>Email:</strong> {user?.email}</p>
        <p className="warning">
          ⚠️ This "session" is only in your browser. 
          The backend has no idea you're logged in!
        </p>
      </div>
      <button onClick={handleLogout} className="logout-btn">
        Logout
      </button>
    </div>
  );
}
