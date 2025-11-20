# Demo Script for Chemical Equipment Parameter Visualizer

This script will guide you through a complete demonstration of the project (2-3 minutes).

## Pre-Demo Setup

1. Ensure all services are running:
   - Backend: `http://localhost:8000`
   - Web Frontend: `http://localhost:3000`
   - Desktop App: Launched and ready

2. Have the sample CSV file ready: `sample_data/sample_equipment.csv`

## Demo Flow (2-3 minutes)

### Part 1: Introduction (15 seconds)

> "This is the Chemical Equipment Parameter Visualizer - a hybrid system with Django REST backend, React web frontend, and PyQt5 desktop application. Both frontends consume the same API for data visualization."

### Part 2: Web Application Demo (60 seconds)

1. **Show Login Screen**
   > "Users must authenticate before accessing features. Let me register a new account."

2. **Register User**
   - Click "Register here"
   - Enter: username: `demo_user`, email: `demo@test.com`, password: `demo123`
   - Click "Register"
   > "Registration is successful, now I'll login."

3. **Login**
   - Enter credentials and login
   > "We're now in the main dashboard."

4. **Upload CSV**
   - Click "Browse" and select `sample_equipment.csv`
   - Click "Upload"
   > "The system validates the CSV structure, processes it with Pandas, and generates summary statistics in under 2 seconds."

5. **Show Summary**
   > "Here we can see total equipment count, average flowrate, pressure, and temperature."

6. **Show Visualizations**
   - Scroll to charts
   > "Chart.js provides interactive visualizations - a pie chart for equipment type distribution and a bar chart for average parameters."

7. **Show Data Table**
   - Scroll to table
   > "All equipment data is displayed in a clean table format."

8. **Download Report**
   - Click "Download PDF Report"
   > "The system generates a comprehensive PDF report with all statistics and can be downloaded instantly."

### Part 3: Desktop Application Demo (45 seconds)

1. **Show Desktop Login**
   > "Now let's see the desktop application. I'll login with the same credentials since both frontends use the same API."

2. **Login to Desktop App**
   - Enter credentials and login

3. **Show Dashboard**
   > "The desktop interface provides the same functionality with a native GUI."

4. **Navigate Tabs**
   - Click "Summary" tab
   > "Here's the summary with detailed statistics."
   
   - Click "Data Table" tab
   > "The data table showing all equipment."
   
   - Click "Charts" tab
   > "Matplotlib provides high-quality embedded charts - pie chart for type distribution and bar chart for averages."
   
   - Click "History" tab
   > "The history tab shows the last 5 uploaded datasets."

5. **Upload Another File** (if time permits)
   - Upload the same file again
   > "I can upload another dataset. The system automatically maintains only the last 5 uploads per user."

### Part 4: Features Highlight (30 seconds)

> "Let me highlight the key features implemented:

1. **Authentication**: JWT-based authentication working across both frontends
2. **Data Processing**: Pandas efficiently parses and validates CSV files up to 5MB
3. **Real-time Analysis**: Summary statistics calculated in under 2 seconds
4. **Dual Visualization**: Chart.js for web, Matplotlib for desktop
5. **History Management**: Automatic tracking of last 5 datasets
6. **Report Generation**: PDF reports with ReportLab including tables and statistics
7. **Responsive Design**: Beautiful, modern UI with excellent UX
8. **API-First Architecture**: Stateless REST API suitable for containerization"

### Part 5: Technical Architecture (15 seconds)

> "The architecture consists of:
- **Backend**: Django REST Framework with JWT authentication, Pandas for analysis, SQLite database
- **Web Frontend**: React 18 with Chart.js, Axios for API calls, responsive design
- **Desktop Frontend**: PyQt5 with Matplotlib, same API endpoints
- **All endpoints are documented and functional as per requirements**"

### Closing (5 seconds)

> "All acceptance criteria have been met - authentication, CSV upload with validation, visualizations, history tracking, and PDF reports are all fully functional. The system is ready for deployment."

## Demo Tips

1. **Keep it Flowing**: Practice the transitions between sections
2. **Show, Don't Tell**: Let the application speak for itself
3. **Highlight Key Features**: Focus on what makes it unique
4. **Handle Errors Gracefully**: If something goes wrong, explain the validation
5. **Time Management**: Aim for 2 minutes, maximum 3 minutes

## Backup Talking Points

If you have extra time or get questions:

### Performance
- "CSV files up to 5MB are supported"
- "Summary generation takes less than 2 seconds"
- "The API is stateless and suitable for horizontal scaling"

### Security
- "JWT tokens with 5-hour expiration"
- "Input validation for all CSV uploads"
- "Password hashing with Django's built-in authentication"

### Scalability
- "Stateless API design"
- "Ready for containerization with Docker"
- "Can be deployed to cloud platforms"

### Code Quality
- "Clean separation of concerns"
- "RESTful API design"
- "Reusable components in React"
- "Modular PyQt5 application"

## Quick Recovery

If something doesn't work:

1. **Backend not responding**: Show the API health check endpoint
2. **Upload fails**: Explain validation rules and show error handling
3. **Charts not loading**: Show the data table as alternative
4. **Desktop app crashes**: Switch to web frontend

## Post-Demo

Have ready to show if requested:
- Code structure in IDE
- API documentation
- Requirements files
- README with setup instructions
- Sample CSV file format

---

**Remember**: Confidence and smooth delivery matter more than covering every feature. Focus on demonstrating that all acceptance criteria are met!

