#!/bin/bash

echo "🧬 Setting up Dubhacks-25 Molecular Analysis Platform"
echo "======================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "molviz" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Starting setup process..."

# --- Backend Setup ---
print_status "Setting up Python backend..."
cd backend

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment"
        exit 1
    fi
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "Failed to install Python dependencies"
    exit 1
fi
print_success "Python dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    if [ -f "env.example" ]; then
        cp env.example .env
        print_success ".env file created from template"
        print_warning "Please update .env file with your API keys"
    else
        print_warning "No env.example found, creating basic .env file..."
        cat > .env << EOF
# API Keys - Replace with your actual keys
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY
STATSIG_SDK_KEY=YOUR_STATSIG_SDK_KEY

# Database
DATABASE_URL=sqlite:///./data/analysis.db

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
EOF
        print_success "Basic .env file created"
    fi
else
    print_status ".env file already exists"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data logs models
print_success "Directories created"

deactivate
print_success "Backend setup complete"

# --- Frontend Setup ---
print_status "Setting up React frontend..."
cd ../molviz

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm."
    exit 1
fi

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    print_error "Failed to install Node.js dependencies"
    exit 1
fi
print_success "Node.js dependencies installed"

# Create necessary directories for frontend
mkdir -p public/assets
print_success "Frontend setup complete"

# --- Project Setup ---
cd ..

# Create deployment script
print_status "Creating deployment script..."
cat > deploy.sh << 'EOF'
#!/bin/bash

echo "🚀 Deploying Dubhacks-25 Molecular Analysis Platform"
echo "=================================================="

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate
python start.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
echo "Starting frontend server..."
cd ../molviz
npm start &
FRONTEND_PID=$!

echo "✅ Both servers started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
EOF

chmod +x deploy.sh
print_success "Deployment script created"

# Create development script
print_status "Creating development script..."
cat > dev.sh << 'EOF'
#!/bin/bash

echo "🔬 Starting Development Environment"
echo "================================="

# Check if servers are already running
if lsof -i :8000 > /dev/null 2>&1; then
    echo "Backend server already running on port 8000"
else
    echo "Starting backend server..."
    cd backend
    source venv/bin/activate
    python start.py &
    cd ..
fi

if lsof -i :3000 > /dev/null 2>&1; then
    echo "Frontend server already running on port 3000"
else
    echo "Starting frontend server..."
    cd molviz
    npm start &
    cd ..
fi

echo "✅ Development environment ready!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
EOF

chmod +x dev.sh
print_success "Development script created"

# Create production build script
print_status "Creating production build script..."
cat > build.sh << 'EOF'
#!/bin/bash

echo "🏗️  Building Production Version"
echo "==============================="

# Build frontend
echo "Building React frontend..."
cd molviz
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed"
    exit 1
fi
cd ..

# Create production directory
mkdir -p production
cp -r backend production/
cp -r molviz/build production/frontend

echo "✅ Production build complete!"
echo "Files are in the 'production' directory"
EOF

chmod +x build.sh
print_success "Production build script created"

# --- Final Setup ---
print_status "Setting up project permissions..."
chmod +x setup.sh

# Create a comprehensive README for deployment
print_status "Creating deployment README..."
cat > DEPLOYMENT.md << 'EOF'
# Deployment Guide

## Quick Start

1. **Setup**: Run `./setup.sh` to install all dependencies
2. **Development**: Run `./dev.sh` to start both servers
3. **Production**: Run `./build.sh` to create production build

## Manual Setup

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python start.py
```

### Frontend
```bash
cd molviz
npm install
npm start
```

## Environment Variables

Update `backend/.env` with your API keys:
- GEMINI_API_KEY
- ELEVENLABS_API_KEY
- STATSIG_SDK_KEY

## Ports
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Production Deployment

1. Run `./build.sh` to create production build
2. Deploy the `production/` directory to your server
3. Install Python dependencies on server
4. Run backend with production settings
EOF

print_success "Deployment documentation created"

# --- Summary ---
echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "📁 Project Structure:"
echo "├── backend/          (Python FastAPI server)"
echo "├── molviz/           (React frontend)"
echo "├── setup.sh          (This setup script)"
echo "├── dev.sh            (Development script)"
echo "├── deploy.sh         (Deployment script)"
echo "└── build.sh          (Production build script)"
echo ""
echo "🚀 Quick Start:"
echo "1. Run './dev.sh' to start development servers"
echo "2. Open http://localhost:3000 in your browser"
echo "3. Open http://localhost:8000/docs for API documentation"
echo ""
echo "📝 Next Steps:"
echo "1. Update backend/.env with your API keys"
echo "2. Test the application with sample molecules"
echo "3. Deploy using './build.sh' for production"
echo ""
print_success "All dependencies installed and project ready!"
