from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

BREVO_API_KEY = os.getenv("BREVO_API_KEY")

print(f"🔧 Brevo API Key: {'✅ Set' if BREVO_API_KEY else '❌ Not set'}")

@app.route("/")
def home():
    return "Pixdot Backend Running 🚀"

@app.route("/api/contact", methods=["POST", "OPTIONS"])
def contact():
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

        admin_html = f"""
        <h2>📩 New Contact Form Submission</h2>
        <p><strong>Name:</strong> {data['firstName']} {data['lastName']}</p>
        <p><strong>Email:</strong> {data['email']}</p>
        <p><strong>Phone:</strong> {data.get('phone', 'N/A')}</p>
        <p><strong>Company:</strong> {data.get('company', 'N/A')}</p>
        <p><strong>Subject:</strong> {data['subject']}</p>
        <p><strong>Message:</strong><br>{data['message']}</p>
        """

        user_html = f"""
        <p>Dear {data['firstName']},</p>
        <p>✅ Thank you for contacting <strong>Pixdot Solutions!</strong><br>
        We've received your message and will get back to you within 24 hours.</p>
        <p><strong>Your Message:</strong><br>{data['message']}</p>
        <p>📞 Need urgent help? Call us:<br>
        +91-87789 96278 / +91-87789 64644</p>
        <p>📧 Email: info@pixdotsolutions.com</p>
        <p>Best regards,<br>Team Pixdot Solutions 🚀</p>
        """

        def send_email(to_email, subject, html_content):
            url = "https://api.brevo.com/v3/smtp/email"
            headers = {
                "accept": "application/json",
                "api-key": BREVO_API_KEY,
                "content-type": "application/json"
            }
            data = {
                "sender": {
                    "name": "Pixdot Solutions",
                    "email": "info@pixdotsolutions.com"  # must be verified in Brevo
                },
                "to": [{"email": to_email}],
                "subject": subject,
                "htmlContent": html_content
            }
            response = requests.post(url, headers=headers, json=data)
            print(f"📤 Sent to {to_email}: {response.status_code}")
            print("🧾 Response:", response.text)
            return response.status_code, response.text

        admin_status, admin_text = send_email(
            "pixdotsolutions@gmail.com",
            f"New Contact: {data['firstName']} {data['lastName']}",
            admin_html
        )

        user_status, user_text = send_email(
            data["email"],
            "Thank you for contacting Pixdot Solutions",
            user_html
        )

        print("📤 Admin Response:", admin_status, admin_text)
        print("📤 User Response:", user_status, user_text)

        return jsonify({
            "success": True,
            "admin_status": admin_status,
            "user_status": user_status
        }), 200

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
