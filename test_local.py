"""
Test script to verify backend works locally
"""

import requests
import json

def test_backend():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Local Backend")
    print("=" * 40)
    
    # Test 1: Basic connectivity
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Basic connection: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Basic connection failed: {e}")
        return False
    
    # Test 2: Contact form submission
    test_data = {
        "firstName": "Test",
        "lastName": "User", 
        "email": "test@example.com",
        "phone": "1234567890",
        "company": "Test Company",
        "subject": "Test Subject",
        "message": "This is a test message from local backend"
    }
    
    try:
        print(f"\n📧 Testing contact form submission...")
        response = requests.post(
            f"{base_url}/api/contact",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Contact form test successful!")
            print("📧 Check your email at pixdotsolutions@gmail.com")
            return True
        else:
            print("❌ Contact form test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Contact form test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Make sure your backend is running: python app.py")
    print("📧 Make sure Gmail credentials are set in .env file")
    print()
    
    success = test_backend()
    
    if success:
        print("\n🎉 Backend is working perfectly!")
        print("📧 Emails should be sent to:")
        print("   • Admin: pixdotsolutions@gmail.com")
        print("   • User: test@example.com")
    else:
        print("\n❌ Backend test failed. Check:")
        print("1. Backend is running: python app.py")
        print("2. .env file exists with Gmail credentials")
        print("3. Gmail App Password is correct")
