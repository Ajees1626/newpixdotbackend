#!/usr/bin/env python3
"""
Setup script to create .env file for Gmail SMTP configuration
"""

import os

def create_env_file():
    """Create .env file with Gmail credentials"""
    
    # Gmail credentials
    email_user = "pixdotsolutions@gmail.com"
    email_pass = "ekrj uwyb atnl fhwy"
    
    env_content = f"""EMAIL_USER={email_user}
EMAIL_PASS={email_pass}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print(f"📧 Email User: {email_user}")
        print("🔑 App Password: Set")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has correct content"""
    if os.path.exists('.env'):
        print("✅ .env file exists")
        try:
            with open('.env', 'r') as f:
                content = f.read()
                if 'EMAIL_USER' in content and 'EMAIL_PASS' in content:
                    print("✅ .env file has correct content")
                    return True
                else:
                    print("❌ .env file missing required variables")
                    return False
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
            return False
    else:
        print("❌ .env file not found")
        return False

if __name__ == "__main__":
    print("🚀 Setting up Gmail SMTP configuration...")
    
    if check_env_file():
        print("✅ Environment already configured!")
    else:
        if create_env_file():
            print("✅ Setup complete! You can now run: python app.py")
        else:
            print("❌ Setup failed. Please check permissions.")
