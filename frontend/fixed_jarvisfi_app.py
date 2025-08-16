#!/usr/bin/env python3
"""
Fixed JarvisFi Application - Debugging and fixing issues
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FixedJarvisFiApp:
    """Fixed JarvisFi Application with debugging and error handling"""
    
    def __init__(self):
        """Initialize the application"""
        self.logger = logger
        self.setup_page_config()
        self.initialize_session_state()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        try:
            st.set_page_config(
                page_title="JarvisFi - AI Finance Assistant",
                page_icon="🤖",
                layout="wide",
                initial_sidebar_state="expanded"
            )
        except Exception as e:
            self.logger.error(f"Page config setup failed: {e}")
    
    def initialize_session_state(self):
        """Initialize session state with default values"""
        try:
            # Initialize session start time
            if 'session_start_time' not in st.session_state:
                st.session_state.session_start_time = time.time()
            
            # Initialize user profile
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
                    }
                }
            
            # Initialize current page
            if 'current_page' not in st.session_state:
                st.session_state.current_page = 'home'
            
            # Initialize chat history
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # Initialize gamification
            if 'gamification' not in st.session_state:
                st.session_state.gamification = {
                    'points': 0,
                    'level': 1,
                    'badges': [],
                    'challenges_completed': 0,
                    'streak_days': 0
                }
            
            # Initialize data save settings
            if 'data_save_settings' not in st.session_state:
                st.session_state.data_save_settings = {
                    'auto_save': True,
                    'retention_period': 30,
                    'last_save': None,
                    'save_location': 'local',
                    'encryption_enabled': True
                }
            
            self.logger.info("Session state initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Session state initialization failed: {e}")
            st.error(f"Failed to initialize application: {e}")
    
    def render_sidebar(self):
        """Render sidebar navigation"""
        try:
            with st.sidebar:
                st.title("🤖 JarvisFi")
                st.markdown("*Your AI Financial Assistant*")
                
                # User profile section
                profile = st.session_state.user_profile
                st.markdown("---")
                st.markdown("### 👤 User Profile")
                
                # Editable user information
                new_name = st.text_input("Name", value=profile['basic_info']['name'])
                if new_name != profile['basic_info']['name']:
                    st.session_state.user_profile['basic_info']['name'] = new_name
                    st.success("Name updated!")
                    st.rerun()
                
                new_income = st.number_input(
                    "Monthly Income (₹)",
                    min_value=5000,
                    max_value=1000000,
                    value=profile['basic_info']['monthly_income'],
                    step=5000
                )
                if new_income != profile['basic_info']['monthly_income']:
                    st.session_state.user_profile['basic_info']['monthly_income'] = new_income
                    st.success(f"Income updated to ₹{new_income:,}!")
                    st.rerun()
                
                new_expenses = st.number_input(
                    "Monthly Expenses (₹)",
                    min_value=1000,
                    max_value=500000,
                    value=profile['financial_profile']['monthly_expenses'],
                    step=1000
                )
                if new_expenses != profile['financial_profile']['monthly_expenses']:
                    st.session_state.user_profile['financial_profile']['monthly_expenses'] = new_expenses
                    st.success(f"Expenses updated to ₹{new_expenses:,}!")
                    st.rerun()
                
                # Language selection
                languages = {
                    'en': '🇺🇸 English',
                    'ta': '🇮🇳 Tamil (தமிழ்)',
                    'hi': '🇮🇳 Hindi (हिंदी)',
                    'te': '🇮🇳 Telugu (తెలుగు)'
                }
                
                selected_lang = st.selectbox(
                    "Language",
                    options=list(languages.keys()),
                    format_func=lambda x: languages[x],
                    index=list(languages.keys()).index(profile['basic_info']['language'])
                )
                
                if selected_lang != profile['basic_info']['language']:
                    st.session_state.user_profile['basic_info']['language'] = selected_lang
                    st.success("Language updated!")
                    st.rerun()
                
                # User type selection
                user_types = {
                    'student': '🎓 Student',
                    'professional': '💼 Professional',
                    'farmer': '👨‍🌾 Farmer',
                    'senior_citizen': '👴 Senior Citizen'
                }
                
                selected_type = st.selectbox(
                    "User Type",
                    options=list(user_types.keys()),
                    format_func=lambda x: user_types[x],
                    index=list(user_types.keys()).index(profile['basic_info']['user_type'])
                )
                
                if selected_type != profile['basic_info']['user_type']:
                    st.session_state.user_profile['basic_info']['user_type'] = selected_type
                    st.success("User type updated!")
                    st.rerun()
                
                st.markdown("---")
                
                # Navigation menu
                st.markdown("### 📱 Navigation")
                
                pages = {
                    'home': '🏠 Home',
                    'dashboard': '📊 Dashboard',
                    'chat': '💬 AI Chat',
                    'calculators': '🧮 Calculators',
                    'investments': '📈 Investments',
                    'credit': '💳 Credit Score',
                    'farmer': '👨‍🌾 Farmer Tools',
                    'voice': '🎤 Voice Assistant'
                }
                
                for page_key, page_name in pages.items():
                    if st.button(page_name, use_container_width=True, key=f"nav_{page_key}"):
                        st.session_state.current_page = page_key
                        st.rerun()
                
                # Current page indicator
                current_page_name = pages.get(st.session_state.current_page, 'Unknown')
                st.info(f"Current: {current_page_name}")
                
                st.markdown("---")
                
                # Quick stats
                st.markdown("### 📊 Quick Stats")
                monthly_income = profile['basic_info']['monthly_income']
                monthly_expenses = profile['financial_profile']['monthly_expenses']
                savings = monthly_income - monthly_expenses
                savings_rate = (savings / monthly_income * 100) if monthly_income > 0 else 0
                
                st.metric("💰 Monthly Savings", f"₹{savings:,}")
                st.metric("📈 Savings Rate", f"{savings_rate:.1f}%")
                st.metric("💳 Credit Score", profile['financial_profile']['credit_score'])
                
        except Exception as e:
            self.logger.error(f"Sidebar rendering failed: {e}")
            st.sidebar.error(f"Sidebar error: {e}")
    
    def render_home_page(self):
        """Render home page"""
        try:
            profile = st.session_state.user_profile
            current_lang = profile['basic_info']['language']
            user_name = profile['basic_info']['name']
            
            # Welcome message
            welcome_messages = {
                'en': f"Welcome back, {user_name}! 👋",
                'ta': f"மீண்டும் வரவேற்கிறோம், {user_name}! 👋",
                'hi': f"वापसी पर स्वागत है, {user_name}! 👋",
                'te': f"తిరిగి స్వాగతం, {user_name}! 👋"
            }
            
            st.markdown(f"# {welcome_messages.get(current_lang, welcome_messages['en'])}")
            st.markdown("### 🏠 Financial Dashboard Overview")
            
            # Financial overview cards
            monthly_income = profile['basic_info']['monthly_income']
            monthly_expenses = profile['financial_profile']['monthly_expenses']
            savings = monthly_income - monthly_expenses
            credit_score = profile['financial_profile']['credit_score']
            savings_rate = (savings / monthly_income * 100) if monthly_income > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💰 Monthly Income", f"₹{monthly_income:,}", help="Your current monthly income")
            
            with col2:
                st.metric("💸 Monthly Expenses", f"₹{monthly_expenses:,}", help="Your monthly expenses")
            
            with col3:
                delta_color = "normal" if savings > 0 else "inverse"
                st.metric("💰 Monthly Savings", f"₹{savings:,}", f"{savings_rate:.1f}%", delta_color=delta_color)
            
            with col4:
                score_status = "Excellent" if credit_score >= 750 else "Good" if credit_score >= 650 else "Fair"
                st.metric("💳 Credit Score", credit_score, score_status)
            
            # Charts
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                # Savings rate gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = savings_rate,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Savings Rate (%)"},
                    delta = {'reference': 20},
                    gauge = {
                        'axis': {'range': [None, 50]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 10], 'color': "lightgray"},
                            {'range': [10, 20], 'color': "yellow"},
                            {'range': [20, 50], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 20
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Expense breakdown
                expense_data = {
                    'Category': ['Housing', 'Food', 'Transportation', 'Entertainment', 'Others'],
                    'Amount': [monthly_expenses * 0.4, monthly_expenses * 0.2, 
                              monthly_expenses * 0.15, monthly_expenses * 0.1, monthly_expenses * 0.15]
                }
                
                fig = px.pie(expense_data, values='Amount', names='Category', 
                            title='Expense Breakdown')
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            # Quick actions
            st.markdown("---")
            st.markdown("### 🚀 Quick Actions")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("💬 Start AI Chat", use_container_width=True):
                    st.session_state.current_page = 'chat'
                    st.rerun()
            
            with col2:
                if st.button("🧮 Calculators", use_container_width=True):
                    st.session_state.current_page = 'calculators'
                    st.rerun()
            
            with col3:
                if st.button("📈 Investments", use_container_width=True):
                    st.session_state.current_page = 'investments'
                    st.rerun()
            
            with col4:
                if st.button("📊 Full Dashboard", use_container_width=True):
                    st.session_state.current_page = 'dashboard'
                    st.rerun()
            
            # Recommendations
            st.markdown("---")
            st.markdown("### 💡 Personalized Recommendations")
            
            recommendations = self.get_recommendations(profile)
            for rec in recommendations:
                st.info(rec)
            
        except Exception as e:
            self.logger.error(f"Home page rendering failed: {e}")
            st.error(f"Home page error: {e}")
    
    def get_recommendations(self, profile: Dict) -> List[str]:
        """Get personalized recommendations"""
        try:
            user_type = profile['basic_info']['user_type']
            monthly_income = profile['basic_info']['monthly_income']
            monthly_expenses = profile['financial_profile']['monthly_expenses']
            savings = monthly_income - monthly_expenses
            savings_rate = (savings / monthly_income * 100) if monthly_income > 0 else 0
            
            recommendations = []
            
            if user_type == 'student':
                recommendations = [
                    "🎓 Start with small SIPs (₹500-1000) to build investment habit",
                    "📚 Focus on education loans with lower interest rates",
                    "💰 Build emergency fund of ₹10,000-20,000"
                ]
            elif user_type == 'farmer':
                recommendations = [
                    "🌾 Utilize PM-KISAN scheme for ₹6,000 annual benefit",
                    "🚜 Consider crop insurance for risk management",
                    "💰 Invest surplus after harvest in mutual funds"
                ]
            elif user_type == 'professional':
                recommendations = [
                    "💼 Maximize 80C deductions up to ₹1.5 lakh",
                    "📈 Start SIP with 15% of income for wealth building",
                    "🏠 Plan for home loan with EMI <40% of income"
                ]
            else:
                recommendations = [
                    "💰 Build emergency fund of 6 months expenses",
                    "📈 Diversify investments across equity and debt",
                    "💳 Monitor credit score regularly"
                ]
            
            # Add savings rate specific recommendations
            if savings_rate < 10:
                recommendations.append("⚠️ Urgent: Review and reduce unnecessary expenses")
            elif savings_rate > 30:
                recommendations.append("🎉 Excellent savings! Consider increasing investment allocation")
            
            return recommendations[:4]  # Return top 4
            
        except Exception as e:
            self.logger.error(f"Recommendations generation failed: {e}")
            return ["💡 Update your profile for personalized recommendations"]

    def render_dashboard_page(self):
        """Render comprehensive dashboard"""
        try:
            st.markdown("# 📊 Financial Dashboard")

            profile = st.session_state.user_profile
            monthly_income = profile['basic_info']['monthly_income']
            monthly_expenses = profile['financial_profile']['monthly_expenses']
            savings = monthly_income - monthly_expenses

            # Key metrics with real-time updates
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                net_worth = savings * 12 + 100000  # Estimated
                st.metric("💰 Net Worth", f"₹{net_worth:,}", "↗️ +15%")

            with col2:
                investments = monthly_income * 0.15 * 12  # 15% of income
                st.metric("📈 Investments", f"₹{investments:,}", "↗️ +8%")

            with col3:
                st.metric("💳 Credit Score", profile['financial_profile']['credit_score'], "↗️ +25")

            with col4:
                goal_progress = min(65 + (savings / 1000), 100)  # Dynamic progress
                st.metric("🎯 Goal Progress", f"{goal_progress:.0f}%", "↗️ +5%")

            # Charts with real data
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

            # Financial goals with dynamic progress
            st.markdown("### 🎯 Financial Goals Progress")

            goals = [
                {'name': 'Emergency Fund', 'target': monthly_expenses * 6, 'current': savings * 3},
                {'name': 'Retirement Corpus', 'target': monthly_income * 12 * 25, 'current': investments * 2},
                {'name': 'House Down Payment', 'target': 2000000, 'current': savings * 8}
            ]

            for goal in goals:
                progress = min((goal['current'] / goal['target']) * 100, 100)

                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.markdown(f"**{goal['name']}**")
                    st.progress(progress / 100)

                with col2:
                    st.metric("Current", f"₹{goal['current']:,.0f}")

                with col3:
                    st.metric("Target", f"₹{goal['target']:,.0f}")

                if progress >= 80:
                    st.success(f"🎉 {progress:.1f}% complete - Almost there!")
                elif progress >= 50:
                    st.info(f"📈 {progress:.1f}% complete - Good progress!")
                else:
                    st.warning(f"⏳ {progress:.1f}% complete - Keep going!")

                st.markdown("---")

        except Exception as e:
            self.logger.error(f"Dashboard rendering failed: {e}")
            st.error(f"Dashboard error: {e}")

    def render_chat_page(self):
        """Render AI chat page"""
        try:
            st.markdown("# 💬 AI Financial Assistant")

            profile = st.session_state.user_profile
            current_lang = profile['basic_info']['language']

            # Language-specific greetings
            greetings = {
                'en': "Hello! I'm your AI financial assistant. How can I help you today?",
                'ta': "வணக்கம்! நான் உங்கள் AI நிதி உதவியாளர். இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?",
                'hi': "नमस्ते! मैं आपका AI वित्तीय सहायक हूँ। आज मैं आपकी कैसे मदद कर सकता हूँ?",
                'te': "నమస్కారం! నేను మీ AI ఆర్థిక సహాయకుడను. ఈరోజు నేను మీకు ఎలా సహాయం చేయగలను?"
            }

            st.info(greetings.get(current_lang, greetings['en']))

            # Chat history
            for message in st.session_state.chat_history:
                with st.chat_message(message['role']):
                    st.write(message['content'])

            # Chat input
            if prompt := st.chat_input("Ask me anything about finance..."):
                # Add user message
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': prompt,
                    'timestamp': datetime.now().isoformat()
                })

                # Generate AI response (simplified)
                response = self.generate_ai_response(prompt, current_lang)
                st.session_state.chat_history.append(response)

                st.rerun()

            # Quick questions
            st.markdown("### 💡 Quick Questions")
            quick_questions = {
                'en': [
                    "What's my current savings rate?",
                    "How much should I invest monthly?",
                    "Calculate my retirement corpus",
                    "Show me tax-saving options"
                ],
                'ta': [
                    "என் தற்போதைய சேமிப்பு விகிதம் என்ன?",
                    "மாதம் எவ்வளவு முதலீடு செய்ய வேண்டும்?",
                    "என் ஓய்வூதிய நிதியை கணக்கிடுங்கள்",
                    "வரி சேமிப்பு விருப்பங்களைக் காட்டுங்கள்"
                ]
            }

            questions = quick_questions.get(current_lang, quick_questions['en'])

            col1, col2 = st.columns(2)
            for i, question in enumerate(questions):
                with col1 if i % 2 == 0 else col2:
                    if st.button(question, key=f"quick_{i}"):
                        # Add question to chat
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': question,
                            'timestamp': datetime.now().isoformat()
                        })

                        # Generate response
                        response = self.generate_ai_response(question, current_lang)
                        st.session_state.chat_history.append(response)

                        st.rerun()

        except Exception as e:
            self.logger.error(f"Chat page rendering failed: {e}")
            st.error(f"Chat error: {e}")

    def generate_ai_response(self, prompt: str, language: str) -> Dict:
        """Generate AI response (simplified version)"""
        try:
            profile = st.session_state.user_profile
            monthly_income = profile['basic_info']['monthly_income']
            monthly_expenses = profile['financial_profile']['monthly_expenses']
            savings = monthly_income - monthly_expenses
            savings_rate = (savings / monthly_income * 100) if monthly_income > 0 else 0

            # Simple keyword-based responses
            prompt_lower = prompt.lower()

            if 'savings rate' in prompt_lower or 'சேமிப்பு விகிதம்' in prompt_lower:
                if language == 'ta':
                    content = f"உங்கள் தற்போதைய சேமிப்பு விகிதம் {savings_rate:.1f}%. இது {'சிறந்தது' if savings_rate >= 20 else 'நல்லது' if savings_rate >= 10 else 'மேம்படுத்த வேண்டும்'}."
                else:
                    content = f"Your current savings rate is {savings_rate:.1f}%. This is {'excellent' if savings_rate >= 20 else 'good' if savings_rate >= 10 else 'needs improvement'}."

            elif 'invest' in prompt_lower or 'முதலீடு' in prompt_lower:
                recommended_sip = int(monthly_income * 0.15)
                if language == 'ta':
                    content = f"உங்கள் வருமானத்தின் அடிப்படையில், மாதம் ₹{recommended_sip:,} SIP முதலீடு செய்வது நல்லது (வருமானத்தின் 15%)."
                else:
                    content = f"Based on your income, I recommend investing ₹{recommended_sip:,} monthly through SIP (15% of income)."

            elif 'retirement' in prompt_lower or 'ஓய்வூதியம்' in prompt_lower:
                retirement_corpus = monthly_income * 12 * 25
                if language == 'ta':
                    content = f"ஓய்வூதியத்திற்கு தேவையான நிதி தோராயமாக ₹{retirement_corpus:,} (வருடாந்திர செலவின் 25 மடங்கு)."
                else:
                    content = f"For retirement, you'll need approximately ₹{retirement_corpus:,} (25x annual expenses)."

            elif 'tax' in prompt_lower or 'வரி' in prompt_lower:
                if language == 'ta':
                    content = "வரி சேமிப்பு விருப்பங்கள்: ELSS (₹1.5 லட்சம் வரை), PPF, NSC, வீட்டுக் கடன் வட்டி."
                else:
                    content = "Tax-saving options: ELSS (up to ₹1.5 lakh), PPF, NSC, home loan interest deduction."

            else:
                if language == 'ta':
                    content = "நான் உங்களுக்கு நிதி ஆலோசனை வழங்க இங்கே இருக்கிறேன். குறிப்பிட்ட கேள்விகள் கேளுங்கள்!"
                else:
                    content = "I'm here to help with your financial questions. Please ask specific questions about savings, investments, or financial planning!"

            return {
                'role': 'assistant',
                'content': content,
                'timestamp': datetime.now().isoformat(),
                'confidence': 0.85,
                'sources': ['User Profile Analysis'],
                'language': language
            }

        except Exception as e:
            self.logger.error(f"AI response generation failed: {e}")
            return {
                'role': 'assistant',
                'content': "I apologize, but I'm having trouble processing your request. Please try again.",
                'timestamp': datetime.now().isoformat(),
                'confidence': 0.0,
                'sources': ['Error Handler'],
                'language': language
            }

    def render_calculators_page(self):
        """Render financial calculators page"""
        try:
            st.markdown("# 🧮 Financial Calculators")

            # Calculator selection
            calculator_type = st.selectbox(
                "Choose Calculator",
                ["SIP Calculator", "EMI Calculator", "Tax Calculator", "Retirement Calculator"]
            )

            if calculator_type == "SIP Calculator":
                st.markdown("### 📈 SIP Calculator")

                col1, col2 = st.columns(2)

                with col1:
                    monthly_sip = st.number_input("Monthly SIP Amount (₹)", 500, 100000, 5000, 500)
                    annual_return = st.slider("Expected Annual Return (%)", 8.0, 20.0, 12.0, 0.5)
                    investment_period = st.slider("Investment Period (Years)", 1, 30, 10)

                with col2:
                    # Calculate SIP returns
                    monthly_return = annual_return / 12 / 100
                    total_months = investment_period * 12

                    if monthly_return > 0:
                        future_value = monthly_sip * (((1 + monthly_return) ** total_months - 1) / monthly_return) * (1 + monthly_return)
                    else:
                        future_value = monthly_sip * total_months

                    total_invested = monthly_sip * total_months
                    total_returns = future_value - total_invested

                    st.metric("Total Investment", f"₹{total_invested:,.0f}")
                    st.metric("Expected Returns", f"₹{total_returns:,.0f}")
                    st.metric("Maturity Amount", f"₹{future_value:,.0f}")

                # Chart
                years = list(range(1, investment_period + 1))
                invested_amounts = [monthly_sip * 12 * year for year in years]
                maturity_amounts = []

                for year in years:
                    months = year * 12
                    if monthly_return > 0:
                        amount = monthly_sip * (((1 + monthly_return) ** months - 1) / monthly_return) * (1 + monthly_return)
                    else:
                        amount = monthly_sip * months
                    maturity_amounts.append(amount)

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=years, y=invested_amounts, name='Total Invested', fill='tonexty'))
                fig.add_trace(go.Scatter(x=years, y=maturity_amounts, name='Maturity Value', fill='tonexty'))
                fig.update_layout(title='SIP Growth Over Time', xaxis_title='Years', yaxis_title='Amount (₹)')
                st.plotly_chart(fig, use_container_width=True)

            elif calculator_type == "EMI Calculator":
                st.markdown("### 🏠 EMI Calculator")

                col1, col2 = st.columns(2)

                with col1:
                    loan_amount = st.number_input("Loan Amount (₹)", 100000, 50000000, 2500000, 100000)
                    interest_rate = st.slider("Annual Interest Rate (%)", 6.0, 20.0, 8.5, 0.1)
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

                # EMI breakdown chart
                fig = go.Figure(data=[
                    go.Bar(name='Principal', x=['Loan Breakdown'], y=[loan_amount]),
                    go.Bar(name='Interest', x=['Loan Breakdown'], y=[total_interest])
                ])
                fig.update_layout(barmode='stack', title='Loan Breakdown')
                st.plotly_chart(fig, use_container_width=True)

            # Add more calculators as needed

        except Exception as e:
            self.logger.error(f"Calculators page rendering failed: {e}")
            st.error(f"Calculators error: {e}")

    def render_investments_page(self):
        """Render investments page with real-time updates"""
        try:
            st.markdown("# 📈 Investment Portfolio")

            profile = st.session_state.user_profile
            monthly_income = profile['basic_info']['monthly_income']

            # Portfolio overview with dynamic values
            col1, col2, col3, col4 = st.columns(4)

            # Calculate dynamic values based on income
            total_portfolio = monthly_income * 0.15 * 12 * 3  # 3 years of 15% investment
            monthly_sip = monthly_income * 0.15
            annual_returns = 14.5
            goal_progress = min(68 + (monthly_income / 10000), 100)

            with col1:
                st.metric("Total Portfolio", f"₹{total_portfolio:,.0f}", "↗️ +12%")
            with col2:
                st.metric("Monthly SIP", f"₹{monthly_sip:,.0f}", f"↗️ +₹{monthly_sip*0.1:,.0f}")
            with col3:
                st.metric("Returns (1Y)", f"{annual_returns}%", "↗️ +2.1%")
            with col4:
                st.metric("Goal Progress", f"{goal_progress:.0f}%", "↗️ +5%")

            # Asset allocation
            st.markdown("#### 🎯 Asset Allocation")

            col1, col2 = st.columns(2)

            with col1:
                # Current allocation
                allocation_data = {
                    'Asset Class': ['Large Cap Equity', 'Mid Cap Equity', 'Small Cap Equity', 'Debt Funds', 'Gold ETF'],
                    'Allocation': [40, 25, 15, 15, 5],
                    'Amount': [total_portfolio * 0.4, total_portfolio * 0.25,
                              total_portfolio * 0.15, total_portfolio * 0.15, total_portfolio * 0.05]
                }

                fig = px.pie(allocation_data, values='Allocation', names='Asset Class',
                            title='Current Allocation')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Recommended allocation based on age
                user_age = profile['basic_info']['age']
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

            recommended_sip = int(monthly_income * 0.15)

            recommendations = [
                f"💰 Current SIP: ₹{monthly_sip:,.0f} (15% of income) - Good allocation!",
                f"📈 Consider adding international equity exposure for diversification",
                f"🏦 Rebalance portfolio quarterly to maintain target allocation",
                f"💎 Current gold allocation: 5% - Consider increasing to 10% for stability"
            ]

            for rec in recommendations:
                st.info(rec)

            # SIP performance tracker
            st.markdown("#### 📊 SIP Performance Tracker")

            # Simulated SIP performance with real values
            months = list(range(1, 13))
            invested = [monthly_sip * i for i in months]
            current_value = [monthly_sip * i * (1 + 0.12/12)**i for i in months]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=invested, name='Amount Invested', fill='tonexty'))
            fig.add_trace(go.Scatter(x=months, y=current_value, name='Current Value', fill='tonexty'))
            fig.update_layout(title='SIP Performance (Last 12 Months)', xaxis_title='Months', yaxis_title='Amount (₹)')
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            self.logger.error(f"Investments page rendering failed: {e}")
            st.error(f"Investments error: {e}")

    def render_credit_page(self):
        """Render credit score page"""
        try:
            st.markdown("# 💳 Credit Score Tracking")

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

        except Exception as e:
            self.logger.error(f"Credit page rendering failed: {e}")
            st.error(f"Credit error: {e}")

    def render_farmer_page(self):
        """Render farmer tools page"""
        try:
            st.markdown("# 👨‍🌾 Farmer Financial Tools")

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

        except Exception as e:
            self.logger.error(f"Farmer page rendering failed: {e}")
            st.error(f"Farmer error: {e}")

    def render_voice_page(self):
        """Render voice interface page"""
        try:
            st.markdown("# 🎤 Voice Assistant")

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

        except Exception as e:
            self.logger.error(f"Voice page rendering failed: {e}")
            st.error(f"Voice error: {e}")

    def run(self):
        """Main application runner"""
        try:
            # Render sidebar
            self.render_sidebar()

            # Render main content based on current page
            current_page = st.session_state.current_page

            if current_page == 'home':
                self.render_home_page()
            elif current_page == 'dashboard':
                self.render_dashboard_page()
            elif current_page == 'chat':
                self.render_chat_page()
            elif current_page == 'calculators':
                self.render_calculators_page()
            elif current_page == 'investments':
                self.render_investments_page()
            elif current_page == 'credit':
                self.render_credit_page()
            elif current_page == 'farmer':
                self.render_farmer_page()
            elif current_page == 'voice':
                self.render_voice_page()
            else:
                st.error(f"Unknown page: {current_page}")
                self.render_home_page()

        except Exception as e:
            self.logger.error(f"Application run failed: {e}")
            st.error(f"Application error: {e}")
            st.markdown("### 🔧 Debug Information")
            st.code(f"Error: {e}")
            st.code(f"Current page: {st.session_state.get('current_page', 'Unknown')}")


def main():
    """Main function to run the fixed JarvisFi application"""
    try:
        app = FixedJarvisFiApp()
        app.run()
    except Exception as e:
        st.error(f"Application startup failed: {e}")
        st.info("Please refresh the page to restart the application.")


if __name__ == "__main__":
    main()
