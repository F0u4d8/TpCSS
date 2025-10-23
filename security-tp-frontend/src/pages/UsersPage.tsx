import { useEffect, useState } from 'react';
import { AuthService } from '../services/auth.service';
import type { User } from '../types/auth.types';

export function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [warning, setWarning] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        const response = await AuthService.getAllUsers();
        setUsers(response.users);
        
        if (response.warning) {
          setWarning(response.warning);
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return <div className="page">Loading users...</div>;
  }

  if (error) {
    return <div className="page error">Error: {error}</div>;
  }

  return (
    <div className="page">
      <div className="users-container">
        <h2>👥 All Users (Mock Admin Page)</h2>

        {warning && (
          <div className="warning-banner">
            {warning}
          </div>
        )}

        <div className="users-list">
          {users.map((user) => (
            <div key={user.id} className="user-card">
              <div className="user-id">ID: {user.id}</div>
              <div className="user-email">{user.email}</div>
            </div>
          ))}
        </div>

        <div className="security-demo">
          <h3>🔓 Authorization Flaw Demo (Phase 1):</h3>
          <p>This page shows all users without any authorization check!</p>
          <ul>
            <li>❌ No role-based access control (RBAC)</li>
            <li>❌ No admin permission check</li>
            <li>❌ Any logged-in user can see this</li>
            <li>❌ Even non-logged users can access via curl!</li>
          </ul>
          <p className="code-example">
            Try: <code>curl http://localhost:3000/api/auth/users</code>
          </p>
        </div>
      </div>
    </div>
  );
}
