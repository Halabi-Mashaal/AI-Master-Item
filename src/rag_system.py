"""
Enhanced RAG (Retrieval-Augmented Generation) System for Warehouse Yamama AI Agent
Provides intelligent document processing and context-aware responses
"""

import os
import json
import sqlite3
import hashlib
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class DocumentStore:
    """Persistent document storage and retrieval system"""
    
    def __init__(self, db_path='data/document_store.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.document_vectors = None
        self.documents = []
        self._load_documents()
    
    def init_database(self):
        """Initialize SQLite database for document storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_type TEXT,
                file_size INTEGER,
                processed BOOLEAN DEFAULT FALSE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT,
                chunk_text TEXT,
                chunk_index INTEGER,
                vector_data TEXT,
                FOREIGN KEY (document_id) REFERENCES documents (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_document(self, filename: str, content: str, metadata: Dict = None) -> str:
        """Add document to store and return document ID"""
        doc_id = hashlib.md5(f"{filename}{content}".encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO documents 
            (id, filename, content, metadata, file_type, file_size)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            doc_id, 
            filename, 
            content, 
            json.dumps(metadata or {}),
            filename.split('.')[-1].lower() if '.' in filename else 'unknown',
            len(content)
        ))
        
        # Split document into chunks for better retrieval
        chunks = self._split_into_chunks(content)
        for i, chunk in enumerate(chunks):
            cursor.execute('''
                INSERT OR REPLACE INTO document_chunks 
                (document_id, chunk_text, chunk_index)
                VALUES (?, ?, ?)
            ''', (doc_id, chunk, i))
        
        conn.commit()
        conn.close()
        
        # Reload documents and rebuild vectors
        self._load_documents()
        self._build_vectors()
        
        return doc_id
    
    def _split_into_chunks(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into overlapping chunks for better context retrieval"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size // 2):  # 50% overlap
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def _load_documents(self):
        """Load all documents from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT d.id, d.filename, d.content, d.metadata, d.file_type,
                   GROUP_CONCAT(c.chunk_text, ' ') as full_chunks
            FROM documents d
            LEFT JOIN document_chunks c ON d.id = c.document_id
            GROUP BY d.id, d.filename, d.content, d.metadata, d.file_type
        ''')
        
        self.documents = []
        for row in cursor.fetchall():
            doc_id, filename, content, metadata, file_type, chunks = row
            self.documents.append({
                'id': doc_id,
                'filename': filename,
                'content': content,
                'chunks': chunks or content,
                'metadata': json.loads(metadata or '{}'),
                'file_type': file_type
            })
        
        conn.close()
    
    def _build_vectors(self):
        """Build TF-IDF vectors for document similarity search"""
        if not self.documents:
            return
        
        # Use chunks for vectorization for better granular search
        chunk_texts = [doc['chunks'] for doc in self.documents]
        
        try:
            self.document_vectors = self.vectorizer.fit_transform(chunk_texts)
        except Exception as e:
            logging.error(f"Error building document vectors: {e}")
            self.document_vectors = None
    
    def search_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search documents using semantic similarity"""
        if not self.documents or self.document_vectors is None:
            return []
        
        try:
            # Vectorize query
            query_vector = self.vectorizer.transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vector, self.document_vectors)[0]
            
            # Get top-k most similar documents
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum similarity threshold
                    doc = self.documents[idx].copy()
                    doc['similarity_score'] = float(similarities[idx])
                    results.append(doc)
            
            return results
            
        except Exception as e:
            logging.error(f"Error searching documents: {e}")
            return []
    
    def get_document(self, doc_id: str) -> Optional[Dict]:
        """Get specific document by ID"""
        for doc in self.documents:
            if doc['id'] == doc_id:
                return doc
        return None
    
    def get_all_documents(self) -> List[Dict]:
        """Get all stored documents"""
        return self.documents
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete document from store"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM document_chunks WHERE document_id = ?', (doc_id,))
        cursor.execute('DELETE FROM documents WHERE id = ?', (doc_id,))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if deleted:
            self._load_documents()
            self._build_vectors()
        
        return deleted


class RAGSystem:
    """Retrieval-Augmented Generation System"""
    
    def __init__(self, document_store: DocumentStore):
        self.document_store = document_store
        self.conversation_context = {}
    
    def process_query_with_context(self, query: str, session_id: str, user_language: str = 'en') -> Dict[str, Any]:
        """Process user query with document context"""
        
        # Search for relevant documents
        relevant_docs = self.document_store.search_documents(query, top_k=3)
        
        # Build context from retrieved documents
        context = self._build_context(relevant_docs, query)
        
        # Store conversation context
        self.conversation_context[session_id] = {
            'last_query': query,
            'retrieved_docs': relevant_docs,
            'context_used': context,
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'query': query,
            'relevant_documents': relevant_docs,
            'context': context,
            'has_context': len(relevant_docs) > 0,
            'session_id': session_id
        }
    
    def _build_context(self, documents: List[Dict], query: str) -> str:
        """Build contextual information from retrieved documents"""
        if not documents:
            return ""
        
        context_parts = []
        context_parts.append("📚 **Relevant Information from Your Documents:**\n")
        
        for i, doc in enumerate(documents, 1):
            # Extract most relevant snippet
            snippet = self._extract_relevant_snippet(doc['content'], query)
            
            context_parts.append(f"**{i}. {doc['filename']}** (Relevance: {doc['similarity_score']:.2%})")
            context_parts.append(f"   {snippet}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def _extract_relevant_snippet(self, content: str, query: str, snippet_length: int = 200) -> str:
        """Extract most relevant snippet from document content"""
        words = content.split()
        query_words = query.lower().split()
        
        # Find the section with most query word matches
        best_score = 0
        best_start = 0
        window_size = 50  # words
        
        for i in range(len(words) - window_size + 1):
            window_text = ' '.join(words[i:i + window_size]).lower()
            score = sum(1 for qw in query_words if qw in window_text)
            
            if score > best_score:
                best_score = score
                best_start = i
        
        # Extract snippet around best match
        start = max(0, best_start - 10)
        end = min(len(words), best_start + window_size + 10)
        snippet_words = words[start:end]
        
        snippet = ' '.join(snippet_words)
        if len(snippet) > snippet_length:
            snippet = snippet[:snippet_length] + "..."
        
        return snippet
    
    def get_conversation_context(self, session_id: str) -> Dict[str, Any]:
        """Get conversation context for session"""
        return self.conversation_context.get(session_id, {})
    
    def add_document_from_upload(self, file_obj, filename: str) -> str:
        """Add document from file upload"""
        try:
            # Read file content based on type
            content = ""
            file_ext = filename.lower().split('.')[-1] if '.' in filename else ''
            
            if file_ext in ['txt', 'csv']:
                content = file_obj.read().decode('utf-8')
            elif file_ext in ['xlsx', 'xls']:
                # Handle Excel files
                df = pd.read_excel(file_obj)
                content = df.to_string()
            else:
                # For other files, try to read as text
                content = str(file_obj.read())
            
            # Add to document store
            metadata = {
                'file_type': file_ext,
                'upload_time': datetime.now().isoformat(),
                'processed_by': 'rag_system'
            }
            
            doc_id = self.document_store.add_document(filename, content, metadata)
            return doc_id
            
        except Exception as e:
            logging.error(f"Error processing uploaded file {filename}: {e}")
            return None


class SessionManager:
    """Persistent session management for cloud deployment"""
    
    def __init__(self, db_path='data/sessions.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize session database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_data TEXT,
                conversation_history TEXT,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_or_create_session(self, request_headers: Dict) -> str:
        """Get or create session ID based on request"""
        # Try to get session from various sources
        session_id = None
        
        # Check for session in headers
        if 'X-Session-ID' in request_headers:
            session_id = request_headers['X-Session-ID']
        
        # Check for session in user agent + IP (simple fallback)
        if not session_id:
            user_agent = request_headers.get('User-Agent', '')
            x_forwarded_for = request_headers.get('X-Forwarded-For', '')
            if user_agent and x_forwarded_for:
                session_id = hashlib.md5(f"{user_agent}{x_forwarded_for}".encode()).hexdigest()
        
        # Create new session if none found
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())
        
        # Ensure session exists in database
        self._ensure_session_exists(session_id)
        
        return session_id
    
    def _ensure_session_exists(self, session_id: str):
        """Ensure session exists in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT session_id FROM sessions WHERE session_id = ?', (session_id,))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO sessions (session_id, user_data, conversation_history)
                VALUES (?, ?, ?)
            ''', (session_id, '{}', '[]'))
        
        # Update last activity
        cursor.execute('''
            UPDATE sessions SET last_activity = CURRENT_TIMESTAMP 
            WHERE session_id = ?
        ''', (session_id,))
        
        conn.commit()
        conn.close()
    
    def get_session_data(self, session_id: str) -> Dict:
        """Get session data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_data, conversation_history FROM sessions 
            WHERE session_id = ?
        ''', (session_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            user_data, history = row
            return {
                'user_data': json.loads(user_data or '{}'),
                'conversation_history': json.loads(history or '[]')
            }
        
        return {'user_data': {}, 'conversation_history': []}
    
    def update_session_data(self, session_id: str, user_data: Dict, conversation_history: List):
        """Update session data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sessions 
            SET user_data = ?, conversation_history = ?, last_activity = CURRENT_TIMESTAMP
            WHERE session_id = ?
        ''', (json.dumps(user_data), json.dumps(conversation_history), session_id))
        
        conn.commit()
        conn.close()
    
    def cleanup_old_sessions(self, days: int = 7):
        """Cleanup sessions older than specified days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM sessions 
            WHERE last_activity < datetime('now', '-{} days')
        '''.format(days))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted
