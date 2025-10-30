# Quick Setup Instructions

## Prerequisites
- Node.js 18+ installed
- npm or pnpm installed
- Terminal/Command Prompt

## Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
npm install

# Create .env file (if it doesn't exist)
# Create a file named .env with:
DATABASE_URL="file:./prisma/dev.db"
PORT=3000
NODE_ENV=development

# Run Prisma migrations
npm run prisma:migrate

# Generate Prisma Client
npm run prisma:generate

# Start backend server
npm run dev
```

Backend will run on: `http://localhost:3000`

## Frontend Setup

Open a **NEW** terminal window/tab:

```bash
# Navigate to frontend directory
cd security-tp-frontend

# Install dependencies
npm install

# Start frontend development server
npm run dev
```

Frontend will run on: `http://localhost:5173`

## Quick Test

1. Open browser to `http://localhost:5173`
2. Register a new account
3. Login with your credentials
4. Explore the dashboard and pages

## View Database

```bash
# In the backend directory
npm run prisma:studio
```

Opens Prisma Studio on `http://localhost:5555` to view database contents.

## Common Issues

### Backend won't start
- Make sure `.env` file exists in backend directory
- Check if port 3000 is available
- Run `npm install` to ensure all dependencies are installed

### Frontend won't start
- Check if backend is running first
- Verify `react-router-dom` and `zustand` are installed
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`

### CORS errors
- Ensure backend is running before frontend
- Check that `cors()` is enabled in backend `server.ts`

### Prisma errors
- Run `npx prisma generate`
- Delete `dev.db` and run migrations again
- Check DATABASE_URL in `.env`

## Project Structure Summary

```
TpCSS/
├── backend/                    # Express + TypeScript + Prisma
│   ├── src/
│   │   ├── controllers/       # HTTP request handlers
│   │   ├── services/          # Business logic
│   │   ├── routes/            # API routes
│   │   ├── config/            # Database config
│   │   ├── types/             # TypeScript types
│   │   └── server.ts          # Entry point
│   ├── prisma/
│   │   └── schema.prisma      # Database schema
│   ├── .env                    # Environment variables
│   └── package.json
│
└── security-tp-frontend/       # React + TypeScript + Vite
    ├── src/
    │   ├── components/        # Reusable components
    │   ├── pages/             # Page components
    │   ├── stores/            # Zustand stores
    │   ├── services/          # API services
    │   ├── types/             # TypeScript types
    │   ├── App.tsx            # Main app component
    │   └── main.tsx           # Entry point
    └── package.json
```

## API Endpoints

### Public
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### "Protected" (Phase 1 - Not Actually Protected!)
- `GET /api/auth/profile/:id` - Get user profile
- `GET /api/auth/users` - Get all users
- `GET /api/auth/health` - Health check

## Testing with curl

```bash
# Register
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"password123"}'

# Get profile (replace 1 with actual user ID)
curl http://localhost:3000/api/auth/profile/1

# Get all users
curl http://localhost:3000/api/auth/users
```

## For Instructors

### Automated Setup Script

**Windows (PowerShell):**
```powershell
# Save as setup.ps1
cd backend
if (!(Test-Path ".env")) {
    @"
DATABASE_URL="file:./prisma/dev.db"
PORT=3000
NODE_ENV=development
"@ | Out-File -FilePath .env -Encoding UTF8
}
npm install
npx prisma migrate dev --name init
npx prisma generate

cd ../security-tp-frontend
npm install

Write-Host "✅ Setup complete!"
Write-Host "Run 'npm run dev' in backend directory"
Write-Host "Run 'npm run dev' in security-tp-frontend directory"
```

**Linux/Mac (Bash):**
```bash
#!/bin/bash
# Save as setup.sh and run: chmod +x setup.sh && ./setup.sh

cd backend
if [ ! -f .env ]; then
    cat > .env << EOF
DATABASE_URL="file:./prisma/dev.db"
PORT=3000
NODE_ENV=development
EOF
fi
npm install
npx prisma migrate dev --name init
npx prisma generate

cd ../security-tp-frontend
npm install

echo "✅ Setup complete!"
echo "Run 'npm run dev' in backend directory"
echo "Run 'npm run dev' in security-tp-frontend directory"
```

## Reset Everything

If you need to start fresh:

```bash
# Backend
cd backend
rm -rf node_modules prisma/dev.db prisma/migrations
npm install
npm run prisma:migrate
npm run prisma:generate

# Frontend
cd security-tp-frontend
rm -rf node_modules
npm install
```

## Next Steps

Once everything is running:
1. Read through the main README.md for detailed explanations
2. Test all features (register, login, navigation)
3. Explore security vulnerabilities
4. Prepare for Phase 2 (adding proper security)

