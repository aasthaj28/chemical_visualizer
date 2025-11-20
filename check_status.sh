#!/bin/bash

echo "========================================"
echo "Chemical Equipment Visualizer - Status"
echo "========================================"
echo ""

# Check Backend (Django)
echo "🔧 Backend (Django REST API):"
if curl -s http://localhost:8000/api/health/ | grep -q "status"; then
    echo "   ✅ Running at http://localhost:8000"
    echo "   ✅ API: http://localhost:8000/api/"
else
    echo "   ⚠️  Not responding or port conflict detected"
    echo "   💡 Try: cd backend && source venv/bin/activate && python manage.py runserver"
fi
echo ""

# Check Web Frontend (React)
echo "🌐 Web Frontend (React):"
if curl -s http://localhost:3000 | grep -q "root"; then
    echo "   ✅ Running at http://localhost:3000"
    echo "   💻 Open in browser: http://localhost:3000"
else
    echo "   ⚠️  Not responding"
    echo "   💡 Try: cd web-frontend && npm start"
fi
echo ""

# Desktop App Info
echo "🖥️  Desktop App (PyQt5):"
echo "   To run desktop app:"
echo "   cd desktop-frontend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""

echo "========================================"
echo "Quick Test:"
echo "========================================"
echo "Test API: curl http://localhost:8000/api/health/"
echo "Open Web: open http://localhost:3000"
echo ""

