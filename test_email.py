#!/usr/bin/env python3
"""
Test script to verify Gmail SMTP configuration
"""

import requests
import json

def test_backend_connection():
    """Test if backend is running"""
    try:
        response = requests.get('http://localhost:5000')
        if response.status_code == 200:
            print("✅ Backend is running")
            print(f"Response: {response.text}")
            return True
        else:
            print(f"❌ Backend error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_contact_endpoint():
    """Test the contact endpoint with sample data"""
    test_data = {
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "phone": "+91-1234567890",
        "company": "Test Company",
        "subject": "Test Message",
        "message": "This is a test message to verify email functionality."
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/contact',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            print("✅ Contact endpoint working")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Contact endpoint error: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Contact test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Backend Configuration...")
    print("=" * 50)
    
    # Test 1: Backend connection
    print("1. Testing backend connection...")
    if test_backend_connection():
        print("✅ Backend is accessible")
    else:
        print("❌ Backend not accessible")
        exit(1)
    
    print("\n2. Testing contact endpoint...")
    if test_contact_endpoint():
        print("✅ Email functionality working!")
        print("📧 Check your Gmail inbox for test emails")
    else:
        print("❌ Email functionality failed")
        print("💡 Make sure Gmail credentials are correct in .env file")

