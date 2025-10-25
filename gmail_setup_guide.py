#!/usr/bin/env python3
"""
Gmail SMTP Setup Guide and Test
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def check_gmail_setup():
    """Check if Gmail 2FA and App Password are properly configured"""
    
    print("🔍 Gmail SMTP Setup Check")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    # Read credentials
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        email_user = None
        email_pass = None
        
        for line in lines:
            if line.startswith('EMAIL_USER='):
                email_user = line.split('=')[1].strip()
            elif line.startswith('EMAIL_PASS='):
                email_pass = line.split('=')[1].strip()
        
        if not email_user or not email_pass:
            print("❌ Missing credentials in .env file")
            return False
        
        print(f"📧 Email User: {email_user}")
        print(f"🔑 App Password: {email_pass} (Length: {len(email_pass)})")
        
        # Test Gmail SMTP connection
        try:
            print("\n🧪 Testing Gmail SMTP connection...")
            
            # Create test email
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_user  # Send to self for testing
            msg['Subject'] = "Gmail SMTP Test"
            
            body = "This is a test email to verify Gmail SMTP configuration."
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)
            server.quit()
            
            print("✅ Gmail SMTP connection successful!")
            print("📧 Test email sent to your inbox")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Gmail Authentication Failed: {e}")
            print("\n💡 Solutions:")
            print("1. Enable 2-Factor Authentication on your Gmail account")
            print("2. Generate a new App Password:")
            print("   - Go to Google Account Settings")
            print("   - Security → 2-Step Verification → App passwords")
            print("   - Generate password for 'Mail'")
            print("3. Update .env file with the new 16-character password")
            return False
            
        except Exception as e:
            print(f"❌ SMTP Error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def create_correct_env():
    """Create a template .env file with instructions"""
    
    template = """# Gmail SMTP Configuration
# Replace with your actual Gmail credentials

EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-16-character-app-password

# Instructions:
# 1. Enable 2-Factor Authentication on your Gmail account
# 2. Go to Google Account → Security → 2-Step Verification → App passwords
# 3. Generate a new App Password for 'Mail'
# 4. Replace the values above with your actual credentials
# 5. The App Password should be 16 characters without spaces
"""
    
    try:
        with open('.env.template', 'w') as f:
            f.write(template)
        print("✅ Created .env.template file with instructions")
        return True
    except Exception as e:
        print(f"❌ Error creating template: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Gmail SMTP Setup Assistant")
    print("=" * 50)
    
    if check_gmail_setup():
        print("\n✅ Gmail SMTP is properly configured!")
        print("🎉 Your backend should now work correctly")
    else:
        print("\n❌ Gmail SMTP setup needs attention")
        create_correct_env()
        print("\n📝 Please follow the instructions in .env.template")
        print("🔧 After updating credentials, run this script again")
