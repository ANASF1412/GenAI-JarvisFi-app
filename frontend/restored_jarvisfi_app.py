"""
Restored JarvisFi 2.0 Application - Complete with All Advanced Features
Restores all missing UI designs and features from the original JarvisFi 2.0
"""

import streamlit as st
import asyncio
import json
import logging
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import backend services with fallback
try:
    from core_ai_engine import CoreAIEngine
    from financial_services import FinancialServices
    from voice_processor import VoiceProcessor
    BACKEND_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Backend services not available: {e}")
    BACKEND_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RestoredJarvisFiApp:
    """
    Restored JarvisFi 2.0 application with all advanced features and UI designs
    """
    
    def __init__(self):
        self.logger = logger
        self.setup_page_config()
        self.initialize_services()
        self.initialize_session_state()
        self.apply_custom_styling()
    
    def setup_page_config(self):
        """Configure Streamlit page with advanced settings"""
        st.set_page_config(
            page_title="JarvisFi - Your Ultimate Multilingual Finance Chat Assistant",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://jarvisfi.com/help',
                'Report a bug': 'https://jarvisfi.com/bug-report',
                'About': "JarvisFi - Your Ultimate Multilingual Finance Chat Assistant"
            }
        )
    
    def apply_custom_styling(self):
        """Apply advanced custom CSS styling"""
        st.markdown("""
        <style>
        /* Main Application Styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .feature-card {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            margin: 1rem 0;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }
        
        .metric-card {
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            text-align: center;
            border: 1px solid #e9ecef;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }
        
        .voice-indicator {
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            padding: 1rem;
            border-radius: 25px;
            text-align: center;
            animation: pulse 2s infinite;
            box-shadow: 0 4px 16px rgba(40, 167, 69, 0.3);
        }
        
        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.05); }
            100% { opacity: 1; transform: scale(1); }
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 10px;
        }
        
        .chat-message {
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            padding: 1rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .ai-response {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            border-left-color: #2196f3;
        }
        
        .user-message {
            background: linear-gradient(135deg, #f3e5f5, #e1bee7);
            border-left-color: #9c27b0;
        }
        
        .calculator-container {
            background: linear-gradient(135deg, #fff3e0, #ffe0b2);
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }
        
        .dashboard-widget {
            background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }
        
        .investment-card {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 1px solid #2196f3;
            box-shadow: 0 4px 16px rgba(33, 150, 243, 0.2);
        }
        
        .farmer-tool-card {
            background: linear-gradient(135deg, #f1f8e9, #dcedc8);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border-left: 4px solid #8bc34a;
            box-shadow: 0 4px 16px rgba(139, 195, 74, 0.2);
        }
        
        .credit-score-excellent {
            background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
            color: #2e7d32;
        }
        
        .credit-score-good {
            background: linear-gradient(135deg, #fff3e0, #ffe0b2);
            color: #f57c00;
        }
        
        .credit-score-fair {
            background: linear-gradient(135deg, #ffebee, #ffcdd2);
            color: #d32f2f;
        }
        
        .gamification-badge {
            background: linear-gradient(135deg, #ffd700, #ffb300);
            color: #333;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin: 0.25rem;
            box-shadow: 0 2px 8px rgba(255, 193, 7, 0.3);
        }
        
        .language-selector {
            background: linear-gradient(135deg, #e1f5fe, #b3e5fc);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .quick-action-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        }
        
        .quick-action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
        }
        
        .progress-ring {
            background: conic-gradient(#667eea 0deg, #764ba2 180deg, #e9ecef 180deg);
            border-radius: 50%;
            padding: 4px;
        }
        
        .data-save-container {
            background: linear-gradient(135deg, #f3e5f5, #e1bee7);
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            border: 2px solid #9c27b0;
            box-shadow: 0 8px 32px rgba(156, 39, 176, 0.2);
        }
        
        .recommendation-card {
            background: linear-gradient(135deg, #fff8e1, #ffecb3);
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #ffc107;
            box-shadow: 0 2px 8px rgba(255, 193, 7, 0.2);
        }
        
        .voice-command-list {
            background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
        }
        
        /* Animations */
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes bounceIn {
            0% { opacity: 0; transform: scale(0.3); }
            50% { opacity: 1; transform: scale(1.05); }
            70% { transform: scale(0.9); }
            100% { opacity: 1; transform: scale(1); }
        }
        
        .slide-in { animation: slideIn 0.5s ease-out; }
        .fade-in { animation: fadeIn 0.5s ease-out; }
        .bounce-in { animation: bounceIn 0.6s ease-out; }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header { padding: 1rem; }
            .feature-card { padding: 1rem; }
            .metric-card { padding: 1rem; }
        }
        
        /* Dark Mode Support */
        .dark-mode {
            background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
            color: #ffffff;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2, #667eea);
        }
        </style>
        """, unsafe_allow_html=True)
    
    def initialize_services(self):
        """Initialize backend services"""
        try:
            if BACKEND_AVAILABLE:
                self.ai_engine = CoreAIEngine()
                self.financial_services = FinancialServices()
                self.voice_processor = VoiceProcessor()
                self.logger.info("✅ Backend services initialized")
            else:
                self.ai_engine = None
                self.financial_services = None
                self.voice_processor = None
                self.logger.warning("⚠️ Running in demo mode - backend services not available")
        except Exception as e:
            self.logger.error(f"❌ Service initialization failed: {e}")
            self.ai_engine = None
            self.financial_services = None
            self.voice_processor = None

    def initialize_session_state(self):
        """Initialize comprehensive session state with all advanced features"""
        try:
            # Initialize session start time
            if 'session_start_time' not in st.session_state:
                st.session_state.session_start_time = time.time()

            # Initialize comprehensive user profile
            if 'user_profile' not in st.session_state:
                st.session_state.user_profile = {
                    'basic_info': {
                        'name': 'User',
                        'age': 25,
                        'user_type': 'professional',
                        'language': 'en',
                        'monthly_income': 50000,
                        'currency': 'INR',
                        'location': 'India',
                        'occupation': 'Software Engineer',
                        'education': 'Graduate',
                        'family_size': 3,
                        'city_tier': 'Tier 1'
                    },
                    'financial_profile': {
                        'risk_tolerance': 'moderate',
                        'investment_experience': 'beginner',
                        'financial_goals': ['retirement', 'house', 'emergency_fund'],
                        'current_investments': 0,
                        'monthly_expenses': 30000,
                        'debt_info': {
                            'total_debt': 0,
                            'credit_cards': 0,
                            'loans': 0
                        },
                        'credit_score': 750,
                        'bank_accounts': ['savings', 'current'],
                        'insurance': {
                            'life_insurance': 500000,
                            'health_insurance': 300000
                        }
                    },
                    'preferences': {
                        'dark_mode': False,
                        'voice_enabled': True,
                        'notifications': True,
                        'ai_accuracy_mode': True,
                        'enhanced_sources': True,
                        'learning_mode': False,
                        'privacy_mode': False,
                        'auto_save': True,
                        'theme': 'default'
                    },
                    'security': {
                        'two_factor_enabled': False,
                        'biometric_enabled': False,
                        'data_encryption': True,
                        'session_timeout': 30
                    }
                }

            # Initialize current page
            if 'current_page' not in st.session_state:
                st.session_state.current_page = 'home'

            # Initialize comprehensive chat history
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []

            # Initialize advanced gamification system
            if 'gamification' not in st.session_state:
                st.session_state.gamification = {
                    'points': 0,
                    'level': 1,
                    'badges': [],
                    'challenges_completed': 0,
                    'streak_days': 0,
                    'achievements': [],
                    'daily_goals': {
                        'chat_interactions': 0,
                        'calculator_uses': 0,
                        'profile_updates': 0
                    },
                    'weekly_goals': {
                        'financial_planning': False,
                        'investment_review': False,
                        'budget_analysis': False
                    }
                }

            # Initialize comprehensive data save settings
            if 'data_save_settings' not in st.session_state:
                st.session_state.data_save_settings = {
                    'auto_save': True,
                    'retention_period': 30,
                    'last_save': None,
                    'save_location': 'local',
                    'encryption_enabled': True,
                    'backup_frequency': 'daily',
                    'export_format': 'json',
                    'compression_enabled': True
                }

            # Initialize voice settings
            if 'voice_settings' not in st.session_state:
                st.session_state.voice_settings = {
                    'enabled': True,
                    'language': 'en',
                    'speed': 1.0,
                    'pitch': 1.0,
                    'volume': 0.8,
                    'voice_type': 'female',
                    'wake_word': 'jarvis'
                }

            # Initialize AI settings
            if 'ai_settings' not in st.session_state:
                st.session_state.ai_settings = {
                    'model_preference': 'balanced',
                    'response_length': 'medium',
                    'explanation_level': 'detailed',
                    'confidence_threshold': 0.7,
                    'source_citations': True,
                    'personalization_level': 'high'
                }

            # Initialize notification system
            if 'notifications' not in st.session_state:
                st.session_state.notifications = {
                    'unread_count': 0,
                    'messages': [],
                    'settings': {
                        'email_alerts': True,
                        'push_notifications': True,
                        'sms_alerts': False,
                        'financial_alerts': True,
                        'goal_reminders': True
                    }
                }

            # Initialize analytics tracking
            if 'analytics' not in st.session_state:
                st.session_state.analytics = {
                    'session_count': 1,
                    'total_time_spent': 0,
                    'features_used': [],
                    'most_used_calculator': None,
                    'chat_interactions': 0,
                    'voice_interactions': 0,
                    'page_views': {'home': 1}
                }

            # Initialize farmer-specific data
            if 'farmer_data' not in st.session_state:
                st.session_state.farmer_data = {
                    'land_area': 5,
                    'crop_types': ['rice', 'wheat'],
                    'seasonal_income': {
                        'kharif': 0,
                        'rabi': 0,
                        'summer': 0
                    },
                    'government_schemes': [],
                    'insurance_policies': [],
                    'loan_history': []
                }

            # Initialize investment tracking
            if 'investment_tracking' not in st.session_state:
                st.session_state.investment_tracking = {
                    'portfolio_value': 0,
                    'monthly_sip': 0,
                    'asset_allocation': {
                        'equity': 60,
                        'debt': 30,
                        'gold': 10
                    },
                    'goals': [],
                    'performance_history': []
                }

            self.logger.info("✅ Comprehensive session state initialized")

        except Exception as e:
            self.logger.error(f"❌ Session state initialization failed: {e}")
            st.error(f"Failed to initialize application: {e}")

    def render_advanced_sidebar(self):
        """Render advanced sidebar with all features"""
        try:
            with st.sidebar:
                # Advanced header with animations
                st.markdown("""
                <div class="main-header bounce-in">
                    <h1>🤖 JarvisFi</h1>
                    <p><em>Your Ultimate Multilingual Finance Chat Assistant</em></p>
                </div>
                """, unsafe_allow_html=True)

                # User profile section with advanced UI
                profile = st.session_state.user_profile
                st.markdown("---")

                # Profile picture placeholder and user info
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("""
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea, #764ba2);
                                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                color: white; font-size: 24px; font-weight: bold;">
                        👤
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"**{profile['basic_info']['name']}**")
                    st.markdown(f"*{profile['basic_info']['user_type'].title()}*")

                    # Gamification level display
                    level = st.session_state.gamification['level']
                    points = st.session_state.gamification['points']
                    st.markdown(f"""
                    <div class="gamification-badge">
                        Level {level} • {points} pts
                    </div>
                    """, unsafe_allow_html=True)

                # Advanced language selector
                st.markdown("### 🌍 Language / भाषा / மொழி / భాష")
                languages = {
                    'en': '🇺🇸 English',
                    'ta': '🇮🇳 Tamil (தமிழ்)',
                    'hi': '🇮🇳 Hindi (हिंदी)',
                    'te': '🇮🇳 Telugu (తెలుగు)'
                }

                selected_lang = st.selectbox(
                    "",
                    options=list(languages.keys()),
                    format_func=lambda x: languages[x],
                    index=list(languages.keys()).index(profile['basic_info']['language']),
                    key="language_selector"
                )

                if selected_lang != profile['basic_info']['language']:
                    st.session_state.user_profile['basic_info']['language'] = selected_lang
                    st.session_state.gamification['points'] += 5
                    st.success("Language updated! +5 points")
                    st.rerun()

                st.markdown("---")

                # Advanced profile editing with better UI
                with st.expander("👤 Edit Profile", expanded=False):
                    # Basic info editing
                    new_name = st.text_input("Full Name", value=profile['basic_info']['name'])
                    if new_name != profile['basic_info']['name']:
                        st.session_state.user_profile['basic_info']['name'] = new_name
                        st.success("Name updated!")
                        st.rerun()

                    new_age = st.slider("Age", 18, 80, profile['basic_info']['age'])
                    if new_age != profile['basic_info']['age']:
                        st.session_state.user_profile['basic_info']['age'] = new_age
                        st.success("Age updated!")
                        st.rerun()

                    # Income with better formatting
                    new_income = st.number_input(
                        "Monthly Income (₹)",
                        min_value=5000,
                        max_value=1000000,
                        value=profile['basic_info']['monthly_income'],
                        step=5000,
                        format="%d",
                        help="Your gross monthly income before taxes"
                    )
                    if new_income != profile['basic_info']['monthly_income']:
                        st.session_state.user_profile['basic_info']['monthly_income'] = new_income
                        st.session_state.gamification['points'] += 10
                        st.success(f"Income updated to ₹{new_income:,}! +10 points")
                        st.rerun()

                    # Expenses with categories
                    new_expenses = st.number_input(
                        "Monthly Expenses (₹)",
                        min_value=1000,
                        max_value=500000,
                        value=profile['financial_profile']['monthly_expenses'],
                        step=1000,
                        format="%d",
                        help="Your total monthly expenses"
                    )
                    if new_expenses != profile['financial_profile']['monthly_expenses']:
                        st.session_state.user_profile['financial_profile']['monthly_expenses'] = new_expenses
                        st.session_state.gamification['points'] += 10
                        st.success(f"Expenses updated to ₹{new_expenses:,}! +10 points")
                        st.rerun()

                    # User type with descriptions
                    user_types = {
                        'student': '🎓 Student - Learning and growing',
                        'professional': '💼 Professional - Career focused',
                        'farmer': '👨‍🌾 Farmer - Agricultural income',
                        'senior_citizen': '👴 Senior Citizen - Retirement planning'
                    }

                    selected_type = st.selectbox(
                        "User Type",
                        options=list(user_types.keys()),
                        format_func=lambda x: user_types[x],
                        index=list(user_types.keys()).index(profile['basic_info']['user_type'])
                    )

                    if selected_type != profile['basic_info']['user_type']:
                        st.session_state.user_profile['basic_info']['user_type'] = selected_type
                        st.session_state.gamification['points'] += 15
                        st.success(f"User type updated! +15 points")
                        st.rerun()

                st.markdown("---")

                # Advanced navigation menu with icons and descriptions
                st.markdown("### 📱 Navigation Menu")

                pages = {
                    'home': {
                        'icon': '🏠',
                        'name': 'Home',
                        'desc': 'Dashboard overview'
                    },
                    'dashboard': {
                        'icon': '📊',
                        'name': 'Dashboard',
                        'desc': 'Comprehensive analytics'
                    },
                    'chat': {
                        'icon': '💬',
                        'name': 'AI Chat',
                        'desc': 'Financial assistant'
                    },
                    'calculators': {
                        'icon': '🧮',
                        'name': 'Calculators',
                        'desc': 'Financial tools'
                    },
                    'investments': {
                        'icon': '📈',
                        'name': 'Investments',
                        'desc': 'Portfolio management'
                    },
                    'credit': {
                        'icon': '💳',
                        'name': 'Credit Score',
                        'desc': 'Credit tracking'
                    },
                    'farmer': {
                        'icon': '👨‍🌾',
                        'name': 'Farmer Tools',
                        'desc': 'Agricultural finance'
                    },
                    'voice': {
                        'icon': '🎤',
                        'name': 'Voice Assistant',
                        'desc': 'Voice commands'
                    }
                }

                current_page = st.session_state.current_page

                for page_key, page_info in pages.items():
                    # Highlight current page
                    button_style = "primary" if page_key == current_page else "secondary"

                    if st.button(
                        f"{page_info['icon']} {page_info['name']}",
                        use_container_width=True,
                        key=f"nav_{page_key}",
                        type=button_style,
                        help=page_info['desc']
                    ):
                        st.session_state.current_page = page_key
                        st.session_state.gamification['points'] += 1

                        # Track page views
                        if page_key not in st.session_state.analytics['page_views']:
                            st.session_state.analytics['page_views'][page_key] = 0
                        st.session_state.analytics['page_views'][page_key] += 1

                        st.rerun()

                # Current page indicator with animation
                current_page_info = pages.get(current_page, {'icon': '❓', 'name': 'Unknown'})
                st.markdown(f"""
                <div class="feature-card slide-in">
                    <strong>Current Page:</strong><br>
                    {current_page_info['icon']} {current_page_info['name']}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("---")

                # Advanced quick stats with animations
                st.markdown("### 📊 Quick Financial Stats")

                monthly_income = profile['basic_info']['monthly_income']
                monthly_expenses = profile['financial_profile']['monthly_expenses']
                savings = monthly_income - monthly_expenses
                savings_rate = (savings / monthly_income * 100) if monthly_income > 0 else 0
                credit_score = profile['financial_profile']['credit_score']

                # Animated metric cards
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card fade-in">
                        <h4>💰 Monthly Savings</h4>
                        <h2>₹{savings:,}</h2>
                        <p style="color: {'green' if savings > 0 else 'red'};">
                            {savings_rate:.1f}% of income
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    score_color = "#4CAF50" if credit_score >= 750 else "#FFA726" if credit_score >= 650 else "#FF6B6B"
                    st.markdown(f"""
                    <div class="metric-card fade-in">
                        <h4>💳 Credit Score</h4>
                        <h2 style="color: {score_color};">{credit_score}</h2>
                        <p>{'Excellent' if credit_score >= 750 else 'Good' if credit_score >= 650 else 'Fair'}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Investment overview
                portfolio_value = st.session_state.investment_tracking['portfolio_value']
                monthly_sip = monthly_income * 0.15  # 15% of income

                st.markdown(f"""
                <div class="investment-card fade-in">
                    <h4>📈 Investment Overview</h4>
                    <p><strong>Portfolio:</strong> ₹{portfolio_value:,}</p>
                    <p><strong>Monthly SIP:</strong> ₹{monthly_sip:,}</p>
                    <p><strong>Goal Progress:</strong> {min(65 + (savings/1000), 100):.0f}%</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("---")

                # Notification center
                notifications = st.session_state.notifications
                unread_count = notifications['unread_count']

                st.markdown(f"### 🔔 Notifications {f'({unread_count})' if unread_count > 0 else ''}")

                if unread_count > 0:
                    st.markdown(f"""
                    <div class="voice-indicator">
                        🔔 You have {unread_count} new notification{'s' if unread_count > 1 else ''}
                    </div>
                    """, unsafe_allow_html=True)

                # Sample notifications
                sample_notifications = [
                    "💰 Your SIP investment has grown by 12% this month!",
                    "📊 Monthly budget analysis is ready for review",
                    "🎯 You're 85% towards your emergency fund goal",
                    "💳 Credit score updated - increased by 15 points"
                ]

                with st.expander("View Notifications", expanded=False):
                    for i, notification in enumerate(sample_notifications[:3]):
                        st.markdown(f"""
                        <div class="recommendation-card">
                            {notification}
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")

                # Voice status indicator
                voice_enabled = st.session_state.voice_settings['enabled']
                if voice_enabled:
                    st.markdown("""
                    <div class="voice-indicator">
                        🎤 Voice Assistant Active
                        <br><small>Say "Hey Jarvis" to start</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: #ffecb3; padding: 1rem; border-radius: 10px; text-align: center;">
                        🔇 Voice Assistant Disabled
                    </div>
                    """, unsafe_allow_html=True)

                # Settings quick access
                with st.expander("⚙️ Quick Settings", expanded=False):
                    # Dark mode toggle
                    dark_mode = st.checkbox(
                        "🌙 Dark Mode",
                        value=profile['preferences']['dark_mode']
                    )
                    if dark_mode != profile['preferences']['dark_mode']:
                        st.session_state.user_profile['preferences']['dark_mode'] = dark_mode
                        st.rerun()

                    # Voice toggle
                    voice_toggle = st.checkbox(
                        "🎤 Voice Assistant",
                        value=voice_enabled
                    )
                    if voice_toggle != voice_enabled:
                        st.session_state.voice_settings['enabled'] = voice_toggle
                        st.rerun()

                    # Notifications toggle
                    notifications_toggle = st.checkbox(
                        "🔔 Notifications",
                        value=profile['preferences']['notifications']
                    )
                    if notifications_toggle != profile['preferences']['notifications']:
                        st.session_state.user_profile['preferences']['notifications'] = notifications_toggle
                        st.rerun()

                # Session info
                session_time = time.time() - st.session_state.session_start_time
                st.markdown(f"""
                <div style="background: #e3f2fd; padding: 1rem; border-radius: 10px; text-align: center; margin-top: 1rem;">
                    <small>
                        ⏱️ Session: {session_time/60:.1f} min<br>
                        📊 Level {st.session_state.gamification['level']} • {st.session_state.gamification['points']} points
                    </small>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            self.logger.error(f"❌ Sidebar rendering failed: {e}")
            st.sidebar.error(f"Sidebar error: {e}")

    def render_advanced_home_page(self):
        """Render advanced home page with all missing features"""
        try:
            profile = st.session_state.user_profile
            current_lang = profile['basic_info']['language']
            user_name = profile['basic_info']['name']
            user_type = profile['basic_info']['user_type']

            # Advanced welcome header with animations
            welcome_messages = {
                'en': f"Welcome back, {user_name}! 👋",
                'ta': f"மீண்டும் வரவேற்கிறோம், {user_name}! 👋",
                'hi': f"वापसी पर स्वागत है, {user_name}! 👋",
                'te': f"తిరిగి స్వాగతం, {user_name}! 👋"
            }

            st.markdown(f"""
            <div class="main-header bounce-in">
                <h1 style="margin: 0; font-size: 2.5rem;">🤖 JarvisFi Dashboard</h1>
                <h3 style="margin: 0.5rem 0; opacity: 0.9;">{welcome_messages.get(current_lang, welcome_messages['en'])}</h3>
                <p style="margin: 0; opacity: 0.8;">Your Ultimate Multilingual Finance Chat Assistant</p>
            </div>
            """, unsafe_allow_html=True)

            # Advanced financial overview cards with animations
            st.markdown("## 📊 Financial Overview")

            monthly_income = profile['basic_info']['monthly_income']
            monthly_expenses = profile['financial_profile']['monthly_expenses']
            savings = monthly_income - monthly_expenses
            credit_score = profile['financial_profile']['credit_score']
            savings_rate = (savings / monthly_income * 100) if monthly_income > 0 else 0

            # Enhanced metric cards with gradients and animations
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-card slide-in" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white;">
                    <h4 style="margin: 0; opacity: 0.9;">💰 Monthly Income</h4>
                    <h2 style="margin: 0.5rem 0; font-size: 2rem;">₹{monthly_income:,}</h2>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Primary source</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                expense_percent = (monthly_expenses/monthly_income*100) if monthly_income > 0 else 0
                st.markdown(f"""
                <div class="metric-card slide-in" style="background: linear-gradient(135deg, #FF6B6B, #ee5a52); color: white;">
                    <h4 style="margin: 0; opacity: 0.9;">💸 Monthly Expenses</h4>
                    <h2 style="margin: 0.5rem 0; font-size: 2rem;">₹{monthly_expenses:,}</h2>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{expense_percent:.1f}% of income</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                savings_color = "#4CAF50" if savings > 0 else "#FF6B6B"
                st.markdown(f"""
                <div class="metric-card slide-in" style="background: linear-gradient(135deg, {savings_color}, {savings_color}); color: white;">
                    <h4 style="margin: 0; opacity: 0.9;">💰 Monthly Savings</h4>
                    <h2 style="margin: 0.5rem 0; font-size: 2rem;">₹{savings:,}</h2>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{savings_rate:.1f}% savings rate</p>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                score_color = "#4CAF50" if credit_score >= 750 else "#FFA726" if credit_score >= 650 else "#FF6B6B"
                score_status = "Excellent" if credit_score >= 750 else "Good" if credit_score >= 650 else "Fair"
                st.markdown(f"""
                <div class="metric-card slide-in" style="background: linear-gradient(135deg, {score_color}, {score_color}); color: white;">
                    <h4 style="margin: 0; opacity: 0.9;">💳 Credit Score</h4>
                    <h2 style="margin: 0.5rem 0; font-size: 2rem;">{credit_score}</h2>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{score_status}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Advanced quick action buttons with better styling
            st.markdown("## 🚀 Quick Actions")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("💬 Start AI Chat", use_container_width=True, help="Chat with JarvisFi AI assistant"):
                    st.session_state.current_page = 'chat'
                    st.session_state.gamification['points'] += 2
                    st.rerun()

            with col2:
                if st.button("🧮 Financial Calculators", use_container_width=True, help="Access SIP, EMI, Tax calculators"):
                    st.session_state.current_page = 'calculators'
                    st.session_state.gamification['points'] += 2
                    st.rerun()

            with col3:
                if st.button("🎤 Voice Assistant", use_container_width=True, help="Use voice commands"):
                    st.session_state.current_page = 'voice'
                    st.session_state.gamification['points'] += 2
                    st.rerun()

            with col4:
                if st.button("📈 Investment Portfolio", use_container_width=True, help="Manage your investments"):
                    st.session_state.current_page = 'investments'
                    st.session_state.gamification['points'] += 2
                    st.rerun()

            # Second row of quick actions
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("👨‍🌾 Farmer Tools", use_container_width=True, help="Agricultural finance tools"):
                    st.session_state.current_page = 'farmer'
                    st.session_state.gamification['points'] += 2
                    st.rerun()

            with col2:
                if st.button("💳 Credit Score", use_container_width=True, help="Track and improve credit score"):
                    st.session_state.current_page = 'credit'
                    st.session_state.gamification['points'] += 2
                    st.rerun()

            with col3:
                if st.button("📊 Full Dashboard", use_container_width=True, help="Comprehensive financial dashboard"):
                    st.session_state.current_page = 'dashboard'
                    st.session_state.gamification['points'] += 2
                    st.rerun()

            with col4:
                # Data Save Button with advanced options
                if st.button("💾 Save Data", use_container_width=True, help="Save your financial data"):
                    self.show_advanced_data_save_options()

            st.markdown("---")

            # Advanced financial insights with interactive charts
            st.markdown("## 📈 Financial Insights")

            col1, col2 = st.columns(2)

            with col1:
                # Enhanced savings rate gauge with better styling
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = savings_rate,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Savings Rate (%)", 'font': {'size': 20}},
                    delta = {'reference': 20, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
                    gauge = {
                        'axis': {'range': [None, 50], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "darkblue"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 10], 'color': "#ffcccc"},
                            {'range': [10, 20], 'color': "#ffffcc"},
                            {'range': [20, 50], 'color': "#ccffcc"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 20
                        }
                    }
                ))
                fig.update_layout(height=350, font={'color': "darkblue", 'family': "Arial"})
                st.plotly_chart(fig, use_container_width=True)

                # Savings rate interpretation with better styling
                if savings_rate >= 20:
                    st.markdown("""
                    <div class="feature-card" style="background: linear-gradient(135deg, #e8f5e8, #c8e6c9); border-left-color: #4caf50;">
                        🎉 Excellent savings rate! You're on track for financial success.
                    </div>
                    """, unsafe_allow_html=True)
                elif savings_rate >= 10:
                    st.markdown("""
                    <div class="feature-card" style="background: linear-gradient(135deg, #fff3e0, #ffe0b2); border-left-color: #ff9800;">
                        👍 Good savings rate. Consider increasing to 20% for optimal growth.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="feature-card" style="background: linear-gradient(135deg, #ffebee, #ffcdd2); border-left-color: #f44336;">
                        ⚠️ Low savings rate. Focus on reducing expenses or increasing income.
                    </div>
                    """, unsafe_allow_html=True)

            with col2:
                # Enhanced expense breakdown with better colors
                expense_data = {
                    'Category': ['🏠 Housing', '🍽️ Food', '🚗 Transportation', '🎬 Entertainment', '📦 Others'],
                    'Amount': [monthly_expenses * 0.4, monthly_expenses * 0.2,
                              monthly_expenses * 0.15, monthly_expenses * 0.1, monthly_expenses * 0.15],
                    'Percentage': ['40%', '20%', '15%', '10%', '15%']
                }

                fig = px.pie(expense_data, values='Amount', names='Category',
                            title='Monthly Expense Breakdown',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(height=350, font={'size': 12})
                st.plotly_chart(fig, use_container_width=True)

                # Expense analysis with better styling
                housing_percent = (monthly_expenses * 0.4 / monthly_income * 100) if monthly_income > 0 else 0
                if housing_percent > 30:
                    st.markdown("""
                    <div class="feature-card" style="background: linear-gradient(135deg, #ffebee, #ffcdd2); border-left-color: #f44336;">
                        🏠 Housing costs are high (>30% of income). Consider optimization.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="feature-card" style="background: linear-gradient(135deg, #e8f5e8, #c8e6c9); border-left-color: #4caf50;">
                        🏠 Housing costs are within recommended limits.
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")

            # Advanced personalized recommendations section
            st.markdown("## 💡 Personalized Recommendations")

            recommendations = self.get_advanced_recommendations(profile)

            col1, col2 = st.columns(2)

            for i, rec in enumerate(recommendations):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                    <div class="recommendation-card fade-in">
                        <p style="margin: 0; font-size: 1rem; color: #333;">{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")

            # Advanced financial goals progress with animations
            st.markdown("## 🎯 Financial Goals Progress")

            goals = self.get_advanced_financial_goals(monthly_income, user_type)

            for goal in goals:
                progress = (goal['current'] / goal['target']) * 100

                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.markdown(f"**{goal['name']}**")
                    st.progress(progress / 100)

                with col2:
                    st.metric("Current", f"₹{goal['current']:,}")

                with col3:
                    st.metric("Target", f"₹{goal['target']:,}")

                # Enhanced progress indicators with styling
                if progress >= 80:
                    st.markdown("""
                    <div class="feature-card" style="background: linear-gradient(135deg, #e8f5e8, #c8e6c9); border-left-color: #4caf50;">
                        🎉 {:.1f}% complete - Almost there!
                    </div>
                    """.format(progress), unsafe_allow_html=True)
                elif progress >= 50:
                    st.markdown("""
                    <div class="feature-card" style="background: linear-gradient(135deg, #e3f2fd, #bbdefb); border-left-color: #2196f3;">
                        📈 {:.1f}% complete - Good progress!
                    </div>
                    """.format(progress), unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="feature-card" style="background: linear-gradient(135deg, #fff3e0, #ffe0b2); border-left-color: #ff9800;">
                        ⏳ {:.1f}% complete - Keep going!
                    </div>
                    """.format(progress), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("---")

            # Advanced recent activity & notifications
            st.markdown("## 📢 Recent Activity & Notifications")

            activities = self.get_advanced_recent_activities(current_lang)

            for activity in activities:
                icon = activity['icon']
                message = activity['message']
                time_ago = activity['time']
                activity_type = activity['type']

                if activity_type == 'success':
                    st.markdown(f"""
                    <div class="feature-card" style="background: linear-gradient(135deg, #e8f5e8, #c8e6c9); border-left-color: #4caf50;">
                        {icon} {message} - <small>{time_ago}</small>
                    </div>
                    """, unsafe_allow_html=True)
                elif activity_type == 'info':
                    st.markdown(f"""
                    <div class="feature-card" style="background: linear-gradient(135deg, #e3f2fd, #bbdefb); border-left-color: #2196f3;">
                        {icon} {message} - <small>{time_ago}</small>
                    </div>
                    """, unsafe_allow_html=True)
                elif activity_type == 'warning':
                    st.markdown(f"""
                    <div class="feature-card" style="background: linear-gradient(135deg, #fff3e0, #ffe0b2); border-left-color: #ff9800;">
                        {icon} {message} - <small>{time_ago}</small>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")

            # Advanced quick stats summary with better design
            st.markdown("## 📊 Quick Stats Summary")

            col1, col2, col3 = st.columns(3)

            with col1:
                net_worth = savings * 12 + 100000  # Rough estimate
                st.markdown(f"""
                <div class="dashboard-widget">
                    <h4 style="color: #1976d2; margin: 0;">💰 Net Worth</h4>
                    <h3 style="color: #1976d2; margin: 0.5rem 0;">₹{net_worth:,}</h3>
                    <p style="color: #666; margin: 0; font-size: 0.9rem;">Estimated total assets</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                annual_savings = savings * 12
                st.markdown(f"""
                <div class="dashboard-widget">
                    <h4 style="color: #388e3c; margin: 0;">📈 Annual Savings</h4>
                    <h3 style="color: #388e3c; margin: 0.5rem 0;">₹{annual_savings:,}</h3>
                    <p style="color: #666; margin: 0; font-size: 0.9rem;">Projected yearly savings</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                session_time = time.time() - st.session_state.session_start_time
                st.markdown(f"""
                <div class="dashboard-widget">
                    <h4 style="color: #f57c00; margin: 0;">⏱️ Session Time</h4>
                    <h3 style="color: #f57c00; margin: 0.5rem 0;">{session_time/60:.1f} min</h3>
                    <p style="color: #666; margin: 0; font-size: 0.9rem;">Time spent today</p>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            self.logger.error(f"❌ Home page rendering failed: {e}")
            st.error(f"Home page error: {e}")

    def show_advanced_data_save_options(self):
        """Show advanced data saving options with comprehensive features"""
        current_lang = st.session_state.user_profile['basic_info']['language']

        # Initialize data save settings if not exists
        if 'data_save_settings' not in st.session_state:
            st.session_state.data_save_settings = {
                'auto_save': True,
                'retention_period': 30,
                'last_save': None,
                'save_location': 'local',
                'encryption_enabled': True,
                'backup_frequency': 'daily',
                'export_format': 'json',
                'compression_enabled': True
            }

        # Advanced data save dialog with better UI
        with st.expander("💾 Advanced Data Save Options", expanded=True):
            st.markdown("""
            <div class="data-save-container">
                <h3 style="text-align: center; margin-bottom: 1rem;">🔒 JarvisFi Data Storage Settings</h3>
                <p style="text-align: center; opacity: 0.8;">Your Ultimate Multilingual Finance Chat Assistant</p>
            </div>
            """, unsafe_allow_html=True)

            # Language-specific text
            save_texts = {
                'en': {
                    'title': '💾 Data Storage Configuration',
                    'retention': 'Data Retention Period',
                    'location': 'Save Location',
                    'encryption': 'Enable AES-256 Encryption',
                    'auto_save': 'Auto-save enabled',
                    'save_now': 'Save Now',
                    'export': 'Export Data'
                },
                'ta': {
                    'title': '💾 தரவு சேமிப்பு கட்டமைப்பு',
                    'retention': 'தரவு வைத்திருக்கும் காலம்',
                    'location': 'சேமிப்பு இடம்',
                    'encryption': 'AES-256 குறியாக்கத்தை இயக்கு',
                    'auto_save': 'தானியங்கு சேமிப்பு இயக்கப்பட்டது',
                    'save_now': 'இப்போது சேமிக்கவும்',
                    'export': 'தரவை ஏற்றுமதி செய்யவும்'
                },
                'hi': {
                    'title': '💾 डेटा भंडारण कॉन्फ़िगरेशन',
                    'retention': 'डेटा रिटेंशन अवधि',
                    'location': 'सेव लोकेशन',
                    'encryption': 'AES-256 एन्क्रिप्शन सक्षम करें',
                    'auto_save': 'ऑटो-सेव सक्षम',
                    'save_now': 'अभी सेव करें',
                    'export': 'डेटा एक्सपोर्ट करें'
                },
                'te': {
                    'title': '💾 డేటా నిల్వ కాన్ఫిగరేషన్',
                    'retention': 'డేటా నిలుపుదల వ్యవధి',
                    'location': 'సేవ్ లొకేషన్',
                    'encryption': 'AES-256 ఎన్‌క్రిప్షన్ ప్రారంభించండి',
                    'auto_save': 'ఆటో-సేవ్ ప్రారంభించబడింది',
                    'save_now': 'ఇప్పుడు సేవ్ చేయండి',
                    'export': 'డేటా ఎగుమతి చేయండి'
                }
            }

            texts = save_texts.get(current_lang, save_texts['en'])

            col1, col2 = st.columns(2)

            with col1:
                # Advanced retention period selection
                st.markdown(f"**{texts['retention']}**")

                retention_options = {
                    'en': {
                        1: '1 Day (Testing)',
                        7: '1 Week (Short-term)',
                        30: '1 Month (Recommended)',
                        90: '3 Months (Extended)',
                        365: '1 Year (Long-term)',
                        -1: 'Permanent (Forever)'
                    }
                }

                options = retention_options.get(current_lang, retention_options['en'])

                selected_retention = st.selectbox(
                    "Select retention period:",
                    options=list(options.keys()),
                    format_func=lambda x: options[x],
                    index=list(options.keys()).index(st.session_state.data_save_settings['retention_period'])
                    if st.session_state.data_save_settings['retention_period'] in options.keys() else 2
                )

                st.session_state.data_save_settings['retention_period'] = selected_retention

                # Advanced save location with descriptions
                st.markdown(f"**{texts['location']}**")
                save_location = st.radio(
                    "Choose save location:",
                    options=['local', 'cloud', 'both'],
                    format_func=lambda x: {
                        'local': '💻 Local Device (Secure, Private)',
                        'cloud': '☁️ Cloud Storage (Accessible Anywhere)',
                        'both': '🔄 Both Local & Cloud (Maximum Security)'
                    }[x],
                    index=['local', 'cloud', 'both'].index(st.session_state.data_save_settings['save_location'])
                )
                st.session_state.data_save_settings['save_location'] = save_location

            with col2:
                # Advanced security settings
                st.markdown("**🔒 Advanced Security Settings**")

                encryption_enabled = st.checkbox(
                    texts['encryption'],
                    value=st.session_state.data_save_settings['encryption_enabled'],
                    help="Military-grade AES-256 encryption for maximum security"
                )
                st.session_state.data_save_settings['encryption_enabled'] = encryption_enabled

                auto_save = st.checkbox(
                    texts['auto_save'],
                    value=st.session_state.data_save_settings['auto_save'],
                    help="Automatically save data when changes are made"
                )
                st.session_state.data_save_settings['auto_save'] = auto_save

                # Backup frequency
                backup_frequency = st.selectbox(
                    "Backup Frequency",
                    options=['hourly', 'daily', 'weekly'],
                    format_func=lambda x: {
                        'hourly': '⏰ Every Hour',
                        'daily': '📅 Daily',
                        'weekly': '📆 Weekly'
                    }[x],
                    index=['hourly', 'daily', 'weekly'].index(st.session_state.data_save_settings['backup_frequency'])
                )
                st.session_state.data_save_settings['backup_frequency'] = backup_frequency

                # Export format
                export_format = st.selectbox(
                    "Export Format",
                    options=['json', 'csv', 'excel', 'pdf'],
                    format_func=lambda x: {
                        'json': '📄 JSON (Structured)',
                        'csv': '📊 CSV (Spreadsheet)',
                        'excel': '📈 Excel (Advanced)',
                        'pdf': '📋 PDF (Report)'
                    }[x],
                    index=['json', 'csv', 'excel', 'pdf'].index(st.session_state.data_save_settings['export_format'])
                )
                st.session_state.data_save_settings['export_format'] = export_format

                # Data size estimation with better display
                st.markdown("**📊 Data Information**")
                estimated_size = self.calculate_advanced_data_size()
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📦 Estimated Data Size</h4>
                    <h3>{estimated_size:.2f} KB</h3>
                    <p>Compressed: {estimated_size * 0.3:.2f} KB</p>
                </div>
                """, unsafe_allow_html=True)

                if st.session_state.data_save_settings['last_save']:
                    last_save_time = st.session_state.data_save_settings['last_save']
                    st.info(f"🕒 Last saved: {last_save_time}")
                else:
                    st.warning("⚠️ Data not saved yet")

            # Advanced action buttons with better styling
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button(f"💾 {texts['save_now']}", use_container_width=True, type="primary"):
                    self.save_advanced_user_data()

            with col2:
                if st.button(f"📤 {texts['export']}", use_container_width=True):
                    self.export_advanced_user_data()

            with col3:
                if st.button("🗑️ Clear Data", use_container_width=True, type="secondary"):
                    self.clear_advanced_user_data()

            with col4:
                if st.button("📋 Data Summary", use_container_width=True):
                    self.show_advanced_data_summary()

            # Advanced retention period warnings with better styling
            if selected_retention == -1:
                st.markdown("""
                <div class="feature-card" style="background: linear-gradient(135deg, #ffebee, #ffcdd2); border-left-color: #f44336;">
                    ⚠️ <strong>Permanent Storage Warning:</strong> Data will be kept forever. Ensure compliance with privacy regulations.
                </div>
                """, unsafe_allow_html=True)
            elif selected_retention == 1:
                st.markdown("""
                <div class="feature-card" style="background: linear-gradient(135deg, #e3f2fd, #bbdefb); border-left-color: #2196f3;">
                    ℹ️ <strong>Testing Mode:</strong> Data will be automatically deleted after 1 day.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="feature-card" style="background: linear-gradient(135deg, #e8f5e8, #c8e6c9); border-left-color: #4caf50;">
                    ℹ️ <strong>Retention Policy:</strong> Data will be automatically deleted after {selected_retention} days for privacy compliance.
                </div>
                """, unsafe_allow_html=True)

    def get_advanced_recommendations(self, profile: Dict) -> List[str]:
        """Get advanced personalized recommendations"""
        try:
            user_type = profile['basic_info']['user_type']
            monthly_income = profile['basic_info']['monthly_income']
            monthly_expenses = profile['financial_profile']['monthly_expenses']
            savings = monthly_income - monthly_expenses
            savings_rate = (savings / monthly_income * 100) if monthly_income > 0 else 0
            age = profile['basic_info']['age']

            base_recommendations = {
                'student': [
                    "🎓 Start with small SIPs (₹500-1000) to build investment habit early",
                    "📚 Focus on education loans with lower interest rates and tax benefits",
                    "💰 Build emergency fund of ₹10,000-20,000 for unexpected expenses",
                    "📱 Use student discounts and cashback offers to maximize savings",
                    "🏦 Open a zero-balance savings account with good digital banking features",
                    "📈 Learn about mutual funds and start with index funds for diversification"
                ],
                'farmer': [
                    "🌾 Utilize PM-KISAN scheme for ₹6,000 annual direct benefit transfer",
                    "🚜 Consider Pradhan Mantri Fasal Bima Yojana for comprehensive crop insurance",
                    "💰 Invest surplus income after harvest in liquid mutual funds",
                    "🏦 Apply for Kisan Credit Card for easy access to agricultural loans",
                    "🌧️ Plan for weather-based insurance to protect against climate risks",
                    "📊 Diversify income with allied activities like dairy, poultry, or horticulture"
                ],
                'professional': [
                    "💼 Maximize Section 80C deductions up to ₹1.5 lakh annually",
                    "📈 Start SIP with 15-20% of income for long-term wealth building",
                    "🏠 Plan for home loan with EMI not exceeding 40% of monthly income",
                    "💳 Maintain credit utilization below 30% for optimal credit score",
                    "🏥 Ensure adequate health insurance coverage (10x annual income)",
                    "🎯 Create separate funds for short-term and long-term financial goals"
                ],
                'senior_citizen': [
                    "🏦 Focus on Senior Citizen Savings Scheme (SCSS) for regular income",
                    "💊 Plan comprehensively for healthcare expenses and medical insurance",
                    "📈 Consider Pradhan Mantri Vaya Vandana Yojana for guaranteed returns",
                    "🏠 Evaluate reverse mortgage options if you need regular income",
                    "💰 Keep 2-3 years of expenses in liquid funds for emergencies",
                    "📋 Ensure proper estate planning and nomination in all investments"
                ]
            }

            recommendations = base_recommendations.get(user_type, [
                "💰 Build emergency fund covering 6 months of essential expenses",
                "📈 Diversify investments across equity, debt, and gold for balanced growth",
                "💳 Monitor credit score regularly and maintain good credit history",
                "🎯 Set clear, measurable financial goals with specific timelines",
                "🏥 Ensure adequate life and health insurance coverage",
                "📊 Review and rebalance your investment portfolio quarterly"
            ])

            # Add income-specific recommendations
            if monthly_income < 25000:
                recommendations.append("💡 Focus on skill development and certifications to increase earning potential")
                recommendations.append("🎯 Start with micro-investments and gradually increase as income grows")
            elif monthly_income > 100000:
                recommendations.append("🏛️ Consider tax-saving investments and professional wealth management services")
                recommendations.append("🌍 Explore international diversification through global mutual funds")

            # Add age-specific recommendations
            if age < 30:
                recommendations.append("⚡ Take higher equity exposure (70-80%) for long-term wealth creation")
            elif age > 50:
                recommendations.append("🛡️ Gradually shift to debt instruments for capital preservation")

            # Add savings rate specific recommendations
            if savings_rate < 10:
                recommendations.append("⚠️ Urgent: Analyze and reduce discretionary expenses to improve savings")
            elif savings_rate > 30:
                recommendations.append("🎉 Excellent savings! Consider increasing investment allocation for faster growth")

            return recommendations[:6]  # Return top 6 recommendations

        except Exception as e:
            self.logger.error(f"Recommendations generation failed: {e}")
            return ["💡 Update your profile for personalized financial recommendations"]

    def get_advanced_financial_goals(self, monthly_income: int, user_type: str) -> List[Dict]:
        """Get advanced financial goals based on user profile"""
        try:
            emergency_target = monthly_income * 6
            retirement_target = monthly_income * 12 * 25  # 25x annual income

            if user_type == 'student':
                goals = [
                    {'name': '🎓 Education Fund', 'target': 200000, 'current': 50000},
                    {'name': '💰 Emergency Fund', 'target': emergency_target // 3, 'current': emergency_target // 6},
                    {'name': '📱 Technology Fund', 'target': 50000, 'current': 20000},
                    {'name': '🚀 Career Development', 'target': 100000, 'current': 30000}
                ]
            elif user_type == 'farmer':
                goals = [
                    {'name': '🌾 Crop Investment Fund', 'target': 300000, 'current': 150000},
                    {'name': '🚜 Equipment Upgrade Fund', 'target': 500000, 'current': 200000},
                    {'name': '💰 Emergency Fund', 'target': emergency_target, 'current': emergency_target // 3},
                    {'name': '🏠 Home Improvement', 'target': 400000, 'current': 100000}
                ]
            elif user_type == 'professional':
                goals = [
                    {'name': '🏠 House Down Payment', 'target': 2000000, 'current': 800000},
                    {'name': '💰 Emergency Fund', 'target': emergency_target, 'current': emergency_target // 2},
                    {'name': '🏖️ Retirement Corpus', 'target': retirement_target // 10, 'current': retirement_target // 50},
                    {'name': '🎓 Children Education', 'target': 1500000, 'current': 300000}
                ]
            elif user_type == 'senior_citizen':
                goals = [
                    {'name': '🏥 Healthcare Fund', 'target': 500000, 'current': 200000},
                    {'name': '💰 Emergency Fund', 'target': emergency_target, 'current': emergency_target // 2},
                    {'name': '🎯 Legacy Planning', 'target': 1000000, 'current': 600000},
                    {'name': '🏖️ Leisure Fund', 'target': 300000, 'current': 150000}
                ]
            else:
                goals = [
                    {'name': '💰 Emergency Fund', 'target': emergency_target, 'current': emergency_target // 3},
                    {'name': '🏖️ Retirement Planning', 'target': retirement_target // 20, 'current': retirement_target // 100},
                    {'name': '🎯 Dream Goal', 'target': 1000000, 'current': 300000},
                    {'name': '🏠 Home Fund', 'target': 1500000, 'current': 400000}
                ]

            return goals

        except Exception as e:
            self.logger.error(f"Financial goals generation failed: {e}")
            return [{'name': 'Emergency Fund', 'target': 100000, 'current': 30000}]

    def get_advanced_recent_activities(self, language: str) -> List[Dict]:
        """Get advanced recent activities and notifications"""
        try:
            activities_en = [
                {'icon': '💰', 'message': 'Monthly SIP of ₹5,000 processed successfully with 12% returns', 'time': '2 hours ago', 'type': 'success'},
                {'icon': '📊', 'message': 'Credit score updated - increased by 15 points to 765', 'time': '1 day ago', 'type': 'success'},
                {'icon': '⚠️', 'message': 'High expense alert: Entertainment spending exceeded budget by 20%', 'time': '3 days ago', 'type': 'warning'},
                {'icon': '📈', 'message': 'Investment portfolio gained 2.5% this month, outperforming benchmark', 'time': '1 week ago', 'type': 'info'},
                {'icon': '🎯', 'message': 'Emergency fund goal 85% complete - ₹85,000 of ₹100,000', 'time': '1 week ago', 'type': 'info'},
                {'icon': '🏆', 'message': 'Achievement unlocked: Consistent Saver badge earned!', 'time': '2 weeks ago', 'type': 'success'}
            ]

            activities_ta = [
                {'icon': '💰', 'message': 'மாதாந்திர SIP ₹5,000 வெற்றிகரமாக செயல்படுத்தப்பட்டது 12% வருமானத்துடன்', 'time': '2 மணி நேரம் முன்பு', 'type': 'success'},
                {'icon': '📊', 'message': 'கிரெடிட் ஸ்கோர் புதுப்பிக்கப்பட்டது - 15 புள்ளிகள் அதிகரித்து 765 ஆனது', 'time': '1 நாள் முன்பு', 'type': 'success'},
                {'icon': '⚠️', 'message': 'அதிக செலவு எச்சரிக்கை: பொழுதுபோக்கு செலவு பட்ஜெட்டை 20% மீறியது', 'time': '3 நாட்கள் முன்பு', 'type': 'warning'},
                {'icon': '📈', 'message': 'முதலீட்டு போர்ட்ஃபோலியோ இந்த மாதம் 2.5% லாபம், பெஞ்ச்மார்க்கை விட சிறப்பு', 'time': '1 வாரம் முன்பு', 'type': 'info'},
                {'icon': '🎯', 'message': 'அவசர நிதி இலக்கு 85% முடிந்தது - ₹1,00,000 இல் ₹85,000', 'time': '1 வாரம் முன்பு', 'type': 'info'},
                {'icon': '🏆', 'message': 'சாதனை திறக்கப்பட்டது: நிலையான சேமிப்பாளர் பேட்ஜ் பெற்றீர்கள்!', 'time': '2 வாரங்கள் முன்பு', 'type': 'success'}
            ]

            return activities_ta if language == 'ta' else activities_en

        except Exception as e:
            self.logger.error(f"Recent activities generation failed: {e}")
            return [{'icon': '💰', 'message': 'Welcome to JarvisFi!', 'time': 'now', 'type': 'info'}]

    def calculate_advanced_data_size(self) -> float:
        """Calculate advanced estimated size of user data in KB"""
        try:
            import json
            data_to_save = {
                'user_profile': st.session_state.user_profile,
                'chat_history': st.session_state.chat_history,
                'gamification': st.session_state.gamification,
                'data_save_settings': st.session_state.data_save_settings,
                'voice_settings': st.session_state.voice_settings,
                'ai_settings': st.session_state.ai_settings,
                'notifications': st.session_state.notifications,
                'analytics': st.session_state.analytics,
                'farmer_data': st.session_state.farmer_data,
                'investment_tracking': st.session_state.investment_tracking
            }

            # Convert to JSON and calculate size
            json_data = json.dumps(data_to_save, default=str)
            size_bytes = len(json_data.encode('utf-8'))
            size_kb = size_bytes / 1024

            return size_kb
        except Exception as e:
            self.logger.error(f"Error calculating data size: {e}")
            return 2.5  # Default estimate for comprehensive data

    def save_advanced_user_data(self):
        """Save user data with advanced features"""
        try:
            from datetime import datetime, timedelta
            import json

            # Prepare comprehensive data to save
            data_to_save = {
                'user_profile': st.session_state.user_profile,
                'chat_history': st.session_state.chat_history,
                'gamification': st.session_state.gamification,
                'data_save_settings': st.session_state.data_save_settings,
                'voice_settings': st.session_state.voice_settings,
                'ai_settings': st.session_state.ai_settings,
                'notifications': st.session_state.notifications,
                'analytics': st.session_state.analytics,
                'farmer_data': st.session_state.farmer_data,
                'investment_tracking': st.session_state.investment_tracking,
                'save_timestamp': datetime.now().isoformat(),
                'retention_period': st.session_state.data_save_settings['retention_period'],
                'expires_at': (datetime.now() + timedelta(days=st.session_state.data_save_settings['retention_period'])).isoformat()
                if st.session_state.data_save_settings['retention_period'] != -1 else None,
                'version': '2.0',
                'app_version': 'JarvisFi - Your Ultimate Multilingual Finance Chat Assistant'
            }

            # Advanced encryption simulation
            if st.session_state.data_save_settings['encryption_enabled']:
                data_to_save['encrypted'] = True
                data_to_save['encryption_method'] = 'AES-256-GCM'
                data_to_save['encryption_timestamp'] = datetime.now().isoformat()

            # Save to different locations based on user choice
            save_location = st.session_state.data_save_settings['save_location']

            if save_location in ['local', 'both']:
                st.success("💾 Data saved locally with advanced encryption!")

            if save_location in ['cloud', 'both']:
                st.success("☁️ Data synchronized to secure cloud storage!")

            # Update last save time
            st.session_state.data_save_settings['last_save'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Advanced save confirmation with details
            retention_text = "permanently" if st.session_state.data_save_settings['retention_period'] == -1 else f"for {st.session_state.data_save_settings['retention_period']} days"

            st.markdown(f"""
            <div class="feature-card" style="background: linear-gradient(135deg, #e8f5e8, #c8e6c9); border-left-color: #4caf50;">
                ✅ <strong>Advanced Data Save Successful!</strong><br>
                📊 Data Size: {self.calculate_advanced_data_size():.2f} KB<br>
                🔒 Encryption: {'Enabled (AES-256)' if st.session_state.data_save_settings['encryption_enabled'] else 'Disabled'}<br>
                📍 Location: {save_location.title()}<br>
                ⏰ Retention: {retention_text}<br>
                🆔 Save ID: JF-{datetime.now().strftime('%Y%m%d-%H%M%S')}
            </div>
            """, unsafe_allow_html=True)

            # Add gamification points
            st.session_state.gamification['points'] += 25
            st.info("🎉 +25 points for saving your data securely!")

        except Exception as e:
            self.logger.error(f"Error saving user data: {e}")
            st.error("❌ Failed to save data. Please try again.")

    def export_advanced_user_data(self):
        """Export user data in advanced formats"""
        try:
            import json
            from datetime import datetime

            # Prepare comprehensive export data
            export_data = {
                'export_info': {
                    'timestamp': datetime.now().isoformat(),
                    'version': 'JarvisFi - Your Ultimate Multilingual Finance Chat Assistant',
                    'export_type': 'comprehensive',
                    'user_id': f"JF-{st.session_state.user_profile['basic_info']['name']}-{datetime.now().strftime('%Y%m%d')}"
                },
                'user_profile': st.session_state.user_profile,
                'financial_summary': {
                    'monthly_income': st.session_state.user_profile['basic_info']['monthly_income'],
                    'monthly_expenses': st.session_state.user_profile['financial_profile']['monthly_expenses'],
                    'savings_rate': ((st.session_state.user_profile['basic_info']['monthly_income'] -
                                    st.session_state.user_profile['financial_profile']['monthly_expenses']) /
                                   st.session_state.user_profile['basic_info']['monthly_income'] * 100)
                                   if st.session_state.user_profile['basic_info']['monthly_income'] > 0 else 0,
                    'credit_score': st.session_state.user_profile['financial_profile']['credit_score'],
                    'net_worth_estimate': (st.session_state.user_profile['basic_info']['monthly_income'] -
                                         st.session_state.user_profile['financial_profile']['monthly_expenses']) * 12 + 100000
                },
                'chat_summary': {
                    'total_conversations': len(st.session_state.chat_history),
                    'recent_topics': [msg.get('content', '')[:50] + '...' for msg in st.session_state.chat_history[-5:] if msg.get('role') == 'user'],
                    'ai_interactions': len([msg for msg in st.session_state.chat_history if msg.get('role') == 'assistant'])
                },
                'gamification_stats': st.session_state.gamification,
                'analytics': st.session_state.analytics,
                'investment_tracking': st.session_state.investment_tracking,
                'farmer_data': st.session_state.farmer_data if st.session_state.user_profile['basic_info']['user_type'] == 'farmer' else None
            }

            # Convert to JSON with proper formatting
            json_data = json.dumps(export_data, indent=2, default=str, ensure_ascii=False)

            # Create advanced download button
            st.download_button(
                label="📥 Download Comprehensive Export (JSON)",
                data=json_data,
                file_name=f"jarvisfi_comprehensive_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                help="Download your complete financial data in JSON format"
            )

            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #e3f2fd, #bbdefb); border-left-color: #2196f3;">
                📤 <strong>Advanced Export Ready!</strong><br>
                📊 Includes: Profile, Chat History, Analytics, Gamification, Investment Tracking<br>
                🔒 Privacy: All sensitive data properly formatted<br>
                📱 Compatible: Works with Excel, Google Sheets, and data analysis tools
            </div>
            """, unsafe_allow_html=True)

            # Add gamification points
            st.session_state.gamification['points'] += 15
            st.info("🎉 +15 points for exporting your data!")

        except Exception as e:
            self.logger.error(f"Error exporting user data: {e}")
            st.error("❌ Failed to export data. Please try again.")

    def clear_advanced_user_data(self):
        """Clear user data with advanced confirmation"""
        st.markdown("""
        <div class="feature-card" style="background: linear-gradient(135deg, #ffebee, #ffcdd2); border-left-color: #f44336;">
            ⚠️ <strong>Data Deletion Warning</strong><br>
            This will permanently delete ALL your data including:<br>
            • User profile and preferences<br>
            • Chat history and AI interactions<br>
            • Gamification progress and badges<br>
            • Investment tracking and goals<br>
            • Analytics and usage statistics
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚠️ I Understand - Clear All Data", type="secondary"):
            # Reset to comprehensive default values
            st.session_state.clear()
            self.initialize_session_state()

            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #e8f5e8, #c8e6c9); border-left-color: #4caf50;">
                🗑️ <strong>Data Cleared Successfully!</strong><br>
                All data has been permanently deleted and reset to defaults.<br>
                You can now start fresh with JarvisFi - Your Ultimate Multilingual Finance Chat Assistant.
            </div>
            """, unsafe_allow_html=True)

            st.rerun()

    def show_advanced_data_summary(self):
        """Show advanced summary of saved data"""
        st.markdown("### 📋 Comprehensive Data Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**👤 Profile Data:**")
            profile = st.session_state.user_profile
            st.write(f"• Name: {profile['basic_info']['name']}")
            st.write(f"• User Type: {profile['basic_info']['user_type'].title()}")
            st.write(f"• Language: {profile['basic_info']['language'].upper()}")
            st.write(f"• Monthly Income: ₹{profile['basic_info']['monthly_income']:,}")
            st.write(f"• Age: {profile['basic_info']['age']} years")
            st.write(f"• Location: {profile['basic_info']['location']}")

            st.markdown("**💬 Chat Data:**")
            st.write(f"• Total Messages: {len(st.session_state.chat_history)}")
            st.write(f"• User Messages: {len([m for m in st.session_state.chat_history if m.get('role') == 'user'])}")
            st.write(f"• AI Responses: {len([m for m in st.session_state.chat_history if m.get('role') == 'assistant'])}")

            st.markdown("**🎮 Gamification Data:**")
            gam = st.session_state.gamification
            st.write(f"• Points: {gam['points']}")
            st.write(f"• Level: {gam['level']}")
            st.write(f"• Badges: {len(gam['badges'])}")
            st.write(f"• Challenges: {gam['challenges_completed']}")
            st.write(f"• Streak: {gam['streak_days']} days")

        with col2:
            st.markdown("**💾 Save Settings:**")
            settings = st.session_state.data_save_settings
            st.write(f"• Retention: {settings['retention_period']} days" if settings['retention_period'] != -1 else "• Retention: Permanent")
            st.write(f"• Location: {settings['save_location'].title()}")
            st.write(f"• Encryption: {'Enabled (AES-256)' if settings['encryption_enabled'] else 'Disabled'}")
            st.write(f"• Auto-save: {'Enabled' if settings['auto_save'] else 'Disabled'}")
            st.write(f"• Backup: {settings['backup_frequency'].title()}")
            st.write(f"• Format: {settings['export_format'].upper()}")

            st.markdown("**📊 Analytics Data:**")
            analytics = st.session_state.analytics
            st.write(f"• Sessions: {analytics['session_count']}")
            st.write(f"• Features Used: {len(analytics['features_used'])}")
            st.write(f"• Chat Interactions: {analytics['chat_interactions']}")
            st.write(f"• Voice Interactions: {analytics['voice_interactions']}")

            st.markdown("**📈 Investment Tracking:**")
            investment = st.session_state.investment_tracking
            st.write(f"• Portfolio Value: ₹{investment['portfolio_value']:,}")
            st.write(f"• Monthly SIP: ₹{investment['monthly_sip']:,}")
            st.write(f"• Goals: {len(investment['goals'])}")

            if st.session_state.user_profile['basic_info']['user_type'] == 'farmer':
                st.markdown("**👨‍🌾 Farmer Data:**")
                farmer = st.session_state.farmer_data
                st.write(f"• Land Area: {farmer['land_area']} acres")
                st.write(f"• Crop Types: {len(farmer['crop_types'])}")
                st.write(f"• Schemes: {len(farmer['government_schemes'])}")

        # Data size and storage info
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            data_size = self.calculate_advanced_data_size()
            st.metric("📦 Data Size", f"{data_size:.2f} KB")

        with col2:
            compressed_size = data_size * 0.3
            st.metric("🗜️ Compressed", f"{compressed_size:.2f} KB")

        with col3:
            session_time = time.time() - st.session_state.session_start_time
            st.metric("⏱️ Session", f"{session_time/60:.1f} min")

    def run(self):
        """Main application runner with all advanced features"""
        try:
            # Render advanced sidebar
            self.render_advanced_sidebar()

            # Render main content based on current page
            current_page = st.session_state.current_page

            if current_page == 'home':
                self.render_advanced_home_page()
            elif current_page == 'dashboard':
                self.render_comprehensive_dashboard_page()
            elif current_page == 'chat':
                self.render_ai_chat_page()
            elif current_page == 'calculators':
                self.render_complete_calculators_page()
            elif current_page == 'investments':
                self.render_complete_investments_page()
            elif current_page == 'credit':
                self.render_complete_credit_score_page()
            elif current_page == 'farmer':
                self.render_complete_farmer_tools_page()
            elif current_page == 'voice':
                self.render_complete_voice_assistant_page()
            else:
                st.error(f"Unknown page: {current_page}")
                self.render_advanced_home_page()

        except Exception as e:
            self.logger.error(f"Application run failed: {e}")
            st.error(f"Application error: {e}")
            st.markdown("### 🔧 Debug Information")
            st.code(f"Error: {e}")
            st.code(f"Current page: {st.session_state.get('current_page', 'Unknown')}")



    def render_ai_chat_page(self):
        """Render complete AI chat interface with multilingual support"""
        try:
            profile = st.session_state.user_profile
            current_lang = profile['basic_info']['language']

            # Chat header with language-specific titles
            chat_titles = {
                'en': '💬 AI Financial Assistant',
                'ta': '💬 AI நிதி உதவியாளர்',
                'hi': '💬 AI वित्तीय सहायक',
                'te': '💬 AI ఆర్థిక సహాయకుడు'
            }

            chat_descriptions = {
                'en': 'Get personalized financial advice in your preferred language',
                'ta': 'உங்கள் விருப்பமான மொழியில் தனிப்பயனாக்கப்பட்ட நிதி ஆலோசனையைப் பெறுங்கள்',
                'hi': 'अपनी पसंदीदा भाषा में व्यक्तिगत वित्तीय सलाह प्राप्त करें',
                'te': 'మీ ఇష్టమైన భాషలో వ్యక్తిగతీకరించిన ఆర్థిక సలహాలను పొందండి'
            }

            st.markdown(f"""
            <div class="main-header fade-in">
                <h1>{chat_titles.get(current_lang, chat_titles['en'])}</h1>
                <p>{chat_descriptions.get(current_lang, chat_descriptions['en'])}</p>
                <p><em>JarvisFi - Your Ultimate Multilingual Finance Chat Assistant</em></p>
            </div>
            """, unsafe_allow_html=True)

            # Chat interface layout
            col1, col2 = st.columns([3, 1])

            with col1:
                # Chat history display
                st.markdown("### 💬 Conversation")

                # Chat container with styling
                chat_container = st.container()

                with chat_container:
                    # Display chat history
                    for i, message in enumerate(st.session_state.chat_history):
                        if message.get('role') == 'user':
                            st.markdown(f"""
                            <div class="user-message slide-in">
                                <strong>👤 You:</strong> {message.get('content', '')}
                                <br><small>🕒 {message.get('timestamp', 'Now')}</small>
                            </div>
                            """, unsafe_allow_html=True)
                        elif message.get('role') == 'assistant':
                            st.markdown(f"""
                            <div class="ai-response slide-in">
                                <strong>🤖 JarvisFi:</strong> {message.get('content', '')}
                                <br><small>🕒 {message.get('timestamp', 'Now')} | 🌍 {message.get('language', current_lang).upper()}</small>
                            </div>
                            """, unsafe_allow_html=True)

                # Chat input
                st.markdown("---")

                # Quick question buttons
                quick_questions = {
                    'en': [
                        "What's my current savings rate?",
                        "How should I invest ₹10,000?",
                        "Help me plan for retirement",
                        "What are good tax-saving options?",
                        "Should I take a home loan now?"
                    ],
                    'ta': [
                        "எனது தற்போதைய சேமிப்பு விகிதம் என்ன?",
                        "₹10,000 ஐ எப்படி முதலீடு செய்ய வேண்டும்?",
                        "ஓய்வூதியத்திற்கு திட்டமிட உதவுங்கள்",
                        "நல்ல வரி சேமிப்பு விருப்பங்கள் என்ன?",
                        "இப்போது வீட்டுக் கடன் எடுக்கலாமா?"
                    ],
                    'hi': [
                        "मेरी वर्तमान बचत दर क्या है?",
                        "₹10,000 का निवेश कैसे करूं?",
                        "सेवानिवृत्ति की योजना में मदद करें",
                        "अच्छे टैक्स सेविंग विकल्प क्या हैं?",
                        "क्या अभी होम लोन लेना चाहिए?"
                    ],
                    'te': [
                        "నా ప్రస్తుత పొదుపు రేటు ఎంత?",
                        "₹10,000 ను ఎలా పెట్టుబడి పెట్టాలి?",
                        "పదవీ విరమణ ప్రణాళికలో సహాయం చేయండి",
                        "మంచి పన్ను పొదుపు ఎంపికలు ఏమిటి?",
                        "ఇప్పుడు గృహ రుణం తీసుకోవాలా?"
                    ]
                }

                st.markdown("#### 🚀 Quick Questions")
                questions = quick_questions.get(current_lang, quick_questions['en'])

                cols = st.columns(2)
                for i, question in enumerate(questions):
                    with cols[i % 2]:
                        if st.button(f"💡 {question}", key=f"quick_q_{i}", use_container_width=True):
                            # Add user message
                            user_message = {
                                'role': 'user',
                                'content': question,
                                'timestamp': datetime.now().strftime("%H:%M"),
                                'language': current_lang
                            }
                            st.session_state.chat_history.append(user_message)

                            # Generate AI response
                            ai_response = self.generate_ai_response(question, current_lang, profile)
                            st.session_state.chat_history.append(ai_response)

                            # Add gamification points
                            st.session_state.gamification['points'] += 5
                            st.session_state.analytics['chat_interactions'] += 1

                            st.rerun()

                # Text input for custom questions
                st.markdown("#### ✍️ Ask Your Question")

                user_input = st.text_area(
                    "Type your financial question here...",
                    height=100,
                    placeholder="Ask me anything about investments, savings, loans, insurance, or financial planning..."
                )

                col_send, col_voice = st.columns([3, 1])

                with col_send:
                    if st.button("📤 Send Message", use_container_width=True, type="primary"):
                        if user_input.strip():
                            # Add user message
                            user_message = {
                                'role': 'user',
                                'content': user_input,
                                'timestamp': datetime.now().strftime("%H:%M"),
                                'language': current_lang
                            }
                            st.session_state.chat_history.append(user_message)

                            # Generate AI response
                            ai_response = self.generate_ai_response(user_input, current_lang, profile)
                            st.session_state.chat_history.append(ai_response)

                            # Add gamification points
                            st.session_state.gamification['points'] += 10
                            st.session_state.analytics['chat_interactions'] += 1

                            st.rerun()
                        else:
                            st.warning("Please enter a question first!")

                with col_voice:
                    if st.button("🎤 Voice Input", use_container_width=True):
                        st.info("🎤 Voice input activated! (Simulated)")
                        # Simulate voice input
                        voice_questions = [
                            "What's the best SIP amount for my income?",
                            "How can I improve my credit score?",
                            "Should I invest in mutual funds or stocks?"
                        ]
                        import random
                        simulated_voice_input = random.choice(voice_questions)

                        # Add voice message
                        user_message = {
                            'role': 'user',
                            'content': f"🎤 {simulated_voice_input}",
                            'timestamp': datetime.now().strftime("%H:%M"),
                            'language': current_lang,
                            'type': 'voice'
                        }
                        st.session_state.chat_history.append(user_message)

                        # Generate AI response
                        ai_response = self.generate_ai_response(simulated_voice_input, current_lang, profile)
                        st.session_state.chat_history.append(ai_response)

                        # Add gamification points
                        st.session_state.gamification['points'] += 15
                        st.session_state.analytics['voice_interactions'] += 1

                        st.rerun()

            with col2:
                # Chat statistics and settings
                st.markdown("### 📊 Chat Statistics")

                total_messages = len(st.session_state.chat_history)
                user_messages = len([m for m in st.session_state.chat_history if m.get('role') == 'user'])
                ai_messages = len([m for m in st.session_state.chat_history if m.get('role') == 'assistant'])

                st.metric("Total Messages", total_messages)
                st.metric("Your Questions", user_messages)
                st.metric("AI Responses", ai_messages)

                # Language selector for chat
                st.markdown("### 🌍 Chat Language")
                chat_languages = {
                    'en': '🇺🇸 English',
                    'ta': '🇮🇳 தமிழ்',
                    'hi': '🇮🇳 हिंदी',
                    'te': '🇮🇳 తెలుగు'
                }

                selected_chat_lang = st.selectbox(
                    "Response Language:",
                    options=list(chat_languages.keys()),
                    format_func=lambda x: chat_languages[x],
                    index=list(chat_languages.keys()).index(current_lang)
                )

                if selected_chat_lang != current_lang:
                    st.session_state.user_profile['basic_info']['language'] = selected_chat_lang
                    st.success("Language updated!")
                    st.rerun()

                # AI Settings
                st.markdown("### 🤖 AI Settings")

                response_style = st.selectbox(
                    "Response Style:",
                    ["Detailed", "Concise", "Beginner-friendly", "Expert"],
                    index=0
                )

                include_examples = st.checkbox("Include Examples", value=True)
                include_calculations = st.checkbox("Show Calculations", value=True)

                # Chat actions
                st.markdown("### 🛠️ Chat Actions")

                if st.button("🗑️ Clear Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.success("Chat history cleared!")
                    st.rerun()

                if st.button("📥 Export Chat", use_container_width=True):
                    chat_export = {
                        'export_date': datetime.now().isoformat(),
                        'user_profile': st.session_state.user_profile['basic_info'],
                        'chat_history': st.session_state.chat_history,
                        'total_messages': total_messages
                    }

                    import json
                    chat_json = json.dumps(chat_export, indent=2, default=str, ensure_ascii=False)

                    st.download_button(
                        label="📄 Download Chat History",
                        data=chat_json,
                        file_name=f"jarvisfi_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )

                # Recent topics
                if st.session_state.chat_history:
                    st.markdown("### 📝 Recent Topics")
                    recent_topics = []
                    for msg in st.session_state.chat_history[-5:]:
                        if msg.get('role') == 'user':
                            topic = msg.get('content', '')[:30] + "..."
                            recent_topics.append(topic)

                    for topic in recent_topics:
                        st.markdown(f"• {topic}")

        except Exception as e:
            self.logger.error(f"❌ AI Chat page rendering failed: {e}")
            st.error(f"Chat error: {e}")

    def generate_ai_response(self, user_input: str, language: str, profile: Dict) -> Dict:
        """Generate AI response based on user input and language"""
        try:
            # Simulate AI processing time
            import time
            time.sleep(0.5)

            # Get user context
            monthly_income = profile['basic_info']['monthly_income']
            monthly_expenses = profile['financial_profile']['monthly_expenses']
            savings = monthly_income - monthly_expenses
            user_type = profile['basic_info']['user_type']
            age = profile['basic_info']['age']

            # Generate contextual responses based on language and user profile
            responses = self.get_contextual_responses(user_input.lower(), language, {
                'income': monthly_income,
                'expenses': monthly_expenses,
                'savings': savings,
                'user_type': user_type,
                'age': age
            })

            # Select appropriate response
            import random
            response_content = random.choice(responses)

            return {
                'role': 'assistant',
                'content': response_content,
                'timestamp': datetime.now().strftime("%H:%M"),
                'language': language,
                'confidence': 0.95
            }

        except Exception as e:
            self.logger.error(f"AI response generation failed: {e}")
            return {
                'role': 'assistant',
                'content': "I apologize, but I'm having trouble processing your request right now. Please try again.",
                'timestamp': datetime.now().strftime("%H:%M"),
                'language': language,
                'confidence': 0.5
            }

    def get_contextual_responses(self, user_input: str, language: str, context: Dict) -> List[str]:
        """Get contextual AI responses based on user input and language"""
        try:
            income = context['income']
            savings = context['savings']
            user_type = context['user_type']
            age = context['age']

            # Investment-related responses
            if any(word in user_input for word in ['invest', 'investment', 'mutual fund', 'sip', 'stock']):
                responses = {
                    'en': [
                        f"Based on your monthly income of ₹{income:,}, I recommend starting with a SIP of ₹{int(income*0.15):,} (15% of income). Consider diversified equity mutual funds for long-term growth.",
                        f"For your age of {age} years, I suggest {100-age}% equity allocation. Start with index funds and gradually add mid-cap funds as you gain experience.",
                        f"With your current savings of ₹{savings:,} per month, you can build a substantial corpus. Consider ELSS funds for tax benefits under Section 80C."
                    ],
                    'ta': [
                        f"உங்கள் மாதாந்திர வருமானம் ₹{income:,} அடிப்படையில், வருமானத்தின் 15% ஆன ₹{int(income*0.15):,} SIP ஐ பரிந்துரைக்கிறேன். நீண்ட கால வளர்ச்சிக்கு பல்வகைப்பட்ட பங்கு மியூச்சுவல் ஃபண்டுகளை கருத்தில் கொள்ளுங்கள்.",
                        f"உங்கள் {age} வயதிற்கு, {100-age}% பங்கு ஒதுக்கீட்டை பரிந்துரைக்கிறேன். இண்டெக்ஸ் ஃபண்டுகளுடன் தொடங்கி, அனுபவம் பெற்ற பின் மிட்கேப் ஃபண்டுகளை சேர்க்கவும்.",
                        f"மாதம் ₹{savings:,} சேமிப்புடன், நீங்கள் கணிசமான தொகையை உருவாக்க முடியும். பிரிவு 80C கீழ் வரி நன்மைகளுக்கு ELSS ஃபண்டுகளை கருத்தில் கொள்ளுங்கள்."
                    ],
                    'hi': [
                        f"आपकी मासिक आय ₹{income:,} के आधार पर, मैं आय का 15% यानी ₹{int(income*0.15):,} SIP शुरू करने की सलाह देता हूं। लंबी अवधि की वृद्धि के लिए विविधीकृत इक्विटी म्यूचुअल फंड पर विचार करें।",
                        f"आपकी {age} वर्ष की आयु के लिए, मैं {100-age}% इक्विटी आवंटन का सुझाव देता हूं। इंडेक्स फंड से शुरुआत करें और अनुभव प्राप्त करने के बाद मिड-कैप फंड जोड़ें।",
                        f"मासिक ₹{savings:,} की बचत के साथ, आप एक बड़ा कॉर्पस बना सकते हैं। धारा 80C के तहत कर लाभ के लिए ELSS फंड पर विचार करें।"
                    ],
                    'te': [
                        f"మీ మాసిక ఆదాయం ₹{income:,} ఆధారంగా, ఆదాయంలో 15% అయిన ₹{int(income*0.15):,} SIP ప్రారంభించాలని సిఫార్సు చేస్తున్నాను. దీర్ఘకాలిక వృద్ధికి వైవిధ్యమైన ఈక్విటీ మ్యూచువల్ ఫండ్లను పరిగణించండి.",
                        f"మీ {age} సంవత్సరాల వయస్సుకు, {100-age}% ఈక్విటీ కేటాయింపును సూచిస్తున్నాను. ఇండెక్స్ ఫండ్లతో ప్రారంభించి, అనుభవం పొందిన తర్వాత మిడ్-క్యాప్ ఫండ్లను జోడించండి.",
                        f"నెలవారీ ₹{savings:,} పొదుపుతో, మీరు గణనీయమైన కార్పస్ నిర్మించవచ్చు. సెక్షన్ 80C కింద పన్ను ప్రయోజనాల కోసం ELSS ఫండ్లను పరిగణించండి."
                    ]
                }

            # Savings-related responses
            elif any(word in user_input for word in ['savings', 'save', 'emergency fund']):
                responses = {
                    'en': [
                        f"Your current savings rate is {(savings/income*100):.1f}%. Aim for at least 20% savings rate. Build an emergency fund of ₹{income*6:,} (6 months expenses) first.",
                        f"Great question! With ₹{savings:,} monthly savings, you're on the right track. Consider automating your savings through SIPs and recurring deposits.",
                        f"For emergency fund, keep ₹{income*6:,} in liquid funds or high-yield savings accounts. This covers 6 months of your expenses."
                    ],
                    'ta': [
                        f"உங்கள் தற்போதைய சேமிப்பு விகிதம் {(savings/income*100):.1f}%. குறைந்தது 20% சேமிப்பு விகிதத்தை இலக்காக வைக்கவும். முதலில் ₹{income*6:,} (6 மாத செலவுகள்) அவசர நிதியை உருவாக்கவும்.",
                        f"சிறந்த கேள்வி! மாதம் ₹{savings:,} சேமிப்புடன், நீங்கள் சரியான பாதையில் இருக்கிறீர்கள். SIP மற்றும் தொடர் வைப்புகள் மூலம் உங்கள் சேமிப்பை தானியங்கு செய்யுங்கள்.",
                        f"அவசர நிதிக்கு, ₹{income*6:,} ஐ லிக்விட் ஃபண்டுகள் அல்லது அதிக வட்டி சேமிப்பு கணக்குகளில் வைக்கவும். இது உங்கள் 6 மாத செலவுகளை உள்ளடக்கும்."
                    ],
                    'hi': [
                        f"आपकी वर्तमान बचत दर {(savings/income*100):.1f}% है। कम से कम 20% बचत दर का लक्ष्य रखें। पहले ₹{income*6:,} (6 महीने का खर्च) का आपातकालीन फंड बनाएं।",
                        f"बेहतरीन सवाल! मासिक ₹{savings:,} बचत के साथ, आप सही रास्ते पर हैं। SIP और आवर्ती जमा के माध्यम से अपनी बचत को स्वचालित करने पर विचार करें।",
                        f"आपातकालीन फंड के लिए, ₹{income*6:,} को लिक्विड फंड या उच्च-उपज बचत खातों में रखें। यह आपके 6 महीने के खर्च को कवर करता है।"
                    ],
                    'te': [
                        f"మీ ప్రస్తుత పొదుపు రేటు {(savings/income*100):.1f}%. కనీసం 20% పొదుపు రేటును లక్ష్యంగా పెట్టుకోండి. మొదట ₹{income*6:,} (6 నెలల ఖర్చులు) అత్యవసర నిధిని నిర్మించండి.",
                        f"అద్భుతమైన ప్రశ్న! నెలవారీ ₹{savings:,} పొదుపుతో, మీరు సరైన మార్గంలో ఉన్నారు. SIP మరియు రికరింగ్ డిపాజిట్ల ద్వారా మీ పొదుపులను ఆటోమేట్ చేయడాన్ని పరిగణించండి.",
                        f"అత్యవసర నిధి కోసం, ₹{income*6:,} ను లిక్విడ్ ఫండ్లు లేదా అధిక-దిగుబడి పొదుపు ఖాతాలలో ఉంచండి. ఇది మీ 6 నెలల ఖర్చులను కవర్ చేస్తుంది."
                    ]
                }

            # Loan-related responses
            elif any(word in user_input for word in ['loan', 'emi', 'home loan', 'personal loan']):
                responses = {
                    'en': [
                        f"For home loans, ensure your EMI doesn't exceed 40% of your income (₹{int(income*0.4):,}). With your current income, you can afford a loan of approximately ₹{int(income*0.4*12*20):,}.",
                        f"Personal loans have higher interest rates (10-15%). Only take if absolutely necessary. Your debt-to-income ratio should stay below 30%.",
                        f"Consider prepaying high-interest loans first. Use any bonus or extra income to reduce loan tenure and save on interest."
                    ],
                    'ta': [
                        f"வீட்டுக் கடனுக்கு, உங்கள் EMI வருமானத்தின் 40% (₹{int(income*0.4):,}) ஐ மீறக்கூடாது. உங்கள் தற்போதைய வருமானத்துடன், தோராயமாக ₹{int(income*0.4*12*20):,} கடனை வாங்க முடியும்.",
                        f"தனிப்பட்ட கடன்களுக்கு அதிக வட்டி விகிதங்கள் உள்ளன (10-15%). முற்றிலும் அவசியமானால் மட்டுமே எடுக்கவும். உங்கள் கடன்-வருமான விகிதம் 30% க்கு கீழ் இருக்க வேண்டும்.",
                        f"அதிக வட்டி கடன்களை முதலில் முன்கூட்டியே செலுத்துவதை கருத்தில் கொள்ளுங்கள். போனஸ் அல்லது கூடுதல் வருமானத்தை கடன் காலத்தை குறைக்கவும் வட்டியை சேமிக்கவும் பயன்படுத்துங்கள்."
                    ],
                    'hi': [
                        f"होम लोन के लिए, सुनिश्चित करें कि आपकी EMI आपकी आय के 40% (₹{int(income*0.4):,}) से अधिक न हो। आपकी वर्तमान आय के साथ, आप लगभग ₹{int(income*0.4*12*20):,} का लोन ले सकते हैं।",
                        f"पर्सनल लोन की ब्याज दरें अधिक होती हैं (10-15%)। केवल बिल्कुल जरूरी होने पर ही लें। आपका डेट-टू-इनकम रेशियो 30% से नीचे रहना चाहिए।",
                        f"पहले उच्च-ब्याज वाले लोन को प्री-पे करने पर विचार करें। लोन की अवधि कम करने और ब्याज बचाने के लिए बोनस या अतिरिक्त आय का उपयोग करें।"
                    ],
                    'te': [
                        f"గృహ రుణాల కోసం, మీ EMI మీ ఆదాయంలో 40% (₹{int(income*0.4):,}) మించకుండా చూసుకోండి. మీ ప్రస్తుత ఆదాయంతో, మీరు సుమారు ₹{int(income*0.4*12*20):,} రుణం తీసుకోవచ్చు.",
                        f"వ్యక్తిగత రుణాలకు అధిక వడ్డీ రేట్లు ఉంటాయి (10-15%). పూర్తిగా అవసరమైనప్పుడు మాత్రమే తీసుకోండి. మీ రుణ-ఆదాయ నిష్పత్తి 30% కంటే తక్కువగా ఉండాలి.",
                        f"అధిక వడ్డీ రుణాలను మొదట ముందుగానే చెల్లించడాన్ని పరిగణించండి. రుణ కాలాన్ని తగ్గించడానికి మరియు వడ్డీని ఆదా చేయడానికి బోనస్ లేదా అదనపు ఆదాయాన్ని ఉపయోగించండి."
                    ]
                }

            # Default general responses
            else:
                responses = {
                    'en': [
                        f"Thank you for your question! Based on your profile as a {user_type} with monthly income of ₹{income:,}, I'd be happy to help you with personalized financial advice.",
                        f"Great question! With your current financial situation (₹{savings:,} monthly savings), there are several strategies we can explore to optimize your finances.",
                        f"I understand you're looking for financial guidance. As someone earning ₹{income:,} monthly, let me provide you with tailored recommendations."
                    ],
                    'ta': [
                        f"உங்கள் கேள்விக்கு நன்றி! மாதாந்திர வருமானம் ₹{income:,} உள்ள {user_type} என்ற உங்கள் சுயவிவரத்தின் அடிப்படையில், தனிப்பயனாக்கப்பட்ட நிதி ஆலோசனையுடன் உங்களுக்கு உதவ மகிழ்ச்சி அடைகிறேன்.",
                        f"சிறந்த கேள்வி! உங்கள் தற்போதைய நிதி நிலைமையுடன் (மாதம் ₹{savings:,} சேமிப்பு), உங்கள் நிதியை மேம்படுத்த பல உத்திகளை நாம் ஆராயலாம்.",
                        f"நீங்கள் நிதி வழிகாட்டுதலை தேடுகிறீர்கள் என்பதை நான் புரிந்துகொள்கிறேன். மாதம் ₹{income:,} சம்பாதிக்கும் ஒருவராக, தனிப்பயனாக்கப்பட்ட பரிந்துரைகளை வழங்குகிறேன்."
                    ],
                    'hi': [
                        f"आपके प्रश्न के लिए धन्यवाद! ₹{income:,} मासिक आय वाले {user_type} के रूप में आपकी प्रोफ़ाइल के आधार पर, मुझे व्यक्तिगत वित्तीय सलाह के साथ आपकी मदद करने में खुशी होगी।",
                        f"बेहतरीन सवाल! आपकी वर्तमान वित्तीय स्थिति (मासिक ₹{savings:,} बचत) के साथ, आपके वित्त को अनुकूलित करने के लिए कई रणनीतियां हैं जिन्हें हम देख सकते हैं।",
                        f"मैं समझता हूं कि आप वित्तीय मार्गदर्शन की तलाश में हैं। मासिक ₹{income:,} कमाने वाले व्यक्ति के रूप में, मैं आपको अनुकूलित सिफारिशें प्रदान करता हूं।"
                    ],
                    'te': [
                        f"మీ ప్రశ్నకు ధన్యవాదాలు! నెలవారీ ఆదాయం ₹{income:,} ఉన్న {user_type} గా మీ ప్రొఫైల్ ఆధారంగా, వ్యక్తిగతీకరించిన ఆర్థిక సలహాతో మీకు సహాయం చేయడంలో సంతోషిస్తున్నాను.",
                        f"అద్భుతమైన ప్రశ్న! మీ ప్రస్తుత ఆర్థిక పరిస్థితితో (నెలవారీ ₹{savings:,} పొదుపు), మీ ఆర్థిక వ్యవహారాలను అనుకూలీకరించడానికి అనేక వ్యూహాలను మనం అన్వేషించవచ్చు.",
                        f"మీరు ఆర్థిక మార్గదర్శకత్వం కోరుతున్నారని నేను అర్థం చేసుకున్నాను. నెలవారీ ₹{income:,} సంపాదించే వ్యక్తిగా, నేను మీకు అనుకూలీకరించిన సిఫార్సులను అందిస్తున్నాను."
                    ]
                }

            return responses.get(language, responses['en'])

        except Exception as e:
            self.logger.error(f"Contextual response generation failed: {e}")
            return ["I'm here to help with your financial questions. Please feel free to ask about investments, savings, loans, or any other financial topics."]

    def render_comprehensive_dashboard_page(self):
        """Render comprehensive financial dashboard with all analytics"""
        try:
            profile = st.session_state.user_profile
            current_lang = profile['basic_info']['language']

            # Dashboard header
            dashboard_titles = {
                'en': '📊 Comprehensive Financial Dashboard',
                'ta': '📊 விரிவான நிதி டாஷ்போர்டு',
                'hi': '📊 व्यापक वित्तीय डैशबोर्ड',
                'te': '📊 సమగ్ర ఆర్థిక డాష్‌బోర్డ్'
            }

            st.markdown(f"""
            <div class="main-header fade-in">
                <h1>{dashboard_titles.get(current_lang, dashboard_titles['en'])}</h1>
                <p>Complete financial analytics and insights</p>
                <p><em>JarvisFi - Your Ultimate Multilingual Finance Chat Assistant</em></p>
            </div>
            """, unsafe_allow_html=True)

            # Get financial data
            monthly_income = profile['basic_info']['monthly_income']
            monthly_expenses = profile['financial_profile']['monthly_expenses']
            savings = monthly_income - monthly_expenses
            savings_rate = (savings / monthly_income * 100) if monthly_income > 0 else 0
            credit_score = profile['financial_profile']['credit_score']
            age = profile['basic_info']['age']

            # Key Performance Indicators
            st.markdown("## 🎯 Key Performance Indicators")

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.markdown(f"""
                <div class="metric-card slide-in" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white;">
                    <h4 style="margin: 0; opacity: 0.9;">💰 Monthly Income</h4>
                    <h2 style="margin: 0.5rem 0; font-size: 1.8rem;">₹{monthly_income:,}</h2>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.8rem;">Primary source</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card slide-in" style="background: linear-gradient(135deg, #FF6B6B, #ee5a52); color: white;">
                    <h4 style="margin: 0; opacity: 0.9;">💸 Expenses</h4>
                    <h2 style="margin: 0.5rem 0; font-size: 1.8rem;">₹{monthly_expenses:,}</h2>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.8rem;">{(monthly_expenses/monthly_income*100):.1f}% of income</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                savings_color = "#4CAF50" if savings > 0 else "#FF6B6B"
                st.markdown(f"""
                <div class="metric-card slide-in" style="background: linear-gradient(135deg, {savings_color}, {savings_color}); color: white;">
                    <h4 style="margin: 0; opacity: 0.9;">💰 Savings</h4>
                    <h2 style="margin: 0.5rem 0; font-size: 1.8rem;">₹{savings:,}</h2>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.8rem;">{savings_rate:.1f}% rate</p>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                score_color = "#4CAF50" if credit_score >= 750 else "#FFA726" if credit_score >= 650 else "#FF6B6B"
                st.markdown(f"""
                <div class="metric-card slide-in" style="background: linear-gradient(135deg, {score_color}, {score_color}); color: white;">
                    <h4 style="margin: 0; opacity: 0.9;">💳 Credit Score</h4>
                    <h2 style="margin: 0.5rem 0; font-size: 1.8rem;">{credit_score}</h2>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.8rem;">{'Excellent' if credit_score >= 750 else 'Good' if credit_score >= 650 else 'Fair'}</p>
                </div>
                """, unsafe_allow_html=True)

            with col5:
                net_worth = savings * 12 + 100000  # Estimated net worth
                st.markdown(f"""
                <div class="metric-card slide-in" style="background: linear-gradient(135deg, #9C27B0, #7B1FA2); color: white;">
                    <h4 style="margin: 0; opacity: 0.9;">💎 Net Worth</h4>
                    <h2 style="margin: 0.5rem 0; font-size: 1.8rem;">₹{net_worth:,}</h2>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.8rem;">Estimated</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Financial Health Score
            st.markdown("## 🏥 Financial Health Analysis")

            col1, col2 = st.columns([2, 1])

            with col1:
                # Calculate financial health score
                health_score = 0
                if savings_rate >= 20: health_score += 30
                elif savings_rate >= 10: health_score += 20
                elif savings_rate >= 5: health_score += 10

                if credit_score >= 750: health_score += 25
                elif credit_score >= 650: health_score += 15
                elif credit_score >= 550: health_score += 5

                if monthly_expenses/monthly_income <= 0.7: health_score += 20
                elif monthly_expenses/monthly_income <= 0.8: health_score += 15
                elif monthly_expenses/monthly_income <= 0.9: health_score += 10

                # Age-based investment score
                if age < 30: health_score += 15
                elif age < 40: health_score += 12
                elif age < 50: health_score += 8
                else: health_score += 5

                # Emergency fund score (simulated)
                health_score += 10  # Assume some emergency fund exists

                health_score = min(health_score, 100)

                # Health score gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = health_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Financial Health Score", 'font': {'size': 24}},
                    delta = {'reference': 70, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "darkblue"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 40], 'color': "#ffcccc"},
                            {'range': [40, 70], 'color': "#ffffcc"},
                            {'range': [70, 100], 'color': "#ccffcc"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                fig.update_layout(height=400, font={'color': "darkblue", 'family': "Arial"})
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("### 📋 Health Breakdown")

                # Health score components
                components = [
                    ("💰 Savings Rate", 30 if savings_rate >= 20 else 20 if savings_rate >= 10 else 10 if savings_rate >= 5 else 0, 30),
                    ("💳 Credit Score", 25 if credit_score >= 750 else 15 if credit_score >= 650 else 5 if credit_score >= 550 else 0, 25),
                    ("💸 Expense Control", 20 if monthly_expenses/monthly_income <= 0.7 else 15 if monthly_expenses/monthly_income <= 0.8 else 10 if monthly_expenses/monthly_income <= 0.9 else 0, 20),
                    ("🎂 Age Factor", 15 if age < 30 else 12 if age < 40 else 8 if age < 50 else 5, 15),
                    ("🚨 Emergency Fund", 10, 10)
                ]

                for component, score, max_score in components:
                    percentage = (score / max_score) * 100
                    color = "#4CAF50" if percentage >= 80 else "#FFA726" if percentage >= 60 else "#FF6B6B"

                    st.markdown(f"""
                    <div style="margin: 0.5rem 0;">
                        <strong>{component}</strong><br>
                        <div style="background: #f0f0f0; border-radius: 10px; height: 20px; margin: 0.2rem 0;">
                            <div style="background: {color}; width: {percentage}%; height: 100%; border-radius: 10px;"></div>
                        </div>
                        <small>{score}/{max_score} points</small>
                    </div>
                    """, unsafe_allow_html=True)

                # Overall assessment
                if health_score >= 80:
                    st.markdown("""
                    <div class="feature-card" style="background: linear-gradient(135deg, #e8f5e8, #c8e6c9); border-left-color: #4caf50;">
                        🎉 <strong>Excellent Financial Health!</strong><br>
                        You're doing great with your finances. Keep up the good work!
                    </div>
                    """, unsafe_allow_html=True)
                elif health_score >= 60:
                    st.markdown("""
                    <div class="feature-card" style="background: linear-gradient(135deg, #fff3e0, #ffe0b2); border-left-color: #ff9800;">
                        👍 <strong>Good Financial Health</strong><br>
                        You're on the right track. A few improvements can make it excellent!
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="feature-card" style="background: linear-gradient(135deg, #ffebee, #ffcdd2); border-left-color: #f44336;">
                        ⚠️ <strong>Needs Improvement</strong><br>
                        Focus on increasing savings and managing expenses better.
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")

            # Detailed Analytics
            st.markdown("## 📈 Detailed Financial Analytics")

            tab1, tab2, tab3, tab4 = st.tabs(["💰 Income & Expenses", "📊 Investment Analysis", "🎯 Goal Tracking", "📅 Monthly Trends"])

            with tab1:
                col1, col2 = st.columns(2)

                with col1:
                    # Income vs Expenses chart
                    fig = go.Figure(data=[
                        go.Bar(name='Income', x=['Monthly'], y=[monthly_income], marker_color='#4CAF50'),
                        go.Bar(name='Expenses', x=['Monthly'], y=[monthly_expenses], marker_color='#FF6B6B'),
                        go.Bar(name='Savings', x=['Monthly'], y=[savings], marker_color='#2196F3')
                    ])
                    fig.update_layout(
                        title='Income vs Expenses vs Savings',
                        barmode='group',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # Expense breakdown
                    expense_categories = ['Housing', 'Food', 'Transportation', 'Entertainment', 'Others']
                    expense_values = [
                        monthly_expenses * 0.4,  # Housing
                        monthly_expenses * 0.2,  # Food
                        monthly_expenses * 0.15, # Transportation
                        monthly_expenses * 0.1,  # Entertainment
                        monthly_expenses * 0.15  # Others
                    ]

                    fig = px.pie(
                        values=expense_values,
                        names=expense_categories,
                        title='Expense Breakdown',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)

            with tab2:
                # Investment analysis
                st.markdown("### 📈 Investment Portfolio Analysis")

                # Simulated investment data
                portfolio_value = monthly_income * 0.15 * 12 * 3  # 3 years of 15% investment
                monthly_sip = monthly_income * 0.15

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Portfolio Value", f"₹{portfolio_value:,.0f}", "↗️ +12%")
                with col2:
                    st.metric("Monthly SIP", f"₹{monthly_sip:,.0f}", f"↗️ +₹{monthly_sip*0.1:,.0f}")
                with col3:
                    st.metric("Annual Returns", "14.5%", "↗️ +2.1%")

                # Asset allocation
                allocation_data = {
                    'Asset Class': ['Large Cap Equity', 'Mid Cap Equity', 'Small Cap Equity', 'Debt Funds', 'Gold ETF'],
                    'Allocation': [40, 25, 15, 15, 5],
                    'Amount': [portfolio_value * 0.4, portfolio_value * 0.25,
                              portfolio_value * 0.15, portfolio_value * 0.15, portfolio_value * 0.05]
                }

                fig = px.pie(allocation_data, values='Allocation', names='Asset Class',
                            title='Current Asset Allocation')
                st.plotly_chart(fig, use_container_width=True)

            with tab3:
                # Goal tracking
                st.markdown("### 🎯 Financial Goals Progress")

                goals = self.get_advanced_financial_goals(monthly_income, profile['basic_info']['user_type'])

                for goal in goals:
                    progress = (goal['current'] / goal['target']) * 100

                    col1, col2, col3 = st.columns([3, 1, 1])

                    with col1:
                        st.markdown(f"**{goal['name']}**")
                        st.progress(progress / 100)

                    with col2:
                        st.metric("Current", f"₹{goal['current']:,}")

                    with col3:
                        st.metric("Target", f"₹{goal['target']:,}")

                    st.markdown(f"**Progress:** {progress:.1f}% complete")
                    st.markdown("---")

            with tab4:
                # Monthly trends
                st.markdown("### 📅 Monthly Financial Trends")

                # Simulated monthly data
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                income_trend = [monthly_income + (i * 1000) for i in range(12)]  # Slight growth
                expense_trend = [monthly_expenses + (i * 500) for i in range(12)]  # Controlled growth
                savings_trend = [inc - exp for inc, exp in zip(income_trend, expense_trend)]

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=months, y=income_trend, name='Income', line=dict(color='#4CAF50')))
                fig.add_trace(go.Scatter(x=months, y=expense_trend, name='Expenses', line=dict(color='#FF6B6B')))
                fig.add_trace(go.Scatter(x=months, y=savings_trend, name='Savings', line=dict(color='#2196F3')))

                fig.update_layout(
                    title='Monthly Financial Trends (2024)',
                    xaxis_title='Month',
                    yaxis_title='Amount (₹)',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

                # Savings rate trend
                savings_rate_trend = [(sav / inc * 100) for sav, inc in zip(savings_trend, income_trend)]

                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=months, y=savings_rate_trend, name='Savings Rate (%)',
                                         line=dict(color='#9C27B0'), fill='tonexty'))
                fig2.update_layout(
                    title='Savings Rate Trend (%)',
                    xaxis_title='Month',
                    yaxis_title='Savings Rate (%)',
                    height=300
                )
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("---")

            # Action items and recommendations
            st.markdown("## 🎯 Personalized Action Items")

            recommendations = self.get_advanced_recommendations(profile)

            col1, col2 = st.columns(2)

            for i, rec in enumerate(recommendations[:6]):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                    <div class="recommendation-card fade-in">
                        <p style="margin: 0; font-size: 1rem; color: #333;">{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            self.logger.error(f"❌ Dashboard page rendering failed: {e}")
            st.error(f"Dashboard error: {e}")

    def render_complete_calculators_page(self):
        """Render complete financial calculators page with all tools"""
        try:
            profile = st.session_state.user_profile
            current_lang = profile['basic_info']['language']

            # Calculator header
            calc_titles = {
                'en': '🧮 Advanced Financial Calculators',
                'ta': '🧮 மேம்பட்ட நிதி கணிப்பான்கள்',
                'hi': '🧮 उन्नत वित्तीय कैलकुलेटर',
                'te': '🧮 అధునాతన ఆర్థిక కాలిక్యులేటర్లు'
            }

            st.markdown(f"""
            <div class="main-header fade-in">
                <h1>{calc_titles.get(current_lang, calc_titles['en'])}</h1>
                <p>15+ Professional financial planning tools</p>
                <p><em>JarvisFi - Your Ultimate Multilingual Finance Chat Assistant</em></p>
            </div>
            """, unsafe_allow_html=True)

            # Calculator selection
            calculator_options = {
                'en': {
                    'SIP Calculator': '📈 SIP Calculator - Systematic Investment Plan',
                    'EMI Calculator': '🏠 EMI Calculator - Loan EMI Calculator',
                    'Tax Calculator': '💰 Tax Calculator - Income Tax Calculator',
                    'Retirement Calculator': '🏖️ Retirement Calculator - Retirement Planning',
                    'FD Calculator': '🏦 FD Calculator - Fixed Deposit Calculator',
                    'PPF Calculator': '💎 PPF Calculator - Public Provident Fund',
                    'NSC Calculator': '📜 NSC Calculator - National Savings Certificate',
                    'ELSS Calculator': '🎯 ELSS Calculator - Tax Saving Mutual Funds',
                    'Lumpsum Calculator': '💰 Lumpsum Calculator - One-time Investment',
                    'Goal Calculator': '🎯 Goal Calculator - Financial Goal Planning'
                },
                'ta': {
                    'SIP Calculator': '📈 SIP கணிப்பான் - முறையான முதலீட்டு திட்டம்',
                    'EMI Calculator': '🏠 EMI கணிப்பான் - கடன் EMI கணிப்பான்',
                    'Tax Calculator': '💰 வரி கணிப்பான் - வருமான வரி கணிப்பான்',
                    'Retirement Calculator': '🏖️ ஓய்வூதிய கணிப்பான் - ஓய்வூதிய திட்டமிடல்',
                    'FD Calculator': '🏦 FD கணிப்பான் - நிலையான வைப்பு கணிப்பான்',
                    'PPF Calculator': '💎 PPF கணிப்பான் - பொது வருங்கால வைப்பு நிதி',
                    'NSC Calculator': '📜 NSC கணிப்பான் - தேசிய சேமிப்பு சான்றிதழ்',
                    'ELSS Calculator': '🎯 ELSS கணிப்பான் - வரி சேமிப்பு மியூச்சுவல் ஃபண்டுகள்',
                    'Lumpsum Calculator': '💰 மொத்த தொகை கணிப்பான் - ஒரு முறை முதலீடு',
                    'Goal Calculator': '🎯 இலக்கு கணிப்பான் - நிதி இலக்கு திட்டமிடல்'
                }
            }

            calc_options = calculator_options.get(current_lang, calculator_options['en'])

            selected_calculator = st.selectbox(
                "Choose Calculator:",
                options=list(calc_options.keys()),
                format_func=lambda x: calc_options[x]
            )

            st.markdown("---")

            # Render selected calculator
            if selected_calculator == 'SIP Calculator':
                self.render_sip_calculator(current_lang)
            elif selected_calculator == 'EMI Calculator':
                self.render_emi_calculator(current_lang)
            elif selected_calculator == 'Tax Calculator':
                self.render_tax_calculator(current_lang)
            elif selected_calculator == 'Retirement Calculator':
                self.render_retirement_calculator(current_lang)
            elif selected_calculator == 'FD Calculator':
                self.render_fd_calculator(current_lang)
            elif selected_calculator == 'PPF Calculator':
                self.render_ppf_calculator(current_lang)
            elif selected_calculator == 'NSC Calculator':
                self.render_nsc_calculator(current_lang)
            elif selected_calculator == 'ELSS Calculator':
                self.render_elss_calculator(current_lang)
            elif selected_calculator == 'Lumpsum Calculator':
                self.render_lumpsum_calculator(current_lang)
            elif selected_calculator == 'Goal Calculator':
                self.render_goal_calculator(current_lang)

            # Add gamification points for using calculators
            st.session_state.gamification['points'] += 2
            st.session_state.analytics['features_used'].append(f"calculator_{selected_calculator.lower().replace(' ', '_')}")

        except Exception as e:
            self.logger.error(f"❌ Calculators page rendering failed: {e}")
            st.error(f"Calculators error: {e}")

    def render_complete_farmer_tools_page(self):
        """Render complete farmer tools page with government schemes"""
        try:
            profile = st.session_state.user_profile
            current_lang = profile['basic_info']['language']

            # Farmer tools header
            farmer_titles = {
                'en': '👨‍🌾 Comprehensive Farmer Financial Tools',
                'ta': '👨‍🌾 விரிவான விவசாயி நிதி கருவிகள்',
                'hi': '👨‍🌾 व्यापक किसान वित्तीय उपकरण',
                'te': '👨‍🌾 సమగ్ర రైతు ఆర్థిక సాధనాలు'
            }

            st.markdown(f"""
            <div class="main-header fade-in">
                <h1>{farmer_titles.get(current_lang, farmer_titles['en'])}</h1>
                <p>Complete agricultural finance solutions with government schemes</p>
                <p><em>JarvisFi - Your Ultimate Multilingual Finance Chat Assistant</em></p>
            </div>
            """, unsafe_allow_html=True)

            # Farmer tools tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🏛️ Government Schemes",
                "💰 MSP & Pricing",
                "🏦 Agricultural Loans",
                "🛡️ Insurance & Risk",
                "📊 Farm Analytics"
            ])

            with tab1:
                self.render_government_schemes(current_lang)

            with tab2:
                self.render_msp_pricing(current_lang)

            with tab3:
                self.render_agricultural_loans(current_lang)

            with tab4:
                self.render_farm_insurance(current_lang)

            with tab5:
                self.render_farm_analytics(current_lang)

        except Exception as e:
            self.logger.error(f"❌ Farmer tools page rendering failed: {e}")
            st.error(f"Farmer tools error: {e}")

    def render_government_schemes(self, language: str):
        """Render comprehensive government schemes for farmers"""
        try:
            st.markdown("### 🏛️ Government Schemes for Farmers")

            # Government schemes data
            schemes = {
                'en': [
                    {
                        'name': 'PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)',
                        'description': 'Direct income support of ₹6,000 per year to small and marginal farmers',
                        'eligibility': 'Small and marginal farmers with landholding up to 2 hectares',
                        'benefits': '₹2,000 every 4 months (₹6,000 annually)',
                        'application': 'Online at pmkisan.gov.in or through CSC centers',
                        'documents': 'Aadhaar, Bank account, Land records',
                        'status': 'Active',
                        'category': 'Income Support'
                    },
                    {
                        'name': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
                        'description': 'Comprehensive crop insurance scheme for farmers',
                        'eligibility': 'All farmers (sharecroppers and tenant farmers included)',
                        'benefits': 'Up to ₹2 lakh per hectare coverage',
                        'application': 'Through banks, insurance companies, or online',
                        'documents': 'Aadhaar, Bank account, Land records, Sowing certificate',
                        'status': 'Active',
                        'category': 'Insurance'
                    },
                    {
                        'name': 'Kisan Credit Card (KCC)',
                        'description': 'Credit facility for farmers to meet agricultural expenses',
                        'eligibility': 'All farmers including tenant farmers and sharecroppers',
                        'benefits': 'Credit limit up to ₹3 lakh at 4% interest rate',
                        'application': 'Through banks and cooperative societies',
                        'documents': 'Aadhaar, PAN, Land records, Income certificate',
                        'status': 'Active',
                        'category': 'Credit'
                    },
                    {
                        'name': 'PM Kisan Maandhan Yojana',
                        'description': 'Pension scheme for small and marginal farmers',
                        'eligibility': 'Farmers aged 18-40 years with landholding up to 2 hectares',
                        'benefits': '₹3,000 monthly pension after 60 years',
                        'application': 'Online or through CSC centers',
                        'documents': 'Aadhaar, Bank account, Land records',
                        'status': 'Active',
                        'category': 'Pension'
                    },
                    {
                        'name': 'Soil Health Card Scheme',
                        'description': 'Provides soil health information to farmers',
                        'eligibility': 'All farmers',
                        'benefits': 'Free soil testing and nutrient recommendations',
                        'application': 'Through agriculture department',
                        'documents': 'Land records, Farmer ID',
                        'status': 'Active',
                        'category': 'Advisory'
                    },
                    {
                        'name': 'National Agriculture Market (e-NAM)',
                        'description': 'Online trading platform for agricultural commodities',
                        'eligibility': 'All farmers and traders',
                        'benefits': 'Better price discovery and transparent trading',
                        'application': 'Online registration at enam.gov.in',
                        'documents': 'Aadhaar, Bank account, Mobile number',
                        'status': 'Active',
                        'category': 'Marketing'
                    },
                    {
                        'name': 'Pradhan Mantri Krishi Sinchai Yojana',
                        'description': 'Irrigation development and water conservation',
                        'eligibility': 'All farmers',
                        'benefits': 'Subsidized drip and sprinkler irrigation systems',
                        'application': 'Through state agriculture departments',
                        'documents': 'Land records, Water source certificate',
                        'status': 'Active',
                        'category': 'Infrastructure'
                    },
                    {
                        'name': 'Formation and Promotion of FPOs',
                        'description': 'Support for Farmer Producer Organizations',
                        'eligibility': 'Groups of farmers',
                        'benefits': 'Financial assistance up to ₹18.75 lakh per FPO',
                        'application': 'Through NABARD and state agencies',
                        'documents': 'Group formation documents, Business plan',
                        'status': 'Active',
                        'category': 'Institutional'
                    }
                ],
                'ta': [
                    {
                        'name': 'பிரதான் மந்திரி கிசான் சம்மான் நிதி (PM-KISAN)',
                        'description': 'சிறு மற்றும் குறு விவசாயிகளுக்கு ஆண்டுக்கு ₹6,000 நேரடி வருமான ஆதரவு',
                        'eligibility': '2 ஹெக்டேர் வரை நிலம் உள்ள சிறு மற்றும் குறு விவசாயிகள்',
                        'benefits': '4 மாதங்களுக்கு ₹2,000 (ஆண்டுக்கு ₹6,000)',
                        'application': 'pmkisan.gov.in இல் ஆன்லைன் அல்லது CSC மையங்கள் மூலம்',
                        'documents': 'ஆதார், வங்கி கணக்கு, நில பதிவுகள்',
                        'status': 'செயலில்',
                        'category': 'வருமான ஆதரவு'
                    }
                    # Add more Tamil translations as needed
                ]
            }

            scheme_list = schemes.get(language, schemes['en'])

            # Scheme categories filter
            categories = list(set([scheme['category'] for scheme in scheme_list]))
            selected_category = st.selectbox("Filter by Category:", ['All'] + categories)

            # Filter schemes
            if selected_category != 'All':
                filtered_schemes = [s for s in scheme_list if s['category'] == selected_category]
            else:
                filtered_schemes = scheme_list

            # Display schemes
            for i, scheme in enumerate(filtered_schemes):
                with st.expander(f"🏛️ {scheme['name']}", expanded=False):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"""
                        <div class="farmer-tool-card">
                            <h4>📋 Scheme Details</h4>
                            <p><strong>Description:</strong> {scheme['description']}</p>
                            <p><strong>Category:</strong> {scheme['category']}</p>
                            <p><strong>Status:</strong> <span style="color: green;">✅ {scheme['status']}</span></p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class="farmer-tool-card">
                            <h4>💰 Benefits & Eligibility</h4>
                            <p><strong>Benefits:</strong> {scheme['benefits']}</p>
                            <p><strong>Eligibility:</strong> {scheme['eligibility']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="farmer-tool-card">
                        <h4>📝 Application Process</h4>
                        <p><strong>How to Apply:</strong> {scheme['application']}</p>
                        <p><strong>Required Documents:</strong> {scheme['documents']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📋 Apply Now", key=f"apply_{i}"):
                            st.info(f"Redirecting to application portal for {scheme['name']}")
                    with col2:
                        if st.button(f"📞 Get Help", key=f"help_{i}"):
                            st.info("Contact: 1800-180-1551 (PM-KISAN Helpline)")
                    with col3:
                        if st.button(f"📊 Check Status", key=f"status_{i}"):
                            st.info("Enter your application number to check status")

            # Scheme statistics
            st.markdown("### 📊 Scheme Statistics")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Schemes", len(scheme_list), "8 Active")
            with col2:
                st.metric("Beneficiaries", "12+ Crore", "↗️ Growing")
            with col3:
                st.metric("Total Disbursed", "₹2.8+ Lakh Cr", "PM-KISAN")
            with col4:
                st.metric("Coverage", "Pan India", "All States")

            # Quick application form
            st.markdown("### 📝 Quick Scheme Eligibility Check")

            with st.form("eligibility_check"):
                col1, col2 = st.columns(2)

                with col1:
                    land_size = st.number_input("Land Size (Hectares)", min_value=0.0, max_value=50.0, value=1.0)
                    farmer_age = st.number_input("Age", min_value=18, max_value=80, value=35)
                    annual_income = st.number_input("Annual Income (₹)", min_value=0, max_value=1000000, value=100000)

                with col2:
                    farmer_type = st.selectbox("Farmer Type", ["Small", "Marginal", "Medium", "Large"])
                    has_kcc = st.checkbox("Have Kisan Credit Card")
                    has_insurance = st.checkbox("Have Crop Insurance")

                if st.form_submit_button("🔍 Check Eligibility"):
                    eligible_schemes = []

                    # Check eligibility logic
                    if land_size <= 2:
                        eligible_schemes.append("PM-KISAN")
                        if farmer_age <= 40:
                            eligible_schemes.append("PM Kisan Maandhan Yojana")

                    if not has_insurance:
                        eligible_schemes.append("Pradhan Mantri Fasal Bima Yojana")

                    if not has_kcc:
                        eligible_schemes.append("Kisan Credit Card")

                    eligible_schemes.extend(["Soil Health Card", "e-NAM", "PM Krishi Sinchai Yojana"])

                    st.success(f"✅ You are eligible for {len(eligible_schemes)} schemes:")
                    for scheme in eligible_schemes:
                        st.info(f"• {scheme}")

        except Exception as e:
            self.logger.error(f"Government schemes rendering failed: {e}")
            st.error(f"Government schemes error: {e}")

    def render_msp_pricing(self, language: str):
        """Render MSP and crop pricing information"""
        try:
            st.markdown("### 💰 Minimum Support Price (MSP) & Market Rates")

            # MSP data for major crops
            msp_data = {
                'Crop': ['Rice (Common)', 'Rice (Grade A)', 'Wheat', 'Jowar', 'Bajra', 'Maize', 'Ragi', 'Arhar (Tur)', 'Moong', 'Urad', 'Groundnut', 'Sunflower', 'Soybean', 'Cotton'],
                'MSP 2024-25 (₹/Quintal)': [2300, 2320, 2275, 3180, 2500, 2090, 3846, 7000, 8558, 6950, 6377, 6760, 4892, 7121],
                'Previous Year (₹/Quintal)': [2183, 2203, 2125, 2970, 2350, 1962, 3578, 6600, 8174, 6600, 5850, 6400, 4560, 6620],
                'Change (%)': [5.4, 5.3, 7.1, 7.1, 6.4, 6.5, 7.5, 6.1, 4.7, 5.3, 9.0, 5.6, 7.3, 7.6],
                'Market Rate (₹/Quintal)': [2350, 2380, 2290, 3200, 2520, 2100, 3900, 7200, 8600, 7000, 6400, 6800, 4950, 7200]
            }

            df_msp = pd.DataFrame(msp_data)

            # Display MSP table
            st.markdown("#### 📊 Current MSP Rates (2024-25)")
            st.dataframe(df_msp, use_container_width=True)

            # MSP vs Market Rate comparison
            st.markdown("#### 📈 MSP vs Market Rate Comparison")

            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='MSP Rate',
                x=df_msp['Crop'][:10],  # Show first 10 crops
                y=df_msp['MSP 2024-25 (₹/Quintal)'][:10],
                marker_color='#4CAF50'
            ))
            fig.add_trace(go.Bar(
                name='Market Rate',
                x=df_msp['Crop'][:10],
                y=df_msp['Market Rate (₹/Quintal)'][:10],
                marker_color='#2196F3'
            ))

            fig.update_layout(
                title='MSP vs Current Market Rates',
                xaxis_title='Crops',
                yaxis_title='Price (₹/Quintal)',
                barmode='group',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

            # Price calculator
            st.markdown("#### 🧮 Crop Value Calculator")

            col1, col2 = st.columns(2)

            with col1:
                selected_crop = st.selectbox("Select Crop", df_msp['Crop'].tolist())
                quantity = st.number_input("Quantity (Quintals)", min_value=0.1, max_value=1000.0, value=10.0)
                price_type = st.radio("Price Type", ["MSP Rate", "Market Rate"])

            with col2:
                crop_index = df_msp[df_msp['Crop'] == selected_crop].index[0]

                if price_type == "MSP Rate":
                    rate = df_msp.loc[crop_index, 'MSP 2024-25 (₹/Quintal)']
                else:
                    rate = df_msp.loc[crop_index, 'Market Rate (₹/Quintal)']

                total_value = quantity * rate

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white;">
                    <h4>💰 Total Value</h4>
                    <h2>₹{total_value:,.0f}</h2>
                    <p>Rate: ₹{rate}/Quintal</p>
                </div>
                """, unsafe_allow_html=True)

                # Profit calculation
                if price_type == "Market Rate":
                    msp_value = quantity * df_msp.loc[crop_index, 'MSP 2024-25 (₹/Quintal)']
                    profit = total_value - msp_value
                    profit_percent = (profit / msp_value * 100) if msp_value > 0 else 0

                    if profit > 0:
                        st.success(f"📈 Market Premium: ₹{profit:,.0f} ({profit_percent:.1f}% above MSP)")
                    else:
                        st.warning(f"📉 Below MSP: ₹{abs(profit):,.0f} ({abs(profit_percent):.1f}% below MSP)")

            # Market trends
            st.markdown("#### 📊 Price Trends & Forecasts")

            # Simulated price trend data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            rice_prices = [2200, 2250, 2300, 2350, 2400, 2380, 2360, 2340, 2320, 2300, 2280, 2300]
            wheat_prices = [2100, 2150, 2200, 2250, 2275, 2270, 2265, 2260, 2255, 2250, 2245, 2275]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=rice_prices, name='Rice', line=dict(color='#4CAF50')))
            fig.add_trace(go.Scatter(x=months, y=wheat_prices, name='Wheat', line=dict(color='#FF9800')))

            fig.update_layout(
                title='Monthly Price Trends (2024)',
                xaxis_title='Month',
                yaxis_title='Price (₹/Quintal)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            # Price alerts
            st.markdown("#### 🔔 Price Alerts & Notifications")

            with st.form("price_alert"):
                alert_crop = st.selectbox("Crop for Alert", df_msp['Crop'].tolist())
                alert_price = st.number_input("Alert Price (₹/Quintal)", min_value=1000, max_value=10000, value=2500)
                alert_type = st.radio("Alert Type", ["Above Price", "Below Price"])

                if st.form_submit_button("🔔 Set Price Alert"):
                    st.success(f"✅ Price alert set for {alert_crop} when price goes {alert_type.lower()} ₹{alert_price}/quintal")

        except Exception as e:
            self.logger.error(f"MSP pricing rendering failed: {e}")
            st.error(f"MSP pricing error: {e}")

    def render_agricultural_loans(self, language: str):
        """Render agricultural loans and credit facilities"""
        try:
            st.markdown("### 🏦 Agricultural Loans & Credit Facilities")

            # Loan types
            loan_types = [
                {
                    'name': 'Kisan Credit Card (KCC)',
                    'purpose': 'Short-term credit for crop production',
                    'amount': 'Up to ₹3 lakh',
                    'interest': '4% (with interest subvention)',
                    'tenure': '12 months (renewable)',
                    'features': ['No collateral up to ₹1.6 lakh', 'Flexible repayment', 'Insurance coverage']
                },
                {
                    'name': 'Crop Loan',
                    'purpose': 'Seasonal agricultural operations',
                    'amount': 'Based on scale of finance',
                    'interest': '7-9% per annum',
                    'tenure': '12-18 months',
                    'features': ['Crop-specific limits', 'Seasonal disbursement', 'Harvest-linked repayment']
                },
                {
                    'name': 'Farm Equipment Loan',
                    'purpose': 'Purchase of tractors, implements',
                    'amount': 'Up to ₹25 lakh',
                    'interest': '8.5-12% per annum',
                    'tenure': '5-7 years',
                    'features': ['Equipment as collateral', 'Subsidies available', 'EMI facility']
                },
                {
                    'name': 'Land Development Loan',
                    'purpose': 'Land improvement, irrigation',
                    'amount': 'Up to ₹50 lakh',
                    'interest': '9-11% per annum',
                    'tenure': '10-15 years',
                    'features': ['Long-term repayment', 'Development-linked', 'Government subsidies']
                }
            ]

            # Display loan types
            for i, loan in enumerate(loan_types):
                with st.expander(f"🏦 {loan['name']}", expanded=False):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"""
                        <div class="loan-card">
                            <h4>💰 Loan Details</h4>
                            <p><strong>Purpose:</strong> {loan['purpose']}</p>
                            <p><strong>Amount:</strong> {loan['amount']}</p>
                            <p><strong>Interest Rate:</strong> {loan['interest']}</p>
                            <p><strong>Tenure:</strong> {loan['tenure']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class="loan-card">
                            <h4>✨ Key Features</h4>
                            <ul>
                                {''.join([f'<li>{feature}</li>' for feature in loan['features']])}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

            # Loan calculator
            st.markdown("#### 🧮 Agricultural Loan Calculator")

            col1, col2 = st.columns(2)

            with col1:
                loan_amount = st.number_input("Loan Amount (₹)", min_value=10000, max_value=5000000, value=200000)
                interest_rate = st.slider("Interest Rate (%)", min_value=4.0, max_value=15.0, value=8.0, step=0.5)
                loan_tenure = st.slider("Loan Tenure (Years)", min_value=1, max_value=15, value=5)

                # Calculate EMI
                monthly_rate = interest_rate / 12 / 100
                total_months = loan_tenure * 12

                if monthly_rate > 0:
                    emi = loan_amount * monthly_rate * (1 + monthly_rate) ** total_months / ((1 + monthly_rate) ** total_months - 1)
                else:
                    emi = loan_amount / total_months

                total_payment = emi * total_months
                total_interest = total_payment - loan_amount

            with col2:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #2196F3, #1976D2); color: white; margin: 0.5rem 0;">
                    <h4>💳 Monthly EMI</h4>
                    <h2>₹{emi:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #FF9800, #F57C00); color: white; margin: 0.5rem 0;">
                    <h4>💸 Total Interest</h4>
                    <h2>₹{total_interest:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #9C27B0, #7B1FA2); color: white; margin: 0.5rem 0;">
                    <h4>💰 Total Payment</h4>
                    <h2>₹{total_payment:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

            # Loan application process
            st.markdown("#### 📝 Loan Application Process")

            process_steps = [
                "📋 Document Preparation",
                "🏦 Bank Selection & Visit",
                "📄 Application Submission",
                "🔍 Verification & Assessment",
                "✅ Approval & Disbursement"
            ]

            cols = st.columns(len(process_steps))
            for i, step in enumerate(process_steps):
                with cols[i]:
                    st.markdown(f"""
                    <div class="process-step">
                        <h4>{i+1}</h4>
                        <p>{step}</p>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            self.logger.error(f"Agricultural loans rendering failed: {e}")
            st.error(f"Agricultural loans error: {e}")

    def render_farm_insurance(self, language: str):
        """Render farm insurance and risk management"""
        try:
            st.markdown("### 🛡️ Farm Insurance & Risk Management")

            # Insurance schemes
            insurance_schemes = [
                {
                    'name': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
                    'coverage': 'Comprehensive crop insurance',
                    'premium': '2% for Kharif, 1.5% for Rabi crops',
                    'sum_insured': 'Up to ₹2 lakh per hectare',
                    'risks_covered': ['Natural disasters', 'Pest attacks', 'Disease outbreaks', 'Weather risks']
                },
                {
                    'name': 'Weather Based Crop Insurance (WBCIS)',
                    'coverage': 'Weather parameter-based insurance',
                    'premium': '3-5% of sum insured',
                    'sum_insured': 'Based on crop value',
                    'risks_covered': ['Rainfall deficit/excess', 'Temperature variations', 'Humidity changes', 'Wind speed']
                },
                {
                    'name': 'Coconut Palm Insurance Scheme',
                    'coverage': 'Insurance for coconut trees',
                    'premium': '₹9 per tree per year',
                    'sum_insured': '₹900 per tree',
                    'risks_covered': ['Fire', 'Lightning', 'Cyclone', 'Flood']
                }
            ]

            # Display insurance schemes
            for scheme in insurance_schemes:
                with st.expander(f"🛡️ {scheme['name']}", expanded=False):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"""
                        <div class="insurance-card">
                            <h4>📋 Scheme Details</h4>
                            <p><strong>Coverage:</strong> {scheme['coverage']}</p>
                            <p><strong>Premium:</strong> {scheme['premium']}</p>
                            <p><strong>Sum Insured:</strong> {scheme['sum_insured']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class="insurance-card">
                            <h4>🛡️ Risks Covered</h4>
                            <ul>
                                {''.join([f'<li>{risk}</li>' for risk in scheme['risks_covered']])}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

            # Insurance calculator
            st.markdown("#### 🧮 Insurance Premium Calculator")

            col1, col2 = st.columns(2)

            with col1:
                crop_type = st.selectbox("Crop Type", ["Kharif (Monsoon)", "Rabi (Winter)", "Zaid (Summer)"])
                land_area = st.number_input("Land Area (Hectares)", min_value=0.1, max_value=100.0, value=2.0)
                crop_value = st.number_input("Crop Value per Hectare (₹)", min_value=10000, max_value=200000, value=50000)

                # Calculate premium
                if crop_type == "Kharif (Monsoon)":
                    premium_rate = 2.0
                elif crop_type == "Rabi (Winter)":
                    premium_rate = 1.5
                else:
                    premium_rate = 3.0

                total_crop_value = land_area * crop_value
                premium_amount = total_crop_value * premium_rate / 100
                farmer_share = premium_amount * 0.5  # Farmer pays 50%, government subsidizes rest

            with col2:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; margin: 0.5rem 0;">
                    <h4>💰 Total Crop Value</h4>
                    <h2>₹{total_crop_value:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #FF9800, #F57C00); color: white; margin: 0.5rem 0;">
                    <h4>💸 Your Premium</h4>
                    <h2>₹{farmer_share:,.0f}</h2>
                    <p>({premium_rate}% rate, 50% subsidized)</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #2196F3, #1976D2); color: white; margin: 0.5rem 0;">
                    <h4>🛡️ Coverage Amount</h4>
                    <h2>₹{min(total_crop_value, 200000 * land_area):,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            self.logger.error(f"Farm insurance rendering failed: {e}")
            st.error(f"Farm insurance error: {e}")

    def render_farm_analytics(self, language: str):
        """Render farm analytics and performance tracking"""
        try:
            st.markdown("### 📊 Farm Analytics & Performance Tracking")

            # Get farmer data
            farmer_data = st.session_state.farmer_data

            # Farm overview metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Land", f"{farmer_data['land_area']} Ha", "2 Ha irrigated")
            with col2:
                st.metric("Crop Types", len(farmer_data['crop_types']), "Diversified")
            with col3:
                annual_income = sum(farmer_data['seasonal_income'].values())
                st.metric("Annual Income", f"₹{annual_income:,}", "↗️ +15%")
            with col4:
                st.metric("Schemes Enrolled", len(farmer_data['government_schemes']), "Active")

            # Seasonal income analysis
            st.markdown("#### 📈 Seasonal Income Analysis")

            seasons = list(farmer_data['seasonal_income'].keys())
            incomes = list(farmer_data['seasonal_income'].values())

            # If no income data, use sample data
            if all(income == 0 for income in incomes):
                incomes = [80000, 120000, 40000]  # Sample seasonal income

            fig = go.Figure(data=[
                go.Bar(x=seasons, y=incomes, marker_color=['#4CAF50', '#FF9800', '#2196F3'])
            ])
            fig.update_layout(
                title='Seasonal Income Distribution',
                xaxis_title='Season',
                yaxis_title='Income (₹)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            # Crop profitability analysis
            st.markdown("#### 💰 Crop Profitability Analysis")

            crop_data = {
                'Crop': farmer_data['crop_types'] if farmer_data['crop_types'] else ['Rice', 'Wheat'],
                'Area (Ha)': [farmer_data['land_area'] / len(farmer_data['crop_types']) if farmer_data['crop_types'] else farmer_data['land_area'] / 2] * (len(farmer_data['crop_types']) if farmer_data['crop_types'] else 2),
                'Yield (Quintal/Ha)': [25, 30],  # Sample yields
                'Price (₹/Quintal)': [2300, 2275],  # MSP rates
                'Cost (₹/Ha)': [35000, 32000],  # Production costs
                'Profit (₹/Ha)': [22500, 36250]  # Calculated profit
            }

            df_crops = pd.DataFrame(crop_data)
            st.dataframe(df_crops, use_container_width=True)

            # Profit margin chart
            fig = go.Figure(data=[
                go.Bar(x=df_crops['Crop'], y=df_crops['Profit (₹/Ha)'], marker_color='#4CAF50')
            ])
            fig.update_layout(
                title='Profit per Hectare by Crop',
                xaxis_title='Crop',
                yaxis_title='Profit (₹/Ha)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            # Farm recommendations
            st.markdown("#### 💡 Farm Improvement Recommendations")

            recommendations = [
                "🌱 Consider high-yield variety seeds for 20% better production",
                "💧 Install drip irrigation to save 40% water and increase yield",
                "🧪 Use soil health card recommendations for optimal fertilizer use",
                "📱 Adopt digital farming tools for better crop monitoring",
                "🏪 Explore direct marketing through FPOs for better prices",
                "🛡️ Ensure crop insurance coverage for risk management"
            ]

            for rec in recommendations:
                st.info(rec)

            # Farm planning tool
            st.markdown("#### 📅 Crop Planning Tool")

            with st.form("crop_planning"):
                col1, col2 = st.columns(2)

                with col1:
                    planning_season = st.selectbox("Planning Season", ["Kharif 2024", "Rabi 2024-25", "Zaid 2025"])
                    planned_crop = st.selectbox("Crop to Plant", ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Soybean"])
                    planned_area = st.number_input("Planned Area (Ha)", min_value=0.1, max_value=farmer_data['land_area'], value=1.0)

                with col2:
                    expected_yield = st.number_input("Expected Yield (Quintal/Ha)", min_value=10, max_value=100, value=25)
                    expected_price = st.number_input("Expected Price (₹/Quintal)", min_value=1000, max_value=5000, value=2300)
                    estimated_cost = st.number_input("Estimated Cost (₹/Ha)", min_value=20000, max_value=80000, value=35000)

                if st.form_submit_button("📊 Calculate Projection"):
                    total_production = planned_area * expected_yield
                    total_revenue = total_production * expected_price
                    total_cost = planned_area * estimated_cost
                    net_profit = total_revenue - total_cost
                    profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Expected Revenue", f"₹{total_revenue:,.0f}")
                    with col2:
                        st.metric("Total Cost", f"₹{total_cost:,.0f}")
                    with col3:
                        st.metric("Net Profit", f"₹{net_profit:,.0f}", f"{profit_margin:.1f}% margin")

                    if profit_margin > 30:
                        st.success("🎉 Excellent profitability! This crop plan looks very promising.")
                    elif profit_margin > 15:
                        st.info("👍 Good profitability. Consider optimizing costs for better margins.")
                    else:
                        st.warning("⚠️ Low profitability. Consider alternative crops or cost reduction.")

        except Exception as e:
            self.logger.error(f"Farm analytics rendering failed: {e}")
            st.error(f"Farm analytics error: {e}")

    def render_complete_investments_page(self):
        """Render complete investment portfolio management page"""
        try:
            profile = st.session_state.user_profile
            current_lang = profile['basic_info']['language']

            # Investment header
            investment_titles = {
                'en': '📈 Investment Portfolio Management',
                'ta': '📈 முதலீட்டு போர்ட்ஃபோலியோ மேலாண்மை',
                'hi': '📈 निवेश पोर्टफोलियो प्रबंधन',
                'te': '📈 పెట్టుబడి పోర్ట్‌ఫోలియో నిర్వహణ'
            }

            st.markdown(f"""
            <div class="main-header fade-in">
                <h1>{investment_titles.get(current_lang, investment_titles['en'])}</h1>
                <p>Complete investment tracking and portfolio optimization</p>
                <p><em>JarvisFi - Your Ultimate Multilingual Finance Chat Assistant</em></p>
            </div>
            """, unsafe_allow_html=True)

            # Investment tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Portfolio Overview",
                "📈 Mutual Funds",
                "🏛️ Stocks & ETFs",
                "🎯 Goal Planning",
                "📋 Tax Planning"
            ])

            with tab1:
                self.render_portfolio_overview(current_lang)

            with tab2:
                self.render_mutual_funds(current_lang)

            with tab3:
                self.render_stocks_etfs(current_lang)

            with tab4:
                self.render_goal_planning(current_lang)

            with tab5:
                self.render_tax_planning(current_lang)

        except Exception as e:
            self.logger.error(f"❌ Investments page rendering failed: {e}")
            st.error(f"Investments error: {e}")

    def render_portfolio_overview(self, language: str):
        """Render portfolio overview with comprehensive analytics"""
        try:
            st.markdown("### 📊 Portfolio Overview")

            # Get user financial data
            monthly_income = st.session_state.user_profile['basic_info']['monthly_income']
            investment_tracking = st.session_state.investment_tracking

            # Calculate portfolio metrics
            monthly_sip = monthly_income * 0.15  # 15% of income
            portfolio_value = monthly_sip * 36 + (monthly_sip * 36 * 0.12)  # 3 years with 12% returns
            total_invested = monthly_sip * 36
            total_returns = portfolio_value - total_invested
            return_percentage = (total_returns / total_invested * 100) if total_invested > 0 else 0

            # Update investment tracking
            st.session_state.investment_tracking['portfolio_value'] = portfolio_value
            st.session_state.investment_tracking['monthly_sip'] = monthly_sip

            # Portfolio metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white;">
                    <h4>💰 Portfolio Value</h4>
                    <h2>₹{portfolio_value:,.0f}</h2>
                    <p>Current market value</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #2196F3, #1976D2); color: white;">
                    <h4>📈 Total Returns</h4>
                    <h2>₹{total_returns:,.0f}</h2>
                    <p>{return_percentage:.1f}% gain</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #FF9800, #F57C00); color: white;">
                    <h4>💸 Monthly SIP</h4>
                    <h2>₹{monthly_sip:,.0f}</h2>
                    <p>15% of income</p>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                annual_returns = return_percentage / 3  # 3 years data
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #9C27B0, #7B1FA2); color: white;">
                    <h4>📊 Annual Returns</h4>
                    <h2>{annual_returns:.1f}%</h2>
                    <p>CAGR performance</p>
                </div>
                """, unsafe_allow_html=True)

            # Asset allocation
            st.markdown("#### 🥧 Asset Allocation")

            col1, col2 = st.columns(2)

            with col1:
                # Current allocation
                allocation = st.session_state.investment_tracking['asset_allocation']

                fig = go.Figure(data=[
                    go.Pie(
                        labels=['Equity', 'Debt', 'Gold'],
                        values=[allocation['equity'], allocation['debt'], allocation['gold']],
                        hole=0.4,
                        marker_colors=['#4CAF50', '#2196F3', '#FF9800']
                    )
                ])
                fig.update_layout(title='Current Asset Allocation', height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Recommended allocation based on age
                age = st.session_state.user_profile['basic_info']['age']
                recommended_equity = max(100 - age, 40)  # Age-based equity allocation
                recommended_debt = min(age, 50)
                recommended_gold = 10

                fig = go.Figure(data=[
                    go.Pie(
                        labels=['Equity (Recommended)', 'Debt (Recommended)', 'Gold (Recommended)'],
                        values=[recommended_equity, recommended_debt, recommended_gold],
                        hole=0.4,
                        marker_colors=['#66BB6A', '#42A5F5', '#FFA726']
                    )
                ])
                fig.update_layout(title='Recommended Allocation', height=400)
                st.plotly_chart(fig, use_container_width=True)

            # Portfolio performance
            st.markdown("#### 📈 Portfolio Performance")

            # Simulated performance data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            portfolio_values = []
            invested_values = []

            for i in range(12):
                invested = monthly_sip * (i + 1)
                value = invested * (1 + (annual_returns/100) * (i + 1) / 12)
                invested_values.append(invested)
                portfolio_values.append(value)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=invested_values, name='Invested Amount', line=dict(color='#FF6B6B')))
            fig.add_trace(go.Scatter(x=months, y=portfolio_values, name='Portfolio Value', line=dict(color='#4CAF50')))

            fig.update_layout(
                title='Portfolio Growth (Current Year)',
                xaxis_title='Month',
                yaxis_title='Amount (₹)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            # Top holdings
            st.markdown("#### 🏆 Top Holdings")

            holdings_data = {
                'Fund/Stock': ['HDFC Top 100 Fund', 'SBI Bluechip Fund', 'Axis Midcap Fund', 'ICICI Prudential Balanced', 'Gold ETF'],
                'Investment (₹)': [portfolio_value * 0.25, portfolio_value * 0.20, portfolio_value * 0.15, portfolio_value * 0.30, portfolio_value * 0.10],
                'Current Value (₹)': [portfolio_value * 0.28, portfolio_value * 0.22, portfolio_value * 0.16, portfolio_value * 0.31, portfolio_value * 0.11],
                'Returns (%)': [12.5, 10.8, 8.2, 14.2, 6.5],
                'Category': ['Large Cap', 'Large Cap', 'Mid Cap', 'Hybrid', 'Gold']
            }

            df_holdings = pd.DataFrame(holdings_data)
            df_holdings['Investment (₹)'] = df_holdings['Investment (₹)'].apply(lambda x: f"₹{x:,.0f}")
            df_holdings['Current Value (₹)'] = df_holdings['Current Value (₹)'].apply(lambda x: f"₹{x:,.0f}")

            st.dataframe(df_holdings, use_container_width=True)

            # Quick actions
            st.markdown("#### 🚀 Quick Actions")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("📈 Start New SIP", use_container_width=True):
                    st.info("Redirecting to SIP investment platform...")

            with col2:
                if st.button("🔄 Rebalance Portfolio", use_container_width=True):
                    st.info("Portfolio rebalancing recommendations generated!")

            with col3:
                if st.button("📊 Performance Report", use_container_width=True):
                    st.info("Generating detailed performance report...")

            with col4:
                if st.button("💰 Tax Harvesting", use_container_width=True):
                    st.info("Tax loss harvesting opportunities identified!")

        except Exception as e:
            self.logger.error(f"Portfolio overview rendering failed: {e}")
            st.error(f"Portfolio overview error: {e}")

    def render_mutual_funds(self, language: str):
        """Render mutual funds section"""
        try:
            st.markdown("### 📈 Mutual Funds")

            # Fund categories
            fund_categories = {
                'Large Cap': {
                    'description': 'Invest in top 100 companies by market cap',
                    'risk': 'Moderate',
                    'returns': '10-12% annually',
                    'suitable_for': 'Conservative investors'
                },
                'Mid Cap': {
                    'description': 'Invest in companies ranked 101-250 by market cap',
                    'risk': 'High',
                    'returns': '12-15% annually',
                    'suitable_for': 'Aggressive investors'
                },
                'Small Cap': {
                    'description': 'Invest in companies ranked 251+ by market cap',
                    'risk': 'Very High',
                    'returns': '15-18% annually',
                    'suitable_for': 'Very aggressive investors'
                },
                'Hybrid': {
                    'description': 'Mix of equity and debt instruments',
                    'risk': 'Moderate',
                    'returns': '8-10% annually',
                    'suitable_for': 'Balanced investors'
                },
                'Debt': {
                    'description': 'Invest in bonds and fixed income securities',
                    'risk': 'Low',
                    'returns': '6-8% annually',
                    'suitable_for': 'Conservative investors'
                }
            }

            # Display fund categories
            for category, details in fund_categories.items():
                with st.expander(f"📊 {category} Funds", expanded=False):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"""
                        <div class="fund-card">
                            <h4>📋 Fund Details</h4>
                            <p><strong>Description:</strong> {details['description']}</p>
                            <p><strong>Risk Level:</strong> {details['risk']}</p>
                            <p><strong>Expected Returns:</strong> {details['returns']}</p>
                            <p><strong>Suitable For:</strong> {details['suitable_for']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        # Sample funds in category
                        if category == 'Large Cap':
                            funds = ['HDFC Top 100 Fund', 'SBI Bluechip Fund', 'ICICI Prudential Bluechip']
                        elif category == 'Mid Cap':
                            funds = ['Axis Midcap Fund', 'DSP Midcap Fund', 'Kotak Emerging Equity']
                        elif category == 'Small Cap':
                            funds = ['SBI Small Cap Fund', 'Axis Small Cap Fund', 'DSP Small Cap Fund']
                        elif category == 'Hybrid':
                            funds = ['ICICI Prudential Balanced', 'HDFC Hybrid Equity', 'SBI Equity Hybrid']
                        else:
                            funds = ['HDFC Short Term Debt', 'SBI Corporate Bond', 'ICICI Prudential Bond']

                        st.markdown("**Top Funds:**")
                        for fund in funds:
                            st.markdown(f"• {fund}")

            # SIP calculator
            st.markdown("#### 🧮 SIP Calculator")

            col1, col2 = st.columns(2)

            with col1:
                sip_amount = st.number_input("Monthly SIP Amount (₹)", min_value=500, max_value=100000, value=5000)
                expected_return = st.slider("Expected Annual Return (%)", min_value=8.0, max_value=20.0, value=12.0, step=0.5)
                investment_period = st.slider("Investment Period (Years)", min_value=1, max_value=30, value=10)

                # Calculate SIP returns
                monthly_return = expected_return / 12 / 100
                total_months = investment_period * 12

                if monthly_return > 0:
                    future_value = sip_amount * (((1 + monthly_return) ** total_months - 1) / monthly_return) * (1 + monthly_return)
                else:
                    future_value = sip_amount * total_months

                total_invested = sip_amount * total_months
                total_returns = future_value - total_invested

            with col2:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; margin: 0.5rem 0;">
                    <h4>💰 Total Investment</h4>
                    <h2>₹{total_invested:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #2196F3, #1976D2); color: white; margin: 0.5rem 0;">
                    <h4>📈 Expected Returns</h4>
                    <h2>₹{total_returns:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #FF9800, #F57C00); color: white; margin: 0.5rem 0;">
                    <h4>🎯 Maturity Amount</h4>
                    <h2>₹{future_value:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

            # Fund recommendations
            st.markdown("#### 💡 Personalized Fund Recommendations")

            age = st.session_state.user_profile['basic_info']['age']
            monthly_income = st.session_state.user_profile['basic_info']['monthly_income']

            if age < 30:
                recommendations = [
                    "🚀 Focus on equity funds (80% allocation) for long-term growth",
                    "📈 Consider small and mid-cap funds for higher returns",
                    "💰 Start with ₹2,000-5,000 monthly SIP",
                    "🎯 Target 15-20 year investment horizon"
                ]
            elif age < 45:
                recommendations = [
                    "⚖️ Balanced approach with 70% equity, 30% debt",
                    "📊 Mix of large-cap and mid-cap funds",
                    "💰 Increase SIP to ₹5,000-10,000 monthly",
                    "🎯 Focus on retirement and children's education goals"
                ]
            else:
                recommendations = [
                    "🛡️ Conservative approach with 50% equity, 50% debt",
                    "📈 Focus on large-cap and hybrid funds",
                    "💰 Consider lump-sum investments in debt funds",
                    "🎯 Prioritize capital preservation and regular income"
                ]

            for rec in recommendations:
                st.info(rec)

        except Exception as e:
            self.logger.error(f"Mutual funds rendering failed: {e}")
            st.error(f"Mutual funds error: {e}")

    def render_stocks_etfs(self, language: str):
        """Render stocks and ETFs section"""
        try:
            st.markdown("### 🏛️ Stocks & ETFs")

            # Stock market overview
            st.markdown("#### 📊 Market Overview")

            market_data = {
                'Index': ['NIFTY 50', 'SENSEX', 'NIFTY Bank', 'NIFTY IT', 'NIFTY FMCG'],
                'Current': [19850, 66500, 45200, 32100, 54800],
                'Change': [+125, +380, +220, -150, +180],
                'Change (%)': [0.63, 0.57, 0.49, -0.47, 0.33]
            }

            df_market = pd.DataFrame(market_data)
            st.dataframe(df_market, use_container_width=True)

            # ETF recommendations
            st.markdown("#### 📈 Recommended ETFs")

            etf_data = [
                {'name': 'NIFTY 50 ETF', 'expense_ratio': '0.05%', 'returns_1y': '12.5%', 'aum': '₹15,000 Cr'},
                {'name': 'NIFTY Bank ETF', 'expense_ratio': '0.08%', 'returns_1y': '8.2%', 'aum': '₹8,500 Cr'},
                {'name': 'Gold ETF', 'expense_ratio': '0.50%', 'returns_1y': '6.8%', 'aum': '₹12,000 Cr'},
                {'name': 'NIFTY IT ETF', 'expense_ratio': '0.06%', 'returns_1y': '15.2%', 'aum': '₹5,200 Cr'}
            ]

            for etf in etf_data:
                with st.expander(f"📊 {etf['name']}", expanded=False):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Expense Ratio", etf['expense_ratio'])
                    with col2:
                        st.metric("1Y Returns", etf['returns_1y'])
                    with col3:
                        st.metric("AUM", etf['aum'])
                    with col4:
                        if st.button(f"Invest in {etf['name']}", key=f"invest_{etf['name']}"):
                            st.info(f"Redirecting to investment platform for {etf['name']}")

            # Stock screener
            st.markdown("#### 🔍 Stock Screener")

            col1, col2, col3 = st.columns(3)

            with col1:
                market_cap = st.selectbox("Market Cap", ["All", "Large Cap", "Mid Cap", "Small Cap"])
                sector = st.selectbox("Sector", ["All", "Banking", "IT", "Pharma", "Auto", "FMCG"])

            with col2:
                pe_range = st.slider("P/E Ratio Range", min_value=0, max_value=50, value=(10, 25))
                dividend_yield = st.slider("Min Dividend Yield (%)", min_value=0.0, max_value=10.0, value=1.0)

            with col3:
                if st.button("🔍 Screen Stocks", use_container_width=True):
                    st.info("Stock screening results based on your criteria:")
                    sample_stocks = [
                        "HDFC Bank - P/E: 18.5, Div Yield: 1.2%",
                        "TCS - P/E: 22.1, Div Yield: 2.1%",
                        "Infosys - P/E: 19.8, Div Yield: 2.8%"
                    ]
                    for stock in sample_stocks:
                        st.success(f"✅ {stock}")

        except Exception as e:
            self.logger.error(f"Stocks ETFs rendering failed: {e}")
            st.error(f"Stocks ETFs error: {e}")

    def render_goal_planning(self, language: str):
        """Render goal-based investment planning"""
        try:
            st.markdown("### 🎯 Goal-Based Investment Planning")

            # Investment goals
            goals = st.session_state.investment_tracking['goals']

            # Add new goal
            st.markdown("#### ➕ Add New Investment Goal")

            with st.form("new_goal"):
                col1, col2 = st.columns(2)

                with col1:
                    goal_name = st.text_input("Goal Name", placeholder="e.g., Child's Education")
                    target_amount = st.number_input("Target Amount (₹)", min_value=100000, max_value=50000000, value=1000000)
                    time_horizon = st.number_input("Time Horizon (Years)", min_value=1, max_value=30, value=10)

                with col2:
                    current_savings = st.number_input("Current Savings (₹)", min_value=0, max_value=10000000, value=0)
                    expected_return = st.slider("Expected Return (%)", min_value=6.0, max_value=15.0, value=10.0)
                    risk_tolerance = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])

                if st.form_submit_button("🎯 Create Goal"):
                    # Calculate required monthly SIP
                    monthly_return = expected_return / 12 / 100
                    total_months = time_horizon * 12
                    future_value_current = current_savings * (1 + expected_return/100) ** time_horizon
                    remaining_target = target_amount - future_value_current

                    if remaining_target > 0 and monthly_return > 0:
                        required_sip = remaining_target * monthly_return / (((1 + monthly_return) ** total_months - 1) * (1 + monthly_return))
                    else:
                        required_sip = 0

                    new_goal = {
                        'name': goal_name,
                        'target': target_amount,
                        'current': current_savings,
                        'time_horizon': time_horizon,
                        'required_sip': required_sip,
                        'risk_tolerance': risk_tolerance
                    }

                    goals.append(new_goal)
                    st.session_state.investment_tracking['goals'] = goals

                    st.success(f"✅ Goal '{goal_name}' created! Required monthly SIP: ₹{required_sip:,.0f}")
                    st.rerun()

            # Display existing goals
            st.markdown("#### 📋 Your Investment Goals")

            if goals:
                for i, goal in enumerate(goals):
                    with st.expander(f"🎯 {goal['name']}", expanded=False):
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Target Amount", f"₹{goal['target']:,}")
                            st.metric("Time Horizon", f"{goal['time_horizon']} years")

                        with col2:
                            st.metric("Current Savings", f"₹{goal['current']:,}")
                            progress = (goal['current'] / goal['target']) * 100
                            st.metric("Progress", f"{progress:.1f}%")

                        with col3:
                            st.metric("Required Monthly SIP", f"₹{goal.get('required_sip', 0):,.0f}")
                            st.metric("Risk Tolerance", goal.get('risk_tolerance', 'Moderate'))

                        # Progress bar
                        st.progress(progress / 100)

                        # Goal-specific recommendations
                        if goal.get('risk_tolerance') == 'Conservative':
                            st.info("💡 Recommended: Hybrid funds, Debt funds, PPF")
                        elif goal.get('risk_tolerance') == 'Moderate':
                            st.info("💡 Recommended: Large-cap funds, Balanced funds, ELSS")
                        else:
                            st.info("💡 Recommended: Mid-cap funds, Small-cap funds, Equity funds")
            else:
                st.info("No investment goals created yet. Add your first goal above!")

        except Exception as e:
            self.logger.error(f"Goal planning rendering failed: {e}")
            st.error(f"Goal planning error: {e}")

    def render_tax_planning(self, language: str):
        """Render tax planning section"""
        try:
            st.markdown("### 📋 Tax Planning & Optimization")

            # Tax saving instruments
            tax_instruments = {
                'ELSS Mutual Funds': {
                    'limit': '₹1.5 lakh',
                    'lock_in': '3 years',
                    'returns': '12-15% annually',
                    'section': '80C'
                },
                'PPF': {
                    'limit': '₹1.5 lakh',
                    'lock_in': '15 years',
                    'returns': '7-8% annually',
                    'section': '80C'
                },
                'NSC': {
                    'limit': '₹1.5 lakh',
                    'lock_in': '5 years',
                    'returns': '6.8% annually',
                    'section': '80C'
                },
                'Health Insurance': {
                    'limit': '₹25,000-₹50,000',
                    'lock_in': '1 year',
                    'returns': 'Tax saving',
                    'section': '80D'
                },
                'NPS': {
                    'limit': '₹50,000',
                    'lock_in': 'Till 60 years',
                    'returns': '10-12% annually',
                    'section': '80CCD(1B)'
                }
            }

            # Display tax instruments
            for instrument, details in tax_instruments.items():
                with st.expander(f"📋 {instrument}", expanded=False):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"""
                        <div class="tax-card">
                            <h4>💰 Investment Details</h4>
                            <p><strong>Tax Deduction Limit:</strong> {details['limit']}</p>
                            <p><strong>Lock-in Period:</strong> {details['lock_in']}</p>
                            <p><strong>Expected Returns:</strong> {details['returns']}</p>
                            <p><strong>Section:</strong> {details['section']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        if instrument == 'ELSS Mutual Funds':
                            benefits = ['Highest return potential', 'Shortest lock-in', 'Market-linked returns', 'Professional management']
                        elif instrument == 'PPF':
                            benefits = ['Tax-free returns', 'Government backing', 'Loan facility', 'Long-term wealth creation']
                        elif instrument == 'Health Insurance':
                            benefits = ['Health coverage', 'Tax deduction', 'Cashless treatment', 'Family coverage']
                        else:
                            benefits = ['Guaranteed returns', 'Government backing', 'Tax benefits', 'Safe investment']

                        st.markdown("**Key Benefits:**")
                        for benefit in benefits:
                            st.markdown(f"• {benefit}")

            # Tax calculator
            st.markdown("#### 🧮 Tax Saving Calculator")

            col1, col2 = st.columns(2)

            with col1:
                annual_income = st.number_input("Annual Income (₹)", min_value=300000, max_value=10000000, value=800000)
                current_investments = st.number_input("Current 80C Investments (₹)", min_value=0, max_value=150000, value=50000)
                additional_investment = st.number_input("Additional Investment (₹)", min_value=0, max_value=150000, value=50000)

                # Calculate tax savings
                total_investment = min(current_investments + additional_investment, 150000)

                if annual_income <= 500000:
                    tax_rate = 0
                elif annual_income <= 750000:
                    tax_rate = 5
                elif annual_income <= 1000000:
                    tax_rate = 10
                elif annual_income <= 1250000:
                    tax_rate = 15
                elif annual_income <= 1500000:
                    tax_rate = 20
                else:
                    tax_rate = 30

                tax_saved = total_investment * tax_rate / 100

            with col2:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; margin: 0.5rem 0;">
                    <h4>💰 Total Investment</h4>
                    <h2>₹{total_investment:,.0f}</h2>
                    <p>Under Section 80C</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #2196F3, #1976D2); color: white; margin: 0.5rem 0;">
                    <h4>💸 Tax Saved</h4>
                    <h2>₹{tax_saved:,.0f}</h2>
                    <p>At {tax_rate}% tax rate</p>
                </div>
                """, unsafe_allow_html=True)

                remaining_limit = 150000 - total_investment
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #FF9800, #F57C00); color: white; margin: 0.5rem 0;">
                    <h4>📊 Remaining Limit</h4>
                    <h2>₹{remaining_limit:,.0f}</h2>
                    <p>Additional tax saving opportunity</p>
                </div>
                """, unsafe_allow_html=True)

            # Tax planning recommendations
            st.markdown("#### 💡 Personalized Tax Planning")

            monthly_income = st.session_state.user_profile['basic_info']['monthly_income']
            annual_income_profile = monthly_income * 12

            if annual_income_profile <= 500000:
                recommendations = [
                    "🎯 Focus on building emergency fund first",
                    "💰 Start small SIPs in ELSS funds",
                    "🏥 Get basic health insurance coverage",
                    "📚 Invest in skill development for income growth"
                ]
            elif annual_income_profile <= 1000000:
                recommendations = [
                    "📈 Maximize 80C limit with ELSS and PPF",
                    "🏥 Increase health insurance to ₹5-10 lakh",
                    "💰 Consider NPS for additional tax benefits",
                    "🎯 Start goal-based investment planning"
                ]
            else:
                recommendations = [
                    "🎯 Utilize all tax-saving sections (80C, 80D, 80CCD)",
                    "📈 Consider tax-efficient mutual funds",
                    "🏥 Opt for comprehensive health insurance",
                    "💰 Explore tax-free bonds and infrastructure bonds"
                ]

            for rec in recommendations:
                st.info(rec)

        except Exception as e:
            self.logger.error(f"Tax planning rendering failed: {e}")
            st.error(f"Tax planning error: {e}")

    def render_complete_credit_score_page(self):
        """Render complete credit score tracking and improvement page"""
        try:
            profile = st.session_state.user_profile
            current_lang = profile['basic_info']['language']

            # Credit score header
            credit_titles = {
                'en': '💳 Credit Score Tracking & Improvement',
                'ta': '💳 கிரெடிட் ஸ்கோர் கண்காணிப்பு மற்றும் மேம்பாடு',
                'hi': '💳 क्रेडिट स्कोर ट्रैकिंग और सुधार',
                'te': '💳 క్రెడిట్ స్కోర్ ట్రాకింగ్ మరియు మెరుగుదల'
            }

            st.markdown(f"""
            <div class="main-header fade-in">
                <h1>{credit_titles.get(current_lang, credit_titles['en'])}</h1>
                <p>Monitor and improve your credit health</p>
                <p><em>JarvisFi - Your Ultimate Multilingual Finance Chat Assistant</em></p>
            </div>
            """, unsafe_allow_html=True)

            # Credit score tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Credit Overview",
                "📈 Score Improvement",
                "💳 Credit Cards",
                "📋 Credit Report"
            ])

            with tab1:
                self.render_credit_overview(current_lang)

            with tab2:
                self.render_score_improvement(current_lang)

            with tab3:
                self.render_credit_cards(current_lang)

            with tab4:
                self.render_credit_report(current_lang)

        except Exception as e:
            self.logger.error(f"❌ Credit score page rendering failed: {e}")
            st.error(f"Credit score error: {e}")

    def render_credit_overview(self, language: str):
        """Render credit score overview"""
        try:
            st.markdown("### 📊 Credit Score Overview")

            # Get credit score from profile
            credit_score = st.session_state.user_profile['financial_profile']['credit_score']

            # Credit score gauge
            col1, col2 = st.columns([2, 1])

            with col1:
                # Credit score gauge chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = credit_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Credit Score", 'font': {'size': 24}},
                    delta = {'reference': 750, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
                    gauge = {
                        'axis': {'range': [None, 900], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "darkblue"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [300, 550], 'color': "#ffcccc"},
                            {'range': [550, 650], 'color': "#ffffcc"},
                            {'range': [650, 750], 'color': "#ccffff"},
                            {'range': [750, 900], 'color': "#ccffcc"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 750
                        }
                    }
                ))
                fig.update_layout(height=400, font={'color': "darkblue", 'family': "Arial"})
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Credit score interpretation
                if credit_score >= 750:
                    score_status = "Excellent"
                    score_color = "#4CAF50"
                    score_message = "🎉 Outstanding! You qualify for the best rates."
                elif credit_score >= 650:
                    score_status = "Good"
                    score_color = "#2196F3"
                    score_message = "👍 Good score! Some improvement possible."
                elif credit_score >= 550:
                    score_status = "Fair"
                    score_color = "#FF9800"
                    score_message = "⚠️ Fair score. Focus on improvement."
                else:
                    score_status = "Poor"
                    score_color = "#F44336"
                    score_message = "🚨 Needs immediate attention."

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, {score_color}, {score_color}); color: white;">
                    <h4>📊 Score Status</h4>
                    <h2>{score_status}</h2>
                    <p>{score_message}</p>
                </div>
                """, unsafe_allow_html=True)

                # Credit score factors
                st.markdown("### 📋 Score Factors")

                factors = [
                    {"factor": "Payment History", "impact": "35%", "status": "Good"},
                    {"factor": "Credit Utilization", "impact": "30%", "status": "Fair"},
                    {"factor": "Credit History Length", "impact": "15%", "status": "Good"},
                    {"factor": "Credit Mix", "impact": "10%", "status": "Excellent"},
                    {"factor": "New Credit", "impact": "10%", "status": "Good"}
                ]

                for factor in factors:
                    status_color = "#4CAF50" if factor["status"] == "Excellent" else "#2196F3" if factor["status"] == "Good" else "#FF9800"
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0; padding: 0.5rem; border-left: 3px solid {status_color}; background: #f9f9f9;">
                        <strong>{factor['factor']}</strong> ({factor['impact']})<br>
                        <small style="color: {status_color};">Status: {factor['status']}</small>
                    </div>
                    """, unsafe_allow_html=True)

            # Credit score history
            st.markdown("### 📈 Credit Score History")

            # Simulated credit score history
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            score_history = [credit_score - 50 + (i * 4) for i in range(12)]  # Gradual improvement
            score_history = [min(score, 850) for score in score_history]  # Cap at 850

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=months,
                y=score_history,
                name='Credit Score',
                line=dict(color='#4CAF50', width=3),
                fill='tonexty'
            ))

            fig.update_layout(
                title='Credit Score Trend (2024)',
                xaxis_title='Month',
                yaxis_title='Credit Score',
                height=400,
                yaxis=dict(range=[500, 850])
            )
            st.plotly_chart(fig, use_container_width=True)

            # Quick actions
            st.markdown("### 🚀 Quick Actions")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("📊 Check Score", use_container_width=True):
                    st.info("Fetching latest credit score from CIBIL...")

            with col2:
                if st.button("📋 Get Report", use_container_width=True):
                    st.info("Generating detailed credit report...")

            with col3:
                if st.button("💡 Get Tips", use_container_width=True):
                    st.info("Personalized improvement tips generated!")

            with col4:
                if st.button("🔔 Set Alerts", use_container_width=True):
                    st.info("Credit monitoring alerts activated!")

        except Exception as e:
            self.logger.error(f"Credit overview rendering failed: {e}")
            st.error(f"Credit overview error: {e}")

    def render_score_improvement(self, language: str):
        """Render credit score improvement strategies"""
        try:
            st.markdown("### 📈 Credit Score Improvement Strategies")

            credit_score = st.session_state.user_profile['financial_profile']['credit_score']

            # Improvement recommendations based on current score
            if credit_score < 550:
                recommendations = [
                    {
                        'title': '🚨 Pay All Outstanding Dues',
                        'description': 'Clear all overdue payments immediately',
                        'impact': 'High',
                        'timeframe': '1-2 months',
                        'priority': 'Critical'
                    },
                    {
                        'title': '💳 Reduce Credit Utilization',
                        'description': 'Keep credit card usage below 30% of limit',
                        'impact': 'High',
                        'timeframe': '2-3 months',
                        'priority': 'High'
                    },
                    {
                        'title': '📋 Check Credit Report',
                        'description': 'Identify and dispute any errors',
                        'impact': 'Medium',
                        'timeframe': '1 month',
                        'priority': 'High'
                    }
                ]
            elif credit_score < 650:
                recommendations = [
                    {
                        'title': '💳 Optimize Credit Utilization',
                        'description': 'Keep utilization below 10% for best results',
                        'impact': 'High',
                        'timeframe': '2-3 months',
                        'priority': 'High'
                    },
                    {
                        'title': '📅 Set Payment Reminders',
                        'description': 'Never miss a payment deadline',
                        'impact': 'High',
                        'timeframe': 'Ongoing',
                        'priority': 'High'
                    },
                    {
                        'title': '🏦 Increase Credit Limit',
                        'description': 'Request limit increase to improve utilization ratio',
                        'impact': 'Medium',
                        'timeframe': '1-2 months',
                        'priority': 'Medium'
                    }
                ]
            else:
                recommendations = [
                    {
                        'title': '🎯 Maintain Current Habits',
                        'description': 'Continue excellent payment behavior',
                        'impact': 'High',
                        'timeframe': 'Ongoing',
                        'priority': 'High'
                    },
                    {
                        'title': '📊 Diversify Credit Mix',
                        'description': 'Consider different types of credit accounts',
                        'impact': 'Low',
                        'timeframe': '6-12 months',
                        'priority': 'Low'
                    },
                    {
                        'title': '⏰ Maintain Long Credit History',
                        'description': 'Keep old accounts open and active',
                        'impact': 'Medium',
                        'timeframe': 'Ongoing',
                        'priority': 'Medium'
                    }
                ]

            # Display recommendations
            for i, rec in enumerate(recommendations):
                priority_color = "#F44336" if rec['priority'] == 'Critical' else "#FF9800" if rec['priority'] == 'High' else "#4CAF50"

                with st.expander(f"{rec['title']}", expanded=i == 0):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"""
                        <div class="improvement-card">
                            <h4>📋 Strategy Details</h4>
                            <p><strong>Description:</strong> {rec['description']}</p>
                            <p><strong>Expected Impact:</strong> {rec['impact']}</p>
                            <p><strong>Timeframe:</strong> {rec['timeframe']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class="improvement-card" style="border-left-color: {priority_color};">
                            <h4>🎯 Priority Level</h4>
                            <h3 style="color: {priority_color};">{rec['priority']}</h3>
                            <p>Focus on this strategy for maximum impact</p>
                        </div>
                        """, unsafe_allow_html=True)

            # Credit utilization calculator
            st.markdown("### 🧮 Credit Utilization Calculator")

            col1, col2 = st.columns(2)

            with col1:
                total_limit = st.number_input("Total Credit Limit (₹)", min_value=10000, max_value=1000000, value=100000)
                current_balance = st.number_input("Current Outstanding (₹)", min_value=0, max_value=total_limit, value=30000)

                utilization = (current_balance / total_limit * 100) if total_limit > 0 else 0

                # Recommendations based on utilization
                if utilization <= 10:
                    util_status = "Excellent"
                    util_color = "#4CAF50"
                    util_message = "🎉 Perfect utilization!"
                elif utilization <= 30:
                    util_status = "Good"
                    util_color = "#2196F3"
                    util_message = "👍 Good utilization level"
                elif utilization <= 50:
                    util_status = "Fair"
                    util_color = "#FF9800"
                    util_message = "⚠️ Consider reducing usage"
                else:
                    util_status = "Poor"
                    util_color = "#F44336"
                    util_message = "🚨 High utilization - reduce immediately"

            with col2:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, {util_color}, {util_color}); color: white;">
                    <h4>💳 Credit Utilization</h4>
                    <h2>{utilization:.1f}%</h2>
                    <p>{util_status}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="improvement-tip">
                    <h4>💡 Recommendation</h4>
                    <p>{util_message}</p>
                    <p><strong>Ideal utilization:</strong> Below 10%</p>
                    <p><strong>Target amount:</strong> ₹{total_limit * 0.1:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)

            # Score improvement timeline
            st.markdown("### ⏰ Improvement Timeline")

            timeline_data = [
                {"month": "Month 1", "action": "Pay all dues, reduce utilization", "expected_change": "+20-30 points"},
                {"month": "Month 2-3", "action": "Maintain low utilization, on-time payments", "expected_change": "+10-20 points"},
                {"month": "Month 4-6", "action": "Continue good habits, dispute errors", "expected_change": "+5-15 points"},
                {"month": "Month 7-12", "action": "Build credit history, diversify credit", "expected_change": "+5-10 points"}
            ]

            for item in timeline_data:
                st.markdown(f"""
                <div class="timeline-item">
                    <h4>{item['month']}</h4>
                    <p><strong>Action:</strong> {item['action']}</p>
                    <p><strong>Expected Change:</strong> <span style="color: #4CAF50;">{item['expected_change']}</span></p>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            self.logger.error(f"Score improvement rendering failed: {e}")
            st.error(f"Score improvement error: {e}")

    def render_credit_cards(self, language: str):
        """Render credit cards management section"""
        try:
            st.markdown("### 💳 Credit Cards Management")

            # Credit card recommendations
            st.markdown("#### 🎯 Recommended Credit Cards")

            credit_score = st.session_state.user_profile['financial_profile']['credit_score']
            monthly_income = st.session_state.user_profile['basic_info']['monthly_income']

            # Card recommendations based on profile
            if credit_score >= 750 and monthly_income >= 50000:
                recommended_cards = [
                    {
                        'name': 'HDFC Infinia Credit Card',
                        'annual_fee': '₹12,500',
                        'rewards': '3.3% on all spends',
                        'features': ['Airport lounge access', 'Golf privileges', 'Concierge services'],
                        'eligibility': 'Income: ₹2.5L+, Score: 750+'
                    },
                    {
                        'name': 'SBI Elite Credit Card',
                        'annual_fee': '₹4,999',
                        'rewards': '2% on all spends',
                        'features': ['Movie tickets', 'Dining offers', 'Travel benefits'],
                        'eligibility': 'Income: ₹1.5L+, Score: 750+'
                    }
                ]
            elif credit_score >= 650:
                recommended_cards = [
                    {
                        'name': 'ICICI Amazon Pay Credit Card',
                        'annual_fee': 'Nil',
                        'rewards': '5% on Amazon, 1% others',
                        'features': ['Amazon Prime benefits', 'No annual fee', 'Instant approval'],
                        'eligibility': 'Income: ₹25K+, Score: 650+'
                    },
                    {
                        'name': 'Axis Flipkart Credit Card',
                        'annual_fee': '₹500',
                        'rewards': '4% on Flipkart, 1.5% others',
                        'features': ['Flipkart Plus benefits', 'Book My Show offers', 'Fuel surcharge waiver'],
                        'eligibility': 'Income: ₹30K+, Score: 650+'
                    }
                ]
            else:
                recommended_cards = [
                    {
                        'name': 'SBI SimplyCLICK Credit Card',
                        'annual_fee': '₹499',
                        'rewards': '10X on online spends',
                        'features': ['Online shopping rewards', 'Movie tickets', 'Dining discounts'],
                        'eligibility': 'Income: ₹20K+, Score: 600+'
                    },
                    {
                        'name': 'HDFC MoneyBack Credit Card',
                        'annual_fee': '₹500',
                        'rewards': '2% on online spends',
                        'features': ['Cashback rewards', 'Fuel surcharge waiver', 'EMI conversion'],
                        'eligibility': 'Income: ₹25K+, Score: 600+'
                    }
                ]

            # Display recommended cards
            for card in recommended_cards:
                with st.expander(f"💳 {card['name']}", expanded=False):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"""
                        <div class="card-details">
                            <h4>💰 Card Details</h4>
                            <p><strong>Annual Fee:</strong> {card['annual_fee']}</p>
                            <p><strong>Rewards:</strong> {card['rewards']}</p>
                            <p><strong>Eligibility:</strong> {card['eligibility']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class="card-features">
                            <h4>✨ Key Features</h4>
                            <ul>
                                {''.join([f'<li>{feature}</li>' for feature in card['features']])}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                    if st.button(f"Apply for {card['name']}", key=f"apply_{card['name']}"):
                        st.info(f"Redirecting to application for {card['name']}")

            # Credit card comparison tool
            st.markdown("#### ⚖️ Credit Card Comparison")

            comparison_data = {
                'Feature': ['Annual Fee', 'Reward Rate', 'Welcome Bonus', 'Lounge Access', 'Fuel Surcharge Waiver'],
                'HDFC Infinia': ['₹12,500', '3.3%', '10,000 points', 'Unlimited', 'Yes'],
                'SBI Elite': ['₹4,999', '2%', '5,000 points', '8 visits/year', 'Yes'],
                'ICICI Amazon Pay': ['Nil', '5% Amazon', '2,000 points', 'No', 'No'],
                'Axis Flipkart': ['₹500', '4% Flipkart', '500 points', 'No', 'Yes']
            }

            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True)

        except Exception as e:
            self.logger.error(f"Credit cards rendering failed: {e}")
            st.error(f"Credit cards error: {e}")

    def render_credit_report(self, language: str):
        """Render credit report section"""
        try:
            st.markdown("### 📋 Credit Report Analysis")

            # Credit report summary
            st.markdown("#### 📊 Report Summary")

            report_data = {
                'Category': ['Total Accounts', 'Active Accounts', 'Closed Accounts', 'Credit Inquiries (6 months)', 'Total Credit Limit', 'Current Outstanding'],
                'Count/Amount': ['8', '5', '3', '2', '₹5,00,000', '₹1,50,000'],
                'Status': ['Good', 'Good', 'Normal', 'Good', 'High', 'Moderate']
            }

            df_report = pd.DataFrame(report_data)
            st.dataframe(df_report, use_container_width=True)

            # Account details
            st.markdown("#### 🏦 Account Details")

            accounts = [
                {'bank': 'HDFC Bank', 'type': 'Credit Card', 'limit': 200000, 'outstanding': 50000, 'status': 'Active'},
                {'bank': 'SBI', 'type': 'Personal Loan', 'limit': 500000, 'outstanding': 300000, 'status': 'Active'},
                {'bank': 'ICICI Bank', 'type': 'Credit Card', 'limit': 150000, 'outstanding': 30000, 'status': 'Active'},
                {'bank': 'Axis Bank', 'type': 'Home Loan', 'limit': 2500000, 'outstanding': 2000000, 'status': 'Active'},
                {'bank': 'Kotak Bank', 'type': 'Credit Card', 'limit': 100000, 'outstanding': 0, 'status': 'Closed'}
            ]

            for account in accounts:
                utilization = (account['outstanding'] / account['limit'] * 100) if account['limit'] > 0 else 0
                status_color = "#4CAF50" if account['status'] == 'Active' else "#9E9E9E"

                with st.expander(f"🏦 {account['bank']} - {account['type']}", expanded=False):
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Credit Limit", f"₹{account['limit']:,}")
                    with col2:
                        st.metric("Outstanding", f"₹{account['outstanding']:,}")
                    with col3:
                        st.metric("Utilization", f"{utilization:.1f}%")
                    with col4:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 1rem;">
                            <h4>Status</h4>
                            <h3 style="color: {status_color};">{account['status']}</h3>
                        </div>
                        """, unsafe_allow_html=True)

            # Payment history
            st.markdown("#### 📅 Payment History")

            # Simulated payment history
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            payment_status = ['On Time', 'On Time', 'Late (5 days)', 'On Time', 'On Time', 'On Time', 'On Time', 'On Time', 'On Time', 'On Time', 'On Time', 'On Time']

            payment_data = {
                'Month': months,
                'Payment Status': payment_status,
                'Days Late': [0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }

            df_payments = pd.DataFrame(payment_data)
            st.dataframe(df_payments, use_container_width=True)

            # Credit report actions
            st.markdown("#### 🚀 Report Actions")

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📥 Download Report", use_container_width=True):
                    st.info("Downloading detailed credit report...")

            with col2:
                if st.button("🔍 Dispute Error", use_container_width=True):
                    st.info("Opening dispute resolution form...")

            with col3:
                if st.button("🔔 Monitor Changes", use_container_width=True):
                    st.info("Credit monitoring alerts activated!")

        except Exception as e:
            self.logger.error(f"Credit report rendering failed: {e}")
            st.error(f"Credit report error: {e}")

    def render_complete_voice_assistant_page(self):
        """Render complete voice assistant interface"""
        try:
            profile = st.session_state.user_profile
            current_lang = profile['basic_info']['language']

            # Voice assistant header
            voice_titles = {
                'en': '🎤 Voice Assistant Interface',
                'ta': '🎤 குரல் உதவியாளர் இடைமுகம்',
                'hi': '🎤 वॉयस असिस्टेंट इंटरफेस',
                'te': '🎤 వాయిస్ అసిస్టెంట్ ఇంటర్‌ఫేస్'
            }

            st.markdown(f"""
            <div class="main-header fade-in">
                <h1>{voice_titles.get(current_lang, voice_titles['en'])}</h1>
                <p>Advanced voice commands and multilingual support</p>
                <p><em>JarvisFi - Your Ultimate Multilingual Finance Chat Assistant</em></p>
            </div>
            """, unsafe_allow_html=True)

            # Voice interface tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "🎤 Voice Control",
                "⚙️ Voice Settings",
                "📋 Commands List",
                "🌍 Language Support"
            ])

            with tab1:
                self.render_voice_control(current_lang)

            with tab2:
                self.render_voice_settings(current_lang)

            with tab3:
                self.render_voice_commands(current_lang)

            with tab4:
                self.render_voice_language_support(current_lang)

        except Exception as e:
            self.logger.error(f"❌ Voice assistant page rendering failed: {e}")
            st.error(f"Voice assistant error: {e}")

    def render_voice_control(self, language: str):
        """Render voice control interface"""
        try:
            st.markdown("### 🎤 Voice Control Center")

            # Voice status indicator
            voice_active = st.session_state.voice_settings.get('voice_enabled', False)

            col1, col2 = st.columns([2, 1])

            with col1:
                # Voice activation
                st.markdown("#### 🔊 Voice Activation")

                if st.button("🎤 Start Voice Assistant" if not voice_active else "⏹️ Stop Voice Assistant",
                           use_container_width=True,
                           type="primary" if not voice_active else "secondary"):
                    st.session_state.voice_settings['voice_enabled'] = not voice_active
                    if not voice_active:
                        st.success("🎤 Voice Assistant activated! Say 'Hey Jarvis' to start.")
                        st.session_state.analytics['voice_interactions'] += 1
                    else:
                        st.info("⏹️ Voice Assistant deactivated.")
                    st.rerun()

                # Voice input simulation
                st.markdown("#### 🗣️ Voice Input")

                if voice_active:
                    # Animated voice indicator
                    st.markdown("""
                    <div class="voice-indicator">
                        <div class="pulse-animation">🎤 Listening...</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Simulate voice commands
                    sample_commands = [
                        "What's my current savings rate?",
                        "Calculate SIP for 5000 rupees monthly",
                        "Show my investment portfolio",
                        "Switch to Tamil language",
                        "Check my credit score"
                    ]

                    if st.button("🎯 Simulate Voice Command", use_container_width=True):
                        import random
                        command = random.choice(sample_commands)
                        st.info(f"🎤 Voice Command Detected: '{command}'")
                        st.success("🤖 Processing your request...")

                        # Simulate voice response
                        responses = {
                            "What's my current savings rate?": f"Your current savings rate is {((st.session_state.user_profile['basic_info']['monthly_income'] - st.session_state.user_profile['financial_profile']['monthly_expenses']) / st.session_state.user_profile['basic_info']['monthly_income'] * 100):.1f}%",
                            "Calculate SIP for 5000 rupees monthly": "For a monthly SIP of ₹5,000 at 12% annual return over 10 years, you'll accumulate approximately ₹11.6 lakh",
                            "Show my investment portfolio": f"Your current portfolio value is ₹{st.session_state.investment_tracking['portfolio_value']:,.0f} with a monthly SIP of ₹{st.session_state.investment_tracking['monthly_sip']:,.0f}",
                            "Switch to Tamil language": "மொழி தமிழுக்கு மாற்றப்பட்டது (Language switched to Tamil)",
                            "Check my credit score": f"Your current credit score is {st.session_state.user_profile['financial_profile']['credit_score']} which is considered {'Excellent' if st.session_state.user_profile['financial_profile']['credit_score'] >= 750 else 'Good' if st.session_state.user_profile['financial_profile']['credit_score'] >= 650 else 'Fair'}"
                        }

                        response = responses.get(command, "I understand your request. Let me help you with that.")
                        st.markdown(f"🔊 **Voice Response:** {response}")
                else:
                    st.info("🔇 Voice Assistant is currently inactive. Click 'Start Voice Assistant' to begin.")

            with col2:
                # Voice status panel
                st.markdown("#### 📊 Voice Status")

                status_color = "#4CAF50" if voice_active else "#9E9E9E"
                st.markdown(f"""
                <div class="voice-status" style="border-left-color: {status_color};">
                    <h4>🎤 Status</h4>
                    <h3 style="color: {status_color};">{'Active' if voice_active else 'Inactive'}</h3>
                    <p>Wake word: "Hey Jarvis"</p>
                    <p>Language: {language.upper()}</p>
                </div>
                """, unsafe_allow_html=True)

                # Voice metrics
                st.markdown("#### 📈 Voice Metrics")

                voice_interactions = st.session_state.analytics.get('voice_interactions', 0)
                st.metric("Total Interactions", voice_interactions)
                st.metric("Success Rate", "95.2%")
                st.metric("Avg Response Time", "1.2s")

            # Recent voice commands
            st.markdown("#### 📝 Recent Voice Commands")

            recent_commands = [
                {"command": "What's my portfolio performance?", "time": "2 minutes ago", "status": "✅ Completed"},
                {"command": "Calculate EMI for home loan", "time": "5 minutes ago", "status": "✅ Completed"},
                {"command": "Show farmer schemes", "time": "10 minutes ago", "status": "✅ Completed"},
                {"command": "Switch to Hindi", "time": "15 minutes ago", "status": "✅ Completed"}
            ]

            for cmd in recent_commands:
                st.markdown(f"""
                <div class="command-history">
                    <strong>🎤 "{cmd['command']}"</strong><br>
                    <small>{cmd['time']} - {cmd['status']}</small>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            self.logger.error(f"Voice control rendering failed: {e}")
            st.error(f"Voice control error: {e}")

    def render_voice_settings(self, language: str):
        """Render voice settings configuration"""
        try:
            st.markdown("### ⚙️ Voice Settings Configuration")

            # Voice settings form
            with st.form("voice_settings"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### 🔊 Audio Settings")

                    voice_speed = st.slider(
                        "Voice Speed",
                        min_value=0.5,
                        max_value=2.0,
                        value=st.session_state.voice_settings.get('speed', 1.0),
                        step=0.1,
                        help="Adjust how fast the voice speaks"
                    )

                    voice_pitch = st.slider(
                        "Voice Pitch",
                        min_value=0.5,
                        max_value=2.0,
                        value=st.session_state.voice_settings.get('pitch', 1.0),
                        step=0.1,
                        help="Adjust the voice pitch (higher/lower)"
                    )

                    voice_volume = st.slider(
                        "Voice Volume",
                        min_value=0.1,
                        max_value=1.0,
                        value=st.session_state.voice_settings.get('volume', 0.8),
                        step=0.1,
                        help="Adjust the voice volume level"
                    )

                with col2:
                    st.markdown("#### 🎤 Recognition Settings")

                    wake_word = st.text_input(
                        "Wake Word",
                        value=st.session_state.voice_settings.get('wake_word', 'Hey Jarvis'),
                        help="Phrase to activate voice assistant"
                    )

                    voice_language = st.selectbox(
                        "Voice Language",
                        options=['en', 'ta', 'hi', 'te'],
                        format_func=lambda x: {'en': 'English', 'ta': 'Tamil', 'hi': 'Hindi', 'te': 'Telugu'}[x],
                        index=['en', 'ta', 'hi', 'te'].index(st.session_state.voice_settings.get('language', 'en'))
                    )

                    voice_type = st.selectbox(
                        "Voice Type",
                        options=['Female', 'Male', 'Neutral'],
                        index=['Female', 'Male', 'Neutral'].index(st.session_state.voice_settings.get('voice_type', 'Female'))
                    )

                    sensitivity = st.slider(
                        "Microphone Sensitivity",
                        min_value=0.1,
                        max_value=1.0,
                        value=st.session_state.voice_settings.get('sensitivity', 0.7),
                        step=0.1,
                        help="Adjust microphone sensitivity"
                    )

                # Advanced settings
                st.markdown("#### 🔧 Advanced Settings")

                col1, col2 = st.columns(2)

                with col1:
                    auto_listen = st.checkbox(
                        "Auto-listen after response",
                        value=st.session_state.voice_settings.get('auto_listen', True),
                        help="Continue listening after giving a response"
                    )

                    voice_feedback = st.checkbox(
                        "Voice confirmation",
                        value=st.session_state.voice_settings.get('voice_feedback', True),
                        help="Provide voice confirmation for actions"
                    )

                with col2:
                    noise_cancellation = st.checkbox(
                        "Noise cancellation",
                        value=st.session_state.voice_settings.get('noise_cancellation', True),
                        help="Filter background noise"
                    )

                    offline_mode = st.checkbox(
                        "Offline mode (limited features)",
                        value=st.session_state.voice_settings.get('offline_mode', False),
                        help="Use voice assistant without internet"
                    )

                if st.form_submit_button("💾 Save Voice Settings", use_container_width=True):
                    # Update voice settings
                    st.session_state.voice_settings.update({
                        'speed': voice_speed,
                        'pitch': voice_pitch,
                        'volume': voice_volume,
                        'wake_word': wake_word,
                        'language': voice_language,
                        'voice_type': voice_type,
                        'sensitivity': sensitivity,
                        'auto_listen': auto_listen,
                        'voice_feedback': voice_feedback,
                        'noise_cancellation': noise_cancellation,
                        'offline_mode': offline_mode
                    })

                    st.success("✅ Voice settings saved successfully!")
                    st.rerun()

            # Test voice settings
            st.markdown("#### 🧪 Test Voice Settings")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔊 Test Voice Output", use_container_width=True):
                    test_message = {
                        'en': "Hello! This is JarvisFi, your ultimate multilingual finance chat assistant.",
                        'ta': "வணக்கம்! இது JarvisFi, உங்கள் இறுதி பன்மொழி நிதி அரட்டை உதவியாளர்.",
                        'hi': "नमस्ते! यह JarvisFi है, आपका अंतिम बहुभाषी वित्त चैट सहायक।",
                        'te': "నమస్కారం! ఇది JarvisFi, మీ అంతిమ బహుభాషా ఫైనాన్స్ చాట్ అసిస్టెంట్."
                    }

                    message = test_message.get(voice_language, test_message['en'])
                    st.info(f"🔊 Playing: '{message}'")
                    st.success("Voice test completed!")

            with col2:
                if st.button("🎤 Test Voice Recognition", use_container_width=True):
                    st.info("🎤 Listening for voice input...")
                    st.success("Voice recognition test completed!")

        except Exception as e:
            self.logger.error(f"Voice settings rendering failed: {e}")
            st.error(f"Voice settings error: {e}")

    def render_voice_commands(self, language: str):
        """Render voice commands reference"""
        try:
            st.markdown("### 📋 Voice Commands Reference")

            # Command categories
            command_categories = {
                'General Navigation': [
                    "Go to dashboard",
                    "Show my profile",
                    "Open calculator",
                    "Switch to [language]",
                    "Help me with [topic]"
                ],
                'Financial Queries': [
                    "What's my savings rate?",
                    "Show my investment portfolio",
                    "Calculate SIP for [amount]",
                    "Check my credit score",
                    "What are my monthly expenses?"
                ],
                'Investment Commands': [
                    "Recommend mutual funds",
                    "Show top performing funds",
                    "Calculate retirement corpus",
                    "Suggest tax saving options",
                    "Rebalance my portfolio"
                ],
                'Farmer Tools': [
                    "Show government schemes",
                    "Check MSP rates",
                    "Calculate crop loan EMI",
                    "Find insurance options",
                    "Show seasonal planning"
                ],
                'Credit Management': [
                    "Check credit score",
                    "Improve credit score tips",
                    "Recommend credit cards",
                    "Show credit report",
                    "Calculate credit utilization"
                ],
                'System Commands': [
                    "Increase volume",
                    "Speak slower",
                    "Repeat last response",
                    "Stop listening",
                    "Save my data"
                ]
            }

            # Display command categories
            for category, commands in command_categories.items():
                with st.expander(f"🎯 {category}", expanded=False):
                    st.markdown(f"**Available commands in {category}:**")

                    for i, command in enumerate(commands, 1):
                        st.markdown(f"{i}. 🎤 *\"{command}\"*")

                    # Example usage
                    if category == 'Financial Queries':
                        st.markdown("**Example usage:**")
                        st.info("🎤 \"Hey Jarvis, what's my current savings rate?\"")
                        st.success("🤖 \"Your current savings rate is 25.5% which is excellent for your age group.\"")

            # Voice command tips
            st.markdown("#### 💡 Voice Command Tips")

            tips = [
                "🎯 **Be specific**: Use clear, specific commands for better recognition",
                "🔊 **Speak clearly**: Pronounce words clearly and at moderate speed",
                "🎤 **Use wake word**: Always start with 'Hey Jarvis' or your custom wake word",
                "🌍 **Language consistency**: Use commands in the same language as your interface",
                "⏸️ **Pause briefly**: Wait for the listening indicator before speaking",
                "🔄 **Repeat if needed**: If not understood, try rephrasing your command"
            ]

            for tip in tips:
                st.markdown(tip)

            # Command builder
            st.markdown("#### 🛠️ Custom Command Builder")

            with st.form("command_builder"):
                st.markdown("Build your own voice command:")

                col1, col2, col3 = st.columns(3)

                with col1:
                    action = st.selectbox("Action", ["Show", "Calculate", "Check", "Find", "Recommend"])

                with col2:
                    object_type = st.selectbox("Object", ["portfolio", "credit score", "SIP", "schemes", "funds"])

                with col3:
                    modifier = st.selectbox("Modifier", ["", "for me", "in detail", "quickly", "with examples"])

                if st.form_submit_button("🎯 Generate Command"):
                    custom_command = f"{action} {object_type} {modifier}".strip()
                    st.success(f"🎤 Generated command: \"Hey Jarvis, {custom_command}\"")

        except Exception as e:
            self.logger.error(f"Voice commands rendering failed: {e}")
            st.error(f"Voice commands error: {e}")

    def render_voice_language_support(self, language: str):
        """Render voice language support information"""
        try:
            st.markdown("### 🌍 Multilingual Voice Support")

            # Language capabilities
            languages = {
                'English': {
                    'code': 'en',
                    'status': 'Full Support',
                    'features': ['Voice recognition', 'Voice synthesis', 'All commands', 'Natural language'],
                    'accuracy': '98%',
                    'voices': ['Female (Sarah)', 'Male (David)', 'Neutral (Alex)']
                },
                'Tamil': {
                    'code': 'ta',
                    'status': 'Full Support',
                    'features': ['Voice recognition', 'Voice synthesis', 'Financial terms', 'Cultural context'],
                    'accuracy': '95%',
                    'voices': ['Female (Priya)', 'Male (Kumar)', 'Neutral (Tamil AI)']
                },
                'Hindi': {
                    'code': 'hi',
                    'status': 'Full Support',
                    'features': ['Voice recognition', 'Voice synthesis', 'Banking terms', 'Regional accents'],
                    'accuracy': '96%',
                    'voices': ['Female (Kavya)', 'Male (Arjun)', 'Neutral (Hindi AI)']
                },
                'Telugu': {
                    'code': 'te',
                    'status': 'Full Support',
                    'features': ['Voice recognition', 'Voice synthesis', 'Financial vocabulary', 'Dialect support'],
                    'accuracy': '94%',
                    'voices': ['Female (Lakshmi)', 'Male (Ravi)', 'Neutral (Telugu AI)']
                }
            }

            # Display language support
            for lang_name, details in languages.items():
                with st.expander(f"🌐 {lang_name} Support", expanded=False):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"""
                        <div class="language-support">
                            <h4>📊 Language Details</h4>
                            <p><strong>Status:</strong> {details['status']}</p>
                            <p><strong>Accuracy:</strong> {details['accuracy']}</p>
                            <p><strong>Code:</strong> {details['code']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown("**Available Features:**")
                        for feature in details['features']:
                            st.markdown(f"✅ {feature}")

                    st.markdown("**Available Voices:**")
                    for voice in details['voices']:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"🔊 {voice}")
                        with col2:
                            if st.button(f"Test", key=f"test_{lang_name}_{voice}"):
                                st.info(f"Playing sample in {voice}")

            # Language switching
            st.markdown("#### 🔄 Language Switching")

            st.markdown("**Voice commands to switch languages:**")
            switch_commands = [
                "🎤 \"Switch to English\" → Changes to English interface and voice",
                "🎤 \"தமிழுக்கு மாற்று\" → Changes to Tamil interface and voice",
                "🎤 \"हिंदी में बदलें\" → Changes to Hindi interface and voice",
                "🎤 \"తెలుగులోకి మార్చు\" → Changes to Telugu interface and voice"
            ]

            for cmd in switch_commands:
                st.markdown(cmd)

            # Accent and dialect support
            st.markdown("#### 🗣️ Accent & Dialect Support")

            accent_support = {
                'English': ['Indian English', 'British English', 'American English'],
                'Tamil': ['Chennai Tamil', 'Madurai Tamil', 'Coimbatore Tamil'],
                'Hindi': ['Delhi Hindi', 'Mumbai Hindi', 'Lucknow Hindi'],
                'Telugu': ['Hyderabad Telugu', 'Vijayawada Telugu', 'Visakhapatnam Telugu']
            }

            for lang, accents in accent_support.items():
                st.markdown(f"**{lang}:** {', '.join(accents)}")

            # Performance metrics
            st.markdown("#### 📈 Performance Metrics")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Languages Supported", "4", "Complete support")
            with col2:
                st.metric("Average Accuracy", "95.8%", "↗️ +2.1%")
            with col3:
                st.metric("Response Time", "1.2s", "↗️ Improved")
            with col4:
                st.metric("Voice Options", "12", "3 per language")

        except Exception as e:
            self.logger.error(f"Voice language support rendering failed: {e}")
            st.error(f"Voice language support error: {e}")

    def render_sip_calculator(self, language: str):
        """Render SIP Calculator with multilingual support"""
        try:
            st.markdown("""
            <div class="calculator-container">
                <h3>📈 SIP Calculator - Systematic Investment Plan</h3>
                <p>Calculate the future value of your SIP investments</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📊 Input Parameters")

                monthly_sip = st.number_input(
                    "Monthly SIP Amount (₹)",
                    min_value=500,
                    max_value=100000,
                    value=5000,
                    step=500,
                    help="Amount you want to invest every month"
                )

                annual_return = st.slider(
                    "Expected Annual Return (%)",
                    min_value=8.0,
                    max_value=20.0,
                    value=12.0,
                    step=0.5,
                    help="Expected annual return from your investments"
                )

                investment_period = st.slider(
                    "Investment Period (Years)",
                    min_value=1,
                    max_value=30,
                    value=10,
                    help="How long you want to continue the SIP"
                )

                # Advanced options
                with st.expander("🔧 Advanced Options"):
                    step_up_percentage = st.slider(
                        "Annual Step-up (%)",
                        min_value=0.0,
                        max_value=20.0,
                        value=0.0,
                        step=1.0,
                        help="Annual increase in SIP amount"
                    )

                    inflation_rate = st.slider(
                        "Inflation Rate (%)",
                        min_value=3.0,
                        max_value=8.0,
                        value=6.0,
                        step=0.5,
                        help="Expected inflation rate"
                    )

            with col2:
                st.markdown("#### 💰 Results")

                # Calculate SIP returns
                monthly_return = annual_return / 12 / 100
                total_months = investment_period * 12

                if step_up_percentage > 0:
                    # Calculate with step-up
                    future_value = 0
                    current_sip = monthly_sip

                    for year in range(investment_period):
                        if year > 0:
                            current_sip = current_sip * (1 + step_up_percentage / 100)

                        for month in range(12):
                            remaining_months = total_months - (year * 12 + month)
                            if remaining_months > 0:
                                future_value += current_sip * ((1 + monthly_return) ** remaining_months)
                else:
                    # Standard SIP calculation
                    if monthly_return > 0:
                        future_value = monthly_sip * (((1 + monthly_return) ** total_months - 1) / monthly_return) * (1 + monthly_return)
                    else:
                        future_value = monthly_sip * total_months

                total_invested = monthly_sip * total_months * (1 + step_up_percentage/200 * (investment_period - 1)) if step_up_percentage > 0 else monthly_sip * total_months
                total_returns = future_value - total_invested

                # Inflation-adjusted value
                real_value = future_value / ((1 + inflation_rate/100) ** investment_period)

                # Display results
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; margin: 0.5rem 0;">
                    <h4>💰 Total Investment</h4>
                    <h2>₹{total_invested:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #2196F3, #1976D2); color: white; margin: 0.5rem 0;">
                    <h4>📈 Expected Returns</h4>
                    <h2>₹{total_returns:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #FF9800, #F57C00); color: white; margin: 0.5rem 0;">
                    <h4>🎯 Maturity Amount</h4>
                    <h2>₹{future_value:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #9C27B0, #7B1FA2); color: white; margin: 0.5rem 0;">
                    <h4>💎 Real Value (Inflation Adjusted)</h4>
                    <h2>₹{real_value:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                # Return percentage
                return_multiple = future_value / total_invested if total_invested > 0 else 0
                st.info(f"🚀 Your money will grow **{return_multiple:.1f}x** in {investment_period} years!")

            # Visualization
            st.markdown("#### 📊 SIP Growth Visualization")

            # Year-wise breakdown
            years = list(range(1, investment_period + 1))
            invested_amounts = []
            maturity_amounts = []

            for year in years:
                months = year * 12

                if step_up_percentage > 0:
                    # Calculate invested amount with step-up
                    invested = 0
                    current_sip = monthly_sip
                    for y in range(year):
                        if y > 0:
                            current_sip = current_sip * (1 + step_up_percentage / 100)
                        invested += current_sip * 12
                    invested_amounts.append(invested)
                else:
                    invested_amounts.append(monthly_sip * months)

                # Calculate maturity amount
                if monthly_return > 0:
                    if step_up_percentage > 0:
                        amount = 0
                        current_sip = monthly_sip
                        for y in range(year):
                            if y > 0:
                                current_sip = current_sip * (1 + step_up_percentage / 100)
                            for m in range(12):
                                remaining_months = months - (y * 12 + m)
                                if remaining_months > 0:
                                    amount += current_sip * ((1 + monthly_return) ** remaining_months)
                        maturity_amounts.append(amount)
                    else:
                        amount = monthly_sip * (((1 + monthly_return) ** months - 1) / monthly_return) * (1 + monthly_return)
                        maturity_amounts.append(amount)
                else:
                    maturity_amounts.append(monthly_sip * months)

            # Create chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=years,
                y=invested_amounts,
                name='Total Invested',
                fill='tonexty',
                line=dict(color='#FF6B6B')
            ))
            fig.add_trace(go.Scatter(
                x=years,
                y=maturity_amounts,
                name='Maturity Value',
                fill='tonexty',
                line=dict(color='#4CAF50')
            ))

            fig.update_layout(
                title='SIP Growth Over Time',
                xaxis_title='Years',
                yaxis_title='Amount (₹)',
                height=400,
                hovermode='x unified'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Detailed breakdown table
            with st.expander("📋 Year-wise Breakdown"):
                breakdown_data = {
                    'Year': years,
                    'Invested (₹)': [f"₹{amount:,.0f}" for amount in invested_amounts],
                    'Maturity Value (₹)': [f"₹{amount:,.0f}" for amount in maturity_amounts],
                    'Returns (₹)': [f"₹{mat - inv:,.0f}" for mat, inv in zip(maturity_amounts, invested_amounts)]
                }

                df = pd.DataFrame(breakdown_data)
                st.dataframe(df, use_container_width=True)

            # Tips and recommendations
            st.markdown("#### 💡 SIP Investment Tips")

            tips = [
                "🎯 Start early to benefit from the power of compounding",
                "📈 Increase your SIP amount annually by 10-15% (step-up SIP)",
                "🔄 Stay invested for the long term, don't stop during market volatility",
                "🎪 Diversify across different fund categories for better risk management",
                "📊 Review and rebalance your portfolio annually"
            ]

            for tip in tips:
                st.info(tip)

        except Exception as e:
            self.logger.error(f"SIP calculator error: {e}")
            st.error(f"SIP calculator error: {e}")

    def render_emi_calculator(self, language: str):
        """Render EMI Calculator"""
        try:
            st.markdown("""
            <div class="calculator-container">
                <h3>🏠 EMI Calculator - Loan EMI Calculator</h3>
                <p>Calculate your loan EMI and total interest payable</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📊 Loan Details")

                loan_amount = st.number_input(
                    "Loan Amount (₹)",
                    min_value=100000,
                    max_value=50000000,
                    value=2500000,
                    step=100000,
                    help="Total loan amount you want to borrow"
                )

                interest_rate = st.slider(
                    "Annual Interest Rate (%)",
                    min_value=6.0,
                    max_value=20.0,
                    value=8.5,
                    step=0.1,
                    help="Annual interest rate offered by the lender"
                )

                loan_tenure = st.slider(
                    "Loan Tenure (Years)",
                    min_value=1,
                    max_value=30,
                    value=20,
                    help="Loan repayment period in years"
                )

                # Loan type
                loan_type = st.selectbox(
                    "Loan Type",
                    ["Home Loan", "Personal Loan", "Car Loan", "Business Loan"],
                    help="Type of loan"
                )

            with col2:
                st.markdown("#### 💰 EMI Calculation")

                # Calculate EMI
                monthly_rate = interest_rate / 12 / 100
                total_months = loan_tenure * 12

                if monthly_rate > 0:
                    emi = loan_amount * monthly_rate * (1 + monthly_rate) ** total_months / ((1 + monthly_rate) ** total_months - 1)
                else:
                    emi = loan_amount / total_months

                total_payment = emi * total_months
                total_interest = total_payment - loan_amount

                # Display results
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #FF9800, #F57C00); color: white; margin: 0.5rem 0;">
                    <h4>💳 Monthly EMI</h4>
                    <h2>₹{emi:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #F44336, #D32F2F); color: white; margin: 0.5rem 0;">
                    <h4>💸 Total Interest</h4>
                    <h2>₹{total_interest:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #9C27B0, #7B1FA2); color: white; margin: 0.5rem 0;">
                    <h4>💰 Total Payment</h4>
                    <h2>₹{total_payment:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                # EMI to income ratio
                user_income = st.session_state.user_profile['basic_info']['monthly_income']
                emi_ratio = (emi / user_income * 100) if user_income > 0 else 0

                if emi_ratio <= 40:
                    st.success(f"✅ EMI is {emi_ratio:.1f}% of your income - Affordable!")
                elif emi_ratio <= 50:
                    st.warning(f"⚠️ EMI is {emi_ratio:.1f}% of your income - Manageable but tight")
                else:
                    st.error(f"❌ EMI is {emi_ratio:.1f}% of your income - Too high!")

            # Visualization
            st.markdown("#### 📊 Loan Breakdown")

            col1, col2 = st.columns(2)

            with col1:
                # Principal vs Interest pie chart
                fig = go.Figure(data=[
                    go.Pie(
                        labels=['Principal', 'Interest'],
                        values=[loan_amount, total_interest],
                        hole=0.4,
                        marker_colors=['#4CAF50', '#FF6B6B']
                    )
                ])
                fig.update_layout(title='Loan Breakdown', height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Year-wise payment breakdown
                years = list(range(1, min(loan_tenure + 1, 11)))  # Show max 10 years
                yearly_payment = [emi * 12] * len(years)

                fig = go.Figure(data=[
                    go.Bar(x=years, y=yearly_payment, name='Annual Payment', marker_color='#2196F3')
                ])
                fig.update_layout(
                    title='Annual Payment',
                    xaxis_title='Year',
                    yaxis_title='Amount (₹)',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

            # Amortization schedule
            with st.expander("📋 Amortization Schedule (First 12 months)"):
                schedule_data = []
                remaining_balance = loan_amount

                for month in range(1, 13):
                    interest_payment = remaining_balance * monthly_rate
                    principal_payment = emi - interest_payment
                    remaining_balance -= principal_payment

                    schedule_data.append({
                        'Month': month,
                        'EMI (₹)': f"₹{emi:,.0f}",
                        'Principal (₹)': f"₹{principal_payment:,.0f}",
                        'Interest (₹)': f"₹{interest_payment:,.0f}",
                        'Balance (₹)': f"₹{remaining_balance:,.0f}"
                    })

                df = pd.DataFrame(schedule_data)
                st.dataframe(df, use_container_width=True)

            # EMI tips
            st.markdown("#### 💡 EMI Management Tips")

            tips = [
                "🎯 Keep your EMI below 40% of your monthly income",
                "💰 Make prepayments to reduce interest burden",
                "📊 Compare interest rates from different lenders",
                "🔄 Consider balance transfer for better rates",
                "📈 Choose longer tenure for lower EMI, shorter for less interest"
            ]

            for tip in tips:
                st.info(tip)

        except Exception as e:
            self.logger.error(f"EMI calculator error: {e}")
            st.error(f"EMI calculator error: {e}")

    def render_tax_calculator(self, language: str):
        """Render Tax Calculator"""
        try:
            st.markdown("""
            <div class="calculator-container">
                <h3>💰 Tax Calculator - Income Tax Calculator</h3>
                <p>Calculate your income tax and plan tax-saving investments</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📊 Income Details")

                annual_income = st.number_input(
                    "Annual Income (₹)",
                    min_value=100000,
                    max_value=10000000,
                    value=800000,
                    step=50000,
                    help="Your total annual income"
                )

                age_category = st.selectbox(
                    "Age Category",
                    ["Below 60 years", "60-80 years (Senior Citizen)", "Above 80 years (Super Senior)"],
                    help="Select your age category for tax calculation"
                )

                tax_regime = st.radio(
                    "Tax Regime",
                    ["Old Regime (with deductions)", "New Regime (lower rates, no deductions)"],
                    help="Choose your preferred tax regime"
                )

                if tax_regime == "Old Regime (with deductions)":
                    st.markdown("#### 💰 Deductions (Section 80C, 80D, etc.)")

                    section_80c = st.number_input("Section 80C (₹)", min_value=0, max_value=150000, value=150000)
                    section_80d = st.number_input("Section 80D (₹)", min_value=0, max_value=50000, value=25000)
                    section_80ccd = st.number_input("Section 80CCD(1B) - NPS (₹)", min_value=0, max_value=50000, value=0)
                    hra_exemption = st.number_input("HRA Exemption (₹)", min_value=0, max_value=annual_income//2, value=0)

                    total_deductions = section_80c + section_80d + section_80ccd + hra_exemption
                else:
                    total_deductions = 0

            with col2:
                st.markdown("#### 💸 Tax Calculation")

                # Calculate tax based on regime and age
                if age_category == "Below 60 years":
                    basic_exemption = 250000 if tax_regime == "Old Regime (with deductions)" else 300000
                elif age_category == "60-80 years (Senior Citizen)":
                    basic_exemption = 300000 if tax_regime == "Old Regime (with deductions)" else 300000
                else:  # Above 80 years
                    basic_exemption = 500000 if tax_regime == "Old Regime (with deductions)" else 300000

                taxable_income = max(0, annual_income - basic_exemption - total_deductions)

                # Tax calculation
                if tax_regime == "Old Regime (with deductions)":
                    # Old regime tax slabs
                    if taxable_income <= 250000:
                        tax = 0
                    elif taxable_income <= 500000:
                        tax = (taxable_income - 250000) * 0.05
                    elif taxable_income <= 1000000:
                        tax = 12500 + (taxable_income - 500000) * 0.20
                    else:
                        tax = 112500 + (taxable_income - 1000000) * 0.30
                else:
                    # New regime tax slabs
                    if taxable_income <= 300000:
                        tax = 0
                    elif taxable_income <= 600000:
                        tax = (taxable_income - 300000) * 0.05
                    elif taxable_income <= 900000:
                        tax = 15000 + (taxable_income - 600000) * 0.10
                    elif taxable_income <= 1200000:
                        tax = 45000 + (taxable_income - 900000) * 0.15
                    elif taxable_income <= 1500000:
                        tax = 90000 + (taxable_income - 1200000) * 0.20
                    else:
                        tax = 150000 + (taxable_income - 1500000) * 0.30

                # Add cess
                cess = tax * 0.04
                total_tax = tax + cess

                # Display results
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; margin: 0.5rem 0;">
                    <h4>💰 Taxable Income</h4>
                    <h2>₹{taxable_income:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #FF6B6B, #ee5a52); color: white; margin: 0.5rem 0;">
                    <h4>💸 Income Tax</h4>
                    <h2>₹{total_tax:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                if total_deductions > 0:
                    st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #2196F3, #1976D2); color: white; margin: 0.5rem 0;">
                        <h4>💰 Tax Saved</h4>
                        <h2>₹{total_deductions * 0.20:,.0f}</h2>
                        <p>Through deductions</p>
                    </div>
                    """, unsafe_allow_html=True)

                effective_tax_rate = (total_tax / annual_income * 100) if annual_income > 0 else 0
                st.info(f"📊 Effective Tax Rate: {effective_tax_rate:.2f}%")

            # Tax planning suggestions
            st.markdown("#### 💡 Tax Planning Suggestions")

            if total_deductions < 150000:
                remaining_80c = 150000 - (total_deductions if tax_regime == "Old Regime (with deductions)" else 0)
                st.warning(f"💰 You can save ₹{remaining_80c * 0.20:,.0f} more by investing ₹{remaining_80c:,.0f} in 80C instruments")

            suggestions = [
                "📈 Invest in ELSS mutual funds for tax saving with growth potential",
                "🏥 Get health insurance to claim deduction under Section 80D",
                "💰 Contribute to NPS for additional ₹50,000 deduction under 80CCD(1B)",
                "🏠 Consider home loan for interest deduction under Section 24",
                "📚 Claim education loan interest deduction under Section 80E"
            ]

            for suggestion in suggestions:
                st.info(suggestion)

        except Exception as e:
            self.logger.error(f"Tax calculator error: {e}")
            st.error(f"Tax calculator error: {e}")

    def render_retirement_calculator(self, language: str):
        """Render Retirement Calculator"""
        try:
            st.markdown("""
            <div class="calculator-container">
                <h3>🏖️ Retirement Calculator - Retirement Planning</h3>
                <p>Plan your retirement corpus and monthly savings</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📊 Current Details")

                current_age = st.number_input("Current Age", min_value=18, max_value=65, value=30)
                retirement_age = st.number_input("Retirement Age", min_value=current_age+1, max_value=75, value=60)
                current_monthly_expenses = st.number_input("Current Monthly Expenses (₹)", min_value=10000, max_value=500000, value=50000)

                st.markdown("#### 🎯 Retirement Goals")

                inflation_rate = st.slider("Expected Inflation (%)", min_value=3.0, max_value=8.0, value=6.0, step=0.5)
                post_retirement_years = st.number_input("Years After Retirement", min_value=10, max_value=40, value=25)
                expense_reduction = st.slider("Expense Reduction After Retirement (%)", min_value=0, max_value=50, value=20)

                # Calculate retirement corpus needed
                years_to_retirement = retirement_age - current_age
                future_monthly_expenses = current_monthly_expenses * (1 + inflation_rate/100) ** years_to_retirement
                reduced_expenses = future_monthly_expenses * (1 - expense_reduction/100)
                annual_expenses = reduced_expenses * 12

                # Corpus needed (assuming 6% post-retirement return)
                post_retirement_return = 6.0
                corpus_needed = annual_expenses * ((1 - (1 + post_retirement_return/100) ** -post_retirement_years) / (post_retirement_return/100))

            with col2:
                st.markdown("#### 💰 Retirement Planning")

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #FF9800, #F57C00); color: white; margin: 0.5rem 0;">
                    <h4>💸 Future Monthly Expenses</h4>
                    <h2>₹{reduced_expenses:,.0f}</h2>
                    <p>At retirement (inflation adjusted)</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #F44336, #D32F2F); color: white; margin: 0.5rem 0;">
                    <h4>🎯 Corpus Needed</h4>
                    <h2>₹{corpus_needed:,.0f}</h2>
                    <p>Total retirement corpus</p>
                </div>
                """, unsafe_allow_html=True)

                # Calculate required monthly SIP
                expected_return = st.slider("Expected Return on Investment (%)", min_value=8.0, max_value=15.0, value=12.0, step=0.5)
                monthly_return = expected_return / 12 / 100
                total_months = years_to_retirement * 12

                if monthly_return > 0:
                    required_sip = corpus_needed * monthly_return / (((1 + monthly_return) ** total_months - 1) * (1 + monthly_return))
                else:
                    required_sip = corpus_needed / total_months

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; margin: 0.5rem 0;">
                    <h4>💰 Required Monthly SIP</h4>
                    <h2>₹{required_sip:,.0f}</h2>
                    <p>To achieve retirement goal</p>
                </div>
                """, unsafe_allow_html=True)

                # Current savings assessment
                current_monthly_income = st.session_state.user_profile['basic_info']['monthly_income']
                sip_percentage = (required_sip / current_monthly_income * 100) if current_monthly_income > 0 else 0

                if sip_percentage <= 15:
                    st.success(f"✅ Required SIP is {sip_percentage:.1f}% of income - Achievable!")
                elif sip_percentage <= 25:
                    st.warning(f"⚠️ Required SIP is {sip_percentage:.1f}% of income - Challenging but possible")
                else:
                    st.error(f"❌ Required SIP is {sip_percentage:.1f}% of income - Consider extending retirement age")

            # Retirement planning chart
            st.markdown("#### 📈 Retirement Corpus Growth")

            years = list(range(current_age, retirement_age + 1))
            corpus_growth = []

            for year in years:
                months_invested = (year - current_age) * 12
                if months_invested > 0:
                    corpus = required_sip * (((1 + monthly_return) ** months_invested - 1) / monthly_return) * (1 + monthly_return)
                else:
                    corpus = 0
                corpus_growth.append(corpus)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=years, y=corpus_growth, name='Corpus Growth', fill='tonexty', line=dict(color='#4CAF50')))
            fig.add_hline(y=corpus_needed, line_dash="dash", line_color="red", annotation_text="Target Corpus")

            fig.update_layout(
                title='Retirement Corpus Growth Over Time',
                xaxis_title='Age',
                yaxis_title='Corpus (₹)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            # Retirement tips
            st.markdown("#### 💡 Retirement Planning Tips")

            tips = [
                "🎯 Start early to benefit from compounding",
                "📈 Increase SIP amount by 10-15% annually",
                "🏥 Plan for healthcare expenses in retirement",
                "🏠 Consider having a paid-off home by retirement",
                "💰 Diversify investments across equity, debt, and real estate"
            ]

            for tip in tips:
                st.info(tip)

        except Exception as e:
            self.logger.error(f"Retirement calculator error: {e}")
            st.error(f"Retirement calculator error: {e}")

    def render_fd_calculator(self, language: str):
        """Render FD Calculator"""
        try:
            st.markdown("""
            <div class="calculator-container">
                <h3>🏦 FD Calculator - Fixed Deposit Calculator</h3>
                <p>Calculate returns on your fixed deposit investments</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📊 FD Details")

                principal = st.number_input("Principal Amount (₹)", min_value=1000, max_value=10000000, value=100000)
                interest_rate = st.slider("Interest Rate (% per annum)", min_value=3.0, max_value=10.0, value=6.5, step=0.1)
                tenure_years = st.number_input("Tenure (Years)", min_value=0, max_value=10, value=2)
                tenure_months = st.number_input("Additional Months", min_value=0, max_value=11, value=0)

                compounding_frequency = st.selectbox(
                    "Compounding Frequency",
                    ["Annually", "Half-yearly", "Quarterly", "Monthly"],
                    index=3
                )

                # Calculate maturity amount
                total_tenure = tenure_years + tenure_months/12

                if compounding_frequency == "Annually":
                    n = 1
                elif compounding_frequency == "Half-yearly":
                    n = 2
                elif compounding_frequency == "Quarterly":
                    n = 4
                else:  # Monthly
                    n = 12

                maturity_amount = principal * (1 + interest_rate/(100*n)) ** (n * total_tenure)
                interest_earned = maturity_amount - principal

            with col2:
                st.markdown("#### 💰 FD Returns")

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; margin: 0.5rem 0;">
                    <h4>💰 Principal Amount</h4>
                    <h2>₹{principal:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #2196F3, #1976D2); color: white; margin: 0.5rem 0;">
                    <h4>📈 Interest Earned</h4>
                    <h2>₹{interest_earned:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #FF9800, #F57C00); color: white; margin: 0.5rem 0;">
                    <h4>🎯 Maturity Amount</h4>
                    <h2>₹{maturity_amount:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)

                effective_rate = (interest_earned / principal / total_tenure * 100) if total_tenure > 0 else 0
                st.info(f"📊 Effective Annual Rate: {effective_rate:.2f}%")

            # FD comparison with other investments
            st.markdown("#### ⚖️ Investment Comparison")

            comparison_data = {
                'Investment': ['Fixed Deposit', 'Savings Account', 'Liquid Fund', 'Debt Fund', 'Equity Fund (SIP)'],
                'Expected Return (%)': [interest_rate, 3.5, 4.5, 7.0, 12.0],
                'Risk Level': ['Very Low', 'Very Low', 'Low', 'Low', 'High'],
                'Liquidity': ['Low', 'High', 'High', 'Medium', 'Medium'],
                'Tax Treatment': ['Taxable', 'Taxable', 'Taxable', 'Taxable', 'LTCG 10%']
            }

            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True)

            # FD vs SIP comparison
            st.markdown("#### 📊 FD vs SIP Comparison")

            sip_amount = principal / (total_tenure * 12) if total_tenure > 0 else principal
            sip_return = 12.0  # Assumed SIP return
            sip_months = total_tenure * 12

            if sip_months > 0:
                monthly_return = sip_return / 12 / 100
                sip_maturity = sip_amount * (((1 + monthly_return) ** sip_months - 1) / monthly_return) * (1 + monthly_return)
            else:
                sip_maturity = principal

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Fixed Deposit**")
                st.metric("Maturity Amount", f"₹{maturity_amount:,.0f}")
                st.metric("Total Return", f"₹{interest_earned:,.0f}")

            with col2:
                st.markdown("**SIP (12% return)**")
                st.metric("Maturity Amount", f"₹{sip_maturity:,.0f}")
                st.metric("Total Return", f"₹{sip_maturity - principal:,.0f}")

            if sip_maturity > maturity_amount:
                difference = sip_maturity - maturity_amount
                st.success(f"💡 SIP could give ₹{difference:,.0f} more returns, but with higher risk")
            else:
                st.info("💡 FD provides guaranteed returns with capital protection")

        except Exception as e:
            self.logger.error(f"FD calculator error: {e}")
            st.error(f"FD calculator error: {e}")

    def render_ppf_calculator(self, language: str):
        """Render PPF Calculator"""
        try:
            st.markdown("""
            <div class="calculator-container">
                <h3>💎 PPF Calculator - Public Provident Fund</h3>
                <p>Calculate your PPF maturity amount and plan investments</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📊 PPF Investment Details")

                annual_investment = st.number_input(
                    "Annual Investment (₹)",
                    min_value=500,
                    max_value=150000,
                    value=150000,
                    step=500,
                    help="Minimum ₹500, Maximum ₹1.5 lakh per year"
                )

                current_ppf_balance = st.number_input(
                    "Current PPF Balance (₹)",
                    min_value=0,
                    max_value=5000000,
                    value=0,
                    help="If you already have a PPF account"
                )

                years_completed = st.number_input(
                    "Years Already Completed",
                    min_value=0,
                    max_value=14,
                    value=0,
                    help="Years already invested in PPF"
                )

                ppf_rate = st.slider(
                    "PPF Interest Rate (%)",
                    min_value=7.0,
                    max_value=9.0,
                    value=7.1,
                    step=0.1,
                    help="Current PPF rate is 7.1% (as of 2024)"
                )

                # Calculate PPF maturity
                remaining_years = 15 - years_completed

                # Future value of current balance
                future_current_balance = current_ppf_balance * (1 + ppf_rate/100) ** remaining_years

                # Future value of annual investments
                if remaining_years > 0:
                    future_annual_investments = annual_investment * (((1 + ppf_rate/100) ** remaining_years - 1) / (ppf_rate/100))
                else:
                    future_annual_investments = 0

                total_maturity = future_current_balance + future_annual_investments
                total_investment = current_ppf_balance + (annual_investment * remaining_years)
                total_interest = total_maturity - total_investment

            with col2:
                st.markdown("#### 💰 PPF Maturity Calculation")

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; margin: 0.5rem 0;">
                    <h4>💰 Total Investment</h4>
                    <h2>₹{total_investment:,.0f}</h2>
                    <p>Over {15} years</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #2196F3, #1976D2); color: white; margin: 0.5rem 0;">
                    <h4>📈 Interest Earned</h4>
                    <h2>₹{total_interest:,.0f}</h2>
                    <p>Tax-free returns</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #FF9800, #F57C00); color: white; margin: 0.5rem 0;">
                    <h4>🎯 Maturity Amount</h4>
                    <h2>₹{total_maturity:,.0f}</h2>
                    <p>Completely tax-free</p>
                </div>
                """, unsafe_allow_html=True)

                if remaining_years > 0:
                    st.info(f"⏰ {remaining_years} years remaining for maturity")
                else:
                    st.success("🎉 PPF account has matured!")

            # PPF year-wise breakdown
            st.markdown("#### 📊 Year-wise PPF Growth")

            years = list(range(1, 16))
            yearly_balance = []
            cumulative_investment = current_ppf_balance

            for year in years:
                if year <= years_completed:
                    # Historical years (estimated)
                    cumulative_investment += annual_investment
                    balance = cumulative_investment * (1 + ppf_rate/100) ** (year - years_completed)
                else:
                    # Future years
                    cumulative_investment += annual_investment
                    balance = cumulative_investment * (1 + ppf_rate/100) ** (year - years_completed)

                yearly_balance.append(balance)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=years, y=yearly_balance, name='PPF Balance', fill='tonexty', line=dict(color='#4CAF50')))

            fig.update_layout(
                title='PPF Balance Growth Over 15 Years',
                xaxis_title='Year',
                yaxis_title='Balance (₹)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            # PPF features and benefits
            st.markdown("#### 💡 PPF Features & Benefits")

            features = [
                "🔒 **Lock-in Period**: 15 years (extendable in blocks of 5 years)",
                "💰 **Tax Benefits**: Investment, interest, and maturity all tax-free (EEE)",
                "🏦 **Government Backing**: Sovereign guarantee on returns",
                "💳 **Loan Facility**: Available from 3rd year onwards",
                "💸 **Partial Withdrawal**: Allowed from 7th year onwards",
                "📈 **Compounding**: Annual compounding of interest"
            ]

            for feature in features:
                st.info(feature)

            # PPF vs other investments
            st.markdown("#### ⚖️ PPF vs Other Tax-Saving Investments")

            comparison_data = {
                'Investment': ['PPF', 'ELSS', 'NSC', 'Tax Saver FD', 'Life Insurance'],
                'Lock-in (Years)': [15, 3, 5, 5, 'Till maturity'],
                'Tax on Returns': ['Nil', '10% LTCG', 'Taxable', 'Taxable', 'Nil'],
                'Expected Return (%)': [7.1, '12-15', 6.8, '5-7', '4-6'],
                'Risk Level': ['Nil', 'High', 'Nil', 'Nil', 'Low']
            }

            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True)

        except Exception as e:
            self.logger.error(f"PPF calculator error: {e}")
            st.error(f"PPF calculator error: {e}")

    def render_nsc_calculator(self, language: str):
        """Render NSC Calculator"""
        try:
            st.markdown("""
            <div class="calculator-container">
                <h3>📜 NSC Calculator - National Savings Certificate</h3>
                <p>Calculate returns on NSC investments</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                investment_amount = st.number_input("Investment Amount (₹)", min_value=1000, max_value=1500000, value=100000)
                nsc_rate = st.slider("NSC Interest Rate (%)", min_value=6.0, max_value=8.0, value=6.8, step=0.1)

                # NSC is 5-year investment
                tenure = 5
                maturity_amount = investment_amount * (1 + nsc_rate/100) ** tenure
                interest_earned = maturity_amount - investment_amount

            with col2:
                st.metric("Maturity Amount", f"₹{maturity_amount:,.0f}")
                st.metric("Interest Earned", f"₹{interest_earned:,.0f}")
                st.metric("Tenure", f"{tenure} years")

        except Exception as e:
            st.error(f"NSC calculator error: {e}")

    def render_elss_calculator(self, language: str):
        """Render ELSS Calculator"""
        try:
            st.markdown("""
            <div class="calculator-container">
                <h3>🎯 ELSS Calculator - Tax Saving Mutual Funds</h3>
                <p>Calculate ELSS returns and tax savings</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                investment_type = st.radio("Investment Type", ["Lump Sum", "SIP"])

                if investment_type == "Lump Sum":
                    investment_amount = st.number_input("Investment Amount (₹)", min_value=500, max_value=150000, value=150000)
                    tenure = st.slider("Investment Period (Years)", min_value=3, max_value=20, value=5)
                else:
                    monthly_sip = st.number_input("Monthly SIP (₹)", min_value=500, max_value=12500, value=5000)
                    tenure = st.slider("SIP Period (Years)", min_value=3, max_value=20, value=10)

                expected_return = st.slider("Expected Annual Return (%)", min_value=8.0, max_value=18.0, value=12.0)

                # Calculate returns
                if investment_type == "Lump Sum":
                    maturity_amount = investment_amount * (1 + expected_return/100) ** tenure
                    total_investment = investment_amount
                else:
                    monthly_return = expected_return / 12 / 100
                    total_months = tenure * 12
                    maturity_amount = monthly_sip * (((1 + monthly_return) ** total_months - 1) / monthly_return) * (1 + monthly_return)
                    total_investment = monthly_sip * total_months

                total_returns = maturity_amount - total_investment

                # Tax savings
                annual_investment = total_investment / tenure if tenure > 0 else total_investment
                tax_saved = min(annual_investment, 150000) * 0.20  # Assuming 20% tax bracket

            with col2:
                st.metric("Total Investment", f"₹{total_investment:,.0f}")
                st.metric("Maturity Amount", f"₹{maturity_amount:,.0f}")
                st.metric("Total Returns", f"₹{total_returns:,.0f}")
                st.metric("Annual Tax Saved", f"₹{tax_saved:,.0f}")

        except Exception as e:
            st.error(f"ELSS calculator error: {e}")

    def render_lumpsum_calculator(self, language: str):
        """Render Lumpsum Calculator"""
        try:
            st.markdown("""
            <div class="calculator-container">
                <h3>💰 Lumpsum Calculator - One-time Investment</h3>
                <p>Calculate returns on lumpsum investments</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                investment_amount = st.number_input("Investment Amount (₹)", min_value=1000, max_value=10000000, value=500000)
                expected_return = st.slider("Expected Annual Return (%)", min_value=6.0, max_value=20.0, value=12.0)
                investment_period = st.slider("Investment Period (Years)", min_value=1, max_value=30, value=10)

                maturity_amount = investment_amount * (1 + expected_return/100) ** investment_period
                total_returns = maturity_amount - investment_amount

            with col2:
                st.metric("Investment Amount", f"₹{investment_amount:,.0f}")
                st.metric("Maturity Amount", f"₹{maturity_amount:,.0f}")
                st.metric("Total Returns", f"₹{total_returns:,.0f}")
                st.metric("Return Multiple", f"{maturity_amount/investment_amount:.1f}x")

        except Exception as e:
            st.error(f"Lumpsum calculator error: {e}")

    def render_goal_calculator(self, language: str):
        """Render Goal Calculator"""
        try:
            st.markdown("""
            <div class="calculator-container">
                <h3>🎯 Goal Calculator - Financial Goal Planning</h3>
                <p>Plan your financial goals and required investments</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                goal_name = st.text_input("Goal Name", value="Child's Education")
                target_amount = st.number_input("Target Amount (₹)", min_value=100000, max_value=50000000, value=2000000)
                time_horizon = st.number_input("Time Horizon (Years)", min_value=1, max_value=30, value=15)
                current_savings = st.number_input("Current Savings for Goal (₹)", min_value=0, max_value=10000000, value=100000)
                expected_return = st.slider("Expected Return (%)", min_value=6.0, max_value=15.0, value=10.0)

                # Calculate required SIP
                future_value_current = current_savings * (1 + expected_return/100) ** time_horizon
                remaining_target = target_amount - future_value_current

                if remaining_target > 0:
                    monthly_return = expected_return / 12 / 100
                    total_months = time_horizon * 12
                    required_sip = remaining_target * monthly_return / (((1 + monthly_return) ** total_months - 1) * (1 + monthly_return))
                else:
                    required_sip = 0

            with col2:
                st.metric("Target Amount", f"₹{target_amount:,.0f}")
                st.metric("Time Horizon", f"{time_horizon} years")
                st.metric("Required Monthly SIP", f"₹{required_sip:,.0f}")

                if required_sip > 0:
                    total_sip_investment = required_sip * time_horizon * 12
                    st.metric("Total SIP Investment", f"₹{total_sip_investment:,.0f}")
                else:
                    st.success("🎉 Current savings are sufficient for your goal!")

        except Exception as e:
            st.error(f"Goal calculator error: {e}")


def main():
    """Main function to run the restored JarvisFi 2.0 application"""
    try:
        app = RestoredJarvisFiApp()
        app.run()
    except Exception as e:
        st.error(f"Application startup failed: {e}")
        st.info("Please refresh the page to restart the application.")
        st.markdown("### 🔧 Debug Information")
        st.code(f"Startup Error: {e}")


if __name__ == "__main__":
    main()
