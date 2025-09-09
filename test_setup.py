#!/usr/bin/env python3
"""
Test script to verify MailMind setup (Firebase Edition)
"""

import os
import sys
from pathlib import Path

def test_config():
    """Test configuration loading"""
    print("🔧 Testing configuration...")
    try:
        from config import Config
        config = Config()
        print("✅ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_credentials():
    """Test if credentials.json exists"""
    print("\n🔑 Testing Google credentials...")
    if os.path.exists('credentials.json'):
        print("✅ credentials.json found")
        return True
    else:
        print("❌ credentials.json not found")
        print("   Download from Google Cloud Console and place in project root")
        return False

def test_firebase_credentials():
    """Test if Firebase credentials exist"""
    print("\n🔥 Testing Firebase credentials...")
    if os.path.exists('firebase-credentials.json'):
        print("✅ firebase-credentials.json found")
        return True
    else:
        print("❌ firebase-credentials.json not found")
        print("   Download from Firebase Console and place in project root")
        return False

def test_firebase_connection():
    """Test Firebase connection"""
    print("\n🔥 Testing Firebase connection...")
    try:
        from firebase_service import firebase_service
        if firebase_service.db:
            print("✅ Firebase connected successfully")
            return True
        else:
            print("❌ Firebase connection failed")
            return False
    except Exception as e:
        print(f"❌ Firebase connection error: {e}")
        return False

def test_models():
    """Test AI models loading"""
    print("\n🤖 Testing AI models...")
    try:
        from models.unified_model import email_processor
        print("✅ Unified model loaded successfully")
        
        # Check individual models
        if email_processor.spam_model:
            print("   ✅ Spam detection model loaded")
        else:
            print("   ⚠️ Spam detection model not loaded")
            
        if email_processor.nlp:
            print("   ✅ NLP model loaded")
        else:
            print("   ⚠️ NLP model not loaded")
            
        if email_processor.summarizer:
            print("   ✅ Summarization model loaded")
        else:
            print("   ⚠️ Summarization model not loaded")
            
        return True
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False

def test_google_genai():
    """Test Google Generative AI"""
    print("\n🤖 Testing Google Gen AI...")
    try:
        import google.generativeai as genai
        from config import Config
        config = Config()
        
        if config.GOOGLE_GENAI_API_KEY:
            genai.configure(api_key=config.GOOGLE_GENAI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = model.generate_content('Hello, world!')
            print("✅ Google Gen AI working")
            return True
        else:
            print("⚠️ Google Gen AI API key not set")
            return False
    except Exception as e:
        print(f"❌ Google Gen AI error: {e}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'flask', 'pandas', 'sklearn', 'spacy', 'transformers',
        'google', 'requests', 'firebase_admin', 'beautifulsoup4'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\n🔧 Testing environment variables...")
    
    env_vars = [
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET',
        'FIREBASE_PROJECT_ID',
        'GOOGLE_GENAI_API_KEY'
    ]
    
    missing_vars = []
    
    for var in env_vars:
        if os.getenv(var):
            print(f"   ✅ {var}")
        else:
            print(f"   ⚠️ {var} - Not set (using defaults)")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n📝 Please set these environment variables in your .env file:")
        for var in missing_vars:
            print(f"   {var}=your_value_here")
    
    return True

def main():
    """Main test function"""
    print("🧪 MailMind Setup Test (Firebase Edition)")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration", test_config),
        ("Environment", test_environment),
        ("Google Credentials", test_credentials),
        ("Firebase Credentials", test_firebase_credentials),
        ("Firebase Connection", test_firebase_connection),
        ("AI Models", test_models),
        ("Google Gen AI", test_google_genai)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 You can now run:")
        print("   python run.py")
    elif passed >= total * 0.7:
        print("⚠️ Most tests passed. System should work with some limitations.")
    else:
        print("❌ Many tests failed. Please check the issues above.")
        print("\n📖 See setup_guide.md for detailed setup instructions.")

if __name__ == '__main__':
    main()
