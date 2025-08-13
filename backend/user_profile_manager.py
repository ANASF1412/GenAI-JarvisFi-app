"""
Enhanced User Profile Manager for Personal Finance Chatbot
Supports multiple user types with personalized experiences
"""

from typing import Dict, List, Optional
import json
import os
from datetime import datetime

class UserProfileManager:
    """
    Manages user profiles with enhanced categorization and personalization
    """
    
    def __init__(self):
        self.user_types = {
            'student': {
                'description': 'College/University students managing limited budgets',
                'focus_areas': ['budget_basics', 'savings_goals', 'part_time_income', 'education_expenses'],
                'default_goals': ['Emergency fund', 'Education expenses', 'Entertainment budget'],
                'recommended_savings_rate': 0.15,  # 15%
                'priority_categories': ['education', 'food', 'transportation', 'entertainment']
            },
            'professional': {
                'description': 'Working professionals with regular income',
                'focus_areas': ['investment_planning', 'tax_optimization', 'retirement_planning', 'wealth_building'],
                'default_goals': ['Emergency fund', 'Retirement planning', 'Investment portfolio'],
                'recommended_savings_rate': 0.20,  # 20%
                'priority_categories': ['housing', 'transportation', 'healthcare', 'investments']
            },
            'beginner': {
                'description': 'New to personal finance management',
                'focus_areas': ['financial_literacy', 'basic_budgeting', 'savings_habits', 'debt_management'],
                'default_goals': ['Build emergency fund', 'Create first budget', 'Understand investments'],
                'recommended_savings_rate': 0.10,  # 10%
                'priority_categories': ['necessities', 'debt_payment', 'emergency_fund', 'learning']
            },
            'intermediate': {
                'description': 'Some experience with financial planning',
                'focus_areas': ['advanced_budgeting', 'investment_diversification', 'tax_planning', 'goal_optimization'],
                'default_goals': ['Optimize investment portfolio', 'Tax-efficient planning', 'Advanced savings strategies'],
                'recommended_savings_rate': 0.25,  # 25%
                'priority_categories': ['investments', 'tax_planning', 'insurance', 'advanced_goals']
            }
        }
        
        self.experience_levels = {
            'beginner': {
                'explanation_style': 'detailed',
                'use_jargon': False,
                'provide_examples': True,
                'step_by_step': True
            },
            'intermediate': {
                'explanation_style': 'moderate',
                'use_jargon': True,
                'provide_examples': True,
                'step_by_step': False
            },
            'advanced': {
                'explanation_style': 'concise',
                'use_jargon': True,
                'provide_examples': False,
                'step_by_step': False
            }
        }
    
    def create_user_profile(self, user_data: Dict) -> Dict:
        """Create a comprehensive user profile"""
        user_type = user_data.get('user_type', 'beginner')
        
        profile = {
            'basic_info': {
                'name': user_data.get('name', ''),
                'age': user_data.get('age', 25),
                'user_type': user_type,
                'language': user_data.get('language', 'english'),
                'created_at': datetime.now().isoformat()
            },
            'financial_info': {
                'monthly_income': user_data.get('monthly_income', 0),
                'currency': user_data.get('currency', 'INR'),
                'employment_status': user_data.get('employment_status', 'employed'),
                'financial_goals': self.user_types[user_type]['default_goals'].copy()
            },
            'preferences': {
                'explanation_style': self._get_explanation_style(user_type),
                'focus_areas': self.user_types[user_type]['focus_areas'].copy(),
                'priority_categories': self.user_types[user_type]['priority_categories'].copy(),
                'recommended_savings_rate': self.user_types[user_type]['recommended_savings_rate']
            },
            'progress': {
                'onboarding_completed': False,
                'goals_set': False,
                'first_analysis_done': False,
                'data_uploaded': False
            }
        }
        
        return profile
    
    def _get_explanation_style(self, user_type: str) -> Dict:
        """Get explanation style based on user type"""
        if user_type in ['student', 'beginner']:
            return self.experience_levels['beginner']
        elif user_type == 'intermediate':
            return self.experience_levels['intermediate']
        else:  # professional
            return self.experience_levels['intermediate']  # Professionals usually want moderate detail
    
    def get_personalized_greeting(self, profile: Dict, language: str = 'english') -> str:
        """Get personalized greeting based on user profile"""
        user_type = profile.get('basic_info', {}).get('user_type', 'beginner')
        name = profile.get('basic_info', {}).get('name', '')
        
        greetings = {
            'english': {
                'student': f"Hi {name}! 🎓 Ready to master your finances as a student? Let's make every rupee count!",
                'professional': f"Welcome {name}! 💼 Let's optimize your financial strategy and build wealth professionally.",
                'beginner': f"Hello {name}! 🌟 Don't worry, I'll guide you through personal finance step by step.",
                'intermediate': f"Hi {name}! 🚀 Ready to take your financial planning to the next level?"
            },
            'tamil': {
                'student': f"வணக்கம் {name}! 🎓 மாணவராக உங்கள் நிதியை கற்றுக்கொள்ள தயாரா? ஒவ்வொரு ரூபாயையும் பயனுள்ளதாக்குவோம்!",
                'professional': f"வரவேற்கிறோம் {name}! 💼 உங்கள் நிதி உத்தியை மேம்படுத்தி தொழில்முறையாக செல்வத்தை உருவாக்குவோம்.",
                'beginner': f"வணக்கம் {name}! 🌟 கவலைப்பட வேண்டாம், தனிப்பட்ட நிதியை படிப்படியாக கற்றுத்தருவேன்.",
                'intermediate': f"வணக்கம் {name}! 🚀 உங்கள் நிதி திட்டமிடலை அடுத்த நிலைக்கு கொண்டு செல்ல தயாரா?"
            }
        }
        
        return greetings.get(language, greetings['english']).get(user_type, greetings[language]['beginner'])
    
    def get_suggested_topics(self, profile: Dict, language: str = 'english') -> List[str]:
        """Get suggested topics based on user profile"""
        user_type = profile.get('basic_info', {}).get('user_type', 'beginner')
        
        topics = {
            'english': {
                'student': [
                    "How to budget on a student income?",
                    "Best savings strategies for students",
                    "Managing education loan debt",
                    "Part-time income tax implications"
                ],
                'professional': [
                    "Investment portfolio optimization",
                    "Tax-saving investment options",
                    "Retirement planning strategies",
                    "Real estate investment advice"
                ],
                'beginner': [
                    "How to create my first budget?",
                    "What is an emergency fund?",
                    "Basic investment concepts",
                    "How to track expenses?"
                ],
                'intermediate': [
                    "Advanced budgeting techniques",
                    "Diversification strategies",
                    "Tax optimization methods",
                    "Goal-based financial planning"
                ]
            },
            'tamil': {
                'student': [
                    "மாணவர் வருமானத்தில் எப்படி பட்ஜெட் செய்வது?",
                    "மாணவர்களுக்கான சிறந்த சேமிப்பு வழிகள்",
                    "கல்விக் கடன் நிர்வாகம்",
                    "பகுதி நேர வருமான வரி விளைவுகள்"
                ],
                'professional': [
                    "முதலீட்டு போர்ட்ஃபோலியோ மேம்பாடு",
                    "வரி சேமிப்பு முதலீட்டு விருப்பங்கள்",
                    "ஓய்வூதிய திட்டமிடல் உத்திகள்",
                    "ரியல் எஸ்டேட் முதலீட்டு ஆலோசனை"
                ],
                'beginner': [
                    "எனது முதல் பட்ஜெட்டை எப்படி உருவாக்குவது?",
                    "அவசர நிதி என்றால் என்ன?",
                    "அடிப்படை முதலீட்டு கருத்துகள்",
                    "செலவுகளை எப்படி கண்காணிப்பது?"
                ],
                'intermediate': [
                    "மேம்பட்ட பட்ஜெட்டிங் நுட்பங்கள்",
                    "பல்வகைப்படுத்தல் உத்திகள்",
                    "வரி மேம்பாட்டு முறைகள்",
                    "இலக்கு அடிப்படையிலான நிதி திட்டமிடல்"
                ]
            }
        }
        
        return topics.get(language, topics['english']).get(user_type, topics[language]['beginner'])
    
    def get_user_type_info(self, user_type: str) -> Dict:
        """Get detailed information about a user type"""
        return self.user_types.get(user_type, self.user_types['beginner'])
    
    def update_progress(self, profile: Dict, milestone: str) -> Dict:
        """Update user progress"""
        if 'progress' not in profile:
            profile['progress'] = {}
        
        profile['progress'][milestone] = True
        profile['progress']['last_updated'] = datetime.now().isoformat()
        
        return profile
    
    def get_next_steps(self, profile: Dict, language: str = 'english') -> List[str]:
        """Get personalized next steps for the user"""
        progress = profile.get('progress', {})
        user_type = profile.get('basic_info', {}).get('user_type', 'beginner')
        
        next_steps = {
            'english': {
                'not_onboarded': [
                    "Complete your profile setup",
                    "Set your financial goals",
                    "Upload your transaction data"
                ],
                'onboarded_no_data': [
                    "Upload your transaction data for analysis",
                    "Explore budget analysis features",
                    "Set up smart alerts"
                ],
                'data_uploaded': [
                    "Review your budget analysis",
                    "Check smart financial alerts",
                    "Generate your first PDF report"
                ]
            },
            'tamil': {
                'not_onboarded': [
                    "உங்கள் சுயவிவர அமைப்பை முடிக்கவும்",
                    "உங்கள் நிதி இலக்குகளை அமைக்கவும்",
                    "உங்கள் பரிவர்த்தனை தரவைப் பதிவேற்றவும்"
                ],
                'onboarded_no_data': [
                    "பகுப்பாய்விற்காக உங்கள் பரிவர்த்தனை தரவைப் பதிவேற்றவும்",
                    "பட்ஜெட் பகுப்பாய்வு அம்சங்களை ஆராயுங்கள்",
                    "ஸ்மார்ட் எச்சரிக்கைகளை அமைக்கவும்"
                ],
                'data_uploaded': [
                    "உங்கள் பட்ஜெட் பகுப்பாய்வை மதிப்பாய்வு செய்யுங்கள்",
                    "ஸ்மார்ட் நிதி எச்சரிக்கைகளைச் சரிபார்க்கவும்",
                    "உங்கள் முதல் PDF அறிக்கையை உருவாக்கவும்"
                ]
            }
        }
        
        # Determine user's current stage
        if not progress.get('onboarding_completed', False):
            stage = 'not_onboarded'
        elif not progress.get('data_uploaded', False):
            stage = 'onboarded_no_data'
        else:
            stage = 'data_uploaded'
        
        return next_steps.get(language, next_steps['english']).get(stage, [])
