#!/usr/bin/env python3
"""
Simple startup script for MailMind Email Processing System
"""

import os
import sys
import subprocess

def main():
    """Main startup function"""
    print("🚀 MailMind Email Processing System")
    print("=" * 50)
    
    print("\n🎯 Choose an option:")
    print("1. Start Flask backend only")
    print("2. Start React frontend only")
    print("3. Start both (backend + frontend)")
    print("4. Run direct email processing")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\n🚀 Starting Flask backend server...")
            print("Backend will run on http://localhost:5000")
            try:
                subprocess.run([sys.executable, 'app.py'])
            except KeyboardInterrupt:
                print("\n⏹️ Backend server stopped")
            break
            
        elif choice == '2':
            print("\n🚀 Starting React frontend...")
            print("Frontend will run on http://localhost:3000")
            try:
                subprocess.run(['npm', 'start'])
            except KeyboardInterrupt:
                print("\n⏹️ Frontend server stopped")
            break
            
        elif choice == '3':
            print("\n🚀 Starting both servers...")
            print("Backend will run on http://localhost:5000")
            print("Frontend will run on http://localhost:3000")
            
            # Start backend in background
            backend_process = subprocess.Popen([sys.executable, 'app.py'])
            
            try:
                # Start frontend
                subprocess.run(['npm', 'start'])
            except KeyboardInterrupt:
                print("\n⏹️ Stopping servers...")
                backend_process.terminate()
            break
            
        elif choice == '4':
            print("\n🚀 Running direct email processing...")
            try:
                subprocess.run([sys.executable, 'main.py'])
            except KeyboardInterrupt:
                print("\n⏹️ Processing stopped")
            break
            
        elif choice == '5':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == '__main__':
    main()
