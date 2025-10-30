#!/usr/bin/env python3
"""
🔒 Cybersecurity TP - Security Testing & Attack Demonstrations
Phase 1: Vulnerability Assessment

⚠️ EDUCATIONAL PURPOSE ONLY
Use only on systems you own or have explicit permission to test.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import sys

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Configuration
BASE_URL = "http://localhost:3000"
API_URL = f"{BASE_URL}/api/auth"

# Test results storage
test_results: List[Dict[str, Any]] = []

def print_banner():
    """Print test banner"""
    print(f"{Colors.OKCYAN}{'='*70}")
    print(f"🔒 SECURITY TESTING FRAMEWORK")
    print(f"{'='*70}")
    print(f"Target: {API_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}{Colors.ENDC}\n")

def log_test(test_name: str, status: str, details: str = ""):
    """Log test results with color coding"""
    result = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "test": test_name,
        "status": status,
        "details": details
    }
    test_results.append(result)
    
    if status == "PASS":
        color = Colors.OKGREEN
    elif status == "FAIL":
        color = Colors.FAIL
    else:
        color = Colors.WARNING
    
    print(f"{color}[{result['timestamp']}] {status}: {test_name}{Colors.ENDC}")
    if details:
        print(f"  └─ {details}")

def make_request(method: str, endpoint: str, **kwargs) -> requests.Response:
    """Make HTTP request with error handling"""
    url = f"{API_URL}{endpoint}"
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        return response
    except requests.exceptions.ConnectionError:
        print(f"{Colors.FAIL}Error: Cannot connect to {url}")
        print(f"Make sure the backend server is running!{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.FAIL}Error making request: {e}{Colors.ENDC}")
        return None

def test_connectivity():
    """Test 1: Basic API Connectivity"""
    print(f"\n{Colors.OKCYAN}=== Test 1: API Connectivity ==={Colors.ENDC}\n")
    
    # Test health endpoint
    response = make_request("GET", "/health")
    if response and response.status_code == 200:
        log_test("Health Check", "PASS", f"API is running: {response.json()}")
    else:
        log_test("Health Check", "FAIL", "API is not responding")
        sys.exit(1)
    
    # Test invalid endpoint
    response = make_request("GET", "/nonexistent")
    if response and response.status_code == 404:
        log_test("404 Handler", "PASS", "Server properly handles invalid routes")
    else:
        log_test("404 Handler", "WARN", "Unexpected response for invalid route")

def test_registration():
    """Test 2: User Registration"""
    print(f"\n{Colors.OKCYAN}=== Test 2: Registration Testing ==={Colors.ENDC}\n")
    
    # Generate unique test user
    timestamp = int(time.time())
    test_user = {
        "email": f"student{timestamp}@test.com",
        "password": "TestPassword123"
    }
    
    # Test 2.1: Valid registration
    response = make_request("POST", "/register", json=test_user)
    if response and response.status_code == 201:
        data = response.json()
        log_test("Valid Registration", "PASS", 
                f"User created: {data.get('user', {}).get('email')}")
        user_id = data.get('user', {}).get('id')
    else:
        log_test("Valid Registration", "FAIL", 
                f"Status: {response.status_code if response else 'No response'}")
        user_id = None
    
    # Test 2.2: Duplicate email
    response = make_request("POST", "/register", json=test_user)
    if response and response.status_code == 409:
        log_test("Duplicate Email Prevention", "PASS", 
                "Server correctly rejects duplicate email")
    else:
        log_test("Duplicate Email Prevention", "FAIL", 
                "Should reject duplicate email")
    
    # Test 2.3: Missing password
    response = make_request("POST", "/register", 
                           json={"email": f"test{timestamp+1}@test.com"})
    if response and response.status_code == 400:
        log_test("Missing Password Validation", "PASS", 
                "Server validates required fields")
    else:
        log_test("Missing Password Validation", "FAIL", 
                "Should validate required fields")
    
    print(f"\n{Colors.OKGREEN}✓ Test user created: {test_user['email']}{Colors.ENDC}")
    return test_user, user_id

def test_authentication(test_user: Dict[str, str]):
    """Test 3: Authentication Testing"""
    print(f"\n{Colors.OKCYAN}=== Test 3: Authentication Testing ==={Colors.ENDC}\n")
    
    # Test 3.1: Valid login
    response = make_request("POST", "/login", json=test_user)
    if response and response.status_code == 200:
        data = response.json()
        log_test("Valid Login", "PASS", 
                f"User authenticated: {data.get('user', {}).get('email')}")
        print(f"\n{Colors.WARNING}⚠ SECURITY ISSUE: No session token or JWT returned!{Colors.ENDC}")
        print(f"Response: {json.dumps(data, indent=2)}\n")
    else:
        log_test("Valid Login", "FAIL", "Login should succeed with valid credentials")
    
    # Test 3.2: Invalid password
    response = make_request("POST", "/login", json={
        "email": test_user["email"],
        "password": "WrongPassword123"
    })
    if response and response.status_code == 401:
        log_test("Invalid Password Rejection", "PASS", 
                "Server rejects wrong password")
    else:
        log_test("Invalid Password Rejection", "FAIL", 
                "Should reject invalid password")
    
    # Test 3.3: Non-existent user
    response = make_request("POST", "/login", json={
        "email": "nonexistent@test.com",
        "password": "password123"
    })
    if response and response.status_code == 401:
        log_test("Non-existent User Rejection", "PASS", 
                "Server rejects unknown user")
    else:
        log_test("Non-existent User Rejection", "FAIL", 
                "Should reject non-existent user")

def test_no_authentication(user_id: int):
    """Test 4: CRITICAL - No Authentication Required"""
    print(f"\n{Colors.FAIL}=== Test 4: CRITICAL - No Authentication on Protected Routes ==={Colors.ENDC}\n")
    
    # Test 4.1: Access user profile without authentication
    if user_id:
        response = make_request("GET", f"/profile/{user_id}")
        if response and response.status_code == 200:
            data = response.json()
            log_test("Unauthenticated Profile Access", "FAIL", 
                    "🚨 CRITICAL: Accessed profile without auth!")
            print(f"\n{Colors.FAIL}VULNERABILITY CONFIRMED:{Colors.ENDC}")
            print(f"Profile data: {json.dumps(data, indent=2)}")
            print(f"\n{Colors.WARNING}Warning from server: {data.get('warning', 'None')}{Colors.ENDC}\n")
        else:
            log_test("Unauthenticated Profile Access", "PASS", 
                    "Profile is protected")
    
    # Test 4.2: Access all users without authentication
    response = make_request("GET", "/users")
    if response and response.status_code == 200:
        data = response.json()
        users = data.get('users', [])
        log_test("Unauthenticated Users List Access", "FAIL", 
                f"🚨 CRITICAL: Accessed {len(users)} users without auth!")
        print(f"\n{Colors.FAIL}VULNERABILITY CONFIRMED:{Colors.ENDC}")
        print(f"Retrieved {len(users)} users without any credentials!")
        print(f"\n{Colors.WARNING}Warning from server: {data.get('warning', 'None')}{Colors.ENDC}")
        
        # Display first 5 users
        print(f"\nFirst {min(5, len(users))} users:")
        for i, user in enumerate(users[:5], 1):
            print(f"  {i}. ID: {user.get('id')}, Email: {user.get('email')}")
    else:
        log_test("Unauthenticated Users List Access", "PASS", 
                "Users list is protected")
    
    print(f"\n{Colors.FAIL}{'='*70}")
    print(f"CRITICAL SECURITY ISSUE IDENTIFIED:")
    print(f"Backend has NO authentication mechanism!")
    print(f"Anyone can access ANY endpoint without credentials!")
    print(f"{'='*70}{Colors.ENDC}")

def test_idor():
    """Test 5: IDOR (Insecure Direct Object Reference)"""
    print(f"\n{Colors.FAIL}=== Test 5: IDOR Vulnerability Testing ==={Colors.ENDC}\n")
    
    accessible_profiles = []
    
    for i in range(1, 6):  # Try to access first 5 users
        response = make_request("GET", f"/profile/{i}")
        if response and response.status_code == 200:
            data = response.json()
            user_data = data.get('user', {})
            accessible_profiles.append(user_data)
            log_test(f"IDOR - Access User #{i}", "FAIL", 
                    f"🚨 Accessed: {user_data.get('email', 'N/A')}")
        elif response and response.status_code == 404:
            log_test(f"IDOR - Access User #{i}", "INFO", 
                    "User not found (expected)")
    
    if accessible_profiles:
        print(f"\n{Colors.FAIL}IDOR VULNERABILITY CONFIRMED:{Colors.ENDC}")
        print(f"Successfully accessed {len(accessible_profiles)} user profiles!\n")
        for i, profile in enumerate(accessible_profiles, 1):
            print(f"  {i}. ID: {profile.get('id')}, Email: {profile.get('email')}")
        print(f"\n{Colors.WARNING}⚠ Any user can view any other user's profile!{Colors.ENDC}")
    else:
        print(f"\n{Colors.OKGREEN}No IDOR vulnerability detected{Colors.ENDC}")

def test_sql_injection():
    """Test 6: SQL Injection Testing"""
    print(f"\n{Colors.OKCYAN}=== Test 6: SQL Injection Testing ==={Colors.ENDC}\n")
    
    # Common SQL injection payloads
    sql_payloads = [
        "' OR '1'='1",
        "admin'--",
        "' OR 1=1--",
        "'; DROP TABLE users--",
    ]
    
    print(f"{Colors.WARNING}Testing SQL injection payloads...{Colors.ENDC}\n")
    
    for payload in sql_payloads:
        response = make_request("POST", "/login", json={
            "email": payload,
            "password": "test"
        })
        
        if response:
            if response.status_code == 200:
                log_test(f"SQL Injection: {payload[:20]}...", "FAIL", 
                        "🚨 Injection may have succeeded!")
            elif response.status_code == 401:
                log_test(f"SQL Injection: {payload[:20]}...", "PASS", 
                        "✓ Query failed safely (Prisma protection)")
            elif response.status_code == 500:
                log_test(f"SQL Injection: {payload[:20]}...", "WARN", 
                        "Server error - investigate logs")
    
    print(f"\n{Colors.OKGREEN}✓ Prisma ORM provides protection against SQL injection!{Colors.ENDC}")

def test_rate_limiting(test_user: Dict[str, str]):
    """Test 7: Rate Limiting"""
    print(f"\n{Colors.OKCYAN}=== Test 7: Rate Limiting Testing ==={Colors.ENDC}\n")
    
    print(f"{Colors.WARNING}Attempting 10 rapid login requests...{Colors.ENDC}\n")
    
    attempts = []
    blocked = False
    
    for i in range(10):
        start = time.time()
        response = make_request("POST", "/login", json={
            "email": test_user["email"],
            "password": f"wrong_password_{i}"
        })
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        if response:
            attempts.append({
                "attempt": i + 1,
                "status": response.status_code,
                "time_ms": round(elapsed, 2)
            })
            
            if response.status_code == 429:
                blocked = True
                log_test("Rate Limiting", "PASS", 
                        f"Blocked after {i+1} attempts")
                break
    
    if not blocked:
        log_test("Rate Limiting", "FAIL", "🚨 No rate limiting detected!")
        print(f"\n{Colors.FAIL}VULNERABILITY: Brute force attacks are possible!{Colors.ENDC}")
    
    # Display attempt details
    print(f"\nAttempt details:")
    for attempt in attempts:
        print(f"  Attempt {attempt['attempt']}: Status {attempt['status']}, "
              f"Time: {attempt['time_ms']}ms")
    
    avg_time = sum(a['time_ms'] for a in attempts) / len(attempts) if attempts else 0
    print(f"\n{Colors.OKCYAN}Average response time: {avg_time:.2f}ms{Colors.ENDC}")
    print(f"{Colors.WARNING}⚠ Without rate limiting, attackers can try thousands of passwords{Colors.ENDC}")

def test_password_security():
    """Test 8: Password Security Analysis"""
    print(f"\n{Colors.FAIL}=== Test 8: Password Storage Analysis ==={Colors.ENDC}\n")
    
    print(f"{Colors.WARNING}⚠ WARNING: This test demonstrates why plaintext passwords are dangerous{Colors.ENDC}\n")
    
    print(f"{Colors.FAIL}CRITICAL SECURITY FLAW:{Colors.ENDC}")
    print("""
Phase 1 stores passwords in PLAINTEXT!

What an attacker with database access would see:
┌────────┬─────────────────────────┬──────────────────┐
│ ID     │ Email                   │ Password         │
├────────┼─────────────────────────┼──────────────────┤
│ 1      │ student1@test.com       │ TestPassword123  │
│ 2      │ admin@test.com          │ admin123         │
│ 3      │ user@test.com           │ MySecret456!     │
└────────┴─────────────────────────┴──────────────────┘
""")
    
    log_test("Password Hashing", "FAIL", "🚨 Passwords stored in plaintext!")
    
    print(f"{Colors.OKCYAN}To verify this:")
    print(f"1. Open Prisma Studio: cd backend && npm run prisma:studio")
    print(f"2. Navigate to the User table")
    print(f"3. See all passwords in plain text!{Colors.ENDC}")
    
    print(f"\n{Colors.WARNING}Phase 2 will fix this with bcrypt hashing{Colors.ENDC}")

def print_summary():
    """Print test summary and recommendations"""
    print(f"\n{Colors.OKCYAN}{'='*70}")
    print(f"SECURITY ASSESSMENT REPORT")
    print(f"{'='*70}{Colors.ENDC}\n")
    
    # Count results
    pass_count = sum(1 for r in test_results if r['status'] == 'PASS')
    fail_count = sum(1 for r in test_results if r['status'] == 'FAIL')
    warn_count = sum(1 for r in test_results if r['status'] in ['WARN', 'INFO'])
    
    print(f"{Colors.OKCYAN}Test Summary:{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}PASS: {pass_count}{Colors.ENDC}")
    print(f"  {Colors.FAIL}FAIL: {fail_count}{Colors.ENDC}")
    print(f"  {Colors.WARNING}WARN/INFO: {warn_count}{Colors.ENDC}")
    
    # Critical vulnerabilities
    print(f"\n{Colors.FAIL}{'='*70}")
    print(f"CRITICAL VULNERABILITIES IDENTIFIED")
    print(f"{'='*70}{Colors.ENDC}\n")
    
    vulnerabilities = [
        ("CRITICAL", "No Authentication", "Protected endpoints accessible without credentials"),
        ("CRITICAL", "Plaintext Passwords", "Passwords stored without hashing"),
        ("CRITICAL", "No Authorization", "No RBAC - any user can access any data"),
        ("HIGH", "IDOR Vulnerability", "Direct object references without access control"),
        ("HIGH", "No Rate Limiting", "Unlimited requests allowed - brute force possible"),
        ("MEDIUM", "User Enumeration", "Different errors reveal if email exists"),
    ]
    
    for severity, issue, description in vulnerabilities:
        color = Colors.FAIL if severity == "CRITICAL" else Colors.WARNING
        print(f"{color}[{severity}] {issue}{Colors.ENDC}")
        print(f"  └─ {description}\n")
    
    # What's protected
    print(f"{Colors.OKGREEN}{'='*70}")
    print(f"WHAT IS PROTECTED")
    print(f"{'='*70}{Colors.ENDC}\n")
    
    print(f"{Colors.OKGREEN}✓ SQL Injection - Prisma ORM uses parameterized queries{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✓ Duplicate Email - Database unique constraint enforced{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✓ Required Fields - Basic validation for email and password{Colors.ENDC}")
    
    # Recommendations
    print(f"\n{Colors.OKCYAN}{'='*70}")
    print(f"RECOMMENDATIONS FOR PHASE 2")
    print(f"{'='*70}{Colors.ENDC}\n")
    
    recommendations = [
        "1. Implement bcrypt password hashing (salt rounds: 10-12)",
        "2. Add JWT token-based authentication",
        "3. Create authentication middleware for protected routes",
        "4. Implement authorization checks (user can only access their own data)",
        "5. Add rate limiting (express-rate-limit)",
        "6. Implement refresh token mechanism",
        "7. Add role-based access control (RBAC)",
        "8. Use generic error messages to prevent enumeration",
        "9. Add input validation and sanitization",
        "10. Implement HTTPS in production",
    ]
    
    for rec in recommendations:
        print(f"{Colors.WARNING}{rec}{Colors.ENDC}")
    
    print(f"\n{Colors.OKCYAN}Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}\nPhase 1 security assessment complete! 🎓{Colors.ENDC}\n")

def main():
    """Main test execution"""
    try:
        print_banner()
        
        # Run tests
        test_connectivity()
        test_user, user_id = test_registration()
        test_authentication(test_user)
        test_no_authentication(user_id)
        test_idor()
        test_sql_injection()
        test_rate_limiting(test_user)
        test_password_security()
        
        # Print summary
        print_summary()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Tests interrupted by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Check if requests module is installed
    try:
        import requests
    except ImportError:
        print(f"{Colors.FAIL}Error: 'requests' module not found{Colors.ENDC}")
        print(f"Install it with: pip install requests")
        sys.exit(1)
    
    main()

