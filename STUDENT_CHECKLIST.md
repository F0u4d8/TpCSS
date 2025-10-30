# Student Setup Checklist

Use this checklist to verify your Phase 1 setup is working correctly.

---

## ✅ Pre-Setup Checklist

- [ ] Node.js 18+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Code editor installed (VS Code recommended)
- [ ] Terminal/Command Prompt ready

---

## ✅ Backend Setup Checklist

### Installation
- [ ] Navigated to `backend` directory
- [ ] Created `.env` file with:
  ```
  DATABASE_URL="file:./prisma/dev.db"
  PORT=3000
  NODE_ENV=development
  ```
- [ ] Ran `npm install` successfully
- [ ] No errors during dependency installation

### Database Setup
- [ ] Ran `npm run prisma:migrate` (or `npx prisma migrate dev --name init`)
- [ ] Saw "Your database is now in sync with your schema" message
- [ ] Ran `npm run prisma:generate`
- [ ] File `prisma/dev.db` was created

### Start Backend
- [ ] Ran `npm run dev`
- [ ] Saw message: "🚀 Server running on http://localhost:3000"
- [ ] Saw message: "⚠️ WARNING: Phase 1 - INSECURE by design"
- [ ] No error messages in terminal

### Test Backend Endpoints
Open another terminal and test:

- [ ] Health check works:
  ```bash
  curl http://localhost:3000/api/auth/health
  ```
  Expected: `{"status":"ok","message":"Auth service is running"}`

- [ ] Register works:
  ```bash
  curl -X POST http://localhost:3000/api/auth/register \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"test123"}'
  ```
  Expected: Success message with user object

- [ ] Login works:
  ```bash
  curl -X POST http://localhost:3000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"test123"}'
  ```
  Expected: Success message with user object

- [ ] Profile endpoint works:
  ```bash
  curl http://localhost:3000/api/auth/profile/1
  ```
  Expected: User data (notice: no auth required! ⚠️)

- [ ] Users endpoint works:
  ```bash
  curl http://localhost:3000/api/auth/users
  ```
  Expected: Array of users (notice: no auth required! ⚠️)

---

## ✅ Frontend Setup Checklist

### Installation
- [ ] Navigated to `security-tp-frontend` directory
- [ ] Ran `npm install` successfully
- [ ] Dependencies installed without errors
- [ ] Verified `zustand` and `react-router-dom` are installed

### Start Frontend
- [ ] Backend is still running on port 3000
- [ ] Ran `npm run dev`
- [ ] Saw message: "Local: http://localhost:5173/"
- [ ] No error messages in terminal

### Browser Test
- [ ] Opened browser to `http://localhost:5173`
- [ ] Page loads without errors
- [ ] See title: "🔓 Computer Security TP - Phase 1"
- [ ] See warning box with security notes
- [ ] See Register and Login forms

---

## ✅ Functionality Checklist

### Registration
- [ ] Can type in email field
- [ ] Can type in password field
- [ ] Click "Register" button
- [ ] See success message: "✅ Registration successful!"
- [ ] No error messages

### Login
- [ ] Can type in email field
- [ ] Can type in password field  
- [ ] Click "Login" button
- [ ] Redirected to Dashboard page
- [ ] See welcome message with email

### Navigation
- [ ] Navbar appears after login
- [ ] Navbar shows email address
- [ ] "Dashboard" link works
- [ ] "Profile" link works
- [ ] "Users" link works
- [ ] Each page loads correctly

### Dashboard Page
- [ ] Shows user ID
- [ ] Shows email
- [ ] Shows security warning box
- [ ] "View Profile" button works
- [ ] "View All Users" button works

### Profile Page
- [ ] Loads user data
- [ ] Shows user ID and email
- [ ] Shows security warning from backend

### Users Page
- [ ] Shows list of all users
- [ ] Each user shows ID and email
- [ ] Shows security warning from backend
- [ ] Multiple users display correctly (if multiple registered)

### Logout
- [ ] Click "Logout" button in navbar
- [ ] Redirected to login page
- [ ] Navbar disappears
- [ ] Register/Login forms appear

### Protected Routes (Frontend)
- [ ] After logout, try accessing `http://localhost:5173/dashboard`
- [ ] Automatically redirected to login ✅
- [ ] Same for `/profile` and `/users` ✅

---

## ✅ State Persistence Checklist

### localStorage Test
- [ ] Login to the application
- [ ] Open Browser DevTools (F12)
- [ ] Go to Application tab → Local Storage → http://localhost:5173
- [ ] See `auth-storage` key with user data
- [ ] Refresh page (F5)
- [ ] Still logged in ✅ (state persisted)

### Manual State Manipulation (Security Test)
- [ ] In Application tab → Local Storage
- [ ] Edit the user email or ID
- [ ] Refresh page
- [ ] See the changed data displayed
- [ ] **Important**: This shows client-side auth is insecure! ⚠️

---

## ✅ Backend Security Vulnerability Checks

### Test 1: No Authentication Required
- [ ] Logout from frontend
- [ ] In terminal, run:
  ```bash
  curl http://localhost:3000/api/auth/users
  ```
- [ ] Still get all users data! ⚠️
- [ ] This demonstrates: **Backend has no authentication**

### Test 2: Access Any Profile
- [ ] Can access any user's profile with just their ID:
  ```bash
  curl http://localhost:3000/api/auth/profile/1
  curl http://localhost:3000/api/auth/profile/2
  ```
- [ ] Works without any credentials! ⚠️
- [ ] This demonstrates: **No authorization checks**

### Test 3: Plaintext Passwords
- [ ] In backend terminal, run: `npm run prisma:studio`
- [ ] Opens Prisma Studio in browser
- [ ] Click on "User" table
- [ ] See all passwords in **plain text**! ⚠️
- [ ] This demonstrates: **Passwords not hashed**

---

## ✅ Understanding Checklist

Answer these to verify your understanding:

### Architecture
- [ ] Can explain what a Route does
- [ ] Can explain what a Controller does
- [ ] Can explain what a Service does
- [ ] Can explain the request flow: Route → Controller → Service → Prisma

### Frontend
- [ ] Can explain what Zustand store does
- [ ] Can explain why state persists after refresh
- [ ] Can explain what ProtectedRoute component does
- [ ] Can explain the difference between frontend and backend protection

### Security Issues
- [ ] Can list 3 security vulnerabilities in Phase 1
- [ ] Can explain why plaintext passwords are bad
- [ ] Can explain why client-side only auth is insecure
- [ ] Can explain what will be fixed in Phase 2

---

## ✅ Common Issues & Solutions

### Backend won't start
**Issue**: `Error: Cannot find module`
- [ ] Solution: Run `npm install` in backend directory

**Issue**: `Port 3000 already in use`
- [ ] Solution: Kill the process or change PORT in .env

**Issue**: `PrismaClientInitializationError`
- [ ] Solution: Run `npx prisma generate`

### Frontend won't start
**Issue**: `ECONNREFUSED localhost:3000`
- [ ] Solution: Make sure backend is running first

**Issue**: `Cannot find module 'zustand'`
- [ ] Solution: Run `npm install zustand react-router-dom`

**Issue**: Blank page or React errors
- [ ] Solution: Check browser console (F12) for errors
- [ ] Clear cache and reload (Ctrl+Shift+R)

### Database issues
**Issue**: "Table does not exist"
- [ ] Solution: Run `npm run prisma:migrate`

**Issue**: Want to reset database
- [ ] Solution: Delete `prisma/dev.db` and run migrations again

---

## ✅ Final Verification

### Instructor Sign-Off (For Classroom Use)
- [ ] All backend endpoints tested and working
- [ ] All frontend pages load correctly
- [ ] Can register and login successfully
- [ ] State persists across page refresh
- [ ] Can demonstrate security vulnerabilities
- [ ] Understands architecture pattern
- [ ] Ready for Phase 2

### Self-Assessment
Rate your understanding (1-5):
- [ ] Backend architecture (Routes/Controllers/Services): ___/5
- [ ] Prisma ORM usage: ___/5
- [ ] Frontend React components: ___/5
- [ ] Zustand state management: ___/5
- [ ] React Router navigation: ___/5
- [ ] Security vulnerabilities: ___/5

**If any score is below 3, review the README and ask for help!**

---

## 🎯 Ready for Phase 2?

You're ready to proceed to Phase 2 when you can:
- [x] Complete all items in this checklist
- [x] Explain the architecture to someone else
- [x] Demonstrate all security vulnerabilities
- [x] Understand why each vulnerability is dangerous
- [x] Have ideas about how to fix them

**Phase 2 Topics**:
- Password hashing with bcrypt
- JWT token authentication
- Authentication middleware
- Refresh token mechanism
- Role-based access control

---

## 📚 Resources

- Main documentation: `Readme.md`
- Quick setup: `SETUP_INSTRUCTIONS.md`
- What was fixed: `FIXES_APPLIED.md`
- This checklist: `STUDENT_CHECKLIST.md`

---

**Good luck! Ask for help if you get stuck on any checklist item.** 🚀

