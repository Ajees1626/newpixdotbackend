"""
Script to switch between local and Render URLs in Contact.jsx
"""

import re

def switch_to_local():
    """Switch Contact.jsx to use local server"""
    with open('../frontend/src/pages/Contact.jsx', 'r') as f:
        content = f.read()
    
    # Replace Render URLs with local URLs
    content = content.replace('https://pixdotbackend.onrender.com', 'http://localhost:5000')
    
    with open('../frontend/src/pages/Contact.jsx', 'w') as f:
        f.write(content)
    
    print("✅ Switched to LOCAL server (http://localhost:5000)")

def switch_to_render():
    """Switch Contact.jsx to use Render server"""
    with open('../frontend/src/pages/Contact.jsx', 'r') as f:
        content = f.read()
    
    # Replace local URLs with Render URLs
    content = content.replace('http://localhost:5000', 'https://pixdotbackend.onrender.com')
    
    with open('../frontend/src/pages/Contact.jsx', 'w') as f:
        f.write(content)
    
    print("✅ Switched to RENDER server (https://pixdotbackend.onrender.com)")

if __name__ == "__main__":
    print("🔄 URL Switcher for Contact.jsx")
    print("1. Switch to LOCAL (http://localhost:5000)")
    print("2. Switch to RENDER (https://pixdotbackend.onrender.com)")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        switch_to_local()
    elif choice == "2":
        switch_to_render()
    else:
        print("❌ Invalid choice")
