"""
Lightweight NLP Module for Yamama Warehouse AI Agent (Optimized for Render deployment)
Memory-efficient implementation with on-demand model loading and fallback options
"""

import logging
import re
import json
from typing import List, Dict, Tuple, Optional, Any
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Lightweight alternatives only
try:
    import textblob
    from textblob import TextBlob
    textblob_available = True
except ImportError:
    textblob_available = False
    
try:
    from langdetect import detect, LangDetectError
    langdetect_available = True
except ImportError:
    langdetect_available = False
    
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    sklearn_available = True
except ImportError:
    sklearn_available = False

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LightweightNLPProcessor:
    """Memory-efficient NLP processor for production deployment"""
    
    def __init__(self):
        """Initialize with minimal memory footprint"""
        logger.info("Initializing Lightweight NLP Processor...")
        
        # Lazy loading attributes
        self._tfidf_vectorizer = None
        self._warehouse_keywords = None
        self._intent_patterns = None
        
        # Initialize basic components
        self._initialize_basic_patterns()
        
        logger.info("Lightweight NLP Processor initialized successfully")
    
    def _initialize_basic_patterns(self):
        """Initialize basic patterns and keywords"""
        self._warehouse_keywords = {
            'cement_types': ['opc', 'ppc', 'psc', '43', '53', 'ordinary portland', 'pozzolanic'],
            'quality_terms': ['quality', 'grade', 'strength', 'test', 'sample', 'batch', 'compliance'],
            'inventory_terms': ['stock', 'inventory', 'quantity', 'available', 'shortage', 'reorder'],
            'location_terms': ['warehouse', 'section', 'bay', 'rack', 'zone', 'area', 'location'],
            'action_terms': ['check', 'update', 'add', 'remove', 'transfer', 'move', 'analyze']
        }
        
        self._intent_patterns = {
            'inventory_query': r'(?i)(?:how much|quantity|stock|available|inventory).*(?:opc|ppc|psc|cement)',
            'quality_check': r'(?i)(?:quality|grade|test|strength|compliance|batch)',
            'location_query': r'(?i)(?:where|location|section|warehouse|stored)',
            'status_update': r'(?i)(?:update|change|modify|set)',
            'analysis_request': r'(?i)(?:analyze|report|summary|dashboard|statistics)',
            'help_request': r'(?i)(?:help|how to|what is|explain|guide)'
        }
    
    def get_tfidf_vectorizer(self):
        """Lazy loading of TF-IDF vectorizer"""
        if self._tfidf_vectorizer is None and sklearn_available:
            self._tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,  # Limit features for memory
                stop_words='english',
                lowercase=True,
                ngram_range=(1, 2)
            )
        return self._tfidf_vectorizer
    
    def detect_language(self, text: str) -> str:
        """Lightweight language detection"""
        if not langdetect_available:
            # Fallback: simple heuristics
            arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
            if arabic_chars > len(text) * 0.3:
                return 'ar'
            return 'en'
        
        try:
            lang = detect(text)
            return lang if lang in ['ar', 'en'] else 'en'
        except (LangDetectError, Exception):
            return 'en'
    
    def extract_intent(self, text: str) -> Dict[str, Any]:
        """Basic intent recognition using patterns"""
        text_lower = text.lower()
        
        detected_intents = []
        confidence_scores = []
        
        for intent, pattern in self._intent_patterns.items():
            if re.search(pattern, text):
                detected_intents.append(intent)
                # Simple confidence based on pattern match strength
                matches = len(re.findall(pattern, text))
                confidence_scores.append(min(0.9, 0.5 + matches * 0.2))
        
        if not detected_intents:
            detected_intents = ['general_query']
            confidence_scores = [0.3]
        
        return {
            'primary_intent': detected_intents[0],
            'confidence': confidence_scores[0],
            'all_intents': detected_intents,
            'intent_scores': dict(zip(detected_intents, confidence_scores))
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Simple entity extraction using keywords and patterns"""
        entities = {
            'cement_types': [],
            'quantities': [],
            'locations': [],
            'quality_metrics': [],
            'dates': []
        }
        
        text_lower = text.lower()
        
        # Extract cement types
        for cement_type in self._warehouse_keywords['cement_types']:
            if cement_type in text_lower:
                entities['cement_types'].append(cement_type.upper())
        
        # Extract quantities (numbers with units)
        quantity_pattern = r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(kg|ton|tonnes?|bags?|units?)'
        quantities = re.findall(quantity_pattern, text_lower)
        for qty, unit in quantities:
            entities['quantities'].append(f"{qty} {unit}")
        
        # Extract locations
        location_pattern = r'(?:section|bay|rack|zone|area|warehouse)\s*([A-Z0-9-]+)'
        locations = re.findall(location_pattern, text, re.IGNORECASE)
        entities['locations'].extend(locations)
        
        # Extract dates
        date_pattern = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        dates = re.findall(date_pattern, text)
        entities['dates'].extend(dates)
        
        # Clean up empty lists
        return {k: list(set(v)) for k, v in entities.items() if v}
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Lightweight sentiment analysis"""
        if not textblob_available:
            # Fallback: simple keyword-based sentiment
            positive_words = ['good', 'excellent', 'satisfied', 'happy', 'great', 'perfect']
            negative_words = ['bad', 'poor', 'unsatisfied', 'terrible', 'wrong', 'problem']
            
            text_lower = text.lower()
            pos_score = sum(1 for word in positive_words if word in text_lower)
            neg_score = sum(1 for word in negative_words if word in text_lower)
            
            if pos_score > neg_score:
                return {'sentiment': 'positive', 'confidence': 0.6, 'score': 0.3}
            elif neg_score > pos_score:
                return {'sentiment': 'negative', 'confidence': 0.6, 'score': -0.3}
            else:
                return {'sentiment': 'neutral', 'confidence': 0.5, 'score': 0.0}
        
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'confidence': min(abs(polarity) + 0.5, 0.95),
                'score': polarity
            }
        except Exception as e:
            logger.warning(f"Sentiment analysis failed: {e}")
            return {'sentiment': 'neutral', 'confidence': 0.5, 'score': 0.0}
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Basic semantic similarity using TF-IDF"""
        if not sklearn_available:
            # Fallback: Jaccard similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            if not union:
                return 0.0
            
            return len(intersection) / len(union)
        
        try:
            vectorizer = self.get_tfidf_vectorizer()
            if vectorizer is None:
                return 0.0
            
            vectors = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            logger.warning(f"Semantic similarity calculation failed: {e}")
            return 0.0
    
    def extract_warehouse_context(self, text: str) -> Dict[str, Any]:
        """Extract warehouse-specific context"""
        context = {
            'domain': 'warehouse',
            'cement_mentioned': False,
            'inventory_related': False,
            'quality_related': False,
            'location_mentioned': False
        }
        
        text_lower = text.lower()
        
        # Check for cement-related content
        cement_indicators = ['cement', 'opc', 'ppc', 'psc', 'portland', 'pozzolanic']
        context['cement_mentioned'] = any(term in text_lower for term in cement_indicators)
        
        # Check for inventory-related content
        inventory_indicators = ['stock', 'inventory', 'quantity', 'available', 'shortage']
        context['inventory_related'] = any(term in text_lower for term in inventory_indicators)
        
        # Check for quality-related content
        quality_indicators = ['quality', 'grade', 'test', 'strength', 'compliance', 'standard']
        context['quality_related'] = any(term in text_lower for term in quality_indicators)
        
        # Check for location mentions
        location_indicators = ['warehouse', 'section', 'bay', 'rack', 'zone', 'area']
        context['location_mentioned'] = any(term in text_lower for term in location_indicators)
        
        return context
    
    def process_conversation_turn(self, user_input: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Process a single conversation turn with lightweight NLP"""
        if conversation_history is None:
            conversation_history = []
        
        try:
            # Basic processing
            language = self.detect_language(user_input)
            intent_result = self.extract_intent(user_input)
            entities = self.extract_entities(user_input)
            sentiment = self.analyze_sentiment(user_input)
            warehouse_context = self.extract_warehouse_context(user_input)
            
            # Conversation context
            conversation_context = {
                'turn_number': len(conversation_history) + 1,
                'has_history': len(conversation_history) > 0,
                'recent_topics': self._extract_recent_topics(conversation_history[-3:])
            }
            
            return {
                'status': 'success',
                'language': language,
                'intent': intent_result,
                'entities': entities,
                'sentiment': sentiment,
                'warehouse_context': warehouse_context,
                'conversation_context': conversation_context,
                'processing_mode': 'lightweight',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing conversation turn: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'processing_mode': 'lightweight',
                'timestamp': datetime.now().isoformat()
            }
    
    def _extract_recent_topics(self, recent_messages: List[Dict]) -> List[str]:
        """Extract topics from recent conversation"""
        topics = set()
        
        for message in recent_messages:
            text = message.get('text', '').lower()
            
            # Simple topic extraction based on keywords
            for category, keywords in self._warehouse_keywords.items():
                if any(keyword in text for keyword in keywords):
                    topics.add(category.replace('_', ' '))
        
        return list(topics)
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return current NLP capabilities"""
        return {
            'language_detection': langdetect_available,
            'intent_recognition': True,  # Always available with patterns
            'entity_extraction': True,   # Always available with patterns
            'sentiment_analysis': textblob_available,
            'semantic_similarity': sklearn_available,
            'warehouse_context': True,   # Always available
            'conversation_analysis': True,  # Always available
            'advanced_models': False,    # Disabled for memory optimization
            'processing_mode': 'lightweight',
            'memory_optimized': True
        }

# Global instance for the application
lightweight_nlp = LightweightNLPProcessor()

def process_nlp_analysis(text: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
    """Main function for NLP analysis (lightweight version)"""
    return lightweight_nlp.process_conversation_turn(text, conversation_history)

def get_nlp_capabilities() -> Dict[str, Any]:
    """Get current NLP capabilities"""
    return lightweight_nlp.get_capabilities()
