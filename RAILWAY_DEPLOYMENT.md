# Railway Deployment Guide for Pixdot Backend

## 🚀 Quick Deployment Steps

### 1. Prepare Your Repository
- Make sure all files are committed to your Git repository
- Ensure `.env` file is NOT committed (add to .gitignore)

### 2. Deploy to Railway
1. Go to [Railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Choose the `backend` folder as root directory

### 3. Set Environment Variables in Railway
In Railway dashboard, go to your project → Variables tab and add:

```
EMAIL_USER=pixdotsolutions@gmail.com
EMAIL_PASS=your-gmail-app-password
PORT=5000
```

### 4. Important Notes
- **Never commit `.env` file to Git** - it contains sensitive credentials
- Use Gmail App Password, not your regular Gmail password
- Railway automatically sets the PORT environment variable
- The app will restart automatically when you push changes

## 🔧 Troubleshooting

### Common Issues:
1. **App crashes after 1 minute**: Usually caused by `debug=True` in production
2. **Port binding errors**: Make sure to use `os.getenv("PORT", 5000)`
3. **Email authentication fails**: Check Gmail App Password is correct
4. **CORS errors**: Frontend URL should be added to CORS origins

### Gmail App Password Setup:
1. Enable 2-Factor Authentication on Gmail
2. Go to Google Account → Security → App passwords
3. Generate new app password for "Mail"
4. Use this password in EMAIL_PASS variable

## 📁 Required Files for Railway:
- `app.py` (main Flask app)
- `requirements.txt` (with version numbers)
- `Procfile` (tells Railway how to run the app)
- `.env` (environment variables - NOT committed to Git)

## ✅ Deployment Checklist:
- [ ] Debug mode set to False
- [ ] Port configuration uses environment variable
- [ ] Procfile exists
- [ ] requirements.txt has version numbers
- [ ] Environment variables set in Railway dashboard
- [ ] Gmail App Password configured
- [ ] .env file NOT committed to Git
