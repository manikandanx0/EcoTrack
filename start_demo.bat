@echo off
echo 🌍 EcoTrack - Hybrid Carbon Footprint Tracker
echo ================================================

echo.
echo 📦 Installing dependencies...

echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)

echo Installing frontend dependencies...
cd ..\frontend
npm install
if errorlevel 1 (
    echo ❌ Failed to install frontend dependencies
    echo 💡 Make sure Node.js and npm are installed
    pause
    exit /b 1
)

echo.
echo 🚀 Starting servers...

echo Starting backend server...
cd ..\backend
start "EcoTrack Backend" cmd /k "uvicorn main:app --reload --port 8000"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting frontend server...
cd ..\frontend
start "EcoTrack Frontend" cmd /k "npm run dev"

echo Waiting for frontend to start...
timeout /t 8 /nobreak > nul

echo.
echo 🎉 Demo is ready!
echo 📱 Frontend: http://localhost:5173
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs

echo.
echo 🌐 Opening browser...
start http://localhost:5173

echo.
echo 💡 Close the command windows to stop the servers
pause
