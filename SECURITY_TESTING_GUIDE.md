# Security Testing Guide

## Overview

This guide explains how to use the security testing tools to identify and understand vulnerabilities in the Phase 1 application.

---

## 🐍 Python Script (`security_test.py`)

The Python script provides an automated security assessment of your application.

### Prerequisites

1. **Python 3.7+** installed
2. **Backend running** on `http://localhost:3000`
3. **Requests library** installed

### Installation

```bash
# Install required Python package
pip install requests
```

### Running the Tests

```bash
# Make script executable (Linux/Mac)
chmod +x security_test.py

# Run the script
python security_test.py
```

### What It Tests

The script performs 8 comprehensive security tests:

#### Test 1: API Connectivity ✅

- Verifies the backend is running
- Tests health endpoint
- Validates 404 handling

#### Test 2: Registration Testing ✅

- Valid user registration
- Duplicate email prevention
- Missing field validation

#### Test 3: Authentication Testing

- Valid login flow
- Invalid password rejection
- Non-existent user handling
- **Identifies: No session token/JWT issued**

#### Test 4: No Authentication (CRITICAL) 🚨

- Attempts to access protected endpoints without auth
- **Discovers: All endpoints are publicly accessible**
- **Impact: Complete data breach possible**

#### Test 5: IDOR Vulnerability 🚨

- Tests Insecure Direct Object References
- Attempts to access multiple user profiles by ID
- **Discovers: Can enumerate and access all users**

#### Test 6: SQL Injection Testing ✅

- Tests common SQL injection payloads
- **Confirms: Prisma ORM provides protection**

#### Test 7: Rate Limiting 🚨

- Tests for brute force protection
- Sends rapid login attempts
- **Discovers: No rate limiting implemented**
- **Impact: Brute force attacks possible**

#### Test 8: Password Security 🚨

- Analyzes password storage
- **Discovers: Passwords stored in plaintext**
- **Impact: All credentials exposed if DB compromised**

---

## 📓 Jupyter Notebook (`security_testing.ipynb`)

The Jupyter notebook provides an interactive learning experience.

### Prerequisites

1. **Jupyter installed**: `pip install jupyter notebook`
2. **Required packages**: `pip install requests pandas colorama`
3. **Backend running** on `http://localhost:3000`

### Starting Jupyter

```bash
# Start Jupyter Notebook
jupyter notebook

# Open security_testing.ipynb in your browser
```

### Interactive Features

The notebook includes:

- **Color-coded output** for easy understanding
- **Detailed explanations** for each vulnerability
- **Code examples** you can modify and re-run
- **Student exercises** to practice security testing
- **Discussion questions** to verify understanding
- **Data visualization** with pandas DataFrames

### Student Exercises

The notebook includes hands-on exercises:

1. **Exercise 1: Brute Force Attack Simulation**

   - Implement a password guessing attack
   - Measure success rate and time

2. **Exercise 2: Data Exfiltration**

   - Extract all user data
   - Save to CSV file
   - Understand data breach impact

3. **Exercise 3: Custom Vulnerability Test**
   - Design your own security test
   - Find vulnerabilities not covered
   - Document your findings

---

## 🎯 Understanding the Results

### Color Coding

- 🟢 **GREEN (PASS)**: Security feature working correctly
- 🔴 **RED (FAIL)**: Critical vulnerability found
- 🟡 **YELLOW (WARN/INFO)**: Minor issue or informational

### What FAIL Means

A **FAIL** status indicates a security vulnerability:

- For authentication tests: **FAIL is bad** (security broken)
- For injection tests: **PASS is good** (attack blocked)

Example:

```
❌ FAIL: Unauthenticated Profile Access
  └─ 🚨 CRITICAL: Accessed profile without auth!
```

This means the security check **failed** - the profile was accessed without authentication, which is a **vulnerability**.

---

## 🚨 Vulnerabilities Discovered

### Critical Severity

#### 1. No Authentication

**Description**: Protected endpoints accessible without credentials

**Test**:

```bash
curl http://localhost:3000/api/auth/users
# Returns all users without any authentication!
```

**Impact**: Complete data breach, any attacker can access all data

**Phase 2 Fix**: Implement JWT tokens and authentication middleware

---

#### 2. Plaintext Passwords

**Description**: Passwords stored without hashing

**Verification**:

1. Open Prisma Studio: `cd backend && npm run prisma:studio`
2. Click on User table
3. See passwords in plain text!

**Impact**: All credentials exposed if database is compromised

**Phase 2 Fix**: Use bcrypt to hash passwords

---

#### 3. No Authorization

**Description**: No role-based access control

**Test**: User A can access User B's data

**Impact**: Privacy violations, data theft

**Phase 2 Fix**: Implement authorization middleware

---

### High Severity

#### 4. IDOR Vulnerability

**Description**: Direct object references without access control

**Test**:

```bash
# Access any user profile by changing the ID
curl http://localhost:3000/api/auth/profile/1
curl http://localhost:3000/api/auth/profile/2
curl http://localhost:3000/api/auth/profile/3
```

**Impact**: Enumerate and access all user profiles

**Phase 2 Fix**: Validate user ownership before returning data

---

#### 5. No Rate Limiting

**Description**: Unlimited requests allowed

**Attack Scenario**:

```python
# Attacker can try unlimited passwords
for password in password_list:
    try_login(email, password)
```

**Impact**: Brute force attacks, account takeover

**Phase 2 Fix**: Implement express-rate-limit

---

## 📊 Sample Output

```
======================================================================
🔒 SECURITY TESTING FRAMEWORK
======================================================================
Target: http://localhost:3000/api/auth
Time: 2025-10-30 15:30:00
======================================================================

=== Test 1: API Connectivity ===

[15:30:01] PASS: Health Check
  └─ API is running: {'status': 'ok', 'message': 'Auth service is running'}
[15:30:01] PASS: 404 Handler
  └─ Server properly handles invalid routes

=== Test 4: CRITICAL - No Authentication on Protected Routes ===

[15:30:03] FAIL: Unauthenticated Profile Access
  └─ 🚨 CRITICAL: Accessed profile without auth!

VULNERABILITY CONFIRMED:
Profile data: {
  "user": {
    "id": 1,
    "email": "student@test.com"
  },
  "warning": "⚠️ Phase 1: Backend cannot verify this request is from the actual user!"
}

======================================================================
CRITICAL SECURITY ISSUE IDENTIFIED:
Backend has NO authentication mechanism!
Anyone can access ANY endpoint without credentials!
======================================================================
```

---

## 🎓 For Students

### Learning Path

1. **Read the README.md** - Understand the architecture
2. **Build the application** - Follow Phase 1 instructions
3. **Run security_test.py** - See vulnerabilities in action
4. **Open security_testing.ipynb** - Interactive learning
5. **Complete exercises** - Hands-on practice
6. **Answer discussion questions** - Verify understanding
7. **Plan Phase 2 fixes** - Think about solutions

### Discussion Questions

Answer these to verify understanding:

1. **Why is storing passwords in plaintext dangerous?**

   - Hint: What happens if the database is compromised?

2. **What is the difference between authentication and authorization?**

   - Authentication: ******\_******
   - Authorization: ******\_******

3. **How does Prisma protect against SQL injection?**

   - Hint: Think about parameterized queries

4. **Why is rate limiting important?**

   - What attacks does it prevent?

5. **What is IDOR and why is it dangerous?**

   - IDOR = ******\_******
   - Impact: ******\_******

6. **How would you fix the authentication issue in Phase 2?**
   - Hint: Think about JWT tokens

---

## 🛠️ For Instructors

### Classroom Usage

#### Demo Flow (30 minutes)

1. **Introduction (5 min)**

   - Explain ethical hacking
   - Emphasize educational purpose
   - Review legal/ethical considerations

2. **Live Demo (15 min)**

   - Run `security_test.py`
   - Show each vulnerability
   - Open Prisma Studio to show plaintext passwords
   - Demonstrate API calls with curl

3. **Discussion (10 min)**
   - What surprised you?
   - Which vulnerability is most critical?
   - How would you prioritize fixes?

#### Lab Exercise (60 minutes)

1. **Setup (10 min)**

   - Students install Python and Jupyter
   - Verify backend is running
   - Test connectivity

2. **Guided Testing (25 min)**

   - Run notebook cells together
   - Discuss each finding
   - Take notes

3. **Independent Exercises (20 min)**

   - Students complete exercises 1-3
   - Experiment with attacks
   - Document findings

4. **Sharing & Discussion (5 min)**
   - Students share findings
   - Discuss additional vulnerabilities found
   - Preview Phase 2 fixes

### Assessment Questions

Use these to evaluate student understanding:

**Multiple Choice:**

1. Which vulnerability allows accessing other users' data?

   - A) SQL Injection
   - B) IDOR ✓
   - C) XSS
   - D) CSRF

2. Why are plaintext passwords dangerous?
   - A) They take too much storage
   - B) They are visible if database is compromised ✓
   - C) They are slow to compare
   - D) They don't work

**Short Answer:**

1. Explain how the IDOR vulnerability works in this application.
2. Describe the impact of having no authentication on protected routes.
3. List 3 ways to prevent brute force attacks.

---

## 🔧 Troubleshooting

### Backend Not Running

**Error**:

```
Error: Cannot connect to http://localhost:3000/api/auth/health
Make sure the backend server is running!
```

**Solution**:

```bash
cd backend
npm run dev
```

### Missing Python Packages

**Error**:

```
ModuleNotFoundError: No module named 'requests'
```

**Solution**:

```bash
pip install requests pandas colorama
```

### Port Conflicts

**Issue**: Backend running on different port

**Solution**: Update `security_test.py`:

```python
BASE_URL = "http://localhost:YOUR_PORT"  # Change port here
```

### Permission Denied (Linux/Mac)

**Error**:

```
bash: ./security_test.py: Permission denied
```

**Solution**:

```bash
chmod +x security_test.py
```

---

## 📚 Additional Resources

### Security Learning

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- PortSwigger Web Security Academy: https://portswigger.net/web-security
- HackTheBox: https://www.hackthebox.com/

### Tools

- Burp Suite: Intercept and modify HTTP requests
- Postman: API testing
- OWASP ZAP: Automated security testing

### Next Steps

After completing Phase 1 security testing:

1. **Document all vulnerabilities** found
2. **Prioritize fixes** by severity
3. **Research solutions** (bcrypt, JWT, etc.)
4. **Plan Phase 2 implementation**
5. **Review security best practices**

---

## ⚖️ Legal & Ethical Notice

**IMPORTANT**: These tools are for educational purposes only.

### Legal Use

✅ **Allowed**:

- Testing your own applications
- Testing with explicit written permission
- Educational lab environments
- Authorized penetration testing

❌ **Never Allowed**:

- Testing systems you don't own
- Testing without permission
- Malicious attacks
- Unauthorized access

### Consequences

Unauthorized security testing can result in:

- Criminal charges
- Civil lawsuits
- Academic expulsion
- Career consequences

**Always practice ethical hacking!**

---

## 📝 Summary

The security testing tools help you:

- ✅ Identify vulnerabilities in Phase 1
- ✅ Understand attack techniques
- ✅ Learn security concepts hands-on
- ✅ Prepare for Phase 2 improvements
- ✅ Practice ethical hacking

**Remember**: The goal is to learn how to build secure applications, not to attack others!

---

**Questions or issues?** Review the main README.md or consult your instructor.

Happy (ethical) hacking! 🎓🔒
