#!/usr/bin/env python3
"""
Startup script for Mailmind application
This script starts the Flask backend and provides instructions for the React frontend
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import flask
        import firebase_admin
        print("✅ Python dependencies found")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    # Check if node_modules exists
    if not Path("node_modules").exists():
        print("❌ Node.js dependencies not found")
        print("Please run: npm install")
        return False
    
    print("✅ Node.js dependencies found")
    return True

def start_flask_backend():
    """Start the Flask backend server"""
    print("\n🚀 Starting Flask backend...")
    print("Backend will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the backend")
    
    try:
        # Start Flask app
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting backend: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("=" * 50)
    print("🎯 Mailmind - AI Email Processing System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again")
        return
    
    print("\n📋 Setup Instructions:")
    print("1. Make sure you have configured Firebase credentials")
    print("2. Set up Google API credentials for email/calendar access")
    print("3. Configure environment variables in config.py")
    
    print("\n🌐 To run the complete application:")
    print("1. This script will start the Flask backend")
    print("2. In a separate terminal, run: npm start")
    print("3. Frontend will be available at: http://localhost:3000")
    
    # Ask user if they want to start the backend
    response = input("\n🤔 Do you want to start the Flask backend now? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        start_flask_backend()
    else:
        print("\n📝 Manual startup instructions:")
        print("1. Start Flask backend: python app.py")
        print("2. Start React frontend: npm start")
        print("3. Open http://localhost:3000 in your browser")

if __name__ == "__main__":
    main()
