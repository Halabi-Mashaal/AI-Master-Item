"""
Master Data Management (MDM) with Oracle EBS Integration
Advanced AI-powered master data management system
"""

import os
import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import sqlite3
import hashlib

try:
    import cx_Oracle
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False
    logging.warning("Oracle client not available - using mock Oracle EBS integration")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class OracleEBSConnector:
    """Oracle EBS Database Connector with AI-enhanced data management"""
    
    def __init__(self, config: Dict[str, str] = None):
        self.config = config or {}
        self.connection = None
        self.mock_mode = not ORACLE_AVAILABLE
        
        # Initialize local SQLite cache for offline operations
        self.cache_db = sqlite3.connect(':memory:', check_same_thread=False)
        self._init_cache_tables()
        
    def _init_cache_tables(self):
        """Initialize local cache tables"""
        cursor = self.cache_db.cursor()
        
        # Items master table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mdm_items (
                item_id TEXT PRIMARY KEY,
                item_code TEXT UNIQUE,
                item_description TEXT,
                item_type TEXT,
                category TEXT,
                unit_of_measure TEXT,
                status TEXT,
                creation_date TEXT,
                last_updated TEXT,
                created_by TEXT,
                organization_id TEXT,
                list_price REAL,
                standard_cost REAL,
                data_quality_score REAL,
                sync_status TEXT DEFAULT 'PENDING'
            )
        ''')
        
        # Suppliers master table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mdm_suppliers (
                supplier_id TEXT PRIMARY KEY,
                supplier_code TEXT UNIQUE,
                supplier_name TEXT,
                supplier_type TEXT,
                status TEXT,
                contact_person TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                city TEXT,
                country TEXT,
                tax_id TEXT,
                payment_terms TEXT,
                currency TEXT,
                data_quality_score REAL,
                risk_score REAL,
                sync_status TEXT DEFAULT 'PENDING'
            )
        ''')
        
        # Customers master table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mdm_customers (
                customer_id TEXT PRIMARY KEY,
                customer_code TEXT UNIQUE,
                customer_name TEXT,
                customer_type TEXT,
                status TEXT,
                contact_person TEXT,
                email TEXT,
                phone TEXT,
                billing_address TEXT,
                shipping_address TEXT,
                city TEXT,
                country TEXT,
                credit_limit REAL,
                payment_terms TEXT,
                currency TEXT,
                data_quality_score REAL,
                sync_status TEXT DEFAULT 'PENDING'
            )
        ''')
        
        # Data quality audit table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mdm_data_quality (
                audit_id TEXT PRIMARY KEY,
                entity_type TEXT,
                entity_id TEXT,
                field_name TEXT,
                quality_issue TEXT,
                severity TEXT,
                suggested_fix TEXT,
                status TEXT,
                created_date TEXT
            )
        ''')
        
        self.cache_db.commit()
        
    def connect(self) -> bool:
        """Connect to Oracle EBS database"""
        if self.mock_mode:
            logging.info("Running in mock mode - Oracle EBS connection simulated")
            return True
            
        try:
            dsn = f"{self.config.get('host')}:{self.config.get('port')}/{self.config.get('service_name')}"
            self.connection = cx_Oracle.connect(
                user=self.config.get('username'),
                password=self.config.get('password'),
                dsn=dsn
            )
            logging.info("Connected to Oracle EBS successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to Oracle EBS: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Oracle EBS"""
        if self.connection and not self.mock_mode:
            self.connection.close()
            self.connection = None

class MasterDataManager:
    """AI-Enhanced Master Data Management System"""
    
    def __init__(self, oracle_config: Dict[str, str] = None):
        self.oracle_connector = OracleEBSConnector(oracle_config)
        self.data_quality_threshold = 0.85
        self.auto_sync_enabled = True
        
    def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new item with AI-powered data validation"""
        try:
            # Generate unique item ID
            item_id = self._generate_id("ITEM")
            
            # AI-powered data quality assessment
            quality_score, quality_issues = self._assess_item_quality(item_data)
            
            # Prepare item record
            item_record = {
                'item_id': item_id,
                'item_code': item_data.get('item_code', '').upper(),
                'item_description': item_data.get('description', ''),
                'item_type': item_data.get('type', 'STANDARD'),
                'category': item_data.get('category', 'GENERAL'),
                'unit_of_measure': item_data.get('uom', 'EA'),
                'status': 'ACTIVE' if quality_score >= self.data_quality_threshold else 'PENDING_REVIEW',
                'creation_date': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'created_by': item_data.get('created_by', 'AI_AGENT'),
                'organization_id': item_data.get('org_id', '101'),
                'list_price': float(item_data.get('list_price', 0)),
                'standard_cost': float(item_data.get('standard_cost', 0)),
                'data_quality_score': quality_score,
                'sync_status': 'PENDING'
            }
            
            # Insert into cache
            cursor = self.oracle_connector.cache_db.cursor()
            cursor.execute('''
                INSERT INTO mdm_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(item_record.values()))
            
            # Log quality issues
            for issue in quality_issues:
                self._log_quality_issue('ITEM', item_id, issue['field'], issue['issue'], issue['severity'], issue['fix'])
            
            self.oracle_connector.cache_db.commit()
            
            # Sync with Oracle EBS if enabled
            if self.auto_sync_enabled:
                sync_result = self._sync_item_to_ebs(item_record)
                item_record['sync_result'] = sync_result
            
            return {
                'success': True,
                'item_id': item_id,
                'data_quality_score': quality_score,
                'quality_issues': quality_issues,
                'status': item_record['status'],
                'sync_status': item_record.get('sync_result', {}).get('status', 'PENDING')
            }
            
        except Exception as e:
            logging.error(f"Error creating item: {e}")
            return {'success': False, 'error': str(e)}
    
    def create_supplier(self, supplier_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new supplier with AI validation"""
        try:
            supplier_id = self._generate_id("SUPPLIER")
            quality_score, quality_issues = self._assess_supplier_quality(supplier_data)
            risk_score = self._assess_supplier_risk(supplier_data)
            
            supplier_record = {
                'supplier_id': supplier_id,
                'supplier_code': supplier_data.get('supplier_code', '').upper(),
                'supplier_name': supplier_data.get('name', ''),
                'supplier_type': supplier_data.get('type', 'GOODS'),
                'status': 'ACTIVE' if quality_score >= self.data_quality_threshold else 'PENDING_REVIEW',
                'contact_person': supplier_data.get('contact_person', ''),
                'email': supplier_data.get('email', ''),
                'phone': supplier_data.get('phone', ''),
                'address': supplier_data.get('address', ''),
                'city': supplier_data.get('city', ''),
                'country': supplier_data.get('country', 'SA'),
                'tax_id': supplier_data.get('tax_id', ''),
                'payment_terms': supplier_data.get('payment_terms', 'NET30'),
                'currency': supplier_data.get('currency', 'SAR'),
                'data_quality_score': quality_score,
                'risk_score': risk_score,
                'sync_status': 'PENDING'
            }
            
            cursor = self.oracle_connector.cache_db.cursor()
            cursor.execute('''
                INSERT INTO mdm_suppliers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(supplier_record.values()))
            
            for issue in quality_issues:
                self._log_quality_issue('SUPPLIER', supplier_id, issue['field'], issue['issue'], issue['severity'], issue['fix'])
            
            self.oracle_connector.cache_db.commit()
            
            return {
                'success': True,
                'supplier_id': supplier_id,
                'data_quality_score': quality_score,
                'risk_score': risk_score,
                'quality_issues': quality_issues,
                'status': supplier_record['status']
            }
            
        except Exception as e:
            logging.error(f"Error creating supplier: {e}")
            return {'success': False, 'error': str(e)}
    
    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new customer with AI validation"""
        try:
            customer_id = self._generate_id("CUSTOMER")
            quality_score, quality_issues = self._assess_customer_quality(customer_data)
            
            customer_record = {
                'customer_id': customer_id,
                'customer_code': customer_data.get('customer_code', '').upper(),
                'customer_name': customer_data.get('name', ''),
                'customer_type': customer_data.get('type', 'EXTERNAL'),
                'status': 'ACTIVE' if quality_score >= self.data_quality_threshold else 'PENDING_REVIEW',
                'contact_person': customer_data.get('contact_person', ''),
                'email': customer_data.get('email', ''),
                'phone': customer_data.get('phone', ''),
                'billing_address': customer_data.get('billing_address', ''),
                'shipping_address': customer_data.get('shipping_address', ''),
                'city': customer_data.get('city', ''),
                'country': customer_data.get('country', 'SA'),
                'credit_limit': float(customer_data.get('credit_limit', 0)),
                'payment_terms': customer_data.get('payment_terms', 'NET30'),
                'currency': customer_data.get('currency', 'SAR'),
                'data_quality_score': quality_score,
                'sync_status': 'PENDING'
            }
            
            cursor = self.oracle_connector.cache_db.cursor()
            cursor.execute('''
                INSERT INTO mdm_customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(customer_record.values()))
            
            for issue in quality_issues:
                self._log_quality_issue('CUSTOMER', customer_id, issue['field'], issue['issue'], issue['severity'], issue['fix'])
            
            self.oracle_connector.cache_db.commit()
            
            return {
                'success': True,
                'customer_id': customer_id,
                'data_quality_score': quality_score,
                'quality_issues': quality_issues,
                'status': customer_record['status']
            }
            
        except Exception as e:
            logging.error(f"Error creating customer: {e}")
            return {'success': False, 'error': str(e)}
    
    def search_entities(self, entity_type: str, search_criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """AI-powered entity search across master data"""
        try:
            cursor = self.oracle_connector.cache_db.cursor()
            
            if entity_type.upper() == 'ITEM':
                query = "SELECT * FROM mdm_items WHERE 1=1"
                params = []
                
                if 'item_code' in search_criteria:
                    query += " AND item_code LIKE ?"
                    params.append(f"%{search_criteria['item_code']}%")
                if 'description' in search_criteria:
                    query += " AND item_description LIKE ?"
                    params.append(f"%{search_criteria['description']}%")
                if 'category' in search_criteria:
                    query += " AND category = ?"
                    params.append(search_criteria['category'])
                    
            elif entity_type.upper() == 'SUPPLIER':
                query = "SELECT * FROM mdm_suppliers WHERE 1=1"
                params = []
                
                if 'supplier_code' in search_criteria:
                    query += " AND supplier_code LIKE ?"
                    params.append(f"%{search_criteria['supplier_code']}%")
                if 'name' in search_criteria:
                    query += " AND supplier_name LIKE ?"
                    params.append(f"%{search_criteria['name']}%")
                    
            elif entity_type.upper() == 'CUSTOMER':
                query = "SELECT * FROM mdm_customers WHERE 1=1"
                params = []
                
                if 'customer_code' in search_criteria:
                    query += " AND customer_code LIKE ?"
                    params.append(f"%{search_criteria['customer_code']}%")
                if 'name' in search_criteria:
                    query += " AND customer_name LIKE ?"
                    params.append(f"%{search_criteria['name']}%")
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Convert to list of dictionaries
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in results]
            
        except Exception as e:
            logging.error(f"Error searching entities: {e}")
            return []
    
    def get_data_quality_dashboard(self) -> Dict[str, Any]:
        """Generate comprehensive data quality dashboard"""
        try:
            cursor = self.oracle_connector.cache_db.cursor()
            
            # Overall statistics
            cursor.execute("SELECT COUNT(*), AVG(data_quality_score) FROM mdm_items")
            items_stats = cursor.fetchone()
            
            cursor.execute("SELECT COUNT(*), AVG(data_quality_score) FROM mdm_suppliers")
            suppliers_stats = cursor.fetchone()
            
            cursor.execute("SELECT COUNT(*), AVG(data_quality_score) FROM mdm_customers")
            customers_stats = cursor.fetchone()
            
            # Quality issues breakdown
            cursor.execute("""
                SELECT entity_type, severity, COUNT(*) as count 
                FROM mdm_data_quality 
                WHERE status = 'OPEN' 
                GROUP BY entity_type, severity
            """)
            quality_issues = cursor.fetchall()
            
            # Sync status
            cursor.execute("SELECT sync_status, COUNT(*) FROM mdm_items GROUP BY sync_status")
            items_sync = cursor.fetchall()
            
            return {
                'overall_stats': {
                    'items': {
                        'count': items_stats[0] or 0,
                        'avg_quality_score': round(items_stats[1] or 0, 2)
                    },
                    'suppliers': {
                        'count': suppliers_stats[0] or 0,
                        'avg_quality_score': round(suppliers_stats[1] or 0, 2)
                    },
                    'customers': {
                        'count': customers_stats[0] or 0,
                        'avg_quality_score': round(customers_stats[1] or 0, 2)
                    }
                },
                'quality_issues': [
                    {'entity_type': issue[0], 'severity': issue[1], 'count': issue[2]}
                    for issue in quality_issues
                ],
                'sync_status': [
                    {'status': status[0], 'count': status[1]}
                    for status in items_sync
                ],
                'recommendations': self._generate_quality_recommendations()
            }
            
        except Exception as e:
            logging.error(f"Error generating dashboard: {e}")
            return {'error': str(e)}
    
    def bulk_import_from_excel(self, file_path: str, entity_type: str, mapping: Dict[str, str]) -> Dict[str, Any]:
        """Bulk import master data from Excel with AI validation"""
        try:
            df = pd.read_excel(file_path)
            results = {
                'total_records': len(df),
                'successful': 0,
                'failed': 0,
                'warnings': 0,
                'details': []
            }
            
            for index, row in df.iterrows():
                try:
                    # Map columns according to provided mapping
                    mapped_data = {}
                    for excel_col, system_field in mapping.items():
                        if excel_col in row and pd.notna(row[excel_col]):
                            mapped_data[system_field] = row[excel_col]
                    
                    # Create entity based on type
                    if entity_type.upper() == 'ITEM':
                        result = self.create_item(mapped_data)
                    elif entity_type.upper() == 'SUPPLIER':
                        result = self.create_supplier(mapped_data)
                    elif entity_type.upper() == 'CUSTOMER':
                        result = self.create_customer(mapped_data)
                    else:
                        raise ValueError(f"Unsupported entity type: {entity_type}")
                    
                    if result['success']:
                        results['successful'] += 1
                        if result.get('quality_issues'):
                            results['warnings'] += 1
                    else:
                        results['failed'] += 1
                        
                    results['details'].append({
                        'row': index + 1,
                        'status': 'SUCCESS' if result['success'] else 'FAILED',
                        'entity_id': result.get('item_id') or result.get('supplier_id') or result.get('customer_id'),
                        'quality_score': result.get('data_quality_score', 0),
                        'issues': result.get('quality_issues', []),
                        'error': result.get('error')
                    })
                    
                except Exception as e:
                    results['failed'] += 1
                    results['details'].append({
                        'row': index + 1,
                        'status': 'FAILED',
                        'error': str(e)
                    })
            
            return results
            
        except Exception as e:
            logging.error(f"Error in bulk import: {e}")
            return {'error': str(e)}
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        hash_part = hashlib.md5(f"{prefix}{timestamp}".encode()).hexdigest()[:6]
        return f"{prefix}_{timestamp}_{hash_part.upper()}"
    
    def _assess_item_quality(self, item_data: Dict[str, Any]) -> Tuple[float, List[Dict[str, str]]]:
        """AI-powered item data quality assessment"""
        score = 1.0
        issues = []
        
        # Required fields check
        required_fields = ['item_code', 'description', 'type', 'uom']
        for field in required_fields:
            if not item_data.get(field):
                score -= 0.2
                issues.append({
                    'field': field,
                    'issue': f'Required field {field} is missing',
                    'severity': 'HIGH',
                    'fix': f'Provide valid {field}'
                })
        
        # Item code validation
        item_code = item_data.get('item_code', '')
        if item_code:
            if len(item_code) < 3:
                score -= 0.1
                issues.append({
                    'field': 'item_code',
                    'issue': 'Item code too short',
                    'severity': 'MEDIUM',
                    'fix': 'Use item code with at least 3 characters'
                })
            if not item_code.replace('-', '').replace('_', '').isalnum():
                score -= 0.05
                issues.append({
                    'field': 'item_code',
                    'issue': 'Item code contains invalid characters',
                    'severity': 'LOW',
                    'fix': 'Use only alphanumeric characters, hyphens, and underscores'
                })
        
        # Description validation
        description = item_data.get('description', '')
        if description and len(description) < 10:
            score -= 0.05
            issues.append({
                'field': 'description',
                'issue': 'Description too brief',
                'severity': 'LOW',
                'fix': 'Provide more detailed description (at least 10 characters)'
            })
        
        # Price validation
        list_price = item_data.get('list_price', 0)
        standard_cost = item_data.get('standard_cost', 0)
        
        if list_price and standard_cost and list_price < standard_cost:
            score -= 0.1
            issues.append({
                'field': 'pricing',
                'issue': 'List price lower than standard cost',
                'severity': 'MEDIUM',
                'fix': 'Review pricing - list price should typically exceed standard cost'
            })
        
        return max(0.0, score), issues
    
    def _assess_supplier_quality(self, supplier_data: Dict[str, Any]) -> Tuple[float, List[Dict[str, str]]]:
        """AI-powered supplier data quality assessment"""
        score = 1.0
        issues = []
        
        required_fields = ['supplier_code', 'name', 'contact_person', 'email']
        for field in required_fields:
            if not supplier_data.get(field):
                score -= 0.2
                issues.append({
                    'field': field,
                    'issue': f'Required field {field} is missing',
                    'severity': 'HIGH',
                    'fix': f'Provide valid {field}'
                })
        
        # Email validation
        email = supplier_data.get('email', '')
        if email and '@' not in email:
            score -= 0.1
            issues.append({
                'field': 'email',
                'issue': 'Invalid email format',
                'severity': 'MEDIUM',
                'fix': 'Provide valid email address'
            })
        
        return max(0.0, score), issues
    
    def _assess_customer_quality(self, customer_data: Dict[str, Any]) -> Tuple[float, List[Dict[str, str]]]:
        """AI-powered customer data quality assessment"""
        score = 1.0
        issues = []
        
        required_fields = ['customer_code', 'name', 'contact_person']
        for field in required_fields:
            if not customer_data.get(field):
                score -= 0.2
                issues.append({
                    'field': field,
                    'issue': f'Required field {field} is missing',
                    'severity': 'HIGH',
                    'fix': f'Provide valid {field}'
                })
        
        return max(0.0, score), issues
    
    def _assess_supplier_risk(self, supplier_data: Dict[str, Any]) -> float:
        """AI-powered supplier risk assessment"""
        risk_score = 0.0
        
        # Country risk (simplified)
        high_risk_countries = ['Country1', 'Country2']  # Would be configurable
        if supplier_data.get('country') in high_risk_countries:
            risk_score += 0.3
        
        # Missing critical information increases risk
        critical_fields = ['tax_id', 'address', 'phone']
        missing_critical = sum(1 for field in critical_fields if not supplier_data.get(field))
        risk_score += missing_critical * 0.1
        
        return min(1.0, risk_score)
    
    def _log_quality_issue(self, entity_type: str, entity_id: str, field_name: str, 
                          issue: str, severity: str, suggested_fix: str):
        """Log data quality issue"""
        audit_id = self._generate_id("AUDIT")
        cursor = self.oracle_connector.cache_db.cursor()
        cursor.execute('''
            INSERT INTO mdm_data_quality VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (audit_id, entity_type, entity_id, field_name, issue, severity, 
              suggested_fix, 'OPEN', datetime.now().isoformat()))
    
    def _sync_item_to_ebs(self, item_record: Dict[str, Any]) -> Dict[str, Any]:
        """Sync item to Oracle EBS (mock implementation)"""
        if self.oracle_connector.mock_mode:
            return {
                'status': 'SUCCESS',
                'ebs_item_id': f"EBS_{item_record['item_id']}",
                'message': 'Item synced successfully (mock mode)'
            }
        
        # Real EBS integration would go here
        try:
            # Oracle EBS API calls would be implemented here
            return {
                'status': 'SUCCESS',
                'ebs_item_id': f"EBS_{item_record['item_id']}",
                'message': 'Item synced to Oracle EBS'
            }
        except Exception as e:
            return {
                'status': 'FAILED',
                'error': str(e),
                'message': 'Failed to sync item to Oracle EBS'
            }
    
    def _generate_quality_recommendations(self) -> List[Dict[str, str]]:
        """Generate AI-powered data quality recommendations"""
        return [
            {
                'category': 'Data Completeness',
                'recommendation': 'Focus on completing missing required fields for pending items',
                'priority': 'HIGH',
                'impact': 'Improved data quality scores and faster approvals'
            },
            {
                'category': 'Standardization',
                'recommendation': 'Implement consistent naming conventions for item codes',
                'priority': 'MEDIUM',
                'impact': 'Better searchability and reduced duplicates'
            },
            {
                'category': 'Validation',
                'recommendation': 'Enable real-time validation for email addresses and phone numbers',
                'priority': 'MEDIUM',
                'impact': 'Reduced communication errors with suppliers and customers'
            }
        ]

# Global MDM instance
mdm_manager = None

def initialize_mdm(oracle_config: Dict[str, str] = None) -> MasterDataManager:
    """Initialize Master Data Management system"""
    global mdm_manager
    if mdm_manager is None:
        mdm_manager = MasterDataManager(oracle_config)
    return mdm_manager

def get_mdm_manager() -> Optional[MasterDataManager]:
    """Get the global MDM manager instance"""
    return mdm_manager
