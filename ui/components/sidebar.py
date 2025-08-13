"""
JarvisFi - Sidebar Component
Comprehensive sidebar with all user controls and settings
"""

import streamlit as st
import time
from datetime import datetime
from typing import Dict, Any

def render_sidebar():
    """Render comprehensive sidebar"""
    
    with st.sidebar:
        # JarvisFi branding
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 1rem;">
            <h2 style="color: white; margin: 0;">🤖 JarvisFi</h2>
            <p style="color: white; margin: 0; opacity: 0.9; font-size: 0.9rem;">Your AI Financial Genius</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User Profile Section
        render_user_profile_section()
        
        # Language & Preferences
        render_language_section()
        
        # Voice Interface Controls
        render_voice_section()
        
        # Financial Profile
        render_financial_profile_section()
        
        # Security Settings
        render_security_section()
        
        # AI Features
        render_ai_features_section()
        
        # Advanced Settings
        render_advanced_settings()
        
        # Help & Support
        render_help_section()


def render_user_profile_section():
    """Render user profile section"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    st.markdown("### 👤 " + ("User Profile" if current_language == 'en' else 
                           "பயனர் சுயவிவரம்" if current_language == 'ta' else 
                           "उपयोगकर्ता प्रोफ़ाइल" if current_language == 'hi' else "User Profile"))
    
    # Name input
    current_name = st.session_state.user_profile['basic_info']['name']
    name = st.text_input(
        "Name" if current_language == 'en' else "பெயர்" if current_language == 'ta' else "नाम",
        value=current_name,
        key="sidebar_name"
    )
    
    if name != current_name:
        st.session_state.user_profile['basic_info']['name'] = name
    
    # User type selection
    user_types = {
        'en': ['Beginner', 'Intermediate', 'Professional', 'Student', 'Farmer', 'Senior Citizen'],
        'ta': ['தொடக்கநிலை', 'இடைநிலை', 'தொழில்முறை', 'மாணவர்', 'விவசாயி', 'மூத்த குடிமகன்'],
        'hi': ['शुरुआती', 'मध्यम', 'पेशेवर', 'छात्र', 'किसान', 'वरिष्ठ नागरिक']
    }
    
    user_type_values = ['beginner', 'intermediate', 'professional', 'student', 'farmer', 'senior_citizen']
    current_user_type = st.session_state.user_profile['basic_info']['user_type']
    
    try:
        current_index = user_type_values.index(current_user_type)
    except ValueError:
        current_index = 0
    
    selected_user_type = st.selectbox(
        "User Type" if current_language == 'en' else "பயனர் வகை" if current_language == 'ta' else "उपयोगकर्ता प्रकार",
        options=user_types.get(current_language, user_types['en']),
        index=current_index,
        key="sidebar_user_type"
    )
    
    # Update user type
    new_user_type = user_type_values[user_types.get(current_language, user_types['en']).index(selected_user_type)]
    if new_user_type != current_user_type:
        st.session_state.user_profile['basic_info']['user_type'] = new_user_type


def render_language_section():
    """Render language and localization section"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    st.markdown("---")
    st.markdown("### 🌐 " + ("Language & Region" if current_language == 'en' else 
                           "மொழி & பகுதி" if current_language == 'ta' else 
                           "भाषा और क्षेत्र" if current_language == 'hi' else "Language & Region"))
    
    # Language selection
    languages = {
        'English': 'en',
        'தமிழ் (Tamil)': 'ta', 
        'हिंदी (Hindi)': 'hi',
        'తెలుగు (Telugu)': 'te'
    }
    
    current_lang_display = next(k for k, v in languages.items() if v == current_language)
    
    selected_language = st.selectbox(
        "Language" if current_language == 'en' else "மொழி" if current_language == 'ta' else "भाषा",
        options=list(languages.keys()),
        index=list(languages.keys()).index(current_lang_display),
        key="sidebar_language"
    )
    
    new_language = languages[selected_language]
    if new_language != current_language:
        st.session_state.user_profile['basic_info']['language'] = new_language
        st.rerun()
    
    # Currency selection
    currencies = ['INR', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'SGD']
    current_currency = st.session_state.user_profile['basic_info']['currency']
    
    selected_currency = st.selectbox(
        "Currency" if current_language == 'en' else "நாணயம்" if current_language == 'ta' else "मुद्रा",
        options=currencies,
        index=currencies.index(current_currency) if current_currency in currencies else 0,
        key="sidebar_currency"
    )
    
    if selected_currency != current_currency:
        st.session_state.user_profile['basic_info']['currency'] = selected_currency
    
    # Dark mode toggle
    dark_mode = st.toggle(
        "🌙 Dark Mode" if current_language == 'en' else "🌙 இருண்ட பயன்முறை" if current_language == 'ta' else "🌙 डार्क मोड",
        value=st.session_state.user_profile['preferences']['dark_mode'],
        key="sidebar_dark_mode"
    )
    
    if dark_mode != st.session_state.user_profile['preferences']['dark_mode']:
        st.session_state.user_profile['preferences']['dark_mode'] = dark_mode
        st.rerun()


def render_voice_section():
    """Render voice interface section"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    st.markdown("---")
    st.markdown("### 🎤 " + ("Voice Assistant" if current_language == 'en' else 
                           "குரல் உதவியாளர்" if current_language == 'ta' else 
                           "आवाज़ सहायक" if current_language == 'hi' else "Voice Assistant"))
    
    # Voice controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎙️ " + ("Listen" if current_language == 'en' else "கேளுங்கள்" if current_language == 'ta' else "सुनें"), key="voice_listen"):
            st.session_state.voice_listening = True
            st.success("Listening..." if current_language == 'en' else "கேட்கிறது..." if current_language == 'ta' else "सुन रहा है...")
    
    with col2:
        if st.button("🔊 " + ("Speak" if current_language == 'en' else "பேசுங்கள்" if current_language == 'ta' else "बोलें"), key="voice_speak"):
            st.session_state.voice_speaking = True
            st.success("Speaking..." if current_language == 'en' else "பேசுகிறது..." if current_language == 'ta' else "बोल रहा है...")
    
    # Voice settings
    voice_enabled = st.toggle(
        "Enable Voice" if current_language == 'en' else "குரலை இயக்கு" if current_language == 'ta' else "आवाज़ सक्षम करें",
        value=st.session_state.user_profile['preferences']['voice_enabled'],
        key="voice_enabled_toggle"
    )
    
    if voice_enabled != st.session_state.user_profile['preferences']['voice_enabled']:
        st.session_state.user_profile['preferences']['voice_enabled'] = voice_enabled
    
    # Voice speed
    voice_speed = st.slider(
        "Speech Speed" if current_language == 'en' else "பேச்சு வேகம்" if current_language == 'ta' else "बोलने की गति",
        min_value=0.5, max_value=2.0, value=1.0, step=0.1,
        key="voice_speed"
    )


def render_financial_profile_section():
    """Render financial profile section"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    st.markdown("---")
    st.markdown("### 💰 " + ("Financial Profile" if current_language == 'en' else 
                           "நிதி சுயவிவரம்" if current_language == 'ta' else 
                           "वित्तीय प्रोफ़ाइल" if current_language == 'hi' else "Financial Profile"))
    
    # Monthly income
    current_income = st.session_state.user_profile['basic_info']['monthly_income']
    monthly_income = st.number_input(
        "Monthly Income (₹)" if current_language == 'en' else "மாதாந்திர வருமானம் (₹)" if current_language == 'ta' else "मासिक आय (₹)",
        min_value=0,
        max_value=10000000,
        value=current_income,
        step=5000,
        key="sidebar_monthly_income"
    )
    
    if monthly_income != current_income:
        st.session_state.user_profile['basic_info']['monthly_income'] = monthly_income
    
    # Risk tolerance
    risk_levels = {
        'en': ['Conservative', 'Moderate', 'Aggressive'],
        'ta': ['பாதுகாப்பான', 'மிதமான', 'தீவிரமான'],
        'hi': ['रूढ़िवादी', 'मध्यम', 'आक्रामक']
    }
    
    current_risk = st.session_state.user_profile['financial_profile']['risk_tolerance']
    risk_values = ['conservative', 'moderate', 'aggressive']
    
    try:
        risk_index = risk_values.index(current_risk)
    except ValueError:
        risk_index = 1  # Default to moderate
    
    selected_risk = st.selectbox(
        "Risk Tolerance" if current_language == 'en' else "ஆபத்து சகிப்புத்தன்மை" if current_language == 'ta' else "जोखिम सहनशीलता",
        options=risk_levels.get(current_language, risk_levels['en']),
        index=risk_index,
        key="sidebar_risk_tolerance"
    )
    
    new_risk = risk_values[risk_levels.get(current_language, risk_levels['en']).index(selected_risk)]
    if new_risk != current_risk:
        st.session_state.user_profile['financial_profile']['risk_tolerance'] = new_risk
    
    # Investment experience
    experience_levels = {
        'en': ['Beginner', 'Intermediate', 'Advanced'],
        'ta': ['தொடக்கநிலை', 'இடைநிலை', 'மேம்பட்ட'],
        'hi': ['शुरुआती', 'मध्यम', 'उन्नत']
    }
    
    current_exp = st.session_state.user_profile['financial_profile']['investment_experience']
    exp_values = ['beginner', 'intermediate', 'advanced']
    
    try:
        exp_index = exp_values.index(current_exp)
    except ValueError:
        exp_index = 0  # Default to beginner
    
    selected_exp = st.selectbox(
        "Investment Experience" if current_language == 'en' else "முதலீட்டு அனுபவம்" if current_language == 'ta' else "निवेश अनुभव",
        options=experience_levels.get(current_language, experience_levels['en']),
        index=exp_index,
        key="sidebar_investment_experience"
    )
    
    new_exp = exp_values[experience_levels.get(current_language, experience_levels['en']).index(selected_exp)]
    if new_exp != current_exp:
        st.session_state.user_profile['financial_profile']['investment_experience'] = new_exp


def render_security_section():
    """Render security settings section"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    st.markdown("---")
    st.markdown("### 🔐 " + ("Security" if current_language == 'en' else 
                           "பாதுகாப்பு" if current_language == 'ta' else 
                           "सुरक्षा" if current_language == 'hi' else "Security"))
    
    # Security status
    st.markdown("**Status:** 🟢 " + ("Secure" if current_language == 'en' else "பாதுகாப்பான" if current_language == 'ta' else "सुरक्षित"))
    
    # Two-factor authentication
    two_factor = st.toggle(
        "Two-Factor Auth" if current_language == 'en' else "இரு-காரணி அங்கீகாரம்" if current_language == 'ta' else "द्विकारक प्रमाणीकरण",
        value=False,
        key="two_factor_auth"
    )
    
    # Biometric authentication
    biometric = st.toggle(
        "Biometric Auth" if current_language == 'en' else "உயிரியல் அங்கீகாரம்" if current_language == 'ta' else "बायोमेट्रिक प्रमाणीकरण",
        value=False,
        key="biometric_auth"
    )
    
    # Data encryption
    encryption = st.toggle(
        "Data Encryption" if current_language == 'en' else "தரவு குறியாக்கம்" if current_language == 'ta' else "डेटा एन्क्रिप्शन",
        value=True,
        key="data_encryption"
    )


def render_ai_features_section():
    """Render AI features section"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    st.markdown("---")
    st.markdown("### 🧠 " + ("AI Features" if current_language == 'en' else 
                           "AI அம்சங்கள்" if current_language == 'ta' else 
                           "AI सुविधाएं" if current_language == 'hi' else "AI Features"))
    
    # AI accuracy
    ai_accuracy = st.toggle(
        "AI Fact-Checking" if current_language == 'en' else "AI உண்மை சரிபார்ப்பு" if current_language == 'ta' else "AI तथ्य जांच",
        value=True,
        key="ai_accuracy"
    )
    
    # Enhanced sources
    enhanced_sources = st.toggle(
        "Enhanced Sources" if current_language == 'en' else "மேம்பட்ட ஆதாரங்கள்" if current_language == 'ta' else "उन्नत स्रोत",
        value=True,
        key="enhanced_sources"
    )
    
    # Response style
    response_styles = {
        'en': ['Professional', 'Friendly', 'Detailed', 'Concise'],
        'ta': ['தொழில்முறை', 'நட்பு', 'விரிவான', 'சுருக்கமான'],
        'hi': ['पेशेवर', 'मित्रवत', 'विस्तृत', 'संक्षिप्त']
    }
    
    response_style = st.selectbox(
        "Response Style" if current_language == 'en' else "பதில் பாணி" if current_language == 'ta' else "उत्तर शैली",
        options=response_styles.get(current_language, response_styles['en']),
        index=0,
        key="ai_response_style"
    )
    
    # Learning mode
    learning_mode = st.toggle(
        "Learning Mode" if current_language == 'en' else "கற்றல் பயன்முறை" if current_language == 'ta' else "सीखने का मोड",
        value=False,
        key="learning_mode"
    )


def render_advanced_settings():
    """Render advanced settings"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    with st.expander("🔧 " + ("Advanced Settings" if current_language == 'en' else 
                             "மேம்பட்ட அமைப்புகள்" if current_language == 'ta' else 
                             "उन्नत सेटिंग्स" if current_language == 'hi' else "Advanced Settings")):
        
        # Accessibility mode
        accessibility_mode = st.toggle(
            "Accessibility Mode" if current_language == 'en' else "அணுகல்தன்மை பயன்முறை" if current_language == 'ta' else "पहुंच मोड",
            value=st.session_state.user_profile['preferences']['accessibility_mode'],
            key="accessibility_mode"
        )
        
        if accessibility_mode != st.session_state.user_profile['preferences']['accessibility_mode']:
            st.session_state.user_profile['preferences']['accessibility_mode'] = accessibility_mode
            st.rerun()
        
        # Notifications
        notifications = st.toggle(
            "Notifications" if current_language == 'en' else "அறிவிப்புகள்" if current_language == 'ta' else "सूचनाएं",
            value=st.session_state.user_profile['preferences']['notifications'],
            key="notifications_toggle"
        )
        
        if notifications != st.session_state.user_profile['preferences']['notifications']:
            st.session_state.user_profile['preferences']['notifications'] = notifications
        
        # Performance mode
        performance_modes = ['Balanced', 'High Performance', 'Battery Saver']
        performance_mode = st.selectbox(
            "Performance Mode" if current_language == 'en' else "செயல்திறன் பயன்முறை" if current_language == 'ta' else "प्रदर्शन मोड",
            options=performance_modes,
            index=0,
            key="performance_mode"
        )
        
        # Data usage
        data_usage = st.selectbox(
            "Data Usage" if current_language == 'en' else "தரவு பயன்பாடு" if current_language == 'ta' else "डेटा उपयोग",
            options=['Unlimited', 'Limited', 'Offline Only'],
            index=0,
            key="data_usage"
        )


def render_help_section():
    """Render help and support section"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    st.markdown("---")
    st.markdown("### ℹ️ " + ("Help & Support" if current_language == 'en' else 
                           "உதவி & ஆதரவு" if current_language == 'ta' else 
                           "सहायता और समर्थन" if current_language == 'hi' else "Help & Support"))
    
    # Quick help buttons
    if st.button("📚 " + ("User Guide" if current_language == 'en' else "பயனர் வழிகாட்டி" if current_language == 'ta' else "उपयोगकर्ता गाइड"), key="user_guide"):
        st.info("User guide will open in a new tab.")
    
    if st.button("💬 " + ("Contact Support" if current_language == 'en' else "ஆதரவைத் தொடர்பு கொள்ளுங்கள்" if current_language == 'ta' else "सहायता से संपर्क करें"), key="contact_support"):
        st.info("Support chat will be available soon.")
    
    if st.button("🐛 " + ("Report Bug" if current_language == 'en' else "பிழையைப் புகாரளிக்கவும்" if current_language == 'ta' else "बग रिपोर्ट करें"), key="report_bug"):
        st.info("Bug report form will open.")
    
    # App information
    st.markdown("---")
    st.markdown("**JarvisFi v2.0.0**")
    st.markdown("*Your AI-Powered Financial Genius*" if current_language == 'en' else 
               "*உங்கள் AI-இயங்கும் நிதி மேதை*" if current_language == 'ta' else 
               "*आपका AI-संचालित वित्तीय प्रतिभा*")
    
    # System status
    st.markdown("**System Status:** 🟢 " + ("Online" if current_language == 'en' else "ஆன்லைன்" if current_language == 'ta' else "ऑनलाइन"))
