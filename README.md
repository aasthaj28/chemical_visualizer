# Chemical Equipment Parameter Visualizer

A comprehensive hybrid data visualization system for chemical equipment parameters with Django REST backend, React web frontend, and PyQt5 desktop application.

## 🌟 Features

- **User Authentication**: Secure JWT-based authentication system
- **CSV Upload & Parsing**: Upload and validate chemical equipment data
- **Data Analysis**: Automated summary statistics and parameter analysis using Pandas
- **Interactive Visualizations**: 
  - Web: Chart.js for responsive charts
  - Desktop: Matplotlib for embedded visualizations
- **History Tracking**: Maintains last 5 uploaded datasets per user
- **PDF Report Generation**: Comprehensive reports with statistics and charts
- **Dual Frontend**: Both web and desktop interfaces consuming the same REST API

## 📋 System Requirements

- Python 3.8+
- Node.js 16+
- npm or yarn
- Modern web browser (for web frontend)

## 🏗️ Project Structure

```
chemical_visualizer/
├── backend/                  # Django REST API
│   ├── backend/             # Project settings
│   ├── api/                 # API app
│   ├── manage.py
│   └── requirements.txt
├── web-frontend/            # React web application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── api/           # API utilities
│   │   └── App.js
│   ├── public/
│   └── package.json
├── desktop-frontend/        # PyQt5 desktop application
│   ├── main.py
│   └── requirements.txt
├── sample_data/            # Sample CSV files
│   └── sample_equipment.csv
└── README.md
```

## 🚀 Installation & Setup

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### 2. Web Frontend Setup (React)

```bash
# Navigate to web-frontend directory
cd web-frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The web application will open at `http://localhost:3000`

### 3. Desktop Frontend Setup (PyQt5)

```bash
# Navigate to desktop-frontend directory
cd desktop-frontend

# Create virtual environment (or use the same one as backend)
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the desktop application
python main.py
```

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens

### Data Operations
- `POST /api/upload/` - Upload CSV file (authenticated)
- `GET /api/summary/<dataset_id>/` - Get dataset summary and data (authenticated)
- `GET /api/history/` - Get last 5 uploads (authenticated)
- `GET /api/report/<dataset_id>/` - Download PDF report (authenticated)

### Health Check
- `GET /api/health/` - API health check

## 📊 CSV File Format

Your CSV file must include the following columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-001,Reactor,150.5,25.3,180.2
Pump-001,Pump,200.0,50.0,75.5
...
```

**Required Columns:**
- Equipment Name (string)
- Type (string)
- Flowrate (numeric)
- Pressure (numeric)
- Temperature (numeric)

A sample CSV file is provided in `sample_data/sample_equipment.csv`

## 🎯 Usage Guide

### Web Application

1. **Register/Login**: Create an account or login with existing credentials
2. **Upload CSV**: Click "Browse" to select your CSV file and click "Upload"
3. **View Summary**: See statistics including averages, min/max values
4. **Visualize Data**: Interactive charts show type distribution and parameter averages
5. **View Table**: Browse all equipment data in tabular format
6. **Download Report**: Generate and download PDF reports
7. **History**: Access your last 5 uploads from the history section

### Desktop Application

1. **Login**: Launch the application and login with your credentials
2. **Upload**: Use the "Browse" button to select a CSV file and click "Upload"
3. **Navigate Tabs**:
   - **Summary**: View statistical summary
   - **Data Table**: Browse equipment data
   - **Charts**: View embedded matplotlib visualizations
   - **History**: Access previous uploads
4. **Download Reports**: Click "Download PDF Report" to save reports locally

## 🛠️ Development

### Backend Development

```bash
# Run tests (if implemented)
python manage.py test

# Create new migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Access Django admin
# Navigate to http://localhost:8000/admin
```

### Web Frontend Development

```bash
# Build for production
npm run build

# Run tests
npm test
```

### Desktop Frontend Development

The desktop app is a single Python file (`main.py`) that can be modified directly. For building standalone executables:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed main.py
```

## 🔒 Security Notes

- The current `SECRET_KEY` in Django settings is for development only
- Change it for production deployment
- JWT tokens expire after 5 hours
- CORS is currently set to allow all origins for development
- Restrict CORS origins in production

## 📦 Deployment

### Backend (Django)

1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production-grade database (PostgreSQL recommended)
4. Set a strong `SECRET_KEY`
5. Configure CORS to allow only your frontend domain
6. Use gunicorn or uwsgi as WSGI server
7. Set up nginx as reverse proxy

### Web Frontend (React)

1. Update `API_BASE_URL` in `src/api/axios.js` to your backend URL
2. Build the production bundle: `npm run build`
3. Deploy to hosting service (Netlify, Vercel, AWS S3, etc.)

### Desktop Application

- Distribute the Python script with installation instructions
- Or create standalone executables using PyInstaller

## 🧪 Testing

### Sample Test Workflow

1. Start the backend server
2. Register a new user via web or desktop app
3. Upload the sample CSV file from `sample_data/sample_equipment.csv`
4. Verify summary statistics are calculated correctly
5. Check visualizations are rendered properly
6. Download and verify PDF report
7. Upload 5+ files and verify only last 5 are retained in history

## 📄 Acceptance Criteria Checklist

- ✅ All API endpoints functional and tested
- ✅ Web frontend fully connected to backend
- ✅ Desktop app fully connected to backend
- ✅ CSV upload with validation working
- ✅ Summary statistics generation working
- ✅ Charts and visualizations working
- ✅ History tracking (last 5 datasets)
- ✅ JWT authentication functional
- ✅ PDF report generation and download working
- ✅ Responsive design for web interface
- ✅ Error handling and user feedback

## 🤝 Support

For issues or questions:
1. Check the console logs for detailed error messages
2. Verify all dependencies are installed correctly
3. Ensure the backend server is running before starting frontends
4. Check API connectivity from frontend applications

## 📜 License

This project is created for educational/screening test purposes.

## 👨‍💻 Author

Created as part of a screening test project demonstrating full-stack development skills with Django, React, and PyQt5.

---

**Note**: This is a development setup. For production deployment, additional security measures, proper error handling, and performance optimizations should be implemented.

