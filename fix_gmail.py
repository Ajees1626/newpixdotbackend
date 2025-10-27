#!/usr/bin/env python3
"""
Fix Gmail App Password format
"""

import os

def fix_env_file():
    """Fix the .env file with correct Gmail App Password format"""
    
    # Correct Gmail App Password (16 characters, no spaces)
    email_user = "pixdotsolutions@gmail.com"
    email_pass = "ekrj uwyb atnl fhwy".replace(" ", "")  # Remove spaces
    
    env_content = f"""EMAIL_USER={email_user}
EMAIL_PASS={email_pass}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file updated with correct format!")
        print(f"📧 Email User: {email_user}")
        print(f"🔑 App Password: {email_pass} (16 chars, no spaces)")
        return True
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing Gmail App Password format...")
    print("=" * 50)
    
    if fix_env_file():
        print("✅ Gmail credentials fixed!")
        print("💡 Restart the backend server: python app.py")
    else:
        print("❌ Failed to fix credentials")

