#!/bin/bash

# MolViz AI Deployment Script
echo "🧬 MolViz AI Deployment Script"
echo "=============================="

# Check if we're in the right directory
if [ ! -f "molviz/package.json" ] || [ ! -f "backend/main.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists node; then
    echo "❌ Node.js not found. Please install Node.js 16+"
    exit 1
fi

if ! command_exists python3; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd molviz
if [ ! -d "node_modules" ]; then
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Frontend dependency installation failed"
        exit 1
    fi
fi
echo "✅ Frontend dependencies installed"

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd ../backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Backend dependency installation failed"
    exit 1
fi
echo "✅ Backend dependencies installed"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data temp models logs
echo "✅ Directories created"

# Setup environment file
echo "⚙️ Setting up environment..."
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env file from template"
        echo "⚠️  Please update .env with your API keys"
    else
        echo "⚠️  No env.example found, creating basic .env"
        cat > .env << EOF
GEMINI_API_KEY=your-gemini-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
STATSIG_SDK_KEY=your-statsig-sdk-key
DATABASE_TYPE=file
DEBUG=True
EOF
    fi
fi

echo ""
echo "🚀 Setup complete! To start the application:"
echo ""
echo "Frontend (Terminal 1):"
echo "  cd molviz && npm start"
echo ""
echo "Backend (Terminal 2):"
echo "  cd backend && source venv/bin/activate && python start.py"
echo ""
echo "🌐 Frontend will be available at: http://localhost:3000"
echo "🔧 Backend API will be available at: http://localhost:8000"
echo "📚 API documentation at: http://localhost:8000/docs"
echo ""
echo "🧪 Try these example molecules:"
echo "  • Imatinib (Cancer): CC1=CC=C(C=C1)NC(=O)C2=CC(=CC=C2)C3=CN=CC=N3"
echo "  • Metformin (Diabetes): CN(C)C(=N)N=C(N)N"
echo "  • Donepezil (Alzheimer's): CN1CCN(CC1)C2=CC=CC=C2C3=CC=CC=C3"
echo ""
echo "Happy molecular analysis! 🧬✨"
