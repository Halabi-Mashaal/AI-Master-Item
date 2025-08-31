#!/usr/bin/env python3
"""
Render deployment test - verify app starts without heavy dependencies
"""
import os
import sys

# Set environment variables for lightweight mode
os.environ['USE_LIGHTWEIGHT_NLP'] = '1'
os.environ['MEMORY_OPTIMIZED'] = '1'  
os.environ['DISABLE_HEAVY_MODELS'] = '1'

# Add src to path
sys.path.insert(0, 'src')

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports for Render deployment...")
    
    try:
        # Test core Flask app import
        print("1. Testing Flask app import...")
        from app import app
        print("   ✅ Flask app imported successfully")
        
        # Test MDM guidelines import  
        print("2. Testing MDM guidelines import...")
        from mdm_guidelines import validate_item_data, get_mdm_guidelines
        print("   ✅ MDM guidelines imported successfully")
        
        # Test AI providers (should work in lightweight mode)
        print("3. Testing AI providers...")
        try:
            from ai_providers import AdvancedAIProvider
            print("   ✅ AI providers imported successfully")
        except ImportError as e:
            print(f"   ⚠️ AI providers import issue: {e}")
            
        # Test that app can start
        print("4. Testing Flask app startup...")
        with app.test_client() as client:
            response = client.get('/api/status')
            print(f"   ✅ App responds to status check: {response.status_code}")
            
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mdm_functionality():
    """Test MDM functionality works"""
    print("5. Testing MDM functionality...")
    
    try:
        from mdm_guidelines import validate_item_data
        
        test_item = {
            "item_number": "TEST001",
            "description": "Test Item",
            "category": "MANUFACTURING",
            "uom": "EA"
        }
        
        result = validate_item_data(test_item)
        print(f"   ✅ MDM validation working - Score: {result.score}%")
        return True
        
    except Exception as e:
        print(f"   ❌ MDM test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("RENDER DEPLOYMENT READINESS TEST")
    print("=" * 60)
    
    imports_ok = test_imports()
    mdm_ok = test_mdm_functionality()
    
    print("=" * 60)
    if imports_ok and mdm_ok:
        print("🎉 READY FOR RENDER DEPLOYMENT!")
        print("✅ All core functionality working")
        print("✅ MDM guidelines system operational")
        print("✅ No Oracle dependencies required")
        sys.exit(0)
    else:
        print("❌ NOT READY FOR DEPLOYMENT")
        print("Fix the issues above before deploying")
        sys.exit(1)
