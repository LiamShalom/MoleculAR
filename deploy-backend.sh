#!/bin/bash

echo "🚀 Deploying Backend Only with Docker"
echo "====================================="

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
EOF
    print_warning "Please update .env file with your actual API keys"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data logs models

# Stop any existing container
print_status "Stopping existing container..."
docker stop molecular-backend 2>/dev/null || true
docker rm molecular-backend 2>/dev/null || true

# Build the Docker image
print_status "Building Docker image..."
docker build -f Dockerfile.backend -t molecular-backend .

if [ $? -ne 0 ]; then
    print_error "Failed to build Docker image"
    exit 1
fi

# Run the container
print_status "Starting backend container..."
docker run -d \
    --name molecular-backend \
    --env-file .env \
    -p 8000:8000 \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/logs:/app/logs \
    -v $(pwd)/models:/app/models \
    --restart unless-stopped \
    molecular-backend

if [ $? -ne 0 ]; then
    print_error "Failed to start container"
    exit 1
fi

# Wait for service to be ready
print_status "Waiting for service to start..."
sleep 10

# Check if service is running
print_status "Checking service health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_success "Backend is running at http://localhost:8000"
    print_success "API documentation at http://localhost:8000/docs"
else
    print_warning "Backend may not be ready yet. Check logs with: docker logs molecular-backend"
fi

echo ""
echo "🎉 Backend Deployment Complete!"
echo "============================="
echo ""
echo "📱 Service:"
echo "├── Backend API: http://localhost:8000"
echo "└── API Docs: http://localhost:8000/docs"
echo ""
echo "🔧 Management Commands:"
echo "├── View logs: docker logs -f molecular-backend"
echo "├── Stop: docker stop molecular-backend"
echo "├── Start: docker start molecular-backend"
echo "├── Restart: docker restart molecular-backend"
echo "└── Remove: docker rm -f molecular-backend"
echo ""
print_success "Your molecular analysis backend is now running in Docker!"
