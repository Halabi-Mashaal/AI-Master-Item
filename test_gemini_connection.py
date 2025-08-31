#!/usr/bin/env python3
"""
Test Google Gemini API connection and functionality
"""
import os
import sys

# Set environment variables
os.environ['GEMINI_API_KEY'] = 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA'
os.environ['AI_PROVIDER'] = 'gemini'
os.environ['USE_LIGHTWEIGHT_NLP'] = '1'

# Add src to path
sys.path.insert(0, 'src')

def test_gemini_import():
    """Test Gemini API import"""
    print("1. Testing Gemini API import...")
    try:
        import google.generativeai as genai
        print("   ✅ Google Generative AI library imported successfully")
        return True
    except ImportError as e:
        print(f"   ❌ Failed to import Google Generative AI: {e}")
        return False

def test_gemini_configuration():
    """Test Gemini API configuration"""
    print("2. Testing Gemini API configuration...")
    try:
        import google.generativeai as genai
        
        # Configure with API key
        api_key = os.environ.get('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        print(f"   ✅ Gemini configured with API key: {api_key[:10]}...")
        
        # Test model listing
        models = list(genai.list_models())
        print(f"   ✅ Available models: {len(models)} models found")
        
        return True
    except Exception as e:
        print(f"   ❌ Gemini configuration failed: {e}")
        return False

def test_gemini_chat():
    """Test Gemini chat functionality"""
    print("3. Testing Gemini chat...")
    try:
        import google.generativeai as genai
        
        # Configure API
        api_key = os.environ.get('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        
        # Create model with updated name
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test simple chat
        response = model.generate_content("Hello, please respond with 'Gemini is working!'")
        result_text = response.text
        
        print(f"   ✅ Gemini response: {result_text}")
        return True
        
    except Exception as e:
        print(f"   ❌ Gemini chat test failed: {e}")
        return False

def test_ai_provider_integration():
    """Test AI provider integration with Gemini"""
    print("4. Testing AI provider integration...")
    try:
        from ai_providers import AdvancedAIProvider
        
        # Create AI provider instance
        ai_provider = AdvancedAIProvider()
        
        # Test generate_response functionality
        response_data = ai_provider.generate_response("Hello, can you confirm Gemini is working?")
        response_text = response_data.get('response', response_data.get('text', str(response_data)))
        print(f"   ✅ AI Provider response: {response_text[:100]}...")
        
        return True
    except Exception as e:
        print(f"   ❌ AI provider integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mdm_with_gemini():
    """Test MDM functionality with Gemini AI"""
    print("5. Testing MDM with Gemini AI...")
    try:
        from mdm_guidelines import validate_item_data
        from ai_providers import AdvancedAIProvider
        
        # Test item validation
        test_item = {
            "item_number": "GEMINI_TEST_001",
            "description": "Gemini AI Test Item",
            "category": "MANUFACTURING", 
            "uom": "EA"
        }
        
        validation_result = validate_item_data(test_item)
        print(f"   ✅ MDM validation score: {validation_result.score}%")
        
        # Test AI-enhanced validation explanation
        ai_provider = AdvancedAIProvider()
        mdm_question = f"Explain why this item scored {validation_result.score}% in Oracle MDM validation: {test_item}"
        ai_response_data = ai_provider.generate_response(mdm_question)
        ai_response = ai_response_data.get('response', ai_response_data.get('text', str(ai_response_data)))
        print(f"   ✅ Gemini MDM explanation: {ai_response[:150]}...")
        
        return True
    except Exception as e:
        print(f"   ❌ MDM with Gemini failed: {e}")
        return False

def main():
    """Run all Gemini API tests"""
    print("=" * 60)
    print("GOOGLE GEMINI API CONNECTION TEST")
    print(f"API Key: AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA")
    print("=" * 60)
    
    tests = [
        test_gemini_import,
        test_gemini_configuration, 
        test_gemini_chat,
        test_ai_provider_integration,
        test_mdm_with_gemini
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            print()
    
    print("=" * 60)
    print(f"TEST RESULTS: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 GEMINI API FULLY CONNECTED!")
        print("✅ Google Gemini AI is ready for production")
        print("✅ AI Provider integration working")
        print("✅ MDM + Gemini AI ready for deployment")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        print("Please check the API key and network connection")
        return False

if __name__ == "__main__":
    main()
