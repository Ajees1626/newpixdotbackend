#!/usr/bin/env python3
"""
Deployment Verification Script
Run this before deploying to ensure everything is ready
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {str(e)}")
        return False

def check_file_exists(filepath, description):
    """Check if a file exists"""
    print(f"🔍 Checking {description}...")
    if os.path.exists(filepath):
        print(f"✅ {description} - EXISTS")
        return True
    else:
        print(f"❌ {description} - MISSING")
        return False

def main():
    print("🚀 Pixdot Backend Deployment Verification")
    print("=" * 50)
    
    # Check required files
    files_to_check = [
        ("app.py", "Main Flask application"),
        ("requirements.txt", "Python dependencies"),
        ("render.yaml", "Render deployment config"),
        ("Procfile", "Process configuration"),
        (".env", "Environment variables")
    ]
    
    all_files_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    if not all_files_exist:
        print("\n❌ Missing required files. Cannot proceed with deployment.")
        return False
    
    # Test Python imports
    if not run_command("python -c \"import flask, flask_cors, dotenv, smtplib\"", "Testing Python imports"):
        return False
    
    # Test app import
    if not run_command("python -c \"import app; print('App imports successfully')\"", "Testing app import"):
        return False
    
    # Check environment variables
    print("\n🔍 Checking environment variables...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        
        if email_user:
            print(f"✅ EMAIL_USER: {email_user}")
        else:
            print("❌ EMAIL_USER: Not set")
            
        if email_pass and email_pass != "your_app_password_here":
            print("✅ EMAIL_PASS: Configured")
        else:
            print("❌ EMAIL_PASS: Not configured properly")
            
    except Exception as e:
        print(f"❌ Error checking environment: {str(e)}")
    
    print("\n" + "=" * 50)
    print("📋 Deployment Checklist:")
    print("1. ✅ All required files present")
    print("2. ✅ Python dependencies can be imported")
    print("3. ✅ Flask app imports successfully")
    print("4. 🔄 Push code to GitHub")
    print("5. 🔄 Deploy on Render.com")
    print("6. 🔄 Set EMAIL_PASS environment variable")
    print("7. 🔄 Test deployed application")
    
    print("\n🚀 Ready for deployment!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
