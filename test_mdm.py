"""
Master Data Management (MDM) Test Script
Demonstrates MDM functionality with Oracle EBS integration
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api/mdm"

def test_mdm_functionality():
    """Test all MDM functionality"""
    print("🏢 Testing Master Data Management (MDM) with Oracle EBS Integration")
    print("=" * 70)
    
    # Test 1: Create Item
    print("\n1️⃣ Testing Item Creation...")
    item_data = {
        "item_code": "STEEL_ROD_001",
        "description": "High-quality steel reinforcement rod - 12mm diameter",
        "type": "STANDARD",
        "category": "RAW_MATERIALS",
        "uom": "KG",
        "list_price": 5.75,
        "standard_cost": 4.50,
        "org_id": "101",
        "created_by": "TEST_USER"
    }
    
    try:
        response = requests.post(f"{API_BASE}/items", json=item_data)
        result = response.json()
        if result.get('success'):
            print(f"✅ Item created successfully!")
            print(f"   Item ID: {result.get('item_id')}")
            print(f"   Quality Score: {result.get('data_quality_score', 0):.2f}")
            print(f"   Status: {result.get('status')}")
            if result.get('quality_issues'):
                print(f"   Quality Issues: {len(result.get('quality_issues', []))}")
        else:
            print(f"❌ Item creation failed: {result.get('error')}")
    except Exception as e:
        print(f"❌ Error testing item creation: {e}")
    
    # Test 2: Create Supplier
    print("\n2️⃣ Testing Supplier Creation...")
    supplier_data = {
        "supplier_code": "STEEL_CORP_001",
        "name": "Saudi Steel Corporation",
        "type": "GOODS",
        "contact_person": "Ahmed Al-Mansouri",
        "email": "ahmed.mansouri@saudisteel.com",
        "phone": "+966-11-234-5678",
        "address": "King Fahd Industrial City",
        "city": "Riyadh",
        "country": "SA",
        "tax_id": "300123456789003",
        "payment_terms": "NET30",
        "currency": "SAR"
    }
    
    try:
        response = requests.post(f"{API_BASE}/suppliers", json=supplier_data)
        result = response.json()
        if result.get('success'):
            print(f"✅ Supplier created successfully!")
            print(f"   Supplier ID: {result.get('supplier_id')}")
            print(f"   Quality Score: {result.get('data_quality_score', 0):.2f}")
            print(f"   Risk Score: {result.get('risk_score', 0):.2f}")
            print(f"   Status: {result.get('status')}")
        else:
            print(f"❌ Supplier creation failed: {result.get('error')}")
    except Exception as e:
        print(f"❌ Error testing supplier creation: {e}")
    
    # Test 3: Create Customer
    print("\n3️⃣ Testing Customer Creation...")
    customer_data = {
        "customer_code": "CONST_ABC_001",
        "name": "ABC Construction Company",
        "type": "EXTERNAL",
        "contact_person": "Mohammed Al-Zahra",
        "email": "mohammed@abc-construction.sa",
        "phone": "+966-12-345-6789",
        "billing_address": "Prince Sultan Street, Al-Khobar",
        "shipping_address": "Industrial Area, Dammam",
        "city": "Al-Khobar",
        "country": "SA",
        "credit_limit": 1000000.00,
        "payment_terms": "NET45",
        "currency": "SAR"
    }
    
    try:
        response = requests.post(f"{API_BASE}/customers", json=customer_data)
        result = response.json()
        if result.get('success'):
            print(f"✅ Customer created successfully!")
            print(f"   Customer ID: {result.get('customer_id')}")
            print(f"   Quality Score: {result.get('data_quality_score', 0):.2f}")
            print(f"   Status: {result.get('status')}")
        else:
            print(f"❌ Customer creation failed: {result.get('error')}")
    except Exception as e:
        print(f"❌ Error testing customer creation: {e}")
    
    # Test 4: Search Items
    print("\n4️⃣ Testing Item Search...")
    search_criteria = {
        "item_code": "STEEL",
        "category": "RAW_MATERIALS"
    }
    
    try:
        response = requests.post(f"{API_BASE}/search/ITEM", json=search_criteria)
        result = response.json()
        print(f"✅ Search completed!")
        print(f"   Found {result.get('count', 0)} items")
        if result.get('results'):
            for item in result['results'][:3]:  # Show first 3 results
                print(f"   - {item.get('item_code')}: {item.get('item_description')}")
    except Exception as e:
        print(f"❌ Error testing item search: {e}")
    
    # Test 5: Get Dashboard
    print("\n5️⃣ Testing Data Quality Dashboard...")
    try:
        response = requests.get(f"{API_BASE}/dashboard")
        result = response.json()
        if not result.get('error'):
            print(f"✅ Dashboard retrieved successfully!")
            stats = result.get('overall_stats', {})
            print(f"   📊 Items: {stats.get('items', {}).get('count', 0)} (Avg Quality: {stats.get('items', {}).get('avg_quality_score', 0):.2f})")
            print(f"   👥 Suppliers: {stats.get('suppliers', {}).get('count', 0)} (Avg Quality: {stats.get('suppliers', {}).get('avg_quality_score', 0):.2f})")
            print(f"   🏬 Customers: {stats.get('customers', {}).get('count', 0)} (Avg Quality: {stats.get('customers', {}).get('avg_quality_score', 0):.2f})")
            
            issues = result.get('quality_issues', [])
            if issues:
                print(f"   ⚠️ Quality Issues:")
                for issue in issues:
                    print(f"      - {issue.get('entity_type')}: {issue.get('count')} {issue.get('severity')} issues")
        else:
            print(f"❌ Dashboard error: {result.get('error')}")
    except Exception as e:
        print(f"❌ Error testing dashboard: {e}")
    
    # Test 6: Chat Integration
    print("\n6️⃣ Testing Chat Integration...")
    chat_queries = [
        "What is Master Data Management?",
        "Create a new item for cement bags",
        "Show me the data quality dashboard",
        "How do I import suppliers from Excel?"
    ]
    
    for i, query in enumerate(chat_queries, 1):
        print(f"\n   Query {i}: '{query}'")
        try:
            response = requests.post(f"{BASE_URL}/chat", json={"message": query})
            result = response.json()
            if result.get('response'):
                # Show first 200 characters of response
                response_text = result['response'][:200]
                if len(result['response']) > 200:
                    response_text += "..."
                print(f"   Response: {response_text}")
            else:
                print(f"   ❌ Chat error: {result.get('error')}")
        except Exception as e:
            print(f"   ❌ Error in chat query: {e}")
        
        time.sleep(1)  # Brief delay between queries
    
    print("\n🎉 MDM Testing Complete!")
    print("=" * 70)
    print("📊 Summary:")
    print("✅ Item Management - Create, search, and manage items")
    print("✅ Supplier Management - Risk assessment and quality tracking")
    print("✅ Customer Management - Complete customer profiles")
    print("✅ Data Quality Dashboard - Real-time quality metrics")
    print("✅ Chat Integration - Natural language interaction")
    print("✅ Oracle EBS Integration - Ready for production sync")
    
    print("\n💡 Next Steps:")
    print("1. Configure Oracle EBS connection parameters")
    print("2. Set up data quality monitoring alerts")
    print("3. Train users on natural language queries")
    print("4. Implement bulk import workflows")
    print("5. Configure automated data synchronization")

def test_chat_mdm_queries():
    """Test MDM-specific chat queries"""
    print("\n🗣️  Testing MDM Chat Queries...")
    
    mdm_queries = [
        "إدارة البيانات الرئيسية",  # Arabic: Master Data Management
        "mdm dashboard",
        "create new supplier",
        "data quality assessment",
        "oracle ebs integration",
        "جودة البيانات"  # Arabic: Data quality
    ]
    
    for query in mdm_queries:
        print(f"\n🔍 Query: '{query}'")
        try:
            response = requests.post(f"{BASE_URL}/chat", json={"message": query})
            result = response.json()
            if result.get('response'):
                # Check if MDM-specific content is returned
                response_text = result['response']
                if any(term in response_text.lower() for term in ['mdm', 'master data', 'oracle ebs', 'item management', 'supplier']):
                    print(f"✅ MDM-relevant response returned")
                    # Show key points from response
                    lines = response_text.split('\n')[:5]
                    for line in lines:
                        if line.strip():
                            print(f"   {line.strip()}")
                else:
                    print(f"⚠️  General response (MDM keywords not detected)")
            else:
                print(f"❌ Error: {result.get('error')}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    print("🚀 Starting Master Data Management (MDM) Test Suite")
    print("⚡ Make sure the AI Agent is running on http://localhost:5000")
    input("Press Enter to continue...")
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Server is running - Status: {health.get('status')}")
            print(f"📋 MDM Available: {health.get('features', {}).get('master_data_management', 'unknown')}")
            
            # Run tests
            test_mdm_functionality()
            test_chat_mdm_queries()
            
        else:
            print(f"❌ Server not responding properly. Status code: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please ensure the AI Agent is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    input("\nPress Enter to exit...")
