import os
import json
import requests
from typing import Dict, List, Optional
from ibm_watson import AssistantV2, NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import logging

class WatsonIntegration:
    """
    Watson integration for natural language processing and conversation management
    """
    
    def __init__(self):
        # Initialize logger first
        self.setup_logger()

        # Initialize Watson services
        self.setup_watson_assistant()
        self.setup_watson_nlu()

    def setup_logger(self):
        """Initialize logger with proper configuration"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create stream handler if not already exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)

            # Create formatter with timestamp, log level, and message
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)

            # Add handler to logger
            self.logger.addHandler(handler)

    def setup_watson_assistant(self):
        """Initialize Watson Assistant service"""
        try:
            authenticator = IAMAuthenticator(os.getenv('WATSON_ASSISTANT_API_KEY'))
            self.assistant = AssistantV2(
                version='2023-06-15',
                authenticator=authenticator
            )
            self.assistant.set_service_url(os.getenv('WATSON_ASSISTANT_URL'))
            self.assistant_id = os.getenv('WATSON_ASSISTANT_ID')
        except Exception as e:
            self.logger.error(f"Error setting up Watson Assistant: {e}")
            self.assistant = None
    
    def setup_watson_nlu(self):
        """Initialize Watson Natural Language Understanding service"""
        try:
            authenticator = IAMAuthenticator(os.getenv('WATSON_NLU_API_KEY'))
            self.nlu = NaturalLanguageUnderstandingV1(
                version='2022-04-07',
                authenticator=authenticator
            )
            self.nlu.set_service_url(os.getenv('WATSON_NLU_URL'))
        except Exception as e:
            self.logger.error(f"Error setting up Watson NLU: {e}")
            self.nlu = None
    
    def create_session(self) -> Optional[str]:
        """Create a new Watson Assistant session"""
        try:
            if self.assistant:
                response = self.assistant.create_session(
                    assistant_id=self.assistant_id
                ).get_result()
                return response['session_id']
        except Exception as e:
            self.logger.error(f"Error creating session: {e}")
        return None
    
    def send_message(self, session_id: str, message: str, context: Dict = None) -> Dict:
        """Send message to Watson Assistant and get response"""
        try:
            if self.assistant:
                response = self.assistant.message(
                    assistant_id=self.assistant_id,
                    session_id=session_id,
                    input={
                        'message_type': 'text',
                        'text': message
                    },
                    context=context or {}
                ).get_result()
                return response
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
        return {}
    
    def analyze_intent_and_entities(self, text: str) -> Dict:
        """Analyze text using Watson NLU to extract financial intents and entities"""
        try:
            if self.nlu:
                response = self.nlu.analyze(
                    text=text,
                    features=Features(
                        entities=EntitiesOptions(limit=10),
                        keywords=KeywordsOptions(limit=10),
                        sentiment=SentimentOptions()
                    )
                ).get_result()
                
                # Extract financial-specific information
                financial_entities = self._extract_financial_entities(response.get('entities', []))
                keywords = response.get('keywords', [])
                sentiment = response.get('sentiment', {})
                
                return {
                    'financial_entities': financial_entities,
                    'keywords': keywords,
                    'sentiment': sentiment,
                    'intent': self._classify_financial_intent(text, keywords)
                }
        except Exception as e:
            self.logger.error(f"Error analyzing text: {e}")
        
        return {
            'financial_entities': [],
            'keywords': [],
            'sentiment': {},
            'intent': 'general'
        }
    
    def _extract_financial_entities(self, entities: List) -> List[Dict]:
        """Extract and categorize financial entities"""
        financial_categories = ['Money', 'Quantity', 'Percent', 'Date', 'Organization']
        financial_entities = []
        
        for entity in entities:
            if entity.get('type') in financial_categories:
                financial_entities.append({
                    'text': entity.get('text'),
                    'type': entity.get('type'),
                    'confidence': entity.get('confidence', 0),
                    'category': self._categorize_financial_entity(entity)
                })
        
        return financial_entities
    
    def _categorize_financial_entity(self, entity: Dict) -> str:
        """Categorize financial entities into specific types"""
        entity_text = entity.get('text', '').lower()
        entity_type = entity.get('type', '')
        
        # Define financial categories
        if entity_type == 'Money' or any(word in entity_text for word in ['dollar', 'usd', 'inr', 'rupee']):
            return 'currency'
        elif entity_type == 'Percent' or '%' in entity_text:
            return 'percentage'
        elif any(word in entity_text for word in ['bank', 'credit', 'loan', 'mortgage']):
            return 'financial_institution'
        elif any(word in entity_text for word in ['investment', 'stock', 'mutual fund', 'sip']):
            return 'investment'
        elif any(word in entity_text for word in ['tax', 'deduction', 'exemption']):
            return 'tax'
        else:
            return 'general'
    
    def _classify_financial_intent(self, text: str, keywords: List) -> str:
        """Classify the financial intent of the user's message"""
        text_lower = text.lower()
        keyword_texts = [kw.get('text', '').lower() for kw in keywords]
        all_text = text_lower + ' ' + ' '.join(keyword_texts)
        
        # Define intent patterns
        budget_patterns = ['budget', 'spending', 'expense', 'track', 'manage money']
        savings_patterns = ['save', 'saving', 'emergency fund', 'goal']
        investment_patterns = ['invest', 'stock', 'mutual fund', 'sip', 'portfolio']
        tax_patterns = ['tax', 'deduction', 'exemption', '80c', 'filing']
        debt_patterns = ['loan', 'debt', 'credit card', 'emi', 'interest']
        
        if any(pattern in all_text for pattern in budget_patterns):
            return 'budget_management'
        elif any(pattern in all_text for pattern in savings_patterns):
            return 'savings_advice'
        elif any(pattern in all_text for pattern in investment_patterns):
            return 'investment_guidance'
        elif any(pattern in all_text for pattern in tax_patterns):
            return 'tax_advice'
        elif any(pattern in all_text for pattern in debt_patterns):
            return 'debt_management'
        else:
            return 'general_financial'
    
    def generate_contextual_response(self, intent: str, entities: List, user_profile: Dict) -> str:
        """Generate contextual response based on intent and user profile"""
        demographic = user_profile.get('demographic', 'professional')
        
        response_templates = {
            'budget_management': {
                'student': "As a student, budgeting is super important! Let me help you create a simple budget that tracks your expenses and helps you save for both essentials and fun activities.",
                'professional': "Let's optimize your budget strategy. I can help you analyze your spending patterns and suggest areas for improvement based on your professional income and goals."
            },
            'savings_advice': {
                'student': "Great question about savings! Even small amounts matter. Let's explore student-friendly saving strategies and emergency fund basics.",
                'professional': "I'll provide comprehensive savings strategies tailored to your professional income. Let's discuss emergency funds, goal-based savings, and optimal saving rates."
            },
            'investment_guidance': {
                'student': "Investing as a student is smart thinking! Let me explain basic investment concepts and low-cost options that work well for students.",
                'professional': "Let's dive into investment strategies suitable for your professional profile. I can help with portfolio allocation, risk assessment, and long-term wealth building."
            },
            'tax_advice': {
                'student': "Tax planning for students involves different considerations. Let me explain deductions and exemptions relevant to your situation.",
                'professional': "I'll help you with comprehensive tax planning strategies, including deductions, exemptions, and tax-efficient investments for professionals."
            }
        }
        
        if intent in response_templates and demographic in response_templates[intent]:
            return response_templates[intent][demographic]
        else:
            return "I'm here to help with your financial questions. Could you provide more details about what specific financial guidance you're looking for?"