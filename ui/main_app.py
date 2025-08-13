"""
JarvisFi - Main Streamlit Application
Your AI-Powered Financial Genius - Comprehensive Frontend
"""

import streamlit as st
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import json
import time

# Page configuration
st.set_page_config(
    page_title="JarvisFi - Your AI-Powered Financial Genius",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://jarvisfi.com/help',
        'Report a bug': 'https://jarvisfi.com/bug-report',
        'About': "JarvisFi - Your AI-Powered Financial Genius"
    }
)

# Import components
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface
from components.dashboard import render_dashboard
from components.calculators import render_calculators
from components.voice_interface import render_voice_interface
from components.accessibility import apply_accessibility_settings
from utils.api_client import APIClient
from utils.session_manager import SessionManager
from utils.language_manager import LanguageManager

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize utilities
api_client = APIClient()
session_manager = SessionManager()
language_manager = LanguageManager()


class JarvisFiApp:
    """Main JarvisFi Application Class"""
    
    def __init__(self):
        self.initialize_session_state()
        self.apply_custom_css()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        
        # User profile
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
                    'location': 'India'
                },
                'preferences': {
                    'dark_mode': False,
                    'voice_enabled': True,
                    'notifications': True,
                    'accessibility_mode': False
                },
                'financial_profile': {
                    'risk_tolerance': 'moderate',
                    'investment_experience': 'beginner',
                    'financial_goals': []
                }
            }
        
        # Chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Current page
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        
        # Voice interface
        if 'voice_listening' not in st.session_state:
            st.session_state.voice_listening = False
        
        if 'voice_speaking' not in st.session_state:
            st.session_state.voice_speaking = False
        
        # Authentication
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        
        if 'auth_token' not in st.session_state:
            st.session_state.auth_token = None
        
        # UI state
        if 'sidebar_expanded' not in st.session_state:
            st.session_state.sidebar_expanded = True
        
        # Performance tracking
        if 'page_load_time' not in st.session_state:
            st.session_state.page_load_time = time.time()
    
    def apply_custom_css(self):
        """Apply custom CSS styling"""
        
        # Get current theme
        dark_mode = st.session_state.user_profile['preferences']['dark_mode']
        accessibility_mode = st.session_state.user_profile['preferences']['accessibility_mode']
        
        # Base CSS
        css = """
        <style>
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Root variables */
        :root {
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --accent-color: #f093fb;
            --success-color: #4ade80;
            --warning-color: #fbbf24;
            --error-color: #f87171;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --bg-primary: #ffffff;
            --bg-secondary: #f9fafb;
            --border-color: #e5e7eb;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Dark mode variables */
        [data-theme="dark"] {
            --text-primary: #f9fafb;
            --text-secondary: #d1d5db;
            --bg-primary: #111827;
            --bg-secondary: #1f2937;
            --border-color: #374151;
        }
        
        /* Main app styling */
        .main {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
        }
        
        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: var(--shadow);
        }
        
        .main-header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .main-header p {
            font-size: 1.2rem;
            opacity: 0.9;
            font-style: italic;
        }
        
        /* Card styling */
        .metric-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1);
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        /* Chat interface styling */
        .chat-message {
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            box-shadow: var(--shadow);
        }
        
        .chat-message.user {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            margin-left: 2rem;
        }
        
        .chat-message.assistant {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            margin-right: 2rem;
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        /* Voice interface styling */
        .voice-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .voice-indicator.listening {
            background: var(--error-color);
            animation: pulse 1s infinite;
        }
        
        .voice-indicator.speaking {
            background: var(--success-color);
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        /* Accessibility enhancements */
        .accessibility-mode {
            font-size: 1.2em !important;
            line-height: 1.6 !important;
        }
        
        .accessibility-mode button {
            min-height: 44px !important;
            min-width: 44px !important;
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2rem;
            }
            
            .chat-message.user {
                margin-left: 0.5rem;
            }
            
            .chat-message.assistant {
                margin-right: 0.5rem;
            }
        }
        
        /* Loading animations */
        .loading-spinner {
            border: 4px solid var(--border-color);
            border-top: 4px solid var(--primary-color);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Success/Error messages */
        .success-message {
            background: var(--success-color);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .error-message {
            background: var(--error-color);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
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
            </style>
            """
        
        # Apply accessibility mode
        if accessibility_mode:
            css += """
            <style>
            .stApp {
                font-size: 1.2em !important;
                line-height: 1.6 !important;
            }
            
            button {
                min-height: 44px !important;
                min-width: 44px !important;
                font-size: 1.1em !important;
            }
            
            .stSelectbox > div > div {
                min-height: 44px !important;
            }
            
            .stTextInput > div > div > input {
                min-height: 44px !important;
                font-size: 1.1em !important;
            }
            </style>
            """
        
        st.markdown(css, unsafe_allow_html=True)
    
    def render_header(self):
        """Render main application header"""
        current_language = st.session_state.user_profile['basic_info']['language']
        user_name = st.session_state.user_profile['basic_info']['name']
        
        if current_language == 'en':
            title = "JarvisFi"
            slogan = "Your AI-Powered Financial Genius"
            welcome = f"Welcome back, {user_name}!" if user_name else "Welcome to JarvisFi!"
        elif current_language == 'ta':
            title = "JarvisFi"
            slogan = "உங்கள் AI-இயங்கும் நிதி மேதை"
            welcome = f"மீண்டும் வரவேற்கிறோம், {user_name}!" if user_name else "JarvisFi-க்கு வரவேற்கிறோம்!"
        elif current_language == 'hi':
            title = "JarvisFi"
            slogan = "आपका AI-संचालित वित्तीय प्रतिभा"
            welcome = f"वापस स्वागत है, {user_name}!" if user_name else "JarvisFi में आपका स्वागत है!"
        else:
            title = "JarvisFi"
            slogan = "Your AI-Powered Financial Genius"
            welcome = f"Welcome back, {user_name}!" if user_name else "Welcome to JarvisFi!"
        
        st.markdown(f"""
        <div class="main-header">
            <h1>🤖 {title}</h1>
            <p>{slogan}</p>
            <small style="opacity: 0.8; font-size: 0.9rem;">{welcome}</small>
        </div>
        """, unsafe_allow_html=True)
    
    def render_navigation(self):
        """Render main navigation"""
        current_language = st.session_state.user_profile['basic_info']['language']
        
        # Navigation tabs
        if current_language == 'en':
            tab_labels = [
                "🏠 Home", "💬 Chat", "📊 Dashboard", 
                "🧮 Calculators", "🎤 Voice", "👨‍🌾 Farmer Tools",
                "👥 Community", "👤 Profile"
            ]
        elif current_language == 'ta':
            tab_labels = [
                "🏠 முகப்பு", "💬 அரட்டை", "📊 டாஷ்போர்டு",
                "🧮 கணக்கீட்டாளர்கள்", "🎤 குரல்", "👨‍🌾 விவசாயி கருவிகள்",
                "👥 சமூகம்", "👤 சுயவிவரம்"
            ]
        elif current_language == 'hi':
            tab_labels = [
                "🏠 होम", "💬 चैट", "📊 डैशबोर्ड",
                "🧮 कैलकुलेटर", "🎤 आवाज़", "👨‍🌾 किसान उपकरण",
                "👥 समुदाय", "👤 प्रोफ़ाइल"
            ]
        else:
            tab_labels = [
                "🏠 Home", "💬 Chat", "📊 Dashboard", 
                "🧮 Calculators", "🎤 Voice", "👨‍🌾 Farmer Tools",
                "👥 Community", "👤 Profile"
            ]
        
        tabs = st.tabs(tab_labels)
        
        return tabs
    
    def run(self):
        """Main application runner"""
        try:
            # Apply accessibility settings
            apply_accessibility_settings()
            
            # Render sidebar
            render_sidebar()
            
            # Render header
            self.render_header()
            
            # Render navigation and content
            tabs = self.render_navigation()
            
            # Home tab
            with tabs[0]:
                self.render_home_page()
            
            # Chat tab
            with tabs[1]:
                render_chat_interface()
            
            # Dashboard tab
            with tabs[2]:
                render_dashboard()
            
            # Calculators tab
            with tabs[3]:
                render_calculators()
            
            # Voice tab
            with tabs[4]:
                render_voice_interface()
            
            # Farmer tools tab
            with tabs[5]:
                self.render_farmer_tools()
            
            # Community tab
            with tabs[6]:
                self.render_community()
            
            # Profile tab
            with tabs[7]:
                self.render_profile()
            
            # Performance monitoring
            self.monitor_performance()
            
        except Exception as e:
            logger.error(f"Application error: {e}")
            st.error("An error occurred. Please refresh the page.")
    
    def render_home_page(self):
        """Render home page"""
        current_language = st.session_state.user_profile['basic_info']['language']
        
        if current_language == 'en':
            st.markdown("### 🏠 Welcome to JarvisFi")
            st.markdown("Your comprehensive AI-powered financial assistant")
        elif current_language == 'ta':
            st.markdown("### 🏠 JarvisFi-க்கு வரவேற்கிறோம்")
            st.markdown("உங்கள் விரிவான AI-இயங்கும் நிதி உதவியாளர்")
        elif current_language == 'hi':
            st.markdown("### 🏠 JarvisFi में आपका स्वागत है")
            st.markdown("आपका व्यापक AI-संचालित वित्तीय सहायक")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Users", "10,000+", "↗️ 15%")
        
        with col2:
            st.metric("Languages", "4", "🌐")
        
        with col3:
            st.metric("Financial Tools", "25+", "🧮")
        
        with col4:
            st.metric("Success Rate", "95%", "✅")
        
        # Quick actions
        st.markdown("---")
        if current_language == 'en':
            st.markdown("### 🚀 Quick Actions")
        elif current_language == 'ta':
            st.markdown("### 🚀 விரைவு செயல்கள்")
        elif current_language == 'hi':
            st.markdown("### 🚀 त्वरित कार्य")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💬 Start Chat" if current_language == 'en' else "💬 அரட்டை தொடங்கு" if current_language == 'ta' else "💬 चैट शुरू करें"):
                st.session_state.current_page = 'chat'
                st.rerun()
        
        with col2:
            if st.button("📊 View Dashboard" if current_language == 'en' else "📊 டாஷ்போர்டு பார்க்க" if current_language == 'ta' else "📊 डैशबोर्ड देखें"):
                st.session_state.current_page = 'dashboard'
                st.rerun()
        
        with col3:
            if st.button("🧮 Use Calculators" if current_language == 'en' else "🧮 கணக்கீட்டாளர்களைப் பயன்படுத்து" if current_language == 'ta' else "🧮 कैलकुलेटर का उपयोग करें"):
                st.session_state.current_page = 'calculators'
                st.rerun()
    
    def render_farmer_tools(self):
        """Render farmer-specific tools"""
        st.markdown("### 👨‍🌾 Farmer Tools - Coming Soon!")
        st.info("Specialized tools for farmers including crop loan calculators, MSP alerts, and subsidy checks will be available soon.")
    
    def render_community(self):
        """Render community forum"""
        st.markdown("### 👥 Community Forum - Coming Soon!")
        st.info("Connect with other users, share experiences, and get peer-to-peer financial advice.")
    
    def render_profile(self):
        """Render user profile"""
        st.markdown("### 👤 User Profile")
        
        # Profile editing form
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Name", value=st.session_state.user_profile['basic_info']['name'])
                email = st.text_input("Email", value=st.session_state.user_profile['basic_info']['email'])
                phone = st.text_input("Phone", value=st.session_state.user_profile['basic_info']['phone'])
            
            with col2:
                user_type = st.selectbox("User Type", 
                    ['beginner', 'intermediate', 'professional', 'student', 'farmer', 'senior_citizen'],
                    index=['beginner', 'intermediate', 'professional', 'student', 'farmer', 'senior_citizen'].index(
                        st.session_state.user_profile['basic_info']['user_type']
                    )
                )
                
                language = st.selectbox("Language", 
                    ['en', 'ta', 'hi', 'te'],
                    index=['en', 'ta', 'hi', 'te'].index(
                        st.session_state.user_profile['basic_info']['language']
                    )
                )
                
                currency = st.selectbox("Currency", 
                    ['INR', 'USD', 'EUR', 'GBP'],
                    index=['INR', 'USD', 'EUR', 'GBP'].index(
                        st.session_state.user_profile['basic_info']['currency']
                    )
                )
            
            monthly_income = st.number_input("Monthly Income", 
                value=st.session_state.user_profile['basic_info']['monthly_income'],
                min_value=0, step=1000
            )
            
            if st.form_submit_button("Update Profile"):
                # Update session state
                st.session_state.user_profile['basic_info'].update({
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'user_type': user_type,
                    'language': language,
                    'currency': currency,
                    'monthly_income': monthly_income
                })
                
                st.success("Profile updated successfully!")
                st.rerun()
    
    def monitor_performance(self):
        """Monitor application performance"""
        current_time = time.time()
        load_time = current_time - st.session_state.page_load_time
        
        # Log performance if slow
        if load_time > 2.0:
            logger.warning(f"Slow page load: {load_time:.2f}s")
        
        # Update load time for next measurement
        st.session_state.page_load_time = current_time


# Run the application
if __name__ == "__main__":
    app = JarvisFiApp()
    app.run()
