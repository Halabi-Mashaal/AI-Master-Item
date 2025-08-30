import requests
import os

def test_excel_analysis():
    """Test the Excel file analysis endpoint"""
    
    url = 'http://127.0.0.1:8000/chat'
    file_path = 'New Microsoft Excel Worksheet.xlsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Test file {file_path} not found!")
        return
    
    try:
        print(f"🧪 Testing Excel file analysis...")
        print(f"📁 File: {file_path}")
        print(f"🌐 URL: {url}")
        
        # Prepare the request
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'message': 'make analysis on this file',
                'language': 'en'
            }
            
            print(f"🚀 Sending request...")
            response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS! Response received:")
            print("=" * 80)
            print(result.get('response', 'No response content'))
            print("=" * 80)
            
            # Print additional insights if available
            if 'rag_insights' in result:
                print(f"\n📚 RAG Insights:")
                rag_insights = result['rag_insights']
                print(f"   Documents Found: {rag_insights.get('documents_found', 0)}")
                if rag_insights.get('max_relevance'):
                    print(f"   Max Relevance: {rag_insights['max_relevance']:.1%}")
                print(f"   Sources: {rag_insights.get('sources', [])}")
            
            if 'nlp_insights' in result:
                print(f"\n🧠 NLP Insights:")
                nlp_insights = result['nlp_insights']
                print(f"   Intent: {nlp_insights.get('intent', 'unknown')}")
                if nlp_insights.get('confidence'):
                    print(f"   Confidence: {nlp_insights['confidence']:.1%}")
                print(f"   Sentiment: {nlp_insights.get('sentiment', 'neutral')}")
            
            return True
            
        else:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text[:500]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the server")
        print("Make sure the application is running on http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🧪 RAG-Enhanced Excel Analysis Test")
    print("=" * 50)
    success = test_excel_analysis()
    
    if success:
        print(f"\n🎉 TEST PASSED - Excel analysis is working correctly!")
    else:
        print(f"\n💥 TEST FAILED - There are issues with Excel analysis")
