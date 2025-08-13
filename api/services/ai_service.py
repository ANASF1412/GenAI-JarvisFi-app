"""
JarvisFi - AI Service Integration
Comprehensive AI service for financial advice, translation, and intelligent responses
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Union
import json
from datetime import datetime

# AI/ML imports
from transformers import pipeline, AutoTokenizer, AutoModel
import torch
from sentence_transformers import SentenceTransformer
import numpy as np

# IBM Watson integration
try:
    from ibm_watson import AssistantV2
    from ibm_watsonx_ai import APIClient, Credentials
    from ibm_watsonx_ai.foundation_models import Model
    WATSON_AVAILABLE = True
except ImportError:
    WATSON_AVAILABLE = False
    logging.warning("IBM Watson libraries not available")

# OpenAI fallback
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI library not available")

from core.config import get_settings
from core.cache import cache_manager, cached
from utils.helpers import sanitize_text, detect_language

settings = get_settings()
logger = logging.getLogger(__name__)


class AIService:
    """Comprehensive AI service for JarvisFi"""
    
    def __init__(self):
        self.watson_assistant = None
        self.watsonx_model = None
        self.sentence_transformer = None
        self.translation_models = {}
        self.financial_classifier = None
        self.sentiment_analyzer = None
        self.initialized = False
    
    async def initialize(self):
        """Initialize AI services"""
        try:
            logger.info("🤖 Initializing AI services...")
            
            # Initialize IBM Watson if available
            if WATSON_AVAILABLE and settings.IBM_WATSON_API_KEY:
                await self._initialize_watson()
            
            # Initialize Hugging Face models
            await self._initialize_huggingface_models()
            
            # Initialize OpenAI as fallback
            if OPENAI_AVAILABLE and settings.OPENAI_API_KEY:
                openai.api_key = settings.OPENAI_API_KEY
            
            self.initialized = True
            logger.info("✅ AI services initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ AI service initialization failed: {e}")
            raise
    
    async def _initialize_watson(self):
        """Initialize IBM Watson services"""
        try:
            # Watson Assistant
            if settings.IBM_WATSON_ASSISTANT_ID:
                self.watson_assistant = AssistantV2(
                    version='2023-06-15',
                    authenticator=Credentials(
                        api_key=settings.IBM_WATSON_API_KEY,
                        url=settings.IBM_WATSON_URL
                    ).get_authenticator()
                )
            
            # WatsonX Foundation Models
            if settings.IBM_WATSONX_PROJECT_ID:
                credentials = Credentials(
                    api_key=settings.IBM_WATSONX_API_KEY,
                    url="https://us-south.ml.cloud.ibm.com"
                )
                
                client = APIClient(credentials)
                client.set.default_project(settings.IBM_WATSONX_PROJECT_ID)
                
                self.watsonx_model = Model(
                    model_id="meta-llama/llama-2-70b-chat",
                    params={
                        "decoding_method": "greedy",
                        "max_new_tokens": 500,
                        "temperature": 0.7,
                        "top_p": 0.9
                    },
                    credentials=credentials,
                    project_id=settings.IBM_WATSONX_PROJECT_ID
                )
            
            logger.info("✅ IBM Watson services initialized")
            
        except Exception as e:
            logger.error(f"❌ Watson initialization failed: {e}")
    
    async def _initialize_huggingface_models(self):
        """Initialize Hugging Face models"""
        try:
            # Sentence transformer for embeddings
            self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Financial text classifier
            self.financial_classifier = pipeline(
                "text-classification",
                model="ProsusAI/finbert",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Sentiment analyzer
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Translation models
            translation_models = {
                'en-ta': settings.TRANSLATION_MODEL_EN_TA,
                'en-hi': settings.TRANSLATION_MODEL_EN_HI,
                'en-te': settings.TRANSLATION_MODEL_EN_TE
            }
            
            for lang_pair, model_name in translation_models.items():
                try:
                    self.translation_models[lang_pair] = pipeline(
                        "translation",
                        model=model_name,
                        device=0 if torch.cuda.is_available() else -1
                    )
                except Exception as e:
                    logger.warning(f"Failed to load translation model {lang_pair}: {e}")
            
            logger.info("✅ Hugging Face models initialized")
            
        except Exception as e:
            logger.error(f"❌ Hugging Face initialization failed: {e}")
    
    @cached("ai_response", ttl=3600)
    async def generate_financial_advice(
        self, 
        query: str, 
        user_context: Dict[str, Any],
        language: str = "en"
    ) -> Dict[str, Any]:
        """Generate personalized financial advice"""
        try:
            # Sanitize input
            query = sanitize_text(query)
            
            # Detect query intent
            intent = await self._classify_financial_intent(query)
            
            # Generate context-aware prompt
            prompt = self._build_financial_prompt(query, user_context, intent)
            
            # Generate response using best available model
            response = await self._generate_response(prompt, language)
            
            # Analyze sentiment and confidence
            sentiment = await self._analyze_sentiment(response)
            confidence = await self._calculate_confidence(query, response)
            
            return {
                "response": response,
                "intent": intent,
                "sentiment": sentiment,
                "confidence": confidence,
                "language": language,
                "timestamp": datetime.utcnow().isoformat(),
                "sources": await self._get_relevant_sources(intent)
            }
            
        except Exception as e:
            logger.error(f"Financial advice generation failed: {e}")
            return {
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again later.",
                "error": True,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _classify_financial_intent(self, query: str) -> str:
        """Classify financial query intent"""
        try:
            if self.financial_classifier:
                result = self.financial_classifier(query)
                return result[0]['label'].lower()
            
            # Fallback rule-based classification
            query_lower = query.lower()
            
            if any(word in query_lower for word in ['budget', 'expense', 'spending']):
                return 'budgeting'
            elif any(word in query_lower for word in ['invest', 'investment', 'sip', 'mutual fund']):
                return 'investment'
            elif any(word in query_lower for word in ['save', 'saving', 'savings']):
                return 'savings'
            elif any(word in query_lower for word in ['loan', 'debt', 'credit']):
                return 'debt_management'
            elif any(word in query_lower for word in ['tax', 'taxation', 'deduction']):
                return 'tax_planning'
            elif any(word in query_lower for word in ['insurance', 'policy']):
                return 'insurance'
            else:
                return 'general_financial'
                
        except Exception as e:
            logger.error(f"Intent classification failed: {e}")
            return 'general_financial'
    
    def _build_financial_prompt(self, query: str, user_context: Dict[str, Any], intent: str) -> str:
        """Build context-aware financial prompt"""
        user_type = user_context.get('user_type', 'beginner')
        monthly_income = user_context.get('monthly_income', 0)
        age = user_context.get('age', 25)
        location = user_context.get('location', 'India')
        
        prompt = f"""
You are JarvisFi, an AI-powered financial genius providing personalized advice to Indian users.

User Context:
- Type: {user_type}
- Monthly Income: ₹{monthly_income:,}
- Age: {age}
- Location: {location}
- Query Intent: {intent}

User Query: {query}

Provide helpful, accurate, and personalized financial advice considering:
1. Indian financial regulations and tax laws
2. User's income level and life stage
3. Cultural and regional factors
4. Risk tolerance based on user type
5. Practical, actionable recommendations

Keep the response conversational, encouraging, and easy to understand.
Include specific numbers, percentages, or amounts where relevant.
Mention relevant Indian financial instruments (PPF, ELSS, NSC, etc.) when appropriate.
"""
        return prompt
    
    async def _generate_response(self, prompt: str, language: str = "en") -> str:
        """Generate response using best available model"""
        try:
            # Try WatsonX first
            if self.watsonx_model:
                response = self.watsonx_model.generate_text(prompt=prompt)
                if response and language != "en":
                    response = await self.translate_text(response, "en", language)
                return response
            
            # Try OpenAI as fallback
            if OPENAI_AVAILABLE and settings.OPENAI_API_KEY:
                response = await openai.ChatCompletion.acreate(
                    model=settings.OPENAI_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.7
                )
                text = response.choices[0].message.content
                if language != "en":
                    text = await self.translate_text(text, "en", language)
                return text
            
            # Fallback to rule-based responses
            return await self._generate_fallback_response(prompt, language)
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return "I apologize, but I'm having trouble generating a response right now."
    
    async def _generate_fallback_response(self, prompt: str, language: str) -> str:
        """Generate fallback response when AI models are unavailable"""
        # Extract intent from prompt
        if "budgeting" in prompt.lower():
            response = """Here are some budgeting tips:
1. Follow the 50/30/20 rule: 50% needs, 30% wants, 20% savings
2. Track your expenses for at least a month
3. Use budgeting apps to monitor spending
4. Review and adjust your budget monthly
5. Build an emergency fund of 6 months expenses"""
        
        elif "investment" in prompt.lower():
            response = """Investment guidance:
1. Start with SIPs in diversified equity funds
2. Consider ELSS for tax benefits
3. Diversify across asset classes
4. Invest for long-term (5+ years)
5. Review your portfolio quarterly"""
        
        elif "savings" in prompt.lower():
            response = """Savings strategies:
1. Pay yourself first - save before spending
2. Use high-yield savings accounts
3. Automate your savings
4. Set specific savings goals
5. Consider PPF for long-term savings"""
        
        else:
            response = """I'm here to help with your financial questions! I can assist with:
- Budgeting and expense management
- Investment planning and SIPs
- Savings strategies
- Tax planning
- Insurance guidance
- Debt management"""
        
        if language != "en":
            response = await self.translate_text(response, "en", language)
        
        return response
    
    async def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text between languages"""
        try:
            if source_lang == target_lang:
                return text
            
            lang_pair = f"{source_lang}-{target_lang}"
            
            if lang_pair in self.translation_models:
                result = self.translation_models[lang_pair](text)
                return result[0]['translation_text']
            
            # Fallback to basic translation dictionary for common phrases
            return await self._basic_translation(text, target_lang)
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return text  # Return original text if translation fails
    
    async def _basic_translation(self, text: str, target_lang: str) -> str:
        """Basic translation for common financial terms"""
        if target_lang == "ta":  # Tamil
            translations = {
                "budget": "பட்ஜெட்",
                "savings": "சேமிப்பு",
                "investment": "முதலீடு",
                "money": "பணம்",
                "income": "வருமானம்",
                "expense": "செலவு"
            }
        elif target_lang == "hi":  # Hindi
            translations = {
                "budget": "बजट",
                "savings": "बचत",
                "investment": "निवेश",
                "money": "पैसा",
                "income": "आय",
                "expense": "खर्च"
            }
        else:
            return text
        
        for english, translated in translations.items():
            text = text.replace(english, translated)
        
        return text
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            if self.sentiment_analyzer:
                result = self.sentiment_analyzer(text)
                return {
                    "label": result[0]['label'],
                    "score": result[0]['score']
                }
            
            # Basic sentiment analysis
            positive_words = ['good', 'great', 'excellent', 'positive', 'beneficial']
            negative_words = ['bad', 'poor', 'negative', 'risky', 'dangerous']
            
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            if positive_count > negative_count:
                return {"label": "POSITIVE", "score": 0.7}
            elif negative_count > positive_count:
                return {"label": "NEGATIVE", "score": 0.7}
            else:
                return {"label": "NEUTRAL", "score": 0.5}
                
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {"label": "NEUTRAL", "score": 0.5}
    
    async def _calculate_confidence(self, query: str, response: str) -> float:
        """Calculate confidence score for response"""
        try:
            # Simple confidence calculation based on response length and specificity
            confidence = 0.5  # Base confidence
            
            # Increase confidence for longer, more detailed responses
            if len(response) > 100:
                confidence += 0.2
            
            # Increase confidence if response contains specific financial terms
            financial_terms = ['investment', 'savings', 'budget', 'SIP', 'mutual fund', 'PPF', 'ELSS']
            term_count = sum(1 for term in financial_terms if term.lower() in response.lower())
            confidence += min(term_count * 0.1, 0.3)
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Confidence calculation failed: {e}")
            return 0.5
    
    async def _get_relevant_sources(self, intent: str) -> List[str]:
        """Get relevant sources for financial advice"""
        sources = {
            'investment': [
                'SEBI Guidelines',
                'Mutual Fund Fact Sheets',
                'RBI Investment Guidelines'
            ],
            'tax_planning': [
                'Income Tax Act 1961',
                'CBDT Circulars',
                'Tax Planning Guidelines'
            ],
            'savings': [
                'RBI Savings Guidelines',
                'Bank Interest Rate Policies',
                'Government Savings Schemes'
            ],
            'insurance': [
                'IRDAI Guidelines',
                'Insurance Product Comparisons',
                'Claim Settlement Ratios'
            ]
        }
        
        return sources.get(intent, ['General Financial Guidelines', 'RBI Publications'])
    
    async def cleanup(self):
        """Cleanup AI service resources"""
        try:
            # Cleanup models and free memory
            if self.sentence_transformer:
                del self.sentence_transformer
            
            if self.financial_classifier:
                del self.financial_classifier
            
            if self.sentiment_analyzer:
                del self.sentiment_analyzer
            
            # Clear translation models
            self.translation_models.clear()
            
            # Force garbage collection
            import gc
            gc.collect()
            
            logger.info("✅ AI service cleanup completed")
            
        except Exception as e:
            logger.error(f"❌ AI service cleanup failed: {e}")


# Global AI service instance
ai_service = AIService()
