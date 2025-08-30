#!/usr/bin/env python3
"""
Performance test for the optimized RAG system
"""

import requests
import time
import json

def test_response_time(message, expected_max_time=3.0):
    """Test response time for a given message"""
    url = 'http://127.0.0.1:8000/chat'
    
    start_time = time.time()
    
    try:
        response = requests.post(url, 
            json={'message': message, 'language': 'en'},
            timeout=10
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            server_time = result.get('response_time', response_time)
            
            print(f"✅ Message: '{message}'")
            print(f"   Client Time: {response_time:.3f}s")
            print(f"   Server Time: {server_time:.3f}s")
            
            if server_time <= expected_max_time:
                print(f"   🚀 FAST - Within {expected_max_time}s target")
            else:
                print(f"   ⚠️  SLOW - Exceeded {expected_max_time}s target")
            
            print(f"   Response Length: {len(result['response'])} chars")
            print()
            
            return server_time
        else:
            print(f"❌ ERROR {response.status_code}: {response.text}")
            return float('inf')
            
    except Exception as e:
        end_time = time.time()
        print(f"❌ EXCEPTION: {e} (Time: {end_time - start_time:.3f}s)")
        return float('inf')

def main():
    print("🧪 Performance Test Suite - RAG System Optimization")
    print("=" * 60)
    
    test_cases = [
        ("Hi", 1.0),  # Simple greeting - should be very fast
        ("Hello, how are you?", 1.5),  # Simple conversation
        ("What is cement analysis?", 2.0),  # Medium complexity
        ("Analyze cement inventory management system", 3.0),  # Complex query
        ("Hi", 0.5),  # Repeated query - should hit cache
    ]
    
    total_time = 0
    successful_tests = 0
    
    for message, max_time in test_cases:
        response_time = test_response_time(message, max_time)
        if response_time != float('inf'):
            total_time += response_time
            successful_tests += 1
        time.sleep(0.5)  # Brief pause between tests
    
    print("📊 Performance Summary:")
    print("-" * 30)
    if successful_tests > 0:
        avg_time = total_time / successful_tests
        print(f"Average Response Time: {avg_time:.3f}s")
        print(f"Successful Tests: {successful_tests}/{len(test_cases)}")
        
        if avg_time < 2.0:
            print("🎉 EXCELLENT - System performing well!")
        elif avg_time < 3.0:
            print("✅ GOOD - System within acceptable range")
        else:
            print("⚠️ NEEDS OPTIMIZATION - Consider further improvements")
    else:
        print("❌ All tests failed - Check if server is running")

if __name__ == "__main__":
    main()
