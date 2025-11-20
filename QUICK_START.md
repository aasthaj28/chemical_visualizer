# Quick Start Commands

Copy and paste these commands to get started immediately!

## 🚀 Option 1: Automated Setup (Easiest)

### On macOS/Linux:
```bash
cd /Users/aasthajoshi/Downloads/chemical_visualizer
./setup.sh
```

### On Windows:
```cmd
cd C:\path\to\chemical_visualizer
setup.bat
```

## 🛠️ Option 2: Manual Setup

### Step 1: Setup Backend (Terminal 1)
```bash
cd /Users/aasthajoshi/Downloads/chemical_visualizer/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
✅ Backend running at: http://localhost:8000

### Step 2: Setup Web Frontend (Terminal 2)
```bash
cd /Users/aasthajoshi/Downloads/chemical_visualizer/web-frontend
npm install
npm start
```
✅ Web app opening at: http://localhost:3000

### Step 3: Setup Desktop App (Terminal 3)
```bash
cd /Users/aasthajoshi/Downloads/chemical_visualizer/desktop-frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
✅ Desktop app window will open

## 📝 First Steps After Setup

1. **Register a new account** (web or desktop)
   - Username: `demo_user`
   - Email: `demo@test.com`
   - Password: `demo123`

2. **Upload sample data**
   - File location: `/Users/aasthajoshi/Downloads/chemical_visualizer/sample_data/sample_equipment.csv`

3. **Explore features**
   - View summary statistics
   - Check visualizations
   - Download PDF report
   - Browse upload history

## 🧪 Quick Test Commands

### Test API Health:
```bash
curl http://localhost:8000/api/health/
```

### Test Registration:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@test.com","password":"testpass123"}'
```

### Test Login:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

## 📚 Documentation Files

- **README.md** - Complete project documentation
- **SETUP_GUIDE.md** - Detailed setup instructions  
- **API_DOCUMENTATION.md** - API reference
- **DEMO_SCRIPT.md** - Demo presentation guide
- **PROJECT_SUMMARY.md** - Project overview

## ⚡ Troubleshooting One-Liners

### Reset Backend Database:
```bash
cd backend
rm db.sqlite3
python manage.py migrate
```

### Clear Web Frontend Cache:
```bash
cd web-frontend
rm -rf node_modules package-lock.json
npm install
```

### Reinstall Desktop Dependencies:
```bash
cd desktop-frontend
pip install --force-reinstall -r requirements.txt
```

## 🎯 What to Demo

1. **Authentication** - Register/Login on both web and desktop
2. **CSV Upload** - Upload sample_equipment.csv
3. **Visualizations** - Show charts on both platforms
4. **PDF Report** - Generate and download report
5. **History** - Upload multiple files, show last 5 tracking

## 💡 Pro Tips

- Keep all three terminals open while developing
- Backend must be running for frontends to work
- Use Chrome/Firefox DevTools for web debugging
- Check terminal logs for detailed error messages
- Sample CSV has 20 records across 5 equipment types

---

**Need Help?** Check SETUP_GUIDE.md for detailed troubleshooting!

