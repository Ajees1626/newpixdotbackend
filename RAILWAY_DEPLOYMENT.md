# Render Deployment Guide for Pixdot Backend

## 🚀 Quick Deployment Steps

### 1. Prepare Your Repository
- Make sure all files are committed to your Git repository
- Ensure `.env` file is NOT committed (add to .gitignore)

### 2. Deploy to Render
1. Go to [Render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Choose the `backend` folder as root directory

### 3. Configure Render Service
**Basic Settings:**
- **Name**: `pixdot-backend` (or any name you prefer)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

### 4. Set Environment Variables in Render
In Render dashboard, go to your service → Environment tab and add:

```
EMAIL_USER=pixdotsolutions@gmail.com
EMAIL_PASS=your-gmail-app-password
```

**Note**: Render automatically sets the `PORT` environment variable, so you don't need to set it manually.

### 5. Advanced Settings (Optional)
- **Auto-Deploy**: Enable to automatically deploy on git push
- **Health Check Path**: `/` (uses your home route)
- **Instance Type**: Free tier is sufficient for testing

## 🔧 Troubleshooting

### Common Issues:
1. **Build fails**: Check that `requirements.txt` has all dependencies with versions
2. **App crashes**: Usually caused by missing environment variables
3. **Email authentication fails**: Verify Gmail App Password is correct
4. **CORS errors**: Frontend URL should be added to CORS origins
5. **Timeout errors**: Render free tier has 15-minute sleep timeout

### Gmail App Password Setup:
1. Enable 2-Factor Authentication on Gmail
2. Go to Google Account → Security → App passwords
3. Generate new app password for "Mail"
4. Use this password in EMAIL_PASS variable

## 📁 Required Files for Render:
- `app.py` (main Flask app)
- `requirements.txt` (with version numbers)
- `Procfile` (tells Render how to run the app)
- `render.yaml` (optional, for advanced configuration)
- `.env` (environment variables - NOT committed to Git)

## ✅ Deployment Checklist:
- [ ] Debug mode set to False
- [ ] Port configuration uses environment variable
- [ ] Procfile exists with proper gunicorn settings
- [ ] requirements.txt has version numbers
- [ ] Environment variables set in Render dashboard
- [ ] Gmail App Password configured
- [ ] .env file NOT committed to Git
- [ ] Root directory set to `backend` folder

## 🌐 After Deployment:
- Your API will be available at: `https://your-service-name.onrender.com`
- Test endpoint: `https://your-service-name.onrender.com/`
- Contact API: `https://your-service-name.onrender.com/api/contact`

## 💡 Render vs Railway:
- **Render**: More stable, better free tier, easier configuration
- **Railway**: Faster deployments, more flexible pricing
- **Recommendation**: Render is better for production apps
