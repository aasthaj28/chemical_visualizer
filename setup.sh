#!/bin/bash

echo "========================================="
echo "Chemical Equipment Visualizer Setup"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python and Node.js are installed${NC}"
echo ""

# Setup Backend
echo -e "${YELLOW}Setting up Backend...${NC}"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Run migrations
python manage.py makemigrations
python manage.py migrate
echo -e "${GREEN}✓ Database migrations completed${NC}"

# Deactivate virtual environment
deactivate

cd ..
echo ""

# Setup Web Frontend
echo -e "${YELLOW}Setting up Web Frontend...${NC}"
cd web-frontend

# Install dependencies
npm install
echo -e "${GREEN}✓ Web frontend dependencies installed${NC}"

cd ..
echo ""

# Setup Desktop Frontend
echo -e "${YELLOW}Setting up Desktop Frontend...${NC}"
cd desktop-frontend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
echo -e "${GREEN}✓ Desktop frontend dependencies installed${NC}"

# Deactivate virtual environment
deactivate

cd ..
echo ""

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "To start the application:"
echo ""
echo "1. Start Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "2. Start Web Frontend (Terminal 2):"
echo "   cd web-frontend"
echo "   npm start"
echo ""
echo "3. Start Desktop App (Terminal 3):"
echo "   cd desktop-frontend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "Sample data is available in: sample_data/sample_equipment.csv"
echo ""

