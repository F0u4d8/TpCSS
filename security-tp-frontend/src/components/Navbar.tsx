import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
export function Navbar() {
const { user, isAuthenticated, clearAuth } = useAuthStore();
const navigate = useNavigate();
const handleLogout = () => {
clearAuth();
navigate('/login');
};
return (
<nav className=
"navbar">
<div className=
"navbar-brand">
<Link to=
"/">🔓 Security TP</Link>
</div>
<div className=
"navbar-links">
{isAuthenticated ? (
<>
<Link to=
"/dashboard">Dashboard</Link>
<Link to=
"/profile">Profile</Link>
<Link to=
"/users">Users</Link>
<span className=
"navbar-user">{user?.email}</span>
<button onClick={handleLogout} className=
"btn-logout">
Logout
</button>
</>
) : (
<Link to=
"/login">Login</Link>
)}
</div>
</nav>
);
}