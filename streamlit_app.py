"""
JarvisFi - Multilingual AI Personal Finance Chatbot
Main entry point for Streamlit Cloud deployment
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))
sys.path.insert(0, str(project_root / "frontend"))

# Set page config first
st.set_page_config(
    page_title="JarvisFi - AI Financial Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/ANASF1412/GenAI-JarvisFi-app',
        'Report a bug': 'https://github.com/ANASF1412/GenAI-JarvisFi-app/issues',
        'About': """
        # JarvisFi - AI Financial Assistant
        
        Your multilingual AI-powered financial genius supporting:
        - 🌍 4 Languages (EN, TA, HI, TE)
        - 🎤 Voice Interface
        - 👨‍🌾 Farmer Tools
        - 💳 Credit Score Tracking
        - 📈 Investment Management
        - 🧮 15+ Financial Calculators
        
        Built with ❤️ for financial inclusion
        """
    }
)

# Import and run the main application
try:
    # Try to import the complete application first
    from frontend.complete_jarvisfi_app import CompleteJarvisFiApp
    
    # Initialize and run the app
    if __name__ == "__main__":
        app = CompleteJarvisFiApp()
        app.run()
        
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.info("Falling back to basic application...")
    
    try:
        # Fallback to comprehensive app
        from frontend.comprehensive_app import ComprehensiveJarvisFiApp
        
        if __name__ == "__main__":
            app = ComprehensiveJarvisFiApp()
            app.run()
            
    except ImportError as e2:
        st.error(f"Fallback Import Error: {e2}")
        st.info("Loading basic demo version...")
        
        # Basic demo version
        st.title("🤖 JarvisFi - AI Financial Assistant")
        st.markdown("### Welcome to JarvisFi!")
        
        st.markdown("""
        **JarvisFi** is your multilingual AI-powered financial genius that helps with:
        
        - 🌍 **Multilingual Support**: English, Tamil, Hindi, Telugu
        - 🎤 **Voice Interface**: Speech-to-text and text-to-speech
        - 👨‍🌾 **Farmer Tools**: Crop loans, MSP tracking, government schemes
        - 💳 **Credit Score**: Tracking and improvement tips
        - 📈 **Investments**: Portfolio management and recommendations
        - 🧮 **Calculators**: SIP, EMI, Tax, Retirement planning
        
        ---
        
        **Note**: This is a demo version. The full application requires additional dependencies.
        
        For the complete experience, please visit our [GitHub repository](https://github.com/ANASF1412/GenAI-JarvisFi-app).
        """)
        
        # Basic calculator demo
        st.markdown("### 🧮 Quick SIP Calculator Demo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_investment = st.number_input("Monthly Investment (₹)", 500, 100000, 5000, 500)
            annual_return = st.number_input("Expected Annual Return (%)", 1.0, 30.0, 12.0, 0.5)
            investment_period = st.number_input("Investment Period (Years)", 1, 50, 10, 1)
        
        with col2:
            # Calculate SIP returns
            monthly_rate = annual_return / (12 * 100)
            total_months = investment_period * 12
            
            if monthly_rate > 0:
                future_value = monthly_investment * (((1 + monthly_rate) ** total_months - 1) / monthly_rate) * (1 + monthly_rate)
            else:
                future_value = monthly_investment * total_months
            
            total_invested = monthly_investment * total_months
            total_returns = future_value - total_invested
            
            st.metric("Total Investment", f"₹{total_invested:,.0f}")
            st.metric("Future Value", f"₹{future_value:,.0f}")
            st.metric("Total Returns", f"₹{total_returns:,.0f}")
        
        # Language selector demo
        st.markdown("### 🌍 Language Support Demo")
        
        language = st.selectbox("Select Language", 
                               ["English", "Tamil (தமிழ்)", "Hindi (हिंदी)", "Telugu (తెలుగు)"])
        
        greetings = {
            "English": "Welcome to JarvisFi! How can I help you with your finances today?",
            "Tamil (தமிழ்)": "JarvisFi-க்கு வரவேற்கிறோம்! இன்று உங்கள் நிதி விஷயங்களில் நான் எப்படி உதவ முடியும்?",
            "Hindi (हिंदी)": "JarvisFi में आपका स्वागत है! आज मैं आपकी वित्तीय मामलों में कैसे मदद कर सकता हूँ?",
            "Telugu (తెలుగు)": "JarvisFi కి స్వాగతం! ఈరోజు మీ ఆర్థిక విషయాలలో నేను ఎలా సహాయం చేయగలను?"
        }
        
        st.info(greetings[language])
        
        st.markdown("---")
        st.markdown("**🚀 For the full JarvisFi experience with all features, please run the complete application locally or check our GitHub repository.**")

except Exception as e:
    st.error(f"Application Error: {e}")
    st.markdown("### 🔧 Troubleshooting")
    st.markdown("""
    If you're seeing this error, it might be due to:
    1. Missing dependencies
    2. Configuration issues
    3. File path problems
    
    Please check the [GitHub repository](https://github.com/ANASF1412/GenAI-JarvisFi-app) for setup instructions.
    """)
