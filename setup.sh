#!/bin/bash

#    Financial Health Asses  nt Platform - Setup Script
# This script sets up the development environment for both backend and frontend

echo "========================================="
echo "   FinHealth AI - Setup Script"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 16 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"
echo ""

# Backend Setup
echo "========================================="
echo "Setting up Backend..."
echo "========================================="

cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env and add your configuration${NC}"
    echo -e "${YELLOW}  - OPENAI_API_KEY (optional, will use rule-based fallback)${NC}"
    echo -e "${YELLOW}  - SECRET_KEY (generate with: openssl rand -hex 32)${NC}"
    echo -e "${YELLOW}  - ENCRYPTION_KEY (generate with: openssl rand -hex 16)${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

echo -e "${GREEN}✓ Backend setup complete${NC}"
echo ""

# Frontend Setup
echo "========================================="
echo "Setting up Frontend..."
echo "========================================="

cd ../frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

echo -e "${GREEN}✓ Frontend setup complete${NC}"
echo ""

# Final Instructions
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure environment variables:"
echo "   cd backend"
echo "   nano .env  # or use your preferred editor"
echo ""
echo "2. Start the backend server:"
echo "   cd backend"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   uvicorn main:app --reload"
echo "   # Server will run on http://localhost:8000"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm start"
echo "   # App will run on http://localhost:3000"
echo ""
echo "4. Open your browser and navigate to http://localhost:3000"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
