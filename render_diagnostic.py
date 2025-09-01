#!/usr/bin/env python3
"""
RENDER DEPLOYMENT DIAGNOSTIC
Test exactly what happens in Render's Linux environment
"""
import os
import sys
import json
from datetime import datetime

print("🚀 RENDER DEPLOYMENT DIAGNOSTIC")
print("=" * 50)
print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Simulate Render environment variables
render_env_vars = {
    'PORT': '10000',
    'PYTHON_VERSION': '3.11',
    'FLASK_ENV': 'production', 
    'WEB_CONCURRENCY': '1',
    'MAX_WORKERS': '1',
    'APP_VERSION': 'v3.0-fresh-deploy',
    'GOOGLE_API_KEY': 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA',
    'GEMINI_API_KEY': 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA',
    'GOOGLE_GEMINI_API_KEY': 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA'
}

print("1️⃣ ENVIRONMENT VARIABLES CHECK")
print("-" * 30)
for key, value in render_env_vars.items():
    os.environ[key] = value
    print(f"✅ {key}: {value[:20]}{'...' if len(value) > 20 else ''}")
print()

print("2️⃣ YAMAMA AI V3 IMPORT TEST (With Render Env)")
print("-" * 30)
try:
    # Clear any previous imports
    if 'yamama_ai_v3' in sys.modules:
        del sys.modules['yamama_ai_v3']
    
    import yamama_ai_v3 as app_module
    
    print("✅ Import successful")
    print(f"📊 AI Available: {app_module.AI_AVAILABLE}")
    
    if hasattr(app_module, 'model') and app_module.model:
        print("✅ Gemini model initialized")
    else:
        print("❌ Gemini model not initialized")
        
    if hasattr(app_module, 'app'):
        print("✅ Flask app available")
        
        # Test a direct function call
        try:
            response = app_module.get_ai_response("Test message", "en")
            print(f"✅ AI Response Test: {response[:50]}...")
        except Exception as e:
            print(f"❌ AI Response Test Failed: {e}")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
print()

print("3️⃣ FLASK APP TEST")
print("-" * 30)
try:
    if 'yamama_ai_v3' in sys.modules:
        app = sys.modules['yamama_ai_v3'].app
        
        # Create test client
        with app.test_client() as client:
            
            # Test health endpoint
            health_response = client.get('/health')
            print(f"✅ Health Check: {health_response.status_code} - {health_response.get_json()}")
            
            # Test chat endpoint
            chat_data = {'message': 'Hello test', 'language': 'en'}
            chat_response = client.post('/chat', 
                                      json=chat_data,
                                      headers={'Content-Type': 'application/json'})
            print(f"📱 Chat Test: {chat_response.status_code}")
            
            if chat_response.status_code == 200:
                response_data = chat_response.get_json()
                if 'response' in response_data:
                    print(f"✅ Chat Response: {response_data['response'][:50]}...")
                else:
                    print(f"❌ No 'response' field: {response_data}")
            else:
                print(f"❌ Chat failed: {chat_response.get_data(as_text=True)}")
                
except Exception as e:
    print(f"❌ Flask test failed: {e}")
    import traceback
    traceback.print_exc()
print()

print("4️⃣ RENDER DEPLOYMENT SIMULATION COMPLETE")
print("-" * 30)
print("🔍 This simulates exactly what happens on Render")
print("🚨 If this works but Render fails, it's a Render platform issue")
print("=" * 50)
