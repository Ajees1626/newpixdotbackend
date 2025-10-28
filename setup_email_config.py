#!/usr/bin/env python3
"""
Email Configuration Setup Script
Run this script to set up your email configuration
"""

import os

def create_env_file():
    """Create .env file with email configuration"""
    env_content = """# Email Configuration
EMAIL_USER=pixdotsolutions@gmail.com
EMAIL_PASS=your_app_password_here
RECEIVER_EMAIL=pixdotsolutions@gmail.com

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print("\n📧 IMPORTANT: Update the EMAIL_PASS with your Gmail App Password")
    print("   Follow these steps:")
    print("   1. Go to your Google Account settings")
    print("   2. Enable 2-Factor Authentication")
    print("   3. Generate an App Password for 'Mail'")
    print("   4. Replace 'your_app_password_here' with the generated password")

if __name__ == "__main__":
    create_env_file()
