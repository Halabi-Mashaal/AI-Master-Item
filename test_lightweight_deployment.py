#!/usr/bin/env python3
"""
Test lightweight NLP mode for Render deployment
Ensures no heavy models are loaded
"""
import os
import sys

# Set environment variables for lightweight mode
os.environ['USE_LIGHTWEIGHT_NLP'] = '1'
os.environ['MEMORY_OPTIMIZED'] = '1'
os.environ['DISABLE_HEAVY_MODELS'] = '1'
os.environ['GEMINI_API_KEY'] = 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA'
os.environ['AI_PROVIDER'] = 'gemini'

# Add src to path
sys.path.insert(0, 'src')

def test_lightweight_imports():
    """Test that imports work in lightweight mode without downloading models"""
    print("Testing lightweight NLP imports (no model downloads)...")
    
    try:
        # Test advanced NLP with lightweight mode
        print("1. Testing AdvancedNLPProcessor in lightweight mode...")
        from advanced_nlp import AdvancedNLPProcessor
        
        processor = AdvancedNLPProcessor()
        
        if processor.use_lightweight_nlp:
            print("   ✅ Lightweight mode properly enabled")
        else:
            print("   ❌ Lightweight mode not enabled")
            return False
            
        if processor.nlp_model is None:
            print("   ✅ No heavy spaCy model loaded")
        else:
            print("   ❌ SpaCy model was loaded despite lightweight mode")
            return False
            
        # Test basic text processing without models
        result = processor.extract_entities("Test text for warehouse inventory")
        print(f"   ✅ Basic entity extraction working: {len(result.get('entities', []))} entities found")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_startup():
    """Test that the main app can start in lightweight mode"""
    print("2. Testing Flask app startup in lightweight mode...")
    
    try:
        from app import app
        print("   ✅ Flask app imported successfully")
        
        # Test that app can create test client
        with app.test_client() as client:
            print("   ✅ Flask test client created successfully")
            
        return True
        
    except Exception as e:
        print(f"   ❌ App startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gemini_integration():
    """Test Gemini integration without heavy models"""
    print("3. Testing Gemini AI integration...")
    
    try:
        from ai_providers import AdvancedAIProvider
        
        ai_provider = AdvancedAIProvider()
        
        if ai_provider.provider == 'gemini':
            print("   ✅ Gemini provider selected")
            
            # Test a simple response
            response = ai_provider.generate_response("Hello, are you working?")
            if response and response.get('response'):
                print("   ✅ Gemini generating responses")
                return True
            else:
                print("   ❌ Gemini not responding properly")
                return False
        else:
            print(f"   ❌ Wrong provider selected: {ai_provider.provider}")
            return False
            
    except Exception as e:
        print(f"   ❌ Gemini integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all lightweight deployment tests"""
    print("=" * 60)
    print("RENDER DEPLOYMENT LIGHTWEIGHT MODE TEST")
    print("Environment: USE_LIGHTWEIGHT_NLP=1, DISABLE_HEAVY_MODELS=1")
    print("=" * 60)
    
    tests = [
        test_lightweight_imports,
        test_app_startup,
        test_gemini_integration
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
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 RENDER DEPLOYMENT READY!")
        print("✅ No heavy models loaded")
        print("✅ Lightweight NLP mode working")
        print("✅ Gemini AI integration functional")
        print("✅ No spaCy/transformers downloads required")
        return True
    else:
        print("❌ DEPLOYMENT NOT READY")
        print("Some issues detected - fix before deploying")
        return False

if __name__ == "__main__":
    main()
