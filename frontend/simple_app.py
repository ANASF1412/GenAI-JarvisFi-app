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

# Add backend modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import backend modules with graceful fallbacks
watson_integration = None
budget_analyzer = None
demographic_adapter = None
nlp_processor = None
currency_converter = None
pdf_generator = None
smart_alerts = None
language_support = None
user_profile_manager = None
enhanced_ui = None
mongodb_manager = None
security_manager = None
voice_interface = None
ai_accuracy_rag = None
currency_localization = None

# Try to import each module individually
try:
    from backend.language_support import LanguageSupport
    language_support = LanguageSupport
except ImportError:
    print("⚠️ LanguageSupport not available")

try:
    from frontend.enhanced_ui import EnhancedUI
    enhanced_ui = EnhancedUI
except ImportError:
    print("⚠️ EnhancedUI not available")

try:
    from backend.watson_integration import WatsonIntegration
    watson_integration = WatsonIntegration
except ImportError:
    print("⚠️ WatsonIntegration not available")

try:
    from backend.voice_interface import VoiceInterface
    voice_interface = VoiceInterface
except ImportError:
    print("⚠️ VoiceInterface not available")

try:
    from backend.user_profile_manager import UserProfileManager
    user_profile_manager = UserProfileManager
except ImportError:
    print("⚠️ UserProfileManager not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveFinanceApp:
    def __init__(self):
        """Initialize Comprehensive Finance App with graceful fallbacks"""
        # Setup logger first
        self.logger = logging.getLogger(__name__)

        # Initialize core components with fallbacks
        self.watson = watson_integration() if watson_integration else None
        self.language_support = language_support() if language_support else self.create_fallback_language_support()
        self.enhanced_ui = enhanced_ui() if enhanced_ui else self.create_fallback_ui()
        self.user_profile_manager = user_profile_manager() if user_profile_manager else self.create_fallback_profile_manager()
        self.voice_interface = voice_interface() if voice_interface else self.create_fallback_voice_interface()

        # Optional advanced features (can be None)
        self.mongodb_manager = None
        self.security_manager = None
        self.ai_rag = None
        self.currency_manager = None
        self.budget_analyzer = None
        self.demographic_adapter = None
        self.nlp_processor = None
        self.currency_converter = None
        self.pdf_generator = None
        self.alert_system = None

        self.logger.info("✅ Finance app initialized with available features")

        # Initialize session state and user data
        self.init_session_state()
        self.load_user_data()

    def create_fallback_language_support(self):
        """Create fallback language support"""
        class FallbackLanguageSupport:
            def __init__(self):
                self.current_language = 'english'

            def set_language(self, language):
                self.current_language = language

            def get_text(self, key):
                texts = {
                    'ask_question': "Ask about budgets, savings, investments..." if self.current_language == 'english' else "பட்ஜெட், சேமிப்பு, முதலீடு பற்றி கேளுங்கள்..."
                }
                return texts.get(key, key)

            def translate_response(self, text):
                return text  # Simple passthrough

        return FallbackLanguageSupport()

    def create_fallback_ui(self):
        """Create fallback UI"""
        class FallbackUI:
            def setup_custom_css(self, dark_mode=False):
                pass

            def create_info_card(self, title, content, icon):
                st.info(f"{icon} **{title}**: {content}")

            def create_chat_message(self, content, is_user=True, language='english'):
                role = "🙋 You" if is_user else "🤖 Assistant"
                st.markdown(f"**{role}:** {content}")

        return FallbackUI()

    def create_fallback_profile_manager(self):
        """Create fallback profile manager"""
        class FallbackProfileManager:
            def create_user_profile(self, data):
                return {
                    'basic_info': {
                        'name': data.get('name', ''),
                        'age': data.get('age', 25),
                        'user_type': data.get('user_type', 'beginner'),
                        'language': data.get('language', 'english'),
                        'currency': data.get('currency', 'INR')
                    }
                }

            def get_personalized_greeting(self, profile, language):
                name = profile.get('basic_info', {}).get('name', 'User')
                if language == 'tamil':
                    return f"வணக்கம் {name}! உங்கள் நிதி உதவியாளருக்கு வரவேற்கிறோம்."
                return f"Welcome {name}! Ready to manage your finances?"

        return FallbackProfileManager()

    def create_fallback_voice_interface(self):
        """Create fallback voice interface"""
        class FallbackVoiceInterface:
            def text_to_speech(self, text, language='english'):
                pass  # No voice output in fallback

        return FallbackVoiceInterface()
        
    def setup_page_config(self):
        """Setup page configuration"""
        try:
            st.set_page_config(
                page_title="Personal Finance Assistant",
                page_icon="💰",
                layout="wide",
                initial_sidebar_state="expanded"
            )
        except Exception as e:
            # Page config already set, ignore
            pass

    def setup_session_state(self):
        """Setup basic session state for compatibility"""
        if 'language' not in st.session_state:
            st.session_state.language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')

        if 'user_type' not in st.session_state:
            st.session_state.user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')
        
    def init_session_state(self):
        """Initialize comprehensive session state"""
        if 'user_profile' not in st.session_state:
            # Initialize with comprehensive default profile
            st.session_state.user_profile = self.user_profile_manager.create_user_profile({
                'name': '',
                'age': 25,
                'user_type': 'beginner',
                'language': 'english',
                'monthly_income': 30000,
                'currency': 'INR',
                'location': 'India'
            })
            # Ensure language is properly set
            self.language_support.set_language('english')

        # Initialize comprehensive session variables
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False

        if 'voice_listening' not in st.session_state:
            st.session_state.voice_listening = False

        if 'voice_speaking' not in st.session_state:
            st.session_state.voice_speaking = False

        if 'security_authenticated' not in st.session_state:
            st.session_state.security_authenticated = False

        if 'user_data_encrypted' not in st.session_state:
            st.session_state.user_data_encrypted = True

        if 'ai_accuracy_enabled' not in st.session_state:
            st.session_state.ai_accuracy_enabled = True

        if 'rag_enabled' not in st.session_state:
            st.session_state.rag_enabled = True

    def load_user_data(self):
        """Load user data from secure storage"""
        try:
            if self.mongodb_manager:
                # Try to load from MongoDB if available
                try:
                    user_data = self.mongodb_manager.get_user_data(st.session_state.get('user_id', 'default'))
                    if user_data:
                        st.session_state.user_profile.update(user_data)
                        self.logger.info("✅ User data loaded from MongoDB")
                except AttributeError:
                    # Method doesn't exist, use fallback
                    self.logger.info("📁 MongoDB method not available, using local storage")
            else:
                # Fallback to local storage
                self.logger.info("📁 Using local storage fallback")
        except Exception as e:
            self.logger.error(f"❌ Error loading user data: {e}")
    
    def apply_simple_css(self):
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
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
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
    
    def create_comprehensive_sidebar(self):
        """Create simple, working sidebar"""
        with st.sidebar:
            # User Profile Section
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
                if self.language_support:
                    self.language_support.set_language(selected_lang)
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

            st.markdown("---")

            # Simple Settings
            st.markdown("### ⚙️ Settings" if current_language == 'english' else "### ⚙️ அமைப்புகள்")

            # AI Features toggle
            ai_enabled = st.toggle(
                "AI Features" if current_language == 'english' else "AI அம்சங்கள்",
                value=st.session_state.get('ai_accuracy_enabled', True),
                key="ai_toggle"
            )
            st.session_state.ai_accuracy_enabled = ai_enabled
            st.session_state.rag_enabled = ai_enabled



            # Currency selector (simple)
            st.markdown("### 💱 Currency" if current_language == 'english' else "### 💱 நாணயம்")

            currency_options = ['INR', 'USD', 'EUR', 'GBP', 'JPY']
            current_currency = st.session_state.user_profile.get('basic_info', {}).get('currency', 'INR')

            selected_currency = st.selectbox(
                "Currency" if current_language == 'english' else "நாணயம்",
                options=currency_options,
                index=currency_options.index(current_currency) if current_currency in currency_options else 0,
                key="currency_selector"
            )

            if selected_currency != current_currency:
                st.session_state.user_profile['basic_info']['currency'] = selected_currency
                st.rerun()


    
    def create_header(self):
        """Create simple header"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')

        title = "Personal Finance Assistant" if current_language == 'english' else "தனிப்பட்ட நிதி உதவியாளர்"
        subtitle = f"{user_type.title()} Dashboard" if current_language == 'english' else f"{user_type} டாஷ்போர்டு"

        st.markdown(f"""
        <div class="main-header">
            <h1>💰 {title}</h1>
            <p>{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def show_chat_interface(self):
        """Show comprehensive chat interface with all advanced features"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')

        # Enhanced chat header
        welcome_text = "Personal Finance Assistant" if current_language == 'english' else "தனிப்பட்ட நிதி உதவியாளர்"
        st.markdown(f"### 💬 {welcome_text}")

        # Show personalized greeting
        if st.session_state.user_profile.get('basic_info', {}).get('name'):
            try:
                if hasattr(self.user_profile_manager, 'get_personalized_greeting'):
                    greeting = self.user_profile_manager.get_personalized_greeting(
                        st.session_state.user_profile,
                        current_language
                    )
                    if hasattr(self.enhanced_ui, 'create_info_card'):
                        self.enhanced_ui.create_info_card("Welcome!", greeting, "👋")
                    else:
                        st.info(f"👋 {greeting}")
                else:
                    name = st.session_state.user_profile.get('basic_info', {}).get('name', '')
                    welcome_msg = f"Welcome back, {name}!" if current_language == 'english' else f"மீண்டும் வரவேற்கிறோம், {name}!"
                    st.info(f"👋 {welcome_msg}")
            except Exception as e:
                self.logger.error(f"Greeting error: {e}")
                st.info("👋 Welcome to your Personal Finance Assistant!")

        # Voice input processing
        if st.session_state.get('voice_listening', False):
            st.info("🎙️ Listening for voice input..." if current_language == 'english' else "🎙️ குரல் உள்ளீட்டைக் கேட்கிறேன்...")

            # Voice demo button
            if st.button("🎤 Demo Voice Input" if current_language == 'english' else "🎤 குரல் உள்ளீட்டு டெமோ"):
                sample_inputs = {
                    'english': ["How can I save money?", "What's my budget status?", "Help me with investments"],
                    'tamil': ["எப்படி பணம் சேமிக்கலாம்?", "என் பட்ஜெட் நிலை என்ன?", "முதலீட்டில் உதவுங்கள்"]
                }

                import random
                voice_input = random.choice(sample_inputs.get(current_language, sample_inputs['english']))
                st.success(f"🎤 Voice detected: {voice_input}")
                st.session_state.voice_listening = False

                # Process voice input
                self.process_comprehensive_user_message(voice_input)
                st.rerun()

        # Display enhanced chat history
        for message in st.session_state.chat_history[-10:]:  # Show last 10 for performance
            try:
                if hasattr(self.enhanced_ui, 'create_chat_message'):
                    if message['role'] == 'user':
                        self.enhanced_ui.create_chat_message(message['content'], is_user=True, language=current_language)
                    else:
                        self.enhanced_ui.create_chat_message(message['content'], is_user=False, language=current_language)
                else:
                    # Simple fallback chat display
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
            except Exception as e:
                self.logger.error(f"Chat display error: {e}")
                # Ultra-simple fallback
                role_icon = "🙋" if message['role'] == 'user' else "🤖"
                role_name = "You" if message['role'] == 'user' else "Assistant"
                st.markdown(f"**{role_icon} {role_name}:** {message['content']}")

        # Enhanced chat input
        try:
            if hasattr(self.language_support, 'get_text'):
                placeholder = self.language_support.get_text('ask_question')
            else:
                placeholder = "Ask about budgets, savings, investments..." if current_language == 'english' else "பட்ஜெட், சேமிப்பு, முதலீடு பற்றி கேளுங்கள்..."
        except:
            placeholder = "Ask about budgets, savings, investments..." if current_language == 'english' else "பட்ஜெட், சேமிப்பு, முதலீடு பற்றி கேளுங்கள்..."

        user_input = st.chat_input(placeholder)

        if user_input:
            self.process_comprehensive_user_message(user_input)
    
    def process_comprehensive_user_message(self, user_input: str):
        """Process user message with all advanced features"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')

        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })

        # Generate comprehensive response
        response = self.generate_comprehensive_response(user_input, current_language, user_type)

        # Add assistant response
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now()
        })

        # Store last response for voice output
        st.session_state.last_response = response

        # Voice output if enabled
        if st.session_state.get('voice_speaking', False) and self.voice_interface:
            try:
                self.voice_interface.text_to_speech(response, language=current_language)
            except Exception as e:
                self.logger.error(f"Voice output failed: {e}")

        # Save to database if available
        if self.mongodb_manager:
            try:
                # Try different method names for compatibility
                if hasattr(self.mongodb_manager, 'save_chat_message'):
                    self.mongodb_manager.save_chat_message(
                        st.session_state.get('user_id', 'default'),
                        user_input,
                        response
                    )
                elif hasattr(self.mongodb_manager, 'store_chat_history'):
                    self.mongodb_manager.store_chat_history(
                        st.session_state.get('user_id', 'default'),
                        {'user': user_input, 'assistant': response}
                    )
            except Exception as e:
                self.logger.error(f"Database save failed: {e}")

        st.rerun()
    
    def generate_comprehensive_response(self, user_input: str, language: str, user_type: str) -> str:
        """Generate comprehensive response using available features"""
        try:
            # Set language for processing
            if self.language_support:
                self.language_support.set_language(language)

            # Process query with NLP if available
            query_analysis = None
            if self.nlp_processor:
                try:
                    query_analysis = self.nlp_processor.process_query(user_input, st.session_state.user_profile)
                except Exception as e:
                    self.logger.error(f"NLP processing failed: {e}")

            # Use AI accuracy and RAG if available and enabled
            if self.ai_rag and st.session_state.get('ai_accuracy_enabled', True):
                try:
                    # Get fact-checked response with sources
                    rag_response = self.ai_rag.get_verified_response(
                        user_input,
                        query_analysis,
                        language,
                        user_type
                    )

                    if rag_response and rag_response.get('success'):
                        response = rag_response['response']

                        # Add sources if available
                        if rag_response.get('sources'):
                            sources_text = "\n\n📚 Sources:" if language == 'english' else "\n\n📚 ஆதாரங்கள்:"
                            for i, source in enumerate(rag_response['sources'][:3], 1):
                                sources_text += f"\n{i}. {source}"
                            response += sources_text

                        # Add disclaimer
                        disclaimer = "\n\n⚠️ This is AI-generated advice. Please consult a financial advisor for personalized guidance." if language == 'english' else "\n\n⚠️ இது AI உருவாக்கிய ஆலோசனை. தனிப்பயனாக்கப்பட்ட வழிகாட்டுதலுக்கு நிதி ஆலோசகரை அணுகவும்."
                        response += disclaimer

                        return response
                except Exception as e:
                    self.logger.error(f"AI RAG processing failed: {e}")

            # Fallback to Watson integration if available
            if self.watson:
                try:
                    watson_response = self.watson.get_response(
                        user_input,
                        st.session_state.user_profile,
                        query_analysis
                    )

                    if watson_response:
                        # Translate response if needed and language support available
                        if language == 'tamil' and self.language_support:
                            try:
                                translated_response = self.language_support.translate_response(watson_response)
                                return translated_response
                            except:
                                pass  # Fall through to original response
                        return watson_response

                except Exception as e:
                    self.logger.error(f"Watson integration failed: {e}")

            # Enhanced fallback responses
            return self.generate_enhanced_fallback_response(user_input, language, user_type)

        except Exception as e:
            self.logger.error(f"Comprehensive response generation failed: {e}")
            return self.generate_simple_fallback_response(language)

    def generate_enhanced_fallback_response(self, user_input: str, language: str, user_type: str) -> str:
        """Generate enhanced fallback response"""
        user_input_lower = user_input.lower()

        # Budget-related queries
        if any(word in user_input_lower for word in ['budget', 'பட்ஜெட்', 'expense', 'செலவு']):
            if language == 'english':
                if user_type == 'beginner':
                    return "🏦 **Budget Planning for Beginners**\n\nStart with the 50/30/20 rule:\n• 50% for needs (rent, food, utilities)\n• 30% for wants (entertainment, dining out)\n• 20% for savings and debt repayment\n\nTrack your expenses for a month to understand your spending patterns. Use apps like Mint or YNAB to get started!"
                else:
                    return "🏦 **Advanced Budget Strategies**\n\nConsider zero-based budgeting or envelope method. Analyze your spending categories and optimize:\n• Fixed costs: Negotiate bills, refinance loans\n• Variable costs: Use cashback cards, bulk buying\n• Investments: Automate transfers to investment accounts\n\nReview and adjust monthly based on your financial goals."
            else:
                if user_type == 'beginner':
                    return "🏦 **ஆரம்பநிலையாளர்களுக்கான பட்ஜெட் திட்டமிடல்**\n\n50/30/20 விதியுடன் தொடங்குங்கள்:\n• 50% தேவைகளுக்கு (வாடகை, உணவு, பயன்பாடுகள்)\n• 30% விருப்பங்களுக்கு (பொழுதுபோக்கு, வெளியில் சாப்பிடுதல்)\n• 20% சேமிப்பு மற்றும் கடன் திருப்பிச் செலுத்துதல்\n\nஉங்கள் செலவு முறைகளைப் புரிந்துகொள்ள ஒரு மாதத்திற்கு உங்கள் செலவுகளைக் கண்காணிக்கவும்!"
                else:
                    return "🏦 **மேம்பட்ட பட்ஜெட் உத்திகள்**\n\nபூஜ்ய அடிப்படை பட்ஜெட் அல்லது உறை முறையைக் கருத்தில் கொள்ளுங்கள். உங்கள் செலவு வகைகளை பகுப்பாய்வு செய்து மேம்படுத்துங்கள்:\n• நிலையான செலவுகள்: பில்களை பேரம் பேசுங்கள், கடன்களை மறுநிதியளிக்கவும்\n• மாறி செலவுகள்: கேஷ்பேக் கார்டுகள், மொத்த வாங்குதல்\n• முதலீடுகள்: முதலீட்டு கணக்குகளுக்கு தானியங்கு பரிமாற்றங்கள்"

        # Savings-related queries
        elif any(word in user_input_lower for word in ['save', 'saving', 'சேமிப்பு', 'சேமிக்க']):
            if language == 'english':
                return "💰 **Smart Savings Strategies**\n\n1. **Emergency Fund**: Build 6 months of expenses first\n2. **High-Yield Savings**: Use accounts with 4-6% interest\n3. **Automate Savings**: Set up automatic transfers\n4. **Reduce Expenses**: Cancel unused subscriptions, cook at home\n5. **Increase Income**: Side hustles, skill development\n\n**Pro Tip**: Pay yourself first - save before spending!"
            else:
                return "💰 **புத்திசாலித்தனமான சேமிப்பு உத்திகள்**\n\n1. **அவசரகால நிதி**: முதலில் 6 மாத செலவுகளை உருவாக்குங்கள்\n2. **அதிக வருமான சேமிப்பு**: 4-6% வட்டி கொண்ட கணக்குகளைப் பயன்படுத்துங்கள்\n3. **சேமிப்பை தானியங்கு செய்யுங்கள்**: தானியங்கு பரிமாற்றங்களை அமைக்கவும்\n4. **செலவுகளைக் குறைக்கவும்**: பயன்படுத்தாத சந்தாக்களை ரத்து செய்யுங்கள், வீட்டில் சமைக்கவும்\n5. **வருமானத்தை அதிகரிக்கவும்**: பக்க வேலைகள், திறன் மேம்பாடு"

        # Investment-related queries
        elif any(word in user_input_lower for word in ['invest', 'investment', 'முதலீடு', 'sip', 'mutual fund']):
            if language == 'english':
                return "📈 **Investment Guide**\n\n**For Beginners:**\n• Start with SIPs in diversified equity funds\n• Invest in PPF for tax benefits\n• Consider index funds for low-cost investing\n\n**Risk Management:**\n• Diversify across asset classes\n• Don't put all money in one investment\n• Review portfolio quarterly\n\n**Long-term Strategy:**\n• Stay invested for 5+ years\n• Don't panic during market downturns\n• Increase SIP amount annually"
            else:
                return "📈 **முதலீட்டு வழிகாட்டி**\n\n**ஆரம்பநிலையாளர்களுக்கு:**\n• பல்வகைப்படுத்தப்பட்ட ஈக்விட்டி ஃபண்டுகளில் SIP களுடன் தொடங்குங்கள்\n• வரி நன்மைகளுக்காக PPF இல் முதலீடு செய்யுங்கள்\n• குறைந்த செலவு முதலீட்டிற்கு இண்டெக்ஸ் ஃபண்டுகளைக் கருத்தில் கொள்ளுங்கள்\n\n**ரிஸ்க் மேலாண்மை:**\n• சொத்து வகைகளில் பல்வகைப்படுத்துங்கள்\n• எல்லா பணத்தையும் ஒரே முதலீட்டில் போடாதீர்கள்\n• காலாண்டுக்கு ஒருமுறை போர்ட்ஃபோலியோவை மதிப்பாய்வு செய்யுங்கள்"

        else:
            if language == 'english':
                return f"👋 **Hello {user_type.title()}!**\n\nI'm your AI financial assistant. I can help you with:\n\n💰 **Budgeting & Expense Tracking**\n📈 **Investment Planning & SIPs**\n🏦 **Savings Strategies**\n💱 **Currency Conversion**\n📊 **Financial Reports**\n🎯 **Goal-based Planning**\n\nWhat would you like to know about your finances today?"
            else:
                return f"👋 **வணக்கம் {user_type}!**\n\nநான் உங்கள் AI நிதி உதவியாளர். நான் உங்களுக்கு உதவ முடியும்:\n\n💰 **பட்ஜெட் & செலவு கண்காணிப்பு**\n📈 **முதலீட்டு திட்டமிடல் & SIP கள்**\n🏦 **சேமிப்பு உத்திகள்**\n💱 **நாணய மாற்றம்**\n📊 **நிதி அறிக்கைகள்**\n🎯 **இலக்கு அடிப்படையிலான திட்டமிடல்**\n\nஇன்று உங்கள் நிதி பற்றி என்ன தெரிந்து கொள்ள விரும்புகிறீர்கள்?"

    def generate_simple_fallback_response(self, language: str) -> str:
        """Generate simple fallback response for errors"""
        if language == 'tamil':
            return "மன்னிக்கவும், ஒரு பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்."
        else:
            return "I apologize, but I encountered an issue. Please try again."
    
    def show_budget_calculator(self):
        """Simple budget calculator"""
        st.markdown("### 💰 Budget Calculator" if st.session_state.language == 'english' else "### 💰 பட்ஜெட் கணக்கீட்டாளர்")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Income** / **வருமானம்**")
            monthly_income = st.number_input("Monthly Income / மாதாந்திர வருமானம்", min_value=0, value=50000, step=1000)
            other_income = st.number_input("Other Income / பிற வருமானம்", min_value=0, value=0, step=500)

        with col2:
            st.markdown("**Expenses** / **செலவுகள்**")
            rent = st.number_input("Rent / வாடகை", min_value=0, value=15000, step=1000)
            food = st.number_input("Food / உணவு", min_value=0, value=8000, step=500)
            transport = st.number_input("Transport / போக்குவரத்து", min_value=0, value=3000, step=500)
            utilities = st.number_input("Utilities / பயன்பாடுகள்", min_value=0, value=2000, step=500)
            other_expenses = st.number_input("Other / பிற", min_value=0, value=5000, step=500)

        total_income = monthly_income + other_income
        total_expenses = rent + food + transport + utilities + other_expenses
        savings = total_income - total_expenses

        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Income / மொத்த வருமானம்", f"₹{total_income:,}")
        with col2:
            st.metric("Total Expenses / மொத்த செலவு", f"₹{total_expenses:,}")
        with col3:
            st.metric("Savings / சேமிப்பு", f"₹{savings:,}", delta=f"{(savings/total_income*100):.1f}%" if total_income > 0 else "0%")

        if savings > 0:
            st.success("Great! You're saving money! / சிறப்பு! நீங்கள் பணம் சேமிக்கிறீர்கள்!")
        elif savings == 0:
            st.warning("You're breaking even. Try to reduce expenses. / நீங்கள் சமநிலையில் இருக்கிறீர்கள். செலவுகளைக் குறைக்க முயற்சிக்கவும்.")
        else:
            st.error("You're spending more than you earn! / நீங்கள் சம்பாதிப்பதை விட அதிகம் செலவு செய்கிறீர்கள்!")

    def show_investment_calculator(self):
        """Simple investment calculator"""
        st.markdown("### 📈 Investment Calculator" if st.session_state.language == 'english' else "### 📈 முதலீட்டு கணக்கீட்டாளர்")

        col1, col2 = st.columns(2)

        with col1:
            principal = st.number_input("Initial Investment / ஆரம்ப முதலீடு", min_value=0, value=100000, step=10000)
            monthly_sip = st.number_input("Monthly SIP / மாதாந்திர SIP", min_value=0, value=5000, step=500)

        with col2:
            annual_return = st.slider("Expected Annual Return % / எதிர்பார்க்கப்படும் ஆண்டு வருமானம் %", 1, 20, 12)
            years = st.slider("Investment Period (Years) / முதலீட்டு காலம் (ஆண்டுகள்)", 1, 30, 10)

        # Calculate compound interest
        monthly_rate = annual_return / 100 / 12
        months = years * 12

        # Future value of lump sum
        fv_lumpsum = principal * (1 + annual_return/100) ** years

        # Future value of SIP
        if monthly_sip > 0:
            fv_sip = monthly_sip * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        else:
            fv_sip = 0

        total_investment = principal + (monthly_sip * months)
        total_value = fv_lumpsum + fv_sip
        total_returns = total_value - total_investment

        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Investment / மொத்த முதலீடு", f"₹{total_investment:,.0f}")
        with col2:
            st.metric("Future Value / எதிர்கால மதிப்பு", f"₹{total_value:,.0f}")
        with col3:
            st.metric("Returns / வருமானம்", f"₹{total_returns:,.0f}", delta=f"{(total_returns/total_investment*100):.1f}%" if total_investment > 0 else "0%")

    def show_currency_converter(self):
        """Simple currency converter"""
        st.markdown("### 💱 Currency Converter" if st.session_state.language == 'english' else "### 💱 நாணய மாற்றி")

        # Simple exchange rates (in real app, these would be fetched from API)
        exchange_rates = {
            'USD': 83.12,
            'EUR': 90.45,
            'GBP': 105.23,
            'JPY': 0.56,
            'AUD': 54.78,
            'CAD': 61.34,
            'SGD': 61.89
        }

        col1, col2, col3 = st.columns(3)

        with col1:
            amount = st.number_input("Amount / தொகை", min_value=0.0, value=1000.0, step=100.0)

        with col2:
            from_currency = st.selectbox("From / இருந்து", ['INR'] + list(exchange_rates.keys()))

        with col3:
            to_currency = st.selectbox("To / வரை", ['INR'] + list(exchange_rates.keys()))

        if st.button("Convert / மாற்று"):
            if from_currency == to_currency:
                converted_amount = amount
            elif from_currency == 'INR':
                converted_amount = amount / exchange_rates[to_currency]
            elif to_currency == 'INR':
                converted_amount = amount * exchange_rates[from_currency]
            else:
                # Convert through INR
                inr_amount = amount * exchange_rates[from_currency]
                converted_amount = inr_amount / exchange_rates[to_currency]

            st.success(f"{amount:,.2f} {from_currency} = {converted_amount:,.2f} {to_currency}")

        st.markdown("---")
        st.markdown("**Exchange Rates (1 INR = ?) / மாற்று விகிதங்கள்**")

        rate_cols = st.columns(4)
        for i, (currency, rate) in enumerate(exchange_rates.items()):
            with rate_cols[i % 4]:
                st.metric(currency, f"{1/rate:.4f}")

    def show_savings_tips(self):
        """Show savings tips"""
        st.markdown("### 💡 Savings Tips" if st.session_state.language == 'english' else "### 💡 சேமிப்பு குறிப்புகள்")

        if st.session_state.language == 'english':
            tips = [
                "🏦 **50/30/20 Rule**: 50% needs, 30% wants, 20% savings",
                "📱 **Track Expenses**: Use apps to monitor your spending",
                "🛒 **Smart Shopping**: Compare prices and use coupons",
                "🍽️ **Cook at Home**: Reduce dining out expenses",
                "💡 **Energy Saving**: Use LED bulbs and unplug devices",
                "🚗 **Transportation**: Use public transport or carpool",
                "📚 **Emergency Fund**: Save 6 months of expenses",
                "💳 **Avoid Debt**: Pay credit cards in full each month"
            ]
        else:
            tips = [
                "🏦 **50/30/20 விதி**: 50% தேவைகள், 30% விருப்பங்கள், 20% சேமிப்பு",
                "📱 **செலவுகளைக் கண்காணிக்கவும்**: உங்கள் செலவுகளைக் கண்காணிக்க ஆப்ஸைப் பயன்படுத்தவும்",
                "🛒 **புத்திசாலித்தனமான ஷாப்பிங்**: விலைகளை ஒப்பிட்டு கூப்பன்களைப் பயன்படுத்தவும்",
                "🍽️ **வீட்டில் சமைக்கவும்**: வெளியில் சாப்பிடும் செலவுகளைக் குறைக்கவும்",
                "💡 **ஆற்றல் சேமிப்பு**: LED பல்புகளைப் பயன்படுத்தி சாதனங்களை அன்பிளக் செய்யவும்",
                "🚗 **போக்குவரத்து**: பொதுப் போக்குவரத்து அல்லது கார்பூலைப் பயன்படுத்தவும்",
                "📚 **அவசரகால நிதி**: 6 மாத செலவுகளைச் சேமிக்கவும்",
                "💳 **கடனைத் தவிர்க்கவும்**: கிரெடிட் கார்டுகளை ஒவ்வொரு மாதமும் முழுமையாகச் செலுத்தவும்"
            ]

        for tip in tips:
            st.markdown(tip)
            st.markdown("")

    def show_comprehensive_dashboard(self):
        """Show comprehensive dashboard with analytics"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')

        st.markdown("### 📊 Financial Dashboard" if current_language == 'english' else "### 📊 நிதி டாஷ்போர்டு")

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Monthly Income", "₹50,000", delta="5%")
        with col2:
            st.metric("Total Expenses", "₹35,000", delta="-2%")
        with col3:
            st.metric("Savings Rate", "30%", delta="3%")
        with col4:
            st.metric("Investment Value", "₹2,50,000", delta="12%")

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            # Expense breakdown
            expenses = {
                'Rent': 15000,
                'Food': 8000,
                'Transport': 3000,
                'Utilities': 2000,
                'Entertainment': 4000,
                'Others': 3000
            }

            fig = px.pie(
                values=list(expenses.values()),
                names=list(expenses.keys()),
                title="Expense Breakdown"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Savings trend
            dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='M')
            savings = [12000, 15000, 13000, 18000, 16000, 20000, 22000, 19000, 25000, 23000, 27000, 30000]

            fig = px.line(
                x=dates,
                y=savings,
                title="Savings Trend",
                labels={'x': 'Month', 'y': 'Savings (₹)'}
            )
            st.plotly_chart(fig, use_container_width=True)

    def show_ai_insights(self):
        """Show AI-powered financial insights"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')

        st.markdown("### 🧠 AI Financial Insights" if current_language == 'english' else "### 🧠 AI நிதி நுண்ணறிவு")

        if self.ai_rag and st.session_state.ai_accuracy_enabled:
            # AI-powered insights
            insights = [
                {
                    'title': 'Spending Pattern Alert' if current_language == 'english' else 'செலவு முறை எச்சரிக்கை',
                    'message': 'Your dining out expenses increased by 25% this month. Consider meal planning to save ₹3,000.' if current_language == 'english' else 'இந்த மாதம் உங்கள் வெளியில் சாப்பிடும் செலவு 25% அதிகரித்துள்ளது. ₹3,000 சேமிக்க உணவு திட்டமிடலைக் கருத்தில் கொள்ளுங்கள்.',
                    'type': 'warning'
                },
                {
                    'title': 'Investment Opportunity' if current_language == 'english' else 'முதலீட்டு வாய்ப்பு',
                    'message': 'Based on your risk profile, consider increasing SIP by ₹2,000 for better long-term returns.' if current_language == 'english' else 'உங்கள் ரிஸ்க் சுயவிவரத்தின் அடிப்படையில், சிறந்த நீண்ட கால வருமானத்திற்காக SIP ஐ ₹2,000 அதிகரிக்கவும்.',
                    'type': 'success'
                },
                {
                    'title': 'Tax Saving Reminder' if current_language == 'english' else 'வரி சேமிப்பு நினைவூட்டல்',
                    'message': 'You can save ₹15,600 in taxes by investing ₹52,000 more in ELSS funds before March 31st.' if current_language == 'english' else 'மார்ச் 31க்கு முன் ELSS ஃபண்டுகளில் ₹52,000 அதிகம் முதலீடு செய்வதன் மூலம் வரியில் ₹15,600 சேமிக்கலாம்.',
                    'type': 'info'
                }
            ]

            for insight in insights:
                if insight['type'] == 'warning':
                    st.warning(f"⚠️ **{insight['title']}**\n\n{insight['message']}")
                elif insight['type'] == 'success':
                    st.success(f"💡 **{insight['title']}**\n\n{insight['message']}")
                else:
                    st.info(f"ℹ️ **{insight['title']}**\n\n{insight['message']}")
        else:
            st.info("Enable AI Accuracy in sidebar for personalized insights" if current_language == 'english' else "தனிப்பயனாக்கப்பட்ட நுண்ணறிவுகளுக்கு பக்கப்பட்டியில் AI துல்லியத்தை இயக்கவும்")

    def show_reports_analytics(self):
        """Show comprehensive reports and analytics"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')

        st.markdown("### 📈 Reports & Analytics" if current_language == 'english' else "### 📈 அறிக்கைகள் & பகுப்பாய்வு")

        # Report generation
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📊 Monthly Report" if current_language == 'english' else "📊 மாதாந்திர அறிக்கை"):
                if self.pdf_generator:
                    try:
                        # Generate monthly report
                        report_data = {
                            'user_profile': st.session_state.user_profile,
                            'period': 'monthly',
                            'data': {
                                'income': 50000,
                                'expenses': 35000,
                                'savings': 15000,
                                'investments': 250000
                            }
                        }

                        pdf_buffer = self.pdf_generator.generate_monthly_report(report_data)

                        # Create download link
                        b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
                        href = f'<a href="data:application/pdf;base64,{b64}" download="monthly_report.pdf">Download Report</a>'
                        st.markdown(href, unsafe_allow_html=True)
                        st.success("Report generated!" if current_language == 'english' else "அறிக்கை உருவாக்கப்பட்டது!")

                    except Exception as e:
                        st.error(f"Report generation failed: {e}")
                else:
                    st.warning("PDF generator not available")

        with col2:
            if st.button("📋 Tax Report" if current_language == 'english' else "📋 வரி அறிக்கை"):
                st.info("Tax report generation coming soon!" if current_language == 'english' else "வரி அறிக்கை உருவாக்கம் விரைவில்!")

        with col3:
            if st.button("💼 Investment Report" if current_language == 'english' else "💼 முதலீட்டு அறிக்கை"):
                st.info("Investment report generation coming soon!" if current_language == 'english' else "முதலீட்டு அறிக்கை உருவாக்கம் விரைவில்!")

    def run(self):
        """Run the comprehensive app"""
        self.setup_page_config()
        self.setup_session_state()
        self.apply_simple_css()

        # Get current language and dark mode
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        dark_mode = st.session_state.get('dark_mode', False)

        # Force language setting and debug
        self.language_support.set_language(current_language)

        # Setup enhanced CSS
        try:
            if hasattr(self.enhanced_ui, 'setup_custom_css'):
                self.enhanced_ui.setup_custom_css(dark_mode)
            else:
                # Use the simple CSS from this class
                self.apply_simple_css()
        except Exception as e:
            self.logger.error(f"CSS setup error: {e}")
            # Fallback to simple CSS
            self.apply_simple_css()

        # Create comprehensive sidebar
        self.create_comprehensive_sidebar()

        # Create header
        self.create_header()

        # Create comprehensive tabs
        tab_names = [
            "💬 Chat", "📊 Dashboard", "💰 Budget", "📈 Investment",
            "💱 Currency", "🧠 AI Insights", "📈 Reports", "💡 Tips"
        ]

        if current_language == 'tamil':
            tab_names = [
                "💬 அரட்டை", "📊 டாஷ்போர்டு", "💰 பட்ஜெட்", "📈 முதலீடு",
                "💱 நாணயம்", "🧠 AI நுண்ணறிவு", "📈 அறிக்கைகள்", "💡 குறிப்புகள்"
            ]

        tabs = st.tabs(tab_names)

        with tabs[0]:
            self.show_chat_interface()

        with tabs[1]:
            self.show_comprehensive_dashboard()

        with tabs[2]:
            self.show_budget_calculator()

        with tabs[3]:
            self.show_investment_calculator()

        with tabs[4]:
            self.show_currency_converter()

        with tabs[5]:
            self.show_ai_insights()

        with tabs[6]:
            self.show_reports_analytics()

        with tabs[7]:
            self.show_savings_tips()

if __name__ == "__main__":
    app = ComprehensiveFinanceApp()
    app.run()
