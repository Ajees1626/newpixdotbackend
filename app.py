from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Brevo API key (from your Render environment variables)
BREVO_API_KEY = os.getenv("BREVO_API_KEY")

# Debug check
print(f"🔧 Brevo API Key: {'✅ Set' if BREVO_API_KEY else '❌ Not set'}")

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

        required = ["firstName", "lastName", "email", "subject", "message"]
        for field in required:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        # --- Email to Admin ---
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

        # --- Auto reply to User ---
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

        # Function to send email via Brevo
        def send_email(to_email, subject, html_content):
            url = "https://api.brevo.com/v3/smtp/email"
            headers = {
                "accept": "application/json",
                "api-key": BREVO_API_KEY,
                "content-type": "application/json"
            }
            data = {
                "sender": {"name": "Pixdot Solutions", "email": "noreply@pixdotsolutions.com"},
                "to": [{"email": to_email}],
                "subject": subject,
                "htmlContent": f"<pre>{html_content}</pre>"
            }
            response = requests.post(url, headers=headers, json=data)
            return response.status_code, response.text

        # Send to Admin
        admin_status, admin_text = send_email(
            "pixdotsolutions@gmail.com",
            f"New Contact: {data['firstName']} {data['lastName']}",
            admin_body
        )

        # Send Auto Reply to User
        user_status, user_text = send_email(
            data["email"],
            "Thank you for contacting Pixdot Solutions",
            user_body
        )

        print(f"✅ Admin mail: {admin_status}, User mail: {user_status}")

        return jsonify({
            "success": True,
            "message": "Emails sent successfully",
            "admin_status": admin_status,
            "user_status": user_status
        }), 200

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
