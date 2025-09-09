#!/usr/bin/env python3
"""
Test script to verify Gemini integration
"""

import google.generativeai as genai
from config import Config

def test_gemini_connection():
    """Test Gemini API connection"""
    print("🧪 Testing Gemini Integration")
    print("=" * 40)
    
    config = Config()
    
    if not config.GOOGLE_GEN_AI_API_KEY:
        print("❌ No Gemini API key found")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=config.GOOGLE_GEN_AI_API_KEY)
        
        # Create model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Test simple prompt
        prompt = "Say 'Hello, Gemini is working!' in one sentence."
        response = model.generate_content(prompt)
        
        if response.text:
            print("✅ Gemini connection successful!")
            print(f"Response: {response.text}")
            return True
        else:
            print("❌ No response from Gemini")
            return False
            
    except Exception as e:
        print(f"❌ Gemini test failed: {e}")
        return False

def test_email_analysis():
    """Test email analysis with Gemini"""
    print("\n📧 Testing Email Analysis")
    print("=" * 40)
    
    config = Config()
    
    if not config.GOOGLE_GEN_AI_API_KEY:
        print("❌ No Gemini API key found")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=config.GOOGLE_GEN_AI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Sample email
        sample_email = """
        Hi Team,
        
        We have a meeting tomorrow at 2 PM in the conference room.
        Please bring your project updates.
        
        Best regards,
        John
        """
        
        # Test event extraction
        prompt = f"""
        Analyze this email text and extract event information if present.
        Return the result as a JSON object with these fields:
        - event_detected: boolean
        - title: string (event title)
        - start_time: string (ISO format if found)
        - end_time: string (ISO format if found)
        - location: string
        - description: string
        
        Email text:
        {sample_email}
        
        Return only the JSON object, no other text.
        """
        
        response = model.generate_content(prompt)
        
        if response.text:
            print("✅ Email analysis successful!")
            print(f"Response: {response.text}")
            return True
        else:
            print("❌ No response from Gemini")
            return False
            
    except Exception as e:
        print(f"❌ Email analysis test failed: {e}")
        return False

def main():
    print("🚀 Gemini Integration Test")
    print("=" * 50)
    
    # Test basic connection
    connection_ok = test_gemini_connection()
    
    # Test email analysis
    analysis_ok = test_email_analysis()
    
    if connection_ok and analysis_ok:
        print("\n🎉 All Gemini tests passed!")
        print("✅ Ready to process emails with Gemini")
    else:
        print("\n❌ Some tests failed")
        print("💡 Check your Gemini API key and internet connection")

if __name__ == "__main__":
    main()
