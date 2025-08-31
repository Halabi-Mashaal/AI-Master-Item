#!/usr/bin/env python3
"""
Check available Gemini models
"""
import google.generativeai as genai

# Configure API
genai.configure(api_key='AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA')

print("🔍 Checking available Gemini models...")

try:
    models = genai.list_models()
    print("\n✅ Available models:")
    for model in models:
        print(f"  - {model.name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"    Supported methods: {model.supported_generation_methods}")
        print()
        
except Exception as e:
    print(f"❌ Error listing models: {e}")

# Try different model names
model_names_to_try = [
    'gemini-pro',
    'gemini-1.5-flash',
    'gemini-1.5-pro', 
    'models/gemini-pro',
    'models/gemini-1.5-flash',
    'models/gemini-1.5-pro'
]

print("\n🧪 Testing model names:")
for model_name in model_names_to_try:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        if response and response.text:
            print(f"✅ {model_name}: SUCCESS - {response.text[:50]}...")
        else:
            print(f"❌ {model_name}: Empty response")
    except Exception as e:
        print(f"❌ {model_name}: {str(e)[:100]}...")
