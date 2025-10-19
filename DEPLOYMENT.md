# 🧬 Dubhacks-25 Molecular Analysis Platform - Deployment Guide

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone <your-repo-url>
cd dubhacks-25

# Run the setup script
./setup.sh

# Start development servers
./dev.sh
```

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python start.py
```

#### Frontend Setup
```bash
cd molviz
npm install
npm start
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f
```

### Using Docker directly
```bash
# Build the image
docker build -t molecular-analysis .

# Run the container
docker run -p 8000:8000 molecular-analysis
```

## 🌐 Production Deployment

### 1. Environment Setup
```bash
# Update environment variables
cp backend/env.example backend/.env
# Edit backend/.env with your API keys
```

### 2. Build Production Version
```bash
# Create production build
./build.sh

# The production files will be in the 'production' directory
```

### 3. Deploy to Server
```bash
# Copy production files to your server
scp -r production/ user@your-server:/path/to/deployment/

# On your server, install Python dependencies
cd /path/to/deployment/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the server
python start.py
```

## 🔧 Configuration

### Environment Variables
Create `backend/.env` with the following variables:

```env
# API Keys (Required for full functionality)
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
STATSIG_SDK_KEY=your_statsig_sdk_key

# Database
DATABASE_URL=sqlite:///./data/analysis.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

### API Keys Setup
1. **Gemini API**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **ElevenLabs API**: Get from [ElevenLabs](https://elevenlabs.io/app/settings/api-keys)
3. **Statsig SDK**: Get from [Statsig](https://console.statsig.com/)

## 📊 Monitoring & Health Checks

### Health Endpoints
- Backend Health: `http://localhost:8000/health`
- API Documentation: `http://localhost:8000/docs`

### Logs
- Backend logs: `backend/logs/`
- Application logs: `logs/`

## 🛠️ Development

### Available Scripts
```bash
# Setup everything
./setup.sh

# Start development servers
./dev.sh

# Build for production
./build.sh

# Deploy with Docker
docker-compose up --build
```

### Project Structure
```
dubhacks-25/
├── backend/                 # Python FastAPI backend
│   ├── services/           # Business logic services
│   ├── main.py            # FastAPI application
│   ├── start.py           # Server startup script
│   └── requirements.txt   # Python dependencies
├── molviz/                 # React frontend
│   ├── src/               # React source code
│   ├── public/            # Static assets
│   └── package.json       # Node.js dependencies
├── setup.sh               # Automated setup script
├── dev.sh                 # Development script
├── deploy.sh              # Deployment script
├── build.sh               # Production build script
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
└── DEPLOYMENT.md          # This file
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill processes using ports 3000 and 8000
   lsof -ti:3000 | xargs kill -9
   lsof -ti:8000 | xargs kill -9
   ```

2. **Python Dependencies Issues**
   ```bash
   cd backend
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Node.js Dependencies Issues**
   ```bash
   cd molviz
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Docker Build Issues**
   ```bash
   docker system prune -a
   docker-compose build --no-cache
   ```

### Performance Optimization

1. **Backend Optimization**
   - Use production WSGI server (Gunicorn)
   - Enable caching
   - Use connection pooling

2. **Frontend Optimization**
   - Enable code splitting
   - Use CDN for static assets
   - Implement service workers

## 📈 Scaling

### Horizontal Scaling
- Use load balancer (nginx)
- Multiple backend instances
- Database clustering

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Use caching layers

## 🔒 Security

### Production Security Checklist
- [ ] Update all API keys
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Use environment variables for secrets
- [ ] Regular security updates

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Check the API documentation at `/docs`
4. Create an issue in the repository

## 🎯 Next Steps

1. **Customize the UI**: Modify React components in `molviz/src/`
2. **Add New Features**: Extend backend services in `backend/services/`
3. **Deploy to Cloud**: Use AWS, GCP, or Azure
4. **Add Monitoring**: Integrate with monitoring services
5. **Scale**: Implement load balancing and caching
