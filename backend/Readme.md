# Computer System Security - TP Series
## Building & Breaking a Full-Stack Authentication System

### 🎯 Learning Objectives
By the end of this TP series, you will:
- Build a complete authentication system with modern architecture patterns
- Use industry-standard tools (TypeScript, Prisma, Zustand)
- Learn proper code organization (routes, controllers, services, stores)
- Understand common security vulnerabilities by exploiting them
- Master authentication, authorization, and access control concepts

---

## ⚠️ Important Security Notice
**Phase 1 is intentionally insecure** to help you understand authentication flow before adding security layers. Never deploy Phase 1 code to production.

---

## 🏗️ Architecture Overview

### Backend Pattern: MVC with Services Layer
- **Routes**: Define API endpoints
- **Controllers**: Handle HTTP requests/responses
- **Services**: Business logic (framework-agnostic)
- **Middleware**: Request processing pipeline
- **Prisma**: Type-safe database access

### Frontend Pattern: Component + Store
- **Components**: UI elements
- **Zustand Store**: Global state management for auth
- **Types**: Shared TypeScript interfaces

---

## 🚀 Phase 1: Professional Architecture with Basic Flow

### Prerequisites
- Node.js 18+ and npm installed
- Basic knowledge of JavaScript/TypeScript, Express, React
- Code editor (VS Code recommended)

---

## Part A: Backend Setup (Express + TypeScript + Prisma + Clean Architecture)

### Step 1: Initialize Backend Project

mkdir security-tp-backend
cd security-tp-backend
npm init -y
npm install express cors dotenv
npm install --save-dev typescript ts-node @types/node @types/express @types/cors nodemon
npm install prisma --save-dev
npm install @prisma/client

text

[web:80][web:78]

### Step 2: Initialize TypeScript

npx tsc --init

text

Update `tsconfig.json`:

{
"compilerOptions": {
"target": "ES2020",
"module": "commonjs",
"lib": ["ES2020"],
"outDir": "./dist",
"rootDir": "./src",
"strict": true,
"esModuleInterop": true,
"skipLibCheck": true,
"forceConsistentCasingInFileNames": true,
"resolveJsonModule": true,
"moduleResolution": "node"
},
"include": ["src/**/*"],
"exclude": ["node_modules", "dist"]
}

text

[web:78][web:80]

### Step 3: Initialize Prisma

npx prisma init --datasource-provider sqlite

text

Edit `prisma/schema.prisma`:

generator client {
provider = "prisma-client-js"
}

datasource db {
provider = "sqlite"
url = env("DATABASE_URL")
}

model User {
id Int @id @default(autoincrement())
email String @unique
password String // ⚠️ INSECURE: Will store plaintext in Phase 1
createdAt DateTime @default(now())
}

text

[web:20][web:80]

Run migration:

npx prisma migrate dev --name init
npx prisma generate

text

[web:20]

### Step 4: Create Backend Folder Structure

mkdir -p src/{config,routes,controllers,services,middleware,types,utils}

text

[web:77][web:78][web:80]

Final structure:
src/
├── config/
│ └── database.ts # Prisma client singleton
├── types/
│ └── auth.types.ts # TypeScript interfaces
├── services/
│ └── auth.service.ts # Business logic
├── controllers/
│ └── auth.controller.ts # Request handlers
├── routes/
│ └── auth.routes.ts # Route definitions
├── middleware/
│ └── error.middleware.ts # Error handling
├── utils/
│ └── response.util.ts # Response helpers
└── server.ts # App entry point

text

[web:78][web:80][web:73]

### Step 5: Create Database Config

Create `src/config/database.ts`:

import { PrismaClient } from '@prisma/client';

// Singleton pattern for Prisma Client
const prismaClientSingleton = () => {
return new PrismaClient({
log: ['error', 'warn'],
});
};

declare global {
var prisma: undefined | ReturnType<typeof prismaClientSingleton>;
}

const prisma = globalThis.prisma ?? prismaClientSingleton();

export default prisma;

if (process.env.NODE_ENV !== 'production') globalThis.prisma = prisma;

text

[web:85][web:80]

### Step 6: Create Types

Create `src/types/auth.types.ts`:

export interface UserResponse {
id: number;
email: string;
}

export interface RegisterRequest {
email: string;
password: string;
}

export interface LoginRequest {
email: string;
password: string;
}

export interface AuthResponse {
message: string;
user?: UserResponse;
}

text

[web:78]

### Step 7: Create Service Layer (Business Logic)

Create `src/services/auth.service.ts`:

import prisma from '../config/database';
import { RegisterRequest, LoginRequest, UserResponse } from '../types/auth.types';

export class AuthService {
/**

Register a new user

⚠️ INSECURE: Storing plaintext password (Phase 1 only)
*/
async register(data: RegisterRequest): Promise<UserResponse> {
const { email, password } = data;

text
// Check if user already exists
text
const existingUser = await prisma.user.findUnique({
  where: { email },
});

if (existingUser) {
  throw new Error('EMAIL_EXISTS');
}

// Create user with plaintext password (INSECURE - Phase 1)
const user = await prisma.user.create({
  data: {
    email,
    password, // ⚠️ Plaintext password
  },
});

return {
  id: user.id,
  email: user.email,
};
}

/**

Login user

⚠️ INSECURE: Plaintext password comparison (Phase 1 only)
*/
async login(data: LoginRequest): Promise<UserResponse> {
const { email, password } = data;

text
// Find user
text
const user = await prisma.user.findUnique({
  where: { email },
});

if (!user) {
  throw new Error('INVALID_CREDENTIALS');
}

// Compare plaintext passwords (INSECURE - Phase 1)
if (user.password !== password) {
  throw new Error('INVALID_CREDENTIALS');
}

return {
  id: user.id,
  email: user.email,
};
}

/**

Get user by ID
*/
async getUserById(id: number): Promise<UserResponse | null> {
const user = await prisma.user.findUnique({
where: { id },
});

text
if (!user) {
text
  return null;
}

return {
  id: user.id,
  email: user.email,
};
}
}

text

[web:78][web:80][web:73]

### Step 8: Create Controllers (Request Handlers)

Create `src/controllers/auth.controller.ts`:

import { Request, Response } from 'express';
import { AuthService } from '../services/auth.service';
import { RegisterRequest, LoginRequest } from '../types/auth.types';

const authService = new AuthService();

// In-memory "session" storage (Phase 1 only)
const sessions = new Map<string, number>(); // sessionId -> userId

export class AuthController {
/**

Register endpoint handler
*/
async register(req: Request, res: Response): Promise<void> {
try {
const { email, password } = req.body as RegisterRequest;

if (!email || !password) {
res.status(400).json({ error: 'Email and password required' });
return;
}

const user = await authService.register({ email, password });

res.status(201).json({
message: 'User registered successfully',
user,
});
} catch (error: any) {
if (error.message === 'EMAIL_EXISTS') {
res.status(409).json({ error: 'Email already exists' });
return;
}
console.error('Register error:', error);
res.status(500).json({ error: 'Registration failed' });
}
}

/**

Login endpoint handler
*/
async login(req: Request, res: Response): Promise<void> {
try {
const { email, password } = req.body as LoginRequest;

if (!email || !password) {
res.status(400).json({ error: 'Email and password required' });
return;
}

const user = await authService.login({ email, password });

// Create simple session (Phase 1)
const sessionId = session_${Date.now()}_${Math.random()};
sessions.set(sessionId, user.id);

res.json({
message: 'Login successful',
user,
sessionId, // Sent to client for demonstration
});
} catch (error: any) {
if (error.message === 'INVALID_CREDENTIALS') {
res.status(401).json({ error: 'Invalid credentials' });
return;
}
console.error('Login error:', error);
res.status(500).json({ error: 'Login failed' });
}
}

/**

Get current user
*/
async me(req: Request, res: Response): Promise<void> {
try {
const sessionId = req.headers['x-session-id'] as string;

if (!sessionId || !sessions.has(sessionId)) {
res.status(401).json({ error: 'Not authenticated' });
return;
}

const userId = sessions.get(sessionId)!;
const user = await authService.getUserById(userId);

if (!user) {
res.status(404).json({ error: 'User not found' });
return;
}

res.json({ user });
} catch (error) {
console.error('Me error:', error);
res.status(500).json({ error: 'Failed to get user' });
}
}

/**

Logout
*/
logout(req: Request, res: Response): void {
const sessionId = req.headers['x-session-id'] as string;

text
if (sessionId) {
text
  sessions.delete(sessionId);
}

res.json({ message: 'Logged out successfully' });
}
}

text

[web:74][web:78][web:80]

### Step 9: Create Routes

Create `src/routes/auth.routes.ts`:

import { Router } from 'express';
import { AuthController } from '../controllers/auth.controller';

const router = Router();
const authController = new AuthController();

// Health check
router.get('/health', (req, res) => {
res.json({ status: 'ok', message: 'Auth service is running' });
});

// Auth routes
router.post('/register', (req, res) => authController.register(req, res));
router.post('/login', (req, res) => authController.login(req, res));
router.get('/me', (req, res) => authController.me(req, res));
router.post('/logout', (req, res) => authController.logout(req, res));

export default router;

text

[web:74][web:75][web:78]

### Step 10: Create Server

Create `src/server.ts`:

import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import authRoutes from './routes/auth.routes';
import prisma from './config/database';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/auth', authRoutes);

// Global health check
app.get('/api/health', (req, res) => {
res.json({ status: 'ok', message: 'Server is running' });
});

// 404 handler
app.use((req, res) => {
res.status(404).json({ error: 'Route not found' });
});

// Graceful shutdown
process.on('SIGINT', async () => {
console.log('\n🛑 Shutting down gracefully...');
await prisma.$disconnect();
process.exit();
});

// Start server
app.listen(PORT, () => {
console.log(🚀 Server running on http://localhost:${PORT});
console.log(📊 API endpoints: http://localhost:${PORT}/api/auth);
console.log('⚠️ WARNING: Phase 1 - INSECURE by design');
console.log('📊 Prisma Studio: npx prisma studio');
});

text

[web:78][web:80][web:86]

### Step 11: Update package.json

{
"scripts": {
"dev": "nodemon --exec ts-node src/server.ts",
"build": "tsc",
"start": "node dist/server.js",
"prisma:studio": "npx prisma studio",
"prisma:migrate": "npx prisma migrate dev"
}
}

text

### Step 12: Run Backend

npm run dev

text

Test with curl:

Register
curl -X POST http://localhost:3000/api/auth/register
-H "Content-Type: application/json"
-d '{"email":"test@example.com","password":"123456"}'

Login (save the sessionId from response)
curl -X POST http://localhost:3000/api/auth/login
-H "Content-Type: application/json"
-d '{"email":"test@example.com","password":"123456"}'

Me (use sessionId from login)
curl http://localhost:3000/api/auth/me
-H "x-session-id: YOUR_SESSION_ID_HERE"

text

[web:78]

---

## Part B: Frontend Setup (React + TypeScript + Vite + Zustand)

### Step 1: Create React Project

cd ..
npm create vite@latest security-tp-frontend -- --template react-ts
cd security-tp-frontend
npm install zustand

text

[web:82][web:87]

### Step 2: Create Folder Structure

mkdir -p src/{components,stores,types,services}

text

Structure:
src/
├── components/
│ ├── Login.tsx
│ ├── Register.tsx
│ └── Dashboard.tsx
├── stores/
│ └── authStore.ts # Zustand store
├── types/
│ └── auth.types.ts # Shared types
├── services/
│ └── auth.service.ts # API calls
└── App.tsx

text

[web:79][web:82]

### Step 3: Create Types

Create `src/types/auth.types.ts`:

export interface User {
id: number;
email: string;
}

export interface AuthState {
user: User | null;
sessionId: string | null;
isAuthenticated: boolean;
isLoading: boolean;
error: string | null;
}

export interface AuthActions {
setUser: (user: User, sessionId: string) => void;
clearAuth: () => void;
setLoading: (loading: boolean) => void;
setError: (error: string | null) => void;
}

export interface AuthStore extends AuthState, AuthActions {}

text

[web:79][web:82]

### Step 4: Create Zustand Auth Store

Create `src/stores/authStore.ts`:

import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { AuthStore, User } from '../types/auth.types';

/**

Global authentication store using Zustand

Persists auth state to localStorage
*/
export const useAuthStore = create<AuthStore>()(
devtools(
persist(
(set) => ({
// State
user: null,
sessionId: null,
isAuthenticated: false,
isLoading: false,
error: null,

text
 // Actions
 setUser: (user: User, sessionId: string) => {
   set({
     user,
     sessionId,
     isAuthenticated: true,
     error: null,
   });
 },

 clearAuth: () => {
   set({
     user: null,
     sessionId: null,
     isAuthenticated: false,
     error: null,
   });
 },

 setLoading: (loading: boolean) => {
   set({ isLoading: loading });
 },

 setError: (error: string | null) => {
   set({ error });
 },
}),
{
name: 'auth-storage', // localStorage key
partialize: (state) => ({
user: state.user,
sessionId: state.sessionId,
isAuthenticated: state.isAuthenticated,
}),
}
),
{ name: 'AuthStore' }
)
);

// Selector hooks for better performance
export const useUser = () => useAuthStore((state) => state.user);
export const useIsAuthenticated = () => useAuthStore((state) => state.isAuthenticated);
export const useSessionId = () => useAuthStore((state) => state.sessionId);

text

[web:79][web:82][web:84]

### Step 5: Create Auth Service (API Layer)

Create `src/services/auth.service.ts`:

const API_BASE_URL = 'http://localhost:3000/api/auth';

export interface RegisterData {
email: string;
password: string;
}

export interface LoginData {
email: string;
password: string;
}

export class AuthService {
/**

Register a new user
*/
static async register(data: RegisterData) {
const response = await fetch(${API_BASE_URL}/register, {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify(data),
});

text
if (!response.ok) {
text
  const error = await response.json();
  throw new Error(error.error || 'Registration failed');
}

return response.json();
}

/**

Login user
*/
static async login(data: LoginData) {
const response = await fetch(${API_BASE_URL}/login, {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify(data),
});

text
if (!response.ok) {
text
  const error = await response.json();
  throw new Error(error.error || 'Login failed');
}

return response.json();
}

/**

Get current user
*/
static async getMe(sessionId: string) {
const response = await fetch(${API_BASE_URL}/me, {
headers: {
'x-session-id': sessionId,
},
});

text
if (!response.ok) {
text
  const error = await response.json();
  throw new Error(error.error || 'Failed to get user');
}

return response.json();
}

/**

Logout
*/
static async logout(sessionId: string) {
const response = await fetch(${API_BASE_URL}/logout, {
method: 'POST',
headers: {
'x-session-id': sessionId,
},
});

text
if (!response.ok) {
text
  throw new Error('Logout failed');
}

return response.json();
}
}

text

[web:79]

### Step 6: Create Components

Create `src/components/Register.tsx`:

import { useState, FormEvent } from 'react';
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

text
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

text

Create `src/components/Login.tsx`:

import { useState, FormEvent } from 'react';
import { useAuthStore } from '../stores/authStore';
import { AuthService } from '../services/auth.service';

export function Login() {
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [message, setMessage] = useState('');
const [isLoading, setIsLoading] = useState(false);

const { setUser, setError } = useAuthStore();

const handleSubmit = async (e: FormEvent) => {
e.preventDefault();
setMessage('');
setIsLoading(true);

text
try {
  const response = await AuthService.login({ email, password });
  setUser(response.user, response.sessionId);
  setMessage('✅ Login successful!');
} catch (error: any) {
  setError(error.message);
  setMessage(`❌ ${error.message}`);
} finally {
  setIsLoading(false);
}
};

return (
<div className="form-container">
<h2>Login</h2>
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
{isLoading ? 'Logging in...' : 'Login'}
</button>
</form>
{message && <p className="message">{message}</p>}
</div>
);
}

text

Create `src/components/Dashboard.tsx`:

import { useAuthStore } from '../stores/authStore';
import { AuthService } from '../services/auth.service';

export function Dashboard() {
const { user, sessionId, clearAuth } = useAuthStore();

const handleLogout = async () => {
try {
if (sessionId) {
await AuthService.logout(sessionId);
}
clearAuth();
} catch (error) {
console.error('Logout error:', error);
clearAuth(); // Clear anyway
}
};

return (
<div className="dashboard">
<h2>✅ Logged in as: {user?.email}</h2>
<div className="user-info">
<p><strong>User ID:</strong> {user?.id}</p>
<p><strong>Email:</strong> {user?.email}</p>
<p><strong>Session ID:</strong> {sessionId?.substring(0, 20)}...</p>
</div>
<button onClick={handleLogout} className="logout-btn">
Logout
</button>
</div>
);
}

text

### Step 7: Update App.tsx

Replace `src/App.tsx`:

import { useAuthStore } from './stores/authStore';
import { Register } from './components/Register';
import { Login } from './components/Login';
import { Dashboard } from './components/Dashboard';
import './App.css';

function App() {
const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

return (
<div className="App">
<header>
<h1>🔓 Computer Security TP - Phase 1</h1>
<h2>TypeScript + Express + Prisma + Zustand</h2>
</header>

text
  <div className="warning-box">
    <strong>⚠️ WARNING:</strong> Phase 1 - Intentionally insecure for learning!
    <ul>
      <li>✅ Clean architecture (Routes/Controllers/Services)</li>
      <li>✅ Type-safe with TypeScript & Prisma</li>
      <li>✅ Global state with Zustand</li>
      <li>✅ Protected from SQL injection (Prisma)</li>
      <li>❌ Passwords stored in plaintext</li>
      <li>❌ Simple session (not secure)</li>
      <li>❌ No HTTPS</li>
    </ul>
  </div>

  <main>
    {!isAuthenticated ? (
      <div className="auth-forms">
        <Register />
        <Login />
      </div>
    ) : (
      <Dashboard />
    )}
  </main>
</div>
);
}

export default App;

text

### Step 8: Update App.css

Replace `src/App.css`:

.App {
max-width: 1200px;
margin: 0 auto;
padding: 20px;
}

header {
text-align: center;
margin-bottom: 30px;
}

.warning-box {
background: #fff3cd;
border: 2px solid #856404;
border-radius: 8px;
padding: 20px;
margin: 20px 0;
}

.warning-box ul {
text-align: left;
margin: 10px 0;
}

.auth-forms {
display: grid;
grid-template-columns: 1fr 1fr;
gap: 20px;
margin: 20px 0;
}

.form-container {
border: 1px solid #ccc;
border-radius: 8px;
padding: 20px;
background: #f9f9f9;
}

.form-group {
margin: 15px 0;
}

.form-group input {
width: 100%;
padding: 10px;
border: 1px solid #ddd;
border-radius: 4px;
font-size: 14px;
}

button {
width: 100%;
padding: 12px;
background: #007bff;
color: white;
border: none;
border-radius: 4px;
cursor: pointer;
font-size: 16px;
}

button:hover:not(:disabled) {
background: #0056b3;
}

button:disabled {
background: #ccc;
cursor: not-allowed;
}

.message {
margin-top: 15px;
padding: 10px;
border-radius: 4px;
text-align: center;
}

.dashboard {
border: 2px solid #28a745;
border-radius: 8px;
padding: 30px;
text-align: center;
background: #f0fff4;
}

.user-info {
margin: 20px 0;
text-align: left;
background: white;
padding: 20px;
border-radius: 4px;
}

.logout-btn {
background: #dc3545;
max-width: 200px;
margin: 20px auto 0;
}

.logout-btn:hover {
background: #c82333;
}

@media (max-width: 768px) {
.auth-forms {
grid-template-columns: 1fr;
}
}

text

### Step 9: Run Frontend

npm run dev

text

Visit `http://localhost:5173` [web:43]

---

## 🧪 Testing Phase 1

### 1. Test Registration
- Register a new user
- Try duplicate email (should fail)
- Check Prisma Studio to see plaintext password

### 2. Test Login with Zustand
- Login with credentials
- Open React DevTools → Components → AuthStore
- See state persisted in localStorage
- Refresh page → state persists

### 3. Test Session
- Login successfully
- Copy sessionId from network tab
- Test `/me` endpoint with curl

### 4. Test Logout
- Click logout
- Check localStorage is cleared
- Check Zustand store is reset

### 5. Code Architecture Review
**Backend:**
- Navigate through routes → controllers → services
- Show separation of concerns
- Explain why business logic is in services (testable, reusable)

**Frontend:**
- Show Zustand store managing global state
- Show service layer for API calls
- Explain component responsibilities

---

## 📝 Discussion Questions

### 1. Why separate Routes, Controllers, and Services?

**Routes**: Define API structure and endpoints [web:74][web:78]

**Controllers**: Handle HTTP layer (request/response) [web:78][web:80]

**Services**: Pure business logic, framework-agnostic [web:73][web:80]

Benefits:
- Easier testing (test services without HTTP)
- Reusability (services can be called from multiple controllers)
- Maintainability (clear separation of concerns)
- Swappable (can change Express to Fastify without touching services)

### 2. Why use Zustand over Context API?

- Less boilerplate than Redux [web:82]
- Better performance (no unnecessary re-renders) [web:82]
- Persistent state (localStorage integration) [web:79]
- DevTools support [web:79]
- Outside React components (can use in services) [web:82]

### 3. What security problems remain?

Same as before, but now with better code organization to fix them later!

### 4. Prisma Singleton Pattern

Why the singleton? Prevents too many database connections [web:85]

---

## 🔜 Phase 2 Preview: Adding Security

### Backend Updates

**Service Layer** (business logic):
// auth.service.ts
import bcrypt from 'bcrypt';

async register(data: RegisterRequest) {
const passwordHash = await bcrypt.hash(data.password, 10);
const user = await prisma.user.create({
data: { email: data.email, passwordHash }
});
// ...
}

text

**Controller Layer** (HTTP handling):
// auth.controller.ts - no changes needed!
// Services handle the security, controllers just coordinate

text

### Frontend Updates

**Zustand Store** - add token management:
interface AuthStore {
accessToken: string | null;
refreshToken: string | null;
// ...
}

text

---

## ✅ Phase 1 Completion Checklist

**Backend:**
- [ ] Proper folder structure (routes/controllers/services)
- [ ] Prisma migrations run successfully
- [ ] All endpoints working
- [ ] Code is modular and testable

**Frontend:**
- [ ] Zustand store managing auth state
- [ ] State persists across page refresh
- [ ] Clean component organization
- [ ] Service layer for API calls

**Understanding:**
- [ ] Can explain MVC pattern
- [ ] Can explain why separate services from controllers
- [ ] Can explain Zustand benefits
- [ ] Understand remaining security issues
- [ ] Ready for Phase 2 (adding security)

---

## 📁 Final Project Structure

security-tp-backend/
├── prisma/
│ ├── schema.prisma
│ └── dev.db
├── src/
│ ├── config/
│ │ └── database.ts
│ ├── types/
│ │ └── auth.types.ts
│ ├── services/
│ │ └── auth.service.ts # Business logic
│ ├── controllers/
│ │ └── auth.controller.ts # HTTP handlers
│ ├── routes/
│ │ └── auth.routes.ts # Route definitions
│ ├── middleware/ # (Future phases)
│ ├── utils/ # (Future phases)
│ └── server.ts # Entry point
└── package.json

security-tp-frontend/
├── src/
│ ├── components/
│ │ ├── Register.tsx
│ │ ├── Login.tsx
│ │ └── Dashboard.tsx
│ ├── stores/
│ │ └── authStore.ts # Zustand store
│ ├── types/
│ │ └── auth.types.ts
│ ├── services/
│ │ └── auth.service.ts # API layer
│ ├── App.tsx
│ └── App.css
└── package.json

text

---

## 🎓 Instructor Notes

### Time Allocation (Total: 3 hours)
- Backend structure explanation: 15 min
- Backend coding: 60 min
- Frontend structure explanation: 10 min
- Frontend coding with Zustand: 45 min
- Testing & architecture review: 30 min
- Discussion: 20 min

### Key Teaching Moments

1. **Draw architecture diagram** on whiteboard showing:
   - Request flow: Route → Controller → Service → Prisma
   - Response flow: Service → Controller → Route → Client
   - Zustand: Components → Store → State

2. **Code walk-through**:
   - Start with types (contracts)
   - Then services (business logic)
   - Then controllers (HTTP layer)
   - Finally routes (API surface)

3. **Zustand demonstration**:
   - Show React DevTools
   - Show localStorage persistence
   - Show re-renders (or lack thereof)

4. **Why this matters**:
   - Industry standard patterns
   - Easier to add security features later
   - Testable code
   - Team collaboration

### Common Issues

- **Prisma Client not generated**: Run `npx prisma generate`
- **Port conflicts**: Check 3000, 5173, 5555
- **CORS errors**: Verify cors() middleware
- **Zustand not persisting**: Check browser localStorage permissions
- **TypeScript errors**: Ensure all @types packages installed

---

**End of Phase 1 README**

Next TP: Add bcrypt, proper sessions, and JWT tokens using the same clean architecture!