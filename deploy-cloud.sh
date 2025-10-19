#!/bin/bash

echo "☁️  Deploying Molecular Analysis Backend to Cloud"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "Choose your deployment platform:"
echo "1) Heroku (Free tier available)"
echo "2) Railway (Free tier available)"
echo "3) DigitalOcean App Platform"
echo "4) Render (Free tier available)"
echo "5) Fly.io (Free tier available)"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        print_status "Setting up Heroku deployment..."
        
        # Check if Heroku CLI is installed
        if ! command -v heroku &> /dev/null; then
            print_error "Heroku CLI is not installed. Please install it first:"
            echo "https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        # Login to Heroku
        heroku login
        
        # Create Heroku app
        read -p "Enter your app name (or press Enter for auto-generated): " app_name
        if [ -z "$app_name" ]; then
            heroku create
        else
            heroku create $app_name
        fi
        
        # Set environment variables
        print_status "Setting environment variables..."
        heroku config:set GEMINI_API_KEY=your-gemini-api-key
        heroku config:set ELEVENLABS_API_KEY=your-elevenlabs-api-key
        heroku config:set STATSIG_SDK_KEY=your-statsig-sdk-key
        heroku config:set HOST=0.0.0.0
        heroku config:set PORT=8000
        
        # Deploy
        print_status "Deploying to Heroku..."
        git add .
        git commit -m "Deploy to Heroku"
        git push heroku main
        
        print_success "Deployed to Heroku! Your app is available at:"
        heroku apps:info --json | grep '"web_url"' | cut -d'"' -f4
        ;;
        
    2)
        print_status "Setting up Railway deployment..."
        
        # Check if Railway CLI is installed
        if ! command -v railway &> /dev/null; then
            print_error "Railway CLI is not installed. Please install it first:"
            echo "npm install -g @railway/cli"
            exit 1
        fi
        
        # Login to Railway
        railway login
        
        # Create Railway project
        railway init
        
        # Set environment variables
        print_status "Setting environment variables..."
        railway variables set GEMINI_API_KEY=your-gemini-api-key
        railway variables set ELEVENLABS_API_KEY=your-elevenlabs-api-key
        railway variables set STATSIG_SDK_KEY=your-statsig-sdk-key
        railway variables set HOST=0.0.0.0
        railway variables set PORT=8000
        
        # Deploy
        print_status "Deploying to Railway..."
        railway up
        
        print_success "Deployed to Railway! Check your dashboard for the URL."
        ;;
        
    3)
        print_status "Setting up DigitalOcean App Platform deployment..."
        print_warning "You'll need to create a DigitalOcean account and set up the app manually."
        echo ""
        echo "Steps:"
        echo "1. Go to https://cloud.digitalocean.com/apps"
        echo "2. Create a new app"
        echo "3. Connect your GitHub repository"
        echo "4. Use the Dockerfile.production file"
        echo "5. Set environment variables:"
        echo "   - GEMINI_API_KEY=your-gemini-api-key"
        echo "   - ELEVENLABS_API_KEY=your-elevenlabs-api-key"
        echo "   - STATSIG_SDK_KEY=your-statsig-sdk-key"
        echo "   - HOST=0.0.0.0"
        echo "   - PORT=8000"
        ;;
        
    4)
        print_status "Setting up Render deployment..."
        print_warning "You'll need to create a Render account and set up the service manually."
        echo ""
        echo "Steps:"
        echo "1. Go to https://render.com"
        echo "2. Create a new Web Service"
        echo "3. Connect your GitHub repository"
        echo "4. Use these settings:"
        echo "   - Build Command: pip install -r backend/requirements.txt"
        echo "   - Start Command: cd backend && python start.py"
        echo "   - Environment: Python 3"
        echo "5. Set environment variables:"
        echo "   - GEMINI_API_KEY=your-gemini-api-key"
        echo "   - ELEVENLABS_API_KEY=your-elevenlabs-api-key"
        echo "   - STATSIG_SDK_KEY=your-statsig-sdk-key"
        echo "   - HOST=0.0.0.0"
        echo "   - PORT=8000"
        ;;
        
    5)
        print_status "Setting up Fly.io deployment..."
        
        # Check if Fly CLI is installed
        if ! command -v fly &> /dev/null; then
            print_error "Fly CLI is not installed. Please install it first:"
            echo "https://fly.io/docs/hands-on/install-flyctl/"
            exit 1
        fi
        
        # Create fly.toml
        cat > fly.toml << EOF
app = "molecular-analysis"
primary_region = "sjc"

[build]

[env]
  HOST = "0.0.0.0"
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
EOF
        
        # Login to Fly
        fly auth login
        
        # Deploy
        print_status "Deploying to Fly.io..."
        fly deploy
        
        print_success "Deployed to Fly.io! Your app is available at:"
        fly info --json | grep '"hostname"' | cut -d'"' -f4
        ;;
        
    *)
        print_error "Invalid choice. Please run the script again and choose 1-5."
        exit 1
        ;;
esac

echo ""
print_success "Deployment setup complete!"
echo ""
echo "📝 Next Steps:"
echo "1. Update your environment variables with real API keys"
echo "2. Test your deployed API"
echo "3. Share the URL with others!"
echo ""
echo "🔗 Your API will be available at:"
echo "   - Health check: https://your-app-url/health"
echo "   - API docs: https://your-app-url/docs"
echo "   - Quantum analysis: https://your-app-url/api/quantum_simulate"
