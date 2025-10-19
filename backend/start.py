#!/usr/bin/env python3
"""
Startup script for the Molecular Analysis API
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import rdkit
        logger.info("✓ Core dependencies found")
        return True
    except ImportError as e:
        logger.error(f"Missing dependencies: {e}")
        logger.info("Please install requirements: pip install -r requirements.txt")
        return False

def setup_environment():
    """Setup environment variables"""
    env_file = Path(".env")
    if not env_file.exists():
        logger.info("Creating .env file from template...")
        if Path("env.example").exists():
            with open("env.example", "r") as f:
                content = f.read()
            with open(".env", "w") as f:
                f.write(content)
            logger.info("✓ Created .env file - please update with your API keys")
        else:
            logger.warning("No env.example file found")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check for required API keys
    required_keys = ["GEMINI_API_KEY", "ELEVENLABS_API_KEY", "STATSIG_SDK_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key) or os.getenv(key) == f"your-{key.lower().replace('_', '-')}"]
    
    if missing_keys:
        logger.warning(f"Missing or default API keys: {', '.join(missing_keys)}")
        logger.info("The application will run with mock data for missing services")
    else:
        logger.info("✓ All API keys configured")

def create_directories():
    """Create necessary directories"""
    directories = ["data", "temp", "models", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    logger.info("✓ Created necessary directories")

def start_server():
    """Start the FastAPI server"""
    try:
        import uvicorn
        from main import app
        
        logger.info("Starting Molecular Analysis API server...")
        logger.info("Server will be available at: http://localhost:8000")
        logger.info("API documentation at: http://localhost:8000/docs")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    logger.info("🧬 Molecular Analysis API Startup")
    logger.info("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Create directories
    create_directories()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
