# Deploy Smart Watches E-commerce to Render.com

## Prerequisites
- GitHub account with your code pushed
- Render.com account (free tier available)

## Step-by-Step Deployment Guide

### 1. Prepare Your Repository
Your app is already configured with:
- ✅ `render.yaml` - Render configuration
- ✅ `build.sh` - Build script
- ✅ `requirements.txt` - Python dependencies
- ✅ `wsgi.py` - WSGI entry point

### 2. Push to GitHub
```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 3. Create Render Account
1. Go to https://render.com
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### 4. Deploy Your App

#### Option A: Using render.yaml (Recommended - One Click)
1. Click **"New +"** → **"Blueprint"**
2. Connect your GitHub repository: `yawriches/digital`
3. Render will automatically detect `render.yaml`
4. Click **"Apply"**
5. Render will create:
   - Web Service (your Flask app)
   - PostgreSQL Database (automatically connected)

#### Option B: Manual Setup
1. **Create PostgreSQL Database:**
   - Click **"New +"** → **"PostgreSQL"**
   - Name: `smartwatches-db`
   - Region: Choose closest to you
   - Click **"Create Database"**

2. **Create Web Service:**
   - Click **"New +"** → **"Web Service"**
   - Connect your repository: `yawriches/digital`
   - Root Directory: `smartwatches`
   - Environment: **Python 3**
   - Build Command: `pip install -r requirements.txt && chmod +x build.sh && ./build.sh`
   - Start Command: `gunicorn wsgi:app`
   - Click **"Create Web Service"**

### 5. Configure Environment Variables

In your Web Service settings, add these environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | (Auto-filled from database) | Internal connection string |
| `SECRET_KEY` | (Auto-generate or use your own) | Flask secret key |
| `PAYSTACK_SECRET_KEY` | `sk_test_1e411c84085bea8bd50afcc3046602bb08d13450` | Your Paystack test key |
| `PAYSTACK_PUBLIC_KEY` | `pk_test_20f85304711302d863977ca96e048725bb95ec25` | Your Paystack public key |

### 6. Seed the Database (Optional)

After first deployment, you can seed your database:

1. Go to your Web Service → **"Shell"** tab
2. Run:
```bash
python seed.py
```

This will create:
- Admin account: `admin@smartwatches.com` / `admin123`
- Customer account: `john@example.com` / `password123`
- 8 sample products across 4 categories

### 7. Access Your Live Site

Once deployed, Render will provide you with a URL like:
```
https://smartwatches-ecommerce.onrender.com
```

Your e-commerce site is now live! 🎉

## Important Notes

### Free Tier Limitations
- Web service spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds (cold start)
- PostgreSQL database: 90-day expiration on free tier

### Upgrade to Paid Plan ($7/month)
- No spin-down (always active)
- Faster performance
- Persistent database
- Custom domain support

### File Uploads
Render provides **ephemeral disk storage**. For production:
- Use Cloudinary for product images (recommended)
- Or use Render Disk (paid add-on, $1/GB/month)

### Database Backups
- Free tier: No automatic backups
- Paid tier: Daily automatic backups included

## Troubleshooting

### Build Failed
- Check build logs in Render dashboard
- Verify all dependencies in `requirements.txt`
- Ensure Python version compatibility

### Database Connection Error
- Verify `DATABASE_URL` environment variable is set
- Check database is running and accessible
- Review connection string format

### 500 Internal Server Error
- Check application logs in Render dashboard
- Verify all environment variables are set correctly
- Ensure database tables are created (run `build.sh`)

### Static Files Not Loading
- Render serves static files automatically from `app/static/`
- Check file paths in templates are correct
- Verify static files are committed to Git

## Next Steps

1. **Custom Domain**: Add your own domain in Render settings
2. **SSL Certificate**: Automatically provided by Render (free)
3. **Monitoring**: Set up health checks and alerts
4. **Scaling**: Upgrade plan as traffic grows
5. **Production Database**: Consider upgrading to paid PostgreSQL

## Support

- Render Documentation: https://render.com/docs
- Community Forum: https://community.render.com
- Status Page: https://status.render.com

---

**Your Smart Watches E-commerce is ready for the cloud! 🚀**
