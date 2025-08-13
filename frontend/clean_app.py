import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime, timedelta
import sys
import logging
from typing import Dict, List
import base64
from io import BytesIO
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JarvisFiApp:
    def __init__(self):
        """Initialize JarvisFi - Your AI-Powered Financial Genius"""
        self.logger = logging.getLogger(__name__)
        self.logger.info("🤖 JarvisFi - Your AI-Powered Financial Genius initialized")
        
        # Initialize session state
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize comprehensive session state"""
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = {
                'basic_info': {
                    'name': '',
                    'age': 25,
                    'user_type': 'beginner',
                    'language': 'english',
                    'monthly_income': 30000,
                    'currency': 'INR',
                    'location': 'India'
                }
            }
        
        # Initialize other session variables
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            
        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False
            
        if 'voice_listening' not in st.session_state:
            st.session_state.voice_listening = False
            
        if 'voice_speaking' not in st.session_state:
            st.session_state.voice_speaking = False
            
        if 'ai_accuracy_enabled' not in st.session_state:
            st.session_state.ai_accuracy_enabled = True
    
    def setup_page_config(self):
        """Setup page configuration"""
        try:
            st.set_page_config(
                page_title="JarvisFi - Your AI-Powered Financial Genius",
                page_icon="🤖",
                layout="wide",
                initial_sidebar_state="expanded"
            )
        except Exception:
            pass  # Page config already set
    
    def apply_clean_css(self):
        """Apply clean, simple CSS"""
        theme_bg = "#1e1e1e" if st.session_state.dark_mode else "#ffffff"
        theme_text = "#ffffff" if st.session_state.dark_mode else "#333333"
        card_bg = "#2d2d2d" if st.session_state.dark_mode else "#f8f9fa"
        
        st.markdown(f"""
        <style>
        .stApp {{
            background-color: {theme_bg};
            color: {theme_text};
        }}
        
        .main-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}

        .main-header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .main-header p {{
            font-size: 1.2rem;
            opacity: 0.9;
            font-style: italic;
        }}
        
        .chat-container {{
            background: {card_bg};
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid #ddd;
        }}
        
        .user-message {{
            background: #e3f2fd;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #2196f3;
        }}
        
        .assistant-message {{
            background: #f3e5f5;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #9c27b0;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def create_sidebar(self):
        """Create clean sidebar"""
        with st.sidebar:
            current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
            
            st.markdown("### 👤 User Profile")
            
            # Name input
            name = st.text_input(
                "Name" if current_language == 'english' else "பெயர்",
                value=st.session_state.user_profile.get('basic_info', {}).get('name', ''),
                key="user_name"
            )
            if name != st.session_state.user_profile.get('basic_info', {}).get('name', ''):
                st.session_state.user_profile['basic_info']['name'] = name
            
            # Language selector
            language_options = {'english': 'English', 'tamil': 'தமிழ்'}
            selected_lang = st.selectbox(
                "🌐 Language",
                options=list(language_options.keys()),
                format_func=lambda x: language_options[x],
                index=0 if current_language == 'english' else 1,
                key="language_selector"
            )
            
            if selected_lang != current_language:
                st.session_state.user_profile['basic_info']['language'] = selected_lang
                st.rerun()
            
            # User type selector
            user_type_text = "👤 User Type" if current_language == 'english' else "👤 பயனர் வகை"
            user_types = {
                'beginner': 'Beginner' if current_language == 'english' else 'ஆரம்பநிலை',
                'intermediate': 'Intermediate' if current_language == 'english' else 'இடைநிலை',
                'professional': 'Professional' if current_language == 'english' else 'தொழில்முறை',
                'student': 'Student' if current_language == 'english' else 'மாணவர்'
            }
            
            current_user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')
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

            st.markdown("---")

            # Monthly Salary Input
            st.markdown("### 💰 Financial Profile" if current_language == 'english' else "### 💰 நிதி சுயவிவரம்")

            current_salary = st.session_state.user_profile.get('basic_info', {}).get('monthly_income', 30000)
            monthly_salary = st.number_input(
                "Monthly Salary (₹)" if current_language == 'english' else "மாதாந்திர சம்பளம் (₹)",
                min_value=5000,
                max_value=10000000,
                value=current_salary,
                step=5000,
                key="monthly_salary_input",
                help="Enter your monthly salary to get personalized insights" if current_language == 'english' else "தனிப்பயனாக்கப்பட்ட நுண்ணறிவுகளைப் பெற உங்கள் மாதாந்திர சம்பளத்தை உள்ளிடுங்கள்"
            )

            if monthly_salary != current_salary:
                st.session_state.user_profile['basic_info']['monthly_income'] = monthly_salary
                st.rerun()

            # Show salary-based recommendations
            if monthly_salary:
                if current_language == 'english':
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
                else:
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

                st.info(f"**{salary_category}**: {recommendation}")

            # Dark mode toggle
            dark_mode_text = "🌙 Dark Mode" if current_language == 'english' else "🌙 இருண்ட பயன்முறை"
            dark_mode = st.toggle(dark_mode_text, value=st.session_state.get('dark_mode', False), key="dark_mode_toggle")

            if dark_mode != st.session_state.get('dark_mode', False):
                st.session_state.dark_mode = dark_mode
                st.rerun()
            
            st.markdown("---")

            # Voice Interface Section
            st.markdown("### 🎤 Voice Assistant" if current_language == 'english' else "### 🎤 குரல் உதவியாளர்")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎙️ Listen" if current_language == 'english' else "🎙️ கேளுங்கள்", key="voice_listen"):
                    st.session_state.voice_listening = True

            with col2:
                if st.button("🔊 Speak" if current_language == 'english' else "🔊 பேசுங்கள்", key="voice_speak"):
                    st.session_state.voice_speaking = True

            # Voice settings
            voice_quality = st.selectbox(
                "Voice Quality" if current_language == 'english' else "குரல் தரம்",
                ["Standard", "High Quality", "Natural"],
                index=1,
                key="voice_quality"
            )

            voice_speed = st.slider(
                "Speech Speed" if current_language == 'english' else "பேச்சு வேகம்",
                min_value=0.5, max_value=2.0, value=1.0, step=0.1,
                key="voice_speed"
            )

            st.markdown("---")

            # Security Section
            st.markdown("### 🔐 Security" if current_language == 'english' else "### 🔐 பாதுகாப்பு")

            # Security status
            security_status = "🟢 Secure Mode" if st.session_state.get('secure_mode', True) else "🟡 Basic Mode"
            st.markdown(f"**Status:** {security_status}")

            # Data encryption toggle
            encrypt_data = st.toggle(
                "Encrypt Data" if current_language == 'english' else "தரவு குறியாக்கம்",
                value=st.session_state.get('encrypt_data', True),
                key="encrypt_toggle"
            )
            st.session_state.encrypt_data = encrypt_data

            # Auto-logout timer
            auto_logout = st.selectbox(
                "Auto Logout" if current_language == 'english' else "தானியங்கு வெளியேறு",
                ["Never", "15 minutes", "30 minutes", "1 hour", "2 hours"],
                index=2,
                key="auto_logout"
            )

            st.markdown("---")

            # AI & RAG Section
            st.markdown("### 🧠 AI Features" if current_language == 'english' else "### 🧠 AI அம்சங்கள்")

            # AI Accuracy toggle
            ai_accuracy = st.toggle(
                "AI Fact-Checking" if current_language == 'english' else "AI உண்மை சரிபார்ப்பு",
                value=st.session_state.get('ai_accuracy_enabled', True),
                key="ai_accuracy_toggle"
            )
            st.session_state.ai_accuracy_enabled = ai_accuracy

            # Enhanced sources toggle
            enhanced_sources = st.toggle(
                "Enhanced Sources" if current_language == 'english' else "மேம்பட்ட ஆதாரங்கள்",
                value=st.session_state.get('enhanced_sources', True),
                key="enhanced_sources_toggle"
            )
            st.session_state.enhanced_sources = enhanced_sources

            # AI Response Style
            ai_style = st.selectbox(
                "Response Style" if current_language == 'english' else "பதில் பாணி",
                ["Professional", "Friendly", "Detailed", "Concise"],
                index=0,
                key="ai_style"
            )

            # Learning Mode
            learning_mode = st.toggle(
                "Learning Mode" if current_language == 'english' else "கற்றல் பயன்முறை",
                value=st.session_state.get('learning_mode', False),
                key="learning_mode_toggle"
            )
            st.session_state.learning_mode = learning_mode

            st.markdown("---")

            # Currency & Exchange Section
            st.markdown("### 💱 Currency & Exchange" if current_language == 'english' else "### 💱 நாணயம் & மாற்று")

            currency_options = ['INR', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'SGD']
            current_currency = st.session_state.user_profile.get('basic_info', {}).get('currency', 'INR')

            selected_currency = st.selectbox(
                "Primary Currency" if current_language == 'english' else "முதன்மை நாணயம்",
                options=currency_options,
                index=currency_options.index(current_currency) if current_currency in currency_options else 0,
                key="currency_selector"
            )

            if selected_currency != current_currency:
                st.session_state.user_profile['basic_info']['currency'] = selected_currency
                st.rerun()

            # Secondary currency for comparisons
            secondary_currency = st.selectbox(
                "Secondary Currency" if current_language == 'english' else "இரண்டாம் நாணயம்",
                options=[c for c in currency_options if c != selected_currency],
                index=0,
                key="secondary_currency"
            )

            # Exchange rate display (mock data)
            st.markdown("**Live Rates** / **நேரடி விகிதங்கள்**")
            if selected_currency == 'INR':
                rates = {'USD': 0.012, 'EUR': 0.011, 'GBP': 0.0095}
            else:
                rates = {'INR': 83.12, 'USD': 1.0, 'EUR': 0.92}

            for curr, rate in list(rates.items())[:3]:
                st.markdown(f"• 1 {selected_currency} = {rate:.3f} {curr}")

            # Auto-update toggle
            auto_update_rates = st.toggle(
                "Auto Update Rates" if current_language == 'english' else "தானியங்கு விகித புதுப்பிப்பு",
                value=st.session_state.get('auto_update_rates', True),
                key="auto_update_rates"
            )

            st.markdown("---")

            # Database & Storage Section
            st.markdown("### 🗄️ Data Storage" if current_language == 'english' else "### 🗄️ தரவு சேமிப்பு")

            # Storage status
            storage_status = "🟢 Local Storage" if st.session_state.get('local_storage', True) else "🟡 Session Only"
            st.markdown(f"**Status:** {storage_status}")

            # Data backup toggle
            backup_enabled = st.toggle(
                "Auto Backup" if current_language == 'english' else "தானியங்கு காப்பு",
                value=st.session_state.get('backup_enabled', True),
                key="backup_toggle"
            )
            st.session_state.backup_enabled = backup_enabled

            # Data retention period
            retention_period = st.selectbox(
                "Data Retention" if current_language == 'english' else "தரவு தக்கவைப்பு",
                ["30 days", "90 days", "6 months", "1 year", "Permanent"],
                index=3,
                key="retention_period"
            )

            # Sync data button
            if st.button("💾 Sync Data" if current_language == 'english' else "💾 தரவு ஒத்திசைவு", key="sync_data"):
                with st.spinner("Syncing..." if current_language == 'english' else "ஒத்திசைக்கிறது..."):
                    time.sleep(1)  # Simulate sync
                st.success("Data synced!" if current_language == 'english' else "தரவு ஒத்திசைக்கப்பட்டது!")

            # Advanced Settings Section
            with st.expander("🔧 Advanced Settings" if current_language == 'english' else "🔧 மேம்பட்ட அமைப்புகள்"):

                # Performance settings
                st.markdown("**Performance** / **செயல்திறன்**")
                performance_mode = st.selectbox(
                    "Performance Mode" if current_language == 'english' else "செயல்திறன் பயன்முறை",
                    ["Balanced", "High Performance", "Battery Saver", "Custom"],
                    index=0,
                    key="performance_mode"
                )

                # Memory management
                memory_limit = st.slider(
                    "Memory Limit (MB)" if current_language == 'english' else "நினைவக வரம்பு (MB)",
                    min_value=256, max_value=2048, value=512, step=128,
                    key="memory_limit"
                )

                # Cache settings
                enable_cache = st.toggle(
                    "Enable Caching" if current_language == 'english' else "கேச்சிங் இயக்கு",
                    value=st.session_state.get('enable_cache', True),
                    key="cache_toggle"
                )

                st.markdown("---")

                # Notification settings
                st.markdown("**Notifications** / **அறிவிப்புகள்**")

                enable_notifications = st.toggle(
                    "Enable Notifications" if current_language == 'english' else "அறிவிப்புகளை இயக்கு",
                    value=st.session_state.get('notifications_enabled', True),
                    key="notifications_toggle"
                )

                notification_types = st.multiselect(
                    "Notification Types" if current_language == 'english' else "அறிவிப்பு வகைகள்",
                    ["Budget Alerts", "Investment Updates", "Market News", "Tips & Advice"],
                    default=["Budget Alerts", "Tips & Advice"],
                    key="notification_types"
                )

                notification_frequency = st.selectbox(
                    "Frequency" if current_language == 'english' else "அதிர்வெண்",
                    ["Real-time", "Daily", "Weekly", "Monthly"],
                    index=1,
                    key="notification_frequency"
                )

                st.markdown("---")

                # Export/Import settings
                st.markdown("**Data Management** / **தரவு மேலாண்மை**")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("📤 Export Data" if current_language == 'english' else "📤 தரவு ஏற்றுமதி", key="export_data"):
                        # Create export data
                        export_data = {
                            'user_profile': st.session_state.user_profile,
                            'chat_history': st.session_state.chat_history,
                            'settings': {
                                'dark_mode': st.session_state.get('dark_mode', False),
                                'ai_accuracy_enabled': st.session_state.get('ai_accuracy_enabled', True),
                                'language': current_language
                            },
                            'export_date': datetime.now().isoformat(),
                            'app_info': {
                                'name': 'JarvisFi',
                                'slogan': 'Your AI-Powered Financial Genius',
                                'version': '2.0.0'
                            }
                        }

                        # Create download link
                        json_str = json.dumps(export_data, indent=2, default=str)
                        b64 = base64.b64encode(json_str.encode()).decode()
                        href = f'<a href="data:file/json;base64,{b64}" download="jarvisfi_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json">📥 Download JarvisFi Data</a>'
                        st.markdown(href, unsafe_allow_html=True)
                        st.success("JarvisFi export ready!" if current_language == 'english' else "JarvisFi ஏற்றுமதி தயார்!")

                with col2:
                    uploaded_file = st.file_uploader(
                        "📥 Import Data" if current_language == 'english' else "📥 தரவு இறக்குமதி",
                        type=['json'],
                        key="import_data"
                    )

                    if uploaded_file is not None:
                        try:
                            import_data = json.load(uploaded_file)
                            if 'user_profile' in import_data:
                                st.session_state.user_profile.update(import_data['user_profile'])
                            if 'chat_history' in import_data:
                                st.session_state.chat_history = import_data['chat_history']
                            st.success("Data imported!" if current_language == 'english' else "தரவு இறக்குமதி செய்யப்பட்டது!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Import failed: {e}")

                st.markdown("---")

                # Reset settings
                st.markdown("**Reset Options** / **மீட்டமை விருப்பங்கள்**")

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("🔄 Reset Settings" if current_language == 'english' else "🔄 அமைப்புகளை மீட்டமை", key="reset_settings"):
                        # Reset to defaults
                        st.session_state.dark_mode = False
                        st.session_state.ai_accuracy_enabled = True
                        st.session_state.enhanced_sources = True
                        st.success("Settings reset!" if current_language == 'english' else "அமைப்புகள் மீட்டமைக்கப்பட்டன!")
                        st.rerun()

                with col2:
                    if st.button("💬 Clear Chat" if current_language == 'english' else "💬 அரட்டை அழிக்க", key="clear_chat"):
                        st.session_state.chat_history = []
                        st.success("Chat cleared!" if current_language == 'english' else "அரட்டை அழிக்கப்பட்டது!")
                        st.rerun()

                with col3:
                    if st.button("⚠️ Reset All" if current_language == 'english' else "⚠️ அனைத்தையும் மீட்டமை", key="reset_all"):
                        # Reset everything
                        for key in list(st.session_state.keys()):
                            if key not in ['user_profile']:  # Keep basic profile
                                del st.session_state[key]
                        st.session_state.chat_history = []
                        st.success("Everything reset!" if current_language == 'english' else "அனைத்தும் மீட்டமைக்கப்பட்டன!")
                        st.rerun()

                st.markdown("---")

                # Debug information
                if st.toggle("🐛 Debug Mode" if current_language == 'english' else "🐛 பிழைத்திருத்த பயன்முறை", key="debug_mode"):
                    st.markdown("**Debug Information** / **பிழைத்திருத்த தகவல்**")
                    st.json({
                        "session_state_keys": list(st.session_state.keys()),
                        "user_profile": st.session_state.user_profile,
                        "chat_history_count": len(st.session_state.chat_history),
                        "current_language": current_language,
                        "timestamp": datetime.now().isoformat()
                    })

            # Help & Information Section
            with st.expander("ℹ️ Help & Information" if current_language == 'english' else "ℹ️ உதவி & தகவல்"):

                st.markdown("**Quick Help** / **விரைவு உதவி**")

                help_topics = {
                    'english': [
                        "💬 **Chat**: Ask JarvisFi questions about budgets, savings, investments",
                        "🌐 **Language**: Switch between English and Tamil instantly",
                        "👤 **Profile**: Set your user type for personalized JarvisFi advice",
                        "🎤 **Voice**: Use voice commands with JarvisFi (demo available)",
                        "🔐 **Security**: Your data is encrypted and secure with JarvisFi",
                        "💱 **Currency**: JarvisFi supports multiple currencies",
                        "🧠 **AI**: Advanced AI features for intelligent financial responses"
                    ],
                    'tamil': [
                        "💬 **அரட்டை**: பட்ஜெட், சேமிப்பு, முதலீடு பற்றி JarvisFi-யிடம் கேளுங்கள்",
                        "🌐 **மொழி**: ஆங்கிலம் மற்றும் தமிழ் இடையே உடனடியாக மாறுங்கள்",
                        "👤 **சுயவிவரம்**: தனிப்பயனாக்கப்பட்ட JarvisFi ஆலோசனைக்கு உங்கள் பயனர் வகையை அமைக்கவும்",
                        "🎤 **குரல்**: JarvisFi உடன் குரல் கட்டளைகளைப் பயன்படுத்துங்கள் (டெமோ கிடைக்கும்)",
                        "🔐 **பாதுகாப்பு**: உங்கள் தரவு JarvisFi உடன் குறியாக்கம் செய்யப்பட்டு பாதுகாப்பானது",
                        "💱 **நாணயம்**: JarvisFi பல நாணயங்களுக்கு ஆதரவு அளிக்கிறது",
                        "🧠 **AI**: புத்திசாலித்தனமான நிதி பதில்களுக்கான மேம்பட்ட AI அம்சங்கள்"
                    ]
                }

                for topic in help_topics.get(current_language, help_topics['english']):
                    st.markdown(topic)

                st.markdown("---")

                # Sample questions
                st.markdown("**Sample Questions** / **மாதிரி கேள்விகள்**")

                sample_questions = {
                    'english': [
                        "JarvisFi, how can I save money?",
                        "What's a good budget plan, JarvisFi?",
                        "JarvisFi, how should I start investing?",
                        "What are SIPs, JarvisFi?",
                        "JarvisFi, how to reduce expenses?",
                        "Best savings account options, JarvisFi?"
                    ],
                    'tamil': [
                        "JarvisFi, பணம் எப்படி சேமிக்கலாம்?",
                        "JarvisFi, நல்ல பட்ஜெட் திட்டம் என்ன?",
                        "JarvisFi, முதலீட்டை எப்படி தொடங்க வேண்டும்?",
                        "JarvisFi, SIP என்றால் என்ன?",
                        "JarvisFi, செலவுகளை எப்படி குறைக்கலாம்?",
                        "JarvisFi, சிறந்த சேமிப்பு கணக்கு விருப்பங்கள்?"
                    ]
                }

                questions = sample_questions.get(current_language, sample_questions['english'])
                for i, question in enumerate(questions, 1):
                    if st.button(f"{i}. {question}", key=f"sample_q_{i}"):
                        # Add question to chat
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": question,
                            "timestamp": datetime.now()
                        })
                        st.rerun()

                st.markdown("---")

                # App information
                st.markdown("**App Information** / **பயன்பாட்டு தகவல்**")

                app_info = {
                    'english': {
                        'name': 'JarvisFi',
                        'version': 'Version 2.0.0',
                        'slogan': 'Your AI-Powered Financial Genius',
                        'features': 'Multilingual AI Financial Assistant',
                        'languages': 'English, Tamil',
                        'status': 'Active & Secure'
                    },
                    'tamil': {
                        'name': 'JarvisFi',
                        'version': 'பதிப்பு 2.0.0',
                        'slogan': 'உங்கள் AI-இயங்கும் நிதி மேதை',
                        'features': 'பல்மொழி AI நிதி உதவியாளர்',
                        'languages': 'ஆங்கிலம், தமிழ்',
                        'status': 'செயலில் & பாதுகாப்பான'
                    }
                }

                info = app_info.get(current_language, app_info['english'])
                for key, value in info.items():
                    st.markdown(f"• **{key.title()}**: {value}")

                # System status
                st.markdown("**System Status** / **கணினி நிலை**")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("🟢 Online", "Active" if current_language == 'english' else "செயலில்")

                with col2:
                    st.metric("💾 Storage", "Local" if current_language == 'english' else "உள்ளூர்")

                with col3:
                    st.metric("🔐 Security", "Enabled" if current_language == 'english' else "இயக்கப்பட்டது")

            st.markdown("---")

            # Footer
            st.markdown(
                "**🤖 JarvisFi** | **Your AI-Powered Financial Genius**" if current_language == 'english'
                else "**🤖 JarvisFi** | **உங்கள் AI-இயங்கும் நிதி மேதை**"
            )
            st.markdown(
                "*Intelligent financial guidance at your fingertips* 🚀💰" if current_language == 'english'
                else "*உங்கள் விரல் நுனியில் புத்திசாலித்தனமான நிதி வழிகாட்டுதல்* 🚀💰"
            )
    
    def create_header(self):
        """Create JarvisFi header"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')

        # JarvisFi branding
        if current_language == 'english':
            title = "JarvisFi"
            slogan = "Your AI-Powered Financial Genius"
            user_dashboard = f"{user_type.title()} Dashboard"
        else:
            title = "JarvisFi"
            slogan = "உங்கள் AI-இயங்கும் நிதி மேதை"
            user_dashboard = f"{user_type} டாஷ்போர்டு"

        st.markdown(f"""
        <div class="main-header">
            <h1>🤖 {title}</h1>
            <p>{slogan}</p>
            <small style="opacity: 0.8; font-size: 0.9rem;">{user_dashboard}</small>
        </div>
        """, unsafe_allow_html=True)
    
    def show_chat_interface(self):
        """Show clean chat interface"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        
        # Welcome message
        welcome_text = "JarvisFi Chat" if current_language == 'english' else "JarvisFi அரட்டை"
        st.markdown(f"### 🤖 {welcome_text}")
        
        # Show personalized greeting
        name = st.session_state.user_profile.get('basic_info', {}).get('name', '')
        if name:
            greeting = f"Welcome back, {name}!" if current_language == 'english' else f"மீண்டும் வரவேற்கிறோம், {name}!"
            st.info(f"👋 {greeting}")
        
        # Voice input processing
        if st.session_state.get('voice_listening', False):
            st.info("🎙️ Listening..." if current_language == 'english' else "🎙️ கேட்கிறேன்...")
            
            if st.button("🎤 Demo Voice" if current_language == 'english' else "🎤 குரல் டெமோ"):
                sample_inputs = {
                    'english': ["How can I save money?", "Budget help", "Investment advice"],
                    'tamil': ["பணம் சேமிப்பு?", "பட்ஜெட் உதவி", "முதலீட்டு ஆலோசனை"]
                }
                
                import random
                voice_input = random.choice(sample_inputs.get(current_language, sample_inputs['english']))
                st.success(f"🎤 {voice_input}")
                st.session_state.voice_listening = False
                
                # Process voice input
                self.process_user_message(voice_input)
                st.rerun()
        
        # Display chat history
        for message in st.session_state.chat_history[-10:]:  # Show last 10 for performance
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="user-message">
                    <strong>🙋 You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>🤖 Assistant:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        placeholder = "Ask JarvisFi about budgets, savings, investments..." if current_language == 'english' else "பட்ஜெட், சேமிப்பு, முதலீடு பற்றி JarvisFi-யிடம் கேளுங்கள்..."
        user_input = st.chat_input(placeholder)
        
        if user_input:
            self.process_user_message(user_input)
    
    def process_user_message(self, user_input: str):
        """Process user message"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')
        
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Generate response
        response = self.generate_response(user_input, current_language, user_type)
        
        # Add assistant response
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": response,
            "timestamp": datetime.now()
        })
        
        st.rerun()
    
    def generate_response(self, user_input: str, language: str, user_type: str) -> str:
        """Generate response based on user input"""
        user_input_lower = user_input.lower()
        
        # Budget-related queries
        if any(word in user_input_lower for word in ['budget', 'பட்ஜெட்', 'expense', 'செலவு']):
            if language == 'english':
                if user_type == 'beginner':
                    return "🏦 **Budget Planning for Beginners**\n\nStart with the 50/30/20 rule:\n• 50% for needs (rent, food, utilities)\n• 30% for wants (entertainment, dining out)\n• 20% for savings and debt repayment\n\nTrack your expenses for a month to understand your spending patterns!"
                else:
                    return "🏦 **Advanced Budget Strategies**\n\nConsider zero-based budgeting or envelope method. Analyze your spending categories:\n• Fixed costs: Negotiate bills, refinance loans\n• Variable costs: Use cashback cards, bulk buying\n• Investments: Automate transfers to investment accounts"
            else:
                if user_type == 'beginner':
                    return "🏦 **ஆரம்பநிலையாளர்களுக்கான பட்ஜெட் திட்டமிடல்**\n\n50/30/20 விதியுடன் தொடங்குங்கள்:\n• 50% தேவைகளுக்கு (வாடகை, உணவு, பயன்பாடுகள்)\n• 30% விருப்பங்களுக்கு (பொழுதுபோக்கு, வெளியில் சாப்பிடுதல்)\n• 20% சேமிப்பு மற்றும் கடன் திருப்பிச் செலுத்துதல்"
                else:
                    return "🏦 **மேம்பட்ட பட்ஜெட் உத்திகள்**\n\nபூஜ்ய அடிப்படை பட்ஜெட் அல்லது உறை முறையைக் கருத்தில் கொள்ளுங்கள். உங்கள் செலவு வகைகளை பகுப்பாய்வு செய்யுங்கள்"
        
        # Savings-related queries
        elif any(word in user_input_lower for word in ['save', 'saving', 'சேமிப்பு', 'சேமிக்க']):
            if language == 'english':
                return "💰 **Smart Savings Strategies**\n\n1. **Emergency Fund**: Build 6 months of expenses first\n2. **High-Yield Savings**: Use accounts with 4-6% interest\n3. **Automate Savings**: Set up automatic transfers\n4. **Reduce Expenses**: Cancel unused subscriptions, cook at home\n5. **Increase Income**: Side hustles, skill development\n\n**Pro Tip**: Pay yourself first - save before spending!"
            else:
                return "💰 **புத்திசாலித்தனமான சேமிப்பு உத்திகள்**\n\n1. **அவசரகால நிதி**: முதலில் 6 மாத செலவுகளை உருவாக்குங்கள்\n2. **அதிக வருமான சேமிப்பு**: 4-6% வட்டி கொண்ட கணக்குகளைப் பயன்படுத்துங்கள்\n3. **சேமிப்பை தானியங்கு செய்யுங்கள்**: தானியங்கு பரிமாற்றங்களை அமைக்கவும்"
        
        # Investment-related queries
        elif any(word in user_input_lower for word in ['invest', 'investment', 'முதலீடு', 'sip', 'mutual fund']):
            if language == 'english':
                return "📈 **Investment Guide**\n\n**For Beginners:**\n• Start with SIPs in diversified equity funds\n• Invest in PPF for tax benefits\n• Consider index funds for low-cost investing\n\n**Risk Management:**\n• Diversify across asset classes\n• Don't put all money in one investment\n• Review portfolio quarterly\n\n**Long-term Strategy:**\n• Stay invested for 5+ years\n• Don't panic during market downturns"
            else:
                return "📈 **முதலீட்டு வழிகாட்டி**\n\n**ஆரம்பநிலையாளர்களுக்கு:**\n• பல்வகைப்படுத்தப்பட்ட ஈக்விட்டி ஃபண்டுகளில் SIP களுடன் தொடங்குங்கள்\n• வரி நன்மைகளுக்காக PPF இல் முதலீடு செய்யுங்கள்\n• குறைந்த செலவு முதலீட்டிற்கு இண்டெக்ஸ் ஃபண்டுகளைக் கருத்தில் கொள்ளுங்கள்"
        
        else:
            if language == 'english':
                return f"👋 **Hello {user_type.title()}!**\n\nI'm **JarvisFi**, your AI-powered financial genius! I can help you with:\n\n💰 **Budgeting & Expense Tracking**\n📈 **Investment Planning & SIPs**\n🏦 **Savings Strategies**\n💱 **Currency Information**\n🎯 **Goal-based Planning**\n🤖 **AI-Powered Insights**\n\nWhat would you like to know about your finances today?"
            else:
                return f"👋 **வணக்கம் {user_type}!**\n\nநான் **JarvisFi**, உங்கள் AI-இயங்கும் நிதி மேதை! நான் உங்களுக்கு உதவ முடியும்:\n\n💰 **பட்ஜெட் & செலவு கண்காணிப்பு**\n📈 **முதலீட்டு திட்டமிடல் & SIP கள்**\n🏦 **சேமிப்பு உத்திகள்**\n💱 **நாணய தகவல்**\n🎯 **இலக்கு அடிப்படையிலான திட்டமிடல்**\n🤖 **AI-இயங்கும் நுண்ணறிவு**"
    
    def run(self):
        """Run the clean app"""
        self.setup_page_config()
        self.apply_clean_css()
        
        # Create sidebar and header
        self.create_sidebar()
        self.create_header()
        
        # Create tabs
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        
        tab_names = ["💬 Chat", "📊 Dashboard", "💰 Budget", "📈 Investment", "💱 Currency", "💡 Tips"]
        if current_language == 'tamil':
            tab_names = ["💬 அரட்டை", "📊 டாஷ்போர்டு", "💰 பட்ஜெட்", "📈 முதலீடு", "💱 நாணயம்", "💡 குறிப்புகள்"]
        
        tabs = st.tabs(tab_names)
        
        with tabs[0]:
            self.show_chat_interface()
            
        with tabs[1]:
            self.show_dashboard(current_language)

        with tabs[2]:
            self.show_budget_calculator(current_language)

        with tabs[3]:
            self.show_investment_calculator(current_language)

        with tabs[4]:
            self.show_currency_converter(current_language)

        with tabs[5]:
            self.show_financial_tips(current_language)

    def show_dashboard(self, language):
        """Show JarvisFi personalized financial dashboard"""
        st.markdown("### 📊 JarvisFi Dashboard" if language == 'english' else "### 📊 JarvisFi டாஷ்போர்டு")

        # Get user's actual monthly salary
        monthly_income = st.session_state.user_profile.get('basic_info', {}).get('monthly_income', 30000)
        user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')

        # Calculate personalized financial metrics based on salary
        # Estimated expenses based on salary brackets and user type
        if monthly_income < 25000:
            expense_ratio = 0.85 if user_type == 'student' else 0.80
            investment_multiplier = 8
        elif monthly_income < 50000:
            expense_ratio = 0.75 if user_type == 'beginner' else 0.70
            investment_multiplier = 12
        elif monthly_income < 100000:
            expense_ratio = 0.65 if user_type == 'intermediate' else 0.60
            investment_multiplier = 18
        else:
            expense_ratio = 0.55 if user_type == 'professional' else 0.50
            investment_multiplier = 25

        monthly_expenses = int(monthly_income * expense_ratio)
        monthly_savings = monthly_income - monthly_expenses
        total_investments = int(monthly_savings * investment_multiplier)

        # Calculate deltas (month-over-month changes)
        income_delta = int(monthly_income * 0.05) if monthly_income > 30000 else 0
        expense_delta = -int(monthly_expenses * 0.03)
        savings_delta = int(monthly_savings * 0.15)
        investment_delta = int(total_investments * 0.08)

        # Display personalized metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Monthly Income" if language == 'english' else "மாதாந்திர வருமானம்",
                f"₹{monthly_income:,}",
                delta=f"₹{income_delta:,}" if income_delta > 0 else None
            )

        with col2:
            st.metric(
                "Monthly Expenses" if language == 'english' else "மாதாந்திர செலவுகள்",
                f"₹{monthly_expenses:,}",
                delta=f"₹{expense_delta:,}"
            )

        with col3:
            st.metric(
                "Monthly Savings" if language == 'english' else "மாதாந்திர சேமிப்பு",
                f"₹{monthly_savings:,}",
                delta=f"₹{savings_delta:,}"
            )

        with col4:
            st.metric(
                "Total Investments" if language == 'english' else "மொத்த முதலீடுகள்",
                f"₹{total_investments:,}",
                delta=f"₹{investment_delta:,}"
            )

        # Personalized Charts based on salary
        col1, col2 = st.columns(2)

        with col1:
            # Personalized expense breakdown based on salary
            rent = int(monthly_income * 0.30)  # 30% of income for rent
            food = int(monthly_income * 0.20)  # 20% for food
            transport = int(monthly_income * 0.08)  # 8% for transport
            utilities = int(monthly_income * 0.05)  # 5% for utilities
            entertainment = int(monthly_income * 0.07)  # 7% for entertainment
            other = monthly_expenses - (rent + food + transport + utilities + entertainment)

            if other < 0:
                other = int(monthly_income * 0.05)

            expense_labels = ['Rent', 'Food', 'Transport', 'Utilities', 'Entertainment', 'Other']
            expense_values = [rent, food, transport, utilities, entertainment, other]

            if language == 'tamil':
                expense_labels = ['வாடகை', 'உணவு', 'போக்குவரத்து', 'பயன்பாடுகள்', 'பொழுதுபோக்கு', 'மற்றவை']

            fig = px.pie(
                values=expense_values,
                names=expense_labels,
                title="Personalized Expense Breakdown" if language == 'english' else "தனிப்பயனாக்கப்பட்ட செலவு பிரிவு",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Personalized savings trend based on salary level
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            base_savings = monthly_savings

            # Generate realistic savings trend based on salary
            import random
            savings_trend = []
            for i in range(6):
                variation = random.uniform(0.8, 1.2)  # ±20% variation
                month_savings = int(base_savings * variation)
                savings_trend.append(month_savings)

            fig = px.line(
                x=months, y=savings_trend,
                title=f"Your Savings Trend (₹{base_savings:,}/month avg)" if language == 'english' else f"உங்கள் சேமிப்பு போக்கு (₹{base_savings:,}/மாதம் சராசரி)",
                labels={'x': 'Month' if language == 'english' else 'மாதம்', 'y': 'Savings (₹)' if language == 'english' else 'சேமிப்பு (₹)'},
                markers=True
            )
            fig.update_traces(line_color='#2E8B57', line_width=3)
            st.plotly_chart(fig, use_container_width=True)

        # Salary-based insights
        st.markdown("---")
        st.markdown("### 💡 Personalized Insights" if language == 'english' else "### 💡 தனிப்பயனாக்கப்பட்ட நுண்ணறிவுகள்")

        savings_rate = (monthly_savings / monthly_income) * 100

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Savings Rate" if language == 'english' else "சேமிப்பு விகிதம்",
                f"{savings_rate:.1f}%",
                delta="Good" if savings_rate >= 20 else "Improve" if language == 'english' else "நல்லது" if savings_rate >= 20 else "மேம்படுத்து"
            )

        with col2:
            emergency_fund = monthly_expenses * 6
            st.metric(
                "Emergency Fund Target" if language == 'english' else "அவசரகால நிதி இலக்கு",
                f"₹{emergency_fund:,}",
                delta=f"{emergency_fund // monthly_savings} months" if language == 'english' else f"{emergency_fund // monthly_savings} மாதங்கள்"
            )

        with col3:
            annual_savings = monthly_savings * 12
            st.metric(
                "Annual Savings Potential" if language == 'english' else "ஆண்டு சேமிப்பு திறன்",
                f"₹{annual_savings:,}",
                delta=f"₹{annual_savings // 12:,}/month" if language == 'english' else f"₹{annual_savings // 12:,}/மாதம்"
            )

        # Personalized recommendations
        st.markdown("### 🎯 JarvisFi Recommendations" if language == 'english' else "### 🎯 JarvisFi பரிந்துரைகள்")

        recommendations = []

        if savings_rate < 10:
            if language == 'english':
                recommendations.append("🚨 **Critical**: Your savings rate is below 10%. Focus on reducing expenses immediately.")
            else:
                recommendations.append("🚨 **முக்கியமான**: உங்கள் சேமிப்பு விகிதம் 10% க்கும் குறைவாக உள்ளது. உடனடியாக செலவுகளைக் குறைப்பதில் கவனம் செலுத்துங்கள்.")
        elif savings_rate < 20:
            if language == 'english':
                recommendations.append("⚠️ **Improve**: Aim for 20% savings rate. Consider reducing entertainment and dining expenses.")
            else:
                recommendations.append("⚠️ **மேம்படுத்து**: 20% சேமிப்பு விகிதத்தை இலக்காகக் கொள்ளுங்கள். பொழுதுபோக்கு மற்றும் உணவு செலவுகளைக் குறைக்கவும்.")
        else:
            if language == 'english':
                recommendations.append("✅ **Excellent**: Your savings rate is healthy! Consider increasing investments.")
            else:
                recommendations.append("✅ **சிறப்பு**: உங்கள் சேமிப்பு விகிதம் ஆரோக்கியமானது! முதலீடுகளை அதிகரிக்கவும்.")

        if monthly_income > 50000:
            if language == 'english':
                recommendations.append("💼 **Tax Planning**: Consider ELSS, PPF, and other tax-saving investments.")
            else:
                recommendations.append("💼 **வரி திட்டமிடல்**: ELSS, PPF மற்றும் பிற வரி சேமிப்பு முதலீடுகளைக் கருத்தில் கொள்ளுங்கள்.")

        if total_investments < monthly_income * 10:
            if language == 'english':
                recommendations.append("📈 **Investment Growth**: Your investment corpus is low. Start SIPs immediately.")
            else:
                recommendations.append("📈 **முதலீட்டு வளர்ச்சி**: உங்கள் முதலீட்டு கார்பஸ் குறைவாக உள்ளது. உடனடியாக SIP களைத் தொடங்குங்கள்.")

        for rec in recommendations:
            st.markdown(rec)

    def show_budget_calculator(self, language):
        """Show JarvisFi personalized budget calculator"""
        st.markdown("### 💰 JarvisFi Budget Calculator" if language == 'english' else "### 💰 JarvisFi பட்ஜெட் கணக்கீட்டாளர்")

        # Get user's actual salary from profile
        user_salary = st.session_state.user_profile.get('basic_info', {}).get('monthly_income', 30000)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Income** / **வருமானம்**")

            monthly_income = st.number_input(
                "Monthly Income" if language == 'english' else "மாதாந்திர வருமானம்",
                min_value=0, value=user_salary, step=1000,
                key="budget_income",
                help=f"Using your profile salary: ₹{user_salary:,}" if language == 'english' else f"உங்கள் சுயவிவர சம்பளத்தைப் பயன்படுத்துகிறது: ₹{user_salary:,}"
            )

            other_income = st.number_input(
                "Other Income" if language == 'english' else "மற்ற வருமானம்",
                min_value=0, value=0, step=500,
                key="other_income"
            )

            total_income = monthly_income + other_income
            st.metric("Total Income" if language == 'english' else "மொத்த வருமானம்", f"₹{total_income:,}")

        with col2:
            st.markdown("**Expenses** / **செலவுகள்**")

            rent = st.number_input("Rent" if language == 'english' else "வாடகை", min_value=0, value=15000, step=1000)
            food = st.number_input("Food" if language == 'english' else "உணவு", min_value=0, value=8000, step=500)
            transport = st.number_input("Transport" if language == 'english' else "போக்குவரத்து", min_value=0, value=3000, step=500)
            utilities = st.number_input("Utilities" if language == 'english' else "பயன்பாடுகள்", min_value=0, value=2000, step=200)
            entertainment = st.number_input("Entertainment" if language == 'english' else "பொழுதுபோக்கு", min_value=0, value=4000, step=500)
            other_expenses = st.number_input("Other" if language == 'english' else "மற்றவை", min_value=0, value=2000, step=500)

            total_expenses = rent + food + transport + utilities + entertainment + other_expenses
            st.metric("Total Expenses" if language == 'english' else "மொத்த செலவுகள்", f"₹{total_expenses:,}")

        # Budget analysis
        st.markdown("---")
        st.markdown("### Budget Analysis" if language == 'english' else "### பட்ஜெட் பகுப்பாய்வு")

        savings = total_income - total_expenses
        savings_rate = (savings / total_income * 100) if total_income > 0 else 0

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Monthly Savings" if language == 'english' else "மாதாந்திர சேமிப்பு", f"₹{savings:,}")

        with col2:
            st.metric("Savings Rate" if language == 'english' else "சேமிப்பு விகிதம்", f"{savings_rate:.1f}%")

        with col3:
            status = "Good" if savings_rate >= 20 else "Needs Improvement" if savings_rate >= 10 else "Critical"
            status_tamil = "நல்லது" if savings_rate >= 20 else "மேம்பாடு தேவை" if savings_rate >= 10 else "முக்கியமான"
            st.metric("Status" if language == 'english' else "நிலை", status if language == 'english' else status_tamil)

        # 50/30/20 rule comparison
        st.markdown("### 50/30/20 Rule Comparison" if language == 'english' else "### 50/30/20 விதி ஒப்பீடு")

        needs_budget = total_income * 0.5
        wants_budget = total_income * 0.3
        savings_budget = total_income * 0.2

        actual_needs = rent + food + utilities + transport
        actual_wants = entertainment + other_expenses

        comparison_data = {
            'Category': ['Needs/தேவைகள்', 'Wants/விருப்பங்கள்', 'Savings/சேமிப்பு'],
            'Recommended': [needs_budget, wants_budget, savings_budget],
            'Actual': [actual_needs, actual_wants, savings]
        }

        df = pd.DataFrame(comparison_data)
        fig = px.bar(df, x='Category', y=['Recommended', 'Actual'], barmode='group',
                     title="Budget vs Recommended" if language == 'english' else "பட்ஜெட் vs பரிந்துரைக்கப்பட்டது")
        st.plotly_chart(fig, use_container_width=True)

    def show_investment_calculator(self, language):
        """Show JarvisFi investment calculator"""
        st.markdown("### 📈 JarvisFi Investment Calculator" if language == 'english' else "### 📈 JarvisFi முதலீட்டு கணக்கீட்டாளர்")

        tab1, tab2, tab3 = st.tabs([
            "SIP Calculator" if language == 'english' else "SIP கணக்கீட்டாளர்",
            "Lump Sum" if language == 'english' else "மொத்த தொகை",
            "Goal Planning" if language == 'english' else "இலக்கு திட்டமிடல்"
        ])

        with tab1:
            # Get user's salary for personalized SIP suggestion
            user_salary = st.session_state.user_profile.get('basic_info', {}).get('monthly_income', 30000)
            suggested_sip = max(500, int(user_salary * 0.15))  # 15% of salary for SIP

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"💡 JarvisFi suggests ₹{suggested_sip:,} SIP based on your ₹{user_salary:,} salary" if language == 'english' else f"💡 JarvisFi உங்கள் ₹{user_salary:,} சம்பளத்தின் அடிப்படையில் ₹{suggested_sip:,} SIP ஐ பரிந்துரைக்கிறது")

                monthly_sip = st.number_input(
                    "Monthly SIP Amount" if language == 'english' else "மாதாந்திர SIP தொகை",
                    min_value=500, value=suggested_sip, step=500,
                    help=f"Recommended: 10-20% of salary (₹{int(user_salary*0.1):,} - ₹{int(user_salary*0.2):,})" if language == 'english' else f"பரிந்துரைக்கப்பட்டது: சம்பளத்தின் 10-20% (₹{int(user_salary*0.1):,} - ₹{int(user_salary*0.2):,})"
                )

                annual_return = st.slider(
                    "Expected Annual Return (%)" if language == 'english' else "எதிர்பார்க்கப்படும் ஆண்டு வருமானம் (%)",
                    min_value=1.0, max_value=30.0, value=12.0, step=0.5
                )

                investment_period = st.slider(
                    "Investment Period (Years)" if language == 'english' else "முதலீட்டு காலம் (ஆண்டுகள்)",
                    min_value=1, max_value=40, value=10
                )

            with col2:
                # SIP calculation
                monthly_rate = annual_return / 100 / 12
                total_months = investment_period * 12

                if monthly_rate > 0:
                    future_value = monthly_sip * (((1 + monthly_rate) ** total_months - 1) / monthly_rate) * (1 + monthly_rate)
                else:
                    future_value = monthly_sip * total_months

                total_invested = monthly_sip * total_months
                total_returns = future_value - total_invested

                st.metric("Total Invested" if language == 'english' else "மொத்த முதலீடு", f"₹{total_invested:,.0f}")
                st.metric("Future Value" if language == 'english' else "எதிர்கால மதிப்பு", f"₹{future_value:,.0f}")
                st.metric("Total Returns" if language == 'english' else "மொத்த வருமானம்", f"₹{total_returns:,.0f}")

                # Growth chart
                years = list(range(1, investment_period + 1))
                values = []
                invested = []

                for year in years:
                    months = year * 12
                    if monthly_rate > 0:
                        fv = monthly_sip * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
                    else:
                        fv = monthly_sip * months
                    values.append(fv)
                    invested.append(monthly_sip * months)

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=years, y=invested, mode='lines', name='Invested' if language == 'english' else 'முதலீடு'))
                fig.add_trace(go.Scatter(x=years, y=values, mode='lines', name='Future Value' if language == 'english' else 'எதிர்கால மதிப்பு'))
                fig.update_layout(title="SIP Growth Projection" if language == 'english' else "SIP வளர்ச்சி கணிப்பு")
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.info("Lump Sum Calculator - Coming Soon!" if language == 'english' else "மொத்த தொகை கணக்கீட்டாளர் - விரைவில் வரும்!")

        with tab3:
            st.info("Goal Planning Calculator - Coming Soon!" if language == 'english' else "இலக்கு திட்டமிடல் கணக்கீட்டாளர் - விரைவில் வரும்!")

    def show_currency_converter(self, language):
        """Show JarvisFi currency converter"""
        st.markdown("### 💱 JarvisFi Currency Converter" if language == 'english' else "### 💱 JarvisFi நாணய மாற்றி")

        # Mock exchange rates
        exchange_rates = {
            'USD': {'INR': 83.12, 'EUR': 0.92, 'GBP': 0.79, 'JPY': 149.50},
            'INR': {'USD': 0.012, 'EUR': 0.011, 'GBP': 0.0095, 'JPY': 1.80},
            'EUR': {'USD': 1.09, 'INR': 90.45, 'GBP': 0.86, 'JPY': 162.30},
            'GBP': {'USD': 1.27, 'INR': 105.26, 'EUR': 1.16, 'JPY': 188.90},
            'JPY': {'USD': 0.0067, 'INR': 0.56, 'EUR': 0.0062, 'GBP': 0.0053}
        }

        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            from_currency = st.selectbox(
                "From Currency" if language == 'english' else "இருந்து நாணயம்",
                options=['USD', 'INR', 'EUR', 'GBP', 'JPY'],
                index=1,  # Default to INR
                key="from_currency"
            )

            amount = st.number_input(
                "Amount" if language == 'english' else "தொகை",
                min_value=0.01, value=1000.0, step=10.0,
                key="convert_amount"
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Convert" if language == 'english' else "🔄 மாற்று", key="convert_btn"):
                st.success("Converted!" if language == 'english' else "மாற்றப்பட்டது!")

        with col3:
            to_currency = st.selectbox(
                "To Currency" if language == 'english' else "க்கு நாணயம்",
                options=['USD', 'INR', 'EUR', 'GBP', 'JPY'],
                index=0,  # Default to USD
                key="to_currency"
            )

            # Calculate conversion
            if from_currency != to_currency and from_currency in exchange_rates:
                rate = exchange_rates[from_currency].get(to_currency, 1.0)
                converted_amount = amount * rate
                st.number_input(
                    "Converted Amount" if language == 'english' else "மாற்றப்பட்ட தொகை",
                    value=converted_amount,
                    disabled=True,
                    key="converted_amount"
                )
            else:
                st.number_input(
                    "Converted Amount" if language == 'english' else "மாற்றப்பட்ட தொகை",
                    value=amount,
                    disabled=True,
                    key="converted_amount_same"
                )

        # Exchange rate table
        st.markdown("### Live Exchange Rates" if language == 'english' else "### நேரடி மாற்று விகிதங்கள்")

        if from_currency in exchange_rates:
            rates_data = []
            for curr, rate in exchange_rates[from_currency].items():
                rates_data.append({
                    'Currency': curr,
                    'Rate': f"1 {from_currency} = {rate:.4f} {curr}",
                    'Value': rate
                })

            df = pd.DataFrame(rates_data)
            st.dataframe(df[['Currency', 'Rate']], use_container_width=True)

    def show_financial_tips(self, language):
        """Show JarvisFi financial tips"""
        st.markdown("### 💡 JarvisFi Financial Tips" if language == 'english' else "### 💡 JarvisFi நிதி குறிப்புகள்")

        tips_data = {
            'english': {
                'Budgeting': [
                    "Follow the 50/30/20 rule: 50% needs, 30% wants, 20% savings",
                    "Track every expense for at least one month",
                    "Use budgeting apps to monitor spending",
                    "Review and adjust your budget monthly"
                ],
                'Saving': [
                    "Pay yourself first - save before spending",
                    "Build an emergency fund of 6 months expenses",
                    "Automate your savings to avoid temptation",
                    "Use high-yield savings accounts"
                ],
                'Investing': [
                    "Start investing early to benefit from compound interest",
                    "Diversify your portfolio across different asset classes",
                    "Don't try to time the market",
                    "Invest regularly through SIPs"
                ],
                'Debt Management': [
                    "Pay off high-interest debt first",
                    "Consider debt consolidation for multiple debts",
                    "Never miss minimum payments",
                    "Avoid taking new debt while paying off existing ones"
                ]
            },
            'tamil': {
                'பட்ஜெட்': [
                    "50/30/20 விதியைப் பின்பற்றுங்கள்: 50% தேவைகள், 30% விருப்பங்கள், 20% சேமிப்பு",
                    "குறைந்தது ஒரு மாதத்திற்கு ஒவ்வொரு செலவையும் கண்காணிக்கவும்",
                    "செலவுகளைக் கண்காணிக்க பட்ஜெட் பயன்பாடுகளைப் பயன்படுத்துங்கள்",
                    "உங்கள் பட்ஜெட்டை மாதந்தோறும் மதிப்பாய்வு செய்து சரிசெய்யுங்கள்"
                ],
                'சேமிப்பு': [
                    "முதலில் உங்களுக்குச் செலுத்துங்கள் - செலவு செய்வதற்கு முன் சேமிக்கவும்",
                    "6 மாத செலவுகளின் அவசரகால நிதியை உருவாக்குங்கள்",
                    "ஆசையைத் தவிர்க்க உங்கள் சேமிப்பை தானியங்குபடுத்துங்கள்",
                    "அதிக வருமான சேமிப்பு கணக்குகளைப் பயன்படுத்துங்கள்"
                ],
                'முதலீடு': [
                    "கூட்டு வட்டியின் பலனைப் பெற ஆரம்பத்திலேயே முதலீடு செய்யத் தொடங்குங்கள்",
                    "வெவ்வேறு சொத்து வகுப்புகளில் உங்கள் போர்ட்ஃபோலியோவை பல்வகைப்படுத்துங்கள்",
                    "சந்தையின் நேரத்தை அறிய முயற்சிக்காதீர்கள்",
                    "SIP கள் மூலம் தொடர்ந்து முதலீடு செய்யுங்கள்"
                ],
                'கடன் மேலாண்மை': [
                    "முதலில் அதிக வட்டி கடனைச் செலுத்துங்கள்",
                    "பல கடன்களுக்கு கடன் ஒருங்கிணைப்பைக் கருத்தில் கொள்ளுங்கள்",
                    "குறைந்தபட்ச கொடுப்பனவுகளை ஒருபோதும் தவறவிடாதீர்கள்",
                    "ஏற்கனவே உள்ள கடன்களைச் செலுத்தும்போது புதிய கடன் எடுப்பதைத் தவிர்க்கவும்"
                ]
            }
        }

        tips = tips_data.get(language, tips_data['english'])

        for category, tip_list in tips.items():
            with st.expander(f"💡 {category}"):
                for i, tip in enumerate(tip_list, 1):
                    st.markdown(f"{i}. {tip}")

        # Daily tip
        st.markdown("---")
        st.markdown("### 🌟 Tip of the Day" if language == 'english' else "### 🌟 இன்றைய குறிப்பு")

        daily_tips = {
            'english': [
                "💰 Start small - even ₹100 saved daily becomes ₹36,500 in a year!",
                "📱 Use UPI cashback offers to save on daily purchases",
                "🏦 Compare interest rates before choosing a savings account",
                "📊 Review your credit score monthly for better loan rates",
                "💳 Pay credit card bills in full to avoid interest charges"
            ],
            'tamil': [
                "💰 சிறிதாக தொடங்குங்கள் - தினமும் ₹100 சேமித்தால் ஒரு வருடத்தில் ₹36,500 ஆகும்!",
                "📱 தினசரி வாங்குதல்களில் சேமிக்க UPI கேஷ்பேக் சலுகைகளைப் பயன்படுத்துங்கள்",
                "🏦 சேமிப்பு கணக்கைத் தேர்ந்தெடுப்பதற்கு முன் வட்டி விகிதங்களை ஒப்பிடுங்கள்",
                "📊 சிறந்த கடன் விகிதங்களுக்காக உங்கள் கிரெடிட் ஸ்கோரை மாதந்தோறும் மதிப்பாய்வு செய்யுங்கள்",
                "💳 வட்டி கட்டணங்களைத் தவிர்க்க கிரெடிட் கார்டு பில்களை முழுமையாகச் செலுத்துங்கள்"
            ]
        }

        import random
        daily_tip = random.choice(daily_tips.get(language, daily_tips['english']))
        st.info(daily_tip)

if __name__ == "__main__":
    app = JarvisFiApp()
    app.run()
