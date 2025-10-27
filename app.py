from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Flask App Configuration
# -----------------------------
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Gmail Configuration
# -----------------------------
EMAIL_ADDRESS = os.getenv("EMAIL_USER", "pixdotsolutions@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# Debug info
logger.info(f"📧 Email configured: {'✅' if EMAIL_ADDRESS else '❌ MISSING'}")
logger.info(f"🔑 Password configured: {'✅' if EMAIL_PASSWORD else '❌ MISSING'}")

# -----------------------------
# Utility Functions
# -----------------------------
def validate_email(email):
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[-1]

def send_email_notification(name, email, message):
    """Send email notification to admin"""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = f"📩 New Contact Message from {name}"
        
        body = f"""
        You received a new message from your website contact form:
        
        📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        👤 Name: {name}
        📧 Email: {email}
        
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

# -----------------------------
# API Routes
# -----------------------------

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
            "send_email": "/send_email",
            "test_email": "/test_email"
        }
    }), 200

@app.route("/send_email", methods=["POST"])
def send_email():
    """Send contact form email"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False, 
                "error": "No data received"
            }), 400
        
        # Extract and validate data
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        message = data.get("message", "").strip()
        
        # Validation
        if not name:
            return jsonify({
                "success": False, 
                "error": "Name is required"
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
            
        if not message:
            return jsonify({
                "success": False, 
                "error": "Message is required"
            }), 400
        
        # Send email
        if send_email_notification(name, email, message):
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

@app.route("/test_email", methods=["POST"])
def test_email():
    """Test email functionality"""
    try:
        test_data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test email from Pixdot Backend API"
        }
        
        if send_email_notification(
            test_data["name"], 
            test_data["email"], 
            test_data["message"]
        ):
            return jsonify({
                "success": True,
                "message": "Test email sent successfully!"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Failed to send test email"
            }), 500
            
    except Exception as e:
        logger.error(f"❌ Test email error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# -----------------------------
# Error Handlers
# -----------------------------

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

# -----------------------------
# Run Flask App
# -----------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"🚀 Starting Pixdot Backend on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)