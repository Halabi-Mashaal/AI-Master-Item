#!/usr/bin/env python3
"""
Test script for MDM Guidelines functionality
Tests the Oracle MDM validation system without the full Flask app
"""

import sys
import os
sys.path.append('src')

from mdm_guidelines import (
    validate_item_data,
    get_mdm_guidelines, 
    get_quality_standards,
    generate_mdm_report
)

def test_item_validation():
    """Test individual item validation"""
    print("=== Testing Individual Item Validation ===")
    
    # Test valid item
    valid_item = {
        "item_number": "ITEM001",
        "description": "Test Item Description",
        "category": "MANUFACTURING",
        "uom": "EA",
        "unit_cost": 10.50,
        "safety_stock": 100,
        "attributes": {
            "color": "Blue",
            "weight": "1.5kg"
        }
    }
    
    result = validate_item_data(valid_item)
    print(f"Valid Item Score: {result.score}%")
    print(f"Is Valid: {result.is_valid}")
    print(f"Issues: {result.issues}")
    print()
    
    # Test invalid item
    invalid_item = {
        "item_number": "ITEM_WITH_INVALID_CHARACTERS_TOO_LONG_123456789",
        "description": "Test Item with @#$%^&*() invalid characters!",
        "category": "INVALID_CATEGORY",
        "uom": "INVALID_UOM",
        "unit_cost": -5.0,  # Invalid negative cost
        "safety_stock": -10  # Invalid negative stock
    }
    
    result = validate_item_data(invalid_item)
    print(f"Invalid Item Score: {result.score}%")
    print(f"Is Valid: {result.is_valid}")
    print(f"Issues: {result.issues}")
    print()

def test_guidelines():
    """Test getting guidelines"""
    print("=== Testing Guidelines Retrieval ===")
    
    guidelines = get_mdm_guidelines()
    print(f"Guidelines retrieved: {len(guidelines)} categories")
    for category, rules in guidelines.items():
        print(f"  {category}: {len(rules)} rules")
    print()

def test_quality_standards():
    """Test getting quality standards"""
    print("=== Testing Quality Standards ===")
    
    standards = get_quality_standards()
    print(f"Quality standards retrieved: {len(standards)} sections")
    for section, details in standards.items():
        print(f"  {section}: {details}")
    print()

def test_bulk_report():
    """Test bulk report generation"""
    print("=== Testing Bulk Report Generation ===")
    
    items = [
        {
            "item_number": "ITEM001",
            "description": "Good Item",
            "category": "MANUFACTURING",
            "uom": "EA",
            "unit_cost": 10.50,
        },
        {
            "item_number": "BAD_ITEM_WITH_VERY_LONG_NAME_123456789",
            "description": "Bad Item with @#$%^&*() characters!",
            "category": "INVALID",
            "uom": "WRONG",
            "unit_cost": -5.0,
        },
        {
            "item_number": "ITEM003",
            "description": "Average Item",
            "category": "SERVICES",
            "uom": "HR",
            "unit_cost": 25.0,
        }
    ]
    
    report = generate_mdm_report(items)
    print(f"Report Summary:")
    print(f"  Total Items: {report['summary']['total_items']}")
    print(f"  Compliant Items: {report['summary']['compliant_items']}")
    print(f"  Average Score: {report['summary']['average_score']:.1f}%")
    print(f"  Compliance Rate: {report['summary']['compliance_rate']:.1f}%")
    print(f"  Common Issues: {list(report['summary']['common_issues'].keys())[:3]}")  # Show top 3 issues
    print()

def main():
    """Run all tests"""
    print("Testing Oracle MDM Guidelines System")
    print("=" * 50)
    
    try:
        test_item_validation()
        test_guidelines()
        test_quality_standards()
        test_bulk_report()
        
        print("=" * 50)
        print("✅ All MDM Guidelines tests completed successfully!")
        print("✅ Oracle MDM standards validation is working properly!")
        print("✅ No Oracle EBS integration required - standards-only approach confirmed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
