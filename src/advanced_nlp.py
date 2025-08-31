"""
Advanced NLP Module for Yamama Warehouse AI Agent
Implements comprehensive natural language processing capabilities including:
- Intent Recognition using spaCy and Transformers
- Named Entity Recognition for warehouse items/locations
- Semantic similarity for better query matching
- Advanced sentiment analysis with ML models
- Text summarization for conversation history
- Topic modeling using LDA and BERT
- Language detection (automatic)
- Conversation flow analysis
- Specialized Warehouse NLP features
"""

import logging
import re
import json
from typing import List, Dict, Tuple, Optional, Any
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Core NLP Libraries
try:
    import spacy
    from spacy.matcher import Matcher
    from spacy.util import filter_spans
    spacy_available = True
except ImportError:
    spacy_available = False
    logging.warning("spaCy not available - basic NLP will be used")

try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    import torch
    transformers_available = True
except ImportError:
    transformers_available = False
    logging.warning("Transformers not available - advanced ML features disabled")

try:
    from sentence_transformers import SentenceTransformer
    sentence_transformers_available = True
except ImportError:
    sentence_transformers_available = False
    logging.warning("SentenceTransformers not available - semantic similarity disabled")

try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
    from nltk.corpus import stopwords
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.stem import WordNetLemmatizer
    nltk_available = True
except ImportError:
    nltk_available = False
    logging.warning("NLTK not available - sentiment analysis limited")

try:
    from textblob import TextBlob
    textblob_available = True
except ImportError:
    textblob_available = False
    logging.warning("TextBlob not available - basic text processing only")

try:
    from langdetect import detect, detect_langs
    langdetect_available = True
except ImportError:
    langdetect_available = False
    logging.warning("langdetect not available - language detection disabled")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    from sklearn.decomposition import LatentDirichletAllocation
    from sklearn.metrics.pairwise import cosine_similarity
    sklearn_available = True
except ImportError:
    sklearn_available = False
    logging.warning("scikit-learn not available - ML features disabled")

try:
    from gensim import corpora, models
    from gensim.models import LdaModel
    gensim_available = True
except ImportError:
    gensim_available = False
    logging.warning("Gensim not available - advanced topic modeling disabled, using scikit-learn fallback")

import numpy as np
import pandas as pd
import os


class AdvancedNLPProcessor:
    """Advanced NLP processor with comprehensive warehouse-specific features"""
    
    def __init__(self):
        """Initialize all NLP models and processors"""
        self.logger = logging.getLogger(__name__)
        
        # Check for lightweight mode
        self.use_lightweight_nlp = os.getenv('USE_LIGHTWEIGHT_NLP', '0') == '1'
        self.disable_heavy_models = os.getenv('DISABLE_HEAVY_MODELS', '0') == '1'
        
        if self.use_lightweight_nlp or self.disable_heavy_models:
            self.logger.info("Lightweight NLP mode enabled - skipping heavy model loading")
        
        # Initialize models
        self.nlp_model = None
        self.sentiment_analyzer = None
        self.language_detector = None
        self.semantic_model = None
        self.intent_classifier = None
        self.entity_matcher = None
        self.conversation_analyzer = None
        
        # Warehouse-specific patterns and entities
        self.warehouse_entities = self._init_warehouse_entities()
        self.intent_patterns = self._init_intent_patterns()
        self.location_patterns = self._init_location_patterns()
        self.quantity_patterns = self._init_quantity_patterns()
        
        # Initialize models
        self._load_models()
        
    def _load_models(self):
        """Load all available NLP models"""
        try:
            # Skip heavy model loading in lightweight mode
            if self.use_lightweight_nlp or self.disable_heavy_models:
                self.logger.info("Skipping heavy NLP model loading due to lightweight mode")
                return
                
            # Load spaCy model
            if spacy_available:
                try:
                    self.nlp_model = spacy.load("en_core_web_sm")
                    self.entity_matcher = Matcher(self.nlp_model.vocab)
                    self._setup_custom_patterns()
                    self.logger.info("spaCy model loaded successfully")
                except OSError:
                    self.logger.warning("spaCy model not found, using basic processing")
            
            # Load sentiment analyzer
            if nltk_available:
                try:
                    self.sentiment_analyzer = SentimentIntensityAnalyzer()
                    self.lemmatizer = WordNetLemmatizer()
                    self.logger.info("NLTK sentiment analyzer loaded")
                except:
                    self.logger.warning("NLTK data not available")
            
            # Load semantic similarity model
            if sentence_transformers_available:
                try:
                    self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
                    self.logger.info("Sentence transformer model loaded")
                except:
                    self.logger.warning("Could not load sentence transformer model")
            
            # Load intent classification pipeline
            if transformers_available:
                try:
                    self.intent_classifier = pipeline(
                        "text-classification",
                        model="microsoft/DialoGPT-medium",
                        return_all_scores=True
                    )
                    self.logger.info("Intent classifier loaded")
                except:
                    self.logger.warning("Could not load intent classifier")
                    
        except Exception as e:
            self.logger.error(f"Error loading NLP models: {e}")
    
    def _init_warehouse_entities(self) -> Dict[str, List[str]]:
        """Initialize warehouse-specific entities"""
        return {
            "materials": [
                "steel", "concrete", "rebar", "cement", "aggregate", "sand", "gravel",
                "aluminum", "copper", "iron", "stainless steel", "carbon steel",
                "galvanized steel", "structural steel", "reinforcement bar",
                "wire mesh", "pipes", "fittings", "valves", "flanges"
            ],
            "specifications": [
                "grade", "strength", "diameter", "length", "width", "thickness",
                "weight", "density", "compression strength", "tensile strength",
                "yield strength", "modulus", "hardness", "ductility"
            ],
            "locations": [
                "warehouse", "storage", "section", "aisle", "rack", "shelf",
                "bay", "zone", "area", "floor", "level", "building", "facility"
            ],
            "quantities": [
                "ton", "tons", "kg", "kilogram", "pound", "meter", "feet",
                "piece", "pieces", "unit", "units", "roll", "sheet", "bar"
            ],
            "operations": [
                "inventory", "stock", "delivery", "shipment", "order", "purchase",
                "supply", "procurement", "logistics", "storage", "handling"
            ]
        }
    
    def _init_intent_patterns(self) -> Dict[str, List[str]]:
        """Initialize intent classification patterns"""
        return {
            "inventory_inquiry": [
                "what is in stock", "check inventory", "available quantity",
                "how much do we have", "stock level", "current stock"
            ],
            "product_search": [
                "find product", "search for", "looking for", "need material",
                "where is", "locate item", "product information"
            ],
            "specification_query": [
                "specifications", "properties", "strength", "grade",
                "technical details", "material properties", "characteristics"
            ],
            "pricing_inquiry": [
                "price", "cost", "how much", "rate", "pricing", "quotation",
                "estimate", "budget", "expense"
            ],
            "delivery_status": [
                "delivery", "shipment", "when will arrive", "tracking",
                "order status", "expected date", "shipping"
            ],
            "comparison_request": [
                "compare", "difference", "versus", "better", "best option",
                "which one", "alternative", "substitute"
            ]
        }
    
    def _init_location_patterns(self) -> List[str]:
        """Initialize location extraction patterns"""
        return [
            r"(warehouse|section|aisle|rack|shelf|bay|zone)\s*([A-Z]?\d+[A-Z]?)",
            r"(floor|level)\s*(\d+)",
            r"(building|facility)\s*([A-Z]+\d*)",
            r"(row|column)\s*(\d+)",
            r"(area|region)\s*([A-Z]+)"
        ]
    
    def _init_quantity_patterns(self) -> List[str]:
        """Initialize quantity extraction patterns"""
        return [
            r"(\d+\.?\d*)\s*(tons?|kg|kilograms?|pounds?|lbs?)",
            r"(\d+\.?\d*)\s*(meters?|feet|ft|inches?|in)",
            r"(\d+)\s*(pieces?|units?|items?|rolls?|sheets?|bars?)",
            r"(\d+\.?\d*)\s*(%|percent|percentage)"
        ]
    
    def _setup_custom_patterns(self):
        """Setup custom entity patterns for spaCy matcher"""
        if not self.entity_matcher or not self.nlp_model:
            return
        
        # Material patterns
        material_patterns = []
        for material in self.warehouse_entities["materials"]:
            material_patterns.append([{"LOWER": word} for word in material.lower().split()])
        
        self.entity_matcher.add("MATERIAL", material_patterns)
        
        # Location patterns
        location_patterns = [
            [{"LOWER": {"IN": ["warehouse", "section", "aisle"]}},
             {"IS_ALPHA": True, "IS_UPPER": True, "LENGTH": {">=": 1}}],
            [{"LOWER": {"IN": ["rack", "shelf", "bay"]}},
             {"IS_DIGIT": True}]
        ]
        self.entity_matcher.add("LOCATION", location_patterns)
        
        # Quantity patterns
        quantity_patterns = [
            [{"IS_DIGIT": True},
             {"LOWER": {"IN": ["tons", "ton", "kg", "pieces", "units"]}}]
        ]
        self.entity_matcher.add("QUANTITY", quantity_patterns)
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language of input text"""
        if not langdetect_available or not text.strip():
            return {"language": "en", "confidence": 0.5}
        
        try:
            # Detect primary language
            primary_lang = detect(text)
            
            # Get confidence scores for multiple languages
            lang_probs = detect_langs(text)
            
            result = {
                "language": primary_lang,
                "confidence": max([prob.prob for prob in lang_probs]),
                "alternatives": [{"lang": prob.lang, "confidence": prob.prob} 
                              for prob in lang_probs[:3]]
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Language detection error: {e}")
            return {"language": "en", "confidence": 0.5}
    
    def extract_entities(self, text: str) -> Dict[str, List[Dict]]:
        """Extract named entities from text"""
        entities = {
            "materials": [],
            "locations": [],
            "quantities": [],
            "specifications": [],
            "operations": []
        }
        
        try:
            # spaCy NER
            if self.nlp_model:
                doc = self.nlp_model(text)
                
                # Built-in entities
                for ent in doc.ents:
                    if ent.label_ in ["ORG", "GPE", "FAC"]:
                        entities["locations"].append({
                            "text": ent.text,
                            "label": ent.label_,
                            "start": ent.start_char,
                            "end": ent.end_char,
                            "confidence": 0.8
                        })
                    elif ent.label_ in ["QUANTITY", "CARDINAL"]:
                        entities["quantities"].append({
                            "text": ent.text,
                            "label": ent.label_,
                            "start": ent.start_char,
                            "end": ent.end_char,
                            "confidence": 0.8
                        })
                
                # Custom entity matching
                if self.entity_matcher:
                    matches = self.entity_matcher(doc)
                    spans = [doc[start:end] for _, start, end in matches]
                    spans = filter_spans(spans)
                    
                    for span in spans:
                        entity_type = self.nlp_model.vocab.strings[matches[0][0]].lower()
                        if entity_type in entities:
                            entities[entity_type].append({
                                "text": span.text,
                                "label": entity_type.upper(),
                                "start": span.start_char,
                                "end": span.end_char,
                                "confidence": 0.9
                            })
            
            # Regex-based extraction for warehouse-specific patterns
            self._extract_warehouse_entities(text, entities)
            
        except Exception as e:
            self.logger.error(f"Entity extraction error: {e}")
        
        return entities
    
    def _extract_warehouse_entities(self, text: str, entities: Dict):
        """Extract warehouse-specific entities using regex patterns"""
        text_lower = text.lower()
        
        # Extract locations
        for pattern in self.location_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities["locations"].append({
                    "text": match.group(),
                    "label": "WAREHOUSE_LOCATION",
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.85,
                    "location_type": match.group(1),
                    "identifier": match.group(2) if match.lastindex > 1 else None
                })
        
        # Extract quantities
        for pattern in self.quantity_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities["quantities"].append({
                    "text": match.group(),
                    "label": "QUANTITY",
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.9,
                    "value": float(match.group(1)),
                    "unit": match.group(2)
                })
        
        # Extract materials by keyword matching
        for material in self.warehouse_entities["materials"]:
            if material.lower() in text_lower:
                start_idx = text_lower.find(material.lower())
                entities["materials"].append({
                    "text": material,
                    "label": "MATERIAL",
                    "start": start_idx,
                    "end": start_idx + len(material),
                    "confidence": 0.8
                })
    
    def classify_intent(self, text: str) -> Dict[str, Any]:
        """Classify user intent from text"""
        try:
            # Rule-based intent classification
            text_lower = text.lower()
            intent_scores = {}
            
            for intent, patterns in self.intent_patterns.items():
                score = 0
                for pattern in patterns:
                    if pattern.lower() in text_lower:
                        score += 1
                if score > 0:
                    intent_scores[intent] = score / len(patterns)
            
            if intent_scores:
                primary_intent = max(intent_scores.items(), key=lambda x: x[1])
                
                result = {
                    "intent": primary_intent[0],
                    "confidence": primary_intent[1],
                    "all_scores": intent_scores
                }
            else:
                result = {
                    "intent": "general_inquiry",
                    "confidence": 0.3,
                    "all_scores": {"general_inquiry": 0.3}
                }
            
            # Enhanced classification with transformers if available
            if transformers_available and self.intent_classifier:
                try:
                    transformer_result = self.intent_classifier(text)
                    result["transformer_analysis"] = transformer_result
                except:
                    pass
            
            return result
            
        except Exception as e:
            self.logger.error(f"Intent classification error: {e}")
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "all_scores": {}
            }
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Advanced sentiment analysis using multiple methods"""
        sentiment_result = {
            "compound_score": 0.0,
            "positive": 0.0,
            "negative": 0.0,
            "neutral": 0.0,
            "classification": "neutral",
            "confidence": 0.0
        }
        
        try:
            # NLTK VADER sentiment
            if self.sentiment_analyzer:
                vader_scores = self.sentiment_analyzer.polarity_scores(text)
                sentiment_result.update({
                    "compound_score": vader_scores["compound"],
                    "positive": vader_scores["pos"],
                    "negative": vader_scores["neg"],
                    "neutral": vader_scores["neu"]
                })
            
            # TextBlob sentiment
            if textblob_available:
                blob = TextBlob(text)
                textblob_polarity = blob.sentiment.polarity
                textblob_subjectivity = blob.sentiment.subjectivity
                
                sentiment_result["textblob"] = {
                    "polarity": textblob_polarity,
                    "subjectivity": textblob_subjectivity
                }
            
            # Determine final classification
            compound = sentiment_result["compound_score"]
            if compound >= 0.05:
                sentiment_result["classification"] = "positive"
                sentiment_result["confidence"] = abs(compound)
            elif compound <= -0.05:
                sentiment_result["classification"] = "negative"
                sentiment_result["confidence"] = abs(compound)
            else:
                sentiment_result["classification"] = "neutral"
                sentiment_result["confidence"] = 1 - abs(compound)
            
        except Exception as e:
            self.logger.error(f"Sentiment analysis error: {e}")
        
        return sentiment_result
    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        try:
            if self.semantic_model and sentence_transformers_available:
                # Using sentence transformers
                embeddings = self.semantic_model.encode([text1, text2])
                similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
                return float(similarity)
            
            elif sklearn_available:
                # Fallback to TF-IDF similarity
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform([text1, text2])
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                return float(similarity)
            
        except Exception as e:
            self.logger.error(f"Semantic similarity error: {e}")
        
        return 0.0
    
    def summarize_conversation(self, conversation_history: List[Dict], max_length: int = 200) -> str:
        """Summarize conversation history using extractive summarization"""
        try:
            if not conversation_history:
                return "No conversation history available."
            
            # Combine all messages
            all_text = []
            for msg in conversation_history[-10:]:  # Last 10 messages
                user_input = msg.get('user_input', '')
                ai_response = msg.get('ai_response', '')
                if user_input:
                    all_text.append(f"User: {user_input}")
                if ai_response:
                    all_text.append(f"AI: {ai_response}")
            
            if not all_text:
                return "No meaningful conversation content found."
            
            full_text = ' '.join(all_text)
            
            if len(full_text) <= max_length:
                return full_text
            
            # Extractive summarization using sentence ranking
            if self.nlp_model and spacy_available:
                doc = self.nlp_model(full_text)
                sentences = [sent.text for sent in doc.sents]
                
                if len(sentences) <= 3:
                    return ' '.join(sentences)
                
                # Simple sentence ranking by length and keyword presence
                important_words = ['inventory', 'stock', 'material', 'warehouse', 'delivery', 'price']
                scored_sentences = []
                
                for sent in sentences:
                    score = len(sent.split())  # Base score on length
                    for word in important_words:
                        if word.lower() in sent.lower():
                            score += 10
                    scored_sentences.append((sent, score))
                
                # Select top sentences
                scored_sentences.sort(key=lambda x: x[1], reverse=True)
                top_sentences = [sent[0] for sent in scored_sentences[:3]]
                
                summary = ' '.join(top_sentences)
                if len(summary) > max_length:
                    summary = summary[:max_length] + "..."
                
                return summary
            
            # Fallback: simple truncation
            return full_text[:max_length] + "..." if len(full_text) > max_length else full_text
            
        except Exception as e:
            self.logger.error(f"Conversation summarization error: {e}")
            return "Error generating conversation summary."
    
    def topic_modeling(self, texts: List[str], num_topics: int = 5) -> Dict[str, Any]:
        """Perform topic modeling on a collection of texts"""
        try:
            if not texts or len(texts) < 2:
                return {"topics": [], "error": "Insufficient text data"}
            
            # Preprocess texts
            processed_texts = []
            if self.nlp_model and spacy_available:
                for text in texts:
                    doc = self.nlp_model(text)
                    tokens = [token.lemma_.lower() for token in doc 
                             if not token.is_stop and not token.is_punct 
                             and token.is_alpha and len(token.text) > 2]
                    processed_texts.append(tokens)
            else:
                # Fallback preprocessing
                for text in texts:
                    tokens = text.lower().split()
                    processed_texts.append(tokens)
            
            # LDA with Gensim
            if gensim_available and processed_texts:
                dictionary = corpora.Dictionary(processed_texts)
                corpus = [dictionary.doc2bow(text) for text in processed_texts]
                
                if len(corpus) < num_topics:
                    num_topics = len(corpus)
                
                lda_model = LdaModel(
                    corpus=corpus,
                    id2word=dictionary,
                    num_topics=num_topics,
                    random_state=42,
                    passes=10,
                    alpha='auto',
                    per_word_topics=True
                )
                
                topics = []
                for idx, topic in lda_model.print_topics():
                    topic_words = []
                    word_scores = topic.split(' + ')
                    for word_score in word_scores:
                        score, word = word_score.split('*')
                        word = word.strip('"')
                        topic_words.append({
                            "word": word,
                            "score": float(score)
                        })
                    
                    topics.append({
                        "id": idx,
                        "words": topic_words[:5],  # Top 5 words
                        "description": f"Topic {idx + 1}"
                    })
                
                return {
                    "topics": topics,
                    "num_topics": num_topics,
                    "model_type": "LDA",
                    "coherence": "Not calculated"
                }
            
            # Fallback: simple keyword extraction
            elif sklearn_available:
                all_text = ' '.join(texts)
                vectorizer = TfidfVectorizer(max_features=20, stop_words='english')
                tfidf_matrix = vectorizer.fit_transform([all_text])
                feature_names = vectorizer.get_feature_names_out()
                tfidf_scores = tfidf_matrix.toarray()[0]
                
                word_scores = list(zip(feature_names, tfidf_scores))
                word_scores.sort(key=lambda x: x[1], reverse=True)
                
                topics = [{
                    "id": 0,
                    "words": [{"word": word, "score": score} for word, score in word_scores[:10]],
                    "description": "Main Topic"
                }]
                
                return {
                    "topics": topics,
                    "num_topics": 1,
                    "model_type": "TF-IDF",
                    "coherence": "Not calculated"
                }
            
        except Exception as e:
            self.logger.error(f"Topic modeling error: {e}")
        
        return {"topics": [], "error": "Topic modeling failed"}
    
    def analyze_conversation_flow(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Analyze conversation flow and patterns"""
        try:
            if not conversation_history:
                return {"error": "No conversation history"}
            
            analysis = {
                "total_exchanges": len(conversation_history),
                "conversation_duration": None,
                "intent_progression": [],
                "topic_shifts": [],
                "user_engagement": {
                    "average_message_length": 0,
                    "question_ratio": 0,
                    "sentiment_trend": []
                },
                "ai_performance": {
                    "response_relevance": [],
                    "response_length_trend": []
                }
            }
            
            # Calculate conversation duration
            if conversation_history:
                first_msg = conversation_history[0]
                last_msg = conversation_history[-1]
                if 'timestamp' in first_msg and 'timestamp' in last_msg:
                    try:
                        first_time = datetime.fromisoformat(first_msg['timestamp'])
                        last_time = datetime.fromisoformat(last_msg['timestamp'])
                        duration = last_time - first_time
                        analysis["conversation_duration"] = str(duration)
                    except:
                        pass
            
            # Analyze intent progression
            previous_intent = None
            for msg in conversation_history:
                user_input = msg.get('user_input', '')
                if user_input:
                    intent_result = self.classify_intent(user_input)
                    current_intent = intent_result['intent']
                    
                    analysis["intent_progression"].append({
                        "intent": current_intent,
                        "confidence": intent_result['confidence'],
                        "timestamp": msg.get('timestamp')
                    })
                    
                    if previous_intent and previous_intent != current_intent:
                        analysis["topic_shifts"].append({
                            "from": previous_intent,
                            "to": current_intent,
                            "timestamp": msg.get('timestamp')
                        })
                    
                    previous_intent = current_intent
            
            # User engagement metrics
            user_messages = [msg.get('user_input', '') for msg in conversation_history if msg.get('user_input')]
            if user_messages:
                total_length = sum(len(msg.split()) for msg in user_messages)
                analysis["user_engagement"]["average_message_length"] = total_length / len(user_messages)
                
                questions = sum(1 for msg in user_messages if '?' in msg)
                analysis["user_engagement"]["question_ratio"] = questions / len(user_messages)
                
                # Sentiment trend
                for msg in user_messages:
                    sentiment = self.analyze_sentiment(msg)
                    analysis["user_engagement"]["sentiment_trend"].append({
                        "score": sentiment["compound_score"],
                        "classification": sentiment["classification"]
                    })
            
            # AI performance metrics
            ai_responses = [msg.get('ai_response', '') for msg in conversation_history if msg.get('ai_response')]
            if ai_responses:
                response_lengths = [len(response.split()) for response in ai_responses]
                analysis["ai_performance"]["response_length_trend"] = response_lengths
                
                # Calculate relevance scores (simplified)
                for i, msg in enumerate(conversation_history):
                    user_input = msg.get('user_input', '')
                    ai_response = msg.get('ai_response', '')
                    
                    if user_input and ai_response:
                        relevance = self.semantic_similarity(user_input, ai_response)
                        analysis["ai_performance"]["response_relevance"].append(relevance)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Conversation flow analysis error: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def extract_technical_specifications(self, text: str) -> Dict[str, Any]:
        """Extract technical specifications from text"""
        specifications = {
            "materials": [],
            "dimensions": [],
            "strengths": [],
            "grades": [],
            "standards": []
        }
        
        try:
            # Strength specifications
            strength_patterns = [
                r"(\d+\.?\d*)\s*(mpa|psi|ksi|n/mm2)",
                r"(yield|tensile|compressive|flexural)\s+strength:?\s*(\d+\.?\d*)\s*(mpa|psi|ksi)",
                r"(grade|class)\s*([a-z]?\d+[a-z]?)",
                r"(\d+)%?\s*(elongation|ductility)"
            ]
            
            text_lower = text.lower()
            for pattern in strength_patterns:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    if 'grade' in match.group().lower() or 'class' in match.group().lower():
                        specifications["grades"].append({
                            "text": match.group(),
                            "type": "material_grade",
                            "value": match.group(2) if match.lastindex >= 2 else match.group(1)
                        })
                    else:
                        specifications["strengths"].append({
                            "text": match.group(),
                            "type": "strength",
                            "value": match.group(1) if match.group(1).replace('.','').isdigit() else match.group(2),
                            "unit": match.group(-1)
                        })
            
            # Dimension specifications
            dimension_patterns = [
                r"(\d+\.?\d*)\s*(mm|cm|m|inch|in|ft|feet)\s*x\s*(\d+\.?\d*)\s*(mm|cm|m|inch|in|ft|feet)",
                r"diameter:?\s*(\d+\.?\d*)\s*(mm|cm|m|inch|in)",
                r"thickness:?\s*(\d+\.?\d*)\s*(mm|cm|m|inch|in)"
            ]
            
            for pattern in dimension_patterns:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    specifications["dimensions"].append({
                        "text": match.group(),
                        "type": "dimension",
                        "values": [g for g in match.groups() if g and not g.isalpha()],
                        "units": [g for g in match.groups() if g and g.isalpha()]
                    })
            
            # Standards and certifications
            standards_patterns = [
                r"(astm|iso|en|bs|din|jis)\s*[a-z]?\d+[a-z]?",
                r"(api|asme|aws|aisc)\s*\d+[a-z]?",
                r"(grade|class|type)\s*[a-z]?\d+[a-z]?"
            ]
            
            for pattern in standards_patterns:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    specifications["standards"].append({
                        "text": match.group(),
                        "type": "standard",
                        "organization": match.group(1) if match.lastindex >= 1 else "unknown"
                    })
        
        except Exception as e:
            self.logger.error(f"Technical specification extraction error: {e}")
        
        return specifications
    
    def process_warehouse_query(self, text: str, language: str = 'en') -> Dict[str, Any]:
        """Comprehensive processing of warehouse queries"""
        try:
            # Language detection (override user selection if confident)
            detected_lang = self.detect_language(text)
            if detected_lang['confidence'] > 0.8:
                language = detected_lang['language']
            
            # Extract all NLP features
            entities = self.extract_entities(text)
            intent = self.classify_intent(text)
            sentiment = self.analyze_sentiment(text)
            tech_specs = self.extract_technical_specifications(text)
            
            # Warehouse-specific processing
            warehouse_context = self._analyze_warehouse_context(text, entities)
            
            result = {
                "processed_text": text,
                "language": {
                    "detected": detected_lang,
                    "used": language
                },
                "entities": entities,
                "intent": intent,
                "sentiment": sentiment,
                "technical_specifications": tech_specs,
                "warehouse_context": warehouse_context,
                "processing_timestamp": datetime.now().isoformat(),
                "confidence_score": self._calculate_overall_confidence(intent, entities, sentiment)
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Warehouse query processing error: {e}")
            return {
                "error": f"Processing failed: {str(e)}",
                "processed_text": text,
                "language": {"used": language}
            }
    
    def _analyze_warehouse_context(self, text: str, entities: Dict) -> Dict[str, Any]:
        """Analyze warehouse-specific context from the query"""
        context = {
            "query_type": "general",
            "urgency": "normal",
            "scope": "single_item",
            "operational_context": [],
            "suggested_actions": []
        }
        
        text_lower = text.lower()
        
        # Determine query type
        if any(word in text_lower for word in ['urgent', 'asap', 'emergency', 'immediately']):
            context["urgency"] = "high"
        elif any(word in text_lower for word in ['when possible', 'no rush', 'later']):
            context["urgency"] = "low"
        
        # Determine scope
        if any(word in text_lower for word in ['all', 'entire', 'complete', 'full inventory']):
            context["scope"] = "multiple_items"
        elif any(word in text_lower for word in ['bulk', 'large quantity', 'wholesale']):
            context["scope"] = "bulk_operation"
        
        # Operational context
        if entities["quantities"]:
            context["operational_context"].append("quantity_specific")
        if entities["locations"]:
            context["operational_context"].append("location_specific")
        if entities["materials"]:
            context["operational_context"].append("material_specific")
        
        # Suggest actions based on intent and entities
        intent_type = entities.get("intent", {}).get("intent", "general")
        
        if intent_type == "inventory_inquiry":
            context["suggested_actions"].append("check_stock_levels")
            if entities["locations"]:
                context["suggested_actions"].append("verify_location")
        elif intent_type == "product_search":
            context["suggested_actions"].append("search_catalog")
            context["suggested_actions"].append("check_alternatives")
        elif intent_type == "pricing_inquiry":
            context["suggested_actions"].append("generate_quote")
            context["suggested_actions"].append("check_bulk_discounts")
        
        return context
    
    def _calculate_overall_confidence(self, intent: Dict, entities: Dict, sentiment: Dict) -> float:
        """Calculate overall confidence score for the NLP processing"""
        try:
            intent_conf = intent.get("confidence", 0.0)
            
            # Entity confidence (average of all detected entities)
            entity_confidences = []
            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    if isinstance(entity, dict) and "confidence" in entity:
                        entity_confidences.append(entity["confidence"])
            
            entity_conf = sum(entity_confidences) / len(entity_confidences) if entity_confidences else 0.5
            
            sentiment_conf = sentiment.get("confidence", 0.0)
            
            # Weighted average
            overall_confidence = (
                intent_conf * 0.4 +
                entity_conf * 0.4 +
                sentiment_conf * 0.2
            )
            
            return round(overall_confidence, 3)
            
        except Exception:
            return 0.5


# Global instance
nlp_processor = AdvancedNLPProcessor()


def get_nlp_processor():
    """Get the global NLP processor instance"""
    return nlp_processor


# Convenience functions for integration
def process_user_query(text: str, language: str = 'en') -> Dict[str, Any]:
    """Main entry point for processing user queries"""
    return nlp_processor.process_warehouse_query(text, language)


def analyze_conversation_history(conversation_history: List[Dict]) -> Dict[str, Any]:
    """Analyze conversation history for insights"""
    return {
        "summary": nlp_processor.summarize_conversation(conversation_history),
        "flow_analysis": nlp_processor.analyze_conversation_flow(conversation_history),
        "topics": nlp_processor.topic_modeling([
            msg.get('user_input', '') for msg in conversation_history[-20:] 
            if msg.get('user_input')
        ])
    }


def extract_warehouse_intelligence(texts: List[str]) -> Dict[str, Any]:
    """Extract comprehensive warehouse intelligence from multiple texts"""
    if not texts:
        return {"error": "No texts provided"}
    
    results = {
        "individual_analyses": [],
        "aggregate_insights": {},
        "topic_analysis": {},
        "entity_summary": {
            "materials": set(),
            "locations": set(), 
            "quantities": [],
            "specifications": set()
        }
    }
    
    # Process each text
    for text in texts:
        analysis = nlp_processor.process_warehouse_query(text)
        results["individual_analyses"].append(analysis)
        
        # Aggregate entities
        entities = analysis.get("entities", {})
        for material in entities.get("materials", []):
            if isinstance(material, dict):
                results["entity_summary"]["materials"].add(material.get("text", ""))
        
        for location in entities.get("locations", []):
            if isinstance(location, dict):
                results["entity_summary"]["locations"].add(location.get("text", ""))
        
        for quantity in entities.get("quantities", []):
            if isinstance(quantity, dict):
                results["entity_summary"]["quantities"].append(quantity)
        
        for spec in entities.get("specifications", []):
            if isinstance(spec, dict):
                results["entity_summary"]["specifications"].add(spec.get("text", ""))
    
    # Convert sets to lists for JSON serialization
    results["entity_summary"]["materials"] = list(results["entity_summary"]["materials"])
    results["entity_summary"]["locations"] = list(results["entity_summary"]["locations"])
    results["entity_summary"]["specifications"] = list(results["entity_summary"]["specifications"])
    
    # Topic modeling on all texts
    results["topic_analysis"] = nlp_processor.topic_modeling(texts)
    
    return results
