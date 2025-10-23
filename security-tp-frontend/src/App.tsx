import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './stores/authStore';
import { Navbar } from './components/Navbar';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { ProfilePage } from './pages/ProfilePage';
import { UsersPage } from './pages/UsersPage';
import './App.css';
function App() {
const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
return (
<BrowserRouter>
<div className=
"App">
<Navbar />
<header>
<h1>🔓 Computer Security TP - Phase 1</h1>
<h2>TypeScript + Express + Prisma + Zustand</h2>
</header>
<div className=
"warning-box">
<strong>⚠️ WARNING:</strong> Phase 1 - Intentionally insecure for learning!
<ul>
<li>✅ Clean architecture (Routes/Controllers/Services)</li>
<li>✅ Type-safe with TypeScript & Prisma</li>
<li>✅ Global state with Zustand</li>
<li>✅ Protected from SQL injection (Prisma)</li>
<li>✅ Frontend route protection (ProtectedRoute)</li>
<li>❌ Passwords stored in plaintext</li>
<li>❌ <strong>Backend has NO authentication/authorization!</strong></li>
<li>❌ Anyone can access backend endpoints directly</li>
<li>❌ No HTTPS</li>
</ul>
</div>
<main>
<Routes>
<Route
path=
"/"
element={
isAuthenticated ?
<Navigate to=
"/dashboard" replace /> :
<Navigate to=
"/login" replace />
}
/>
<Route path=
"/login" element={<LoginPage />} />
<Route
path=
"/dashboard"
element={
<ProtectedRoute>
<DashboardPage />
</ProtectedRoute>
}
/>
<Route
path=
"/profile"
element={
<ProtectedRoute>
<ProfilePage />
</ProtectedRoute>
}
/>
<Route
path=
"/users"
element={
<ProtectedRoute>
<UsersPage />
</ProtectedRoute>
}
/>
</Routes>
</main>
</div>
</BrowserRouter>
);
}
export default App;