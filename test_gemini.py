#!/usr/bin/env python3

import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv('.env')

async def test_gemini_connection():
    print("Testing Gemini API connection...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Simple test
        response = model.generate_content("Hello, respond with 'API working'")
        print(f"✅ Gemini response: {response.text}")
        
    except Exception as e:
        print(f"❌ Gemini API error: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini_connection())
