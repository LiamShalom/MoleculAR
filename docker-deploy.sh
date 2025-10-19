#!/bin/bash

echo "🐳 Deploying Dubhacks-25 Molecular Analysis Platform with Docker"
echo "================================================================="

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

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    cat > .env << EOF
# API Keys - Replace with your actual keys
GEMINI_API_KEY=your-gemini-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
STATSIG_SDK_KEY=your-statsig-sdk-key

# Database
DATABASE_URL=sqlite:///./data/analysis.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Frontend
REACT_APP_API_URL=http://localhost:8000
EOF
    print_warning "Please update .env file with your actual API keys"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data logs models

# Stop any existing containers
print_status "Stopping existing containers..."
docker-compose down

# Build and start services
print_status "Building Docker images..."
docker-compose build

if [ $? -ne 0 ]; then
    print_error "Failed to build Docker images"
    exit 1
fi

print_status "Starting services..."
docker-compose up -d

if [ $? -ne 0 ]; then
    print_error "Failed to start services"
    exit 1
fi

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 10

# Check if services are running
print_status "Checking service health..."

# Check backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_success "Backend is running at http://localhost:8000"
else
    print_warning "Backend may not be ready yet. Check logs with: docker-compose logs backend"
fi

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_success "Frontend is running at http://localhost:3000"
else
    print_warning "Frontend may not be ready yet. Check logs with: docker-compose logs frontend"
fi

echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo ""
echo "📱 Services:"
echo "├── Backend API: http://localhost:8000"
echo "├── Frontend: http://localhost:3000"
echo "├── API Docs: http://localhost:8000/docs"
echo "└── Nginx Proxy: http://localhost:80"
echo ""
echo "🔧 Management Commands:"
echo "├── View logs: docker-compose logs -f"
echo "├── Stop services: docker-compose down"
echo "├── Restart: docker-compose restart"
echo "└── Update: docker-compose pull && docker-compose up -d"
echo ""
print_success "Your molecular analysis platform is now running in Docker!"
