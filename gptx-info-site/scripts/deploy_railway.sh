#!/bin/bash

# GPTX Exchange - Railway Deployment Script
# This script helps deploy the GPTX Exchange to Railway

set -e

echo "🚀 GPTX Exchange - Railway Deployment"
echo "======================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found."
    echo ""
    echo "Please install Railway CLI using one of these methods:"
    echo ""
    echo "Option 1 - Using npm (with sudo):"
    echo "  sudo npm install -g @railway/cli"
    echo ""
    echo "Option 2 - Using npm (user install):"
    echo "  npm install -g @railway/cli --prefix ~/.local"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Option 3 - Download binary directly:"
    echo "  curl -fsSL https://railway.app/install.sh | sh"
    echo ""
    echo "After installation, run this script again:"
    echo "  make deploy-railway"
    echo ""
    exit 1
fi

# Check if git repo is clean
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  You have uncommitted changes. Committing them now..."
    git add .
    git commit -m "Prepare for Railway deployment"
    echo "✅ Changes committed"
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main
echo "✅ Code pushed to GitHub"

# Login to Railway (if not already logged in)
echo "🔐 Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    echo "Please login to Railway:"
    railway login
fi

# Initialize Railway project (if not already initialized)
if [ ! -f "railway.toml" ]; then
    echo "❌ railway.toml not found. This shouldn't happen!"
    exit 1
fi

echo "🚀 Deploying to Railway..."
railway up

echo ""
echo "🎉 Deployment initiated!"
echo ""
echo "Next steps:"
echo "1. Go to railway.app dashboard"
echo "2. Add environment variables (DATABASE_URL, SECRET_KEY, etc.)"
echo "3. Add PostgreSQL service if needed"
echo "4. Configure custom domain (optional)"
echo ""
echo "Your app will be available at the Railway-provided URL"
echo "Check the Railway dashboard for deployment status and logs"