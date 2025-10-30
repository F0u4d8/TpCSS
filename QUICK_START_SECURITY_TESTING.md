# 🚀 Quick Start: Security Testing

## In 3 Simple Steps

### Step 1: Install Python Dependencies (30 seconds)

```bash
pip install requests
```

### Step 2: Make Sure Backend is Running

```bash
# In one terminal
cd backend
npm run dev
```

### Step 3: Run Security Tests

```bash
# In another terminal (from project root)
python security_test.py
```

## Expected Output

You should see something like:

```
======================================================================
🔒 SECURITY TESTING FRAMEWORK
======================================================================
Target: http://localhost:3000/api/auth
Time: 2025-10-30 15:30:00
======================================================================

=== Test 1: API Connectivity ===

✅ [15:30:01] PASS: Health Check
  └─ API is running: {'status': 'ok', 'message': 'Auth service is running'}

=== Test 4: CRITICAL - No Authentication on Protected Routes ===

❌ [15:30:03] FAIL: Unauthenticated Profile Access
  └─ 🚨 CRITICAL: Accessed profile without auth!

...

======================================================================
SECURITY ASSESSMENT REPORT
======================================================================

Test Summary:
  ✅ PASS: 8
  ❌ FAIL: 5
  ⚠  WARN/INFO: 2

======================================================================
CRITICAL VULNERABILITIES IDENTIFIED
======================================================================

[CRITICAL] No Authentication
  └─ Protected endpoints accessible without credentials

[CRITICAL] Plaintext Passwords
  └─ Passwords stored without hashing

[CRITICAL] No Authorization
  └─ No RBAC - any user can access any data
```

## What Happens?

The script will:
1. ✅ Connect to your backend API
2. ✅ Register test users
3. ✅ Test authentication and authorization
4. ✅ Attempt to exploit vulnerabilities
5. ✅ Generate a comprehensive report
6. ✅ Show you exactly what's broken

## Manual Verification

After running the script, you can verify vulnerabilities manually:

### 1. View Plaintext Passwords

```bash
cd backend
npm run prisma:studio
```

Then:
- Open http://localhost:5555 in browser
- Click on "User" table
- See passwords in **plain text**! 🚨

### 2. Access Protected Data Without Auth

```bash
# Get all users without any credentials
curl http://localhost:3000/api/auth/users

# Access any user profile
curl http://localhost:3000/api/auth/profile/1
curl http://localhost:3000/api/auth/profile/2
```

Both work without authentication! 🚨

### 3. Test IDOR Vulnerability

```bash
# Enumerate users by changing IDs
for i in {1..10}; do
  echo "User $i:"
  curl -s http://localhost:3000/api/auth/profile/$i | grep -o '"email":"[^"]*"'
done
```

## Troubleshooting

### Backend not running?

```bash
Error: Cannot connect to http://localhost:3000/api/auth/health
```

**Fix**: Start the backend:
```bash
cd backend
npm run dev
```

### Python package missing?

```bash
ModuleNotFoundError: No module named 'requests'
```

**Fix**: Install requests:
```bash
pip install requests
```

### Colors not showing (Windows)?

**Fix**: Install colorama:
```bash
pip install colorama
```

## Next Steps

1. ✅ Run the security test
2. ✅ Read the generated report
3. ✅ Manually verify vulnerabilities
4. ✅ Read `SECURITY_TESTING_GUIDE.md` for details
5. ✅ Try the Jupyter notebook for interactive learning
6. ✅ Plan fixes for Phase 2

## Full Documentation

- **SECURITY_TOOLS_README.md** - Overview of all tools
- **SECURITY_TESTING_GUIDE.md** - Complete testing guide
- **Readme.md** - Main project documentation

---

**That's it! Happy (ethical) hacking! 🎓🔒**

