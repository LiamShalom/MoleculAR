# Multi-stage Docker build for Dubhacks-25 Molecular Analysis Platform

# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/molviz
COPY molviz/package*.json ./
RUN npm ci --only=production
COPY molviz/ ./
RUN npm run build

# Stage 2: Python Backend
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy built frontend
COPY --from=frontend-builder /app/molviz/build ./static

# Create necessary directories
RUN mkdir -p data logs models

# Create .env file
RUN echo "HOST=0.0.0.0\nPORT=8000\nDEBUG=False" > .env

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["python", "start.py"]
