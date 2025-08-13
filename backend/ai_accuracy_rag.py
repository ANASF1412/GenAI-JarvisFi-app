#!/usr/bin/env python3
"""
AI Accuracy and RAG (Retrieval Augmented Generation) Module
Implements fact-checking, verified sources, and guardrails for financial advice
"""

import os
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import re
import requests
from pathlib import Path

# Vector database and embeddings
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

# Sentence transformers for embeddings
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

# PDF processing
try:
    import PyPDF2
    import fitz  # PyMuPDF
    PDF_PROCESSING_AVAILABLE = True
except ImportError:
    PDF_PROCESSING_AVAILABLE = False

# IBM Watson for fact-checking (optional)
try:
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    IBM_WATSON_AVAILABLE = True
except ImportError:
    IBM_WATSON_AVAILABLE = False

class AIAccuracyRAG:
    """
    AI Accuracy and RAG system for financial advice verification
    """
    
    def __init__(self, data_dir: str = "data/knowledge_base"):
        """Initialize RAG system"""
        self.logger = self._setup_logger()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self._setup_vector_database()
        self._setup_embeddings()
        self._setup_fact_checking()
        
        # Financial data sources
        self.verified_sources = {
            'rbi': {
                'name': 'Reserve Bank of India',
                'base_url': 'https://www.rbi.org.in',
                'documents': ['monetary_policy', 'banking_regulations', 'interest_rates']
            },
            'sebi': {
                'name': 'Securities and Exchange Board of India',
                'base_url': 'https://www.sebi.gov.in',
                'documents': ['investment_guidelines', 'mutual_funds', 'stock_market']
            },
            'irdai': {
                'name': 'Insurance Regulatory and Development Authority',
                'base_url': 'https://www.irdai.gov.in',
                'documents': ['insurance_policies', 'regulations', 'guidelines']
            },
            'cbdt': {
                'name': 'Central Board of Direct Taxes',
                'base_url': 'https://www.incometaxindia.gov.in',
                'documents': ['tax_rules', 'deductions', 'filing_guidelines']
            }
        }
        
        # Guardrails and disclaimers
        self.high_risk_topics = [
            'investment_advice', 'stock_recommendations', 'crypto_currency',
            'high_return_schemes', 'tax_evasion', 'loan_defaults'
        ]
        
        self.disclaimer_templates = {
            'investment': "⚠️ This is general information only. Please consult a certified financial advisor before making investment decisions.",
            'tax': "⚠️ Tax laws are complex and change frequently. Please consult a tax professional for personalized advice.",
            'loan': "⚠️ Loan terms vary by lender and individual circumstances. Please verify details with financial institutions.",
            'insurance': "⚠️ Insurance needs are personal. Please consult with licensed insurance agents for suitable coverage."
        }
        
        self.logger.info("AI Accuracy RAG system initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _setup_vector_database(self):
        """Setup ChromaDB for document storage and retrieval"""
        try:
            if CHROMADB_AVAILABLE:
                # Initialize ChromaDB
                self.chroma_client = chromadb.PersistentClient(
                    path=str(self.data_dir / "chroma_db"),
                    settings=Settings(anonymized_telemetry=False)
                )
                
                # Create collections for different document types
                self.collections = {
                    'financial_docs': self.chroma_client.get_or_create_collection(
                        name="financial_documents",
                        metadata={"description": "Verified financial documents and guidelines"}
                    ),
                    'regulations': self.chroma_client.get_or_create_collection(
                        name="regulations",
                        metadata={"description": "Government regulations and policies"}
                    ),
                    'faq': self.chroma_client.get_or_create_collection(
                        name="faq",
                        metadata={"description": "Frequently asked questions and answers"}
                    )
                }
                
                self.logger.info("ChromaDB vector database initialized")
            else:
                self.logger.warning("ChromaDB not available, using fallback storage")
                self._setup_fallback_storage()
                
        except Exception as e:
            self.logger.error(f"Vector database setup failed: {e}")
            self._setup_fallback_storage()
    
    def _setup_embeddings(self):
        """Setup sentence transformer for embeddings"""
        try:
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                # Use multilingual model for Indian languages
                self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                self.logger.info("Sentence transformer model loaded")
            else:
                self.logger.warning("Sentence transformers not available")
                self.embedding_model = None
        except Exception as e:
            self.logger.error(f"Embedding model setup failed: {e}")
            self.embedding_model = None
    
    def _setup_fact_checking(self):
        """Setup fact-checking services"""
        try:
            if IBM_WATSON_AVAILABLE:
                watson_api_key = os.getenv('IBM_WATSON_NLU_API_KEY')
                watson_url = os.getenv('IBM_WATSON_NLU_URL')
                
                if watson_api_key and watson_url:
                    authenticator = IAMAuthenticator(watson_api_key)
                    self.watson_nlu = NaturalLanguageUnderstandingV1(
                        version='2022-04-07',
                        authenticator=authenticator
                    )
                    self.watson_nlu.set_service_url(watson_url)
                    self.logger.info("IBM Watson NLU initialized for fact-checking")
                else:
                    self.watson_nlu = None
                    self.logger.info("IBM Watson credentials not found")
            else:
                self.watson_nlu = None
                self.logger.info("IBM Watson not available")
        except Exception as e:
            self.logger.error(f"Fact-checking setup failed: {e}")
            self.watson_nlu = None
    
    def _setup_fallback_storage(self):
        """Setup fallback document storage"""
        self.fallback_docs = {}
        self.fallback_file = self.data_dir / "fallback_docs.json"
        
        try:
            if self.fallback_file.exists():
                with open(self.fallback_file, 'r', encoding='utf-8') as f:
                    self.fallback_docs = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load fallback storage: {e}")
            self.fallback_docs = {}
    
    def ingest_document(self, document_path: str, source: str, doc_type: str) -> bool:
        """Ingest and index a document"""
        try:
            # Extract text from document
            text_content = self._extract_text_from_document(document_path)
            if not text_content:
                return False
            
            # Split into chunks
            chunks = self._split_text_into_chunks(text_content)
            
            # Generate embeddings and store
            doc_id = hashlib.md5(f"{document_path}_{source}".encode()).hexdigest()
            
            if CHROMADB_AVAILABLE and self.embedding_model:
                # Store in ChromaDB
                collection = self.collections.get(doc_type, self.collections['financial_docs'])
                
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{doc_id}_chunk_{i}"
                    embedding = self.embedding_model.encode(chunk).tolist()
                    
                    collection.add(
                        embeddings=[embedding],
                        documents=[chunk],
                        metadatas=[{
                            'source': source,
                            'doc_type': doc_type,
                            'chunk_index': i,
                            'ingested_at': datetime.utcnow().isoformat()
                        }],
                        ids=[chunk_id]
                    )
            else:
                # Store in fallback
                self.fallback_docs[doc_id] = {
                    'source': source,
                    'doc_type': doc_type,
                    'chunks': chunks,
                    'ingested_at': datetime.utcnow().isoformat()
                }
                self._save_fallback_docs()
            
            self.logger.info(f"Document ingested: {document_path} ({len(chunks)} chunks)")
            return True
            
        except Exception as e:
            self.logger.error(f"Document ingestion failed: {e}")
            return False
    
    def _extract_text_from_document(self, document_path: str) -> str:
        """Extract text from various document formats"""
        try:
            path = Path(document_path)
            
            if not path.exists():
                return ""
            
            if path.suffix.lower() == '.pdf' and PDF_PROCESSING_AVAILABLE:
                # Extract from PDF
                text = ""
                try:
                    # Try PyMuPDF first (better for complex PDFs)
                    doc = fitz.open(document_path)
                    for page in doc:
                        text += page.get_text()
                    doc.close()
                except:
                    # Fallback to PyPDF2
                    with open(document_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        for page in pdf_reader.pages:
                            text += page.extract_text()
                
                return text
            
            elif path.suffix.lower() in ['.txt', '.md']:
                # Extract from text files
                with open(document_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif path.suffix.lower() == '.json':
                # Extract from JSON
                with open(document_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return json.dumps(data, indent=2)
            
            return ""
            
        except Exception as e:
            self.logger.error(f"Text extraction failed: {e}")
            return ""
    
    def _split_text_into_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        try:
            chunks = []
            start = 0
            
            while start < len(text):
                end = start + chunk_size
                
                # Try to break at sentence boundary
                if end < len(text):
                    # Look for sentence endings
                    sentence_end = text.rfind('.', start, end)
                    if sentence_end > start + chunk_size // 2:
                        end = sentence_end + 1
                
                chunk = text[start:end].strip()
                if chunk:
                    chunks.append(chunk)
                
                start = end - overlap
            
            return chunks
            
        except Exception as e:
            self.logger.error(f"Text chunking failed: {e}")
            return [text]  # Return original text as single chunk
    
    def retrieve_relevant_documents(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant documents for a query"""
        try:
            results = []
            
            if CHROMADB_AVAILABLE and self.embedding_model:
                # Generate query embedding
                query_embedding = self.embedding_model.encode(query).tolist()
                
                # Search in all collections
                for collection_name, collection in self.collections.items():
                    try:
                        search_results = collection.query(
                            query_embeddings=[query_embedding],
                            n_results=top_k,
                            include=['documents', 'metadatas', 'distances']
                        )
                        
                        for i, doc in enumerate(search_results['documents'][0]):
                            results.append({
                                'content': doc,
                                'metadata': search_results['metadatas'][0][i],
                                'similarity': 1 - search_results['distances'][0][i],  # Convert distance to similarity
                                'collection': collection_name
                            })
                    except Exception as e:
                        self.logger.warning(f"Search in {collection_name} failed: {e}")
            
            else:
                # Fallback: simple text matching
                query_lower = query.lower()
                for doc_id, doc_data in self.fallback_docs.items():
                    for i, chunk in enumerate(doc_data['chunks']):
                        if any(word in chunk.lower() for word in query_lower.split()):
                            results.append({
                                'content': chunk,
                                'metadata': {
                                    'source': doc_data['source'],
                                    'doc_type': doc_data['doc_type'],
                                    'chunk_index': i
                                },
                                'similarity': 0.5,  # Default similarity
                                'collection': 'fallback'
                            })
            
            # Sort by similarity and return top results
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:top_k]
            
        except Exception as e:
            self.logger.error(f"Document retrieval failed: {e}")
            return []
    
    def _save_fallback_docs(self):
        """Save fallback documents to file"""
        try:
            with open(self.fallback_file, 'w', encoding='utf-8') as f:
                json.dump(self.fallback_docs, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save fallback docs: {e}")

    def fact_check_response(self, response: str, query: str) -> Dict:
        """Fact-check AI response against verified sources"""
        try:
            fact_check_result = {
                'verified': False,
                'confidence': 0.0,
                'sources': [],
                'warnings': [],
                'disclaimers': [],
                'risk_level': 'low'
            }

            # Retrieve relevant documents
            relevant_docs = self.retrieve_relevant_documents(query, top_k=3)

            if relevant_docs:
                fact_check_result['sources'] = [
                    {
                        'source': doc['metadata'].get('source', 'unknown'),
                        'similarity': doc['similarity'],
                        'content_preview': doc['content'][:200] + "..."
                    }
                    for doc in relevant_docs
                ]

                # Calculate confidence based on source similarity
                avg_similarity = sum(doc['similarity'] for doc in relevant_docs) / len(relevant_docs)
                fact_check_result['confidence'] = min(avg_similarity, 0.95)  # Cap at 95%
                fact_check_result['verified'] = avg_similarity > 0.7

            # Check for high-risk topics
            risk_level = self._assess_risk_level(response, query)
            fact_check_result['risk_level'] = risk_level

            # Add appropriate disclaimers
            disclaimers = self._get_disclaimers(response, query, risk_level)
            fact_check_result['disclaimers'] = disclaimers

            # Add warnings for high-risk content
            if risk_level in ['high', 'critical']:
                fact_check_result['warnings'].append(
                    "This topic requires professional consultation. Please verify with certified experts."
                )

            # Use Watson NLU for additional fact-checking if available
            if self.watson_nlu:
                try:
                    watson_result = self._watson_fact_check(response)
                    fact_check_result['watson_analysis'] = watson_result
                except Exception as e:
                    self.logger.warning(f"Watson fact-checking failed: {e}")

            return fact_check_result

        except Exception as e:
            self.logger.error(f"Fact-checking failed: {e}")
            return {
                'verified': False,
                'confidence': 0.0,
                'sources': [],
                'warnings': ['Fact-checking service unavailable'],
                'disclaimers': ['Please verify information independently'],
                'risk_level': 'unknown'
            }

    def _assess_risk_level(self, response: str, query: str) -> str:
        """Assess risk level of financial advice"""
        try:
            response_lower = response.lower()
            query_lower = query.lower()

            # Critical risk indicators
            critical_keywords = [
                'guaranteed returns', 'risk-free investment', 'get rich quick',
                'double your money', 'no risk', 'sure profit', 'insider information'
            ]

            # High risk indicators
            high_risk_keywords = [
                'stock recommendation', 'buy this stock', 'sell everything',
                'invest all', 'take loan for investment', 'crypto currency',
                'bitcoin', 'day trading', 'margin trading'
            ]

            # Medium risk indicators
            medium_risk_keywords = [
                'investment advice', 'portfolio allocation', 'mutual funds',
                'insurance policy', 'tax planning', 'retirement planning'
            ]

            combined_text = f"{response_lower} {query_lower}"

            if any(keyword in combined_text for keyword in critical_keywords):
                return 'critical'
            elif any(keyword in combined_text for keyword in high_risk_keywords):
                return 'high'
            elif any(keyword in combined_text for keyword in medium_risk_keywords):
                return 'medium'
            else:
                return 'low'

        except Exception as e:
            self.logger.error(f"Risk assessment failed: {e}")
            return 'unknown'

    def _get_disclaimers(self, response: str, query: str, risk_level: str) -> List[str]:
        """Get appropriate disclaimers based on content"""
        try:
            disclaimers = []
            response_lower = response.lower()
            query_lower = query.lower()

            # Topic-specific disclaimers
            if any(word in f"{response_lower} {query_lower}" for word in ['invest', 'stock', 'mutual fund', 'return']):
                disclaimers.append(self.disclaimer_templates['investment'])

            if any(word in f"{response_lower} {query_lower}" for word in ['tax', 'deduction', 'filing', 'income tax']):
                disclaimers.append(self.disclaimer_templates['tax'])

            if any(word in f"{response_lower} {query_lower}" for word in ['loan', 'credit', 'emi', 'interest rate']):
                disclaimers.append(self.disclaimer_templates['loan'])

            if any(word in f"{response_lower} {query_lower}" for word in ['insurance', 'policy', 'coverage', 'claim']):
                disclaimers.append(self.disclaimer_templates['insurance'])

            # Risk-based disclaimers
            if risk_level == 'critical':
                disclaimers.append("🚨 CRITICAL: This advice may be misleading or harmful. Please consult certified professionals immediately.")
            elif risk_level == 'high':
                disclaimers.append("⚠️ HIGH RISK: This information requires professional verification before acting upon it.")

            # General disclaimer for all financial advice
            if not disclaimers:
                disclaimers.append("💡 This is general information only. Individual circumstances may vary.")

            return list(set(disclaimers))  # Remove duplicates

        except Exception as e:
            self.logger.error(f"Disclaimer generation failed: {e}")
            return ["Please consult financial professionals for personalized advice."]

    def _watson_fact_check(self, text: str) -> Dict:
        """Use IBM Watson NLU for fact-checking"""
        try:
            from ibm_watson.natural_language_understanding_v1 import Features, ConceptsOptions, KeywordsOptions

            response = self.watson_nlu.analyze(
                text=text,
                features=Features(
                    concepts=ConceptsOptions(limit=5),
                    keywords=KeywordsOptions(limit=10)
                )
            ).get_result()

            return {
                'concepts': response.get('concepts', []),
                'keywords': response.get('keywords', []),
                'analysis_successful': True
            }

        except Exception as e:
            self.logger.error(f"Watson fact-checking failed: {e}")
            return {'analysis_successful': False, 'error': str(e)}

    def generate_rag_response(self, query: str, context: Dict = None) -> Dict:
        """Generate RAG-enhanced response with fact-checking"""
        try:
            # Retrieve relevant documents
            relevant_docs = self.retrieve_relevant_documents(query, top_k=5)

            # Prepare context for response generation
            context_text = ""
            if relevant_docs:
                context_text = "\n\n".join([
                    f"Source: {doc['metadata'].get('source', 'Unknown')}\n{doc['content']}"
                    for doc in relevant_docs[:3]  # Use top 3 most relevant
                ])

            # Generate response (this would integrate with your main AI model)
            response_text = self._generate_contextual_response(query, context_text, context)

            # Fact-check the response
            fact_check = self.fact_check_response(response_text, query)

            # Compile final response
            rag_response = {
                'response': response_text,
                'sources': relevant_docs,
                'fact_check': fact_check,
                'context_used': len(relevant_docs) > 0,
                'generated_at': datetime.utcnow().isoformat(),
                'query': query
            }

            # Add disclaimers to response if high risk
            if fact_check['risk_level'] in ['high', 'critical']:
                rag_response['response'] += f"\n\n{' '.join(fact_check['disclaimers'])}"

            return rag_response

        except Exception as e:
            self.logger.error(f"RAG response generation failed: {e}")
            return {
                'response': "I apologize, but I'm unable to provide a reliable answer right now. Please consult with a financial professional.",
                'sources': [],
                'fact_check': {'verified': False, 'risk_level': 'unknown'},
                'context_used': False,
                'error': str(e)
            }

    def _generate_contextual_response(self, query: str, context: str, user_context: Dict = None) -> str:
        """Generate response using retrieved context (placeholder for AI integration)"""
        try:
            # This is a placeholder - in production, this would integrate with your main AI model
            # The AI model would use the context to generate accurate, grounded responses

            if context:
                return f"Based on verified financial sources: {context[:500]}... [This would be processed by your AI model to generate a proper response]"
            else:
                return "I don't have enough verified information to answer this question accurately. Please consult with a financial professional."

        except Exception as e:
            self.logger.error(f"Contextual response generation failed: {e}")
            return "I'm unable to provide a reliable answer. Please consult with a financial professional."
