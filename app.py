from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Gmail credentials (from .env)
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

# Debug: Print credentials status
print(f"🔧 Gmail User: {'✅ Set' if GMAIL_USER else '❌ Not set'}")
print(f"🔧 Gmail Pass: {'✅ Set' if GMAIL_PASS else '❌ Not set'}")

@app.route("/")
def home():
    return "Pixdot Backend Running 🚀"

@app.route("/api/contact", methods=["POST", "OPTIONS"])
def contact():
    # Handle CORS preflight request
    if request.method == "OPTIONS":
        response = jsonify({"status": "OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON body received"}), 400

        # Required fields
        required = ["firstName", "lastName", "email", "subject", "message"]
        for field in required:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        # --- Email to Admin (pixdotsolutions@gmail.com) ---
        admin_body = f"""
        📩 New Contact Form Submission

        👤 Name: {data['firstName']} {data['lastName']}
        📧 Email: {data['email']}
        📱 Phone: {data.get('phone', 'N/A')}
        🏢 Company: {data.get('company', 'N/A')}

        📝 Subject: {data['subject']}
        💬 Message:
        {data['message']}
        """

        msg_admin = MIMEMultipart()
        msg_admin["From"] = GMAIL_USER
        msg_admin["To"] = "pixdotsolutions@gmail.com"
        msg_admin["Subject"] = f"New Contact: {data['firstName']} {data['lastName']}"
        msg_admin.attach(MIMEText(admin_body, "plain"))

        # --- Auto reply to User (Thank You mail) ---
        user_body = f"""
        Dear {data['firstName']},

        ✅ Thank you for contacting Pixdot Solutions!
        We've received your message and will get back to you within 24 hours.

        📌 Your Message:
        {data['message']}

        📞 Need urgent help? Call us at:
        • +91-87789 96278
        • +91-87789 64644

        📧 Email: info@pixdotsolutions.com

        Best regards,
        Team Pixdot Solutions 🚀
        """

        msg_user = MIMEMultipart()
        msg_user["From"] = GMAIL_USER
        msg_user["To"] = data["email"]
        msg_user["Subject"] = "Thank you for contacting Pixdot Solutions"
        msg_user.attach(MIMEText(user_body, "plain"))

        # --- Send Emails ---
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(GMAIL_USER, GMAIL_PASS)
                
                # Send to Admin
                server.sendmail(GMAIL_USER, "pixdotsolutions@gmail.com", msg_admin.as_string())
                print(f"✅ Email sent to admin: pixdotsolutions@gmail.com")
                
                # Send to User
                server.sendmail(GMAIL_USER, data["email"], msg_user.as_string())
                print(f"✅ Auto-reply sent to user: {data['email']}")

            return jsonify({
                "success": True, 
                "message": "Message sent successfully",
                "admin_email": "pixdotsolutions@gmail.com",
                "user_email": data["email"]
            }), 200

        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Gmail Authentication Error: {e}")
            return jsonify({"error": "Gmail authentication failed. Please check your credentials."}), 500
        except smtplib.SMTPException as e:
            print(f"❌ SMTP Error: {e}")
            return jsonify({"error": f"Email sending failed: {str(e)}"}), 500

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)