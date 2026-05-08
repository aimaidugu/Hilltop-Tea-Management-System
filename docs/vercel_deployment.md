# Vercel deployment for Hilltop Tea

This guide will help you deploy the Hilltop Tea application to Vercel.

## Prerequisites

1. A Vercel account (free tier works)
2. Git repository (GitHub, GitLab, or Bitbucket)
3. Python 3.8+ installed locally

## Step 1: Prepare Your Repository

### 1.1 Initialize Git (if not already done)

```bash
cd "/Users/Apple/Desktop/Final year Project/hilltop_tea"
git init
git add .
git commit -m "Initial commit: Hilltop Tea Management System"
```

### 1.2 Push to GitHub

1. Create a new repository on GitHub
2. Add remote and push:

```bash
git remote add origin https://github.com/YOUR_USERNAME/hilltop_tea.git
git branch -M main
git push -u origin main
```

## Step 2: Set Up PostgreSQL Database

Vercel provides a free PostgreSQL database through their integration.

### 2.1 Create PostgreSQL Database on Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Go to your project settings
3. Click "Storage" → "Create Database"
4. Select "PostgreSQL" and create a free database
5. Copy the `DATABASE_URL` from the database settings

### 2.2 Alternative: Use Supabase (Free PostgreSQL)

1. Go to [Supabase](https://supabase.com)
2. Create a free account
3. Create a new project
4. Go to Settings → Database
5. Copy the connection string (use "Session" or "Transaction" pooler)

## Step 3: Deploy to Vercel

### 3.1 Import Project to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure the project:

**Framework Preset:** Other
**Root Directory:** `./`
**Build Command:** (leave empty)
**Output Directory:** (leave empty)

### 3.2 Configure Environment Variables

Add these environment variables in Vercel project settings:

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | Generate a random string | Flask secret key |
| `DATABASE_URL` | Your PostgreSQL connection string | Database connection |
| `PYTHON_VERSION` | `3.9` | Python version |

**Generate SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**DATABASE_URL format:**
```
postgresql://username:password@host:port/database
```

### 3.3 Deploy

Click "Deploy" and wait for the deployment to complete.

## Step 4: Initialize Database

After deployment, you need to create the database tables and default admin user.

### 4.1 Option 1: Use Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Run Python commands in serverless environment
vercel env pull .env
```

### 4.2 Option 2: Create a Setup Script

Run this script locally with your production database URL:

```bash
export DATABASE_URL="your_production_database_url"
python setup_db.py
```

## Step 5: Configure Domain (Optional)

### 5.1 Use Vercel's Default Domain

Your app will be available at: `https://your-project-name.vercel.app`

### 5.2 Add Custom Domain

1. Go to project settings in Vercel
2. Click "Domains"
3. Add your custom domain
4. Configure DNS records as instructed

## Step 6: Test Your Deployment

1. Visit your Vercel URL
2. Login with: `admin` / `admin123`
3. Change the default password immediately
4. Test all features

## Troubleshooting

### Issue: "Module not found" errors

**Solution:** Ensure all dependencies are in `requirements.txt`

### Issue: Database connection errors

**Solution:** Verify `DATABASE_URL` is correct and accessible

### Issue: Static files not loading

**Solution:** Vercel serves static files from the `static/` directory automatically

### Issue: Session issues

**Solution:** Ensure `SECRET_KEY` is set in environment variables

## Security Recommendations

1. **Change default password** immediately after first login
2. **Use HTTPS** (Vercel provides this automatically)
3. **Set strong SECRET_KEY** in environment variables
4. **Enable 2FA** on your Vercel account
5. **Regular backups** of your PostgreSQL database
6. **Monitor logs** in Vercel dashboard

## Monitoring

### View Logs

1. Go to Vercel Dashboard
2. Select your project
3. Click "Logs" tab
4. View real-time logs

### View Analytics

1. Go to Vercel Dashboard
2. Select your project
3. Click "Analytics" tab

## Updating Your Application

1. Make changes locally
2. Commit and push to GitHub
3. Vercel will automatically deploy on push

```bash
git add .
git commit -m "Update: description of changes"
git push
```

## Cost

- **Vercel:** Free tier (100GB bandwidth, 100GB-hours execution)
- **PostgreSQL:** Free tier (500MB storage)
- **Total:** $0/month for small deployments

## Alternative: Render.com

If you prefer Render.com:

1. Create account at [render.com](https://render.com)
2. Create "Web Service"
3. Connect your GitHub repository
4. Set environment variables
5. Add PostgreSQL database
6. Deploy

## Support

For issues:
- Check Vercel logs
- Review Vercel documentation: https://vercel.com/docs
- Check Flask documentation: https://flask.palletsprojects.com/
