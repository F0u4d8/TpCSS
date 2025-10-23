import { useEffect, useState } from 'react';
import { useAuthStore } from '../stores/authStore';
import { AuthService } from '../services/auth.service';
import type { User } from '../types/auth.types';

export function ProfilePage() {
  const currentUser = useAuthStore((state) => state.user);
  const [profile, setProfile] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProfile = async () => {
      if (!currentUser) return;

      try {
        setLoading(true);
        const response = await AuthService.getProfile(currentUser.id);
        setProfile(response.user);
        
        if (response.warning) {
          setError(response.warning);
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [currentUser]);

  if (loading) {
    return <div className="page">Loading profile...</div>;
  }

  return (
    <div className="page">
      <div className="profile-container">
        <h2>👤 User Profile</h2>

        {error && (
          <div className="warning-banner">
            {error}
          </div>
        )}

        {profile && (
          <div className="profile-card">
            <div className="profile-field">
              <label>User ID:</label>
              <span>{profile.id}</span>
            </div>
            <div className="profile-field">
              <label>Email:</label>
              <span>{profile.email}</span>
            </div>
          </div>
        )}

        <div className="security-demo">
          <h3>🔓 Security Flaw Demo (Phase 1):</h3>
          <p>Try accessing another user's profile by changing the URL:</p>
          <code>http://localhost:3000/api/auth/profile/1</code>
          <code>http://localhost:3000/api/auth/profile/2</code>
          <p className="warning-text">
            ❌ Anyone can view any profile! Backend doesn't verify identity.
          </p>
        </div>
      </div>
    </div>
  );
}
