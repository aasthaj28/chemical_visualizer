# Quick Setup Guide

This guide will help you get the Chemical Equipment Parameter Visualizer up and running in minutes.

## Prerequisites

Make sure you have installed:
- Python 3.8 or higher
- Node.js 16 or higher
- npm (comes with Node.js)

## Quick Start

### Option 1: Automated Setup (Recommended)

#### On macOS/Linux:

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup script
./setup.sh
```

#### On Windows:

```cmd
# Run setup script
setup.bat
```

### Option 2: Manual Setup

Follow these steps in order:

#### Step 1: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server (keep this terminal open)
python manage.py runserver
```

Backend will run at: http://localhost:8000

#### Step 2: Setup Web Frontend (New Terminal)

```bash
# Navigate to web-frontend directory
cd web-frontend

# Install dependencies
npm install

# Start the development server (keep this terminal open)
npm start
```

Web app will open at: http://localhost:3000

#### Step 3: Setup Desktop App (New Terminal)

```bash
# Navigate to desktop-frontend directory
cd desktop-frontend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## First Time Usage

1. **Register an Account**
   - Open the web app at http://localhost:3000
   - Click "Register here"
   - Fill in username, email, and password
   - Click "Register"

2. **Login**
   - Use your credentials to login
   - You'll be redirected to the dashboard

3. **Upload Sample Data**
   - Click "Browse" and select `sample_data/sample_equipment.csv`
   - Click "Upload"
   - View the summary, charts, and data table

4. **Try Desktop App**
   - Run the desktop application
   - Login with the same credentials
   - Upload data and explore visualizations

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem**: Database errors
```bash
# Delete database and recreate
rm db.sqlite3
python manage.py migrate
```

### Web Frontend Issues

**Problem**: `npm install` fails
```bash
# Clear npm cache
npm cache clean --force

# Try again
npm install
```

**Problem**: CORS errors
- Make sure backend is running on port 8000
- Check that API_BASE_URL in `src/api/axios.js` is correct

### Desktop App Issues

**Problem**: PyQt5 installation fails
```bash
# On macOS with Apple Silicon
pip install PyQt5 --no-binary PyQt5

# On Linux, you might need system packages
sudo apt-get install python3-pyqt5
```

**Problem**: Connection refused
- Make sure the backend server is running
- Check API_BASE_URL in main.py (should be http://localhost:8000/api)

## Common Ports

- Backend API: http://localhost:8000
- Web Frontend: http://localhost:3000
- Django Admin: http://localhost:8000/admin

## Sample Data

Use the provided sample CSV file located at:
```
sample_data/sample_equipment.csv
```

This file contains 20 chemical equipment records with proper formatting.

## API Testing

You can test the API using curl or Postman:

### Health Check
```bash
curl http://localhost:8000/api/health/
```

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@test.com","password":"testpass123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

## Next Steps

1. Create more CSV files with your own equipment data
2. Explore the visualization features
3. Download PDF reports
4. Check the upload history

## Need Help?

- Check the main README.md for detailed documentation
- Review error messages in the console
- Ensure all dependencies are installed
- Verify that all required ports are available

---

Happy Visualizing! 🚀

