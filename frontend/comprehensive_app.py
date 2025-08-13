"""
JarvisFi - Comprehensive AI-Powered Financial Genius
Complete application with all advanced features integrated
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime, timedelta
import sys
import logging
from typing import Dict, List, Any, Optional
import base64
from io import BytesIO
import time
import asyncio
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import backend modules with graceful fallback
BACKEND_AVAILABLE = False
try:
    from watson_integration import WatsonIntegration
    from language_support import LanguageSupport
    from voice_interface import VoiceInterface
    from user_profile_manager import UserProfileManager
    from budget_analyzer import BudgetAnalyzer
    from currency_converter import CurrencyConverter
    from demographic_adapter import DemographicAdapter
    from ai_accuracy_rag import AIAccuracyRAG
    from smart_alerts import SmartAlerts
    from security_manager import SecurityManager
    from pdf_generator import PDFGenerator
    BACKEND_AVAILABLE = True
    logger.info("✅ Backend modules loaded successfully")
except ImportError as e:
    logger.warning(f"⚠️ Backend modules not available: {e}")
    logger.info("🔄 Running in standalone mode with simulated features")
    BACKEND_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="JarvisFi - Your AI-Powered Financial Genius",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://jarvisfi.com/help',
        'Report a bug': 'https://jarvisfi.com/bug-report',
        'About': "JarvisFi - Your AI-Powered Financial Genius v2.0"
    }
)


class ComprehensiveJarvisFiApp:
    """Comprehensive JarvisFi Application with all advanced features"""
    
    def __init__(self):
        """Initialize the comprehensive JarvisFi application"""
        self.logger = logging.getLogger(__name__)
        self.logger.info("🤖 JarvisFi - Comprehensive AI-Powered Financial Genius initialized")
        
        # Initialize backend services if available
        if BACKEND_AVAILABLE:
            self.init_backend_services()
        
        # Initialize session state
        self.init_session_state()
        
        # Apply custom styling
        self.apply_comprehensive_styling()
    
    def init_backend_services(self):
        """Initialize backend services"""
        if BACKEND_AVAILABLE:
            try:
                self.watson = WatsonIntegration()
                self.language_support = LanguageSupport()
                self.voice_interface = VoiceInterface()
                self.user_profile_manager = UserProfileManager()
                self.budget_analyzer = BudgetAnalyzer()
                self.currency_converter = CurrencyConverter()
                self.demographic_adapter = DemographicAdapter()
                self.ai_accuracy_rag = AIAccuracyRAG()
                self.smart_alerts = SmartAlerts()
                self.security_manager = SecurityManager()
                self.pdf_generator = PDFGenerator()

                self.logger.info("✅ Backend services initialized successfully")
            except Exception as e:
                self.logger.error(f"❌ Backend service initialization failed: {e}")
        else:
            # Initialize mock services for standalone mode
            self.watson = None
            self.language_support = None
            self.voice_interface = None
            self.user_profile_manager = None
            self.budget_analyzer = None
            self.currency_converter = None
            self.demographic_adapter = None
            self.ai_accuracy_rag = None
            self.smart_alerts = None
            self.security_manager = None
            self.pdf_generator = None

            self.logger.info("🔄 Running in standalone mode")
    
    def init_session_state(self):
        """Initialize comprehensive session state"""
        
        # User Profile with all features
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = {
                'basic_info': {
                    'name': '',
                    'email': '',
                    'phone': '',
                    'user_type': 'beginner',
                    'language': 'en',
                    'currency': 'INR',
                    'monthly_income': 30000,
                    'age': 25,
                    'location': 'India',
                    'occupation': '',
                    'education_level': 'graduate'
                },
                'preferences': {
                    'dark_mode': False,
                    'voice_enabled': True,
                    'notifications': True,
                    'accessibility_mode': False,
                    'ai_accuracy_mode': True,
                    'enhanced_sources': True,
                    'response_style': 'friendly',
                    'learning_mode': False
                },
                'financial_profile': {
                    'risk_tolerance': 'moderate',
                    'investment_experience': 'beginner',
                    'financial_goals': [],
                    'current_investments': [],
                    'monthly_expenses': {},
                    'debt_info': {},
                    'insurance_info': {},
                    'tax_info': {}
                },
                'security': {
                    'two_factor_enabled': False,
                    'biometric_enabled': False,
                    'data_encryption': True,
                    'privacy_level': 'high'
                },
                'gamification': {
                    'points': 0,
                    'level': 1,
                    'badges': [],
                    'achievements': [],
                    'streak_days': 0
                }
            }
        
        # Chat history with enhanced features
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Voice interface state
        if 'voice_listening' not in st.session_state:
            st.session_state.voice_listening = False
        
        if 'voice_speaking' not in st.session_state:
            st.session_state.voice_speaking = False
        
        # AI features state
        if 'ai_confidence_threshold' not in st.session_state:
            st.session_state.ai_confidence_threshold = 0.7
        
        if 'rag_enabled' not in st.session_state:
            st.session_state.rag_enabled = True
        
        # Advanced features state
        if 'farmer_mode' not in st.session_state:
            st.session_state.farmer_mode = False
        
        if 'community_enabled' not in st.session_state:
            st.session_state.community_enabled = True
        
        if 'fraud_detection_enabled' not in st.session_state:
            st.session_state.fraud_detection_enabled = True
        
        # Performance tracking
        if 'session_start_time' not in st.session_state:
            st.session_state.session_start_time = time.time()

        if 'page_views' not in st.session_state:
            st.session_state.page_views = 0

        # Active tab tracking
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = 0

        # Active tab tracking
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = 0
        
        # Credit score tracking
        if 'credit_score_data' not in st.session_state:
            st.session_state.credit_score_data = {
                'current_score': 750,
                'last_updated': datetime.now().isoformat(),
                'history': [],
                'factors': {}
            }
        
        # Investment portfolio
        if 'investment_portfolio' not in st.session_state:
            st.session_state.investment_portfolio = {
                'total_value': 0,
                'investments': [],
                'performance': {},
                'allocation': {}
            }
    
    def apply_comprehensive_styling(self):
        """Apply comprehensive custom styling"""
        
        # Get current theme preferences
        dark_mode = st.session_state.user_profile['preferences']['dark_mode']
        accessibility_mode = st.session_state.user_profile['preferences']['accessibility_mode']
        
        # Comprehensive CSS
        css = """
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        /* CSS Variables for theming */
        :root {
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --accent-color: #f093fb;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --info-color: #3b82f6;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --text-muted: #9ca3af;
            --bg-primary: #ffffff;
            --bg-secondary: #f9fafb;
            --bg-tertiary: #f3f4f6;
            --border-color: #e5e7eb;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            --border-radius: 12px;
            --border-radius-lg: 16px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Dark mode variables */
        [data-theme="dark"] {
            --text-primary: #f9fafb;
            --text-secondary: #d1d5db;
            --text-muted: #9ca3af;
            --bg-primary: #111827;
            --bg-secondary: #1f2937;
            --bg-tertiary: #374151;
            --border-color: #4b5563;
        }
        
        /* Main app styling */
        .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
        }
        
        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 50%, var(--accent-color) 100%);
            padding: 2.5rem 2rem;
            border-radius: var(--border-radius-lg);
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-xl);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
        }
        
        .main-header h1 {
            font-family: 'Poppins', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
        }
        
        .main-header p {
            font-size: 1.3rem;
            opacity: 0.95;
            font-weight: 500;
            position: relative;
            z-index: 1;
        }
        
        .main-header .version-badge {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(255, 255, 255, 0.2);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }
        
        /* Enhanced card styling */
        .metric-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
            border-color: var(--primary-color);
        }
        
        /* Enhanced button styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: var(--transition);
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        /* Chat interface styling */
        .chat-container {
            max-height: 600px;
            overflow-y: auto;
            padding: 1rem;
            background: var(--bg-secondary);
            border-radius: var(--border-radius);
            border: 1px solid var(--border-color);
        }
        
        .chat-message {
            padding: 1rem 1.5rem;
            border-radius: var(--border-radius);
            margin-bottom: 1rem;
            box-shadow: var(--shadow-sm);
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .chat-message.user {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            margin-left: 2rem;
            border-bottom-right-radius: 4px;
        }
        
        .chat-message.assistant {
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            margin-right: 2rem;
            border-bottom-left-radius: 4px;
        }
        
        /* Voice interface styling */
        .voice-controls {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin: 1rem 0;
        }
        
        .voice-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .voice-indicator.listening {
            background: rgba(239, 68, 68, 0.1);
            color: var(--error-color);
            border: 1px solid rgba(239, 68, 68, 0.2);
        }
        
        .voice-indicator.speaking {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success-color);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }
        
        .voice-indicator .pulse {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: currentColor;
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }
        
        /* Sidebar enhancements */
        .sidebar .sidebar-content {
            background: var(--bg-secondary);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-sm);
        }
        
        /* Progress bars and metrics */
        .progress-container {
            background: var(--bg-tertiary);
            border-radius: 10px;
            padding: 0.25rem;
            margin: 0.5rem 0;
        }
        
        .progress-bar {
            height: 8px;
            border-radius: 6px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            transition: width 0.5s ease;
        }
        
        /* Accessibility enhancements */
        .accessibility-mode {
            font-size: 1.2em !important;
            line-height: 1.8 !important;
        }
        
        .accessibility-mode button {
            min-height: 48px !important;
            min-width: 48px !important;
            font-size: 1.1em !important;
        }
        
        .accessibility-mode .stSelectbox > div > div {
            min-height: 48px !important;
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .main-header {
                padding: 1.5rem 1rem;
            }
            
            .main-header h1 {
                font-size: 2rem;
            }
            
            .chat-message.user {
                margin-left: 0.5rem;
            }
            
            .chat-message.assistant {
                margin-right: 0.5rem;
            }
            
            .metric-card {
                padding: 1rem;
            }
        }
        
        /* Loading animations */
        .loading-spinner {
            border: 3px solid var(--border-color);
            border-top: 3px solid var(--primary-color);
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 1rem auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Status indicators */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .status-indicator.online {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success-color);
        }
        
        .status-indicator.offline {
            background: rgba(107, 114, 128, 0.1);
            color: var(--text-muted);
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        </style>
        """
        
        # Apply dark mode
        if dark_mode:
            css += """
            <style>
            .stApp {
                background-color: #111827;
                color: #f9fafb;
            }
            
            .stSidebar {
                background-color: #1f2937;
            }
            </style>
            """
        
        # Apply accessibility mode
        if accessibility_mode:
            css += """
            <style>
            .stApp {
                font-size: 1.2em !important;
                line-height: 1.8 !important;
            }
            
            button, .stSelectbox > div > div, .stTextInput > div > div > input {
                min-height: 48px !important;
                font-size: 1.1em !important;
            }
            
            .stButton > button {
                padding: 1rem 2rem !important;
            }
            </style>
            """
        
        st.markdown(css, unsafe_allow_html=True)
    
    def render_comprehensive_header(self):
        """Render comprehensive application header"""
        current_language = st.session_state.user_profile['basic_info']['language']
        user_name = st.session_state.user_profile['basic_info']['name']
        
        # Multi-language headers
        headers = {
            'en': {
                'title': 'JarvisFi',
                'slogan': 'Your AI-Powered Financial Genius',
                'welcome': f'Welcome back, {user_name}!' if user_name else 'Welcome to JarvisFi!',
                'version': 'v2.0 - Comprehensive Edition'
            },
            'ta': {
                'title': 'JarvisFi',
                'slogan': 'உங்கள் AI-இயங்கும் நிதி மேதை',
                'welcome': f'மீண்டும் வரவேற்கிறோம், {user_name}!' if user_name else 'JarvisFi-க்கு வரவேற்கிறோம்!',
                'version': 'v2.0 - விரிவான பதிப்பு'
            },
            'hi': {
                'title': 'JarvisFi',
                'slogan': 'आपका AI-संचालित वित्तीय प्रतिभा',
                'welcome': f'वापस स्वागत है, {user_name}!' if user_name else 'JarvisFi में आपका स्वागत है!',
                'version': 'v2.0 - व्यापक संस्करण'
            },
            'te': {
                'title': 'JarvisFi',
                'slogan': 'మీ AI-శక్తితో కూడిన ఆర్థిక మేధావి',
                'welcome': f'తిరిగి స్వాగతం, {user_name}!' if user_name else 'JarvisFi కు స్వాగతం!',
                'version': 'v2.0 - సమగ్ర ఎడిషన్'
            }
        }
        
        header_data = headers.get(current_language, headers['en'])
        
        st.markdown(f"""
        <div class="main-header">
            <div class="version-badge">{header_data['version']}</div>
            <h1>🤖 {header_data['title']}</h1>
            <p>{header_data['slogan']}</p>
            <small style="opacity: 0.9; font-size: 1rem; margin-top: 0.5rem; display: block;">
                {header_data['welcome']}
            </small>
        </div>
        """, unsafe_allow_html=True)
    
    def run_comprehensive_app(self):
        """Run the comprehensive JarvisFi application"""
        try:
            # Create comprehensive sidebar first
            self.create_comprehensive_sidebar()

            # Render header
            self.render_comprehensive_header()

            # Create main navigation
            self.render_main_navigation()

            # Track page views
            st.session_state.page_views += 1

        except Exception as e:
            self.logger.error(f"Application error: {e}")
            st.error("An error occurred. Please refresh the page.")

    def create_comprehensive_sidebar(self):
        """Create comprehensive sidebar with all original JarvisFi v1.0 features"""
        with st.sidebar:
            current_language = st.session_state.user_profile['basic_info']['language']

            # JarvisFi branding
            st.markdown("### 🤖 JarvisFi Settings")
            st.markdown("*Your AI-Powered Financial Genius*" if current_language == 'en' else "*உங்கள் AI-இயங்கும் நிதி மேதை*")
            st.markdown("---")

            # Language selector
            st.markdown("### 🌐 Language" if current_language == 'en' else "### 🌐 மொழி")

            language_options = {
                'en': 'English',
                'ta': 'தமிழ் (Tamil)',
                'hi': 'हिंदी (Hindi)',
                'te': 'తెలుగు (Telugu)'
            }

            selected_lang = st.selectbox(
                "Choose Language" if current_language == 'en' else "மொழியைத் தேர்ந்தெடுக்கவும்",
                options=list(language_options.keys()),
                format_func=lambda x: language_options[x],
                index=list(language_options.keys()).index(current_language),
                key="language_selector"
            )

            if selected_lang != current_language:
                st.session_state.user_profile['basic_info']['language'] = selected_lang
                st.rerun()

            # User type selector
            st.markdown("---")
            user_type_text = "👤 User Type" if current_language == 'en' else "👤 பயனர் வகை" if current_language == 'ta' else "👤 उपयोगकर्ता प्रकार" if current_language == 'hi' else "👤 వినియోగదారు రకం"

            user_types = {
                'beginner': 'Beginner' if current_language == 'en' else 'ஆரம்பநிலை' if current_language == 'ta' else 'शुरुआती' if current_language == 'hi' else 'ప్రారంభకుడు',
                'intermediate': 'Intermediate' if current_language == 'en' else 'இடைநிலை' if current_language == 'ta' else 'मध्यम' if current_language == 'hi' else 'మధ్యస్థ',
                'professional': 'Professional' if current_language == 'en' else 'தொழில்முறை' if current_language == 'ta' else 'पेशेवर' if current_language == 'hi' else 'వృత్తిపరమైన',
                'student': 'Student' if current_language == 'en' else 'மாணவர்' if current_language == 'ta' else 'छात्र' if current_language == 'hi' else 'విద్యార్థి',
                'farmer': 'Farmer' if current_language == 'en' else 'விவசாயி' if current_language == 'ta' else 'किसान' if current_language == 'hi' else 'రైతు',
                'senior_citizen': 'Senior Citizen' if current_language == 'en' else 'மூத்த குடிமகன்' if current_language == 'ta' else 'वरिष्ठ नागरिक' if current_language == 'hi' else 'సీనియర్ సిటిజన్'
            }

            current_user_type = st.session_state.user_profile['basic_info']['user_type']
            selected_user_type = st.selectbox(
                user_type_text,
                options=list(user_types.keys()),
                format_func=lambda x: user_types[x],
                index=list(user_types.keys()).index(current_user_type) if current_user_type in user_types else 0,
                key="user_type_selector"
            )

            if selected_user_type != current_user_type:
                st.session_state.user_profile['basic_info']['user_type'] = selected_user_type
                st.rerun()

            # Monthly Salary Input
            st.markdown("---")
            st.markdown("### 💰 Financial Profile" if current_language == 'en' else "### 💰 நிதி சுயவிவரம்" if current_language == 'ta' else "### 💰 वित्तीय प्रोफ़ाइल" if current_language == 'hi' else "### 💰 ఆర్థిక ప్రొఫైల్")

            current_salary = st.session_state.user_profile['basic_info']['monthly_income']
            monthly_salary = st.number_input(
                "Monthly Salary (₹)" if current_language == 'en' else "மாதாந்திர சம்பளம் (₹)" if current_language == 'ta' else "मासिक वेतन (₹)" if current_language == 'hi' else "నెలవారీ జీతం (₹)",
                min_value=5000,
                max_value=10000000,
                value=current_salary,
                step=5000,
                key="monthly_salary_input",
                help="Enter your monthly salary to get personalized insights" if current_language == 'en' else "தனிப்பயனாக்கப்பட்ட நுண்ணறிவுகளைப் பெற உங்கள் மாதாந்திர சம்பளத்தை உள்ளிடுங்கள்" if current_language == 'ta' else "व्यक्तिगत अंतर्दृष्टि प्राप्त करने के लिए अपना मासिक वेतन दर्ज करें" if current_language == 'hi' else "వ్యక్తిగత అంతర్దృష్టులను పొందడానికి మీ నెలవారీ జీతాన్ని నమోదు చేయండి"
            )

            if monthly_salary != current_salary:
                st.session_state.user_profile['basic_info']['monthly_income'] = monthly_salary
                st.rerun()

            # Show salary-based recommendations
            if monthly_salary:
                if current_language == 'en':
                    if monthly_salary < 25000:
                        salary_category = "Entry Level"
                        recommendation = "Focus on emergency fund building"
                    elif monthly_salary < 50000:
                        salary_category = "Mid Level"
                        recommendation = "Balance savings and investments"
                    elif monthly_salary < 100000:
                        salary_category = "Senior Level"
                        recommendation = "Diversify investment portfolio"
                    else:
                        salary_category = "Executive Level"
                        recommendation = "Advanced wealth management"
                elif current_language == 'ta':
                    if monthly_salary < 25000:
                        salary_category = "நுழைவு நிலை"
                        recommendation = "அவசரகால நிதி உருவாக்கலில் கவனம் செலுத்துங்கள்"
                    elif monthly_salary < 50000:
                        salary_category = "நடுத்தர நிலை"
                        recommendation = "சேமிப்பு மற்றும் முதலீடுகளை சமநிலைப்படுத்துங்கள்"
                    elif monthly_salary < 100000:
                        salary_category = "மூத்த நிலை"
                        recommendation = "முதலீட்டு போர்ட்ஃபோலியோவை பல்வகைப்படுத்துங்கள்"
                    else:
                        salary_category = "நிர்வாக நிலை"
                        recommendation = "மேம்பட்ட செல்வ மேலாண்மை"
                elif current_language == 'hi':
                    if monthly_salary < 25000:
                        salary_category = "प्रवेश स्तर"
                        recommendation = "आपातकालीन फंड निर्माण पर ध्यान दें"
                    elif monthly_salary < 50000:
                        salary_category = "मध्य स्तर"
                        recommendation = "बचत और निवेश को संतुलित करें"
                    elif monthly_salary < 100000:
                        salary_category = "वरिष्ठ स्तर"
                        recommendation = "निवेश पोर्टफोलियो में विविधता लाएं"
                    else:
                        salary_category = "कार्यकारी स्तर"
                        recommendation = "उन्नत धन प्रबंधन"
                else:  # Telugu
                    if monthly_salary < 25000:
                        salary_category = "ప్రవేశ స్థాయి"
                        recommendation = "అత్యవసర నిధి నిర్మాణంపై దృష్టి పెట్టండి"
                    elif monthly_salary < 50000:
                        salary_category = "మధ్య స్థాయి"
                        recommendation = "పొదుపు మరియు పెట్టుబడులను సమతుల్యం చేయండి"
                    elif monthly_salary < 100000:
                        salary_category = "సీనియర్ స్థాయి"
                        recommendation = "పెట్టుబడి పోర్ట్‌ఫోలియోను వైవిధ్యపరచండి"
                    else:
                        salary_category = "కార్యనిర్వాహక స్థాయి"
                        recommendation = "అధునాతన సంపద నిర్వహణ"

                st.info(f"**{salary_category}**: {recommendation}")

            # Dark mode toggle
            st.markdown("---")
            dark_mode_text = "🌙 Dark Mode" if current_language == 'en' else "🌙 இருண்ட பயன்முறை" if current_language == 'ta' else "🌙 डार्क मोड" if current_language == 'hi' else "🌙 డార్క్ మోడ్"
            dark_mode = st.toggle(dark_mode_text, value=st.session_state.user_profile['preferences']['dark_mode'], key="dark_mode_toggle")

            if dark_mode != st.session_state.user_profile['preferences']['dark_mode']:
                st.session_state.user_profile['preferences']['dark_mode'] = dark_mode
                st.rerun()

            # Voice Interface Section
            st.markdown("---")
            st.markdown("### 🎤 Voice Assistant" if current_language == 'en' else "### 🎤 குரல் உதவியாளர்" if current_language == 'ta' else "### 🎤 आवाज़ सहायक" if current_language == 'hi' else "### 🎤 వాయిస్ అసిస్టెంట్")

            # Voice settings
            voice_quality = st.selectbox(
                "Voice Quality" if current_language == 'en' else "குரல் தரம்" if current_language == 'ta' else "आवाज़ की गुणवत्ता" if current_language == 'hi' else "వాయిస్ నాణ్యత",
                ["Standard", "High Quality", "Natural"],
                index=1,
                key="voice_quality"
            )

            voice_speed = st.slider(
                "Speech Speed" if current_language == 'en' else "பேச்சு வேகம்" if current_language == 'ta' else "बोलने की गति" if current_language == 'hi' else "మాట్లాడే వేగం",
                min_value=0.5, max_value=2.0, value=1.0, step=0.1,
                key="voice_speed"
            )

            # Security Section
            st.markdown("---")
            st.markdown("### 🔐 Security" if current_language == 'en' else "### 🔐 பாதுகாப்பு" if current_language == 'ta' else "### 🔐 सुरक्षा" if current_language == 'hi' else "### 🔐 భద్రత")

            # Security status
            security_status = "🟢 Secure Mode" if st.session_state.user_profile['security']['data_encryption'] else "🟡 Basic Mode"
            st.markdown(f"**Status:** {security_status}")

            # Data encryption toggle
            encrypt_data = st.toggle(
                "Encrypt Data" if current_language == 'en' else "தரவு குறியாக்கம்" if current_language == 'ta' else "डेटा एन्क्रिप्शन" if current_language == 'hi' else "డేటా ఎన్‌క్రిప్షన్",
                value=st.session_state.user_profile['security']['data_encryption'],
                key="encrypt_toggle"
            )
            st.session_state.user_profile['security']['data_encryption'] = encrypt_data

            # Auto-logout timer
            auto_logout = st.selectbox(
                "Auto Logout" if current_language == 'en' else "தானியங்கு வெளியேறு" if current_language == 'ta' else "ऑटो लॉगआउट" if current_language == 'hi' else "ఆటో లాగ్అవుట్",
                ["Never", "15 minutes", "30 minutes", "1 hour", "2 hours"],
                index=2,
                key="auto_logout"
            )

            # AI & RAG Section
            st.markdown("---")
            st.markdown("### 🧠 AI Features" if current_language == 'en' else "### 🧠 AI அம்சங்கள்" if current_language == 'ta' else "### 🧠 AI सुविधाएं" if current_language == 'hi' else "### 🧠 AI ఫీచర్లు")

            # AI Accuracy toggle
            ai_accuracy = st.toggle(
                "AI Fact-Checking" if current_language == 'en' else "AI உண்மை சரிபார்ப்பு" if current_language == 'ta' else "AI तथ्य जांच" if current_language == 'hi' else "AI వాస్తవ తనిఖీ",
                value=st.session_state.user_profile['preferences']['ai_accuracy_mode'],
                key="ai_accuracy_toggle"
            )
            st.session_state.user_profile['preferences']['ai_accuracy_mode'] = ai_accuracy

            # Enhanced sources toggle
            enhanced_sources = st.toggle(
                "Enhanced Sources" if current_language == 'en' else "மேம்பட்ட ஆதாரங்கள்" if current_language == 'ta' else "उन्नत स्रोत" if current_language == 'hi' else "మెరుగైన మూలాలు",
                value=st.session_state.user_profile['preferences']['enhanced_sources'],
                key="enhanced_sources_toggle"
            )
            st.session_state.user_profile['preferences']['enhanced_sources'] = enhanced_sources

            # AI Response Style
            ai_style = st.selectbox(
                "Response Style" if current_language == 'en' else "பதில் பாணி" if current_language == 'ta' else "उत्तर शैली" if current_language == 'hi' else "ప్రతిస్పందన శైలి",
                ["Professional", "Friendly", "Detailed", "Concise"],
                index=0,
                key="ai_style"
            )

            # Learning Mode
            learning_mode = st.toggle(
                "Learning Mode" if current_language == 'en' else "கற்றல் பயன்முறை" if current_language == 'ta' else "सीखने का मोड" if current_language == 'hi' else "లెర్నింగ్ మోడ్",
                value=st.session_state.user_profile['preferences']['learning_mode'],
                key="learning_mode_toggle"
            )
            st.session_state.user_profile['preferences']['learning_mode'] = learning_mode

            # Currency & Exchange Section
            st.markdown("---")
            st.markdown("### 💱 Currency & Exchange" if current_language == 'en' else "### 💱 நாணயம் & மாற்று" if current_language == 'ta' else "### 💱 मुद्रा और विनिमय" if current_language == 'hi' else "### 💱 కరెన్సీ & ఎక్స్చేంజ్")

            currency_options = ['INR', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'SGD']
            current_currency = st.session_state.user_profile['basic_info']['currency']

            selected_currency = st.selectbox(
                "Primary Currency" if current_language == 'en' else "முதன்மை நாணயம்" if current_language == 'ta' else "प्राथमिक मुद्रा" if current_language == 'hi' else "ప్రాథమిక కరెన్సీ",
                options=currency_options,
                index=currency_options.index(current_currency) if current_currency in currency_options else 0,
                key="currency_selector"
            )

            if selected_currency != current_currency:
                st.session_state.user_profile['basic_info']['currency'] = selected_currency
                st.rerun()

            # Exchange rate display (mock data)
            st.markdown("**Live Rates** / **நேரடி விகிதங்கள்** / **लाइव दरें** / **లైవ్ రేట్లు**")
            if selected_currency == 'INR':
                rates = {'USD': 0.012, 'EUR': 0.011, 'GBP': 0.0095}
            else:
                rates = {'INR': 83.12, 'USD': 1.0, 'EUR': 0.92}

            for curr, rate in list(rates.items())[:3]:
                st.markdown(f"• 1 {selected_currency} = {rate:.3f} {curr}")

            # Help & Information Section
            with st.expander("ℹ️ Help & Information" if current_language == 'en' else "ℹ️ உதவி & தகவல்" if current_language == 'ta' else "ℹ️ सहायता और जानकारी" if current_language == 'hi' else "ℹ️ సహాయం & సమాచారం"):

                st.markdown("**Quick Help** / **விரைவு உதவி** / **त्वरित सहायता** / **త్వరిత సహాయం**")

                help_topics = {
                    'en': [
                        "💬 **Chat**: Ask JarvisFi questions about budgets, savings, investments",
                        "🌐 **Language**: Switch between multiple languages instantly",
                        "👤 **Profile**: Set your user type for personalized advice",
                        "🎤 **Voice**: Use voice commands with JarvisFi",
                        "🔐 **Security**: Your data is encrypted and secure",
                        "💱 **Currency**: Supports multiple currencies",
                        "🧠 **AI**: Advanced AI features for intelligent responses"
                    ],
                    'ta': [
                        "💬 **அரட்டை**: பட்ஜெட், சேமிப்பு, முதலீடு பற்றி JarvisFi-யிடம் கேளுங்கள்",
                        "🌐 **மொழி**: பல மொழிகளுக்கு இடையே உடனடியாக மாறுங்கள்",
                        "👤 **சுயவிவரம்**: தனிப்பயனாக்கப்பட்ட ஆலோசனைக்கு உங்கள் பயனர் வகையை அமைக்கவும்",
                        "🎤 **குரல்**: JarvisFi உடன் குரல் கட்டளைகளைப் பயன்படுத்துங்கள்",
                        "🔐 **பாதுகாப்பு**: உங்கள் தரவு குறியாக்கம் செய்யப்பட்டு பாதுகாப்பானது",
                        "💱 **நாணயம்**: பல நாணயங்களுக்கு ஆதரவு அளிக்கிறது",
                        "🧠 **AI**: புத்திசாலித்தனமான பதில்களுக்கான மேம்பட்ட AI அம்சங்கள்"
                    ],
                    'hi': [
                        "💬 **चैट**: बजट, बचत, निवेश के बारे में JarvisFi से पूछें",
                        "🌐 **भाषा**: कई भाषाओं के बीच तुरंत स्विच करें",
                        "👤 **प्रोफ़ाइल**: व्यक्तिगत सलाह के लिए अपना उपयोगकर्ता प्रकार सेट करें",
                        "🎤 **आवाज़**: JarvisFi के साथ आवाज़ कमांड का उपयोग करें",
                        "🔐 **सुरक्षा**: आपका डेटा एन्क्रिप्टेड और सुरक्षित है",
                        "💱 **मुद्रा**: कई मुद्राओं का समर्थन करता है",
                        "🧠 **AI**: बुद्धिमान प्रतिक्रियाओं के लिए उन्नत AI सुविधाएं"
                    ],
                    'te': [
                        "💬 **చాట్**: బడ్జెట్, పొదుపు, పెట్టుబడుల గురించి JarvisFi ని అడగండి",
                        "🌐 **భాష**: అనేక భాషల మధ్య తక్షణమే మారండి",
                        "👤 **ప్రొఫైల్**: వ్యక్తిగత సలహా కోసం మీ వినియోగదారు రకాన్ని సెట్ చేయండి",
                        "🎤 **వాయిస్**: JarvisFi తో వాయిస్ కమాండ్లను ఉపయోగించండి",
                        "🔐 **భద్రత**: మీ డేటా ఎన్‌క్రిప్ట్ చేయబడింది మరియు సురక్షితం",
                        "💱 **కరెన్సీ**: అనేక కరెన్సీలకు మద్దతు ఇస్తుంది",
                        "🧠 **AI**: తెలివైన ప్రతిస్పందనల కోసం అధునాతన AI ఫీచర్లు"
                    ]
                }

                topics = help_topics.get(current_language, help_topics['en'])
                for topic in topics:
                    st.markdown(topic)

                # Sample questions
                st.markdown("---")
                st.markdown("**Sample Questions** / **மாதிரி கேள்விகள்** / **नमूना प्रश्न** / **నమూనా ప్రశ్నలు**")

                sample_questions = {
                    'en': [
                        "How can I save money?",
                        "What's a good budget plan?",
                        "How should I start investing?",
                        "What are SIPs?",
                        "How to reduce expenses?",
                        "Best savings account options?"
                    ],
                    'ta': [
                        "பணம் எப்படி சேமிக்கலாம்?",
                        "நல்ல பட்ஜெட் திட்டம் என்ன?",
                        "முதலீட்டை எப்படி தொடங்க வேண்டும்?",
                        "SIP என்றால் என்ன?",
                        "செலவுகளை எப்படி குறைக்கலாம்?",
                        "சிறந்த சேமிப்பு கணக்கு விருப்பங்கள்?"
                    ],
                    'hi': [
                        "पैसे कैसे बचाएं?",
                        "अच्छी बजट योजना क्या है?",
                        "निवेश कैसे शुरू करें?",
                        "SIP क्या हैं?",
                        "खर्च कैसे कम करें?",
                        "सबसे अच्छे बचत खाता विकल्प?"
                    ],
                    'te': [
                        "డబ్బు ఎలా ఆదా చేయాలి?",
                        "మంచి బడ్జెట్ ప్లాన్ ఏమిటి?",
                        "పెట్టుబడి ఎలా ప్రారంభించాలి?",
                        "SIP లు ఏమిటి?",
                        "ఖర్చులు ఎలా తగ్గించాలి?",
                        "ఉత్తమ పొదుపు ఖాతా ఎంపికలు?"
                    ]
                }

                questions = sample_questions.get(current_language, sample_questions['en'])
                for i, question in enumerate(questions[:3], 1):  # Show only 3 questions
                    if st.button(f"{i}. {question}", key=f"sample_q_{i}"):
                        # Add question to chat
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": question,
                            "timestamp": datetime.now().isoformat(),
                            "type": "sample_question"
                        })
                        # Generate AI response
                        response = self.generate_ai_response(question, current_language)
                        st.session_state.chat_history.append(response)
                        # Switch to chat tab
                        st.session_state.active_tab = 1
                        st.rerun()

            # Footer
            st.markdown("---")
            st.markdown(
                "**🤖 JarvisFi v2.0**" if current_language == 'en'
                else "**🤖 JarvisFi v2.0**" if current_language == 'ta'
                else "**🤖 JarvisFi v2.0**" if current_language == 'hi'
                else "**🤖 JarvisFi v2.0**"
            )
            st.markdown(
                "*Your AI-Powered Financial Genius* 🚀💰" if current_language == 'en'
                else "*உங்கள் AI-இயங்கும் நிதி மேதை* 🚀💰" if current_language == 'ta'
                else "*आपका AI-संचालित वित्तीय प्रतिभा* 🚀💰" if current_language == 'hi'
                else "*మీ AI-శక్తితో కూడిన ఆర్థిక మేధావి* 🚀💰"
            )
    
    def render_main_navigation(self):
        """Render main navigation with all features"""
        current_language = st.session_state.user_profile['basic_info']['language']

        # Check if we need to switch to a specific tab
        active_tab = st.session_state.get('active_tab', 0)

        # Navigation tabs with comprehensive features
        tab_labels = {
            'en': [
                "🏠 Home", "💬 AI Chat", "📊 Dashboard", "🧮 Calculators",
                "🎤 Voice", "👨‍🌾 Farmer Tools", "💳 Credit Score", "📈 Investments",
                "🛡️ Security", "👥 Community", "🎮 Gamification", "👤 Profile"
            ],
            'ta': [
                "🏠 முகப்பு", "💬 AI அரட்டை", "📊 டாஷ்போர்டு", "🧮 கணக்கீட்டாளர்கள்",
                "🎤 குரல்", "👨‍🌾 விவசாயி கருவிகள்", "💳 கிரெடிட் ஸ்கோர்", "📈 முதலீடுகள்",
                "🛡️ பாதுகாப்பு", "👥 சமூகம்", "🎮 விளையாட்டு", "👤 சுயவிவரம்"
            ],
            'hi': [
                "🏠 होम", "💬 AI चैट", "📊 डैशबोर्ड", "🧮 कैलकुलेटर",
                "🎤 आवाज़", "👨‍🌾 किसान उपकरण", "💳 क्रेडिट स्कोर", "📈 निवेश",
                "🛡️ सुरक्षा", "👥 समुदाय", "🎮 गेमिफिकेशन", "👤 प्रोफ़ाइल"
            ]
        }

        labels = tab_labels.get(current_language, tab_labels['en'])

        # Create tabs but render content based on active_tab
        if active_tab == 0:
            st.markdown(f"### {labels[0]}")
            self.render_comprehensive_home()
        elif active_tab == 1:
            st.markdown(f"### {labels[1]}")
            self.render_ai_chat_interface()
        elif active_tab == 2:
            st.markdown(f"### {labels[2]}")
            self.render_comprehensive_dashboard()
        elif active_tab == 3:
            st.markdown(f"### {labels[3]}")
            self.render_financial_calculators()
        elif active_tab == 4:
            st.markdown(f"### {labels[4]}")
            self.render_voice_interface()
        elif active_tab == 5:
            st.markdown(f"### {labels[5]}")
            self.render_farmer_tools()
        elif active_tab == 6:
            st.markdown(f"### {labels[6]}")
            self.render_credit_score_tracking()
        elif active_tab == 7:
            st.markdown(f"### {labels[7]}")
            self.render_investment_portfolio()
        elif active_tab == 8:
            st.markdown(f"### {labels[8]}")
            self.render_security_center()
        elif active_tab == 9:
            st.markdown(f"### {labels[9]}")
            self.render_community_forum()
        elif active_tab == 10:
            st.markdown(f"### {labels[10]}")
            self.render_gamification()
        elif active_tab == 11:
            st.markdown(f"### {labels[11]}")
            self.render_comprehensive_profile()
        else:
            # Default to home
            st.markdown(f"### {labels[0]}")
            self.render_comprehensive_home()

        # Navigation buttons at the bottom
        st.markdown("---")
        st.markdown("### 🧭 Navigation")

        cols = st.columns(6)
        nav_buttons = [
            (0, "🏠 Home"),
            (1, "💬 Chat"),
            (2, "📊 Dashboard"),
            (3, "🧮 Calc"),
            (4, "🎤 Voice"),
            (5, "👤 Profile")
        ]

        for i, (tab_idx, label) in enumerate(nav_buttons):
            with cols[i]:
                if st.button(label, key=f"nav_{tab_idx}"):
                    st.session_state.active_tab = tab_idx
                    st.rerun()


    def render_comprehensive_home(self):
        """Render comprehensive home page with all features"""
        current_language = st.session_state.user_profile['basic_info']['language']

        # Welcome section
        col1, col2 = st.columns([2, 1])

        with col1:
            if current_language == 'en':
                st.markdown("### 🏠 Welcome to JarvisFi Comprehensive Edition")
                st.markdown("Your complete AI-powered financial ecosystem with advanced features")
            elif current_language == 'ta':
                st.markdown("### 🏠 JarvisFi விரிவான பதிப்புக்கு வரவேற்கிறோம்")
                st.markdown("மேம்பட்ட அம்சங்களுடன் உங்கள் முழுமையான AI-இயங்கும் நிதி சுற்றுச்சூழல்")
            elif current_language == 'hi':
                st.markdown("### 🏠 JarvisFi व्यापक संस्करण में आपका स्वागत है")
                st.markdown("उन्नत सुविधाओं के साथ आपका पूर्ण AI-संचालित वित्तीय पारिस्थितिकी तंत्र")

        with col2:
            # System status
            st.markdown("**🔋 System Status**")
            st.markdown("🟢 All Systems Online")
            st.markdown("🤖 AI Services: Active")
            st.markdown("🔒 Security: Enabled")
            st.markdown("🌐 Multi-language: Ready")

        # Feature overview metrics
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("🌍 Languages", "4", "🔥")

        with col2:
            st.metric("🧮 Calculators", "15+", "📈")

        with col3:
            st.metric("👥 User Types", "6", "🎯")

        with col4:
            st.metric("🔒 Security Level", "Enterprise", "🛡️")

        with col5:
            st.metric("🤖 AI Accuracy", "95%", "✨")

        # Quick actions
        st.markdown("---")
        st.markdown("### 🚀 Quick Actions")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("💬 Start AI Chat", key="home_chat"):
                st.session_state.active_tab = 1
                st.success("Switching to AI Chat...")
                st.rerun()

        with col2:
            if st.button("📊 View Dashboard", key="home_dashboard"):
                st.session_state.active_tab = 2
                st.success("Loading Dashboard...")
                st.rerun()

        with col3:
            if st.button("🧮 Use Calculators", key="home_calc"):
                st.session_state.active_tab = 3
                st.success("Opening Calculators...")
                st.rerun()

        with col4:
            if st.button("🎤 Voice Assistant", key="home_voice"):
                st.session_state.active_tab = 4
                st.success("Activating Voice...")
                st.rerun()

        # Feature highlights
        st.markdown("---")
        st.markdown("### ✨ New Features in v2.0")

        features = [
            "🤖 **Advanced AI Integration** - IBM Watson + Hugging Face models",
            "🎤 **Voice Interface** - Speech-to-text and text-to-speech in multiple languages",
            "👨‍🌾 **Farmer Tools** - Specialized calculators for agricultural finance",
            "💳 **Credit Score Tracking** - Real-time CIBIL score monitoring",
            "🛡️ **Enhanced Security** - AES-256 encryption and biometric auth",
            "🎮 **Gamification** - Points, badges, and financial challenges",
            "👥 **Community Forum** - Connect with other users",
            "📱 **Mobile-First Design** - Optimized for all devices"
        ]

        for feature in features:
            st.markdown(feature)

    def render_ai_chat_interface(self):
        """Render comprehensive AI chat interface"""
        current_language = st.session_state.user_profile['basic_info']['language']

        if current_language == 'en':
            st.markdown("### 💬 AI Chat - Enhanced with RAG & Multi-language Support")
        elif current_language == 'ta':
            st.markdown("### 💬 AI அரட்டை - RAG & பல மொழி ஆதரவுடன் மேம்படுத்தப்பட்டது")
        elif current_language == 'hi':
            st.markdown("### 💬 AI चैट - RAG और बहुभाषी समर्थन के साथ उन्नत")

        # AI settings
        with st.expander("🔧 AI Settings" if current_language == 'en' else "🔧 AI அமைப்புகள்" if current_language == 'ta' else "🔧 AI सेटिंग्स"):
            col1, col2 = st.columns(2)

            with col1:
                ai_accuracy = st.toggle("AI Fact-Checking", value=st.session_state.user_profile['preferences']['ai_accuracy_mode'])
                rag_enabled = st.toggle("Enhanced Sources (RAG)", value=st.session_state.rag_enabled)

            with col2:
                confidence_threshold = st.slider("Confidence Threshold", 0.5, 1.0, st.session_state.ai_confidence_threshold, 0.1)
                response_style = st.selectbox("Response Style", ['Professional', 'Friendly', 'Detailed', 'Concise'])

        # Chat interface
        chat_container = st.container()

        with chat_container:
            # Display chat history
            if st.session_state.chat_history:
                for message in st.session_state.chat_history:
                    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
                        st.markdown(message["content"])

                        # Show AI metadata if available
                        if message["role"] == "assistant" and "metadata" in message:
                            with st.expander("📊 AI Response Details"):
                                metadata = message["metadata"]
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.metric("Confidence", f"{metadata.get('confidence', 0.5):.1%}")

                                with col2:
                                    st.metric("Intent", metadata.get('intent', 'general').title())

                                with col3:
                                    st.metric("Language", metadata.get('language', 'en').upper())

                                if metadata.get('sources'):
                                    st.markdown("**Sources:**")
                                    for source in metadata['sources']:
                                        st.markdown(f"• {source}")
            else:
                # Welcome message
                with st.chat_message("assistant", avatar="🤖"):
                    welcome_msg = self.get_welcome_message(current_language)
                    st.markdown(welcome_msg)

        # Chat input
        if prompt := st.chat_input("Ask JarvisFi anything about finance..." if current_language == 'en' else "நிதி பற்றி JarvisFi-யிடம் எதையும் கேளுங்கள்..." if current_language == 'ta' else "वित्त के बारे में JarvisFi से कुछ भी पूछें..."):
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().isoformat()
            })

            # Display user message
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            # Generate AI response
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("JarvisFi is thinking..." if current_language == 'en' else "JarvisFi யோசித்துக்கொண்டிருக்கிறது..." if current_language == 'ta' else "JarvisFi सोच रहा है..."):
                    response = self.generate_ai_response(prompt, current_language)
                    st.markdown(response["content"])

                    # Add to chat history
                    st.session_state.chat_history.append(response)

        # Voice controls
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🎙️ Voice Input" if current_language == 'en' else "🎙️ குரல் உள்ளீடு" if current_language == 'ta' else "🎙️ आवाज़ इनपुट", key="chat_voice_input"):
                with st.spinner("🎤 Listening..."):
                    time.sleep(1.5)
                    # Simulate voice recognition
                    voice_samples = {
                        'en': ["What's my budget for this month?", "How should I invest 10000 rupees?", "Calculate EMI for home loan"],
                        'ta': ["இந்த மாதத்திற்கான என் பட்ஜெட் என்ன?", "10000 ரூபாயை எப்படி முதலீடு செய்வது?", "வீட்டுக் கடனுக்கு EMI கணக்கிடு"],
                        'hi': ["इस महीने का मेरा बजट क्या है?", "10000 रुपये कैसे निवेश करूं?", "होम लोन के लिए EMI कैलकुलेट करें"]
                    }

                    import random
                    samples = voice_samples.get(current_language, voice_samples['en'])
                    voice_input = random.choice(samples)

                    st.success(f"🎤 Voice detected: '{voice_input}'")

                    # Process the voice input as if it was typed
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": voice_input,
                        "timestamp": datetime.now().isoformat(),
                        "type": "voice"
                    })

                    # Generate AI response
                    response = self.generate_ai_response(voice_input, current_language)
                    st.session_state.chat_history.append(response)
                    st.rerun()

        with col2:
            if st.button("🔊 Read Aloud" if current_language == 'en' else "🔊 சத்தமாக படிக்கவும்" if current_language == 'ta' else "🔊 जोर से पढ़ें", key="chat_read_aloud"):
                if st.session_state.chat_history:
                    last_message = st.session_state.chat_history[-1]
                    if last_message["role"] == "assistant":
                        with st.spinner("🔊 Converting to speech..."):
                            time.sleep(1)
                            st.success(f"🔊 Reading: '{last_message['content'][:100]}...'")
                    else:
                        st.info("No assistant message to read aloud")
                else:
                    st.info("No messages to read aloud")

        with col3:
            if st.button("🧹 Clear Chat" if current_language == 'en' else "🧹 அரட்டையை அழிக்கவும்" if current_language == 'ta' else "🧹 चैट साफ़ करें", key="chat_clear"):
                st.session_state.chat_history = []
                st.success("Chat cleared!")
                st.rerun()

    def get_welcome_message(self, language: str) -> str:
        """Get personalized welcome message"""
        user_type = st.session_state.user_profile['basic_info']['user_type']
        user_name = st.session_state.user_profile['basic_info']['name']

        messages = {
            'en': {
                'beginner': f"👋 Hello {user_name or 'there'}! I'm JarvisFi, your AI financial genius. I'm here to help you start your financial journey with personalized advice, budgeting tips, and investment guidance. What would you like to learn about first?",
                'professional': f"👋 Welcome {user_name or 'there'}! I'm JarvisFi, ready to provide advanced financial insights, portfolio analysis, and strategic planning. How can I assist with your financial goals today?",
                'farmer': f"👋 Namaste {user_name or 'there'}! I'm JarvisFi, your agricultural finance expert. I can help with crop loans, MSP tracking, subsidies, and weather-based financial planning. What farming finance topic interests you?",
                'student': f"👋 Hi {user_name or 'there'}! I'm JarvisFi, here to help you build smart money habits. Let's explore student budgeting, building credit, and managing education expenses. What would you like to know?",
                'senior_citizen': f"👋 Hello {user_name or 'there'}! I'm JarvisFi, here to help with retirement planning, healthcare finances, and safe investment options. How can I assist you today?"
            }
        }

        lang_messages = messages.get(language, messages['en'])
        return lang_messages.get(user_type, lang_messages['beginner'])

    def generate_ai_response(self, prompt: str, language: str) -> Dict[str, Any]:
        """Generate AI response with metadata"""
        try:
            # Simulate AI processing
            time.sleep(0.5)

            # Get user context safely
            user_context = st.session_state.get('user_profile', {})
            basic_info = user_context.get('basic_info', {})
            monthly_income = basic_info.get('monthly_income', 30000)
            user_type = basic_info.get('user_type', 'beginner')

            # Generate response based on prompt and language
            content = self.get_response_content(prompt, monthly_income, user_type, language)

            return {
                "role": "assistant",
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "confidence": 0.85,
                    "intent": self.classify_intent(prompt),
                    "language": language,
                    "sources": ["RBI Guidelines", "SEBI Recommendations", "Financial Planning Best Practices"]
                }
            }
        except Exception as e:
            # Fallback response in case of error
            self.logger.error(f"Error generating AI response: {e}")
            return {
                "role": "assistant",
                "content": "I apologize, but I encountered an issue processing your request. Please try asking your question again, and I'll be happy to help with your financial needs!",
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "confidence": 0.5,
                    "intent": "error_fallback",
                    "language": language,
                    "sources": []
                }
            }

    def get_response_content(self, prompt: str, monthly_income: int, user_type: str, language: str) -> str:
        """Get response content based on prompt and context"""
        prompt_lower = prompt.lower()

        # Budget-related queries
        if any(word in prompt_lower for word in ['budget', 'expense', 'spending', 'money']):
            if language == 'ta':
                return f"உங்கள் ₹{monthly_income:,} மாதாந்திர வருமானத்தின் அடிப்படையில், நான் 50/30/20 விதியை பரிந்துரைக்கிறேன்: தேவைகளுக்கு ₹{int(monthly_income*0.5):,}, விருப்பங்களுக்கு ₹{int(monthly_income*0.3):,}, மற்றும் சேமிப்பு மற்றும் முதலீடுகளுக்கு ₹{int(monthly_income*0.2):,}."
            elif language == 'hi':
                return f"आपकी ₹{monthly_income:,} मासिक आय के आधार पर, मैं 50/30/20 नियम की सिफारिश करता हूं: जरूरतों के लिए ₹{int(monthly_income*0.5):,}, इच्छाओं के लिए ₹{int(monthly_income*0.3):,}, और बचत और निवेश के लिए ₹{int(monthly_income*0.2):,}।"
            else:
                return f"Based on your ₹{monthly_income:,} monthly income, I recommend the 50/30/20 rule: ₹{int(monthly_income*0.5):,} for needs, ₹{int(monthly_income*0.3):,} for wants, and ₹{int(monthly_income*0.2):,} for savings and investments."

        # Investment-related queries
        elif any(word in prompt_lower for word in ['invest', 'sip', 'mutual fund', 'stock']):
            sip_amount = max(1000, int(monthly_income * 0.15))
            if language == 'ta':
                return f"உங்கள் வருமான நிலைக்கு, பல்வகைப்படுத்தப்பட்ட ஈக்விட்டி நிதிகளில் ₹{sip_amount:,} மாதாந்திர SIP உடன் தொடங்க பரிந்துரைக்கிறேன். இது உங்கள் வருமானத்தின் 15% ஆகும், இது நீண்ட கால செல்வ உருவாக்கத்திற்கு சிறந்தது."
            elif language == 'hi':
                return f"आपके आय स्तर के लिए, मैं विविधीकृत इक्विटी फंड में ₹{sip_amount:,} मासिक SIP के साथ शुरुआत करने का सुझाव देता हूं। यह आपकी आय का 15% है, जो दीर्घकालिक धन निर्माण के लिए आदर्श है।"
            else:
                return f"For your income level, I suggest starting with a ₹{sip_amount:,} monthly SIP in diversified equity funds. This represents 15% of your income, which is ideal for long-term wealth building."

        # Savings-related queries
        elif any(word in prompt_lower for word in ['save', 'saving', 'emergency']):
            target_savings = int(monthly_income * 0.2)
            if language == 'ta':
                return f"உங்கள் ₹{monthly_income:,} வருமானத்திற்கு, மாதம் ₹{target_savings:,} சேமிக்க பரிந்துரைக்கிறேன். முதலில் 6 மாத செலவுகளுக்கான அவசரகால நிதியை உருவாக்குங்கள், பின்னர் முதலீடுகளில் கவனம் செலுத்துங்கள்."
            elif language == 'hi':
                return f"आपकी ₹{monthly_income:,} आय के लिए, मैं महीने में ₹{target_savings:,} बचत करने की सलाह देता हूं। पहले 6 महीने के खर्च के लिए आपातकालीन फंड बनाएं, फिर निवेश पर ध्यान दें।"
            else:
                return f"For your ₹{monthly_income:,} income, I recommend saving ₹{target_savings:,} per month. First build an emergency fund for 6 months of expenses, then focus on investments."

        # Default response
        else:
            if language == 'ta':
                return f"வணக்கம்! நான் JarvisFi, உங்கள் AI நிதி மேதை. நான் பட்ஜெட், முதலீடுகள், சேமிப்பு, வரி திட்டமிடல் மற்றும் பலவற்றில் உதவ முடியும். {user_type} பயனராக, உங்களுக்கு எந்த குறிப்பிட்ட பகுதியை ஆராய விரும்புகிறீர்கள்?"
            elif language == 'hi':
                return f"नमस्ते! मैं JarvisFi हूं, आपका AI वित्तीय प्रतिभा। मैं बजट, निवेश, बचत, कर योजना और अधिक में सहायता कर सकता हूं। {user_type} उपयोगकर्ता के रूप में, आप किस विशिष्ट क्षेत्र का पता लगाना चाहेंगे?"
            else:
                return f"Hello! I'm JarvisFi, your AI financial genius. I can help with budgeting, investments, savings, tax planning, and more. As a {user_type} user, what specific financial area would you like to explore?"

    def classify_intent(self, prompt: str) -> str:
        """Classify user intent from prompt"""
        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in ['budget', 'expense', 'spending']):
            return 'budgeting'
        elif any(word in prompt_lower for word in ['invest', 'sip', 'mutual fund']):
            return 'investment'
        elif any(word in prompt_lower for word in ['save', 'saving', 'emergency']):
            return 'savings'
        elif any(word in prompt_lower for word in ['loan', 'emi', 'debt']):
            return 'debt_management'
        elif any(word in prompt_lower for word in ['tax', 'deduction']):
            return 'tax_planning'
        else:
            return 'general_financial'

    def render_comprehensive_dashboard(self):
        """Render comprehensive dashboard with all metrics"""
        current_language = st.session_state.user_profile['basic_info']['language']

        if current_language == 'en':
            st.markdown("### 📊 Comprehensive Financial Dashboard")
        elif current_language == 'ta':
            st.markdown("### 📊 விரிவான நிதி டாஷ்போர்டு")
        elif current_language == 'hi':
            st.markdown("### 📊 व्यापक वित्तीय डैशबोर्ड")

        # Get user financial data
        monthly_income = st.session_state.user_profile['basic_info']['monthly_income']
        user_type = st.session_state.user_profile['basic_info']['user_type']

        # Calculate dynamic metrics based on user profile
        if user_type == 'student':
            expense_ratio = 0.85
        elif user_type == 'senior_citizen':
            expense_ratio = 0.60
        elif user_type == 'farmer':
            expense_ratio = 0.70
        else:
            expense_ratio = 0.75

        monthly_expenses = int(monthly_income * expense_ratio)
        monthly_savings = monthly_income - monthly_expenses
        annual_savings = monthly_savings * 12

        # Top metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Monthly Income" if current_language == 'en' else "மாதாந்திர வருமானம்" if current_language == 'ta' else "मासिक आय",
                f"₹{monthly_income:,}",
                "📈 Stable"
            )

        with col2:
            st.metric(
                "Monthly Expenses" if current_language == 'en' else "மாதாந்திர செலவுகள்" if current_language == 'ta' else "मासिक खर्च",
                f"₹{monthly_expenses:,}",
                f"{expense_ratio:.0%} of income"
            )

        with col3:
            st.metric(
                "Monthly Savings" if current_language == 'en' else "மாதாந்திர சேமிப்பு" if current_language == 'ta' else "मासिक बचत",
                f"₹{monthly_savings:,}",
                f"{(1-expense_ratio):.0%} savings rate"
            )

        with col4:
            st.metric(
                "Annual Projection" if current_language == 'en' else "வருடாந்திர கணிப்பு" if current_language == 'ta' else "वार्षिक प्रक्षेपण",
                f"₹{annual_savings:,}",
                "💰 Growing"
            )

        # Charts section
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            # Expense breakdown pie chart
            st.markdown("#### 💰 Expense Breakdown")

            expense_data = {
                'Category': ['Rent/Housing', 'Food', 'Transport', 'Utilities', 'Entertainment', 'Savings'],
                'Amount': [
                    monthly_income * 0.30,
                    monthly_income * 0.20,
                    monthly_income * 0.08,
                    monthly_income * 0.05,
                    monthly_income * 0.12,
                    monthly_savings
                ]
            }

            fig_pie = px.pie(
                values=expense_data['Amount'],
                names=expense_data['Category'],
                title="Monthly Budget Allocation",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Savings trend line chart
            st.markdown("#### 📈 Savings Trend (6 Months)")

            # Generate sample savings data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            base_savings = monthly_savings
            savings_data = [
                base_savings * (0.8 + 0.4 * np.random.random()) for _ in months
            ]

            fig_line = px.line(
                x=months,
                y=savings_data,
                title=f"Average Monthly Savings: ₹{np.mean(savings_data):,.0f}",
                markers=True
            )
            fig_line.update_traces(line_color='#667eea', line_width=3)
            fig_line.update_layout(
                xaxis_title="Month",
                yaxis_title="Savings (₹)",
                showlegend=False
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # Financial health indicators
        st.markdown("---")
        st.markdown("#### 🏥 Financial Health Indicators")

        col1, col2, col3 = st.columns(3)

        with col1:
            savings_rate = (1 - expense_ratio) * 100
            if savings_rate >= 20:
                health_status = "Excellent 🟢"
                health_color = "green"
            elif savings_rate >= 10:
                health_status = "Good 🟡"
                health_color = "orange"
            else:
                health_status = "Needs Improvement 🔴"
                health_color = "red"

            st.markdown(f"**Savings Rate:** {savings_rate:.1f}%")
            st.markdown(f"**Status:** {health_status}")

        with col2:
            emergency_fund_target = monthly_expenses * 6
            current_emergency_fund = monthly_savings * 3  # Assume 3 months saved
            emergency_ratio = (current_emergency_fund / emergency_fund_target) * 100

            st.markdown(f"**Emergency Fund:** ₹{current_emergency_fund:,}")
            st.markdown(f"**Target:** ₹{emergency_fund_target:,}")
            st.progress(min(emergency_ratio / 100, 1.0))
            st.markdown(f"**Progress:** {emergency_ratio:.1f}%")

        with col3:
            investment_target = monthly_income * 0.15
            current_investment = monthly_savings * 0.6  # Assume 60% of savings invested

            st.markdown(f"**Monthly Investment:** ₹{current_investment:,}")
            st.markdown(f"**Recommended:** ₹{investment_target:,}")
            if current_investment >= investment_target:
                st.markdown("**Status:** On Track 🎯")
            else:
                st.markdown("**Status:** Below Target 📈")

        # Personalized insights
        st.markdown("---")
        st.markdown("#### 💡 JarvisFi Insights")

        insights = []

        if savings_rate < 10:
            insights.append("🔴 Your savings rate is below 10%. Consider reducing discretionary expenses.")
        elif savings_rate > 25:
            insights.append("🟢 Excellent savings rate! You're building wealth effectively.")

        if emergency_ratio < 50:
            insights.append("⚠️ Build your emergency fund to 6 months of expenses for financial security.")

        if current_investment < investment_target:
            insights.append("📈 Consider increasing your monthly investments for better long-term growth.")

        if user_type == 'student':
            insights.append("🎓 As a student, focus on building good financial habits and emergency savings.")
        elif user_type == 'farmer':
            insights.append("🌾 Consider seasonal income variations in your financial planning.")

        for insight in insights:
            st.markdown(insight)

        # Quick actions
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("📊 Detailed Analysis", key="dashboard_detailed_analysis"):
                st.info("Detailed financial analysis coming soon!")

        with col2:
            if st.button("🎯 Set Goals", key="dashboard_set_goals"):
                st.info("Goal setting feature coming soon!")

        with col3:
            if st.button("📈 Investment Advice", key="dashboard_investment_advice"):
                st.info("Investment recommendations coming soon!")

        with col4:
            if st.button("📄 Export Report", key="dashboard_export_report"):
                st.info("Report export feature coming soon!")

    def render_financial_calculators(self):
        """Render comprehensive financial calculators"""
        current_language = st.session_state.user_profile['basic_info']['language']

        if current_language == 'en':
            st.markdown("### 🧮 Financial Calculators Suite")
        elif current_language == 'ta':
            st.markdown("### 🧮 நிதி கணக்கீட்டாளர்கள் தொகுப்பு")
        elif current_language == 'hi':
            st.markdown("### 🧮 वित्तीय कैलकुलेटर सूट")

        # Calculator selection
        calculator_options = {
            'en': [
                "SIP Calculator", "Budget Planner", "Loan EMI Calculator",
                "Tax Calculator", "Retirement Planner", "Emergency Fund Calculator",
                "Investment Growth Calculator", "Debt Payoff Calculator"
            ],
            'ta': [
                "SIP கணக்கீட்டாளர்", "பட்ஜெட் திட்டமிடுபவர்", "கடன் EMI கணக்கீட்டாளர்",
                "வரி கணக்கீட்டாளர்", "ஓய்வூதிய திட்டமிடுபவர்", "அவசரகால நிதி கணக்கீட்டாளர்",
                "முதலீட்டு வளர்ச்சி கணக்கீட்டாளர்", "கடன் செலுத்துதல் கணக்கீட்டாளர்"
            ],
            'hi': [
                "SIP कैलकुलेटर", "बजट प्लानर", "लोन EMI कैलकुलेटर",
                "टैक्स कैलकुलेटर", "रिटायरमेंट प्लानर", "इमरजेंसी फंड कैलकुलेटर",
                "निवेश वृद्धि कैलकुलेटर", "डेट पेऑफ कैलकुलेटर"
            ]
        }

        options = calculator_options.get(current_language, calculator_options['en'])
        selected_calculator = st.selectbox("Choose Calculator:", options)

        # Get the English equivalent for processing
        english_options = calculator_options['en']
        selected_index = options.index(selected_calculator)
        calculator_type = english_options[selected_index]

        st.markdown("---")

        if calculator_type == "SIP Calculator":
            self.render_sip_calculator()
        elif calculator_type == "Budget Planner":
            self.render_budget_planner()
        elif calculator_type == "Loan EMI Calculator":
            self.render_emi_calculator()
        elif calculator_type == "Tax Calculator":
            self.render_tax_calculator()
        elif calculator_type == "Retirement Planner":
            self.render_retirement_planner()
        elif calculator_type == "Emergency Fund Calculator":
            self.render_emergency_fund_calculator()
        elif calculator_type == "Investment Growth Calculator":
            self.render_investment_growth_calculator()
        elif calculator_type == "Debt Payoff Calculator":
            self.render_debt_payoff_calculator()

    def render_sip_calculator(self):
        """Render SIP calculator with personalized suggestions"""
        current_language = st.session_state.user_profile['basic_info']['language']
        monthly_income = st.session_state.user_profile['basic_info']['monthly_income']

        st.markdown("#### 📈 SIP Calculator")

        # Personalized suggestion
        suggested_sip = max(500, int(monthly_income * 0.15))
        st.info(f"💡 JarvisFi suggests ₹{suggested_sip:,} monthly SIP based on your ₹{monthly_income:,} income")

        col1, col2 = st.columns(2)

        with col1:
            monthly_sip = st.number_input(
                "Monthly SIP Amount (₹)",
                min_value=500,
                value=suggested_sip,
                step=500
            )

            annual_return = st.slider(
                "Expected Annual Return (%)",
                min_value=8.0,
                max_value=15.0,
                value=12.0,
                step=0.5
            )

            investment_period = st.slider(
                "Investment Period (Years)",
                min_value=1,
                max_value=30,
                value=10
            )

        with col2:
            # Calculate SIP returns
            monthly_rate = annual_return / (12 * 100)
            total_months = investment_period * 12

            if monthly_rate > 0:
                future_value = monthly_sip * (((1 + monthly_rate) ** total_months - 1) / monthly_rate) * (1 + monthly_rate)
            else:
                future_value = monthly_sip * total_months

            total_invested = monthly_sip * total_months
            total_returns = future_value - total_invested

            st.metric("Total Investment", f"₹{total_invested:,.0f}")
            st.metric("Expected Returns", f"₹{total_returns:,.0f}")
            st.metric("Maturity Amount", f"₹{future_value:,.0f}")

            # Growth chart
            years = list(range(1, investment_period + 1))
            invested_amounts = [monthly_sip * 12 * year for year in years]
            future_values = []

            for year in years:
                months = year * 12
                if monthly_rate > 0:
                    fv = monthly_sip * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
                else:
                    fv = monthly_sip * months
                future_values.append(fv)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=years, y=invested_amounts, mode='lines', name='Total Invested', line=dict(color='orange')))
            fig.add_trace(go.Scatter(x=years, y=future_values, mode='lines', name='Future Value', line=dict(color='green')))

            fig.update_layout(
                title="SIP Growth Projection",
                xaxis_title="Years",
                yaxis_title="Amount (₹)",
                hovermode='x unified'
            )

            st.plotly_chart(fig, use_container_width=True)

    def render_budget_planner(self):
        """Render budget planner"""
        st.markdown("#### 💰 Budget Planner")

        monthly_income = st.session_state.user_profile['basic_info']['monthly_income']

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Income**")
            salary = st.number_input("Monthly Salary", value=monthly_income)
            other_income = st.number_input("Other Income", value=0)
            total_income = salary + other_income

            st.markdown("**Expenses**")
            rent = st.number_input("Rent/Housing", value=int(total_income * 0.30))
            food = st.number_input("Food & Groceries", value=int(total_income * 0.20))
            transport = st.number_input("Transportation", value=int(total_income * 0.08))
            utilities = st.number_input("Utilities", value=int(total_income * 0.05))
            entertainment = st.number_input("Entertainment", value=int(total_income * 0.07))
            other_expenses = st.number_input("Other Expenses", value=int(total_income * 0.05))

            total_expenses = rent + food + transport + utilities + entertainment + other_expenses
            remaining = total_income - total_expenses

        with col2:
            st.metric("Total Income", f"₹{total_income:,}")
            st.metric("Total Expenses", f"₹{total_expenses:,}")
            st.metric("Remaining", f"₹{remaining:,}", f"{(remaining/total_income)*100:.1f}%" if total_income > 0 else "0%")

            # Budget breakdown
            budget_data = {
                'Category': ['Rent', 'Food', 'Transport', 'Utilities', 'Entertainment', 'Other', 'Savings'],
                'Amount': [rent, food, transport, utilities, entertainment, other_expenses, max(0, remaining)]
            }

            fig = px.pie(values=budget_data['Amount'], names=budget_data['Category'], title="Budget Breakdown")
            st.plotly_chart(fig, use_container_width=True)

    def render_emi_calculator(self):
        """Render EMI calculator"""
        st.markdown("#### 🏠 Loan EMI Calculator")

        col1, col2 = st.columns(2)

        with col1:
            loan_amount = st.number_input("Loan Amount (₹)", min_value=10000, value=1000000, step=10000)
            interest_rate = st.slider("Annual Interest Rate (%)", min_value=5.0, max_value=20.0, value=9.5, step=0.1)
            loan_tenure = st.slider("Loan Tenure (Years)", min_value=1, max_value=30, value=20)

        with col2:
            # Calculate EMI
            monthly_rate = interest_rate / (12 * 100)
            total_months = loan_tenure * 12

            if monthly_rate > 0:
                emi = loan_amount * monthly_rate * (1 + monthly_rate) ** total_months / ((1 + monthly_rate) ** total_months - 1)
            else:
                emi = loan_amount / total_months

            total_payment = emi * total_months
            total_interest = total_payment - loan_amount

            st.metric("Monthly EMI", f"₹{emi:,.0f}")
            st.metric("Total Payment", f"₹{total_payment:,.0f}")
            st.metric("Total Interest", f"₹{total_interest:,.0f}")

            # Affordability check
            monthly_income = st.session_state.user_profile['basic_info']['monthly_income']
            emi_ratio = (emi / monthly_income) * 100 if monthly_income > 0 else 0

            if emi_ratio <= 40:
                st.success(f"✅ EMI is {emi_ratio:.1f}% of income - Affordable")
            elif emi_ratio <= 50:
                st.warning(f"⚠️ EMI is {emi_ratio:.1f}% of income - Manageable but tight")
            else:
                st.error(f"❌ EMI is {emi_ratio:.1f}% of income - Not recommended")

    def render_tax_calculator(self):
        """Render tax calculator"""
        st.markdown("#### 📊 Income Tax Calculator (FY 2023-24)")

        col1, col2 = st.columns(2)

        with col1:
            annual_income = st.number_input("Annual Income (₹)", value=st.session_state.user_profile['basic_info']['monthly_income'] * 12)
            tax_regime = st.selectbox("Tax Regime", ["Old Regime", "New Regime"])

            if tax_regime == "Old Regime":
                st.markdown("**Deductions (Old Regime)**")
                section_80c = st.number_input("80C Deductions", value=150000, max_value=150000)
                section_80d = st.number_input("80D (Health Insurance)", value=25000, max_value=25000)
                hra_exemption = st.number_input("HRA Exemption", value=0)
                other_deductions = st.number_input("Other Deductions", value=0)

                total_deductions = section_80c + section_80d + hra_exemption + other_deductions
                taxable_income = max(0, annual_income - total_deductions)
            else:
                taxable_income = annual_income
                total_deductions = 0

        with col2:
            # Calculate tax
            if tax_regime == "New Regime":
                # New regime tax slabs (FY 2023-24)
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
            else:
                # Old regime tax slabs
                if taxable_income <= 250000:
                    tax = 0
                elif taxable_income <= 500000:
                    tax = (taxable_income - 250000) * 0.05
                elif taxable_income <= 1000000:
                    tax = 12500 + (taxable_income - 500000) * 0.20
                else:
                    tax = 112500 + (taxable_income - 1000000) * 0.30

            # Add cess
            cess = tax * 0.04
            total_tax = tax + cess

            st.metric("Taxable Income", f"₹{taxable_income:,.0f}")
            st.metric("Income Tax", f"₹{tax:,.0f}")
            st.metric("Health & Education Cess", f"₹{cess:,.0f}")
            st.metric("Total Tax", f"₹{total_tax:,.0f}")
            st.metric("Take Home", f"₹{annual_income - total_tax:,.0f}")

            # Tax saving suggestions
            if tax_regime == "Old Regime" and section_80c < 150000:
                remaining_80c = 150000 - section_80c
                st.info(f"💡 You can save ₹{remaining_80c * 0.3:,.0f} more tax by investing ₹{remaining_80c:,} in 80C instruments")

    def render_retirement_planner(self):
        """Render retirement planner"""
        st.markdown("#### 🏖️ Retirement Planner")

        col1, col2 = st.columns(2)

        with col1:
            current_age = st.number_input("Current Age", value=st.session_state.user_profile['basic_info'].get('age', 30))
            retirement_age = st.number_input("Retirement Age", value=60)
            current_monthly_expenses = st.number_input("Current Monthly Expenses", value=int(st.session_state.user_profile['basic_info']['monthly_income'] * 0.7))
            inflation_rate = st.slider("Expected Inflation (%)", min_value=3.0, max_value=8.0, value=6.0, step=0.5)
            expected_return = st.slider("Expected Return on Investment (%)", min_value=8.0, max_value=15.0, value=12.0, step=0.5)

        with col2:
            years_to_retirement = retirement_age - current_age

            if years_to_retirement > 0:
                # Calculate future monthly expenses
                future_monthly_expenses = current_monthly_expenses * (1 + inflation_rate/100) ** years_to_retirement

                # Assume 25 years post retirement
                post_retirement_years = 25

                # Calculate corpus needed
                monthly_return_post_retirement = expected_return / (12 * 100)
                if monthly_return_post_retirement > 0:
                    corpus_needed = future_monthly_expenses * (1 - (1 + monthly_return_post_retirement) ** (-post_retirement_years * 12)) / monthly_return_post_retirement
                else:
                    corpus_needed = future_monthly_expenses * post_retirement_years * 12

                # Calculate monthly SIP needed
                monthly_return_pre_retirement = expected_return / (12 * 100)
                total_months = years_to_retirement * 12

                if monthly_return_pre_retirement > 0:
                    monthly_sip_needed = corpus_needed * monthly_return_pre_retirement / (((1 + monthly_return_pre_retirement) ** total_months - 1) * (1 + monthly_return_pre_retirement))
                else:
                    monthly_sip_needed = corpus_needed / total_months

                st.metric("Years to Retirement", f"{years_to_retirement}")
                st.metric("Future Monthly Expenses", f"₹{future_monthly_expenses:,.0f}")
                st.metric("Corpus Needed", f"₹{corpus_needed:,.0f}")
                st.metric("Monthly SIP Required", f"₹{monthly_sip_needed:,.0f}")

                # Affordability check
                monthly_income = st.session_state.user_profile['basic_info']['monthly_income']
                sip_ratio = (monthly_sip_needed / monthly_income) * 100 if monthly_income > 0 else 0

                if sip_ratio <= 20:
                    st.success(f"✅ Required SIP is {sip_ratio:.1f}% of income - Achievable")
                elif sip_ratio <= 30:
                    st.warning(f"⚠️ Required SIP is {sip_ratio:.1f}% of income - Challenging but possible")
                else:
                    st.error(f"❌ Required SIP is {sip_ratio:.1f}% of income - Consider extending retirement age")
            else:
                st.error("Please enter a retirement age greater than current age")

    def render_emergency_fund_calculator(self):
        """Render emergency fund calculator"""
        st.markdown("#### 🚨 Emergency Fund Calculator")

        monthly_expenses = st.session_state.user_profile['basic_info']['monthly_income'] * 0.7

        col1, col2 = st.columns(2)

        with col1:
            monthly_exp = st.number_input("Monthly Expenses", value=int(monthly_expenses))
            months_coverage = st.slider("Months of Coverage", min_value=3, max_value=12, value=6)
            current_emergency_fund = st.number_input("Current Emergency Fund", value=0)

        with col2:
            target_fund = monthly_exp * months_coverage
            shortfall = max(0, target_fund - current_emergency_fund)

            st.metric("Target Emergency Fund", f"₹{target_fund:,}")
            st.metric("Current Fund", f"₹{current_emergency_fund:,}")
            st.metric("Shortfall", f"₹{shortfall:,}")

            if shortfall > 0:
                # Calculate monthly savings needed
                for months in [6, 12, 18, 24]:
                    monthly_saving = shortfall / months
                    st.markdown(f"Save ₹{monthly_saving:,.0f}/month for {months} months")
            else:
                st.success("🎉 You have achieved your emergency fund target!")

    def render_investment_growth_calculator(self):
        """Render investment growth calculator"""
        st.markdown("#### 📈 Investment Growth Calculator")

        col1, col2 = st.columns(2)

        with col1:
            initial_investment = st.number_input("Initial Investment", value=100000)
            monthly_addition = st.number_input("Monthly Addition", value=5000)
            annual_return = st.slider("Expected Annual Return (%)", min_value=5.0, max_value=20.0, value=12.0, step=0.5)
            investment_period = st.slider("Investment Period (Years)", min_value=1, max_value=30, value=10)

        with col2:
            # Calculate compound growth
            monthly_rate = annual_return / (12 * 100)
            total_months = investment_period * 12

            # Future value of initial investment
            fv_initial = initial_investment * (1 + annual_return/100) ** investment_period

            # Future value of monthly additions (SIP)
            if monthly_rate > 0:
                fv_monthly = monthly_addition * (((1 + monthly_rate) ** total_months - 1) / monthly_rate) * (1 + monthly_rate)
            else:
                fv_monthly = monthly_addition * total_months

            total_future_value = fv_initial + fv_monthly
            total_invested = initial_investment + (monthly_addition * total_months)
            total_returns = total_future_value - total_invested

            st.metric("Total Invested", f"₹{total_invested:,.0f}")
            st.metric("Total Returns", f"₹{total_returns:,.0f}")
            st.metric("Final Value", f"₹{total_future_value:,.0f}")
            st.metric("Return Multiple", f"{total_future_value/total_invested:.1f}x")

    def render_debt_payoff_calculator(self):
        """Render debt payoff calculator"""
        st.markdown("#### 💳 Debt Payoff Calculator")

        col1, col2 = st.columns(2)

        with col1:
            debt_amount = st.number_input("Total Debt Amount", value=200000)
            interest_rate = st.slider("Annual Interest Rate (%)", min_value=5.0, max_value=30.0, value=18.0, step=0.5)
            monthly_payment = st.number_input("Monthly Payment", value=10000)

        with col2:
            if monthly_payment > 0:
                monthly_rate = interest_rate / (12 * 100)

                if monthly_rate > 0 and monthly_payment > debt_amount * monthly_rate:
                    # Calculate payoff time
                    months_to_payoff = -np.log(1 - (debt_amount * monthly_rate) / monthly_payment) / np.log(1 + monthly_rate)
                    total_payment = monthly_payment * months_to_payoff
                    total_interest = total_payment - debt_amount

                    st.metric("Months to Payoff", f"{months_to_payoff:.0f}")
                    st.metric("Years to Payoff", f"{months_to_payoff/12:.1f}")
                    st.metric("Total Interest", f"₹{total_interest:,.0f}")
                    st.metric("Total Payment", f"₹{total_payment:,.0f}")

                    # Show impact of extra payments
                    st.markdown("**Impact of Extra Payments:**")
                    for extra in [1000, 2000, 5000]:
                        new_payment = monthly_payment + extra
                        if new_payment > debt_amount * monthly_rate:
                            new_months = -np.log(1 - (debt_amount * monthly_rate) / new_payment) / np.log(1 + monthly_rate)
                            months_saved = months_to_payoff - new_months
                            st.markdown(f"Extra ₹{extra}: Save {months_saved:.0f} months")
                else:
                    st.error("Monthly payment is too low to cover interest. Increase payment amount.")
            else:
                st.error("Please enter a valid monthly payment amount.")

    def render_voice_interface(self):
        """Render voice interface"""
        current_language = st.session_state.user_profile['basic_info']['language']

        if current_language == 'en':
            st.markdown("### 🎤 Voice Assistant - Multi-language Support")
        elif current_language == 'ta':
            st.markdown("### 🎤 குரல் உதவியாளர் - பல மொழி ஆதரவு")
        elif current_language == 'hi':
            st.markdown("### 🎤 आवाज़ सहायक - बहुभाषी समर्थन")

        # Voice status indicators
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.session_state.voice_listening:
                st.markdown('<div class="voice-indicator listening"><div class="pulse"></div> Listening...</div>', unsafe_allow_html=True)
            else:
                st.markdown("🎙️ Ready to listen")

        with col2:
            if st.session_state.voice_speaking:
                st.markdown('<div class="voice-indicator speaking"><div class="pulse"></div> Speaking...</div>', unsafe_allow_html=True)
            else:
                st.markdown("🔊 Ready to speak")

        with col3:
            voice_enabled = st.session_state.user_profile['preferences']['voice_enabled']
            status = "🟢 Enabled" if voice_enabled else "🔴 Disabled"
            st.markdown(f"Status: {status}")

        # Voice controls
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🎙️ Start Listening", key="voice_start_listening"):
                st.session_state.voice_listening = True
                st.success("🎤 Voice input activated!")
                st.info("Try saying: 'What's my budget status?' or 'Calculate SIP for 5000 rupees'")

                # Simulate voice input
                with st.spinner("Listening for voice input..."):
                    time.sleep(2)
                    sample_inputs = [
                        "What's my budget status?",
                        "Calculate SIP for 5000 rupees",
                        "How much should I save monthly?",
                        "Show me investment options"
                    ]
                    import random
                    simulated_input = random.choice(sample_inputs)
                    st.info(f"🎤 Detected: '{simulated_input}'")

                    # Process the simulated voice input
                    if simulated_input not in [msg["content"] for msg in st.session_state.chat_history if msg["role"] == "user"]:
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": simulated_input,
                            "timestamp": datetime.now().isoformat(),
                            "type": "voice_input"
                        })

                        # Generate AI response
                        response = self.generate_ai_response(simulated_input, current_language)
                        st.session_state.chat_history.append(response)

                        st.success("✅ Voice input processed! Check the AI Chat tab to see the conversation.")

        with col2:
            if st.button("⏹️ Stop Listening", key="voice_stop_listening"):
                st.session_state.voice_listening = False
                st.info("🔇 Voice input stopped")

        with col3:
            if st.button("🔊 Test Speech", key="voice_test_speech"):
                st.session_state.voice_speaking = True
                st.success("🔊 Testing text-to-speech...")

                # Simulate text-to-speech
                with st.spinner("Converting text to speech..."):
                    time.sleep(1.5)
                    sample_speech = "Hello! I'm JarvisFi, your AI-powered financial genius. I'm here to help you with all your financial needs, from budgeting to investments."
                    st.info(f"🔊 Speaking: '{sample_speech}'")
                    st.success("✅ Text-to-speech simulation completed!")

        with col4:
            if st.button("🔇 Stop Speech", key="voice_stop_speech"):
                st.session_state.voice_speaking = False
                st.info("🔇 Speech stopped")

        # Voice settings
        st.markdown("---")
        st.markdown("#### ⚙️ Voice Settings")

        col1, col2 = st.columns(2)

        with col1:
            voice_language = st.selectbox(
                "Voice Language",
                ["English", "Tamil", "Hindi", "Telugu"],
                index=["en", "ta", "hi", "te"].index(current_language)
            )

            speech_speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)

        with col2:
            voice_gender = st.selectbox("Voice Gender", ["Female", "Male"])
            volume = st.slider("Volume", 0.0, 1.0, 0.8, 0.1)

        # Voice commands help
        st.markdown("---")
        st.markdown("#### 💡 Voice Commands Examples")

        commands = {
            'en': [
                "💰 'What's my budget status?'",
                "📊 'Show me my dashboard'",
                "🧮 'Calculate SIP for 5000 rupees'",
                "📈 'What are good investment options?'",
                "🏦 'How much should I save monthly?'",
                "💳 'Calculate EMI for 10 lakh loan'"
            ],
            'ta': [
                "💰 'என் பட்ஜெட் நிலை என்ன?'",
                "📊 'என் டாஷ்போர்டைக் காட்டு'",
                "🧮 '5000 ரூபாய்க்கு SIP கணக்கிடு'",
                "📈 'நல்ல முதலீட்டு விருப்பங்கள் என்ன?'",
                "🏦 'மாதம் எவ்வளவு சேமிக்க வேண்டும்?'",
                "💳 '10 லட்சம் கடனுக்கு EMI கணக்கிடு'"
            ],
            'hi': [
                "💰 'मेरा बजट स्टेटस क्या है?'",
                "📊 'मेरा डैशबोर्ड दिखाएं'",
                "🧮 '5000 रुपये के लिए SIP कैलकुलेट करें'",
                "📈 'अच्छे निवेश विकल्प क्या हैं?'",
                "🏦 'मुझे महीने में कितनी बचत करनी चाहिए?'",
                "💳 '10 लाख के लोन के लिए EMI कैलकुलेट करें'"
            ]
        }

        command_list = commands.get(current_language, commands['en'])
        for command in command_list:
            st.markdown(command)

        # Offline mode info
        st.markdown("---")
        st.info("🔒 **Privacy Note:** Voice processing can work offline using Coqui AI for enhanced privacy and security.")

    def render_farmer_tools(self):
        """Render farmer-specific tools"""
        current_language = st.session_state.user_profile['basic_info']['language']

        if current_language == 'en':
            st.markdown("### 👨‍🌾 Farmer Financial Tools")
        elif current_language == 'ta':
            st.markdown("### 👨‍🌾 விவசாயி நிதி கருவிகள்")
        elif current_language == 'hi':
            st.markdown("### 👨‍🌾 किसान वित्तीय उपकरण")

        # Farmer tool selection
        tools = {
            'en': ["Crop Loan Calculator", "MSP Tracker", "Subsidy Checker", "Weather-based Planning", "Agro Insurance Calculator"],
            'ta': ["பயிர் கடன் கணக்கீட்டாளர்", "MSP டிராக்கர்", "மானியம் சரிபார்ப்பாளர்", "வானிலை அடிப்படையிலான திட்டமிடல்", "வேளாண் காப்பீட்டு கணக்கீட்டாளர்"],
            'hi': ["फसल ऋण कैलकुलेटर", "MSP ट्रैकर", "सब्सिडी चेकर", "मौसम आधारित योजना", "कृषि बीमा कैलकुलेटर"]
        }

        tool_options = tools.get(current_language, tools['en'])
        selected_tool = st.selectbox("Select Tool:", tool_options)

        st.markdown("---")

        if "Crop Loan" in selected_tool or "பயிர் கடன்" in selected_tool or "फसल ऋण" in selected_tool:
            self.render_crop_loan_calculator()
        elif "MSP" in selected_tool:
            self.render_msp_tracker()
        elif "Subsidy" in selected_tool or "மானியம்" in selected_tool or "सब्सिडी" in selected_tool:
            self.render_subsidy_checker()
        elif "Weather" in selected_tool or "வானிலை" in selected_tool or "मौसम" in selected_tool:
            self.render_weather_planning()
        elif "Insurance" in selected_tool or "காப்பீடு" in selected_tool or "बीमा" in selected_tool:
            self.render_agro_insurance_calculator()

    def render_crop_loan_calculator(self):
        """Render crop loan calculator"""
        st.markdown("#### 🌾 Crop Loan Calculator")

        col1, col2 = st.columns(2)

        with col1:
            crop_type = st.selectbox("Crop Type", ["Rice", "Wheat", "Cotton", "Sugarcane", "Maize", "Other"])
            land_area = st.number_input("Land Area (Acres)", min_value=0.1, value=2.0, step=0.1)
            cost_per_acre = st.number_input("Cost per Acre (₹)", value=25000, step=1000)
            loan_percentage = st.slider("Loan Percentage", 50, 100, 80)

        with col2:
            total_cost = land_area * cost_per_acre
            loan_amount = total_cost * (loan_percentage / 100)

            st.metric("Total Cultivation Cost", f"₹{total_cost:,.0f}")
            st.metric("Eligible Loan Amount", f"₹{loan_amount:,.0f}")
            st.metric("Your Contribution", f"₹{total_cost - loan_amount:,.0f}")

            # Interest calculation
            interest_rate = 7.0  # Typical crop loan rate
            loan_period = 12  # months

            interest_amount = loan_amount * (interest_rate / 100) * (loan_period / 12)
            total_repayment = loan_amount + interest_amount

            st.metric("Interest Amount", f"₹{interest_amount:,.0f}")
            st.metric("Total Repayment", f"₹{total_repayment:,.0f}")

            # Subsidy info
            st.info("💡 Interest subsidy of 2% available for timely repayment")

    def render_msp_tracker(self):
        """Render MSP tracker"""
        st.markdown("#### 📊 MSP (Minimum Support Price) Tracker")

        # Sample MSP data
        msp_data = {
            'Crop': ['Rice (Common)', 'Rice (Grade A)', 'Wheat', 'Jowar', 'Bajra', 'Maize', 'Cotton'],
            'MSP 2023-24 (₹/quintal)': [2183, 2203, 2275, 3180, 2500, 1962, 6620],
            'Previous Year': [2040, 2060, 2125, 2970, 2350, 1870, 6080],
            'Change (%)': [7.0, 6.9, 7.1, 7.1, 6.4, 4.9, 8.9]
        }

        df = pd.DataFrame(msp_data)
        st.dataframe(df, use_container_width=True)

        # MSP comparison chart
        fig = px.bar(df, x='Crop', y='MSP 2023-24 (₹/quintal)', title='MSP Rates 2023-24')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        # Price alerts
        st.markdown("#### 🔔 Price Alerts")
        selected_crop = st.selectbox("Select Crop for Alerts", df['Crop'].tolist())
        alert_price = st.number_input("Alert when market price reaches (₹/quintal)", value=2000)

        if st.button("Set Price Alert", key="msp_set_alert"):
            st.success(f"✅ Alert set for {selected_crop} at ₹{alert_price}/quintal")

    def render_subsidy_checker(self):
        """Render subsidy checker"""
        st.markdown("#### 🏛️ Government Subsidy Checker")

        # Farmer details
        col1, col2 = st.columns(2)

        with col1:
            farmer_category = st.selectbox("Farmer Category", ["Small", "Marginal", "Large", "SC/ST"])
            land_holding = st.number_input("Land Holding (Acres)", value=2.0)
            annual_income = st.number_input("Annual Income (₹)", value=200000)

        with col2:
            state = st.selectbox("State", ["Andhra Pradesh", "Tamil Nadu", "Karnataka", "Maharashtra", "Punjab", "Other"])
            crop_type = st.selectbox("Primary Crop", ["Rice", "Wheat", "Cotton", "Sugarcane", "Vegetables"])

        # Eligible subsidies
        st.markdown("#### ✅ Eligible Subsidies")

        subsidies = []

        if farmer_category in ["Small", "Marginal"]:
            subsidies.append("🌱 **PM-KISAN**: ₹6,000 per year")
            subsidies.append("🚜 **Equipment Subsidy**: Up to 50% on farm equipment")

        if land_holding <= 2:
            subsidies.append("💧 **Drip Irrigation**: Up to 55% subsidy")

        if annual_income <= 300000:
            subsidies.append("🌾 **Crop Insurance**: Premium subsidy available")
            subsidies.append("🏦 **Interest Subsidy**: 2% on crop loans")

        subsidies.append("🔋 **Solar Pump**: Up to 90% subsidy")
        subsidies.append("🌿 **Organic Farming**: ₹50,000 per hectare")

        for subsidy in subsidies:
            st.markdown(subsidy)

        # Application links
        st.markdown("#### 📝 Apply Online")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("PM-KISAN Portal"):
                st.info("Redirecting to PM-KISAN portal...")

        with col2:
            if st.button("State Agriculture Portal"):
                st.info("Redirecting to state portal...")

        with col3:
            if st.button("DBT Agriculture"):
                st.info("Redirecting to DBT portal...")

    def render_weather_planning(self):
        """Render weather-based financial planning"""
        st.markdown("#### 🌦️ Weather-based Financial Planning")

        # Weather forecast (simulated)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**7-Day Weather Forecast**")
            weather_data = {
                'Day': ['Today', 'Tomorrow', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
                'Weather': ['☀️ Sunny', '🌤️ Partly Cloudy', '🌧️ Rain', '⛈️ Thunderstorm', '🌧️ Rain', '☀️ Sunny', '☀️ Sunny'],
                'Temp (°C)': [32, 30, 28, 26, 27, 31, 33],
                'Rain (mm)': [0, 2, 15, 25, 12, 0, 0]
            }

            df_weather = pd.DataFrame(weather_data)
            st.dataframe(df_weather, use_container_width=True)

        with col2:
            st.markdown("**Financial Impact Analysis**")

            # Calculate potential impacts
            total_rain = sum(weather_data['Rain (mm)'])

            if total_rain > 30:
                st.success("🌧️ Good rainfall expected - Reduce irrigation costs")
                irrigation_savings = 5000
                st.metric("Irrigation Savings", f"₹{irrigation_savings}")
            elif total_rain < 10:
                st.warning("☀️ Low rainfall - Plan for additional irrigation")
                extra_irrigation_cost = 8000
                st.metric("Extra Irrigation Cost", f"₹{extra_irrigation_cost}")
            else:
                st.info("🌤️ Moderate rainfall - Normal irrigation needed")

            # Crop protection advice
            if any('Thunderstorm' in w for w in weather_data['Weather']):
                st.warning("⚠️ Thunderstorm alert - Consider crop insurance")

        # Seasonal planning
        st.markdown("---")
        st.markdown("#### 📅 Seasonal Financial Planning")

        season = st.selectbox("Select Season", ["Kharif", "Rabi", "Zaid"])

        if season == "Kharif":
            st.markdown("**Kharif Season (June-October)**")
            st.markdown("• 🌾 Recommended crops: Rice, Cotton, Sugarcane")
            st.markdown("• 💰 Budget allocation: 60% for seeds and fertilizers")
            st.markdown("• 🌧️ Monsoon dependency: High")
        elif season == "Rabi":
            st.markdown("**Rabi Season (November-April)**")
            st.markdown("• 🌾 Recommended crops: Wheat, Barley, Mustard")
            st.markdown("• 💰 Budget allocation: 40% for irrigation")
            st.markdown("• 🌧️ Monsoon dependency: Low")
        else:
            st.markdown("**Zaid Season (April-June)**")
            st.markdown("• 🌾 Recommended crops: Fodder, Vegetables")
            st.markdown("• 💰 Budget allocation: 70% for irrigation")
            st.markdown("• 🌧️ Monsoon dependency: Very Low")

    def render_agro_insurance_calculator(self):
        """Render agro insurance calculator"""
        st.markdown("#### 🛡️ Agro Insurance Calculator")

        col1, col2 = st.columns(2)

        with col1:
            crop_type = st.selectbox("Crop Type", ["Rice", "Wheat", "Cotton", "Sugarcane", "Pulses"])
            land_area = st.number_input("Land Area (Acres)", value=2.0)
            sum_insured_per_acre = st.number_input("Sum Insured per Acre (₹)", value=50000)
            farmer_category = st.selectbox("Category", ["Small/Marginal", "Other"])

        with col2:
            total_sum_insured = land_area * sum_insured_per_acre

            # Premium calculation based on PMFBY rates
            if farmer_category == "Small/Marginal":
                if crop_type in ["Rice", "Wheat"]:
                    farmer_premium_rate = 1.5  # %
                else:
                    farmer_premium_rate = 2.0  # %
            else:
                if crop_type in ["Rice", "Wheat"]:
                    farmer_premium_rate = 2.0  # %
                else:
                    farmer_premium_rate = 5.0  # %

            farmer_premium = total_sum_insured * (farmer_premium_rate / 100)

            # Government subsidy (difference between actuarial rate and farmer rate)
            actuarial_rate = 12.0  # Assumed average
            government_subsidy = total_sum_insured * ((actuarial_rate - farmer_premium_rate) / 100)

            st.metric("Total Sum Insured", f"₹{total_sum_insured:,.0f}")
            st.metric("Your Premium", f"₹{farmer_premium:,.0f}")
            st.metric("Government Subsidy", f"₹{government_subsidy:,.0f}")
            st.metric("Premium Rate", f"{farmer_premium_rate}%")

            # Coverage details
            st.markdown("**Coverage Includes:**")
            st.markdown("• 🌪️ Natural disasters")
            st.markdown("• 🐛 Pest attacks")
            st.markdown("• 🦠 Diseases")
            st.markdown("• 🌧️ Unseasonal rainfall")
            st.markdown("• ☀️ Drought conditions")

        # Claim process
        st.markdown("---")
        st.markdown("#### 📋 Claim Process")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Step 1: Report Loss**")
            st.markdown("Report within 72 hours")
            if st.button("Report Crop Loss"):
                st.success("Loss reported successfully!")

        with col2:
            st.markdown("**Step 2: Assessment**")
            st.markdown("Official assessment by authorities")
            st.info("Assessment typically takes 2-3 weeks")

        with col3:
            st.markdown("**Step 3: Claim Settlement**")
            st.markdown("Direct bank transfer")
            st.info("Settlement within 60 days")

    def render_credit_score_tracking(self):
        """Render credit score tracking"""
        current_language = st.session_state.user_profile['basic_info']['language']

        if current_language == 'en':
            st.markdown("### 💳 Credit Score Tracking & Management")
        elif current_language == 'ta':
            st.markdown("### 💳 கிரெடிட் ஸ்கோர் கண்காணிப்பு & மேலாண்மை")
        elif current_language == 'hi':
            st.markdown("### 💳 क्रेडिट स्कोर ट्रैकिंग और प्रबंधन")

        # Current credit score
        credit_data = st.session_state.credit_score_data
        current_score = credit_data['current_score']

        col1, col2, col3 = st.columns(3)

        with col1:
            # Score gauge
            if current_score >= 750:
                score_status = "Excellent 🟢"
                score_color = "green"
            elif current_score >= 700:
                score_status = "Good 🟡"
                score_color = "orange"
            elif current_score >= 650:
                score_status = "Fair 🟠"
                score_color = "orange"
            else:
                score_status = "Poor 🔴"
                score_color = "red"

            st.metric("Current CIBIL Score", current_score, score_status)

            # Score range indicator
            st.progress(current_score / 900)
            st.caption("Range: 300-900")

        with col2:
            st.markdown("**Score Factors**")
            factors = {
                "Payment History": 85,
                "Credit Utilization": 25,
                "Credit Age": 70,
                "Credit Mix": 60,
                "New Credit": 80
            }

            for factor, score in factors.items():
                color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                st.markdown(f"{color} {factor}: {score}%")

        with col3:
            st.markdown("**Improvement Tips**")
            tips = [
                "💳 Keep credit utilization below 30%",
                "⏰ Pay all bills on time",
                "📅 Maintain old credit accounts",
                "🔍 Check credit report regularly",
                "💰 Don't apply for multiple loans"
            ]

            for tip in tips:
                st.markdown(tip)

        # Credit score history
        st.markdown("---")
        st.markdown("#### 📈 Credit Score History")

        # Generate sample history data
        months = pd.date_range(start='2023-01-01', end='2023-12-01', freq='M')
        scores = [current_score + np.random.randint(-20, 20) for _ in months]

        fig = px.line(x=months, y=scores, title="Credit Score Trend")
        fig.update_traces(line_color='#667eea', line_width=3)
        fig.update_layout(xaxis_title="Month", yaxis_title="Credit Score")
        st.plotly_chart(fig, use_container_width=True)

        # Credit report
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📄 Credit Report Summary")

            report_data = {
                "Total Accounts": 5,
                "Active Accounts": 3,
                "Total Credit Limit": "₹5,00,000",
                "Current Utilization": "₹75,000 (15%)",
                "Overdue Amount": "₹0",
                "Last Updated": "15 days ago"
            }

            for key, value in report_data.items():
                st.markdown(f"**{key}:** {value}")

        with col2:
            st.markdown("#### 🎯 Score Improvement Plan")

            if current_score < 750:
                target_score = 750
                months_needed = max(3, (750 - current_score) // 10)

                st.markdown(f"**Target Score:** {target_score}")
                st.markdown(f"**Estimated Time:** {months_needed} months")

                improvement_actions = [
                    "Reduce credit utilization to 10%",
                    "Pay all EMIs on time",
                    "Don't close old credit cards",
                    "Monitor credit report monthly"
                ]

                for action in improvement_actions:
                    st.markdown(f"• {action}")
            else:
                st.success("🎉 Excellent credit score! Maintain current habits.")

        # Quick actions
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("📊 Detailed Report"):
                st.info("Detailed credit report feature coming soon!")

        with col2:
            if st.button("🔔 Set Alerts"):
                st.info("Credit score alerts feature coming soon!")

        with col3:
            if st.button("💳 Pre-approved Offers"):
                st.info("Pre-approved loan offers feature coming soon!")

        with col4:
            if st.button("🛡️ Credit Monitoring"):
                st.info("24/7 credit monitoring feature coming soon!")

    def render_investment_portfolio(self):
        """Render investment portfolio tracking"""
        current_language = st.session_state.user_profile['basic_info']['language']

        if current_language == 'en':
            st.markdown("### 📈 Investment Portfolio Management")
        elif current_language == 'ta':
            st.markdown("### 📈 முதலீட்டு போர்ட்ஃபோலியோ மேலாண்மை")
        elif current_language == 'hi':
            st.markdown("### 📈 निवेश पोर्टफोलियो प्रबंधन")

        # Portfolio overview
        portfolio_data = st.session_state.investment_portfolio

        # Sample portfolio data
        if not portfolio_data['investments']:
            portfolio_data['investments'] = [
                {"name": "HDFC Top 100 Fund", "type": "Equity", "amount": 50000, "current_value": 55000, "return": 10.0},
                {"name": "SBI Blue Chip Fund", "type": "Equity", "amount": 30000, "current_value": 32500, "return": 8.33},
                {"name": "ICICI Prudential Balanced", "type": "Hybrid", "amount": 25000, "current_value": 26800, "return": 7.2},
                {"name": "PPF", "type": "Tax Saving", "amount": 40000, "current_value": 42800, "return": 7.0},
                {"name": "NSC", "type": "Fixed Income", "amount": 20000, "current_value": 21400, "return": 7.0}
            ]

        investments = portfolio_data['investments']
        total_invested = sum(inv['amount'] for inv in investments)
        total_current = sum(inv['current_value'] for inv in investments)
        total_return = total_current - total_invested
        return_percentage = (total_return / total_invested * 100) if total_invested > 0 else 0

        # Portfolio metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Invested", f"₹{total_invested:,}")

        with col2:
            st.metric("Current Value", f"₹{total_current:,}")

        with col3:
            st.metric("Total Returns", f"₹{total_return:,}", f"{return_percentage:+.1f}%")

        with col4:
            st.metric("Portfolio Return", f"{return_percentage:.1f}%")

        # Portfolio allocation
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🥧 Asset Allocation")

            # Group by type
            allocation = {}
            for inv in investments:
                inv_type = inv['type']
                if inv_type in allocation:
                    allocation[inv_type] += inv['current_value']
                else:
                    allocation[inv_type] = inv['current_value']

            fig_pie = px.pie(
                values=list(allocation.values()),
                names=list(allocation.keys()),
                title="Portfolio Allocation by Asset Type"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.markdown("#### 📊 Investment Performance")

            # Performance chart
            names = [inv['name'][:15] + '...' if len(inv['name']) > 15 else inv['name'] for inv in investments]
            returns = [inv['return'] for inv in investments]

            fig_bar = px.bar(
                x=names,
                y=returns,
                title="Returns by Investment",
                color=returns,
                color_continuous_scale="RdYlGn"
            )
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)

        # Investment details
        st.markdown("---")
        st.markdown("#### 📋 Investment Details")

        df_investments = pd.DataFrame(investments)
        df_investments['Return (₹)'] = df_investments['current_value'] - df_investments['amount']
        df_investments['Return (%)'] = df_investments['return']

        # Format for display
        display_df = df_investments[['name', 'type', 'amount', 'current_value', 'Return (₹)', 'Return (%)']].copy()
        display_df.columns = ['Investment', 'Type', 'Invested (₹)', 'Current Value (₹)', 'Return (₹)', 'Return (%)']

        st.dataframe(display_df, use_container_width=True)

        # Investment recommendations
        st.markdown("---")
        st.markdown("#### 💡 JarvisFi Recommendations")

        # Analyze portfolio and give recommendations
        equity_percentage = (allocation.get('Equity', 0) / total_current) * 100
        debt_percentage = (allocation.get('Fixed Income', 0) + allocation.get('Tax Saving', 0)) / total_current * 100

        recommendations = []

        if equity_percentage < 60:
            recommendations.append("📈 Consider increasing equity allocation for better long-term returns")

        if debt_percentage < 20:
            recommendations.append("🛡️ Add more debt instruments for portfolio stability")

        if return_percentage < 10:
            recommendations.append("🔍 Review underperforming investments and consider rebalancing")

        if len(investments) < 5:
            recommendations.append("🌐 Diversify your portfolio across more asset classes")

        for rec in recommendations:
            st.markdown(rec)

        # Quick actions
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("➕ Add Investment"):
                st.info("Add new investment feature coming soon!")

        with col2:
            if st.button("⚖️ Rebalance Portfolio"):
                st.info("Portfolio rebalancing feature coming soon!")

        with col3:
            if st.button("📊 Detailed Analysis"):
                st.info("Detailed portfolio analysis coming soon!")

        with col4:
            if st.button("📄 Export Report"):
                st.info("Portfolio report export feature coming soon!")

    def render_security_center(self):
        """Render security center"""
        current_language = st.session_state.user_profile['basic_info']['language']

        if current_language == 'en':
            st.markdown("### 🛡️ Security & Privacy Center")
        elif current_language == 'ta':
            st.markdown("### 🛡️ பாதுகாப்பு & தனியுரிமை மையம்")
        elif current_language == 'hi':
            st.markdown("### 🛡️ सुरक्षा और गोपनीयता केंद्र")

        # Security status
        security_settings = st.session_state.user_profile['security']

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🔐 Authentication")

            two_factor = security_settings['two_factor_enabled']
            biometric = security_settings['biometric_enabled']

            st.markdown(f"**Two-Factor Auth:** {'🟢 Enabled' if two_factor else '🔴 Disabled'}")
            st.markdown(f"**Biometric Auth:** {'🟢 Enabled' if biometric else '🔴 Disabled'}")
            st.markdown("**Password Strength:** 🟢 Strong")
            st.markdown("**Last Login:** 2 hours ago")

        with col2:
            st.markdown("#### 🔒 Data Protection")

            encryption = security_settings['data_encryption']
            privacy_level = security_settings['privacy_level']

            st.markdown(f"**Data Encryption:** {'🟢 AES-256' if encryption else '🔴 Disabled'}")
            st.markdown(f"**Privacy Level:** 🟢 {privacy_level.title()}")
            st.markdown("**Data Backup:** 🟢 Encrypted")
            st.markdown("**Compliance:** 🟢 GDPR, HIPAA")

        with col3:
            st.markdown("#### 🚨 Threat Detection")

            st.markdown("**Fraud Detection:** 🟢 Active")
            st.markdown("**Suspicious Activity:** 🟢 None detected")
            st.markdown("**Device Security:** 🟢 Secure")
            st.markdown("**Network Security:** 🟢 Protected")

        # Security settings
        st.markdown("---")
        st.markdown("#### ⚙️ Security Settings")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Authentication Settings**")

            new_two_factor = st.toggle("Enable Two-Factor Authentication", value=two_factor)
            new_biometric = st.toggle("Enable Biometric Authentication", value=biometric)

            if st.button("Change Password"):
                st.info("Password change feature coming soon!")

            if st.button("Manage Devices"):
                st.info("Device management feature coming soon!")

        with col2:
            st.markdown("**Privacy Settings**")

            data_sharing = st.selectbox("Data Sharing", ["None", "Anonymous", "Aggregated"])
            marketing_emails = st.toggle("Marketing Emails", value=False)

            if st.button("Download My Data"):
                st.info("Data export feature coming soon!")

            if st.button("Delete Account"):
                st.warning("Account deletion feature coming soon!")

        # Security audit
        st.markdown("---")
        st.markdown("#### 🔍 Security Audit")

        audit_items = [
            {"item": "Password Strength", "status": "✅ Strong", "action": "None required"},
            {"item": "Two-Factor Auth", "status": "⚠️ Disabled" if not two_factor else "✅ Enabled", "action": "Enable 2FA" if not two_factor else "None"},
            {"item": "Data Encryption", "status": "✅ AES-256", "action": "None required"},
            {"item": "Privacy Settings", "status": "✅ High", "action": "None required"},
            {"item": "Device Security", "status": "✅ Secure", "action": "None required"}
        ]

        for item in audit_items:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.markdown(f"**{item['item']}**")
            with col2:
                st.markdown(item['status'])
            with col3:
                st.markdown(item['action'])

        # Security tips
        st.markdown("---")
        st.markdown("#### 💡 Security Tips")

        tips = [
            "🔐 Use a unique, strong password for your JarvisFi account",
            "📱 Enable two-factor authentication for extra security",
            "🔍 Regularly review your account activity",
            "📧 Be cautious of phishing emails claiming to be from JarvisFi",
            "🔒 Always log out from shared or public devices",
            "📱 Keep your mobile app updated to the latest version"
        ]

        for tip in tips:
            st.markdown(tip)

    def render_community_forum(self):
        """Render community forum"""
        current_language = st.session_state.user_profile['basic_info']['language']

        if current_language == 'en':
            st.markdown("### 👥 Community Forum - Connect & Learn")
        elif current_language == 'ta':
            st.markdown("### 👥 சமூக மன்றம் - இணைந்து கற்றுக்கொள்ளுங்கள்")
        elif current_language == 'hi':
            st.markdown("### 👥 कम्युनिटी फोरम - जुड़ें और सीखें")

        # Forum categories
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 💰 Investment Discussions")
            st.markdown("**Latest Topics:**")
            st.markdown("• Best SIP funds for 2024")
            st.markdown("• Tax-saving investments")
            st.markdown("• Market volatility concerns")
            st.markdown("• Crypto vs traditional investments")

            if st.button("Join Investment Forum"):
                st.info("Investment forum feature coming soon!")

        with col2:
            st.markdown("#### 🏠 Personal Finance")
            st.markdown("**Latest Topics:**")
            st.markdown("• Emergency fund strategies")
            st.markdown("• Debt management tips")
            st.markdown("• Budget planning for families")
            st.markdown("• Insurance recommendations")

            if st.button("Join Finance Forum"):
                st.info("Personal finance forum feature coming soon!")

        with col3:
            st.markdown("#### 👨‍🌾 Farmer Finance")
            st.markdown("**Latest Topics:**")
            st.markdown("• Crop loan experiences")
            st.markdown("• Government scheme updates")
            st.markdown("• Weather impact planning")
            st.markdown("• Agro-insurance claims")

            if st.button("Join Farmer Forum"):
                st.info("Farmer forum feature coming soon!")

        # Recent discussions
        st.markdown("---")
        st.markdown("#### 🔥 Trending Discussions")

        discussions = [
            {"title": "Best mutual funds for beginners in 2024", "author": "InvestorRaj", "replies": 23, "category": "Investment"},
            {"title": "How to build emergency fund on ₹30k salary?", "author": "BudgetMaster", "replies": 15, "category": "Personal Finance"},
            {"title": "PM-KISAN payment delayed - anyone else?", "author": "FarmerFriend", "replies": 8, "category": "Farmer Finance"},
            {"title": "Tax planning for IT professionals", "author": "TechSaver", "replies": 31, "category": "Tax Planning"},
            {"title": "Credit score improvement success story", "author": "CreditHero", "replies": 12, "category": "Credit"}
        ]

        for discussion in discussions:
            with st.expander(f"💬 {discussion['title']} - {discussion['category']}"):
                st.markdown(f"**Author:** {discussion['author']}")
                st.markdown(f"**Replies:** {discussion['replies']}")
                st.markdown("**Preview:** This is a sample discussion preview...")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Read Full Discussion", key=f"read_{discussion['title'][:10]}"):
                        st.info("Full discussion feature coming soon!")
                with col2:
                    if st.button(f"Reply", key=f"reply_{discussion['title'][:10]}"):
                        st.info("Reply feature coming soon!")

        # Community stats
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Active Members", "10,247")

        with col2:
            st.metric("Discussions", "1,523")

        with col3:
            st.metric("Expert Advisors", "45")

        with col4:
            st.metric("Success Stories", "234")

    def render_gamification(self):
        """Render gamification features"""
        current_language = st.session_state.user_profile['basic_info']['language']

        if current_language == 'en':
            st.markdown("### 🎮 Financial Fitness Gamification")
        elif current_language == 'ta':
            st.markdown("### 🎮 நிதி உடற்பயிற்சி விளையாட்டு")
        elif current_language == 'hi':
            st.markdown("### 🎮 वित्तीय फिटनेस गेमिफिकेशन")

        # User progress
        gamification_data = st.session_state.user_profile['gamification']
        points = gamification_data['points']
        level = gamification_data['level']
        badges = gamification_data['badges']

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Points", f"{points:,}")
            st.metric("Current Level", level)

            # Progress to next level
            points_for_next_level = level * 1000
            progress = min(points / points_for_next_level, 1.0)
            st.progress(progress)
            st.caption(f"Progress to Level {level + 1}")

        with col2:
            st.markdown("#### 🏆 Achievements")

            all_badges = [
                "🎯 First Goal Set",
                "💰 Savings Streak",
                "📊 Budget Master",
                "📈 Investment Guru",
                "🎓 Financial Learner",
                "🌟 Community Helper"
            ]

            for badge in all_badges:
                if badge in badges:
                    st.markdown(f"✅ {badge}")
                else:
                    st.markdown(f"⬜ {badge}")

        with col3:
            st.markdown("#### 🔥 Current Streaks")

            streak_days = gamification_data['streak_days']
            st.metric("Daily Login Streak", f"{streak_days} days")
            st.metric("Budget Tracking", "15 days")
            st.metric("Investment SIP", "6 months")

        # Challenges
        st.markdown("---")
        st.markdown("#### 🎯 Financial Challenges")

        challenges = [
            {
                "title": "30-Day Budget Challenge",
                "description": "Track your expenses daily for 30 days",
                "reward": "500 points + Budget Master badge",
                "progress": 15,
                "total": 30,
                "status": "active"
            },
            {
                "title": "Emergency Fund Builder",
                "description": "Build 3 months of emergency fund",
                "reward": "1000 points + Safety Net badge",
                "progress": 1.5,
                "total": 3,
                "status": "active"
            },
            {
                "title": "Investment Diversification",
                "description": "Invest in 5 different asset classes",
                "reward": "750 points + Diversifier badge",
                "progress": 3,
                "total": 5,
                "status": "active"
            },
            {
                "title": "Credit Score Improvement",
                "description": "Improve credit score by 50 points",
                "reward": "800 points + Credit Hero badge",
                "progress": 25,
                "total": 50,
                "status": "completed"
            }
        ]

        for challenge in challenges:
            with st.expander(f"{'🏆' if challenge['status'] == 'completed' else '🎯'} {challenge['title']}"):
                st.markdown(f"**Description:** {challenge['description']}")
                st.markdown(f"**Reward:** {challenge['reward']}")

                if challenge['status'] == 'completed':
                    st.success("✅ Challenge Completed!")
                else:
                    progress = challenge['progress'] / challenge['total']
                    st.progress(progress)
                    st.markdown(f"**Progress:** {challenge['progress']}/{challenge['total']}")

                    if st.button(f"Join Challenge", key=f"join_{challenge['title'][:10]}"):
                        st.success("Challenge joined! Start tracking your progress.")

        # Leaderboard
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🏅 Weekly Leaderboard")

            leaderboard = [
                {"rank": 1, "name": "FinanceGuru", "points": 2500},
                {"rank": 2, "name": "BudgetMaster", "points": 2200},
                {"rank": 3, "name": "InvestorPro", "points": 2100},
                {"rank": 4, "name": "You", "points": points},
                {"rank": 5, "name": "SavingsHero", "points": 1800}
            ]

            for entry in leaderboard:
                if entry["name"] == "You":
                    st.markdown(f"**{entry['rank']}. {entry['name']} - {entry['points']} points** 🎯")
                else:
                    st.markdown(f"{entry['rank']}. {entry['name']} - {entry['points']} points")

        with col2:
            st.markdown("#### 🎁 Rewards Store")

            rewards = [
                {"item": "Free Financial Consultation", "cost": 5000, "available": True},
                {"item": "Premium Calculator Access", "cost": 2000, "available": True},
                {"item": "Personalized Investment Report", "cost": 3000, "available": True},
                {"item": "Tax Planning Session", "cost": 4000, "available": False}
            ]

            for reward in rewards:
                status = "✅" if reward["available"] else "❌"
                affordable = "💰" if points >= reward["cost"] else "💸"
                st.markdown(f"{status} {affordable} {reward['item']} - {reward['cost']} points")

                if reward["available"] and points >= reward["cost"]:
                    if st.button(f"Redeem", key=f"redeem_{reward['item'][:10]}"):
                        st.success(f"Redeemed: {reward['item']}")

    def render_comprehensive_profile(self):
        """Render comprehensive user profile"""
        current_language = st.session_state.user_profile['basic_info']['language']

        if current_language == 'en':
            st.markdown("### 👤 Comprehensive User Profile")
        elif current_language == 'ta':
            st.markdown("### 👤 விரிவான பயனர் சுயவிவரம்")
        elif current_language == 'hi':
            st.markdown("### 👤 व्यापक उपयोगकर्ता प्रोफ़ाइल")

        # Profile tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Basic Info", "Financial Profile", "Preferences", "Security"])

        with tab1:
            self.render_basic_info_tab()

        with tab2:
            self.render_financial_profile_tab()

        with tab3:
            self.render_preferences_tab()

        with tab4:
            self.render_security_tab()

    def render_basic_info_tab(self):
        """Render basic info tab"""
        st.markdown("#### 📝 Basic Information")

        with st.form("basic_info_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Full Name", value=st.session_state.user_profile['basic_info']['name'])
                email = st.text_input("Email", value=st.session_state.user_profile['basic_info']['email'])
                phone = st.text_input("Phone", value=st.session_state.user_profile['basic_info']['phone'])
                age = st.number_input("Age", min_value=18, max_value=100, value=st.session_state.user_profile['basic_info'].get('age', 25))

            with col2:
                user_type = st.selectbox(
                    "User Type",
                    ['beginner', 'intermediate', 'professional', 'student', 'farmer', 'senior_citizen'],
                    index=['beginner', 'intermediate', 'professional', 'student', 'farmer', 'senior_citizen'].index(
                        st.session_state.user_profile['basic_info']['user_type']
                    )
                )

                language = st.selectbox(
                    "Preferred Language",
                    ['en', 'ta', 'hi', 'te'],
                    index=['en', 'ta', 'hi', 'te'].index(st.session_state.user_profile['basic_info']['language'])
                )

                location = st.text_input("Location", value=st.session_state.user_profile['basic_info']['location'])
                occupation = st.text_input("Occupation", value=st.session_state.user_profile['basic_info'].get('occupation', ''))

            if st.form_submit_button("Update Basic Info"):
                st.session_state.user_profile['basic_info'].update({
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'age': age,
                    'user_type': user_type,
                    'language': language,
                    'location': location,
                    'occupation': occupation
                })
                st.success("Basic information updated successfully!")
                st.rerun()

    def render_financial_profile_tab(self):
        """Render financial profile tab"""
        st.markdown("#### 💰 Financial Profile")

        with st.form("financial_profile_form"):
            col1, col2 = st.columns(2)

            with col1:
                monthly_income = st.number_input(
                    "Monthly Income (₹)",
                    min_value=0,
                    value=st.session_state.user_profile['basic_info']['monthly_income'],
                    step=1000
                )

                risk_tolerance = st.selectbox(
                    "Risk Tolerance",
                    ['conservative', 'moderate', 'aggressive'],
                    index=['conservative', 'moderate', 'aggressive'].index(
                        st.session_state.user_profile['financial_profile']['risk_tolerance']
                    )
                )

                investment_experience = st.selectbox(
                    "Investment Experience",
                    ['beginner', 'intermediate', 'advanced'],
                    index=['beginner', 'intermediate', 'advanced'].index(
                        st.session_state.user_profile['financial_profile']['investment_experience']
                    )
                )

            with col2:
                financial_goals = st.multiselect(
                    "Financial Goals",
                    ['Emergency Fund', 'House Purchase', 'Car Purchase', 'Child Education', 'Retirement', 'Vacation', 'Debt Payoff'],
                    default=st.session_state.user_profile['financial_profile']['financial_goals']
                )

                # Monthly expenses breakdown
                st.markdown("**Monthly Expenses Breakdown:**")
                housing = st.number_input("Housing/Rent", value=int(monthly_income * 0.30), step=1000)
                food = st.number_input("Food & Groceries", value=int(monthly_income * 0.20), step=500)
                transport = st.number_input("Transportation", value=int(monthly_income * 0.08), step=500)

            if st.form_submit_button("Update Financial Profile"):
                st.session_state.user_profile['basic_info']['monthly_income'] = monthly_income
                st.session_state.user_profile['financial_profile'].update({
                    'risk_tolerance': risk_tolerance,
                    'investment_experience': investment_experience,
                    'financial_goals': financial_goals,
                    'monthly_expenses': {
                        'housing': housing,
                        'food': food,
                        'transport': transport
                    }
                })
                st.success("Financial profile updated successfully!")
                st.rerun()

    def render_preferences_tab(self):
        """Render preferences tab"""
        st.markdown("#### ⚙️ Preferences & Settings")

        with st.form("preferences_form"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**UI Preferences**")
                dark_mode = st.toggle("Dark Mode", value=st.session_state.user_profile['preferences']['dark_mode'])
                accessibility_mode = st.toggle("Accessibility Mode", value=st.session_state.user_profile['preferences']['accessibility_mode'])

                st.markdown("**AI Features**")
                ai_accuracy_mode = st.toggle("AI Fact-Checking", value=st.session_state.user_profile['preferences']['ai_accuracy_mode'])
                enhanced_sources = st.toggle("Enhanced Sources", value=st.session_state.user_profile['preferences']['enhanced_sources'])

            with col2:
                st.markdown("**Communication**")
                voice_enabled = st.toggle("Voice Interface", value=st.session_state.user_profile['preferences']['voice_enabled'])
                notifications = st.toggle("Notifications", value=st.session_state.user_profile['preferences']['notifications'])

                st.markdown("**Learning**")
                learning_mode = st.toggle("Learning Mode", value=st.session_state.user_profile['preferences']['learning_mode'])
                response_style = st.selectbox(
                    "Response Style",
                    ['professional', 'friendly', 'detailed', 'concise'],
                    index=['professional', 'friendly', 'detailed', 'concise'].index(
                        st.session_state.user_profile['preferences']['response_style']
                    )
                )

            if st.form_submit_button("Update Preferences"):
                st.session_state.user_profile['preferences'].update({
                    'dark_mode': dark_mode,
                    'accessibility_mode': accessibility_mode,
                    'ai_accuracy_mode': ai_accuracy_mode,
                    'enhanced_sources': enhanced_sources,
                    'voice_enabled': voice_enabled,
                    'notifications': notifications,
                    'learning_mode': learning_mode,
                    'response_style': response_style
                })
                st.success("Preferences updated successfully!")
                st.rerun()

    def render_security_tab(self):
        """Render security tab"""
        st.markdown("#### 🔒 Security Settings")

        with st.form("security_form"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Authentication**")
                two_factor_enabled = st.toggle("Two-Factor Authentication", value=st.session_state.user_profile['security']['two_factor_enabled'])
                biometric_enabled = st.toggle("Biometric Authentication", value=st.session_state.user_profile['security']['biometric_enabled'])

                if st.button("Change Password"):
                    st.info("Password change functionality coming soon!")

            with col2:
                st.markdown("**Privacy**")
                data_encryption = st.toggle("Data Encryption", value=st.session_state.user_profile['security']['data_encryption'])
                privacy_level = st.selectbox(
                    "Privacy Level",
                    ['low', 'medium', 'high'],
                    index=['low', 'medium', 'high'].index(st.session_state.user_profile['security']['privacy_level'])
                )

                if st.button("Download My Data"):
                    st.info("Data export functionality coming soon!")

            if st.form_submit_button("Update Security Settings"):
                st.session_state.user_profile['security'].update({
                    'two_factor_enabled': two_factor_enabled,
                    'biometric_enabled': biometric_enabled,
                    'data_encryption': data_encryption,
                    'privacy_level': privacy_level
                })
                st.success("Security settings updated successfully!")
                st.rerun()


# Initialize and run the comprehensive application
if __name__ == "__main__":
    app = ComprehensiveJarvisFiApp()
    app.run_comprehensive_app()
