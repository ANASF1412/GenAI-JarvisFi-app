"""
Language Support Module for Personal Finance Chatbot
Supports English and Tamil languages with financial terminology
"""

import re
from typing import Dict, List, Optional

class LanguageSupport:
    """
    Multi-language support for the finance chatbot
    """
    
    def __init__(self):
        self.current_language = 'english'
        self.setup_translations()
        self.setup_tamil_patterns()
    
    def setup_translations(self):
        """Setup translation dictionaries"""
        self.translations = {
            'english': {
                # UI Elements
                'welcome': 'Welcome to Personal Finance Assistant',
                'chat': 'Chat',
                'budget_analysis': 'Budget Analysis',
                'smart_alerts': 'Smart Alerts',
                'currency_converter': 'Currency Converter',
                'data_upload': 'Data Upload',
                'pdf_reports': 'PDF Reports',
                'insights_dashboard': 'Insights Dashboard',
                'settings': 'Settings',
                'language': 'Language',
                'user_type': 'User Type',
                'profile': 'Your Profile',
                'name': 'Name',
                'age': 'Age',
                'monthly_income': 'Monthly Income (₹)',
                'submit': 'Submit',
                'clear': 'Clear',
                'upload': 'Upload',
                'download': 'Download',
                
                # User Types
                'student': 'Student',
                'professional': 'Professional',
                'beginner': 'Beginner',
                'intermediate': 'Intermediate',
                
                # Financial Terms
                'budget': 'Budget',
                'savings': 'Savings',
                'investment': 'Investment',
                'expense': 'Expense',
                'income': 'Income',
                'loan': 'Loan',
                'debt': 'Debt',
                'tax': 'Tax',
                'insurance': 'Insurance',
                'emergency_fund': 'Emergency Fund',
                
                # Messages
                'ask_question': 'Ask me anything about personal finance...',
                'upload_data': 'Upload your transaction data to get personalized insights',
                'no_data': 'No data available. Please upload your transaction data.',
                'analysis_complete': 'Analysis completed successfully!',
                'error_occurred': 'An error occurred. Please try again.',
                
                # Greetings
                'greeting_student': 'Hi! I\'m here to help you manage your finances as a student. Let\'s make every rupee count! 💰',
                'greeting_professional': 'Welcome! I\'ll help you optimize your financial strategy and achieve your professional goals. 📈',
                'greeting_beginner': 'Hello! Don\'t worry, I\'ll guide you through the basics of personal finance step by step. 🌟',
                'greeting_intermediate': 'Hi there! Ready to take your financial knowledge to the next level? Let\'s dive in! 🚀',
            },
            
            'tamil': {
                # UI Elements
                'welcome': 'தனிப்பட்ட நிதி உதவியாளருக்கு வரவேற்கிறோம்',
                'chat': 'அரட்டை',
                'budget_analysis': 'பட்ஜெட் பகுப்பாய்வு',
                'smart_alerts': 'ஸ்மார்ட் எச்சரிக்கைகள்',
                'currency_converter': 'நாணய மாற்றி',
                'data_upload': 'தரவு பதிவேற்றம்',
                'pdf_reports': 'PDF அறிக்கைகள்',
                'insights_dashboard': 'நுண்ணறிவு டாஷ்போர்டு',
                'settings': 'அமைப்புகள்',
                'language': 'மொழி',
                'user_type': 'பயனர் வகை',
                'profile': 'உங்கள் சுயவிவரம்',
                'name': 'பெயர்',
                'age': 'வயது',
                'monthly_income': 'மாதாந்திர வருமானம் (₹)',
                'submit': 'சமர்பிக்கவும்',
                'clear': 'அழிக்கவும்',
                'upload': 'பதிவேற்றவும்',
                'download': 'பதிவிறக்கவும்',
                
                # User Types
                'student': 'மாணவர்',
                'professional': 'தொழில்முறை',
                'beginner': 'ஆரம்பநிலை',
                'intermediate': 'இடைநிலை',
                
                # Financial Terms
                'budget': 'பட்ஜெட்',
                'savings': 'சேமிப்பு',
                'investment': 'முதலீடு',
                'expense': 'செலவு',
                'income': 'வருமானம்',
                'loan': 'கடன்',
                'debt': 'கடன்',
                'tax': 'வரி',
                'insurance': 'காப்பீடு',
                'emergency_fund': 'அவசர நிதி',
                
                # Messages
                'ask_question': 'தனிப்பட்ட நிதி பற்றி எதையும் கேளுங்கள்...',
                'upload_data': 'தனிப்பட்ட நுண்ணறிவுகளைப் பெற உங்கள் பரிவர்த்தனை தரவைப் பதிவேற்றவும்',
                'no_data': 'தரவு இல்லை. உங்கள் பரிவர்த்தனை தரவைப் பதிவேற்றவும்.',
                'analysis_complete': 'பகுப்பாய்வு வெற்றிகரமாக முடிந்தது!',
                'error_occurred': 'ஒரு பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்.',
                
                # Greetings
                'greeting_student': 'வணக்கம்! மாணவராக உங்கள் நிதியை நிர்வகிக்க நான் இங்கே இருக்கிறேன். ஒவ்வொரு ரூபாயையும் பயனுள்ளதாக்குவோம்! 💰',
                'greeting_professional': 'வரவேற்கிறோம்! உங்கள் நிதி உத்தியை மேம்படுத்தவும் தொழில்முறை இலக்குகளை அடையவும் நான் உதவுவேன். 📈',
                'greeting_beginner': 'வணக்கம்! கவலைப்பட வேண்டாம், தனிப்பட்ட நிதியின் அடிப்படைகளை படிப்படியாக நான் உங்களுக்கு வழிகாட்டுவேன். 🌟',
                'greeting_intermediate': 'வணக்கம்! உங்கள் நிதி அறிவை அடுத்த நிலைக்கு கொண்டு செல்ல தயாரா? ஆரம்பிக்கலாம்! 🚀',
            }
        }
    
    def setup_tamil_patterns(self):
        """Setup Tamil language patterns for query understanding"""
        self.tamil_patterns = {
            # Budget related
            'budget': ['பட்ஜெட்', 'செலவு திட்டம்', 'பணம் நிர்வாகம்'],
            'savings': ['சேமிப்பு', 'பணம் சேமிக்க', 'சேர்த்து வைக்க'],
            'investment': ['முதலீடு', 'பணம் முதலீடு', 'பங்கு', 'மியூச்சுவல் ஃபண்ட்'],
            'loan': ['கடன்', 'லோன்', 'கடன் வாங்க'],
            'tax': ['வரி', 'டாக்ஸ்', 'வரி சேமிப்பு'],
            'expense': ['செலவு', 'செலவழிப்பு', 'பணம் செலவு'],
            'income': ['வருமானம்', 'சம்பளம்', 'வேலை'],
            
            # Question patterns
            'how': ['எப்படி', 'எவ்வாறு', 'என்ன வழி'],
            'what': ['என்ன', 'எது', 'எதை'],
            'where': ['எங்கே', 'எங்கு', 'எந்த இடத்தில்'],
            'when': ['எப்போது', 'எந்த நேரம்'],
            'why': ['ஏன்', 'எதற்காக'],
            
            # Common phrases
            'help': ['உதவி', 'உதவுங்கள்', 'சொல்லுங்கள்'],
            'money': ['பணம்', 'காசு', 'ரூபாய்'],
            'save': ['சேமிக்க', 'சேர்க்க', 'வைக்க'],
            'spend': ['செலவு', 'செலவழிக்க', 'கொடுக்க'],
        }
    
    def set_language(self, language: str):
        """Set the current language"""
        if language.lower() in ['english', 'tamil']:
            self.current_language = language.lower()
            print(f"✅ Language successfully set to: {self.current_language}")
        else:
            print(f"❌ Invalid language: {language}, keeping current: {self.current_language}")
    
    def get_text(self, key: str) -> str:
        """Get translated text for a key"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def detect_language(self, text: str) -> str:
        """Detect language from input text"""
        # Simple detection based on Tamil characters
        tamil_chars = re.findall(r'[\u0B80-\u0BFF]', text)
        if len(tamil_chars) > 0:
            return 'tamil'
        return 'english'
    
    def translate_query(self, query: str) -> Dict:
        """Translate and understand Tamil queries"""
        detected_lang = self.detect_language(query)
        
        if detected_lang == 'tamil':
            # Convert Tamil query to English concepts
            english_concepts = []
            query_lower = query.lower()
            
            for concept, patterns in self.tamil_patterns.items():
                for pattern in patterns:
                    if pattern in query_lower:
                        english_concepts.append(concept)
            
            return {
                'detected_language': 'tamil',
                'original_query': query,
                'concepts': english_concepts,
                'intent': self._determine_intent_from_concepts(english_concepts)
            }
        else:
            return {
                'detected_language': 'english',
                'original_query': query,
                'concepts': [],
                'intent': 'general'
            }
    
    def _determine_intent_from_concepts(self, concepts: List[str]) -> str:
        """Determine intent from extracted concepts"""
        if 'budget' in concepts or 'expense' in concepts:
            return 'budget_management'
        elif 'savings' in concepts or 'save' in concepts:
            return 'savings_advice'
        elif 'investment' in concepts:
            return 'investment_guidance'
        elif 'loan' in concepts:
            return 'debt_management'
        elif 'tax' in concepts:
            return 'tax_advice'
        else:
            return 'general_financial'
    
    def get_user_type_options(self) -> List[Dict]:
        """Get user type options in current language"""
        return [
            {'value': 'student', 'label': self.get_text('student')},
            {'value': 'professional', 'label': self.get_text('professional')},
            {'value': 'beginner', 'label': self.get_text('beginner')},
            {'value': 'intermediate', 'label': self.get_text('intermediate')}
        ]
    
    def get_language_options(self) -> List[Dict]:
        """Get language options"""
        return [
            {'value': 'english', 'label': 'English'},
            {'value': 'tamil', 'label': 'தமிழ்'}
        ]
    
    def format_response_for_language(self, response: str, user_type: str) -> str:
        """Format response based on current language and user type"""
        if self.current_language == 'tamil':
            # Add Tamil formatting and user-type specific adjustments
            if user_type == 'beginner':
                response = "🌟 " + response + "\n\nமேலும் உதவி தேவையா? கேளுங்கள்!"
            elif user_type == 'student':
                response = "💰 " + response + "\n\nமாணவர்களுக்கான மேலும் குறிப்புகள் தேவையா?"
        else:
            # English formatting
            if user_type == 'beginner':
                response = "🌟 " + response + "\n\nNeed more help? Feel free to ask!"
            elif user_type == 'student':
                response = "💰 " + response + "\n\nWant more student-specific tips?"
        
        return response
