"""
Enhanced UI Components for Personal Finance Chatbot
Provides clean, attractive, and user-friendly interface elements
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional
import base64

class EnhancedUI:
    """
    Enhanced UI components for better user experience
    """
    
    def __init__(self):
        """Initialize Enhanced UI"""
        pass  # CSS will be set up when needed
    
    def setup_custom_css(self, dark_mode=False):
        """Setup custom CSS for enhanced UI with dark/light mode support"""
        try:
            # Define theme colors based on dark mode
            if dark_mode:
                bg_color = "#1e1e1e"
                text_color = "#ffffff"
                card_bg = "#2d2d2d"
                border_color = "#444444"
                gradient_primary = "linear-gradient(135deg, #4a5568 0%, #2d3748 100%)"
                gradient_secondary = "linear-gradient(135deg, #2d3748 0%, #1a202c 100%)"
            else:
                bg_color = "#ffffff"
                text_color = "#333333"
                card_bg = "#ffffff"
                border_color = "#e0e0e0"
                gradient_primary = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                gradient_secondary = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"

            # Apply CSS with theme colors
            st.markdown(f"""
            <style>
            .stApp {{
                background-color: {bg_color};
                color: {text_color};
            }}

            /* Main container styling */
            .main-container {{
                padding: 1rem;
                border-radius: 10px;
                background: {gradient_primary};
                margin-bottom: 1rem;
                color: white;
            }}

            /* Card styling */
            .info-card {{
                background: {card_bg};
                color: {text_color};
                padding: 1.5rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin: 1rem 0;
                border-left: 4px solid #667eea;
                border: 1px solid {border_color};
            }}

            .metric-card {{
                background: {gradient_secondary};
                color: white;
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                margin: 0.5rem;
            }}

            .success-card {{
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 1rem;
                border-radius: 10px;
                margin: 1rem 0;
            }}

            .warning-card {{
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                color: white;
                padding: 1rem;
                border-radius: 10px;
                margin: 1rem 0;
            }}

            /* Button styling */
            .custom-button {{
                background: {gradient_primary};
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s ease;
            }}

            .custom-button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}

            /* Sidebar styling */
            .sidebar-content {{
                background: {gradient_primary};
                padding: 1rem;
                border-radius: 10px;
                color: white;
            }}
        
        /* Chat message styling */
        .user-message {
            background: #e3f2fd;
            padding: 1rem;
            border-radius: 15px 15px 5px 15px;
            margin: 0.5rem 0;
            border-left: 4px solid #2196f3;
        }
        
        .bot-message {
            background: #f3e5f5;
            padding: 1rem;
            border-radius: 15px 15px 15px 5px;
            margin: 0.5rem 0;
            border-left: 4px solid #9c27b0;
        }
        
        /* Language selector */
        .language-selector {
            background: white;
            border: 2px solid #667eea;
            border-radius: 25px;
            padding: 0.5rem;
            margin: 0.5rem 0;
        }
        
        /* User type badges */
        .user-type-badge {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            margin: 0.2rem;
        }
        
        .student-badge {
            background: #e8f5e8;
            color: #2e7d32;
            border: 1px solid #4caf50;
        }
        
        .professional-badge {
            background: #e3f2fd;
            color: #1565c0;
            border: 1px solid #2196f3;
        }
        
        .beginner-badge {
            background: #fff3e0;
            color: #ef6c00;
            border: 1px solid #ff9800;
        }
        
        .intermediate-badge {
            background: #f3e5f5;
            color: #7b1fa2;
            border: 1px solid #9c27b0;
        }
        
        /* Progress indicators */
        .progress-container {
            background: #f5f5f5;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .progress-step {
            display: flex;
            align-items: center;
            margin: 0.5rem 0;
        }
        
        .progress-step.completed {
            color: #4caf50;
        }
        
        .progress-step.current {
            color: #2196f3;
            font-weight: bold;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .info-card {{
                padding: 1rem;
                margin: 0.5rem 0;
            }}

            .metric-card {{
                margin: 0.25rem;
                padding: 0.75rem;
            }}
        }}

        /* Animation classes */
        .fade-in {{
            animation: fadeIn 0.5s ease-in;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .slide-in {{
            animation: slideIn 0.3s ease-out;
        }}

        @keyframes slideIn {{
            from {{ transform: translateX(-100%); }}
            to {{ transform: translateX(0); }}
        }}
        </style>
        """, unsafe_allow_html=True)

        except Exception as e:
            # Fallback CSS if there's an error
            st.markdown("""
            <style>
            .main-container {
                padding: 1rem;
                border-radius: 10px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin-bottom: 1rem;
                color: white;
            }
            .info-card {
                background: white;
                color: #333;
                padding: 1.5rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin: 1rem 0;
                border-left: 4px solid #667eea;
            }
            </style>
            """, unsafe_allow_html=True)
            print(f"CSS setup error: {e}")  # For debugging
    
    def create_header(self, title: str, subtitle: str = "", language: str = "english") -> None:
        """Create an attractive header"""
        if language == "tamil":
            icon = "🏦"
        else:
            icon = "🏦"
        
        st.markdown(f"""
        <div class="main-container fade-in">
            <h1 style="color: white; text-align: center; margin: 0;">
                {icon} {title}
            </h1>
            {f'<p style="color: white; text-align: center; margin: 0.5rem 0 0 0;">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)
    
    def create_info_card(self, title: str, content: str, icon: str = "ℹ️") -> None:
        """Create an information card"""
        st.markdown(f"""
        <div class="info-card fade-in">
            <h3 style="color: #333; margin: 0 0 1rem 0;">
                {icon} {title}
            </h3>
            <p style="color: #666; margin: 0;">{content}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def create_metric_cards(self, metrics: List[Dict]) -> None:
        """Create metric cards in a grid"""
        cols = st.columns(len(metrics))
        
        for i, metric in enumerate(metrics):
            with cols[i]:
                st.markdown(f"""
                <div class="metric-card fade-in">
                    <h2 style="margin: 0; font-size: 1.5rem;">{metric.get('value', 'N/A')}</h2>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">{metric.get('label', '')}</p>
                    {f'<p style="margin: 0; font-size: 0.8rem; opacity: 0.8;">{metric.get("delta", "")}</p>' if metric.get('delta') else ''}
                </div>
                """, unsafe_allow_html=True)
    
    def create_user_type_selector(self, options: List[Dict], current_value: str, language: str = "english") -> str:
        """Create an enhanced user type selector"""
        st.markdown("### " + ("பயனர் வகை" if language == "tamil" else "User Type"))
        
        # Create columns for user type options
        cols = st.columns(2)
        
        selected_type = current_value
        
        for i, option in enumerate(options):
            with cols[i % 2]:
                badge_class = f"{option['value']}-badge"
                
                if st.button(
                    f"{option['label']}",
                    key=f"user_type_{option['value']}",
                    help=f"Select {option['label']} profile"
                ):
                    selected_type = option['value']
                
                # Show badge
                st.markdown(f"""
                <div class="user-type-badge {badge_class}">
                    {option['label']}
                </div>
                """, unsafe_allow_html=True)
        
        return selected_type
    
    def create_language_selector(self, options: List[Dict], current_value: str) -> str:
        """Create language selector"""
        return st.selectbox(
            "🌐 Language / மொழி",
            options=[opt['value'] for opt in options],
            format_func=lambda x: next(opt['label'] for opt in options if opt['value'] == x),
            index=[opt['value'] for opt in options].index(current_value) if current_value in [opt['value'] for opt in options] else 0
        )
    
    def create_progress_indicator(self, steps: List[Dict], language: str = "english") -> None:
        """Create progress indicator"""
        st.markdown(f"""
        <div class="progress-container">
            <h4>{"முன்னேற்றம்" if language == "tamil" else "Progress"}</h4>
        """, unsafe_allow_html=True)
        
        for step in steps:
            status_class = "completed" if step.get('completed') else ("current" if step.get('current') else "")
            icon = "✅" if step.get('completed') else ("🔄" if step.get('current') else "⭕")
            
            st.markdown(f"""
            <div class="progress-step {status_class}">
                {icon} {step.get('title', '')}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def create_chat_message(self, message: str, is_user: bool = False, language: str = "english") -> None:
        """Create styled chat message"""
        message_class = "user-message" if is_user else "bot-message"
        
        st.markdown(f"""
        <div class="{message_class} fade-in">
            {message}
        </div>
        """, unsafe_allow_html=True)
    
    def create_success_alert(self, message: str, language: str = "english") -> None:
        """Create success alert"""
        st.markdown(f"""
        <div class="success-card fade-in">
            ✅ {message}
        </div>
        """, unsafe_allow_html=True)
    
    def create_warning_alert(self, message: str, language: str = "english") -> None:
        """Create warning alert"""
        st.markdown(f"""
        <div class="warning-card fade-in">
            ⚠️ {message}
        </div>
        """, unsafe_allow_html=True)
    
    def create_feature_grid(self, features: List[Dict], language: str = "english") -> None:
        """Create feature grid"""
        cols = st.columns(3)
        
        for i, feature in enumerate(features):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="info-card" style="text-align: center; min-height: 150px;">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">{feature.get('icon', '📊')}</div>
                    <h4 style="color: #333; margin: 0 0 0.5rem 0;">{feature.get('title', '')}</h4>
                    <p style="color: #666; font-size: 0.9rem; margin: 0;">{feature.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def create_enhanced_sidebar(self, profile: Dict, language_support, user_profile_manager) -> Dict:
        """Create enhanced sidebar with better organization"""
        with st.sidebar:
            # Header
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 1rem;">
                <h2 style="margin: 0;">🏦</h2>
                <p style="margin: 0; font-size: 0.9rem;">Personal Finance AI</p>
            </div>
            """, unsafe_allow_html=True)

            # Initialize profile structure if missing
            if 'user_profile' not in st.session_state:
                st.session_state.user_profile = {
                    'basic_info': {
                        'name': '',
                        'age': 25,
                        'user_type': 'beginner',
                        'language': 'english'
                    },
                    'financial_info': {
                        'monthly_income': 30000
                    }
                }

            # Ensure basic_info exists
            if 'basic_info' not in st.session_state.user_profile:
                st.session_state.user_profile['basic_info'] = {
                    'name': '',
                    'age': 25,
                    'user_type': 'beginner',
                    'language': 'english'
                }

            # Ensure financial_info exists
            if 'financial_info' not in st.session_state.user_profile:
                st.session_state.user_profile['financial_info'] = {
                    'monthly_income': 30000
                }

            # Language selector
            current_lang = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
            language_options = language_support.get_language_options()
            selected_language = self.create_language_selector(language_options, current_lang)

            # Update language in session state
            if selected_language != current_lang:
                st.session_state.user_profile['basic_info']['language'] = selected_language
                language_support.set_language(selected_language)
                # Force immediate update
                st.session_state.language_changed = True
                st.rerun()

            # Use selected language for UI elements
            active_lang = selected_language

            # Dark mode toggle
            dark_mode_text = "🌙 Dark Mode" if active_lang == 'english' else "🌙 இருண்ட பயன்முறை"
            dark_mode = st.toggle(dark_mode_text, value=st.session_state.get('dark_mode', False))

            if dark_mode != st.session_state.get('dark_mode', False):
                st.session_state.dark_mode = dark_mode
                st.rerun()

            st.markdown("---")

            # User profile section
            st.markdown(f"### {language_support.get_text('profile')}")

            # User type selector
            user_type_options = language_support.get_user_type_options()
            current_user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')

            selected_user_type = st.selectbox(
                language_support.get_text('user_type'),
                options=[opt['value'] for opt in user_type_options],
                format_func=lambda x: next(opt['label'] for opt in user_type_options if opt['value'] == x),
                index=[opt['value'] for opt in user_type_options].index(current_user_type) if current_user_type in [opt['value'] for opt in user_type_options] else 0
            )

            # Update user type if changed
            if selected_user_type != current_user_type:
                st.session_state.user_profile['basic_info']['user_type'] = selected_user_type
                st.rerun()

            # Basic info
            name = st.text_input(
                language_support.get_text('name'),
                value=st.session_state.user_profile.get('basic_info', {}).get('name', ''),
                key="sidebar_name"
            )

            age = st.number_input(
                language_support.get_text('age'),
                min_value=16,
                max_value=100,
                value=st.session_state.user_profile.get('basic_info', {}).get('age', 25),
                key="sidebar_age"
            )

            monthly_income = st.number_input(
                language_support.get_text('monthly_income'),
                min_value=0,
                value=st.session_state.user_profile.get('financial_info', {}).get('monthly_income', 30000),
                key="sidebar_income"
            )

            # Update profile
            st.session_state.user_profile['basic_info'].update({
                'name': name,
                'age': age,
                'user_type': selected_user_type,
                'language': selected_language
            })

            st.session_state.user_profile['financial_info'].update({
                'monthly_income': monthly_income
            })

            return st.session_state.user_profile

    def create_voice_interface_section(self, language_support, voice_interface=None):
        """Create voice interface section"""
        st.markdown("---")

        # Voice Interface Header
        current_lang = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        voice_title = "🎤 Voice Assistant" if current_lang == 'english' else "🎤 குரல் உதவியாளர்"

        st.markdown(f"### {voice_title}")

        # Voice status indicator
        voice_status = "🟢 Ready" if current_lang == 'english' else "🟢 தயார்"
        if not voice_interface:
            voice_status = "🟡 Installing..." if current_lang == 'english' else "🟡 நிறுவுகிறது..."

        st.markdown(f"**Status:** {voice_status}")

        # Voice controls
        col1, col2, col3 = st.columns(3)

        with col1:
            listen_text = "🎙️ Listen" if current_lang == 'english' else "🎙️ கேளுங்கள்"
            if st.button(listen_text, key="voice_listen"):
                if voice_interface:
                    st.session_state.voice_listening = True
                    st.info("Listening..." if current_lang == 'english' else "கேட்கிறேன்...")
                else:
                    st.warning("Voice interface not available. Install: pip install SpeechRecognition gTTS pygame")

        with col2:
            speak_text = "🔊 Speak" if current_lang == 'english' else "🔊 பேசுங்கள்"
            if st.button(speak_text, key="voice_speak"):
                if voice_interface and 'last_response' in st.session_state:
                    st.session_state.voice_speaking = True
                    st.info("Speaking..." if current_lang == 'english' else "பேசுகிறேன்...")
                else:
                    st.warning("No response to speak" if current_lang == 'english' else "பேச எதுவும் இல்லை")

        with col3:
            stop_text = "⏹️ Stop" if current_lang == 'english' else "⏹️ நிறுத்து"
            if st.button(stop_text, key="voice_stop"):
                st.session_state.voice_listening = False
                st.session_state.voice_speaking = False
                st.success("Stopped" if current_lang == 'english' else "நிறுத்தப்பட்டது")

        # Voice settings
        with st.expander("🔧 Voice Settings" if current_lang == 'english' else "🔧 குரல் அமைப்புகள்"):
            # Language selection for voice
            voice_lang_options = [
                {'value': 'english', 'label': 'English'},
                {'value': 'tamil', 'label': 'தமிழ்'},
                {'value': 'hindi', 'label': 'हिंदी'},
                {'value': 'telugu', 'label': 'తెలుగు'}
            ]

            voice_lang_label = "Voice Language:" if current_lang == 'english' else "குரல் மொழி:"
            selected_voice_lang = st.selectbox(
                voice_lang_label,
                options=[opt['value'] for opt in voice_lang_options],
                format_func=lambda x: next(opt['label'] for opt in voice_lang_options if opt['value'] == x),
                index=0,
                key="voice_language_select"
            )

            # Voice speed
            speed_label = "Speech Speed:" if current_lang == 'english' else "பேச்சு வேகம்:"
            voice_speed = st.slider(speed_label, 0.5, 2.0, 1.0, 0.1, key="voice_speed")

            # Voice commands help
            help_label = "Voice Commands:" if current_lang == 'english' else "குரல் கட்டளைகள்:"
            st.markdown(f"**{help_label}**")

            if current_lang == 'english':
                st.markdown("""
                - "Help" - Get assistance
                - "Repeat" - Repeat last response
                - "Budget" - Budget analysis
                - "Savings" - Savings advice
                - "Stop" - Stop listening
                """)
            else:
                st.markdown("""
                - "உதவி" - உதவி பெறுங்கள்
                - "மீண்டும்" - கடைசி பதிலை மீண்டும் சொல்லுங்கள்
                - "பட்ஜெட்" - பட்ஜெட் பகுப்பாய்வு
                - "சேமிப்பு" - சேமிப்பு ஆலோசனை
                - "நிறுத்து" - கேட்பதை நிறுத்து
                """)

        return {
            'voice_language': selected_voice_lang,
            'voice_speed': voice_speed,
            'listening': st.session_state.get('voice_listening', False),
            'speaking': st.session_state.get('voice_speaking', False)
        }
