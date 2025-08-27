#!/usr/bin/env python3
"""
Jewelry Recommender - Startup Script
Run this script to start the jewelry recommendation application
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def check_requirements():
    """Check if required files exist"""
    required_files = ['main.py', 'requirements.txt', 'static/index.html']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all files are in the correct location.")
        return False
    
    print("✅ All required files found")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_static_directory():
    """Create static directory if it doesn't exist"""
    static_dir = Path('static')
    if not static_dir.exists():
        static_dir.mkdir()
        print("✅ Created static directory")

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Jewelry Recommender server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("\n🔄 Press Ctrl+C to stop the server\n")
    
    # Open browser after a short delay
    import threading
    import time
    
    def open_browser():
        time.sleep(2)  # Wait for server to start
        webbrowser.open('http://localhost:8000')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'main:app', 
            '--reload', 
            '--host', '0.0.0.0', 
            '--port', '8000'
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thank you for using Jewelry Recommender!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("💎 Jewelry Recommender - AI-Powered Custom Design Assistant")
    print("=" * 60)
    
    # Check if running in correct directory
    if not Path('main.py').exists():
        print("❌ Please run this script from the project root directory")
        print("   The directory should contain main.py, requirements.txt, etc.")
        return
    
    # Check requirements
    if not check_requirements():
        return
    
    # Create static directory
    create_static_directory()
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()