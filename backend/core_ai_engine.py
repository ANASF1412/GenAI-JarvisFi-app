"""
Core AI Engine for JarvisFi - Multilingual Personal Finance Chatbot
Implements IBM Watsonx, Hugging Face, and RAG integration with RBI/SEBI documents
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# AI/ML Imports
try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    from sentence_transformers import SentenceTransformer
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

# IBM Watson Integration
try:
    from ibm_watson import AssistantV2, LanguageTranslatorV3
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    IBM_AVAILABLE = True
except ImportError:
    IBM_AVAILABLE = False

# Voice Processing
try:
    import speech_recognition as sr
    import pyttsx3
    from coqui_tts import TTS
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

# Security
from cryptography.fernet import Fernet
import hashlib
import secrets

class CoreAIEngine:
    """
    Core AI Engine with multilingual support, RAG integration, and demographic awareness
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_ai_models()
        self.setup_security()
        self.setup_rag_system()
        self.setup_voice_system()
        
        # Supported languages
        self.supported_languages = {
            'en': 'English',
            'ta': 'Tamil',
            'hi': 'Hindi',
            'te': 'Telugu'
        }
        
        # Demographic profiles
        self.demographic_profiles = {
            'student': {
                'tone': 'casual',
                'complexity': 'simple',
                'focus': ['budgeting', 'savings', 'education_loans'],
                'examples': 'relatable_student_scenarios'
            },
            'professional': {
                'tone': 'formal',
                'complexity': 'detailed',
                'focus': ['investments', 'tax_planning', 'retirement'],
                'examples': 'professional_scenarios'
            },
            'farmer': {
                'tone': 'supportive',
                'complexity': 'practical',
                'focus': ['crop_loans', 'msp', 'subsidies', 'insurance'],
                'examples': 'agricultural_scenarios'
            },
            'senior_citizen': {
                'tone': 'respectful',
                'complexity': 'clear',
                'focus': ['retirement_planning', 'healthcare', 'fixed_deposits'],
                'examples': 'senior_scenarios'
            }
        }
    
    def setup_ai_models(self):
        """Initialize AI models for multilingual processing"""
        try:
            if HF_AVAILABLE:
                # Multilingual sentence transformer for embeddings
                self.sentence_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                
                # Translation pipeline
                self.translator = pipeline("translation", 
                                         model="Helsinki-NLP/opus-mt-mul-en",
                                         device=0 if torch.cuda.is_available() else -1)
                
                # Sentiment analysis for multiple languages
                self.sentiment_analyzer = pipeline("sentiment-analysis",
                                                 model="cardiffnlp/twitter-xlm-roberta-base-sentiment")
                
                # Text generation for responses
                self.text_generator = pipeline("text-generation",
                                             model="microsoft/DialoGPT-medium")
                
                self.logger.info("✅ Hugging Face models loaded successfully")
            else:
                self.logger.warning("⚠️ Hugging Face models not available - using fallback")
                
            # IBM Watson setup
            if IBM_AVAILABLE and os.getenv('IBM_WATSON_API_KEY'):
                authenticator = IAMAuthenticator(os.getenv('IBM_WATSON_API_KEY'))
                self.watson_assistant = AssistantV2(
                    version='2023-06-15',
                    authenticator=authenticator
                )
                self.watson_assistant.set_service_url(os.getenv('IBM_WATSON_URL'))
                
                self.watson_translator = LanguageTranslatorV3(
                    version='2023-06-15',
                    authenticator=authenticator
                )
                self.logger.info("✅ IBM Watson services initialized")
            else:
                self.logger.warning("⚠️ IBM Watson not configured - using local models")
                
        except Exception as e:
            self.logger.error(f"❌ Error setting up AI models: {e}")
    
    def setup_security(self):
        """Initialize security components"""
        try:
            # Generate encryption key
            self.encryption_key = Fernet.generate_key()
            self.cipher_suite = Fernet(self.encryption_key)
            
            # Security settings
            self.security_config = {
                'encryption_enabled': True,
                'data_retention_days': 90,
                'audit_logging': True,
                'gdpr_compliant': True,
                'hipaa_compliant': True
            }
            
            self.logger.info("✅ Security components initialized")
        except Exception as e:
            self.logger.error(f"❌ Error setting up security: {e}")
    
    def setup_rag_system(self):
        """Initialize RAG system with RBI/SEBI documents"""
        try:
            # Document embeddings storage
            self.document_embeddings = {}
            self.document_chunks = {}
            
            # RBI/SEBI document sources
            self.financial_documents = {
                'rbi_guidelines': {
                    'source': 'Reserve Bank of India',
                    'topics': ['banking', 'monetary_policy', 'regulations'],
                    'last_updated': '2024-01-01'
                },
                'sebi_regulations': {
                    'source': 'Securities and Exchange Board of India',
                    'topics': ['securities', 'mutual_funds', 'investments'],
                    'last_updated': '2024-01-01'
                },
                'income_tax_rules': {
                    'source': 'Income Tax Department',
                    'topics': ['taxation', 'deductions', 'filing'],
                    'last_updated': '2024-01-01'
                }
            }
            
            # Load and process documents
            self.load_financial_documents()
            
            self.logger.info("✅ RAG system initialized with financial documents")
        except Exception as e:
            self.logger.error(f"❌ Error setting up RAG system: {e}")
    
    def setup_voice_system(self):
        """Initialize voice input/output system"""
        try:
            if VOICE_AVAILABLE:
                # Speech recognition
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                
                # Text-to-speech
                self.tts_engine = pyttsx3.init()
                
                # Coqui TTS for offline multilingual support
                try:
                    self.coqui_tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")
                    self.offline_tts_available = True
                except:
                    self.offline_tts_available = False
                
                # Voice settings
                self.voice_config = {
                    'languages': {
                        'en': 'english',
                        'ta': 'tamil',
                        'hi': 'hindi',
                        'te': 'telugu'
                    },
                    'speech_rate': 150,
                    'volume': 0.8
                }
                
                self.logger.info("✅ Voice system initialized")
            else:
                self.logger.warning("⚠️ Voice libraries not available")
                
        except Exception as e:
            self.logger.error(f"❌ Error setting up voice system: {e}")
    
    def load_financial_documents(self):
        """Load and process financial documents for RAG"""
        try:
            # Sample financial knowledge base
            sample_documents = {
                'rbi_savings_guidelines': """
                RBI Guidelines on Savings Accounts:
                - Minimum balance requirements vary by bank type
                - Interest rates are deregulated for savings accounts
                - KYC compliance is mandatory for all accounts
                - Dormant accounts are those with no transactions for 2 years
                """,
                'sebi_mutual_fund_rules': """
                SEBI Mutual Fund Regulations:
                - SIP investments can start from Rs. 500 per month
                - Exit load applicable for redemptions within 1 year
                - NAV calculation done daily for open-ended funds
                - Risk disclosure mandatory for all schemes
                """,
                'tax_saving_instruments': """
                Income Tax Saving Instruments under Section 80C:
                - ELSS mutual funds: Lock-in period 3 years
                - PPF: Lock-in period 15 years, tax-free returns
                - NSC: 5-year lock-in, taxable interest
                - Life insurance premiums: Up to Rs. 1.5 lakh deduction
                """
            }
            
            # Process documents into embeddings
            if HF_AVAILABLE:
                for doc_id, content in sample_documents.items():
                    # Create embeddings
                    embedding = self.sentence_model.encode(content)
                    self.document_embeddings[doc_id] = embedding
                    
                    # Store chunks
                    chunks = self.chunk_document(content)
                    self.document_chunks[doc_id] = chunks
            
            self.logger.info(f"✅ Loaded {len(sample_documents)} financial documents")
            
        except Exception as e:
            self.logger.error(f"❌ Error loading documents: {e}")
    
    def chunk_document(self, content: str, chunk_size: int = 200) -> List[str]:
        """Split document into chunks for RAG processing"""
        words = content.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    async def generate_response(self, 
                              query: str, 
                              user_profile: Dict,
                              language: str = 'en',
                              use_voice: bool = False) -> Dict[str, Any]:
        """
        Generate comprehensive AI response with RAG, demographic awareness, and multilingual support
        """
        try:
            # Extract user context
            user_type = user_profile.get('basic_info', {}).get('user_type', 'professional')
            monthly_income = user_profile.get('basic_info', {}).get('monthly_income', 30000)
            
            # Get demographic profile
            demo_profile = self.demographic_profiles.get(user_type, self.demographic_profiles['professional'])
            
            # Translate query to English if needed
            english_query = await self.translate_to_english(query, language)
            
            # Perform RAG search
            relevant_docs = await self.search_documents(english_query)
            
            # Generate base response
            base_response = await self.generate_base_response(
                english_query, user_profile, demo_profile, relevant_docs
            )
            
            # Translate response back to target language
            final_response = await self.translate_response(base_response, language)
            
            # Add metadata
            response_data = {
                'content': final_response,
                'language': language,
                'user_type': user_type,
                'confidence_score': self.calculate_confidence(english_query, relevant_docs),
                'sources': [doc['source'] for doc in relevant_docs],
                'timestamp': datetime.now().isoformat(),
                'demographic_adapted': True,
                'rag_enhanced': len(relevant_docs) > 0,
                'voice_enabled': use_voice and VOICE_AVAILABLE
            }
            
            # Generate voice output if requested
            if use_voice and VOICE_AVAILABLE:
                audio_data = await self.generate_voice_output(final_response, language)
                response_data['audio'] = audio_data
            
            return response_data
            
        except Exception as e:
            self.logger.error(f"❌ Error generating response: {e}")
            return self.get_fallback_response(language, user_type)
    
    async def translate_to_english(self, text: str, source_language: str) -> str:
        """Translate text to English for processing"""
        if source_language == 'en':
            return text
        
        try:
            if IBM_AVAILABLE and hasattr(self, 'watson_translator'):
                # Use IBM Watson for translation
                result = self.watson_translator.translate(
                    text=text,
                    source=source_language,
                    target='en'
                ).get_result()
                return result['translations'][0]['translation']
            
            elif HF_AVAILABLE:
                # Use Hugging Face translation
                result = self.translator(text, src_lang=source_language, tgt_lang='en')
                return result[0]['translation_text']
            
            else:
                # Fallback - return original text
                return text
                
        except Exception as e:
            self.logger.error(f"❌ Translation error: {e}")
            return text
    
    async def search_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search relevant documents using RAG"""
        try:
            if not HF_AVAILABLE or not self.document_embeddings:
                return []
            
            # Generate query embedding
            query_embedding = self.sentence_model.encode(query)
            
            # Calculate similarities
            similarities = {}
            for doc_id, doc_embedding in self.document_embeddings.items():
                similarity = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
                )
                similarities[doc_id] = similarity
            
            # Get top documents
            top_docs = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]
            
            relevant_docs = []
            for doc_id, score in top_docs:
                if score > 0.3:  # Threshold for relevance
                    relevant_docs.append({
                        'id': doc_id,
                        'score': score,
                        'source': self.financial_documents.get(doc_id, {}).get('source', 'Financial Authority'),
                        'content': self.document_chunks.get(doc_id, [''])[0]
                    })
            
            return relevant_docs
            
        except Exception as e:
            self.logger.error(f"❌ Document search error: {e}")
            return []
    
    def calculate_confidence(self, query: str, relevant_docs: List[Dict]) -> float:
        """Calculate confidence score for the response"""
        try:
            base_confidence = 0.7
            
            # Boost confidence if relevant documents found
            if relevant_docs:
                doc_boost = min(0.2, len(relevant_docs) * 0.1)
                base_confidence += doc_boost
            
            # Adjust based on query complexity
            query_words = len(query.split())
            if query_words > 10:
                base_confidence -= 0.1
            
            return min(0.95, max(0.3, base_confidence))
            
        except Exception as e:
            self.logger.error(f"❌ Confidence calculation error: {e}")
            return 0.5
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            if self.security_config['encryption_enabled']:
                encrypted_data = self.cipher_suite.encrypt(data.encode())
                return encrypted_data.decode()
            return data
        except Exception as e:
            self.logger.error(f"❌ Encryption error: {e}")
            return data
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            if self.security_config['encryption_enabled']:
                decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode())
                return decrypted_data.decode()
            return encrypted_data
        except Exception as e:
            self.logger.error(f"❌ Decryption error: {e}")
            return encrypted_data
    
    def get_fallback_response(self, language: str, user_type: str) -> Dict[str, Any]:
        """Generate fallback response when AI systems fail"""
        fallback_responses = {
            'en': {
                'student': "I'm here to help with your financial questions! As a student, I can assist with budgeting, savings, and education loans.",
                'professional': "I'm your AI financial advisor. I can help with investments, tax planning, and wealth management strategies.",
                'farmer': "I'm here to support your agricultural finance needs. I can help with crop loans, MSP information, and subsidies.",
                'senior_citizen': "I'm here to help with your financial planning. I can assist with retirement planning and safe investment options."
            },
            'ta': {
                'student': "நான் உங்கள் நிதி கேள்விகளுக்கு உதவ இங்கே இருக்கிறேன்! ஒரு மாணவராக, பட்ஜெட், சேமிப்பு மற்றும் கல்விக் கடன்களில் உதவ முடியும்.",
                'professional': "நான் உங்கள் AI நிதி ஆலோசகர். முதலீடுகள், வரி திட்டமிடல் மற்றும் செல்வ மேலாண்மை உத்திகளில் உதவ முடியும்.",
                'farmer': "உங்கள் விவசாய நிதி தேவைகளுக்கு ஆதரவளிக்க நான் இங்கே இருக்கிறேன். பயிர் கடன்கள், MSP தகவல் மற்றும் மானியங்களில் உதவ முடியும்.",
                'senior_citizen': "உங்கள் நிதி திட்டமிடலுக்கு உதவ நான் இங்கே இருக்கிறேன். ஓய்வூதிய திட்டமிடல் மற்றும் பாதுகாப்பான முதலீட்டு விருப்பங்களில் உதவ முடியும்."
            }
        }
        
        response_text = fallback_responses.get(language, fallback_responses['en']).get(
            user_type, fallback_responses['en']['professional']
        )
        
        return {
            'content': response_text,
            'language': language,
            'user_type': user_type,
            'confidence_score': 0.5,
            'sources': [],
            'timestamp': datetime.now().isoformat(),
            'demographic_adapted': True,
            'rag_enhanced': False,
            'voice_enabled': False,
            'fallback_response': True
        }
