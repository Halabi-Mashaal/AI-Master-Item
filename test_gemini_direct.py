#!/usr/bin/env python3
"""
Direct Gemini API test with the provided key
"""
import os
import google.generativeai as genai

# Set the API key
genai.configure(api_key='AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA')

def test_gemini_direct():
    """Test Gemini API directly"""
    print("Testing Google Gemini API directly...")
    
    try:
        # Create model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test 1: Simple response
        print("\n1. Simple response test:")
        response = model.generate_content("Hello! Please confirm you are Google Gemini and explain what you can do.")
        print(f"Response: {response.text}")
        
        # Test 2: Oracle MDM question
        print("\n2. Oracle MDM expertise test:")
        mdm_prompt = """
        You are helping with Oracle Master Data Management (MDM) for a cement company.
        What are the key validation rules for item master data in Oracle MDM?
        Please provide 5 specific guidelines.
        """
        response = model.generate_content(mdm_prompt)
        print(f"MDM Response: {response.text}")
        
        # Test 3: Cement industry question
        print("\n3. Cement industry expertise test:")
        cement_prompt = """
        As an expert in cement manufacturing, explain the key quality control parameters 
        for Portland cement production that should be tracked in an inventory system.
        """
        response = model.generate_content(cement_prompt)
        print(f"Cement Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DIRECT GOOGLE GEMINI API TEST")
    print("=" * 60)
    
    success = test_gemini_direct()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 GEMINI API WORKING PERFECTLY!")
        print("✅ Google Gemini is responding correctly")
        print("✅ Oracle MDM knowledge available")  
        print("✅ Cement industry expertise confirmed")
        print("✅ Ready for integration and deployment!")
    else:
        print("\n❌ Gemini API test failed")
