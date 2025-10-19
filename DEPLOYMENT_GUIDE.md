# 🚀 Deploy Your Molecular Analysis Backend

This guide will help you deploy your backend so others can use it from anywhere on the internet.

## Quick Deploy Options

### Option 1: Automated Deployment (Recommended)
```bash
./deploy-cloud.sh
```
This script will guide you through deploying to various cloud platforms.

### Option 2: Manual Deployment

## 🌐 Cloud Platform Options

### 1. **Heroku** (Free tier available)
- **Pros**: Easy setup, free tier, automatic deployments
- **Cons**: Sleeps after 30 minutes of inactivity
- **Best for**: Testing and small projects

**Steps:**
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Run: `./deploy-cloud.sh` and choose option 1
3. Or manually:
   ```bash
   heroku create your-app-name
   heroku config:set GEMINI_API_KEY=your-key
   heroku config:set ELEVENLABS_API_KEY=your-key
   heroku config:set STATSIG_SDK_KEY=your-key
   git push heroku main
   ```

### 2. **Railway** (Free tier available)
- **Pros**: Modern platform, good free tier, easy setup
- **Cons**: Limited free tier resources
- **Best for**: Modern applications

**Steps:**
1. Install Railway CLI: `npm install -g @railway/cli`
2. Run: `./deploy-cloud.sh` and choose option 2
3. Or visit: https://railway.app

### 3. **Render** (Free tier available)
- **Pros**: Good free tier, automatic deployments
- **Cons**: Cold starts can be slow
- **Best for**: Reliable hosting

**Steps:**
1. Go to https://render.com
2. Create new Web Service
3. Connect your GitHub repo
4. Use these settings:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python start.py`
   - **Environment**: Python 3

### 4. **DigitalOcean App Platform**
- **Pros**: Reliable, good performance
- **Cons**: No free tier
- **Best for**: Production applications

### 5. **Fly.io** (Free tier available)
- **Pros**: Global deployment, good performance
- **Cons**: More complex setup
- **Best for**: Global applications

## 🔧 Environment Variables

Set these in your cloud platform:

```bash
GEMINI_API_KEY=your-gemini-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
STATSIG_SDK_KEY=your-statsig-sdk-key
HOST=0.0.0.0
PORT=8000
```

## 📱 Testing Your Deployment

Once deployed, test your API:

```bash
# Health check
curl https://your-app-url/health

# API documentation
open https://your-app-url/docs

# Test quantum analysis
curl -X POST https://your-app-url/api/quantum_simulate \
  -H "Content-Type: application/json" \
  -d '{"molecular_data": "CCO", "analysis_type": "quantum"}'
```

## 🚀 Quick Start

1. **Choose a platform** (Heroku is easiest for beginners)
2. **Run the deployment script**: `./deploy-cloud.sh`
3. **Follow the prompts**
4. **Update your API keys** in the platform dashboard
5. **Test your API** with the health check endpoint
6. **Share your URL** with others!

## 📊 Monitoring Your Deployment

- **Health Check**: `https://your-app-url/health`
- **API Docs**: `https://your-app-url/docs`
- **Logs**: Check your platform's dashboard for logs

## 🔄 Updating Your Deployment

Most platforms support automatic deployments:
- **Heroku**: `git push heroku main`
- **Railway**: `railway up`
- **Render**: Automatic on git push
- **Fly.io**: `fly deploy`

## 🆘 Troubleshooting

### Common Issues:

1. **"Address already in use"**
   - Make sure no local servers are running
   - Check if port 8000 is free

2. **"Module not found"**
   - Ensure all dependencies are in requirements.txt
   - Check if virtual environment is activated

3. **"API key not working"**
   - Verify environment variables are set correctly
   - Check if API keys are valid

4. **"Health check failing"**
   - Wait a few minutes for deployment to complete
   - Check logs for errors

## 📞 Support

If you need help:
1. Check the platform's documentation
2. Look at the deployment logs
3. Test locally first: `cd backend && python start.py`
4. Verify all environment variables are set

## 🎉 Success!

Once deployed, your molecular analysis API will be available to anyone on the internet at:
- **Your API URL**: `https://your-app-url`
- **Health Check**: `https://your-app-url/health`
- **API Documentation**: `https://your-app-url/docs`

Share this URL with others so they can use your molecular analysis platform!
