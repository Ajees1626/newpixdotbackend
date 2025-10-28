# Pixdot Backend Deployment Guide

## 🚀 Complete Backend Setup & Deployment

### 📁 Files Created/Updated:
- ✅ `app.py` - Complete Flask backend with contact form API
- ✅ `.env` - Environment variables for email configuration
- ✅ `requirements.txt` - All necessary Python dependencies
- ✅ `render.yaml` - Render.com deployment configuration
- ✅ `Procfile` - Heroku/Render deployment process
- ✅ `test_complete_backend.py` - Comprehensive test script

### 🔧 Local Development Setup:

#### 1. Install Dependencies:
```bash
cd backend
pip install -r requirements.txt
```

#### 2. Configure Email Settings:
Edit `.env` file:
```env
EMAIL_USER=pixdotsolutions@gmail.com
EMAIL_PASS=your_actual_gmail_app_password
RECEIVER_EMAIL=pixdotsolutions@gmail.com
```

#### 3. Get Gmail App Password:
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Enable **2-Factor Authentication**
3. Go to **Security** → **App passwords**
4. Generate password for "Mail"
5. Replace `your_actual_gmail_app_password` in `.env`

#### 4. Start Backend:
```bash
python app.py
```

#### 5. Test Backend:
```bash
python test_complete_backend.py
```

### 🌐 Deployment to Render.com:

#### 1. Push to GitHub:
```bash
git add .
git commit -m "Complete backend setup with email functionality"
git push origin main
```

#### 2. Deploy on Render:
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - **Name**: `pixdot-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --max-requests 1000`

#### 3. Set Environment Variables in Render:
- `EMAIL_USER`: `pixdotsolutions@gmail.com`
- `EMAIL_PASS`: `your_actual_gmail_app_password`
- `RECEIVER_EMAIL`: `pixdotsolutions@gmail.com`
- `FLASK_ENV`: `production`

#### 4. Update Frontend URL:
After deployment, update your frontend to use the Render URL:
```javascript
// In Contact.jsx, change:
const response = await fetch("http://localhost:5000/api/contact", {
// To:
const response = await fetch("https://your-render-app-name.onrender.com/api/contact", {
```

### 🔍 API Endpoints:

#### Health Check:
- `GET /` - Basic health check
- `GET /health` - Detailed health information

#### Contact Form:
- `POST /api/contact` - Submit contact form
- `POST /test_email` - Test email functionality

#### Request Format:
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "company": "Example Corp",
  "phone": "+1234567890",
  "subject": "Project Inquiry",
  "message": "I'm interested in your services..."
}
```

#### Response Format:
```json
{
  "success": true,
  "message": "Email sent successfully!"
}
```

### 🐛 Troubleshooting:

#### Email Not Sending:
1. Check Gmail App Password is correct
2. Ensure 2FA is enabled on Gmail account
3. Check backend logs for SMTP errors
4. Verify EMAIL_PASS environment variable

#### CORS Issues:
1. Backend includes localhost origins in CORS
2. For production, add your domain to CORS origins
3. Check browser console for CORS errors

#### Connection Issues:
1. Ensure backend is running on correct port
2. Check firewall settings
3. Verify URL in frontend matches backend

### 📧 Email Configuration:
- **SMTP Server**: `smtp.gmail.com`
- **Port**: `465` (SSL)
- **Authentication**: Gmail App Password required
- **From/To**: `pixdotsolutions@gmail.com`

### 🎯 Frontend Integration:
The backend is now fully compatible with your Contact.jsx form:
- ✅ Matches form data structure
- ✅ Proper error handling
- ✅ CORS configured for localhost
- ✅ Email notifications working
- ✅ Ready for production deployment

### 📞 Support:
If you encounter issues:
1. Check backend logs
2. Run test script: `python test_complete_backend.py`
3. Verify email configuration
4. Test with curl or Postman
