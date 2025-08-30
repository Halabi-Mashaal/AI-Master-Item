"""
Fallback Advanced NLP Module - Empty implementations for compatibility
This module provides empty implementations of advanced NLP functions
to maintain compatibility when heavy libraries are not available.
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Mock NLP processor for compatibility
class MockNLPProcessor:
    def __init__(self):
        self.nlp_model = None
        self.intent_classifier = None 
        self.sentiment_analyzer = None
        self.semantic_model = None
        self.warehouse_entities = {
            "materials": ["cement", "opc", "ppc", "psc"],
            "locations": ["warehouse", "section", "bay"],
            "specifications": ["43", "53", "grade"],
            "operations": ["stock", "quality", "test"]
        }

# Create mock processor instance
nlp_processor = MockNLPProcessor()

def process_user_query(text: str, language: str = 'en') -> Dict[str, Any]:
    """Mock implementation - returns basic structure"""
    logger.warning("Using fallback NLP - advanced features disabled")
    
    return {
        'intent': {
            'intent': 'general',
            'confidence': 0.3
        },
        'entities': {
            'materials': [],
            'locations': [],
            'quantities': []
        },
        'sentiment': {
            'classification': 'neutral',
            'confidence': 0.5
        },
        'language': {
            'detected': {
                'language': language,
                'confidence': 0.5
            }
        },
        'confidence_score': 0.3,
        'processing_mode': 'fallback'
    }

def analyze_conversation_history(history: List[Dict]) -> Dict[str, Any]:
    """Mock conversation analysis"""
    logger.warning("Using fallback conversation analysis")
    
    return {
        "conversation_summary": {
            "total_turns": len(history),
            "sentiment_trend": "neutral",
            "user_satisfaction": 0.5
        },
        "key_insights": [
            "Fallback mode active - limited analysis available",
            f"Processed {len(history)} conversation turns"
        ],
        "processing_mode": "fallback"
    }

def extract_warehouse_intelligence(texts: List[str]) -> Dict[str, Any]:
    """Mock warehouse intelligence extraction"""
    logger.warning("Using fallback warehouse intelligence")
    
    return {
        "warehouse_context": {
            "cement_mentioned": any("cement" in text.lower() for text in texts),
            "inventory_related": any("stock" in text.lower() for text in texts)
        },
        "processing_mode": "fallback"
    }
