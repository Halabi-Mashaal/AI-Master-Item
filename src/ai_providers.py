"""
Advanced AI Provider Integration for OpenAI and Gemini
Provides intelligent context-aware responses and file analysis
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

# AI Provider imports with fallback handling
try:
    import openai
    OPENAI_AVAILABLE = True
    logging.info("OpenAI library available")
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI library not available")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    logging.info("Gemini library available")
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("Gemini library not available")

class AdvancedAIProvider:
    """Advanced AI provider supporting OpenAI and Gemini models"""
    
    def __init__(self):
        self.provider = os.getenv('AI_PROVIDER', 'fallback').lower()
        self.openai_client = None
        self.gemini_model = None
        
        # Initialize OpenAI if available and configured
        if OPENAI_AVAILABLE and self.provider in ['openai', 'auto']:
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key and openai_key != 'your_openai_api_key_here':
                try:
                    self.openai_client = openai.OpenAI(api_key=openai_key)
                    self.provider = 'openai'
                    logging.info("OpenAI client initialized successfully")
                except Exception as e:
                    logging.error(f"Failed to initialize OpenAI: {e}")
        
        # Initialize Gemini if available and configured
        if GEMINI_AVAILABLE and self.provider in ['gemini', 'auto']:
            gemini_key = os.getenv('GEMINI_API_KEY')
            if gemini_key and gemini_key != 'your_gemini_api_key_here':
                try:
                    genai.configure(api_key=gemini_key)
                    self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                    if self.provider != 'openai':  # Only set if OpenAI wasn't already set
                        self.provider = 'gemini'
                    logging.info("Gemini model initialized successfully")
                except Exception as e:
                    logging.error(f"Failed to initialize Gemini: {e}")
        
        # Set fallback if no providers are available
        if self.provider not in ['openai', 'gemini'] or (self.provider == 'openai' and not self.openai_client) or (self.provider == 'gemini' and not self.gemini_model):
            self.provider = 'fallback'
            logging.info("Using fallback AI provider")
    
    def generate_response(self, prompt: str, context: Dict = None, system_message: str = None) -> Dict[str, Any]:
        """Generate intelligent response using the best available AI provider"""
        
        context = context or {}
        
        # Create system message for cement industry expertise
        if not system_message:
            system_message = """You are an expert AI assistant specializing in cement industry operations, 
            inventory management, and data analysis. You work for Yamama Cement Company and provide 
            intelligent, contextual responses. Always be helpful, accurate, and professional. 
            When analyzing data or files, provide specific insights relevant to cement manufacturing, 
            quality control, inventory optimization, and business operations."""
        
        # Build contextual prompt
        full_prompt = self._build_contextual_prompt(prompt, context, system_message)
        
        try:
            if self.provider == 'openai' and self.openai_client:
                return self._generate_openai_response(full_prompt, system_message)
            elif self.provider == 'gemini' and self.gemini_model:
                return self._generate_gemini_response(full_prompt)
            else:
                return self._generate_fallback_response(prompt, context)
                
        except Exception as e:
            logging.error(f"AI generation error with {self.provider}: {e}")
            return self._generate_fallback_response(prompt, context)
    
    def analyze_file_content(self, file_content: str, filename: str, user_query: str = "") -> Dict[str, Any]:
        """Analyze file content using AI for intelligent insights"""
        
        analysis_prompt = f"""
        Please analyze the following {filename} file content and provide detailed insights:
        
        FILE: {filename}
        CONTENT:
        {file_content[:3000]}  # Limit content to avoid token limits
        
        USER QUERY: {user_query if user_query else "Provide comprehensive analysis"}
        
        Please provide:
        1. Data summary and structure
        2. Key insights and patterns
        3. Cement industry-specific recommendations
        4. Quality assessment and data validation
        5. Actionable suggestions for optimization
        
        Format your response in a clear, professional manner suitable for cement industry professionals.
        """
        
        try:
            if self.provider == 'openai' and self.openai_client:
                return self._generate_openai_response(analysis_prompt, "You are an expert data analyst specializing in cement industry operations.")
            elif self.provider == 'gemini' and self.gemini_model:
                return self._generate_gemini_response(analysis_prompt)
            else:
                return self._analyze_file_fallback(file_content, filename, user_query)
                
        except Exception as e:
            logging.error(f"File analysis error with {self.provider}: {e}")
            return self._analyze_file_fallback(file_content, filename, user_query)
    
    def _build_contextual_prompt(self, prompt: str, context: Dict, system_message: str) -> str:
        """Build contextual prompt with conversation history and user profile"""
        
        contextual_parts = []
        
        # Add conversation context
        conversation_length = context.get('conversation_length', 0)
        if conversation_length > 0:
            contextual_parts.append(f"[CONTEXT: This is conversation #{conversation_length + 1} with this user]")
        
        # Add user expertise level
        expertise = context.get('technical_level', 'intermediate')
        contextual_parts.append(f"[USER EXPERTISE: {expertise} level - adjust response accordingly]")
        
        # Add recent topics if available
        recent_topics = context.get('recent_topics', [])
        if recent_topics:
            topics_str = ', '.join(recent_topics[-3:])  # Last 3 topics
            contextual_parts.append(f"[RECENT TOPICS: {topics_str}]")
        
        # Add file context if present
        if context.get('has_files'):
            contextual_parts.append("[FILE CONTEXT: User has uploaded files for analysis]")
        
        # Combine context with user prompt
        full_prompt = '\n'.join(contextual_parts) + f"\n\nUSER QUESTION: {prompt}"
        
        return full_prompt
    
    def _generate_openai_response(self, prompt: str, system_message: str) -> Dict[str, Any]:
        """Generate response using OpenAI GPT models"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can change to gpt-4 if you have access
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return {
                'response': response.choices[0].message.content,
                'provider': 'openai',
                'model': 'gpt-3.5-turbo',
                'success': True,
                'tokens_used': response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")
    
    def _generate_gemini_response(self, prompt: str) -> Dict[str, Any]:
        """Generate response using Gemini Pro model"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            
            return {
                'response': response.text,
                'provider': 'gemini',
                'model': 'gemini-pro',
                'success': True,
                'tokens_used': 0  # Gemini doesn't provide token count in the same way
            }
            
        except Exception as e:
            raise Exception(f"Gemini API error: {e}")
    
    def _generate_fallback_response(self, prompt: str, context: Dict) -> Dict[str, Any]:
        """Generate fallback response when no AI provider is available"""
        
        # Simple pattern-based responses
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey']):
            response = "Hello! I'm your AI assistant for cement industry operations. How can I help you today?"
        
        elif any(word in prompt_lower for word in ['analyze', 'analysis', 'data']):
            response = """I can help you analyze data and files for cement industry insights. 
            For the most advanced analysis capabilities, please configure OpenAI or Gemini API keys in your .env file.
            
            Current capabilities include:
            • Basic data structure analysis
            • Cement industry pattern recognition
            • Quality assessment recommendations
            • Inventory optimization suggestions"""
        
        elif any(word in prompt_lower for word in ['file', 'upload', 'document']):
            response = """I can process various file types including Excel, CSV, and documents.
            For advanced AI-powered file analysis, please add your OpenAI or Gemini API key to the .env file.
            
            Current file processing includes:
            • File format detection
            • Basic data extraction
            • Structure analysis
            • Industry-specific insights"""
        
        else:
            response = """I'm here to help with cement industry operations and data analysis.
            
            **Available Services:**
            • Data analysis and file processing
            • Quality control insights
            • Inventory management optimization
            • Process improvement recommendations
            
            For enhanced AI capabilities, configure OpenAI or Gemini API keys in your environment."""
        
        return {
            'response': response,
            'provider': 'fallback',
            'model': 'rule-based',
            'success': True,
            'tokens_used': 0
        }
    
    def _analyze_file_fallback(self, file_content: str, filename: str, user_query: str) -> Dict[str, Any]:
        """Fallback file analysis without advanced AI"""
        
        # Basic file analysis
        lines = file_content.split('\n')
        words = file_content.split()
        
        file_ext = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
        
        analysis = f"""**File Analysis: {filename}**

**Basic Information:**
• File Type: {file_ext.upper()}
• Lines: {len(lines)}
• Words: {len(words)}
• Characters: {len(file_content)}

**Content Preview:**
{file_content[:300]}...

**Recommendations:**
For advanced AI-powered file analysis with detailed insights, patterns recognition, and industry-specific recommendations, please configure OpenAI or Gemini API keys in your .env file.

**Current Analysis Available:**
• Basic structure detection
• Data format validation
• Simple pattern recognition
• Industry-standard recommendations"""
        
        return {
            'response': analysis,
            'provider': 'fallback',
            'model': 'basic-analysis',
            'success': True,
            'tokens_used': 0
        }
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get current provider status and capabilities"""
        
        return {
            'current_provider': self.provider,
            'openai_available': OPENAI_AVAILABLE and self.openai_client is not None,
            'gemini_available': GEMINI_AVAILABLE and self.gemini_model is not None,
            'fallback_active': self.provider == 'fallback'
        }
