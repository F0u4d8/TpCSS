# Computer System Security - TP Series

## Building & Breaking a Full-Stack Authentication System

### 🎯 Learning Objectives

By the end of this TP series, you will:

- Build a complete authentication system with modern architecture patterns
- Use industry-standard tools (TypeScript, Prisma, Zustand, React Router)
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

### Frontend Pattern: Component + Store + Router

- **Components**: UI elements
- **Pages**: Page-level components
- **Zustand Store**: Global state management for auth
- **React Router**: Client-side routing with protected routes
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

```bash
mkdir backend
cd backend
npm init -y
npm install express cors dotenv @prisma/client
npm install --save-dev typescript ts-node @types/node @types/express @types/cors nodemon prisma
```

### Step 2: Initialize TypeScript

```bash
npx tsc --init
```

Update `tsconfig.json`:

```json
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
```

### Step 3: Initialize Prisma

```bash
npx prisma init --datasource-provider sqlite
```

Edit `prisma/schema.prisma`:

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  username  String?  @unique
  email     String   @unique
  password  String   // ⚠️ INSECURE: Will store plaintext in Phase 1
  createdAt DateTime @default(now())
}
```

Create `.env` file in the backend directory:

```env
# Database
DATABASE_URL="file:./prisma/dev.db"

# Server
PORT=3000
NODE_ENV=development
```

Run migration:

```bash
npx prisma migrate dev --name init
npx prisma generate
```

### Step 4: Create Backend Folder Structure

For Windows (PowerShell):

```powershell
mkdir src\config, src\routes, src\controllers, src\services, src\types
```

For Linux/Mac:

```bash
mkdir -p src/{config,routes,controllers,services,types}
```

Final structure:

```
src/
├── config/
│   └── database.ts       # Prisma client singleton
├── types/
│   └── auth.types.ts     # TypeScript interfaces
├── services/
│   └── auth.service.ts   # Business logic
├── controllers/
│   └── auth.controller.ts # Request handlers
├── routes/
│   └── auth.routes.ts    # Route definitions
└── server.ts             # App entry point
```

### Step 5: Create Database Config

Create `src/config/database.ts`:

```typescript
import { PrismaClient } from "@prisma/client";

// Singleton pattern for Prisma Client
const prismaClientSingleton = () => {
  return new PrismaClient({
    log: ["error", "warn"],
  });
};

declare global {
  var prisma: undefined | ReturnType<typeof prismaClientSingleton>;
}

const prisma = globalThis.prisma ?? prismaClientSingleton();

export default prisma;

if (process.env.NODE_ENV !== "production") globalThis.prisma = prisma;
```

### Step 6: Create Types

Create `src/types/auth.types.ts`:

```typescript
export interface UserResponse {
  id: number;
  email: string;
}

export interface RegisterRequest {
  username?: string;
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
```

### Step 7: Create Service Layer (Business Logic)

Create `src/services/auth.service.ts`:

```typescript
import prisma from "../config/database";
import {
  RegisterRequest,
  LoginRequest,
  UserResponse,
} from "../types/auth.types";

export class AuthService {
  /**
   * Register a new user
   * ⚠️ INSECURE: Storing plaintext password (Phase 1 only)
   */
  async register(data: RegisterRequest): Promise<UserResponse> {
    const { username, email, password } = data;

    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email },
    });

    if (existingUser) {
      throw new Error("EMAIL_EXISTS");
    }

    // Create user with plaintext password (INSECURE - Phase 1)
    const user = await prisma.user.create({
      data: {
        email,
        password, // ⚠️ Plaintext password
        username: username,
      },
    });

    return {
      id: user.id,
      email: user.email,
    };
  }

  /**
   * Login user
   * ⚠️ INSECURE: Plaintext password comparison (Phase 1 only)
   */
  async login(data: LoginRequest): Promise<UserResponse> {
    const { email, password } = data;

    // Find user
    const user = await prisma.user.findUnique({
      where: { email },
    });

    if (!user) {
      throw new Error("INVALID_CREDENTIALS");
    }

    // Compare plaintext passwords (INSECURE - Phase 1)
    if (user.password !== password) {
      throw new Error("INVALID_CREDENTIALS");
    }

    return {
      id: user.id,
      email: user.email,
    };
  }

  /**
   * Get user by ID
   */
  async getUserById(id: number): Promise<UserResponse | null> {
    const user = await prisma.user.findUnique({
      where: { id },
    });

    if (!user) {
      return null;
    }

    return {
      id: user.id,
      email: user.email,
    };
  }

  /**
   * Get all users
   * ⚠️ INSECURE: No authorization (Phase 1)
   */
  async getAllUsers(): Promise<UserResponse[]> {
    const users = await prisma.user.findMany({
      select: {
        id: true,
        email: true,
        createdAt: true,
      },
    });

    return users.map((user) => ({
      id: user.id,
      email: user.email,
    }));
  }
}
```

### Step 8: Create Controllers (Request Handlers)

Create `src/controllers/auth.controller.ts`:

```typescript
import { Request, Response } from "express";
import { AuthService } from "../services/auth.service";
import { RegisterRequest, LoginRequest } from "../types/auth.types";

const authService = new AuthService();

export class AuthController {
  /**
   * Register endpoint handler
   */
  async register(req: Request, res: Response): Promise<void> {
    try {
      const { username, email, password } = req.body as RegisterRequest;

      if (!email || !password) {
        res.status(400).json({ error: "Email and password required" });
        return;
      }

      const user = await authService.register({ username, email, password });

      res.status(201).json({
        message: "User registered successfully",
        user,
      });
    } catch (error: any) {
      if (error.message === "EMAIL_EXISTS") {
        res.status(409).json({ error: "Email already exists" });
        return;
      }
      console.error("Register error:", error);
      res.status(500).json({ error: "Registration failed" });
    }
  }

  /**
   * Login endpoint handler
   * ⚠️ INSECURE: Just returns user data, no token/session
   */
  async login(req: Request, res: Response): Promise<void> {
    try {
      const { email, password } = req.body as LoginRequest;

      if (!email || !password) {
        res.status(400).json({ error: "Email and password required" });
        return;
      }

      const user = await authService.login({ email, password });

      // ⚠️ Phase 1: Just return user data, no authentication mechanism!
      res.json({
        message: "Login successful",
        user,
      });
    } catch (error: any) {
      if (error.message === "INVALID_CREDENTIALS") {
        res.status(401).json({ error: "Invalid credentials" });
        return;
      }
      console.error("Login error:", error);
      res.status(500).json({ error: "Login failed" });
    }
  }

  /**
   * Get user profile
   * ⚠️ INSECURE: Anyone can access any profile (Phase 1)
   */
  async getProfile(req: Request, res: Response): Promise<void> {
    try {
      // In Phase 1, we trust the userId from the request
      // ⚠️ Anyone can claim to be any user!
      const userId = parseInt(req.params.id);

      if (isNaN(userId)) {
        res.status(400).json({ error: "Invalid user ID" });
        return;
      }

      const user = await authService.getUserById(userId);

      if (!user) {
        res.status(404).json({ error: "User not found" });
        return;
      }

      res.json({
        user,
        warning:
          "⚠️ Phase 1: Backend cannot verify this request is from the actual user!",
      });
    } catch (error) {
      console.error("Profile error:", error);
      res.status(500).json({ error: "Failed to get profile" });
    }
  }

  /**
   * Get all users (admin-like endpoint)
   * ⚠️ INSECURE: No authorization check!
   */
  async getAllUsers(req: Request, res: Response): Promise<void> {
    try {
      const users = await authService.getAllUsers();
      res.json({
        users,
        warning: "⚠️ Phase 1: Anyone can access this - no authorization!",
      });
    } catch (error) {
      console.error("Get users error:", error);
      res.status(500).json({ error: "Failed to get users" });
    }
  }
}
```

### Step 9: Create Routes

Create `src/routes/auth.routes.ts`:

```typescript
import { Router } from "express";
import { AuthController } from "../controllers/auth.controller";

const router = Router();
const authController = new AuthController();

// Health check
router.get("/health", (req, res) => {
  res.json({ status: "ok", message: "Auth service is running" });
});

// Public routes
router.post("/register", (req, res) => authController.register(req, res));
router.post("/login", (req, res) => authController.login(req, res));

// ⚠️ "Protected" routes (not actually protected in Phase 1)
router.get("/profile/:id", (req, res) => authController.getProfile(req, res));
router.get("/users", (req, res) => authController.getAllUsers(req, res));

export default router;
```

### Step 10: Create Server

Create `src/server.ts`:

```typescript
import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import authRoutes from "./routes/auth.routes";
import prisma from "./config/database";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use("/api/auth", authRoutes);

// Global health check
app.get("/api/health", (req, res) => {
  res.json({ status: "ok", message: "Server is running" });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: "Route not found" });
});

// Graceful shutdown
process.on("SIGINT", async () => {
  console.log("\n🛑 Shutting down gracefully...");
  await prisma.$disconnect();
  process.exit();
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log(`📊 API endpoints: http://localhost:${PORT}/api/auth`);
  console.log("⚠️ WARNING: Phase 1 - INSECURE by design");
  console.log("📊 Prisma Studio: npx prisma studio");
});
```

### Step 11: Update package.json

Add these scripts to `package.json`:

```json
{
  "scripts": {
    "dev": "nodemon --exec ts-node src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js",
    "prisma:generate": "npx prisma generate",
    "prisma:migrate": "npx prisma migrate dev",
    "prisma:studio": "npx prisma studio",
    "prisma:reset": "npx prisma migrate reset && npx prisma generate",
    "postinstall": "prisma generate"
  }
}
```

### Step 12: Run Backend

```bash
npm run dev
```

Test with curl:

```bash
# Register
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"123456"}'

# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"123456"}'

# Get Profile (use the user ID from registration)
curl http://localhost:3000/api/auth/profile/1

# Get All Users
curl http://localhost:3000/api/auth/users
```

---

## Part B: Frontend Setup (React + TypeScript + Vite + Zustand + React Router)

### Step 1: Create React Project

```bash
cd ..
npm create vite@latest security-tp-frontend -- --template react-ts
cd security-tp-frontend
npm install zustand react-router-dom
```

### Step 2: Create Folder Structure

For Windows (PowerShell):

```powershell
mkdir src\components, src\pages, src\stores, src\types, src\services
```

For Linux/Mac:

```bash
mkdir -p src/{components,pages,stores,types,services}
```

Structure:

```
src/
├── components/
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Navbar.tsx
│   └── ProtectedRoute.tsx
├── pages/
│   ├── LoginPage.tsx
│   ├── DashboardPage.tsx
│   ├── ProfilePage.tsx
│   └── UsersPage.tsx
├── stores/
│   └── authStore.ts      # Zustand store
├── types/
│   └── auth.types.ts     # Shared types
├── services/
│   └── auth.service.ts   # API calls
├── App.tsx
└── App.css
```

### Step 3: Create Types

Create `src/types/auth.types.ts`:

```typescript
export interface User {
  id: number;
  email: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  error: string | null;
}

export interface AuthActions {
  setUser: (user: User) => void;
  clearAuth: () => void;
  setError: (error: string | null) => void;
}

export interface AuthStore extends AuthState, AuthActions {}
```

### Step 4: Create Zustand Auth Store

Create `src/stores/authStore.ts`:

```typescript
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";
import type { User } from "../types/auth.types";

interface AuthStore {
  user: User | null;
  isAuthenticated: boolean;
  error: string | null;

  setUser: (user: User) => void;
  clearAuth: () => void;
  setError: (error: string | null) => void;
}

export const useAuthStore = create<AuthStore>()(
  devtools(
    persist(
      (set) => ({
        // State
        user: null,
        isAuthenticated: false,
        error: null,

        // Actions
        setUser: (user: User) => {
          set({
            user,
            isAuthenticated: true,
            error: null,
          });
        },

        clearAuth: () => {
          set({
            user: null,
            isAuthenticated: false,
            error: null,
          });
        },

        setError: (error: string | null) => {
          set({ error });
        },
      }),
      {
        name: "auth-storage",
      }
    ),
    { name: "AuthStore" }
  )
);
```

### Step 5: Create Auth Service (API Layer)

Create `src/services/auth.service.ts`:

```typescript
const API_BASE_URL = "http://localhost:3000/api/auth";

export interface RegisterData {
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export class AuthService {
  static async register(data: RegisterData) {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Registration failed");
    }

    return response.json();
  }

  static async login(data: LoginData) {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Login failed");
    }

    return response.json();
  }

  /**
   * Get user profile
   * ⚠️ Phase 1: Backend can't verify this request
   */
  static async getProfile(userId: number) {
    const response = await fetch(`${API_BASE_URL}/profile/${userId}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Failed to get profile");
    }

    return response.json();
  }

  /**
   * Get all users (mock admin endpoint)
   * ⚠️ Phase 1: No authorization check
   */
  static async getAllUsers() {
    const response = await fetch(`${API_BASE_URL}/users`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Failed to get users");
    }

    return response.json();
  }
}
```

### Step 6: Create Components

Create `src/components/Register.tsx`:

```typescript
import { useState, FormEvent } from "react";
import { AuthService } from "../services/auth.service";

interface RegisterProps {
  onSuccess?: () => void;
}

export function Register({ onSuccess }: RegisterProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMessage("");
    setIsLoading(true);

    try {
      await AuthService.register({ email, password });
      setMessage("✅ Registration successful! You can now login.");
      setEmail("");
      setPassword("");
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
          {isLoading ? "Registering..." : "Register"}
        </button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}
```

Create `src/components/Login.tsx`:

```typescript
import { useState, FormEvent } from "react";
import { useAuthStore } from "../stores/authStore";
import { AuthService } from "../services/auth.service";

interface LoginProps {
  onLoginSuccess?: () => void;
}

export function Login({ onLoginSuccess }: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const { setUser, setError } = useAuthStore();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMessage("");
    setIsLoading(true);

    try {
      const response = await AuthService.login({ email, password });
      setUser(response.user);
      setMessage("✅ Login successful!");
      onLoginSuccess?.();
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
          {isLoading ? "Logging in..." : "Login"}
        </button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}
```

Create `src/components/Navbar.tsx`:

```typescript
import { Link } from "react-router-dom";
import { useAuthStore } from "../stores/authStore";

export function Navbar() {
  const { user, isAuthenticated, clearAuth } = useAuthStore();

  const handleLogout = () => {
    clearAuth();
  };

  return (
    <nav className="navbar">
      <div className="nav-links">
        {isAuthenticated ? (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/profile">Profile</Link>
            <Link to="/users">Users</Link>
          </>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </div>
      {isAuthenticated && (
        <div className="nav-user">
          <span>{user?.email}</span>
          <button onClick={handleLogout} className="btn-logout">
            Logout
          </button>
        </div>
      )}
    </nav>
  );
}
```

Create `src/components/ProtectedRoute.tsx`:

```typescript
import { Navigate } from "react-router-dom";
import { useAuthStore } from "../stores/authStore";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
```

### Step 7: Create Pages

Create `src/pages/LoginPage.tsx`:

```typescript
import { useNavigate } from "react-router-dom";
import { Login } from "../components/Login";
import { Register } from "../components/Register";

export function LoginPage() {
  const navigate = useNavigate();

  const handleLoginSuccess = () => {
    navigate("/dashboard");
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
```

Create `src/pages/DashboardPage.tsx`:

```typescript
import { Link } from "react-router-dom";
import { useAuthStore } from "../stores/authStore";

export function DashboardPage() {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="page">
      <div className="dashboard">
        <h2>✅ Welcome, {user?.email}!</h2>
        <div className="user-info">
          <p>
            <strong>User ID:</strong> {user?.id}
          </p>
          <p>
            <strong>Email:</strong> {user?.email}
          </p>
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
            <li>
              This "session" only exists in your browser (Zustand +
              localStorage)
            </li>
            <li>The backend has NO way to verify you're actually logged in</li>
            <li>Try editing localStorage manually and refresh!</li>
            <li>
              Anyone can access /profile/:id and /users endpoints directly
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
```

Create `src/pages/ProfilePage.tsx`:

```typescript
import { useState, useEffect } from "react";
import { useAuthStore } from "../stores/authStore";
import { AuthService } from "../services/auth.service";

export function ProfilePage() {
  const user = useAuthStore((state) => state.user);
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (user) {
      loadProfile();
    }
  }, [user]);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await AuthService.getProfile(user!.id);
      setProfile(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="page">Loading...</div>;
  if (error) return <div className="page error">Error: {error}</div>;

  return (
    <div className="page">
      <div className="profile">
        <h2>My Profile</h2>
        <div className="profile-info">
          <p>
            <strong>ID:</strong> {profile?.user?.id}
          </p>
          <p>
            <strong>Email:</strong> {profile?.user?.email}
          </p>
        </div>
        {profile?.warning && (
          <div className="warning-box">
            <p>{profile.warning}</p>
          </div>
        )}
      </div>
    </div>
  );
}
```

Create `src/pages/UsersPage.tsx`:

```typescript
import { useState, useEffect } from "react";
import { AuthService } from "../services/auth.service";

export function UsersPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [warning, setWarning] = useState("");

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const data = await AuthService.getAllUsers();
      setUsers(data.users || []);
      setWarning(data.warning || "");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="page">Loading...</div>;
  if (error) return <div className="page error">Error: {error}</div>;

  return (
    <div className="page">
      <div className="users">
        <h2>All Users (Mock Admin)</h2>

        {warning && (
          <div className="warning-box">
            <p>{warning}</p>
          </div>
        )}

        <div className="users-list">
          {users.map((user) => (
            <div key={user.id} className="user-card">
              <p>
                <strong>ID:</strong> {user.id}
              </p>
              <p>
                <strong>Email:</strong> {user.email}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

### Step 8: Update App.tsx

Replace `src/App.tsx`:

```typescript
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuthStore } from "./stores/authStore";
import { Navbar } from "./components/Navbar";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { LoginPage } from "./pages/LoginPage";
import { DashboardPage } from "./pages/DashboardPage";
import { ProfilePage } from "./pages/ProfilePage";
import { UsersPage } from "./pages/UsersPage";
import "./App.css";

function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  return (
    <BrowserRouter>
      <div className="App">
        <Navbar />
        <header>
          <h1>🔓 Computer Security TP - Phase 1</h1>
          <h2>TypeScript + Express + Prisma + Zustand</h2>
        </header>

        <div className="warning-box">
          <strong>⚠️ WARNING:</strong> Phase 1 - Intentionally insecure for
          learning!
          <ul>
            <li>✅ Clean architecture (Routes/Controllers/Services)</li>
            <li>✅ Type-safe with TypeScript & Prisma</li>
            <li>✅ Global state with Zustand</li>
            <li>✅ Protected from SQL injection (Prisma)</li>
            <li>✅ Frontend route protection (ProtectedRoute)</li>
            <li>❌ Passwords stored in plaintext</li>
            <li>
              ❌ <strong>Backend has NO authentication/authorization!</strong>
            </li>
            <li>❌ Anyone can access backend endpoints directly</li>
            <li>❌ No HTTPS</li>
          </ul>
        </div>

        <main>
          <Routes>
            <Route
              path="/"
              element={
                isAuthenticated ? (
                  <Navigate to="/dashboard" replace />
                ) : (
                  <Navigate to="/login" replace />
                )
              }
            />
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/users"
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
```

### Step 9: Update App.css

Replace `src/App.css`:

```css
.App {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  text-align: center;
  margin-bottom: 30px;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #f0f0f0;
  border-radius: 8px;
  margin-bottom: 20px;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  text-decoration: none;
  color: #007bff;
  font-weight: 500;
}

.nav-links a:hover {
  text-decoration: underline;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 15px;
}

.btn-logout {
  padding: 8px 16px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-logout:hover {
  background: #c82333;
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

.page {
  margin: 20px 0;
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
  box-sizing: border-box;
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

.dashboard-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin: 20px 0;
}

.btn {
  padding: 12px 24px;
  border-radius: 4px;
  text-decoration: none;
  color: white;
  font-weight: 500;
}

.btn-primary {
  background: #007bff;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
}

.btn-secondary:hover {
  background: #5a6268;
}

.security-note {
  background: #fff3cd;
  border: 2px solid #856404;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
  text-align: left;
}

.profile {
  max-width: 600px;
  margin: 0 auto;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
}

.profile-info {
  margin: 20px 0;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 4px;
}

.users {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.users-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.user-card {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
}

.error {
  color: red;
  text-align: center;
  padding: 20px;
}

@media (max-width: 768px) {
  .auth-forms {
    grid-template-columns: 1fr;
  }

  .dashboard-actions {
    flex-direction: column;
  }
}
```

### Step 10: Run Frontend

```bash
npm run dev
```

Visit `http://localhost:5173`

---

## 🔒 Security Testing (NEW!)

We've created automated security testing tools to help you identify and understand vulnerabilities!

### Option 1: Python Script (Recommended for Quick Testing)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run automated security tests
python security_test.py
```

### Option 2: Jupyter Notebook (Interactive Learning)

```bash
# Install Jupyter
pip install jupyter notebook requests pandas colorama

# Start Jupyter
jupyter notebook

# Open security_testing.ipynb in your browser
```

### What You'll Learn

The security testing tools will help you discover:

- 🚨 No authentication on protected endpoints
- 🚨 Passwords stored in plaintext
- 🚨 IDOR vulnerabilities
- 🚨 No rate limiting (brute force possible)
- ✅ SQL injection protection (Prisma)
- And more!

**See `SECURITY_TESTING_GUIDE.md` for complete instructions.**

---

## 🧪 Manual Testing Phase 1

### 1. Test Registration

- Register a new user
- Try duplicate email (should fail)
- Open Prisma Studio (`npm run prisma:studio` in backend) to see plaintext password

### 2. Test Login with Zustand

- Login with credentials
- Open React DevTools → Components → find component using useAuthStore
- Check localStorage in browser DevTools → Application → Local Storage
- Refresh page → state persists

### 3. Test Navigation

- Login and navigate to Dashboard
- Click "View Profile" - see your profile
- Click "View All Users" - see all registered users
- Notice the security warnings

### 4. Test Security Vulnerabilities

**Frontend Protection (Works):**

- Logout
- Try accessing `/dashboard` directly → redirects to login ✅

**Backend Vulnerability (Doesn't Work):**

- Use curl or Postman to access:
  ```bash
  curl http://localhost:3000/api/auth/users
  curl http://localhost:3000/api/auth/profile/1
  ```
- Notice: Anyone can access these endpoints! ⚠️

### 5. Explore the Database

```bash
cd backend
npm run prisma:studio
```

- View users table
- See plaintext passwords ⚠️
- Notice the schema structure

---

## 📝 Discussion Questions

### 1. Why separate Routes, Controllers, and Services?

**Routes**: Define API structure and endpoints
**Controllers**: Handle HTTP layer (request/response)
**Services**: Pure business logic, framework-agnostic

Benefits:

- Easier testing (test services without HTTP)
- Reusability (services can be called from multiple controllers)
- Maintainability (clear separation of concerns)
- Swappable (can change Express to Fastify without touching services)

### 2. Why use Zustand over Context API?

- Less boilerplate than Redux
- Better performance (no unnecessary re-renders)
- Persistent state (localStorage integration)
- DevTools support
- Can be used outside React components

### 3. What security problems exist in Phase 1?

**Critical Issues:**

1. **Plaintext passwords** - Visible in database
2. **No backend authentication** - Anyone can call any endpoint
3. **No authorization** - No role-based access control
4. **Client-side only "auth"** - Just localStorage, easily manipulated
5. **No HTTPS** - Data sent in plain text over network

**Frontend Protection:**

- ✅ Protected routes work (but only prevent UI navigation)
- ❌ Backend is wide open to direct API calls

### 4. How does ProtectedRoute work?

- Checks `isAuthenticated` from Zustand store
- If false, redirects to login page
- If true, renders the protected component
- **Limitation**: Only protects frontend navigation, not backend API

### 5. Prisma Singleton Pattern

Why? Prevents creating too many database connections which can exhaust resources.

---

## 🔜 Phase 2 Preview: Adding Security

### Backend Security Improvements

1. **Password hashing** with bcrypt
2. **JWT tokens** for authentication
3. **Middleware** for route protection
4. **Refresh tokens** for session management
5. **Role-based access control** (RBAC)

### Frontend Security Improvements

1. **JWT storage** and automatic inclusion in requests
2. **Token refresh** logic
3. **Proper error handling** for 401/403
4. **Secure logout** (token invalidation)

---

## ✅ Phase 1 Completion Checklist

**Backend:**

- [ ] Proper folder structure (routes/controllers/services)
- [ ] Prisma migrations run successfully
- [ ] All endpoints working (register, login, profile, users)
- [ ] Code is modular and testable
- [ ] Can access Prisma Studio

**Frontend:**

- [ ] Zustand store managing auth state
- [ ] State persists across page refresh
- [ ] React Router navigation working
- [ ] Protected routes redirect when not authenticated
- [ ] All pages render correctly (Login, Dashboard, Profile, Users)

**Understanding:**

- [ ] Can explain MVC pattern
- [ ] Can explain why separate services from controllers
- [ ] Can explain Zustand benefits
- [ ] Understand client-side vs server-side auth
- [ ] Identified all security vulnerabilities
- [ ] Ready for Phase 2 (adding security)

---

## 📁 Final Project Structure

```
TpCSS/
├── backend/
│   ├── prisma/
│   │   ├── schema.prisma
│   │   ├── dev.db
│   │   └── migrations/
│   ├── src/
│   │   ├── config/
│   │   │   └── database.ts
│   │   ├── types/
│   │   │   └── auth.types.ts
│   │   ├── services/
│   │   │   └── auth.service.ts
│   │   ├── controllers/
│   │   │   └── auth.controller.ts
│   │   ├── routes/
│   │   │   └── auth.routes.ts
│   │   └── server.ts
│   ├── .env
│   ├── package.json
│   └── tsconfig.json
│
├── security-tp-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Navbar.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── ProfilePage.tsx
│   │   │   └── UsersPage.tsx
│   │   ├── stores/
│   │   │   └── authStore.ts
│   │   ├── types/
│   │   │   └── auth.types.ts
│   │   ├── services/
│   │   │   └── auth.service.ts
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── security_test.py              # 🔒 Automated security testing
├── security_testing.ipynb        # 🔒 Interactive Jupyter notebook
├── brute_force_demo.py           # 🔒 Brute force attack demo
├── brute_force_exercise.py       # 🔒 Student brute force exercise
├── requirements.txt              # 🔒 Python dependencies
│
├── Readme.md                     # 📚 Main documentation
├── BRUTE_FORCE_GUIDE.md          # 📚 Brute force attack guide
├── SETUP_INSTRUCTIONS.md         # 📚 Quick setup guide
├── STUDENT_CHECKLIST.md          # 📚 Verification checklist
├── FIXES_APPLIED.md              # 📚 What was fixed
├── SECURITY_TESTING_GUIDE.md     # 📚 Security testing guide
└── SECURITY_TOOLS_README.md      # 📚 Security tools quick start
```

---

## 🎓 Instructor Notes

### Time Allocation (Total: 4 hours)

- Backend structure explanation: 20 min
- Backend coding: 70 min
- Frontend structure explanation: 15 min
- Frontend coding: 75 min
- Testing & demonstration: 30 min
- Discussion & Q&A: 30 min

### Key Teaching Moments

1. **Architecture Diagram** - Draw on whiteboard:

   - Request flow: Client → Route → Controller → Service → Prisma → Database
   - Response flow: Database → Prisma → Service → Controller → Route → Client
   - Frontend flow: Component → Zustand Store → localStorage

2. **Code Walk-through Order**:

   - Start with types (contracts between layers)
   - Then services (business logic, core functionality)
   - Then controllers (HTTP adaptation layer)
   - Then routes (API surface definition)
   - Finally frontend (consumption of API)

3. **Live Demonstrations**:

   - Prisma Studio to show plaintext passwords
   - React DevTools to show Zustand state
   - Browser DevTools to show localStorage
   - Network tab to show API calls
   - curl to demonstrate backend vulnerability

4. **Security Discussion**:
   - Why Phase 1 is intentionally insecure
   - Real-world consequences of these vulnerabilities
   - How Phase 2 will fix each issue
   - Industry standards and best practices

### Common Issues & Solutions

**Backend:**

- **Prisma Client not generated**: Run `npx prisma generate`
- **Port 3000 already in use**: Kill the process or change PORT in .env
- **CORS errors**: Verify `cors()` middleware is before routes
- **Import errors**: Check that 'controllers' (not 'ontrollers') is used
- **dotenv not working**: Make sure .env file exists and dotenv is installed

**Frontend:**

- **Port 5173 conflict**: Vite will auto-increment to 5174
- **Zustand not persisting**: Check browser allows localStorage
- **TypeScript errors**: Ensure @types packages are installed
- **Router not working**: Verify BrowserRouter wraps all Routes
- **API connection fails**: Check backend is running and CORS is enabled

### Setup Time Saver

Create a setup script for students:

**Windows (setup.ps1):**

```powershell
# Backend
cd backend
npm install
npx prisma migrate dev --name init
npx prisma generate

# Frontend
cd ../security-tp-frontend
npm install

Write-Host "✅ Setup complete! Run 'npm run dev' in both directories."
```

**Linux/Mac (setup.sh):**

```bash
#!/bin/bash
# Backend
cd backend
npm install
npx prisma migrate dev --name init
npx prisma generate

# Frontend
cd ../security-tp-frontend
npm install

echo "✅ Setup complete! Run 'npm run dev' in both directories."
```

---

## 🚨 Security Vulnerabilities Summary (Phase 1)

### Critical (Must Fix in Phase 2)

1. ✅ **SQL Injection** - Protected by Prisma ORM
2. ❌ **Plaintext Passwords** - Stored without hashing
3. ❌ **No Authentication** - Backend doesn't verify identity
4. ❌ **No Authorization** - No role-based access control
5. ❌ **Client-Side Only Auth** - localStorage can be manipulated
6. ❌ **No HTTPS** - Data transmitted in plain text

### Medium (Consider for Phase 2)

- No rate limiting (brute force attacks possible)
- No input validation/sanitization
- No password complexity requirements
- No session expiration
- No audit logging

### Low (Consider for Phase 3)

- No CSRF protection
- No XSS protection headers
- No email verification
- No password reset functionality
- No 2FA/MFA

---

**End of Phase 1 README**

**Next Phase**: Phase 2 - Implementing Security (bcrypt, JWT, middleware, RBAC)

For questions or issues, please check the Discussion Questions section or review the code comments.
