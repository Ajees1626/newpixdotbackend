from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables (optional)
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

# Flask App Configuration
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email Configuration
EMAIL_ADDRESS = os.getenv("EMAIL_USER", "pixdotsolutions@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# Debug info
logger.info(f"📧 Email configured: {'✅' if EMAIL_ADDRESS else '❌ MISSING'}")
logger.info(f"🔑 Password configured: {'✅' if EMAIL_PASSWORD else '❌ MISSING'}")

def validate_email(email):
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[-1]

def send_email_notification(firstName, lastName, email, company, phone, subject, message):
    """Send email notification to admin"""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = f"📩 New Contact Form: {subject}"
        
        body = f"""
        New Contact Form Submission from Pixdot Website
        
        📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        👤 Contact Details:
        Name: {firstName} {lastName}
        Email: {email}
        Company: {company}
        Phone: {phone}
        Subject: {subject}
        
        💬 Message:
        {message}
        
        ---
        This message was sent from your Pixdot website contact form.
        """
        
        msg.attach(MIMEText(body, "plain"))
        
        # Send email using SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        logger.info("✅ Email sent successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Email send error: {e}")
        return False

# API Routes
@app.route("/")
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "success",
        "message": "✅ Pixdot Backend Running (Gmail SMTP Integration Active)",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }), 200

@app.route("/health")
def health():
    """Detailed health check"""
    return jsonify({
        "status": "healthy",
        "service": "Pixdot Backend API",
        "timestamp": datetime.now().isoformat(),
        "email_configured": bool(EMAIL_ADDRESS and EMAIL_PASSWORD),
        "endpoints": {
            "home": "/",
            "health": "/health",
            "contact": "/api/contact"
        }
    }), 200

@app.route("/api/contact", methods=["POST"])
def send_email():
    """Send contact form email"""
    try:
        data = request.get_json()
        logger.info(f"📧 Received contact form data: {data}")
        
        if not data:
            return jsonify({
                "success": False, 
                "error": "No data received"
            }), 400
        
        # Extract and validate data (matching frontend form structure)
        firstName = data.get("firstName", "").strip()
        lastName = data.get("lastName", "").strip()
        email = data.get("email", "").strip()
        company = data.get("company", "").strip()
        phone = data.get("phone", "").strip()
        subject = data.get("subject", "").strip()
        message = data.get("message", "").strip()
        
        # Validation
        if not firstName:
            return jsonify({
                "success": False, 
                "error": "First name is required"
            }), 400
            
        if not lastName:
            return jsonify({
                "success": False, 
                "error": "Last name is required"
            }), 400
            
        if not email:
            return jsonify({
                "success": False, 
                "error": "Email is required"
            }), 400
            
        if not validate_email(email):
            return jsonify({
                "success": False, 
                "error": "Invalid email format"
            }), 400
            
        if not subject:
            return jsonify({
                "success": False, 
                "error": "Subject is required"
            }), 400
            
        if not message:
            return jsonify({
                "success": False, 
                "error": "Message is required"
            }), 400
        
        # Send email
        if send_email_notification(firstName, lastName, email, company, phone, subject, message):
            return jsonify({
                "success": True, 
                "message": "Email sent successfully!"
            }), 200
        else:
            return jsonify({
                "success": False, 
                "error": "Failed to send email"
            }), 500
            
    except smtplib.SMTPAuthenticationError:
        logger.error("❌ Gmail authentication failed. Check App Password.")
        return jsonify({
            "success": False, 
            "error": "Invalid Gmail credentials"
        }), 500
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return jsonify({
            "success": False, 
            "error": "Internal server error"
        }), 500

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": "Method not allowed"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

# Run Flask App
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"🚀 Starting Pixdot Backend on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)