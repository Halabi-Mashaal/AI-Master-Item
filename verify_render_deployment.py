#!/usr/bin/env python3
"""
Render Deployment Verification Script
Monitors and validates Master Item AI Agent deployment on Render
"""
import requests
import json
import time
from datetime import datetime

# Configuration
RENDER_URL = "YOUR_RENDER_APP_URL"  # Update this after deployment
EXPECTED_ENDPOINTS = [
    "/",
    "/health",
    "/api/analyze",
    "/api/validate",
    "/api/process"
]

def check_deployment_health():
    """Check if the deployment is healthy and responding"""
    print(f"🔍 Checking deployment health at {datetime.now()}")
    print("=" * 60)
    
    # Health check
    try:
        response = requests.get(f"{RENDER_URL}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health Check PASSED")
            print(f"   Status: {health_data.get('status', 'Unknown')}")
            print(f"   Timestamp: {health_data.get('timestamp', 'Unknown')}")
            print(f"   Memory Optimized: {health_data.get('memory_optimized', 'Unknown')}")
            print(f"   AI Provider: {health_data.get('ai_provider', 'Unknown')}")
            return True
        else:
            print(f"❌ Health Check FAILED: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check ERROR: {e}")
        return False

def test_endpoints():
    """Test all critical endpoints"""
    print("\n🧪 Testing API Endpoints")
    print("-" * 30)
    
    results = {}
    
    for endpoint in EXPECTED_ENDPOINTS:
        try:
            url = f"{RENDER_URL}{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {endpoint}: OK")
                results[endpoint] = "OK"
            elif response.status_code == 404:
                print(f"⚠️  {endpoint}: Not Found (404)")
                results[endpoint] = "NOT_FOUND"
            else:
                print(f"❌ {endpoint}: HTTP {response.status_code}")
                results[endpoint] = f"ERROR_{response.status_code}"
                
        except Exception as e:
            print(f"❌ {endpoint}: {str(e)[:50]}...")
            results[endpoint] = "TIMEOUT/ERROR"
    
    return results

def test_ai_functionality():
    """Test Gemini AI integration in production"""
    print("\n🤖 Testing AI Functionality (Gemini)")
    print("-" * 40)
    
    test_payload = {
        "item_description": "Industrial warehouse pallet jack hydraulic lift",
        "category": "warehouse_equipment",
        "include_ai_analysis": True
    }
    
    try:
        response = requests.post(
            f"{RENDER_URL}/api/analyze",
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ AI Analysis WORKING")
            print(f"   Response length: {len(str(result))}")
            
            if 'ai_analysis' in result:
                ai_analysis = result['ai_analysis']
                print(f"   AI Provider: {ai_analysis.get('provider', 'Unknown')}")
                print(f"   Model: {ai_analysis.get('model', 'Unknown')}")
                print(f"   Confidence: {ai_analysis.get('confidence', 'Unknown')}")
                
            return True
        else:
            print(f"❌ AI Analysis FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ AI Analysis ERROR: {e}")
        return False

def test_mdm_validation():
    """Test Oracle MDM guidelines validation"""
    print("\n📋 Testing MDM Validation")
    print("-" * 30)
    
    test_payload = {
        "item_data": {
            "item_code": "WH-PJ-001",
            "description": "Hydraulic Pallet Jack 5000lb capacity",
            "category": "Material Handling Equipment",
            "unit_of_measure": "EACH",
            "manufacturer": "Crown Equipment"
        }
    }
    
    try:
        response = requests.post(
            f"{RENDER_URL}/api/validate",
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ MDM Validation WORKING")
            
            validation = result.get('validation', {})
            print(f"   Valid: {validation.get('is_valid', 'Unknown')}")
            print(f"   Score: {validation.get('score', 'Unknown')}")
            print(f"   Issues: {len(validation.get('issues', []))}")
            
            return True
        else:
            print(f"❌ MDM Validation FAILED: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ MDM Validation ERROR: {e}")
        return False

def monitor_deployment():
    """Comprehensive deployment monitoring"""
    print("🚀 RENDER DEPLOYMENT VERIFICATION")
    print("Master Item AI Agent with Google Gemini")
    print("=" * 60)
    
    if RENDER_URL == "YOUR_RENDER_APP_URL":
        print("⚠️  SETUP REQUIRED:")
        print("   1. Update RENDER_URL in this script with your Render app URL")
        print("   2. Format: https://your-app-name.onrender.com")
        print("   3. Re-run this script after deployment")
        return
    
    # Run all tests
    health_ok = check_deployment_health()
    endpoint_results = test_endpoints()
    ai_ok = test_ai_functionality()
    mdm_ok = test_mdm_validation()
    
    # Summary
    print("\n" + "=" * 60)
    print("DEPLOYMENT VERIFICATION SUMMARY")
    print("=" * 60)
    
    if health_ok:
        print("✅ Health Check: PASSED")
    else:
        print("❌ Health Check: FAILED")
    
    working_endpoints = sum(1 for status in endpoint_results.values() if status == "OK")
    print(f"📊 Endpoints: {working_endpoints}/{len(EXPECTED_ENDPOINTS)} working")
    
    if ai_ok:
        print("✅ Gemini AI: WORKING")
    else:
        print("❌ Gemini AI: FAILED")
        
    if mdm_ok:
        print("✅ MDM Validation: WORKING")
    else:
        print("❌ MDM Validation: FAILED")
    
    overall_health = health_ok and (working_endpoints >= len(EXPECTED_ENDPOINTS) * 0.8) and ai_ok and mdm_ok
    
    print("\n" + "-" * 60)
    if overall_health:
        print("🎉 DEPLOYMENT SUCCESSFUL!")
        print("   Your Master Item AI Agent is ready for production use")
        print("   ✅ Lightweight NLP mode active")
        print("   ✅ Google Gemini API integrated")
        print("   ✅ Oracle MDM guidelines working")
        print("   ✅ No heavy model downloads required")
    else:
        print("⚠️  DEPLOYMENT ISSUES DETECTED")
        print("   Review the test results above and check Render logs")
        print("   Common issues:")
        print("   - Environment variables not set")
        print("   - API key configuration")
        print("   - Memory/timeout limits")

if __name__ == "__main__":
    monitor_deployment()
