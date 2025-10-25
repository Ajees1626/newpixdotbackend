# Pixdot Backend - Contact Form API

Flask backend for handling contact form submissions and sending emails.

## 🚀 Local Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Create .env File
Create a `.env` file in the backend folder:
```
GMAIL_USER=pixdotsolutions@gmail.com
GMAIL_PASS=ekrj uwyb atnl fhwy
```

### 3. Run Locally
```bash
python app.py
```

### 4. Test Backend
```bash
python test_local.py
```

## 🌐 Deploy to Render

### 1. Push to GitHub
- Create a GitHub repository
- Push your backend code to GitHub

### 2. Deploy on Render
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Add environment variables:
   - `GMAIL_USER` = `pixdotsolutions@gmail.com`
   - `GMAIL_PASS` = `ekrj uwyb atnl fhwy`

## 📧 Email Flow

1. **User submits form** → Frontend sends POST to `/api/contact`
2. **Backend processes** → Validates required fields
3. **Sends admin email** → `pixdotsolutions@gmail.com` (notification)
4. **Sends user email** → User's email (auto-reply)
5. **Returns success** → Frontend shows confirmation

## 🔧 API Endpoints

- `GET /` - Health check
- `POST /api/contact` - Submit contact form

## 📝 Required Form Fields

- firstName (required)
- lastName (required)
- email (required)
- subject (required)
- message (required)
- phone (optional)
- company (optional)

## 🛠️ Troubleshooting

### Gmail Authentication Issues
1. Enable 2-Factor Authentication on Gmail
2. Generate App Password (not regular password)
3. Use App Password in .env file
4. App password format: 4 words separated by spaces

### Common Errors
- **401 Unauthorized**: Check Gmail credentials
- **500 Internal Error**: Check Gmail App Password
- **CORS Error**: Backend handles CORS automatically