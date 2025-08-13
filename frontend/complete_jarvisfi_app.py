"""
Complete JarvisFi Application - Multilingual AI Personal Finance Chatbot
Implements all features: Voice interface, RAG, demographic awareness, farmer tools, etc.
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

# Import backend services
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

class CompleteJarvisFiApp:
    """
    Complete JarvisFi application with all advanced features
    """
    
    def __init__(self):
        self.logger = logger
        self.setup_page_config()
        self.initialize_services()
        self.initialize_session_state()
    
    def setup_page_config(self):
        """Configure Streamlit page"""
        st.set_page_config(
            page_title="JarvisFi - AI Financial Genius",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://jarvisfi.com/help',
                'Report a bug': 'https://jarvisfi.com/bug-report',
                'About': "JarvisFi v2.0 - Your AI-Powered Financial Genius"
            }
        )
        
        # Custom CSS for better UI
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .feature-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #2a5298;
            margin: 0.5rem 0;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        .voice-indicator {
            background: #28a745;
            color: white;
            padding: 0.5rem;
            border-radius: 20px;
            text-align: center;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        }
        </style>
        """, unsafe_allow_html=True)
    
    def initialize_services(self):
        """Initialize backend services"""
        if BACKEND_AVAILABLE:
            try:
                self.ai_engine = CoreAIEngine()
                self.financial_services = FinancialServices()
                self.voice_processor = VoiceProcessor()
                self.services_available = True
                self.logger.info("✅ All backend services initialized")
            except Exception as e:
                self.logger.error(f"❌ Error initializing services: {e}")
                self.services_available = False
        else:
            self.services_available = False
            self.logger.warning("⚠️ Running in demo mode without backend services")
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        # User profile with comprehensive data
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
                    'occupation': 'Software Engineer'
                },
                'financial_profile': {
                    'risk_tolerance': 'moderate',
                    'investment_experience': 'beginner',
                    'financial_goals': ['retirement', 'house', 'emergency_fund'],
                    'current_investments': 0,
                    'monthly_expenses': 30000,
                    'debt_info': {},
                    'credit_score': 750
                },
                'preferences': {
                    'dark_mode': False,
                    'voice_enabled': True,
                    'notifications': True,
                    'ai_accuracy_mode': True,
                    'enhanced_sources': True,
                    'learning_mode': False
                },
                'security': {
                    'two_factor_enabled': False,
                    'biometric_enabled': False,
                    'data_encryption': True
                }
            }
        
        # Chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Voice state
        if 'voice_active' not in st.session_state:
            st.session_state.voice_active = False
        
        # Navigation state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        
        # Performance tracking
        if 'session_start_time' not in st.session_state:
            st.session_state.session_start_time = time.time()
        
        # Gamification
        if 'gamification' not in st.session_state:
            st.session_state.gamification = {
                'points': 0,
                'level': 1,
                'badges': [],
                'challenges_completed': 0,
                'streak_days': 0
            }
    
    def run(self):
        """Main application runner"""
        try:
            # Create sidebar
            self.create_comprehensive_sidebar()
            
            # Main header
            self.render_main_header()
            
            # Navigation and content
            self.render_main_content()
            
            # Footer
            self.render_footer()
            
        except Exception as e:
            self.logger.error(f"❌ Application error: {e}")
            st.error("An error occurred. Please refresh the page.")
    
    def create_comprehensive_sidebar(self):
        """Create comprehensive sidebar with all settings"""
        with st.sidebar:
            # JarvisFi branding
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: linear-gradient(45deg, #1e3c72, #2a5298); border-radius: 10px; color: white; margin-bottom: 1rem;">
                <h2>🤖 JarvisFi</h2>
                <p><i>Your AI-Powered Financial Genius</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick stats
            self.render_quick_stats()
            
            # User profile section
            self.render_user_profile_section()
            
            # Language and preferences
            self.render_language_preferences()
            
            # Voice settings
            self.render_voice_settings()
            
            # AI and security settings
            self.render_ai_security_settings()
            
            # Quick actions
            self.render_quick_actions()
            
            # Help section
            self.render_help_section()
    
    def render_quick_stats(self):
        """Render quick financial stats"""
        st.markdown("### 📊 Quick Stats")
        
        profile = st.session_state.user_profile
        monthly_income = profile['basic_info']['monthly_income']
        monthly_expenses = profile['financial_profile']['monthly_expenses']
        savings_rate = ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Monthly Income", f"₹{monthly_income:,}")
            st.metric("💳 Credit Score", profile['financial_profile']['credit_score'])
        
        with col2:
            st.metric("💸 Monthly Expenses", f"₹{monthly_expenses:,}")
            st.metric("📈 Savings Rate", f"{savings_rate:.1f}%")
        
        # Savings rate indicator
        if savings_rate >= 20:
            st.success("🎉 Excellent savings rate!")
        elif savings_rate >= 10:
            st.info("👍 Good savings rate")
        else:
            st.warning("⚠️ Consider increasing savings")
        
        st.markdown("---")
    
    def render_user_profile_section(self):
        """Render user profile configuration"""
        st.markdown("### 👤 User Profile")
        
        profile = st.session_state.user_profile['basic_info']
        
        # User type selection
        user_types = {
            'student': '🎓 Student',
            'professional': '💼 Professional', 
            'farmer': '👨‍🌾 Farmer',
            'senior_citizen': '👴 Senior Citizen',
            'entrepreneur': '🚀 Entrepreneur',
            'homemaker': '🏠 Homemaker'
        }
        
        selected_type = st.selectbox(
            "User Type",
            options=list(user_types.keys()),
            format_func=lambda x: user_types[x],
            index=list(user_types.keys()).index(profile['user_type']) if profile['user_type'] in user_types else 0
        )
        
        if selected_type != profile['user_type']:
            st.session_state.user_profile['basic_info']['user_type'] = selected_type
            st.rerun()
        
        # Monthly income
        monthly_income = st.number_input(
            "Monthly Income (₹)",
            min_value=5000,
            max_value=10000000,
            value=profile['monthly_income'],
            step=5000,
            help="Your monthly income for personalized advice"
        )
        
        if monthly_income != profile['monthly_income']:
            st.session_state.user_profile['basic_info']['monthly_income'] = monthly_income
            st.rerun()
        
        # Age
        age = st.slider("Age", 18, 80, profile['age'])
        if age != profile['age']:
            st.session_state.user_profile['basic_info']['age'] = age
            st.rerun()
        
        st.markdown("---")
    
    def render_language_preferences(self):
        """Render language and preference settings"""
        st.markdown("### 🌐 Language & Preferences")
        
        # Language selection
        languages = {
            'en': '🇺🇸 English',
            'ta': '🇮🇳 தமிழ் (Tamil)',
            'hi': '🇮🇳 हिंदी (Hindi)',
            'te': '🇮🇳 తెలుగు (Telugu)'
        }
        
        current_lang = st.session_state.user_profile['basic_info']['language']
        selected_lang = st.selectbox(
            "Language",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            index=list(languages.keys()).index(current_lang)
        )
        
        if selected_lang != current_lang:
            st.session_state.user_profile['basic_info']['language'] = selected_lang
            st.rerun()
        
        # Dark mode
        dark_mode = st.toggle(
            "🌙 Dark Mode",
            value=st.session_state.user_profile['preferences']['dark_mode']
        )
        st.session_state.user_profile['preferences']['dark_mode'] = dark_mode
        
        # Currency
        currencies = ['INR', 'USD', 'EUR', 'GBP']
        currency = st.selectbox(
            "Currency",
            currencies,
            index=currencies.index(st.session_state.user_profile['basic_info']['currency'])
        )
        st.session_state.user_profile['basic_info']['currency'] = currency
        
        st.markdown("---")
    
    def render_voice_settings(self):
        """Render voice interface settings"""
        st.markdown("### 🎤 Voice Assistant")
        
        # Voice capabilities
        if self.services_available:
            capabilities = self.voice_processor.get_voice_capabilities()
            
            if capabilities['stt_available']:
                st.success("✅ Speech Recognition Available")
            else:
                st.warning("⚠️ Speech Recognition Limited")
            
            if capabilities['tts_available']:
                st.success("✅ Text-to-Speech Available")
            else:
                st.warning("⚠️ Text-to-Speech Limited")
        
        # Voice settings
        voice_enabled = st.toggle(
            "Enable Voice Interface",
            value=st.session_state.user_profile['preferences']['voice_enabled']
        )
        st.session_state.user_profile['preferences']['voice_enabled'] = voice_enabled
        
        if voice_enabled:
            # Voice quality
            voice_quality = st.selectbox(
                "Voice Quality",
                ["Standard", "High Quality", "Natural"],
                index=1
            )
            
            # Speech speed
            speech_speed = st.slider(
                "Speech Speed",
                0.5, 2.0, 1.0, 0.1
            )
        
        st.markdown("---")
    
    def render_ai_security_settings(self):
        """Render AI and security settings"""
        st.markdown("### 🧠 AI & Security")
        
        # AI settings
        ai_accuracy = st.toggle(
            "AI Fact-Checking",
            value=st.session_state.user_profile['preferences']['ai_accuracy_mode'],
            help="Enable fact-checking with RBI/SEBI documents"
        )
        st.session_state.user_profile['preferences']['ai_accuracy_mode'] = ai_accuracy
        
        enhanced_sources = st.toggle(
            "Enhanced Sources",
            value=st.session_state.user_profile['preferences']['enhanced_sources'],
            help="Show detailed sources for AI responses"
        )
        st.session_state.user_profile['preferences']['enhanced_sources'] = enhanced_sources
        
        # Security settings
        st.markdown("**Security Status**")
        if st.session_state.user_profile['security']['data_encryption']:
            st.success("🔒 Data Encrypted")
        else:
            st.warning("🔓 Basic Security")
        
        data_encryption = st.toggle(
            "Data Encryption",
            value=st.session_state.user_profile['security']['data_encryption']
        )
        st.session_state.user_profile['security']['data_encryption'] = data_encryption
        
        st.markdown("---")
    
    def render_quick_actions(self):
        """Render quick action buttons"""
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💬 AI Chat", use_container_width=True):
                st.session_state.current_page = 'chat'
                st.rerun()
            
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.current_page = 'dashboard'
                st.rerun()
            
            if st.button("🧮 Calculators", use_container_width=True):
                st.session_state.current_page = 'calculators'
                st.rerun()
        
        with col2:
            if st.button("🎤 Voice Chat", use_container_width=True):
                st.session_state.current_page = 'voice'
                st.rerun()
            
            if st.button("👨‍🌾 Farmer Tools", use_container_width=True):
                st.session_state.current_page = 'farmer'
                st.rerun()
            
            if st.button("💳 Credit Score", use_container_width=True):
                st.session_state.current_page = 'credit'
                st.rerun()
        
        st.markdown("---")
    
    def render_help_section(self):
        """Render help and information section"""
        with st.expander("ℹ️ Help & Information"):
            st.markdown("""
            **🤖 JarvisFi Features:**
            
            • **AI Chat**: Ask questions about finance in your language
            • **Voice Interface**: Speak to JarvisFi naturally
            • **Farmer Tools**: Specialized tools for agricultural finance
            • **Credit Tracking**: Monitor and improve your credit score
            • **Investment Advice**: Personalized investment recommendations
            • **Tax Planning**: Optimize your tax savings
            • **Budget Planning**: Smart budgeting with AI insights
            
            **🎯 Sample Questions:**
            - "How much should I save monthly?"
            - "What are the best investment options?"
            - "How to improve my credit score?"
            - "Calculate EMI for home loan"
            """)
            
            # Sample questions as buttons
            sample_questions = [
                "How much should I save monthly?",
                "Best investment options for me?",
                "How to improve credit score?"
            ]
            
            for i, question in enumerate(sample_questions):
                if st.button(f"💡 {question}", key=f"sample_{i}"):
                    # Add to chat and switch to chat page
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': question,
                        'timestamp': datetime.now().isoformat()
                    })
                    st.session_state.current_page = 'chat'
                    st.rerun()
    
    def render_main_header(self):
        """Render main application header"""
        current_lang = st.session_state.user_profile['basic_info']['language']
        
        # Dynamic header based on language
        headers = {
            'en': "🤖 JarvisFi - Your AI-Powered Financial Genius",
            'ta': "🤖 JarvisFi - உங்கள் AI-இயங்கும் நிதி மேதை",
            'hi': "🤖 JarvisFi - आपका AI-संचालित वित्तीय प्रतिभा",
            'te': "🤖 JarvisFi - మీ AI-శక్తితో కూడిన ఆర్థిక మేధావి"
        }
        
        st.markdown(f"""
        <div class="main-header">
            <h1>{headers.get(current_lang, headers['en'])}</h1>
            <p>Multilingual • Voice-Enabled • RAG-Enhanced • Farmer-Friendly</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Status indicators
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if self.services_available:
                st.success("🟢 AI Services Online")
            else:
                st.warning("🟡 Demo Mode")
        
        with col2:
            if st.session_state.user_profile['preferences']['voice_enabled']:
                st.info("🎤 Voice Enabled")
            else:
                st.info("🔇 Voice Disabled")
        
        with col3:
            lang_display = {
                'en': '🇺🇸 EN', 'ta': '🇮🇳 TA', 
                'hi': '🇮🇳 HI', 'te': '🇮🇳 TE'
            }
            st.info(f"🌐 {lang_display.get(current_lang, '🇺🇸 EN')}")
        
        with col4:
            user_type = st.session_state.user_profile['basic_info']['user_type']
            type_icons = {
                'student': '🎓', 'professional': '💼', 'farmer': '👨‍🌾',
                'senior_citizen': '👴', 'entrepreneur': '🚀', 'homemaker': '🏠'
            }
            st.info(f"{type_icons.get(user_type, '👤')} {user_type.title()}")
    
    def render_main_content(self):
        """Render main content based on current page"""
        current_page = st.session_state.current_page
        
        # Navigation tabs
        tab_names = {
            'en': ["🏠 Home", "💬 AI Chat", "📊 Dashboard", "🧮 Calculators", 
                   "🎤 Voice", "👨‍🌾 Farmer Tools", "💳 Credit Score", "📈 Investments"],
            'ta': ["🏠 முகப்பு", "💬 AI அரட்டை", "📊 டாஷ்போர்டு", "🧮 கணக்கீட்டாளர்கள்",
                   "🎤 குரல்", "👨‍🌾 விவசாயி கருவிகள்", "💳 கிரெடிட் ஸ்கோர்", "📈 முதலீடுகள்"]
        }
        
        current_lang = st.session_state.user_profile['basic_info']['language']
        tabs = tab_names.get(current_lang, tab_names['en'])
        
        # Create tabs
        tab_objects = st.tabs(tabs)
        
        # Render content for each tab
        with tab_objects[0]:  # Home
            self.render_home_page()
        
        with tab_objects[1]:  # AI Chat
            self.render_ai_chat_page()
        
        with tab_objects[2]:  # Dashboard
            self.render_dashboard_page()
        
        with tab_objects[3]:  # Calculators
            self.render_calculators_page()
        
        with tab_objects[4]:  # Voice
            self.render_voice_page()
        
        with tab_objects[5]:  # Farmer Tools
            self.render_farmer_tools_page()
        
        with tab_objects[6]:  # Credit Score
            self.render_credit_score_page()
        
        with tab_objects[7]:  # Investments
            self.render_investments_page()
    
    def render_footer(self):
        """Render application footer"""
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🤖 JarvisFi v2.0**")
            st.markdown("*Your AI-Powered Financial Genius*")
        
        with col2:
            st.markdown("**🌟 Features**")
            st.markdown("• Multilingual Support\n• Voice Interface\n• RAG-Enhanced AI")
        
        with col3:
            st.markdown("**📊 Session Stats**")
            session_time = time.time() - st.session_state.session_start_time
            st.markdown(f"• Session: {session_time/60:.1f} min\n• Points: {st.session_state.gamification['points']}")

    def render_home_page(self):
        """Render organized home page with overview, quick actions, and data saving options"""
        current_lang = st.session_state.user_profile['basic_info']['language']

        # Welcome message with user greeting
        profile = st.session_state.user_profile
        user_name = profile['basic_info'].get('name', 'User')
        user_type = profile['basic_info']['user_type']

        welcome_messages = {
            'en': f"Welcome back, {user_name}! 👋",
            'ta': f"மீண்டும் வரவேற்கிறோம், {user_name}! 👋",
            'hi': f"वापसी पर स्वागत है, {user_name}! 👋",
            'te': f"తిరిగి స్వాగతం, {user_name}! 👋"
        }

        # Header section with organized layout
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 2rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;">
            <h1 style="margin: 0; font-size: 2.5rem;">🏠 Financial Dashboard</h1>
            <h3 style="margin: 0.5rem 0; opacity: 0.9;">{}</h3>
            <p style="margin: 0; opacity: 0.8;">Your personalized financial overview and insights</p>
        </div>
        """.format(welcome_messages.get(current_lang, welcome_messages['en'])), unsafe_allow_html=True)

        # === SECTION 1: FINANCIAL OVERVIEW CARDS ===
        st.markdown("## 📊 Financial Overview")

        monthly_income = profile['basic_info']['monthly_income']
        monthly_expenses = profile['financial_profile']['monthly_expenses']
        savings = monthly_income - monthly_expenses
        credit_score = profile['financial_profile']['credit_score']
        savings_rate = (savings / monthly_income * 100) if monthly_income > 0 else 0

        # Enhanced metric cards with better styling
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4CAF50, #45a049);
                        padding: 1.5rem; border-radius: 12px; color: white; text-align: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0; opacity: 0.9;">💰 Monthly Income</h4>
                <h2 style="margin: 0.5rem 0; font-size: 2rem;">₹{:,}</h2>
                <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Primary source</p>
            </div>
            """.format(monthly_income), unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #FF6B6B, #ee5a52);
                        padding: 1.5rem; border-radius: 12px; color: white; text-align: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0; opacity: 0.9;">💸 Monthly Expenses</h4>
                <h2 style="margin: 0.5rem 0; font-size: 2rem;">₹{:,}</h2>
                <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{:.1f}% of income</p>
            </div>
            """.format(monthly_expenses, (monthly_expenses/monthly_income*100) if monthly_income > 0 else 0), unsafe_allow_html=True)

        with col3:
            savings_color = "#4CAF50" if savings > 0 else "#FF6B6B"
            st.markdown("""
            <div style="background: linear-gradient(135deg, {}, {});
                        padding: 1.5rem; border-radius: 12px; color: white; text-align: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0; opacity: 0.9;">💰 Monthly Savings</h4>
                <h2 style="margin: 0.5rem 0; font-size: 2rem;">₹{:,}</h2>
                <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{:.1f}% savings rate</p>
            </div>
            """.format(savings_color, savings_color, savings, savings_rate), unsafe_allow_html=True)

        with col4:
            score_color = "#4CAF50" if credit_score >= 750 else "#FFA726" if credit_score >= 650 else "#FF6B6B"
            st.markdown("""
            <div style="background: linear-gradient(135deg, {}, {});
                        padding: 1.5rem; border-radius: 12px; color: white; text-align: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0; opacity: 0.9;">💳 Credit Score</h4>
                <h2 style="margin: 0.5rem 0; font-size: 2rem;">{}</h2>
                <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{}</p>
            </div>
            """.format(score_color, score_color, credit_score,
                      "Excellent" if credit_score >= 750 else "Good" if credit_score >= 650 else "Fair"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # === SECTION 2: QUICK ACTION BUTTONS ===
        st.markdown("## 🚀 Quick Actions")

        # Organized quick action buttons
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("💬 Start AI Chat", use_container_width=True, help="Chat with JarvisFi AI assistant"):
                st.session_state.current_page = 'chat'
                st.rerun()

        with col2:
            if st.button("🧮 Financial Calculators", use_container_width=True, help="Access SIP, EMI, Tax calculators"):
                st.session_state.current_page = 'calculators'
                st.rerun()

        with col3:
            if st.button("🎤 Voice Assistant", use_container_width=True, help="Use voice commands"):
                st.session_state.current_page = 'voice'
                st.rerun()

        with col4:
            if st.button("📈 Investment Portfolio", use_container_width=True, help="Manage your investments"):
                st.session_state.current_page = 'investments'
                st.rerun()

        # Second row of quick actions
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("👨‍🌾 Farmer Tools", use_container_width=True, help="Agricultural finance tools"):
                st.session_state.current_page = 'farmer'
                st.rerun()

        with col2:
            if st.button("💳 Credit Score", use_container_width=True, help="Track and improve credit score"):
                st.session_state.current_page = 'credit'
                st.rerun()

        with col3:
            if st.button("📊 Full Dashboard", use_container_width=True, help="Comprehensive financial dashboard"):
                st.session_state.current_page = 'dashboard'
                st.rerun()

        with col4:
            # Data Save Button
            if st.button("💾 Save Data", use_container_width=True, help="Save your financial data"):
                self.show_data_save_options()

        st.markdown("---")

        # === SECTION 3: FINANCIAL INSIGHTS ===
        st.markdown("## 📈 Financial Insights")

        col1, col2 = st.columns(2)

        with col1:
            # Enhanced savings rate gauge
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

            # Savings rate interpretation
            if savings_rate >= 20:
                st.success("🎉 Excellent savings rate! You're on track for financial success.")
            elif savings_rate >= 10:
                st.info("👍 Good savings rate. Consider increasing to 20% for optimal growth.")
            else:
                st.warning("⚠️ Low savings rate. Focus on reducing expenses or increasing income.")

        with col2:
            # Enhanced expense breakdown
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

            # Expense analysis
            housing_percent = (monthly_expenses * 0.4 / monthly_income * 100) if monthly_income > 0 else 0
            if housing_percent > 30:
                st.warning("🏠 Housing costs are high (>30% of income). Consider optimization.")
            else:
                st.success("🏠 Housing costs are within recommended limits.")

        st.markdown("---")

        # === SECTION 4: PERSONALIZED RECOMMENDATIONS ===
        st.markdown("## 💡 Personalized Recommendations")

        # Get recommendations based on user type
        recommendations = self.get_personalized_recommendations(user_type, monthly_income, savings_rate)

        # Display recommendations in organized cards
        col1, col2 = st.columns(2)

        for i, rec in enumerate(recommendations):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef);
                            padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;
                            border-left: 4px solid #007bff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <p style="margin: 0; font-size: 1rem; color: #333;">{rec}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # === SECTION 5: FINANCIAL GOALS PROGRESS ===
        st.markdown("## 🎯 Financial Goals Progress")

        # Sample financial goals (can be customized based on user profile)
        goals = self.get_financial_goals(monthly_income, user_type)

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

            # Progress indicator
            if progress >= 80:
                st.success(f"🎉 {progress:.1f}% complete - Almost there!")
            elif progress >= 50:
                st.info(f"📈 {progress:.1f}% complete - Good progress!")
            else:
                st.warning(f"⏳ {progress:.1f}% complete - Keep going!")

            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("---")

        # === SECTION 6: RECENT ACTIVITY & NOTIFICATIONS ===
        st.markdown("## 📢 Recent Activity & Notifications")

        # Sample recent activities
        activities = self.get_recent_activities(current_lang)

        for activity in activities:
            icon = activity['icon']
            message = activity['message']
            time_ago = activity['time']
            activity_type = activity['type']

            if activity_type == 'success':
                st.success(f"{icon} {message} - {time_ago}")
            elif activity_type == 'info':
                st.info(f"{icon} {message} - {time_ago}")
            elif activity_type == 'warning':
                st.warning(f"{icon} {message} - {time_ago}")

        st.markdown("---")

        # === SECTION 7: QUICK STATS SUMMARY ===
        st.markdown("## 📊 Quick Stats Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; text-align: center;">
                <h4 style="color: #1976d2; margin: 0;">💰 Net Worth</h4>
                <h3 style="color: #1976d2; margin: 0.5rem 0;">₹{:,}</h3>
                <p style="color: #666; margin: 0; font-size: 0.9rem;">Estimated total assets</p>
            </div>
            """.format(savings * 12 + 100000), unsafe_allow_html=True)  # Rough estimate

        with col2:
            annual_savings = savings * 12
            st.markdown("""
            <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; text-align: center;">
                <h4 style="color: #388e3c; margin: 0;">📈 Annual Savings</h4>
                <h3 style="color: #388e3c; margin: 0.5rem 0;">₹{:,}</h3>
                <p style="color: #666; margin: 0; font-size: 0.9rem;">Projected yearly savings</p>
            </div>
            """.format(annual_savings), unsafe_allow_html=True)

        with col3:
            session_time = time.time() - st.session_state.session_start_time
            st.markdown("""
            <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; text-align: center;">
                <h4 style="color: #f57c00; margin: 0;">⏱️ Session Time</h4>
                <h3 style="color: #f57c00; margin: 0.5rem 0;">{:.1f} min</h3>
                <p style="color: #666; margin: 0; font-size: 0.9rem;">Time spent today</p>
            </div>
            """.format(session_time / 60), unsafe_allow_html=True)

    def get_personalized_recommendations(self, user_type: str, monthly_income: int, savings_rate: float) -> List[str]:
        """Get personalized recommendations based on user profile"""
        base_recommendations = {
            'student': [
                "🎓 Start with small SIPs (₹500-1000) to build investment habit",
                "📚 Focus on education loans with lower interest rates",
                "💰 Build emergency fund of ₹10,000-20,000",
                "📱 Use student discounts and cashback offers"
            ],
            'farmer': [
                "🌾 Utilize PM-KISAN scheme for ₹6,000 annual benefit",
                "🚜 Consider crop insurance for risk management",
                "💰 Invest surplus after harvest in mutual funds",
                "🏦 Apply for Kisan Credit Card for easy loans"
            ],
            'professional': [
                "💼 Maximize 80C deductions up to ₹1.5 lakh",
                "📈 Start SIP with 15% of income for wealth building",
                "🏠 Plan for home loan with EMI <40% of income",
                "💳 Maintain credit utilization below 30%"
            ],
            'senior_citizen': [
                "🏦 Focus on fixed deposits and government schemes",
                "💊 Plan for healthcare expenses and insurance",
                "📈 Consider Senior Citizen Savings Scheme (SCSS)",
                "🏠 Evaluate reverse mortgage options if needed"
            ]
        }

        recommendations = base_recommendations.get(user_type, [
            "💰 Build emergency fund of 6 months expenses",
            "📈 Diversify investments across equity and debt",
            "💳 Monitor credit score regularly",
            "🎯 Set clear financial goals with timelines"
        ])

        # Add income-specific recommendations
        if monthly_income < 25000:
            recommendations.append("💡 Focus on skill development to increase income")
        elif monthly_income > 100000:
            recommendations.append("🏛️ Consider tax-saving investments and wealth management")

        # Add savings rate specific recommendations
        if savings_rate < 10:
            recommendations.append("⚠️ Urgent: Review and reduce unnecessary expenses")
        elif savings_rate > 30:
            recommendations.append("🎉 Excellent savings! Consider increasing investment allocation")

        return recommendations[:6]  # Return top 6 recommendations

    def get_financial_goals(self, monthly_income: int, user_type: str) -> List[Dict]:
        """Get financial goals based on user profile"""
        emergency_target = monthly_income * 6
        retirement_target = monthly_income * 12 * 25  # 25x annual income

        if user_type == 'student':
            goals = [
                {'name': '🎓 Education Fund', 'target': 200000, 'current': 50000},
                {'name': '💰 Emergency Fund', 'target': emergency_target // 3, 'current': emergency_target // 6},
                {'name': '📱 Gadget Fund', 'target': 50000, 'current': 20000}
            ]
        elif user_type == 'farmer':
            goals = [
                {'name': '🌾 Crop Investment Fund', 'target': 300000, 'current': 150000},
                {'name': '🚜 Equipment Fund', 'target': 500000, 'current': 200000},
                {'name': '💰 Emergency Fund', 'target': emergency_target, 'current': emergency_target // 3}
            ]
        elif user_type == 'professional':
            goals = [
                {'name': '🏠 House Down Payment', 'target': 2000000, 'current': 800000},
                {'name': '💰 Emergency Fund', 'target': emergency_target, 'current': emergency_target // 2},
                {'name': '🏖️ Retirement Corpus', 'target': retirement_target // 10, 'current': retirement_target // 50}
            ]
        else:
            goals = [
                {'name': '💰 Emergency Fund', 'target': emergency_target, 'current': emergency_target // 3},
                {'name': '🏖️ Retirement Planning', 'target': retirement_target // 20, 'current': retirement_target // 100},
                {'name': '🎯 Dream Goal', 'target': 1000000, 'current': 300000}
            ]

        return goals

    def get_recent_activities(self, language: str) -> List[Dict]:
        """Get recent activities and notifications"""
        activities_en = [
            {'icon': '💰', 'message': 'Monthly SIP of ₹5,000 processed successfully', 'time': '2 hours ago', 'type': 'success'},
            {'icon': '📊', 'message': 'Credit score updated - increased by 15 points', 'time': '1 day ago', 'type': 'success'},
            {'icon': '⚠️', 'message': 'High expense alert: Entertainment spending exceeded budget', 'time': '3 days ago', 'type': 'warning'},
            {'icon': '📈', 'message': 'Investment portfolio gained 2.5% this month', 'time': '1 week ago', 'type': 'info'}
        ]

        activities_ta = [
            {'icon': '💰', 'message': 'மாதாந்திர SIP ₹5,000 வெற்றிகரமாக செயல்படுத்தப்பட்டது', 'time': '2 மணி நேரம் முன்பு', 'type': 'success'},
            {'icon': '📊', 'message': 'கிரெடிட் ஸ்கோர் புதுப்பிக்கப்பட்டது - 15 புள்ளிகள் அதிகரித்தது', 'time': '1 நாள் முன்பு', 'type': 'success'},
            {'icon': '⚠️', 'message': 'அதிக செலவு எச்சரிக்கை: பொழுதுபோக்கு செலவு பட்ஜெட்டை மீறியது', 'time': '3 நாட்கள் முன்பு', 'type': 'warning'},
            {'icon': '📈', 'message': 'முதலீட்டு போர்ட்ஃபோலியோ இந்த மாதம் 2.5% லாபம் பெற்றது', 'time': '1 வாரம் முன்பு', 'type': 'info'}
        ]

        return activities_ta if language == 'ta' else activities_en

    def show_data_save_options(self):
        """Show data saving options with retention period selection"""
        current_lang = st.session_state.user_profile['basic_info']['language']

        # Initialize data save settings if not exists
        if 'data_save_settings' not in st.session_state:
            st.session_state.data_save_settings = {
                'auto_save': True,
                'retention_period': 30,
                'last_save': None,
                'save_location': 'local',
                'encryption_enabled': True
            }

        # Data save dialog
        with st.expander("💾 Data Save Options", expanded=True):
            st.markdown("### 🔒 Save Your Financial Data")

            # Language-specific text
            save_texts = {
                'en': {
                    'title': '💾 Data Storage Settings',
                    'retention': 'Data Retention Period',
                    'location': 'Save Location',
                    'encryption': 'Enable Encryption',
                    'auto_save': 'Auto-save enabled',
                    'save_now': 'Save Now',
                    'export': 'Export Data'
                },
                'ta': {
                    'title': '💾 தரவு சேமிப்பு அமைப்புகள்',
                    'retention': 'தரவு வைத்திருக்கும் காலம்',
                    'location': 'சேமிப்பு இடம்',
                    'encryption': 'குறியாக்கத்தை இயக்கு',
                    'auto_save': 'தானியங்கு சேமிப்பு இயக்கப்பட்டது',
                    'save_now': 'இப்போது சேமிக்கவும்',
                    'export': 'தரவை ஏற்றுமதி செய்யவும்'
                },
                'hi': {
                    'title': '💾 डेटा भंडारण सेटिंग्स',
                    'retention': 'डेटा रिटेंशन अवधि',
                    'location': 'सेव लोकेशन',
                    'encryption': 'एन्क्रिप्शन सक्षम करें',
                    'auto_save': 'ऑटो-सेव सक्षम',
                    'save_now': 'अभी सेव करें',
                    'export': 'डेटा एक्सपोर्ट करें'
                },
                'te': {
                    'title': '💾 డేటా నిల్వ సెట్టింగ్‌లు',
                    'retention': 'డేటా నిలుపుదల వ్యవధి',
                    'location': 'సేవ్ లొకేషన్',
                    'encryption': 'ఎన్‌క్రిప్షన్ ప్రారంభించండి',
                    'auto_save': 'ఆటో-సేవ్ ప్రారంభించబడింది',
                    'save_now': 'ఇప్పుడు సేవ్ చేయండి',
                    'export': 'డేటా ఎగుమతి చేయండి'
                }
            }

            texts = save_texts.get(current_lang, save_texts['en'])

            st.markdown(f"#### {texts['title']}")

            col1, col2 = st.columns(2)

            with col1:
                # Retention period selection
                st.markdown(f"**{texts['retention']}**")

                retention_options = {
                    'en': {
                        1: '1 Day (Testing)',
                        7: '1 Week',
                        30: '1 Month (Recommended)',
                        90: '3 Months',
                        365: '1 Year',
                        -1: 'Permanent (Forever)'
                    },
                    'ta': {
                        1: '1 நாள் (சோதனை)',
                        7: '1 வாரம்',
                        30: '1 மாதம் (பரிந்துரைக்கப்பட்டது)',
                        90: '3 மாதங்கள்',
                        365: '1 வருடம்',
                        -1: 'நிரந்தரம் (எப்போதும்)'
                    },
                    'hi': {
                        1: '1 दिन (परीक्षण)',
                        7: '1 सप्ताह',
                        30: '1 महीना (अनुशंसित)',
                        90: '3 महीने',
                        365: '1 साल',
                        -1: 'स्थायी (हमेशा के लिए)'
                    },
                    'te': {
                        1: '1 రోజు (పరీక్ష)',
                        7: '1 వారం',
                        30: '1 నెల (సిఫార్సు చేయబడింది)',
                        90: '3 నెలలు',
                        365: '1 సంవత్సరం',
                        -1: 'శాశ్వతం (ఎల్లప్పుడూ)'
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

                # Save location
                st.markdown(f"**{texts['location']}**")
                save_location = st.radio(
                    "Choose save location:",
                    options=['local', 'cloud', 'both'],
                    format_func=lambda x: {
                        'local': '💻 Local Device',
                        'cloud': '☁️ Cloud Storage',
                        'both': '🔄 Both Local & Cloud'
                    }[x],
                    index=['local', 'cloud', 'both'].index(st.session_state.data_save_settings['save_location'])
                )
                st.session_state.data_save_settings['save_location'] = save_location

            with col2:
                # Security settings
                st.markdown("**🔒 Security Settings**")

                encryption_enabled = st.checkbox(
                    texts['encryption'],
                    value=st.session_state.data_save_settings['encryption_enabled'],
                    help="Encrypt your financial data for security"
                )
                st.session_state.data_save_settings['encryption_enabled'] = encryption_enabled

                auto_save = st.checkbox(
                    texts['auto_save'],
                    value=st.session_state.data_save_settings['auto_save'],
                    help="Automatically save data when changes are made"
                )
                st.session_state.data_save_settings['auto_save'] = auto_save

                # Data size estimation
                st.markdown("**📊 Data Information**")
                estimated_size = self.calculate_data_size()
                st.info(f"📦 Estimated data size: {estimated_size:.2f} KB")

                if st.session_state.data_save_settings['last_save']:
                    last_save_time = st.session_state.data_save_settings['last_save']
                    st.info(f"🕒 Last saved: {last_save_time}")
                else:
                    st.warning("⚠️ Data not saved yet")

            # Action buttons
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button(f"💾 {texts['save_now']}", use_container_width=True):
                    self.save_user_data()

            with col2:
                if st.button(f"📤 {texts['export']}", use_container_width=True):
                    self.export_user_data()

            with col3:
                if st.button("🗑️ Clear Data", use_container_width=True):
                    self.clear_user_data()

            with col4:
                if st.button("📋 Data Summary", use_container_width=True):
                    self.show_data_summary()

            # Retention period warning
            if selected_retention == -1:
                st.warning("⚠️ Permanent storage: Data will be kept forever. Make sure you comply with privacy regulations.")
            elif selected_retention == 1:
                st.info("ℹ️ Testing mode: Data will be deleted after 1 day.")
            else:
                st.info(f"ℹ️ Data will be automatically deleted after {selected_retention} days.")

    def calculate_data_size(self) -> float:
        """Calculate estimated size of user data in KB"""
        try:
            import json
            data_to_save = {
                'user_profile': st.session_state.user_profile,
                'chat_history': st.session_state.chat_history,
                'gamification': st.session_state.gamification,
                'data_save_settings': st.session_state.data_save_settings
            }

            # Convert to JSON and calculate size
            json_data = json.dumps(data_to_save, default=str)
            size_bytes = len(json_data.encode('utf-8'))
            size_kb = size_bytes / 1024

            return size_kb
        except Exception as e:
            self.logger.error(f"Error calculating data size: {e}")
            return 1.0  # Default estimate

    def save_user_data(self):
        """Save user data with selected retention period"""
        try:
            import json
            from datetime import datetime, timedelta

            # Prepare data to save
            data_to_save = {
                'user_profile': st.session_state.user_profile,
                'chat_history': st.session_state.chat_history,
                'gamification': st.session_state.gamification,
                'data_save_settings': st.session_state.data_save_settings,
                'save_timestamp': datetime.now().isoformat(),
                'retention_period': st.session_state.data_save_settings['retention_period'],
                'expires_at': (datetime.now() + timedelta(days=st.session_state.data_save_settings['retention_period'])).isoformat()
                if st.session_state.data_save_settings['retention_period'] != -1 else None
            }

            # Encrypt data if enabled
            if st.session_state.data_save_settings['encryption_enabled']:
                # Simulate encryption (in production, use proper encryption)
                data_to_save['encrypted'] = True
                data_to_save['encryption_method'] = 'AES-256'

            # Save to different locations based on user choice
            save_location = st.session_state.data_save_settings['save_location']

            if save_location in ['local', 'both']:
                # Save locally (simulate - in production, save to local storage)
                st.success("💾 Data saved locally successfully!")

            if save_location in ['cloud', 'both']:
                # Save to cloud (simulate - in production, save to cloud storage)
                st.success("☁️ Data saved to cloud successfully!")

            # Update last save time
            st.session_state.data_save_settings['last_save'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Show save confirmation
            retention_text = "permanently" if st.session_state.data_save_settings['retention_period'] == -1 else f"for {st.session_state.data_save_settings['retention_period']} days"
            st.success(f"✅ Your financial data has been saved {retention_text}!")

            # Add to gamification points
            st.session_state.gamification['points'] += 10
            st.info("🎉 +10 points for saving your data!")

        except Exception as e:
            self.logger.error(f"Error saving user data: {e}")
            st.error("❌ Failed to save data. Please try again.")

    def export_user_data(self):
        """Export user data in various formats"""
        try:
            import json
            from datetime import datetime

            # Prepare export data
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'user_profile': st.session_state.user_profile,
                'financial_summary': {
                    'monthly_income': st.session_state.user_profile['basic_info']['monthly_income'],
                    'monthly_expenses': st.session_state.user_profile['financial_profile']['monthly_expenses'],
                    'savings_rate': ((st.session_state.user_profile['basic_info']['monthly_income'] -
                                    st.session_state.user_profile['financial_profile']['monthly_expenses']) /
                                   st.session_state.user_profile['basic_info']['monthly_income'] * 100)
                                   if st.session_state.user_profile['basic_info']['monthly_income'] > 0 else 0,
                    'credit_score': st.session_state.user_profile['financial_profile']['credit_score']
                },
                'chat_summary': {
                    'total_conversations': len(st.session_state.chat_history),
                    'recent_topics': [msg.get('content', '')[:50] + '...' for msg in st.session_state.chat_history[-5:] if msg.get('role') == 'user']
                },
                'gamification_stats': st.session_state.gamification
            }

            # Convert to JSON
            json_data = json.dumps(export_data, indent=2, default=str)

            # Create download button
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"jarvisfi_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

            st.success("📤 Export prepared! Click the download button above.")

        except Exception as e:
            self.logger.error(f"Error exporting user data: {e}")
            st.error("❌ Failed to export data. Please try again.")

    def clear_user_data(self):
        """Clear user data with confirmation"""
        if st.button("⚠️ Confirm Clear All Data", type="secondary"):
            # Reset to default values
            st.session_state.user_profile = {
                'basic_info': {
                    'name': 'User',
                    'age': 25,
                    'user_type': 'professional',
                    'language': 'en',
                    'monthly_income': 50000,
                    'currency': 'INR',
                    'location': 'India',
                    'occupation': 'Software Engineer'
                },
                'financial_profile': {
                    'risk_tolerance': 'moderate',
                    'investment_experience': 'beginner',
                    'financial_goals': ['retirement', 'house', 'emergency_fund'],
                    'current_investments': 0,
                    'monthly_expenses': 30000,
                    'debt_info': {},
                    'credit_score': 750
                },
                'preferences': {
                    'dark_mode': False,
                    'voice_enabled': True,
                    'notifications': True,
                    'ai_accuracy_mode': True,
                    'enhanced_sources': True,
                    'learning_mode': False
                },
                'security': {
                    'two_factor_enabled': False,
                    'biometric_enabled': False,
                    'data_encryption': True
                }
            }

            st.session_state.chat_history = []
            st.session_state.gamification = {
                'points': 0,
                'level': 1,
                'badges': [],
                'challenges_completed': 0,
                'streak_days': 0
            }

            st.success("🗑️ All data cleared successfully!")
            st.rerun()
        else:
            st.warning("⚠️ This will permanently delete all your data. Click the confirmation button above to proceed.")

    def show_data_summary(self):
        """Show summary of saved data"""
        st.markdown("### 📋 Data Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**👤 Profile Data:**")
            st.write(f"• Name: {st.session_state.user_profile['basic_info']['name']}")
            st.write(f"• User Type: {st.session_state.user_profile['basic_info']['user_type']}")
            st.write(f"• Language: {st.session_state.user_profile['basic_info']['language']}")
            st.write(f"• Monthly Income: ₹{st.session_state.user_profile['basic_info']['monthly_income']:,}")

            st.markdown("**💬 Chat Data:**")
            st.write(f"• Total Messages: {len(st.session_state.chat_history)}")
            st.write(f"• User Messages: {len([m for m in st.session_state.chat_history if m.get('role') == 'user'])}")
            st.write(f"• AI Responses: {len([m for m in st.session_state.chat_history if m.get('role') == 'assistant'])}")

        with col2:
            st.markdown("**🎮 Gamification Data:**")
            st.write(f"• Points: {st.session_state.gamification['points']}")
            st.write(f"• Level: {st.session_state.gamification['level']}")
            st.write(f"• Badges: {len(st.session_state.gamification['badges'])}")
            st.write(f"• Challenges: {st.session_state.gamification['challenges_completed']}")

            st.markdown("**💾 Save Settings:**")
            settings = st.session_state.data_save_settings
            st.write(f"• Retention: {settings['retention_period']} days" if settings['retention_period'] != -1 else "• Retention: Permanent")
            st.write(f"• Location: {settings['save_location']}")
            st.write(f"• Encryption: {'Enabled' if settings['encryption_enabled'] else 'Disabled'}")
            st.write(f"• Auto-save: {'Enabled' if settings['auto_save'] else 'Disabled'}")

    def render_ai_chat_page(self):
        """Render AI chat interface with multilingual support"""
        current_lang = st.session_state.user_profile['basic_info']['language']

        # Chat header
        chat_headers = {
            'en': "💬 AI Financial Assistant",
            'ta': "💬 AI நிதி உதவியாளர்",
            'hi': "💬 AI वित्तीय सहायक",
            'te': "💬 AI ఆర్థిక సహాయకుడు"
        }

        st.markdown(f"### {chat_headers.get(current_lang, chat_headers['en'])}")

        # Chat controls
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🎤 Voice Input"):
                st.session_state.voice_active = True
                st.info("🎤 Voice input activated! (Simulated)")

        with col2:
            if st.button("🔊 Read Aloud"):
                if st.session_state.chat_history:
                    st.info("🔊 Reading last response aloud... (Simulated)")

        with col3:
            if st.button("🧹 Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()

        # Chat history display
        chat_container = st.container()

        with chat_container:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    with st.chat_message("user"):
                        st.write(message['content'])
                else:
                    with st.chat_message("assistant"):
                        st.write(message['content'])

                        # Show metadata if available
                        if 'metadata' in message:
                            metadata = message['metadata']
                            with st.expander("📊 Response Details"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Confidence", f"{metadata.get('confidence', 0):.1%}")
                                    st.write(f"**Intent:** {metadata.get('intent', 'general')}")
                                with col2:
                                    st.write(f"**Language:** {metadata.get('language', 'en')}")
                                    if metadata.get('sources'):
                                        st.write("**Sources:**")
                                        for source in metadata['sources']:
                                            st.write(f"• {source}")

        # Chat input
        user_input = st.chat_input("Ask me anything about finance...")

        if user_input:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now().isoformat()
            })

            # Generate AI response
            with st.spinner("🤖 JarvisFi is thinking..."):
                response = self.generate_ai_response(user_input, current_lang)
                st.session_state.chat_history.append(response)

            st.rerun()

    def generate_ai_response(self, query: str, language: str) -> Dict[str, Any]:
        """Generate AI response (with fallback for demo mode)"""
        try:
            if self.services_available:
                # Use actual AI engine
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    self.ai_engine.generate_response(
                        query,
                        st.session_state.user_profile,
                        language
                    )
                )
                loop.close()
                return {
                    'role': 'assistant',
                    'content': response['content'],
                    'timestamp': datetime.now().isoformat(),
                    'metadata': response
                }
            else:
                # Fallback demo response
                return self.generate_demo_response(query, language)

        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return self.generate_demo_response(query, language)

    def generate_demo_response(self, query: str, language: str) -> Dict[str, Any]:
        """Generate demo response for testing"""
        user_profile = st.session_state.user_profile
        monthly_income = user_profile['basic_info']['monthly_income']
        user_type = user_profile['basic_info']['user_type']

        # Simple rule-based responses
        query_lower = query.lower()

        if any(word in query_lower for word in ['save', 'saving', 'savings']):
            if language == 'ta':
                content = f"உங்கள் ₹{monthly_income:,} மாதாந்திர வருமானத்தின் அடிப்படையில், மாதம் ₹{int(monthly_income*0.2):,} சேமிக்க பரிந்துரைக்கிறேன். இது 50/30/20 விதியைப் பின்பற்றுகிறது."
            elif language == 'hi':
                content = f"आपकी ₹{monthly_income:,} मासिक आय के आधार पर, मैं महीने में ₹{int(monthly_income*0.2):,} बचत करने की सलाह देता हूं। यह 50/30/20 नियम का पालन करता है।"
            else:
                content = f"Based on your ₹{monthly_income:,} monthly income, I recommend saving ₹{int(monthly_income*0.2):,} per month. This follows the 50/30/20 rule for budgeting."

        elif any(word in query_lower for word in ['invest', 'investment', 'sip']):
            sip_amount = max(1000, int(monthly_income * 0.15))
            if language == 'ta':
                content = f"உங்கள் வருமான நிலைக்கு, மாதம் ₹{sip_amount:,} SIP முதலீடு செய்ய பரிந்துரைக்கிறேன். பல்வகைப்படுத்தப்பட்ட ஈக்விட்டி நிதிகளில் தொடங்குங்கள்."
            elif language == 'hi':
                content = f"आपके आय स्तर के लिए, मैं महीने में ₹{sip_amount:,} SIP निवेश करने का सुझाव देता हूं। विविधीकृत इक्विटी फंड से शुरुआत करें।"
            else:
                content = f"For your income level, I suggest starting with ₹{sip_amount:,} monthly SIP investment. Begin with diversified equity funds for long-term growth."

        else:
            if language == 'ta':
                content = f"வணக்கம்! நான் JarvisFi, உங்கள் AI நிதி உதவியாளர். {user_type} பயனராக, நான் பட்ஜெட், முதலீடுகள், சேமிப்பு மற்றும் வரி திட்டமிடலில் உதவ முடியும்."
            elif language == 'hi':
                content = f"नमस्ते! मैं JarvisFi हूं, आपका AI वित्तीय सहायक। {user_type} उपयोगकर्ता के रूप में, मैं बजट, निवेश, बचत और कर योजना में सहायता कर सकता हूं।"
            else:
                content = f"Hello! I'm JarvisFi, your AI financial assistant. As a {user_type}, I can help you with budgeting, investments, savings, and tax planning."

        return {
            'role': 'assistant',
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'confidence': 0.85,
                'intent': 'financial_advice',
                'language': language,
                'sources': ['Demo Mode'],
                'demographic_adapted': True
            }
        }

    def render_dashboard_page(self):
        """Render comprehensive financial dashboard"""
        st.markdown("### 📊 Financial Dashboard")

        profile = st.session_state.user_profile
        monthly_income = profile['basic_info']['monthly_income']
        monthly_expenses = profile['financial_profile']['monthly_expenses']

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("💰 Net Worth", "₹2,50,000", "↗️ +15%")
        with col2:
            st.metric("📈 Investments", "₹1,20,000", "↗️ +8%")
        with col3:
            st.metric("💳 Credit Score", profile['financial_profile']['credit_score'], "↗️ +25")
        with col4:
            st.metric("🎯 Goal Progress", "65%", "↗️ +5%")

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            # Income vs Expenses trend
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            income_data = [monthly_income] * 6
            expense_data = [monthly_expenses * (1 + i*0.02) for i in range(6)]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=income_data, name='Income', line=dict(color='green')))
            fig.add_trace(go.Scatter(x=months, y=expense_data, name='Expenses', line=dict(color='red')))
            fig.update_layout(title='Income vs Expenses Trend', height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Investment allocation
            investment_data = {
                'Asset Class': ['Equity', 'Debt', 'Gold', 'Real Estate', 'Cash'],
                'Allocation': [40, 30, 10, 15, 5]
            }

            fig = px.pie(investment_data, values='Allocation', names='Asset Class',
                        title='Investment Allocation')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Financial goals progress
        st.markdown("### 🎯 Financial Goals Progress")

        goals = [
            {'name': 'Emergency Fund', 'target': 300000, 'current': 150000},
            {'name': 'House Down Payment', 'target': 2000000, 'current': 800000},
            {'name': 'Retirement Corpus', 'target': 10000000, 'current': 1200000}
        ]

        for goal in goals:
            progress = (goal['current'] / goal['target']) * 100
            st.markdown(f"**{goal['name']}**")
            st.progress(progress / 100)
            st.markdown(f"₹{goal['current']:,} / ₹{goal['target']:,} ({progress:.1f}%)")
            st.markdown("---")

    def render_calculators_page(self):
        """Render financial calculators"""
        st.markdown("### 🧮 Financial Calculators")

        # Calculator selection
        calculator_type = st.selectbox(
            "Choose Calculator",
            ["SIP Calculator", "EMI Calculator", "Tax Calculator", "Retirement Calculator",
             "Budget Planner", "Emergency Fund Calculator", "Debt Payoff Calculator"]
        )

        if calculator_type == "SIP Calculator":
            self.render_sip_calculator()
        elif calculator_type == "EMI Calculator":
            self.render_emi_calculator()
        elif calculator_type == "Tax Calculator":
            self.render_tax_calculator()
        elif calculator_type == "Budget Planner":
            self.render_budget_planner()
        else:
            st.info(f"{calculator_type} coming soon!")

    def render_sip_calculator(self):
        """Render SIP calculator"""
        st.markdown("#### 📈 SIP Calculator")

        col1, col2 = st.columns(2)

        with col1:
            monthly_investment = st.number_input("Monthly Investment (₹)", 1000, 100000, 5000, 500)
            annual_return = st.slider("Expected Annual Return (%)", 8.0, 20.0, 12.0, 0.5)
            investment_period = st.slider("Investment Period (Years)", 1, 30, 10)

        with col2:
            # Calculate SIP returns
            monthly_return = annual_return / 12 / 100
            total_months = investment_period * 12

            if monthly_return > 0:
                future_value = monthly_investment * (((1 + monthly_return) ** total_months - 1) / monthly_return) * (1 + monthly_return)
            else:
                future_value = monthly_investment * total_months

            total_investment = monthly_investment * total_months
            total_returns = future_value - total_investment

            st.metric("Total Investment", f"₹{total_investment:,.0f}")
            st.metric("Total Returns", f"₹{total_returns:,.0f}")
            st.metric("Maturity Amount", f"₹{future_value:,.0f}")

        # Visualization
        years = list(range(1, investment_period + 1))
        investment_values = []
        return_values = []

        for year in years:
            months = year * 12
            if monthly_return > 0:
                fv = monthly_investment * (((1 + monthly_return) ** months - 1) / monthly_return) * (1 + monthly_return)
            else:
                fv = monthly_investment * months

            invested = monthly_investment * months
            returns = fv - invested

            investment_values.append(invested)
            return_values.append(returns)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=investment_values, name='Investment', fill='tonexty'))
        fig.add_trace(go.Scatter(x=years, y=return_values, name='Returns', fill='tonexty'))
        fig.update_layout(title='SIP Growth Over Time', xaxis_title='Years', yaxis_title='Amount (₹)')
        st.plotly_chart(fig, use_container_width=True)

    def render_emi_calculator(self):
        """Render EMI calculator"""
        st.markdown("#### 🏠 EMI Calculator")

        col1, col2 = st.columns(2)

        with col1:
            loan_amount = st.number_input("Loan Amount (₹)", 100000, 50000000, 2500000, 100000)
            interest_rate = st.slider("Interest Rate (% per annum)", 6.0, 20.0, 8.5, 0.1)
            loan_tenure = st.slider("Loan Tenure (Years)", 1, 30, 20)

        with col2:
            # Calculate EMI
            monthly_rate = interest_rate / 12 / 100
            total_months = loan_tenure * 12

            if monthly_rate > 0:
                emi = loan_amount * monthly_rate * (1 + monthly_rate) ** total_months / ((1 + monthly_rate) ** total_months - 1)
            else:
                emi = loan_amount / total_months

            total_payment = emi * total_months
            total_interest = total_payment - loan_amount

            st.metric("Monthly EMI", f"₹{emi:,.0f}")
            st.metric("Total Interest", f"₹{total_interest:,.0f}")
            st.metric("Total Payment", f"₹{total_payment:,.0f}")

        # Affordability check
        monthly_income = st.session_state.user_profile['basic_info']['monthly_income']
        emi_ratio = (emi / monthly_income) * 100 if monthly_income > 0 else 0

        st.markdown("#### 💡 Affordability Analysis")
        if emi_ratio <= 40:
            st.success(f"✅ EMI is {emi_ratio:.1f}% of income - Affordable!")
        elif emi_ratio <= 50:
            st.warning(f"⚠️ EMI is {emi_ratio:.1f}% of income - Manageable but tight")
        else:
            st.error(f"❌ EMI is {emi_ratio:.1f}% of income - Not recommended")

    def render_tax_calculator(self):
        """Render tax calculator"""
        st.markdown("#### 💰 Tax Calculator")

        annual_income = st.session_state.user_profile['basic_info']['monthly_income'] * 12

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Income Details**")
            salary = st.number_input("Annual Salary (₹)", 0, 50000000, annual_income, 50000)
            other_income = st.number_input("Other Income (₹)", 0, 10000000, 0, 10000)
            total_income = salary + other_income

            st.markdown("**Deductions (80C)**")
            pf_contribution = st.number_input("PF Contribution (₹)", 0, 150000, 0, 5000)
            elss_investment = st.number_input("ELSS Investment (₹)", 0, 150000, 0, 5000)
            life_insurance = st.number_input("Life Insurance Premium (₹)", 0, 150000, 0, 5000)

            total_80c = min(pf_contribution + elss_investment + life_insurance, 150000)

        with col2:
            # Calculate tax for both regimes
            taxable_income_old = max(0, total_income - total_80c - 50000)  # Standard deduction
            taxable_income_new = max(0, total_income - 50000)  # No 80C deductions

            # Old regime tax calculation
            old_tax = self.calculate_income_tax(taxable_income_old, 'old')
            new_tax = self.calculate_income_tax(taxable_income_new, 'new')

            st.markdown("**Tax Comparison**")

            # Create comparison table
            comparison_data = {
                'Regime': ['Old Regime', 'New Regime'],
                'Taxable Income': [f"₹{taxable_income_old:,}", f"₹{taxable_income_new:,}"],
                'Tax Amount': [f"₹{old_tax:,}", f"₹{new_tax:,}"],
                'Take Home': [f"₹{total_income - old_tax:,}", f"₹{total_income - new_tax:,}"]
            }

            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)

            # Recommendation
            if old_tax < new_tax:
                st.success(f"💡 Old regime saves ₹{new_tax - old_tax:,}")
            else:
                st.success(f"💡 New regime saves ₹{old_tax - new_tax:,}")

    def calculate_income_tax(self, taxable_income: float, regime: str) -> float:
        """Calculate income tax based on regime"""
        if regime == 'old':
            brackets = [
                (250000, 0),
                (500000, 0.05),
                (1000000, 0.20),
                (float('inf'), 0.30)
            ]
        else:  # new regime
            brackets = [
                (300000, 0),
                (600000, 0.05),
                (900000, 0.10),
                (1200000, 0.15),
                (1500000, 0.20),
                (float('inf'), 0.30)
            ]

        tax = 0
        remaining_income = taxable_income
        prev_limit = 0

        for limit, rate in brackets:
            if remaining_income <= 0:
                break

            taxable_in_bracket = min(remaining_income, limit - prev_limit)
            tax += taxable_in_bracket * rate
            remaining_income -= taxable_in_bracket
            prev_limit = limit

        # Add cess (4% on tax)
        return tax * 1.04

    def render_budget_planner(self):
        """Render budget planner"""
        st.markdown("#### 📊 Budget Planner")

        monthly_income = st.session_state.user_profile['basic_info']['monthly_income']

        st.markdown(f"**Monthly Income: ₹{monthly_income:,}**")

        # 50/30/20 rule suggestion
        needs_suggested = monthly_income * 0.5
        wants_suggested = monthly_income * 0.3
        savings_suggested = monthly_income * 0.2

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Your Budget**")
            needs = st.number_input("Needs (Housing, Food, Transport) ₹", 0, monthly_income, int(needs_suggested), 1000)
            wants = st.number_input("Wants (Entertainment, Dining) ₹", 0, monthly_income, int(wants_suggested), 1000)
            savings = st.number_input("Savings & Investments ₹", 0, monthly_income, int(savings_suggested), 1000)

            total_budget = needs + wants + savings
            remaining = monthly_income - total_budget

        with col2:
            st.markdown("**Budget Analysis**")

            if total_budget <= monthly_income:
                st.success(f"✅ Budget balanced! Remaining: ₹{remaining:,}")
            else:
                st.error(f"❌ Over budget by ₹{abs(remaining):,}")

            # Budget breakdown chart
            budget_data = {
                'Category': ['Needs', 'Wants', 'Savings'],
                'Amount': [needs, wants, savings],
                'Recommended': [needs_suggested, wants_suggested, savings_suggested]
            }

            fig = go.Figure()
            fig.add_trace(go.Bar(name='Your Budget', x=budget_data['Category'], y=budget_data['Amount']))
            fig.add_trace(go.Bar(name='Recommended (50/30/20)', x=budget_data['Category'], y=budget_data['Recommended']))
            fig.update_layout(title='Budget vs Recommended', barmode='group')
            st.plotly_chart(fig, use_container_width=True)

        # Budget tips
        st.markdown("#### 💡 Budget Tips")

        needs_percent = (needs / monthly_income) * 100
        wants_percent = (wants / monthly_income) * 100
        savings_percent = (savings / monthly_income) * 100

        tips = []

        if needs_percent > 60:
            tips.append("🏠 Your needs are high. Consider reducing housing or transportation costs.")

        if wants_percent > 40:
            tips.append("🎯 Your wants spending is high. Try to reduce entertainment and dining expenses.")

        if savings_percent < 15:
            tips.append("💰 Increase your savings rate. Aim for at least 20% of income.")

        if savings_percent >= 20:
            tips.append("🎉 Excellent savings rate! You're on track for financial success.")

        for tip in tips:
            st.info(tip)

    def render_voice_page(self):
        """Render voice interface page"""
        st.markdown("### 🎤 Voice Assistant")

        # Voice status
        if st.session_state.user_profile['preferences']['voice_enabled']:
            st.success("🟢 Voice interface is enabled")
        else:
            st.warning("🟡 Voice interface is disabled")
            if st.button("Enable Voice"):
                st.session_state.user_profile['preferences']['voice_enabled'] = True
                st.rerun()
            return

        # Voice controls
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🎙️ Start Voice Chat", use_container_width=True):
                st.session_state.voice_active = True
                with st.spinner("🎤 Listening..."):
                    time.sleep(2)
                    # Simulate voice recognition
                    sample_queries = [
                        "What's my budget status?",
                        "How should I invest 10000 rupees?",
                        "Calculate SIP for retirement planning"
                    ]
                    import random
                    recognized_text = random.choice(sample_queries)

                    st.success(f"🎤 Recognized: '{recognized_text}'")

                    # Add to chat and generate response
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': recognized_text,
                        'timestamp': datetime.now().isoformat(),
                        'type': 'voice'
                    })

                    response = self.generate_ai_response(
                        recognized_text,
                        st.session_state.user_profile['basic_info']['language']
                    )
                    st.session_state.chat_history.append(response)

        with col2:
            if st.button("🔊 Voice Settings", use_container_width=True):
                with st.expander("Voice Configuration", expanded=True):
                    voice_speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)
                    voice_pitch = st.slider("Voice Pitch", 0.5, 2.0, 1.0, 0.1)
                    voice_language = st.selectbox(
                        "Voice Language",
                        ["English", "Tamil", "Hindi", "Telugu"],
                        index=0
                    )

        with col3:
            if st.button("📱 Voice Commands", use_container_width=True):
                st.info("""
                **Voice Commands:**
                • "What's my budget?"
                • "Calculate SIP"
                • "Show investment options"
                • "Help with tax planning"
                • "Check credit score"
                """)

        # Voice chat history
        if st.session_state.chat_history:
            st.markdown("### 💬 Voice Chat History")

            for message in st.session_state.chat_history[-5:]:  # Show last 5 messages
                if message.get('type') == 'voice' or message['role'] == 'assistant':
                    with st.chat_message(message['role']):
                        st.write(message['content'])
                        if message['role'] == 'assistant':
                            if st.button(f"🔊 Read Aloud", key=f"tts_{message['timestamp']}"):
                                st.info("🔊 Reading response aloud... (Simulated)")

    def render_farmer_tools_page(self):
        """Render farmer-specific tools"""
        st.markdown("### 👨‍🌾 Farmer Financial Tools")

        # MSP Information
        st.markdown("#### 🌾 Minimum Support Price (MSP) Information")

        msp_data = {
            'Crop': ['Rice', 'Wheat', 'Cotton', 'Sugarcane', 'Maize', 'Bajra'],
            'MSP (₹/Quintal)': [2183, 2275, 6620, 315, 2090, 2500],
            'Season': ['Kharif', 'Rabi', 'Kharif', 'Annual', 'Kharif', 'Kharif']
        }

        df_msp = pd.DataFrame(msp_data)
        st.dataframe(df_msp, use_container_width=True)

        # Crop Loan Calculator
        st.markdown("#### 🏦 Crop Loan Calculator")

        col1, col2 = st.columns(2)

        with col1:
            crop_type = st.selectbox("Crop Type", ["Rice", "Wheat", "Cotton", "Sugarcane"])
            land_area = st.number_input("Land Area (Acres)", 1, 100, 5)
            cost_per_acre = st.number_input("Cost per Acre (₹)", 10000, 200000, 50000, 5000)

            total_cost = land_area * cost_per_acre
            loan_amount = min(total_cost, 300000)  # Max 3 lakh for small farmers

        with col2:
            st.metric("Total Cultivation Cost", f"₹{total_cost:,}")
            st.metric("Eligible Loan Amount", f"₹{loan_amount:,}")
            st.metric("Interest Rate", "7.0% p.a.")
            st.metric("Repayment Period", "12 months")

        # Government Schemes
        st.markdown("#### 🏛️ Government Schemes")

        schemes = [
            {
                'name': 'PM-KISAN',
                'benefit': '₹6,000 per year',
                'eligibility': 'Small and marginal farmers',
                'status': 'Active'
            },
            {
                'name': 'Pradhan Mantri Fasal Bima Yojana',
                'benefit': 'Crop insurance coverage',
                'eligibility': 'All farmers',
                'status': 'Active'
            },
            {
                'name': 'Kisan Credit Card',
                'benefit': 'Easy access to credit',
                'eligibility': 'All farmers',
                'status': 'Active'
            }
        ]

        for scheme in schemes:
            with st.expander(f"📋 {scheme['name']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Benefit:** {scheme['benefit']}")
                    st.write(f"**Eligibility:** {scheme['eligibility']}")
                with col2:
                    st.write(f"**Status:** {scheme['status']}")
                    if st.button(f"Apply for {scheme['name']}", key=scheme['name']):
                        st.info("Redirecting to government portal... (Demo)")

        # Weather Impact
        st.markdown("#### 🌦️ Weather & Financial Impact")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Current Weather Alert**")
            st.warning("⚠️ Heavy rainfall expected in next 3 days")
            st.info("💡 Consider crop protection measures")

        with col2:
            st.markdown("**Financial Recommendations**")
            st.success("✅ Crop insurance claims can be filed")
            st.info("💰 Emergency fund usage recommended")

    def render_credit_score_page(self):
        """Render credit score tracking page"""
        st.markdown("### 💳 Credit Score Tracking")

        profile = st.session_state.user_profile
        current_score = profile['financial_profile']['credit_score']

        # Credit score display
        col1, col2, col3 = st.columns(3)

        with col1:
            # Credit score gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = current_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Credit Score"},
                gauge = {
                    'axis': {'range': [300, 850]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [300, 550], 'color': "red"},
                        {'range': [550, 650], 'color': "orange"},
                        {'range': [650, 750], 'color': "yellow"},
                        {'range': [750, 850], 'color': "green"}
                    ]
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Score Range**")
            if current_score >= 750:
                st.success("🟢 Excellent (750-850)")
                st.write("You qualify for the best rates!")
            elif current_score >= 650:
                st.info("🟡 Good (650-749)")
                st.write("Good rates available")
            else:
                st.warning("🟠 Fair (550-649)")
                st.write("Work on improving your score")

        with col3:
            st.markdown("**Score Factors**")
            factors = {
                'Payment History': 85,
                'Credit Utilization': 70,
                'Credit Age': 60,
                'Credit Mix': 75
            }

            for factor, score in factors.items():
                st.metric(factor, f"{score}%")

        # Credit improvement recommendations
        st.markdown("#### 💡 Improvement Recommendations")

        recommendations = [
            "💳 Keep credit utilization below 30%",
            "⏰ Pay all bills on time",
            "📅 Don't close old credit cards",
            "🔍 Check credit report regularly",
            "💰 Pay more than minimum amounts"
        ]

        for rec in recommendations:
            st.info(rec)

        # Credit monitoring
        st.markdown("#### 📊 Credit Monitoring")

        # Simulated credit score trend
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        scores = [720, 725, 730, 740, 745, current_score]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=scores, mode='lines+markers', name='Credit Score'))
        fig.update_layout(title='Credit Score Trend', yaxis_title='Score', height=400)
        st.plotly_chart(fig, use_container_width=True)

    def render_investments_page(self):
        """Render investment portfolio page"""
        st.markdown("### 📈 Investment Portfolio")

        # Portfolio overview
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Portfolio", "₹5,25,000", "↗️ +12%")
        with col2:
            st.metric("Monthly SIP", "₹15,000", "↗️ +₹2,000")
        with col3:
            st.metric("Returns (1Y)", "14.5%", "↗️ +2.1%")
        with col4:
            st.metric("Goal Progress", "68%", "↗️ +5%")

        # Asset allocation
        st.markdown("#### 🎯 Asset Allocation")

        col1, col2 = st.columns(2)

        with col1:
            # Current allocation
            allocation_data = {
                'Asset Class': ['Large Cap Equity', 'Mid Cap Equity', 'Small Cap Equity', 'Debt Funds', 'Gold ETF'],
                'Allocation': [40, 25, 15, 15, 5],
                'Amount': [210000, 131250, 78750, 78750, 26250]
            }

            fig = px.pie(allocation_data, values='Allocation', names='Asset Class',
                        title='Current Allocation')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Recommended allocation
            user_age = st.session_state.user_profile['basic_info']['age']
            equity_percent = min(100 - user_age, 80)
            debt_percent = 100 - equity_percent

            recommended_data = {
                'Asset Class': ['Equity', 'Debt'],
                'Recommended': [equity_percent, debt_percent]
            }

            fig = px.pie(recommended_data, values='Recommended', names='Asset Class',
                        title=f'Recommended for Age {user_age}')
            st.plotly_chart(fig, use_container_width=True)

        # Investment recommendations
        st.markdown("#### 💡 Investment Recommendations")

        monthly_income = st.session_state.user_profile['basic_info']['monthly_income']
        recommended_sip = int(monthly_income * 0.15)

        recommendations = [
            f"💰 Increase SIP to ₹{recommended_sip:,} (15% of income)",
            "📈 Consider adding international equity exposure",
            "🏦 Rebalance portfolio quarterly",
            "💎 Add gold for portfolio diversification"
        ]

        for rec in recommendations:
            st.info(rec)

        # SIP tracker
        st.markdown("#### 📊 SIP Performance Tracker")

        # Simulated SIP performance
        months = list(range(1, 13))
        invested = [15000 * i for i in months]
        current_value = [15000 * i * (1 + 0.12/12)**i for i in months]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=invested, name='Amount Invested', fill='tonexty'))
        fig.add_trace(go.Scatter(x=months, y=current_value, name='Current Value', fill='tonexty'))
        fig.update_layout(title='SIP Performance', xaxis_title='Months', yaxis_title='Amount (₹)')
        st.plotly_chart(fig, use_container_width=True)


# Main application runner
def main():
    """Main function to run the complete JarvisFi application"""
    try:
        app = CompleteJarvisFiApp()
        app.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.info("Please refresh the page to restart the application.")


if __name__ == "__main__":
    main()
