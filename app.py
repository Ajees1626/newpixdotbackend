from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Flask setup
app = Flask(__name__)
CORS(app)  # Allow all origins (for React frontend)

# ---------------------------
# ENV Variables (Render Setup)
# ---------------------------
EMAIL_USER = os.getenv("EMAIL_USER", "pixdotsolutions@gmail.com")  # your gmail
EMAIL_PASS = os.getenv("EMAIL_PASS")  # your app password
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", EMAIL_USER)  # where mail should be sent

# ---------------------------
# HOME Route (for testing)
# ---------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "✅ Backend Running Successfully!",
        "message": "Pixdot Mail API Ready"
    }), 200


# ---------------------------
# SEND EMAIL Route
# ---------------------------
@app.route("/send_email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400

        name = data.get("name", "Anonymous")
        email = data.get("email", "")
        message = data.get("message", "")

        # Validate inputs
        if not email or not message:
            return jsonify({"success": False, "error": "Email and message are required"}), 400

        # Compose Email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = f"📩 New Enquiry from {name}"

        body = f"""
        You received a new message from your website contact form.

        👤 Name: {name}
        📧 Email: {email}

        💬 Message:
        {message}
        """

        msg.attach(MIMEText(body, "plain"))

        # Send Email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        print("✅ Email sent successfully!")
        return jsonify({"success": True, "message": "Email sent successfully!"}), 200

    except smtplib.SMTPAuthenticationError:
        print("❌ Gmail Authentication Failed — Check App Password.")
        return jsonify({"success": False, "error": "Invalid Gmail credentials"}), 500
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------
# MAIN RUN (Local)
# ---------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
