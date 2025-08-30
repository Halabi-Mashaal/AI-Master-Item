#!/usr/bin/env python3
"""
Test script to create a sample Excel file and test the RAG-enhanced file analysis
"""

import pandas as pd
import requests
import io
import os
import sys

# Prevent the script from importing the app module
sys.path = [p for p in sys.path if 'Master Item AI Agent' not in p]

# Create a sample Excel file for testing
def create_test_excel():
    """Create a test Excel file with cement industry data"""
    
    # Sample cement inventory data
    data = {
        'Item_Code': ['CEM001', 'CEM002', 'CEM003', 'CEM004', 'CEM005'],
        'Cement_Grade': ['OPC 53', 'OPC 43', 'PPC', 'PSC', 'OPC 53'],
        'Quantity_Bags': [5000, 3500, 2800, 1200, 4500],
        'Stock_Location': ['Warehouse A', 'Warehouse B', 'Warehouse A', 'Warehouse C', 'Warehouse B'],
        'Strength_MPa': [53, 43, 33, 33, 53],
        'Supplier': ['Saudi Cement', 'Yamama Cement', 'Riyadh Cement', 'Saudi Cement', 'Yamama Cement'],
        'Unit_Price': [15.5, 14.2, 13.8, 12.9, 15.3],
        'Manufacturing_Date': ['2024-01-15', '2024-01-20', '2024-01-18', '2024-01-22', '2024-01-17'],
        'Quality_Test_Status': ['Passed', 'Passed', 'Pending', 'Passed', 'Passed']
    }
    
    df = pd.DataFrame(data)
    
    # Create Excel file with multiple sheets
    excel_file = 'test_cement_inventory.xlsx'
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Main_Inventory', index=False)
        
        # Add a summary sheet
        summary_data = {
            'Grade': ['OPC 53', 'OPC 43', 'PPC', 'PSC'],
            'Total_Bags': [9500, 3500, 2800, 1200],
            'Avg_Price': [15.4, 14.2, 13.8, 12.9]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    print(f"✅ Created test Excel file: {excel_file}")
    return excel_file

def test_file_upload_analysis(excel_file):
    """Test the file upload and analysis endpoint"""
    
    url = 'http://127.0.0.1:8000/chat'  # Assuming the app runs on port 8000
    
    try:
        # Prepare the multipart form data
        files = {'file': open(excel_file, 'rb')}
        data = {
            'message': 'make analysis on this file',
            'language': 'en'
        }
        
        print(f"🚀 Testing file upload analysis...")
        print(f"📁 File: {excel_file}")
        print(f"💬 Message: {data['message']}")
        
        # Make the request
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS! Response received:")
            print(f"📊 Analysis Response:")
            print("-" * 80)
            print(result.get('response', 'No response content'))
            print("-" * 80)
            
            if 'rag_insights' in result:
                print(f"\n📚 RAG Insights:")
                rag_insights = result['rag_insights']
                print(f"   Documents Found: {rag_insights.get('documents_found', 0)}")
                print(f"   Max Relevance: {rag_insights.get('max_relevance', 0):.1%}")
                print(f"   Sources: {rag_insights.get('sources', [])}")
            
            if 'nlp_insights' in result:
                print(f"\n🧠 NLP Insights:")
                nlp_insights = result['nlp_insights']
                print(f"   Intent: {nlp_insights.get('intent', 'unknown')}")
                print(f"   Confidence: {nlp_insights.get('confidence', 0):.1%}")
                print(f"   Sentiment: {nlp_insights.get('sentiment', 'neutral')}")
            
        else:
            print(f"❌ ERROR: Status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("Make sure the application is running on http://127.0.0.1:8000")
    
    finally:
        if 'files' in locals():
            files['file'].close()

if __name__ == "__main__":
    print("🧪 RAG-Enhanced Excel Analysis Test")
    print("=" * 50)
    
    # Create test Excel file
    excel_file = create_test_excel()
    
    # Test the analysis
    test_file_upload_analysis(excel_file)
    
    # Cleanup
    try:
        os.remove(excel_file)
        print(f"\n🗑️ Cleaned up test file: {excel_file}")
    except:
        pass
