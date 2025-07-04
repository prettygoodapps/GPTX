# Railway Deployment Guide for GPTX Exchange

This guide will walk you through deploying the GPTX Exchange to Railway.

## Prerequisites

1. **GitHub Account**: Your code needs to be in a GitHub repository
2. **Railway Account**: Sign up at [railway.app](https://railway.app)
3. **Project Ready**: Ensure your project is committed and pushed to GitHub

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure your project is committed to GitHub:

```bash
# Add all files
git add .

# Commit changes
git commit -m "Add Railway deployment configuration"

# Push to GitHub
git push origin main
```

### 2. Deploy to Railway

#### Option A: Railway CLI (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

#### Option B: Railway Dashboard
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your GPTX Exchange repository
5. Railway will automatically detect it's a Python project

### 3. Configure Environment Variables

In Railway dashboard, go to your project and add these environment variables:

**Required Variables:**
```
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:port/db
```

**Optional Variables:**
```
SECRET_KEY=your-production-secret-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
CARBON_API_KEY=your-carbon-offset-api-key
WEB3_PROVIDER_URL=your-web3-provider-url
```

### 4. Add PostgreSQL Database

1. In Railway dashboard, click "Add Service"
2. Select "PostgreSQL"
3. Railway will automatically set the `DATABASE_URL` environment variable

### 5. Configure Custom Domain (Optional)

1. In Railway dashboard, go to "Settings"
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## Deployment Files Explained

### `railway.toml`
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "poetry run uvicorn gptx.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[environments.production]
variables = { ENVIRONMENT = "production" }
```

### `Procfile`
```
web: poetry run uvicorn gptx.main:app --host 0.0.0.0 --port $PORT
```

## Production Considerations

### Database Migration
The app will automatically create tables on startup, but for production you should:

1. Use PostgreSQL instead of SQLite
2. Set up proper database migrations
3. Configure database backups

### Security
1. Change the `SECRET_KEY` to a secure random string
2. Set `DEBUG=False` in production
3. Configure CORS properly for your domain
4. Use HTTPS (Railway provides this automatically)

### Monitoring
1. Railway provides built-in monitoring
2. Check logs in Railway dashboard
3. Set up alerts for downtime

## Troubleshooting

### Common Issues

**Build Fails:**
- Check that `pyproject.toml` is properly configured
- Ensure all dependencies are listed
- Check Python version compatibility

**App Won't Start:**
- Verify the start command in `railway.toml`
- Check environment variables are set
- Review logs in Railway dashboard

**Database Connection Issues:**
- Ensure PostgreSQL service is running
- Check `DATABASE_URL` environment variable
- Verify database credentials

### Useful Commands

```bash
# View logs
railway logs

# Open app in browser
railway open

# Check status
railway status

# Connect to database
railway connect postgresql
```

## Post-Deployment

1. **Test the deployment**: Visit your Railway URL
2. **Check API endpoints**: Test `/health`, `/api/docs`, etc.
3. **Verify database**: Ensure tables are created
4. **Monitor performance**: Watch Railway metrics

## Scaling

Railway automatically handles scaling, but you can:
1. Monitor resource usage in dashboard
2. Upgrade plan if needed
3. Configure auto-scaling policies

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- GPTX Exchange Issues: Create GitHub issues in your repository

---

Your GPTX Exchange should now be live on Railway! 🚀