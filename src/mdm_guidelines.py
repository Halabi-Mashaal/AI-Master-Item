"""
Master Data Management Guidelines and Best Practices
Based on Oracle MDM Standards - No Integration Required
Provides comprehensive rules and validation for item management
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass

@dataclass
class MDMValidationResult:
    """Result of MDM validation check"""
    is_valid: bool
    score: float  # 0-100
    issues: List[str]
    recommendations: List[str]
    compliance_level: str  # 'Poor', 'Fair', 'Good', 'Excellent'

class OracleMDMGuidelines:
    """
    Oracle Master Data Management Guidelines and Standards
    Provides validation rules without requiring Oracle EBS connection
    """
    
    def __init__(self):
        self.item_categories = {
            'cement': ['Portland Cement', 'Blended Cement', 'White Cement', 'Oil Well Cement'],
            'raw_materials': ['Limestone', 'Clay', 'Sand', 'Iron Ore', 'Gypsum'],
            'packaging': ['Bags', 'Bulk Containers', 'Pallets', 'Labels'],
            'spare_parts': ['Mechanical Parts', 'Electrical Components', 'Consumables'],
            'services': ['Maintenance', 'Transportation', 'Consulting']
        }
        
        self.uom_standards = {
            'weight': ['KG', 'TON', 'LB', 'G'],
            'volume': ['L', 'M3', 'GAL', 'ML'],
            'length': ['M', 'CM', 'MM', 'IN', 'FT'],
            'area': ['M2', 'CM2', 'FT2'],
            'count': ['EA', 'PCS', 'SET', 'LOT', 'BOX']
        }
        
        self.hazard_classes = [
            'NON-HAZARDOUS',
            'FLAMMABLE',
            'CORROSIVE', 
            'TOXIC',
            'OXIDIZER',
            'EXPLOSIVE',
            'RADIOACTIVE'
        ]
        
    def validate_item_master(self, item_data: Dict[str, Any]) -> MDMValidationResult:
        """
        Comprehensive validation of item master data against Oracle MDM standards
        """
        issues = []
        recommendations = []
        score_components = {}
        
        # 1. Item Number Validation (25% of score)
        item_num_result = self._validate_item_number(item_data.get('item_number', ''))
        score_components['item_number'] = item_num_result[0]
        if not item_num_result[0]:
            issues.extend(item_num_result[1])
            recommendations.extend(item_num_result[2])
        
        # 2. Description Validation (20% of score)
        desc_result = self._validate_descriptions(item_data)
        score_components['description'] = desc_result[0]
        if desc_result[1]:
            issues.extend(desc_result[1])
            recommendations.extend(desc_result[2])
            
        # 3. Category and Classification (15% of score)
        cat_result = self._validate_category(item_data.get('category', ''), item_data.get('subcategory', ''))
        score_components['category'] = cat_result[0]
        if cat_result[1]:
            issues.extend(cat_result[1])
            recommendations.extend(cat_result[2])
            
        # 4. UOM Validation (15% of score)
        uom_result = self._validate_uom(item_data.get('primary_uom', ''), item_data.get('secondary_uom', ''))
        score_components['uom'] = uom_result[0]
        if uom_result[1]:
            issues.extend(uom_result[1])
            recommendations.extend(uom_result[2])
            
        # 5. Attributes Completeness (10% of score)
        attr_result = self._validate_attributes(item_data)
        score_components['attributes'] = attr_result[0]
        if attr_result[1]:
            issues.extend(attr_result[1])
            recommendations.extend(attr_result[2])
            
        # 6. Safety and Compliance (10% of score)
        safety_result = self._validate_safety_compliance(item_data)
        score_components['safety'] = safety_result[0]
        if safety_result[1]:
            issues.extend(safety_result[1])
            recommendations.extend(safety_result[2])
            
        # 7. Financial Data (5% of score)
        financial_result = self._validate_financial_data(item_data)
        score_components['financial'] = financial_result[0]
        if financial_result[1]:
            issues.extend(financial_result[1])
            recommendations.extend(financial_result[2])
        
        # Calculate overall score
        weights = {
            'item_number': 0.25,
            'description': 0.20,
            'category': 0.15,
            'uom': 0.15,
            'attributes': 0.10,
            'safety': 0.10,
            'financial': 0.05
        }
        
        overall_score = sum(score_components[key] * weights[key] for key in weights.keys()) * 100
        
        # Determine compliance level
        if overall_score >= 90:
            compliance_level = 'Excellent'
        elif overall_score >= 75:
            compliance_level = 'Good'
        elif overall_score >= 60:
            compliance_level = 'Fair'
        else:
            compliance_level = 'Poor'
            
        return MDMValidationResult(
            is_valid=overall_score >= 70,
            score=overall_score,
            issues=issues,
            recommendations=recommendations,
            compliance_level=compliance_level
        )
    
    def _validate_item_number(self, item_number: str) -> Tuple[float, List[str], List[str]]:
        """Validate item number according to Oracle MDM naming conventions"""
        issues = []
        recommendations = []
        score = 0.0
        
        if not item_number:
            issues.append("Item number is required")
            recommendations.append("Assign a unique item number following company naming convention")
            return score, issues, recommendations
            
        # Length check (Oracle standard: 10-40 characters)
        if len(item_number) < 5:
            issues.append("Item number too short (minimum 5 characters)")
            recommendations.append("Use descriptive item number with minimum 5 characters")
            score += 0.2
        elif len(item_number) > 40:
            issues.append("Item number too long (maximum 40 characters)")
            recommendations.append("Shorten item number to comply with Oracle EBS limits")
            score += 0.2
        else:
            score += 0.4
            
        # Character validation (alphanumeric, dashes, underscores only)
        if not re.match(r'^[A-Z0-9_-]+$', item_number):
            issues.append("Item number contains invalid characters")
            recommendations.append("Use only uppercase letters, numbers, dashes, and underscores")
        else:
            score += 0.3
            
        # Meaningful structure check
        if re.match(r'^[A-Z]{2,4}-\d{4,}-[A-Z0-9]{2,}$', item_number):
            score += 0.3
        elif re.match(r'^[A-Z]{2,4}\d{4,}$', item_number):
            score += 0.2
        else:
            recommendations.append("Consider structured format: PREFIX-NNNN-SUFFIX for better organization")
            score += 0.1
            
        return score, issues, recommendations
    
    def _validate_descriptions(self, item_data: Dict) -> Tuple[float, List[str], List[str]]:
        """Validate item descriptions"""
        issues = []
        recommendations = []
        score = 0.0
        
        short_desc = item_data.get('short_description', '').strip()
        long_desc = item_data.get('long_description', '').strip()
        
        # Short description validation
        if not short_desc:
            issues.append("Short description is mandatory")
            recommendations.append("Add concise short description (10-60 characters)")
        elif len(short_desc) < 10:
            issues.append("Short description too brief")
            recommendations.append("Expand short description to be more descriptive (10-60 characters)")
            score += 0.2
        elif len(short_desc) > 60:
            issues.append("Short description exceeds Oracle limit")
            recommendations.append("Shorten description to 60 characters maximum")
            score += 0.2
        else:
            score += 0.4
            
        # Long description validation
        if not long_desc:
            recommendations.append("Consider adding detailed long description for better clarity")
            score += 0.3
        elif len(long_desc) < 20:
            recommendations.append("Long description could be more detailed")
            score += 0.3
        elif len(long_desc) > 2000:
            issues.append("Long description exceeds Oracle EBS limit (2000 characters)")
            recommendations.append("Reduce long description to under 2000 characters")
            score += 0.2
        else:
            score += 0.4
            
        # Content quality check
        if short_desc and not any(char.isdigit() for char in short_desc):
            if not any(word in short_desc.lower() for word in ['cement', 'bag', 'kg', 'ton', 'grade']):
                recommendations.append("Include key product attributes in description (grade, size, etc.)")
            else:
                score += 0.2
        
        return score, issues, recommendations
    
    def _validate_category(self, category: str, subcategory: str) -> Tuple[float, List[str], List[str]]:
        """Validate item category and subcategory"""
        issues = []
        recommendations = []
        score = 0.0
        
        if not category:
            issues.append("Item category is required")
            recommendations.append("Assign appropriate category from predefined list")
            return score, issues, recommendations
            
        # Check against predefined categories
        category_lower = category.lower()
        valid_category = False
        
        for cat_key, subcats in self.item_categories.items():
            if cat_key in category_lower or category_lower in cat_key:
                valid_category = True
                score += 0.5
                
                # Validate subcategory
                if subcategory:
                    if any(subcat.lower() in subcategory.lower() or subcategory.lower() in subcat.lower() 
                           for subcat in subcats):
                        score += 0.5
                    else:
                        recommendations.append(f"Consider subcategory from: {', '.join(subcats)}")
                        score += 0.3
                else:
                    recommendations.append("Add subcategory for better classification")
                    score += 0.3
                break
        
        if not valid_category:
            issues.append("Category not recognized in standard classifications")
            recommendations.append(f"Use standard categories: {', '.join(self.item_categories.keys())}")
            
        return score, issues, recommendations
    
    def _validate_uom(self, primary_uom: str, secondary_uom: str) -> Tuple[float, List[str], List[str]]:
        """Validate Unit of Measure"""
        issues = []
        recommendations = []
        score = 0.0
        
        if not primary_uom:
            issues.append("Primary UOM is mandatory")
            recommendations.append("Specify primary unit of measure")
            return score, issues, recommendations
            
        # Check against standard UOMs
        primary_valid = False
        for uom_type, uoms in self.uom_standards.items():
            if primary_uom.upper() in uoms:
                primary_valid = True
                score += 0.6
                break
                
        if not primary_valid:
            issues.append("Primary UOM not in standard list")
            recommendations.append("Use standard UOM codes (KG, TON, EA, M, L, etc.)")
        
        # Secondary UOM validation
        if secondary_uom:
            secondary_valid = False
            for uom_type, uoms in self.uom_standards.items():
                if secondary_uom.upper() in uoms:
                    secondary_valid = True
                    score += 0.3
                    break
            
            if not secondary_valid:
                issues.append("Secondary UOM not in standard list")
                recommendations.append("Use standard secondary UOM or leave blank")
            
            # Check for logical relationship
            if primary_uom.upper() == secondary_uom.upper():
                issues.append("Primary and secondary UOM cannot be the same")
                recommendations.append("Use different units or remove secondary UOM")
        else:
            score += 0.1  # Slight bonus for not having conflicting secondary UOM
            
        return score, issues, recommendations
    
    def _validate_attributes(self, item_data: Dict) -> Tuple[float, List[str], List[str]]:
        """Validate item attributes completeness"""
        issues = []
        recommendations = []
        score = 0.0
        
        required_attrs = ['manufacturer', 'brand', 'model', 'specifications']
        optional_attrs = ['color', 'size', 'weight', 'dimensions', 'material']
        
        # Required attributes check
        required_present = 0
        for attr in required_attrs:
            if item_data.get(attr) and str(item_data[attr]).strip():
                required_present += 1
            else:
                recommendations.append(f"Consider adding {attr.replace('_', ' ').title()}")
        
        score += (required_present / len(required_attrs)) * 0.7
        
        # Optional attributes bonus
        optional_present = 0
        for attr in optional_attrs:
            if item_data.get(attr) and str(item_data[attr]).strip():
                optional_present += 1
        
        score += (optional_present / len(optional_attrs)) * 0.3
        
        # Special validations
        if item_data.get('weight'):
            try:
                weight = float(item_data['weight'])
                if weight <= 0:
                    issues.append("Weight must be positive")
                    recommendations.append("Verify and correct weight value")
            except (ValueError, TypeError):
                issues.append("Weight must be numeric")
                recommendations.append("Enter weight as number (e.g., 50.0)")
        
        return score, issues, recommendations
    
    def _validate_safety_compliance(self, item_data: Dict) -> Tuple[float, List[str], List[str]]:
        """Validate safety and compliance data"""
        issues = []
        recommendations = []
        score = 0.0
        
        # Hazard classification
        hazard_class = item_data.get('hazard_classification', '').upper()
        if hazard_class:
            if hazard_class in self.hazard_classes:
                score += 0.4
            else:
                issues.append("Invalid hazard classification")
                recommendations.append(f"Use standard classifications: {', '.join(self.hazard_classes)}")
        else:
            recommendations.append("Specify hazard classification for safety compliance")
            score += 0.1
        
        # Safety data sheet
        if item_data.get('sds_number'):
            score += 0.3
        else:
            recommendations.append("Add Safety Data Sheet (SDS) reference if applicable")
            score += 0.2
        
        # Environmental compliance
        if item_data.get('environmental_compliance'):
            score += 0.3
        else:
            recommendations.append("Document environmental compliance status")
            score += 0.2
        
        return score, issues, recommendations
    
    def _validate_financial_data(self, item_data: Dict) -> Tuple[float, List[str], List[str]]:
        """Validate financial and costing data"""
        issues = []
        recommendations = []
        score = 0.5  # Base score for non-critical data
        
        # Cost validation
        if item_data.get('standard_cost'):
            try:
                cost = float(item_data['standard_cost'])
                if cost < 0:
                    issues.append("Standard cost cannot be negative")
                    recommendations.append("Verify standard cost value")
                else:
                    score += 0.3
            except (ValueError, TypeError):
                issues.append("Standard cost must be numeric")
                recommendations.append("Enter cost as number (e.g., 100.50)")
        
        # Currency validation
        if item_data.get('currency'):
            if len(item_data['currency']) == 3 and item_data['currency'].isupper():
                score += 0.2
            else:
                issues.append("Use 3-letter currency code (e.g., SAR, USD)")
                recommendations.append("Follow ISO 4217 currency standards")
        
        return score, issues, recommendations
    
    def get_item_creation_guidelines(self) -> Dict[str, Any]:
        """
        Get comprehensive guidelines for creating new items
        """
        return {
            'naming_conventions': {
                'item_number': {
                    'format': 'PREFIX-NNNN-SUFFIX',
                    'examples': ['CEM-5001-OPC', 'RM-2001-LS', 'PKG-1001-BAG'],
                    'rules': [
                        'Use uppercase letters only',
                        '5-40 characters maximum', 
                        'No spaces or special characters except dash and underscore',
                        'Must be unique across all organizations'
                    ]
                },
                'descriptions': {
                    'short_description': {
                        'length': '10-60 characters',
                        'content': 'Concise, descriptive, include key attributes',
                        'example': 'Portland Cement OPC Grade 42.5 - 50kg Bag'
                    },
                    'long_description': {
                        'length': '20-2000 characters', 
                        'content': 'Detailed specifications, usage, technical details',
                        'example': 'Ordinary Portland Cement conforming to SASO standards...'
                    }
                }
            },
            'required_fields': [
                'Item Number',
                'Short Description', 
                'Primary UOM',
                'Item Category',
                'Organization',
                'Item Status'
            ],
            'recommended_fields': [
                'Long Description',
                'Manufacturer',
                'Brand',
                'Model/Grade',
                'Specifications',
                'Hazard Classification',
                'Standard Cost',
                'Weight',
                'Dimensions'
            ],
            'category_structure': self.item_categories,
            'uom_standards': self.uom_standards,
            'validation_checklist': [
                'Item number follows naming convention',
                'All required fields completed',
                'UOM is from standard list',
                'Category properly classified',
                'Safety data documented',
                'Financial data accurate',
                'No duplicate items exist',
                'Approval workflow completed'
            ]
        }
    
    def get_data_quality_rules(self) -> Dict[str, Any]:
        """
        Get data quality rules and standards
        """
        return {
            'completeness_standards': {
                'critical_fields': 95,  # Must be 95%+ complete
                'important_fields': 85,  # Should be 85%+ complete  
                'optional_fields': 60   # Nice to have 60%+ complete
            },
            'consistency_rules': [
                'All item numbers follow same naming convention',
                'UOM codes standardized across all items',
                'Category assignments consistent',
                'Manufacturer names standardized',
                'Currency codes follow ISO standards'
            ],
            'accuracy_validations': [
                'Numeric fields contain valid numbers',
                'Date fields in correct format',
                'UOM codes exist in reference table',
                'Category codes exist in hierarchy',
                'No duplicate item numbers'
            ],
            'timeliness_requirements': [
                'New items created within 24 hours of request',
                'Changes processed within 4 hours',
                'Obsolete items deactivated immediately',
                'Regular reviews every 6 months'
            ]
        }

# Initialize the MDM Guidelines system
mdm_guidelines = OracleMDMGuidelines()

def validate_item_data(item_data: Dict[str, Any]) -> MDMValidationResult:
    """Validate item data against Oracle MDM guidelines"""
    return mdm_guidelines.validate_item_master(item_data)

def get_mdm_guidelines() -> Dict[str, Any]:
    """Get comprehensive MDM guidelines"""
    return mdm_guidelines.get_item_creation_guidelines()

def get_quality_standards() -> Dict[str, Any]:
    """Get data quality rules and standards"""
    return mdm_guidelines.get_data_quality_rules()

def generate_mdm_report(items_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate MDM compliance report for multiple items"""
    if not items_data:
        return {'error': 'No items provided for analysis'}
    
    results = []
    summary = {
        'total_items': len(items_data),
        'compliant_items': 0,
        'average_score': 0.0,
        'compliance_distribution': {'Excellent': 0, 'Good': 0, 'Fair': 0, 'Poor': 0},
        'common_issues': {},
        'recommendations_count': {}
    }
    
    total_score = 0.0
    all_issues = []
    all_recommendations = []
    
    for item in items_data:
        validation_result = validate_item_data(item)
        results.append({
            'item_number': item.get('item_number', 'Unknown'),
            'validation_result': validation_result
        })
        
        total_score += validation_result.score
        
        if validation_result.is_valid:
            summary['compliant_items'] += 1
            
        summary['compliance_distribution'][validation_result.compliance_level] += 1
        
        all_issues.extend(validation_result.issues)
        all_recommendations.extend(validation_result.recommendations)
    
    summary['average_score'] = total_score / len(items_data)
    summary['compliance_rate'] = (summary['compliant_items'] / summary['total_items']) * 100
    
    # Count common issues and recommendations
    from collections import Counter
    summary['common_issues'] = dict(Counter(all_issues).most_common(10))
    summary['recommendations_count'] = dict(Counter(all_recommendations).most_common(10))
    
    return {
        'summary': summary,
        'detailed_results': results,
        'generated_at': datetime.now().isoformat()
    }
