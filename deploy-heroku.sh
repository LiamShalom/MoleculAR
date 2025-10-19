#!/bin/bash

# Heroku Deployment Script for Molecular Analysis API
# This script will deploy your backend to Heroku

set -e  # Exit on any error

echo "🚀 Starting Heroku Deployment for Molecular Analysis API"
echo "=================================================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Installing..."
    brew install heroku/brew/heroku
fi

# Check if user is logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "❌ Not logged in to Heroku. Please log in:"
    heroku login
fi

# Check if account is verified
echo "🔐 Checking Heroku account status..."
if ! heroku apps &> /dev/null; then
    echo "❌ Account verification required!"
    echo "Please visit: https://heroku.com/verify"
    echo "Add a credit card for verification (you won't be charged for free tier)"
    echo "Then run this script again."
    exit 1
fi

echo "✅ Account verified!"

# Create unique app name
APP_NAME="molecular-analysis-api-$(date +%s)"
echo "📱 Creating Heroku app: $APP_NAME"

# Create the app
heroku create $APP_NAME

# Add Heroku remote
echo "🔗 Adding Heroku remote..."
git remote add heroku https://git.heroku.com/$APP_NAME.git

# Set environment variables
echo "⚙️ Setting environment variables..."
heroku config:set --app $APP_NAME \
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY" \
    ELEVENLABS_API_KEY="YOUR_ELEVENLABS_API_KEY" \
    STATSIG_SDK_KEY="YOUR_STATSIG_SDK_KEY" \
    PORT=8000

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git push heroku main

# Open the deployed app
echo "🌐 Opening your deployed app..."
heroku open --app $APP_NAME

echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo "Your API is now live at: https://$APP_NAME.herokuapp.com"
echo "Health check: https://$APP_NAME.herokuapp.com/health"
echo "API docs: https://$APP_NAME.herokuapp.com/docs"
echo "Quantum analysis: https://$APP_NAME.herokuapp.com/api/quantum_simulate"
echo ""
echo "📊 Useful commands:"
echo "  View logs: heroku logs --tail --app $APP_NAME"
echo "  Open app: heroku open --app $APP_NAME"
echo "  Restart: heroku restart --app $APP_NAME"
echo "  Scale: heroku ps:scale web=1 --app $APP_NAME"
echo ""
echo "🔧 To update your app:"
echo "  git add ."
echo "  git commit -m 'Update app'"
echo "  git push heroku main"