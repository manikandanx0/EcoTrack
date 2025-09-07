#!/usr/bin/env python3
"""
Quick start script for EcoTrack Demo
This script helps you start both backend and frontend for the demo
"""

import subprocess
import sys
import time
import os
import webbrowser
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_backend_deps():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install backend dependencies: {e}")
        return False

def install_frontend_deps():
    """Install frontend dependencies"""
    print("\n📦 Installing frontend dependencies...")
    try:
        subprocess.run(["npm", "install"], cwd="frontend", check=True, capture_output=True)
        print("✅ Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install frontend dependencies: {e}")
        print("💡 Make sure Node.js and npm are installed")
        return False

def start_backend():
    """Start the FastAPI backend"""
    print("\n🚀 Starting backend server...")
    try:
        # Start backend in background
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"
        ], cwd="backend")
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test if server is running
        import requests
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server started successfully on http://localhost:8000")
                return backend_process
        except:
            pass
        
        print("⚠️  Backend server started but health check failed")
        return backend_process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the React frontend"""
    print("\n🚀 Starting frontend server...")
    try:
        # Start frontend in background
        frontend_process = subprocess.Popen([
            "npm", "run", "dev"
        ], cwd="frontend")
        
        # Wait a moment for server to start
        time.sleep(5)
        print("✅ Frontend server started on http://localhost:5173")
        return frontend_process
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def run_demo():
    """Run the demo script"""
    print("\n🎬 Running demo...")
    try:
        subprocess.run([sys.executable, "demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Demo failed: {e}")

def main():
    """Main function"""
    print("🌍 EcoTrack - Hybrid Carbon Footprint Tracker")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the EcoTrack root directory")
        return
    
    # Install dependencies
    if not install_backend_deps():
        return
    
    if not install_frontend_deps():
        return
    
    # Start servers
    backend_process = start_backend()
    if not backend_process:
        return
    
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    # Run demo
    run_demo()
    
    # Open browser
    print("\n🌐 Opening browser...")
    time.sleep(2)
    webbrowser.open("http://localhost:5173")
    
    print("\n🎉 Demo is ready!")
    print("📱 Frontend: http://localhost:5173")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n💡 Press Ctrl+C to stop the servers")
    
    try:
        # Keep running until user stops
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Servers stopped")

if __name__ == "__main__":
    main()
