#!/usr/bin/env python3
"""
Student Exercise: Implement a Brute Force Attack

⚠️ EDUCATIONAL PURPOSE ONLY
Complete the TODOs to create a working brute force attack demonstration.

Learning Objectives:
1. Understand how brute force attacks work
2. Learn why rate limiting is critical
3. Practice Python programming with HTTP requests
4. Understand attack patterns and defense strategies
"""

import requests
import time
from datetime import datetime

# Configuration
API_URL = "http://localhost:3000/api/auth/login"
TARGET_EMAIL = "student@test.com"  # Change to your test user

# Small password list for testing
PASSWORDS = [
    "password",
    "123456",
    "qwerty",
    "letmein",
    "TestPassword123",  # Your actual password
]

def attempt_login(email: str, password: str):
    """
    TODO 1: Implement the login attempt function
    
    Instructions:
    - Make a POST request to API_URL
    - Send JSON with email and password
    - Return True if status code is 200, False otherwise
    
    Hints:
    - Use requests.post()
    - Set json parameter
    - Check response.status_code
    """
    # Your code here
    pass

def brute_force_attack(email: str, password_list: list):
    """
    TODO 2: Implement the brute force attack
    
    Instructions:
    - Loop through each password in password_list
    - Try to login with each password
    - Print the attempt number and password being tried
    - If login succeeds, print success message and return the password
    - If all attempts fail, return None
    
    Hints:
    - Use enumerate() to get index and password
    - Call attempt_login() for each password
    - Print progress to show what's happening
    """
    # Your code here
    pass

def measure_attack_speed(email: str, password_list: list):
    """
    TODO 3: Measure how fast the attack is
    
    Instructions:
    - Record the start time before the attack
    - Run the brute force attack
    - Record the end time after the attack
    - Calculate and print:
      * Total time taken
      * Number of attempts
      * Attempts per second
    
    Hints:
    - Use time.time() to get current time
    - Calculate elapsed time: end_time - start_time
    - Calculate rate: attempts / elapsed_time
    """
    # Your code here
    pass

def main():
    """Main execution - COMPLETE THIS"""
    print("=" * 60)
    print("🔓 BRUTE FORCE ATTACK EXERCISE")
    print("=" * 60)
    print(f"Target: {API_URL}")
    print(f"Email: {TARGET_EMAIL}")
    print(f"Passwords to try: {len(PASSWORDS)}")
    print("=" * 60)
    print()
    
    # TODO 4: Call your functions here
    # Example:
    # password = brute_force_attack(TARGET_EMAIL, PASSWORDS)
    # if password:
    #     print(f"Success! Password is: {password}")
    # else:
    #     print("Failed to find password")
    
    # Your code here
    pass

# Bonus Challenges (Optional):
# 
# CHALLENGE 1: Add a delay between attempts
# - Add a parameter 'delay' to brute_force_attack()
# - Use time.sleep(delay) between attempts
# - Compare speed with and without delay
#
# CHALLENGE 2: Save results to a file
# - Create a function to save attempt results to CSV
# - Include: attempt number, password, success/fail, time taken
# - Use Python's csv module
#
# CHALLENGE 3: Detect rate limiting
# - Check if response status code is 429
# - If detected, print a message and stop the attack
# - Explain why this is a good security measure
#
# CHALLENGE 4: Try a larger password list
# - Create a file with 100 common passwords
# - Load passwords from the file
# - Compare time taken vs the small list

if __name__ == "__main__":
    main()

# DISCUSSION QUESTIONS:
# 
# 1. How long did it take to try all passwords?
# 2. How many attempts per second can you make?
# 3. How long would it take to try 1 million passwords?
# 4. Why is this attack successful in Phase 1?
# 5. How would rate limiting prevent this attack?
# 6. What other defenses could stop brute force attacks?
# 7. Is this attack practical in the real world? Why or why not?

