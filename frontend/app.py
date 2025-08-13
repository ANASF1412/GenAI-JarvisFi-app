import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime, timedelta
import sys
import logging

# Add backend modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import backend modules
try:
    from backend.watson_integration import WatsonIntegration
    from backend.budget_analyzer import BudgetAnalyzer
    from backend.demographic_adapter import DemographicAdapter
    from backend.nlp_processor import NLPProcessor
    from backend.currency_converter import CurrencyConverter
    from backend.pdf_generator import FinancialReportGenerator
    from backend.smart_alerts import SmartAlertSystem
    from backend.language_support import LanguageSupport
    from backend.user_profile_manager import UserProfileManager
    from frontend.enhanced_ui import EnhancedUI
except ImportError as e:
    st.error(f"Error importing backend modules: {e}")
    st.error("Please ensure all backend modules are properly installed and .env file is configured")
    st.stop()

# Enhanced imports for new features
from typing import Dict, List
import base64
from io import BytesIO
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonalFinanceChatbot:
    def __init__(self):
        # Setup logger first
        self.logger = logging.getLogger(__name__)

        self.watson = WatsonIntegration()
        self.budget_analyzer = BudgetAnalyzer()
        self.demographic_adapter = DemographicAdapter()
        self.nlp_processor = NLPProcessor()

        # Initialize new innovative features
        self.currency_converter = CurrencyConverter()
        self.pdf_generator = FinancialReportGenerator()
        self.alert_system = SmartAlertSystem()

        # Initialize enhanced features
        self.language_support = LanguageSupport()
        self.user_profile_manager = UserProfileManager()
        self.enhanced_ui = EnhancedUI()

        # Initialize new comprehensive features
        try:
            from backend.mongodb_integration import SecureMongoDBManager
            from backend.security_manager import SecurityManager
            from backend.voice_interface import VoiceInterface
            from backend.ai_accuracy_rag import AIAccuracyRAG
            from backend.currency_localization import CurrencyLocalizationManager

            self.mongodb_manager = SecureMongoDBManager()
            self.security_manager = SecurityManager()
            self.voice_interface = VoiceInterface()
            self.ai_rag = AIAccuracyRAG()
            self.currency_manager = CurrencyLocalizationManager()

            self.logger.info("All comprehensive features initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize comprehensive features: {e}")
            # Initialize fallback None values
            self.mongodb_manager = None
            self.security_manager = None
            self.voice_interface = None
            self.ai_rag = None
            self.currency_manager = None

        # Initialize session state
        self.init_session_state()

        # Load user data
        self.load_user_data()
    
    def init_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'user_profile' not in st.session_state:
            # Initialize with default profile
            st.session_state.user_profile = self.user_profile_manager.create_user_profile({
                'name': '',
                'age': 25,
                'user_type': 'beginner',
                'language': 'english',
                'monthly_income': 30000
            })
            # Ensure language is properly set
            self.language_support.set_language('english')

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        if 'watson_session_id' not in st.session_state:
            st.session_state.watson_session_id = None

        if 'transactions_df' not in st.session_state:
            st.session_state.transactions_df = pd.DataFrame()

        if 'budget_analysis' not in st.session_state:
            st.session_state.budget_analysis = {}

        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Chat'

        if 'alerts' not in st.session_state:
            st.session_state.alerts = []

        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False

        if 'notifications_enabled' not in st.session_state:
            st.session_state.notifications_enabled = True

        if 'current_language' not in st.session_state:
            st.session_state.current_language = 'english'

        if 'onboarding_completed' not in st.session_state:
            st.session_state.onboarding_completed = False
    
    def load_user_data(self):
        """Load user profile and transaction data"""
        try:
            # Load user profiles
            if os.path.exists('data/user_profiles.json'):
                with open('data/user_profiles.json', 'r') as f:
                    user_profiles = json.load(f)
                    # For demo, use first profile or default
                    if user_profiles:
                        st.session_state.user_profile = list(user_profiles.values())[0]
            
            # Load transactions
            if os.path.exists('data/transactions.csv'):
                st.session_state.transactions_df = pd.read_csv('data/transactions.csv')
                st.session_state.transactions_df['date'] = pd.to_datetime(st.session_state.transactions_df['date'])
        
        except Exception as e:
            logger.error(f"Error loading user data: {e}")
    
    def setup_sidebar(self):
        """Setup sidebar with user profile and navigation"""
        st.sidebar.title("🏦 Personal Finance AI")
        
        # User Profile Section
        st.sidebar.subheader("👤 Your Profile")
        
        # Demographic selection
        demographic = st.sidebar.selectbox(
            "I am a:",
            ["student", "professional", "entrepreneur", "retired"],
            index=0 if st.session_state.user_profile.get('demographic') == 'student' else 1,
            key="demographic_select"
        )
        
        # Update profile
        st.session_state.user_profile['demographic'] = demographic
        
        # Basic info
        name = st.sidebar.text_input(
            "Name:", 
            value=st.session_state.user_profile.get('name', ''),
            key="name_input"
        )
        st.session_state.user_profile['name'] = name
        
        age = st.sidebar.number_input(
            "Age:", 
            min_value=18, 
            max_value=100, 
            value=st.session_state.user_profile.get('age', 25),
            key="age_input"
        )
        st.session_state.user_profile['age'] = age
        
        monthly_income = st.sidebar.number_input(
            "Monthly Income (₹):", 
            min_value=0, 
            value=st.session_state.user_profile.get('monthly_income', 30000),
            key="income_input"
        )
        st.session_state.user_profile['monthly_income'] = monthly_income
        
        # Navigation
        st.sidebar.subheader("🧭 Navigation")
        page = st.sidebar.radio(
            "Go to:",
            ["Chat", "Budget Analysis", "Smart Alerts", "Currency Converter", "Data Upload", "PDF Reports", "Insights Dashboard"],
            index=["Chat", "Budget Analysis", "Smart Alerts", "Currency Converter", "Data Upload", "PDF Reports", "Insights Dashboard"].index(st.session_state.current_page) if st.session_state.current_page in ["Chat", "Budget Analysis", "Smart Alerts", "Currency Converter", "Data Upload", "PDF Reports", "Insights Dashboard"] else 0
        )
        st.session_state.current_page = page
        
        # Settings Section
        st.sidebar.subheader("⚙️ Settings")
        
        # Dark Mode Toggle (placeholder - functionality to be implemented)
        dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
        st.session_state.dark_mode = dark_mode
        
        # Notifications Toggle
        notifications = st.sidebar.checkbox("🔔 Smart Alerts", value=st.session_state.notifications_enabled)
        st.session_state.notifications_enabled = notifications
        
        # Quick Actions
        st.sidebar.subheader("⚡ Quick Actions")
        if st.sidebar.button("📊 Analyze My Budget"):
            self.analyze_budget()
        
        if st.sidebar.button("💡 Get Smart Alerts"):
            self.generate_smart_alerts()
        
        if st.sidebar.button("📄 Generate PDF Report"):
            self.generate_pdf_report()
        
        if st.sidebar.button("💱 Quick Currency Convert"):
            st.session_state.current_page = "Currency Converter"
            st.rerun()
        
        if st.sidebar.button("🔄 Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Real-time Currency Display
        st.sidebar.subheader("💱 Live Rates")
        try:
            usd_to_inr = self.currency_converter.get_exchange_rate('USD', 'INR')
            st.sidebar.metric("USD to INR", f"₹{usd_to_inr:.2f}", delta=None)
        except Exception:
            st.sidebar.info("Currency rates unavailable")
    
    def show_chat_interface(self):
        """Main chat interface"""
        st.title("💬 Your Personal Finance Assistant")
        
        # Enhanced UI with loading animation
        if st.session_state.user_profile.get('name'):
            greeting = self.demographic_adapter.get_personalized_greeting(st.session_state.user_profile)
            st.info(greeting)
        
        # Show alerts banner if alerts exist
        if st.session_state.alerts and st.session_state.notifications_enabled:
            critical_alerts = [a for a in st.session_state.alerts if a.get('type') == 'critical']
            warning_alerts = [a for a in st.session_state.alerts if a.get('type') == 'warning']
            
            if critical_alerts:
                st.error(f"🚨 You have {len(critical_alerts)} critical financial alert(s)! Check the Smart Alerts page.")
            elif warning_alerts:
                st.warning(f"⚠️ You have {len(warning_alerts)} financial warning(s). Check Smart Alerts for details.")
        
        # Show suggested topics
        if not st.session_state.chat_history:
            st.subheader("🎯 Suggested Topics")
            demographic = st.session_state.user_profile.get('demographic', 'professional')
            suggestions = self.demographic_adapter.suggest_relevant_topics(demographic)
            
            cols = st.columns(len(suggestions))
            for i, suggestion in enumerate(suggestions):
                with cols[i % len(cols)]:
                    if st.button(suggestion, key=f"suggestion_{i}"):
                        self.process_user_message(suggestion)
        
        # Chat history
        for i, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                st.chat_message("user").write(message['content'])
            else:
                st.chat_message("assistant").write(message['content'])
        
        # Chat input
        user_input = st.chat_input("Ask me anything about personal finance...")
        
        if user_input:
            self.process_user_message(user_input)
    
    def process_user_message(self, user_input: str):
        """Process user message and generate response"""
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Process with NLP
        query_analysis = self.nlp_processor.process_query(
            user_input, 
            st.session_state.user_profile
        )
        
        # Generate response
        response = self.generate_response(user_input, query_analysis)
        
        # Add bot response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now()
        })
        
        st.rerun()
    
    def generate_response(self, user_input: str, query_analysis: Dict) -> str:
        """Generate appropriate response based on query analysis"""
        try:
            intent = query_analysis.get('intent', {}).get('primary', 'general_query')
            demographic = st.session_state.user_profile.get('demographic', 'professional')
            
            # Check if query requires data analysis
            if query_analysis.get('requires_data', {}).get('requires_data'):
                if not st.session_state.transactions_df.empty:
                    return self.generate_data_driven_response(user_input, query_analysis)
                else:
                    return self.generate_no_data_response(intent, demographic)
            
            # Generate contextual response using Watson or demographic adapter
            if intent in ['budget_management', 'savings_advice', 'investment_guidance', 'tax_advice']:
                response = self.demographic_adapter.adapt_response(
                    "", demographic, intent
                )
            else:
                response = self.generate_general_response(user_input, query_analysis)
            
            # Add follow-up questions
            followups = query_analysis.get('suggested_followups', [])
            if followups:
                response += f"\n\n🤔 **You might also want to know:**\n"
                for i, followup in enumerate(followups[:2]):
                    response += f"{i+1}. {followup}\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an issue processing your request. Could you please try rephrasing your question?"
    
    def generate_data_driven_response(self, user_input: str, query_analysis: Dict) -> str:
        """Generate response using user's transaction data"""
        if st.session_state.transactions_df.empty:
            return "I'd love to analyze your data, but I don't see any transaction records. Please upload your data in the 'Data Upload' section!"
        
        # Perform budget analysis
        analysis = self.budget_analyzer.analyze_transactions(
            st.session_state.transactions_df,
            st.session_state.user_profile
        )
        
        # Generate report
        report = self.budget_analyzer.generate_budget_summary_report(
            analysis,
            st.session_state.user_profile
        )
        
        # Extract specific insights based on query
        query_params = self.nlp_processor.extract_transaction_query_params(user_input)
        
        specific_insights = self.extract_specific_insights(analysis, query_params)
        
        return f"{report}\n\n{specific_insights}"
    
    def generate_no_data_response(self, intent: str, demographic: str) -> str:
        """Generate response when data is required but not available"""
        response = "I'd love to give you personalized insights based on your financial data! "
        
        if demographic == 'student':
            response += "Even basic expense tracking can help you save more money for the things you want! 💰"
        else:
            response += "Data-driven financial planning leads to much better outcomes. 📊"
        
        response += "\n\nTo get started:\n"
        response += "1. 📤 Upload your transaction data in the 'Data Upload' section\n"
        response += "2. 📊 I'll analyze your spending patterns\n"
        response += "3. 💡 Get personalized recommendations based on your data\n\n"
        response += "In the meantime, I can provide general advice about " + intent.replace('_', ' ') + "!"
        
        return response
    
    def generate_general_response(self, user_input: str, query_analysis: Dict) -> str:
        """Generate general financial advice response"""
        intent = query_analysis.get('intent', {}).get('primary', 'general_query')
        demographic = st.session_state.user_profile.get('demographic', 'professional')
        
        # Use demographic adapter for general responses
        if intent == 'budget_management':
            base_response = "Let me help you with budget management strategies."
        elif intent == 'savings_advice':
            base_response = "Here's how you can improve your savings."
        elif intent == 'investment_guidance':
            base_response = "Let's explore investment options suitable for you."
        elif intent == 'tax_advice':
            base_response = "Here's some tax planning guidance."
        else:
            base_response = "I'm here to help with your financial questions."
        
        # Adapt response based on demographic
        adapted_response = self.demographic_adapter.adapt_response(
            base_response, demographic, intent
        )
        
        return adapted_response
    
    def extract_specific_insights(self, analysis: Dict, query_params: Dict) -> str:
        """Extract specific insights based on query parameters"""
        insights = []
        
        if query_params.get('time_range'):
            time_range = query_params['time_range']
            insights.append(f"📅 **{time_range.replace('_', ' ').title()} Analysis:**")
        
        if query_params.get('categories'):
            categories = query_params['categories']
            category_data = analysis.get('category_breakdown', {}).get('by_category', {})
            
            for category in categories:
                if category in category_data:
                    amount = category_data[category]
                    insights.append(f"• {category.title()}: ₹{amount:,.2f}")
        
        if query_params.get('analysis_type') == 'trends':
            trends = analysis.get('trends', {})
            trend_direction = trends.get('trend_direction', 'stable')
            trend_percentage = trends.get('trend_percentage', 0)
            
            insights.append(f"📈 **Spending Trend:** {trend_direction.title()} ({trend_percentage:+.1f}%)")
        
        return '\n'.join(insights) if insights else ""
    
    def show_budget_analysis(self):
        """Show comprehensive budget analysis page"""
        st.title("📊 Budget Analysis Dashboard")
        
        if st.session_state.transactions_df.empty:
            st.warning("⚠️ No transaction data found. Please upload your data to see analysis.")
            if st.button("📤 Go to Data Upload"):
                st.session_state.current_page = 'Data Upload'
                st.rerun()
            return
        
        # Analyze data
        if not st.session_state.budget_analysis:
            with st.spinner("Analyzing your financial data..."):
                st.session_state.budget_analysis = self.budget_analyzer.analyze_transactions(
                    st.session_state.transactions_df,
                    st.session_state.user_profile
                )
        
        analysis = st.session_state.budget_analysis
        
        # Overview metrics
        st.subheader("💰 Financial Overview")
        summary = analysis.get('summary', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Spent", 
                f"₹{summary.get('total_spent', 0):,.0f}",
                delta=None
            )
        
        with col2:
            st.metric(
                "Total Income", 
                f"₹{summary.get('total_income', 0):,.0f}",
                delta=None
            )
        
        with col3:
            st.metric(
                "Net Savings", 
                f"₹{summary.get('net_savings', 0):,.0f}",
                delta=None
            )
        
        with col4:
            savings_rate = summary.get('savings_rate', 0)
            st.metric(
                "Savings Rate", 
                f"{savings_rate:.1f}%",
                delta=f"{savings_rate - 20:.1f}%" if savings_rate != 20 else None
            )
        
        # Budget Health Score
        st.subheader("🏥 Budget Health")
        health = analysis.get('budget_health', {})
        score = health.get('score', 0)
        status = health.get('status', 'No Data')
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text': "Health Score"},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': health.get('color', 'gray')},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgray"},
                        {'range': [40, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"### Status: {status}")
            
            breakdown = health.get('breakdown', {})
            st.write(f"**Savings Health:** {breakdown.get('savings_health', 0):.1f}%")
            st.write(f"**Spending Trend:** {breakdown.get('spending_trend', 'Unknown').title()}")
            st.write(f"**Category Balance:** {breakdown.get('category_balance', 0):.1f}% essentials")
        
        # Spending breakdown
        st.subheader("📈 Spending Breakdown")
        
        category_data = analysis.get('category_breakdown', {})
        if category_data.get('by_category'):
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                categories = list(category_data['by_category'].keys())
                values = list(category_data['by_category'].values())
                
                fig = px.pie(
                    values=values,
                    names=categories,
                    title="Spending by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Bar chart
                df_categories = pd.DataFrame({
                    'Category': categories,
                    'Amount': values
                }).sort_values('Amount', ascending=True)
                
                fig = px.bar(
                    df_categories,
                    x='Amount',
                    y='Category',
                    orientation='h',
                    title="Category Spending"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Trends analysis
        st.subheader("📊 Spending Trends")
        trends = analysis.get('trends', {})
        monthly_spending = trends.get('monthly_spending', {})
        
        if monthly_spending:
            df_trends = pd.DataFrame([
                {'Month': str(month), 'Amount': amount} 
                for month, amount in monthly_spending.items()
            ])
            
            fig = px.line(
                df_trends,
                x='Month',
                y='Amount',
                title='Monthly Spending Trend',
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            trend_direction = trends.get('trend_direction', 'stable')
            trend_percentage = trends.get('trend_percentage', 0)
            
            if trend_direction == 'increasing':
                st.warning(f"⚠️ Your spending is increasing by {trend_percentage:.1f}%")
            elif trend_direction == 'decreasing':
                st.success(f"✅ Great! Your spending is decreasing by {abs(trend_percentage):.1f}%")
            else:
                st.info("📊 Your spending is relatively stable")
    
    def show_data_upload(self):
        """Show data upload interface"""
        st.title("📤 Data Upload Center")
        
        st.markdown("""
        Upload your financial data to get personalized insights and recommendations.
        We support CSV files with transaction data.
        """)
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a CSV file with your transactions",
            type=['csv'],
            help="CSV should contain columns: date, description, amount, category"
        )
        
        if uploaded_file is not None:
            try:
                # Read uploaded file
                df = pd.read_csv(uploaded_file)
                
                st.success("✅ File uploaded successfully!")
                
                # Show preview
                st.subheader("📋 Data Preview")
                st.dataframe(df.head(10))
                
                # Data validation
                required_columns = ['date', 'amount']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"❌ Missing required columns: {missing_columns}")
                    st.info("Please ensure your CSV has columns: date, amount, description (optional), category (optional)")
                else:
                    # Process and validate data
                    if st.button("💾 Process and Save Data"):
                        with st.spinner("Processing your data..."):
                            processed_df = self.process_transaction_data(df)
                            st.session_state.transactions_df = processed_df
                            
                            # Clear existing analysis to trigger re-analysis
                            st.session_state.budget_analysis = {}
                            
                            st.success("✅ Data processed and saved successfully!")
                            st.balloons()
                            
                            # Show basic statistics
                            st.subheader("📊 Quick Statistics")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Total Transactions", len(processed_df))
                            
                            with col2:
                                total_spent = abs(processed_df[processed_df['amount'] < 0]['amount'].sum())
                                st.metric("Total Spent", f"₹{total_spent:,.2f}")
                            
                            with col3:
                                date_range = (processed_df['date'].max() - processed_df['date'].min()).days
                                st.metric("Date Range", f"{date_range} days")
            
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
        
        # Sample data section
        st.subheader("📝 Sample Data Format")
        
        sample_data = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'description': ['Groceries', 'Salary Credit', 'Coffee'],
            'amount': [-2500, 50000, -150],
            'category': ['groceries', 'income', 'dining']
        })
        
        st.dataframe(sample_data)
        
        # Download sample template
        csv_sample = sample_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Sample Template",
            data=csv_sample,
            file_name="transaction_template.csv",
            mime="text/csv"
        )
        
        # Manual data entry option
        st.subheader("✍️ Manual Data Entry")
        
        with st.expander("Add Individual Transactions"):
            col1, col2 = st.columns(2)
            
            with col1:
                date = st.date_input("Date")
                description = st.text_input("Description")
            
            with col2:
                amount = st.number_input("Amount (negative for expenses)", value=0.0)
                category = st.selectbox(
                    "Category",
                    ["groceries", "dining", "transportation", "entertainment", "utilities", "healthcare", "shopping", "income", "other"]
                )
            
            if st.button("➕ Add Transaction"):
                new_transaction = pd.DataFrame({
                    'date': [date],
                    'description': [description],
                    'amount': [amount],
                    'category': [category]
                })
                
                if st.session_state.transactions_df.empty:
                    st.session_state.transactions_df = new_transaction
                else:
                    st.session_state.transactions_df = pd.concat([
                        st.session_state.transactions_df, 
                        new_transaction
                    ], ignore_index=True)
                
                st.success("✅ Transaction added!")
                st.rerun()
    
    def process_transaction_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process and clean transaction data"""
        processed_df = df.copy()
        
        # Convert date column
        processed_df['date'] = pd.to_datetime(processed_df['date'])
        
        # Ensure amount is numeric
        processed_df['amount'] = pd.to_numeric(processed_df['amount'], errors='coerce')
        
        # Add default category if not present
        if 'category' not in processed_df.columns:
            processed_df['category'] = 'other'
        
        # Add default description if not present
        if 'description' not in processed_df.columns:
            processed_df['description'] = 'Transaction'
        
        # Remove rows with invalid data
        processed_df = processed_df.dropna(subset=['date', 'amount'])
        
        # Sort by date
        processed_df = processed_df.sort_values('date')
        
        return processed_df
    
    def show_insights_dashboard(self):
        """Show comprehensive insights dashboard"""
        st.title("🔍 Financial Insights Dashboard")
        
        if st.session_state.transactions_df.empty:
            st.warning("⚠️ No data available. Please upload your transaction data first.")
            return
        
        # Ensure we have analysis
        if not st.session_state.budget_analysis:
            with st.spinner("Generating insights..."):
                st.session_state.budget_analysis = self.budget_analyzer.analyze_transactions(
                    st.session_state.transactions_df,
                    st.session_state.user_profile
                )
        
        analysis = st.session_state.budget_analysis
        
        # Key insights
        st.subheader("💡 Key Insights")
        
        insights = analysis.get('insights', [])
        for i, insight in enumerate(insights):
            st.info(f"💡 **Insight {i+1}:** {insight}")
        
        # Recommendations
        st.subheader("🎯 Personalized Recommendations")
        
        recommendations = analysis.get('recommendations', [])
        for i, rec in enumerate(recommendations):
            st.success(f"✅ **Recommendation {i+1}:** {rec}")
        
        # Advanced analytics
        st.subheader("📈 Advanced Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Spending Patterns")
            
            # Weekend vs weekday analysis
            df = st.session_state.transactions_df
            expenses = df[df['amount'] < 0].copy()
            expenses['amount'] = abs(expenses['amount'])
            expenses['day_of_week'] = expenses['date'].dt.day_name()
            
            weekend_spending = expenses[expenses['day_of_week'].isin(['Saturday', 'Sunday'])]['amount'].mean()
            weekday_spending = expenses[~expenses['day_of_week'].isin(['Saturday', 'Sunday'])]['amount'].mean()
            
            pattern_data = pd.DataFrame({
                'Period': ['Weekdays', 'Weekends'],
                'Average Spending': [weekday_spending, weekend_spending]
            })
            
            fig = px.bar(
                pattern_data,
                x='Period',
                y='Average Spending',
                title='Weekday vs Weekend Spending'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Goal Tracking")
            
            # Savings goal tracking
            monthly_income = st.session_state.user_profile.get('monthly_income', 0)
            actual_savings = analysis.get('summary', {}).get('net_savings', 0)
            target_savings = monthly_income * 0.2  # 20% target
            
            if target_savings > 0:
                progress = min((actual_savings / target_savings) * 100, 100)
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = progress,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Savings Goal Progress (%)"},
                    delta = {'reference': 100},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "lightgreen"}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90}}))
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Set your monthly income to track savings goals!")
        
        # Demographic-specific insights
        st.subheader("🎭 Personalized for You")
        
        demographic = st.session_state.user_profile.get('demographic', 'professional')
        customized_metrics = self.demographic_adapter.customize_financial_metrics(
            analysis.get('summary', {}), 
            demographic
        )
        
        if demographic == 'student':
            st.markdown("### 🎓 Student Financial Health")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                daily_spending = customized_metrics.get('daily_spending', 0)
                st.metric("Daily Spending", f"₹{daily_spending:.0f}")
                if daily_spending > 300:
                    st.caption("💡 Try to keep daily spending under ₹300")
            
            with col2:
                monthly_budget = customized_metrics.get('monthly_budget', 0)
                st.metric("Monthly Budget", f"₹{monthly_budget:.0f}")
            
            with col3:
                savings_amount = customized_metrics.get('savings_amount', 0)
                st.metric("Monthly Savings", f"₹{savings_amount:.0f}")
                if savings_amount < 1000:
                    st.caption("💡 Try to save at least ₹1000/month")
        
        else:  # Professional view
            st.markdown("### 💼 Professional Financial Dashboard")
            
            col1, col2, col3, col4 = st.columns(4)
            
            metrics = [
                ("Monthly Income", f"₹{customized_metrics.get('monthly_income', 0):,.0f}"),
                ("Monthly Expenses", f"₹{customized_metrics.get('monthly_expenses', 0):,.0f}"),
                ("Savings Rate", f"{customized_metrics.get('savings_rate', 0):.1f}%"),
                ("Emergency Fund", f"{customized_metrics.get('emergency_fund_months', 0):.1f} months")
            ]
            
            for i, (label, value) in enumerate(metrics):
                with [col1, col2, col3, col4][i]:
                    st.metric(label, value)
    
    def analyze_budget(self):
        """Quick budget analysis trigger"""
        if st.session_state.transactions_df.empty:
            st.warning("Please upload transaction data first!")
            return
        
        with st.spinner("Analyzing your budget..."):
            st.session_state.budget_analysis = self.budget_analyzer.analyze_transactions(
                st.session_state.transactions_df,
                st.session_state.user_profile
            )
        
        st.session_state.current_page = 'Budget Analysis'
        st.rerun()
    
    def show_personalized_tips(self):
        """Show personalized financial tips"""
        demographic = st.session_state.user_profile.get('demographic', 'professional')
        tips = self.demographic_adapter.suggest_relevant_topics(demographic)

        st.sidebar.markdown("### 💡 Personalized Tips")
        for tip in tips:
            st.sidebar.info(tip)
    
    def show_smart_alerts(self):
        """Show smart financial alerts page"""
        st.title("🚨 Smart Financial Alerts")
        
        if st.session_state.transactions_df.empty:
            st.warning("Upload transaction data to see personalized alerts!")
            st.info("Smart alerts help you monitor spending patterns, identify unusual activities, and provide proactive financial guidance.")
            return
        
        # Generate alerts
        if st.button("🔄 Refresh Alerts", type="primary"):
            with st.spinner("Analyzing your financial patterns..."):
                self.generate_smart_alerts()
        
        # Display alerts if available
        if st.session_state.alerts:
            # Alert summary
            col1, col2, col3, col4 = st.columns(4)
            
            alert_counts = self.alert_system.get_alert_counts_by_type(st.session_state.alerts)
            
            with col1:
                st.metric("🚨 Critical", alert_counts.get('critical', 0), delta=None)
            with col2:
                st.metric("⚠️ Warnings", alert_counts.get('warning', 0), delta=None)
            with col3:
                st.metric("ℹ️ Info", alert_counts.get('info', 0), delta=None)
            with col4:
                st.metric("✅ Positive", alert_counts.get('positive', 0), delta=None)
            
            st.markdown("---")
            
            # Display alerts grouped by type
            alert_types = ['critical', 'warning', 'info', 'positive', 'tip']
            
            for alert_type in alert_types:
                type_alerts = [a for a in st.session_state.alerts if a.get('type') == alert_type]
                
                if type_alerts:
                    st.subheader(f"{alert_type.title()} Alerts")
                    
                    for alert in type_alerts:
                        alert_color = alert.get('color', 'blue')
                        formatted_alert = self.alert_system.format_alert_for_display(alert)
                        
                        if alert_type == 'critical':
                            st.error(formatted_alert)
                        elif alert_type == 'warning':
                            st.warning(formatted_alert)
                        elif alert_type == 'positive':
                            st.success(formatted_alert)
                        else:
                            st.info(formatted_alert)
        else:
            st.info("Click 'Refresh Alerts' to generate your personalized financial alerts.")
    
    def show_currency_converter(self):
        """Show currency converter page"""
        st.title("💱 Currency Converter")
        st.markdown("Convert between different currencies with real-time exchange rates.")
        
        # Main converter widget
        self.currency_converter.render_currency_widget()
        
        st.markdown("---")
        
        # Additional features
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Popular Conversions")
            popular_pairs = [
                ('USD', 'INR', 'US Dollar to Indian Rupee'),
                ('EUR', 'INR', 'Euro to Indian Rupee'),
                ('GBP', 'INR', 'British Pound to Indian Rupee'),
                ('INR', 'USD', 'Indian Rupee to US Dollar')
            ]
            
            for from_curr, to_curr, desc in popular_pairs:
                try:
                    rate = self.currency_converter.get_exchange_rate(from_curr, to_curr)
                    st.metric(desc, f"{rate:.4f}", delta=None)
                except:
                    st.info(f"{desc}: Rate unavailable")
        
        with col2:
            st.subheader("💡 Currency Tips")
            st.info("💰 **For International Students**: Keep track of education loan EMIs in foreign currency")
            st.info("🌍 **For Professionals**: Monitor currency trends if you have foreign income")
            st.info("✈️ **For Travel**: Plan currency conversion timing for better rates")
    
    def show_pdf_reports(self):
        """Show PDF report generation page"""
        st.title("📄 Financial Reports")
        st.markdown("Generate comprehensive PDF reports of your financial analysis.")
        
        if st.session_state.transactions_df.empty:
            st.warning("Upload transaction data to generate reports!")
            return
        
        if not st.session_state.budget_analysis:
            st.info("Analyzing your budget first...")
            self.analyze_budget()
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Comprehensive Report")
            st.markdown("Full financial analysis with charts, insights, and recommendations.")
            
            if st.button("📥 Generate Full Report", type="primary", key="full_report"):
                with st.spinner("Creating comprehensive report..."):
                    try:
                        pdf_bytes = self.pdf_generator.generate_comprehensive_report(
                            st.session_state.user_profile,
                            st.session_state.budget_analysis,
                            st.session_state.transactions_df
                        )
                        
                        # Create download button
                        st.download_button(
                            label="📥 Download Full Report",
                            data=pdf_bytes,
                            file_name=f"financial_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                            mime="application/pdf",
                            key="download_full"
                        )
                        st.success("✅ Report generated successfully!")
                        
                    except Exception as e:
                        st.error(f"Error generating report: {str(e)}")
        
        with col2:
            st.subheader("📋 Quick Summary")
            st.markdown("One-page summary with key financial metrics.")
            
            if st.button("📄 Generate Summary", key="summary_report"):
                with st.spinner("Creating summary report..."):
                    try:
                        pdf_bytes = self.pdf_generator.create_quick_summary_report(
                            st.session_state.user_profile,
                            st.session_state.budget_analysis
                        )
                        
                        st.download_button(
                            label="📥 Download Summary",
                            data=pdf_bytes,
                            file_name=f"financial_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                            mime="application/pdf",
                            key="download_summary"
                        )
                        st.success("✅ Summary generated successfully!")
                        
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
        
        st.markdown("---")
        
        # Report customization options
        st.subheader("⚙️ Report Options")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            include_charts = st.checkbox("📊 Include Charts", value=True)
        with col2:
            include_recommendations = st.checkbox("💡 Include Recommendations", value=True) 
        with col3:
            include_goals = st.checkbox("🎯 Include Goals", value=True)
    
    def generate_smart_alerts(self):
        """Generate smart alerts for the user"""
        if st.session_state.transactions_df.empty:
            st.warning("No transaction data available for alerts")
            return
        
        # Ensure budget analysis exists
        if not st.session_state.budget_analysis:
            st.session_state.budget_analysis = self.budget_analyzer.analyze_transactions(
                st.session_state.transactions_df,
                st.session_state.user_profile
            )
        
        # Generate alerts
        st.session_state.alerts = self.alert_system.generate_all_alerts(
            st.session_state.transactions_df,
            st.session_state.user_profile,
            st.session_state.budget_analysis
        )
        
        if st.session_state.notifications_enabled:
            alert_count = len(st.session_state.alerts)
            if alert_count > 0:
                st.success(f"✅ Generated {alert_count} smart alerts for you!")
    
    def generate_pdf_report(self):
        """Generate PDF report quick action"""
        if st.session_state.transactions_df.empty:
            st.warning("Please upload transaction data first!")
            return
        
        # Ensure budget analysis exists
        if not st.session_state.budget_analysis:
            with st.spinner("Analyzing budget..."):
                st.session_state.budget_analysis = self.budget_analyzer.analyze_transactions(
                    st.session_state.transactions_df,
                    st.session_state.user_profile
                )
        
        st.session_state.current_page = 'PDF Reports'
        st.rerun()
    
    def run(self):
        """Main application runner with enhanced UI"""
        # Configure page
        st.set_page_config(
            page_title="Personal Finance AI Assistant",
            page_icon="🏦",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Get current language and dark mode
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        dark_mode = st.session_state.get('dark_mode', False)

        # Force language setting and debug
        self.language_support.set_language(current_language)

        # Debug: Show current language in console
        print(f"🌐 Current UI Language: {current_language}")
        print(f"🌐 Language Support Current: {self.language_support.current_language}")

        # Apply theme
        self.enhanced_ui.setup_custom_css(dark_mode)

        # Setup enhanced sidebar
        updated_profile = self.enhanced_ui.create_enhanced_sidebar(
            st.session_state.user_profile,
            self.language_support,
            self.user_profile_manager
        )
        st.session_state.user_profile = updated_profile

        # Add voice interface to sidebar
        voice_settings = self.enhanced_ui.create_voice_interface_section(
            self.language_support,
            self.voice_interface
        )

        # Create main header
        title = self.language_support.get_text('welcome')
        user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')
        subtitle = f"{self.language_support.get_text(user_type)} Dashboard"

        self.enhanced_ui.create_header(title, subtitle, current_language)

        # Navigation with direct tab switching
        self.setup_enhanced_navigation()

    def setup_enhanced_navigation(self):
        """Setup enhanced navigation with direct tab switching"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')

        # Navigation tabs
        tab_names = [
            self.language_support.get_text('chat'),
            self.language_support.get_text('budget_analysis'),
            self.language_support.get_text('smart_alerts'),
            self.language_support.get_text('currency_converter'),
            self.language_support.get_text('data_upload'),
            self.language_support.get_text('pdf_reports'),
            self.language_support.get_text('insights_dashboard')
        ]

        tab_keys = ['Chat', 'Budget Analysis', 'Smart Alerts', 'Currency Converter', 'Data Upload', 'PDF Reports', 'Insights Dashboard']

        # Create tabs with direct content
        tabs = st.tabs(tab_names)

        # Show content directly in tabs
        with tabs[0]:  # Chat
            self.show_enhanced_chat_interface()

        with tabs[1]:  # Budget Analysis
            self.show_budget_analysis()

        with tabs[2]:  # Smart Alerts
            self.show_smart_alerts()

        with tabs[3]:  # Currency Converter
            self.show_currency_converter()

        with tabs[4]:  # Data Upload
            self.show_data_upload()

        with tabs[5]:  # PDF Reports
            self.show_pdf_reports()

        with tabs[6]:  # Insights Dashboard
            self.show_insights_dashboard()

    def show_enhanced_chat_interface(self):
        """Simple, fast chat interface"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')

        # Simple welcome message
        welcome_text = "Welcome to your Personal Finance Assistant!" if current_language == 'english' else "உங்கள் தனிப்பட்ட நிதி உதவியாளருக்கு வரவேற்கிறோம்!"
        st.markdown(f"### 💬 {welcome_text}")

        # Voice input processing (simplified)
        if st.session_state.get('voice_listening', False):
            st.info("🎙️ Listening..." if current_language == 'english' else "🎙️ கேட்கிறேன்...")

            # Quick voice demo
            if st.button("🎤 Demo Voice" if current_language == 'english' else "🎤 குரல் டெமோ"):
                sample_inputs = {
                    'english': ["How can I save money?", "Budget help", "Investment advice"],
                    'tamil': ["பணம் சேமிப்பு?", "பட்ஜெட் உதவி", "முதலீட்டு ஆலோசனை"]
                }

                import random
                voice_input = random.choice(sample_inputs.get(current_language, sample_inputs['english']))
                st.success(f"🎤 {voice_input}")
                st.session_state.voice_listening = False

                # Quick response
                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []

                st.session_state.chat_history.append({"role": "user", "content": voice_input, "timestamp": datetime.now()})

                # Generate response
                response = self.generate_enhanced_response(voice_input, current_language, user_type)
                st.session_state.chat_history.append({"role": "assistant", "content": response, "timestamp": datetime.now()})

                st.rerun()

        # Show progress if user is new
        if not st.session_state.onboarding_completed:
            progress_steps = [
                {'title': 'Complete Profile', 'completed': bool(st.session_state.user_profile.get('basic_info', {}).get('name'))},
                {'title': 'Upload Data', 'completed': not st.session_state.transactions_df.empty},
                {'title': 'First Analysis', 'completed': bool(st.session_state.budget_analysis)},
                {'title': 'Generate Report', 'completed': False, 'current': True}
            ]
            self.enhanced_ui.create_progress_indicator(progress_steps, current_language)

        # Show alerts banner if alerts exist
        if st.session_state.alerts and st.session_state.notifications_enabled:
            critical_alerts = [a for a in st.session_state.alerts if a.get('type') == 'critical']
            warning_alerts = [a for a in st.session_state.alerts if a.get('type') == 'warning']

            if critical_alerts:
                self.enhanced_ui.create_warning_alert(
                    f"🚨 You have {len(critical_alerts)} critical financial alert(s)! Check the Smart Alerts page."
                )
            elif warning_alerts:
                self.enhanced_ui.create_warning_alert(
                    f"⚠️ You have {len(warning_alerts)} financial warning(s). Check Smart Alerts for details."
                )

        # Show suggested topics
        if not st.session_state.chat_history:
            st.subheader(self.language_support.get_text('ask_question'))

            suggested_topics = self.user_profile_manager.get_suggested_topics(
                st.session_state.user_profile,
                current_language
            )

            # Create feature grid for suggested topics
            features = []
            icons = ["💰", "📊", "🎯", "📈"]
            for i, topic in enumerate(suggested_topics[:4]):
                features.append({
                    'icon': icons[i % len(icons)],
                    'title': f"Topic {i+1}",
                    'description': topic
                })

            self.enhanced_ui.create_feature_grid(features, current_language)

            # Quick action buttons
            cols = st.columns(len(suggested_topics))
            for i, topic in enumerate(suggested_topics):
                with cols[i % len(cols)]:
                    if st.button(topic, key=f"suggestion_{i}"):
                        self.process_enhanced_user_message(topic)

        # Chat history with enhanced styling
        for i, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                self.enhanced_ui.create_chat_message(message['content'], is_user=True, language=current_language)
            else:
                self.enhanced_ui.create_chat_message(message['content'], is_user=False, language=current_language)

        # Chat input
        user_input = st.chat_input(self.language_support.get_text('ask_question'))

        if user_input:
            self.process_enhanced_user_message(user_input)

    def process_enhanced_user_message(self, user_input: str):
        """Process user message with enhanced language support"""
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')

        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })

        # Translate and understand query
        translation_result = self.language_support.translate_query(user_input)

        # Process with NLP (enhanced with language detection)
        if translation_result['detected_language'] == 'tamil':
            # Use translated concepts for processing
            query_analysis = {
                'intent': {'primary': translation_result['intent']},
                'concepts': translation_result['concepts'],
                'language': 'tamil'
            }
        else:
            # Use standard NLP processing
            query_analysis = self.nlp_processor.process_query(
                user_input,
                st.session_state.user_profile
            )
            query_analysis['language'] = 'english'

        # Generate response
        current_language = st.session_state.user_profile.get('basic_info', {}).get('language', 'english')
        user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')
        response = self.generate_enhanced_response(user_input, current_language, user_type)

        # Format response for user type and language
        user_type = st.session_state.user_profile.get('basic_info', {}).get('user_type', 'beginner')
        formatted_response = self.language_support.format_response_for_language(response, user_type)

        # Add bot response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': formatted_response,
            'timestamp': datetime.now()
        })

        st.rerun()

    def generate_enhanced_response(self, user_input: str, language: str, user_type: str) -> str:
        """Generate enhanced response with language and user type support"""
        try:
            # Set language for processing
            self.language_support.set_language(language)

            # Translate and understand query
            translation_result = self.language_support.translate_query(user_input)

            # Create query analysis
            if translation_result['detected_language'] == 'tamil':
                query_analysis = {
                    'intent': {'primary': translation_result['intent']},
                    'concepts': translation_result['concepts'],
                    'language': 'tamil'
                }
            else:
                query_analysis = self.nlp_processor.process_query(user_input, st.session_state.user_profile)
                query_analysis['language'] = language

            # Generate response using the existing method
            return self.generate_enhanced_response_with_analysis(user_input, query_analysis)

        except Exception as e:
            self.logger.error(f"Enhanced response generation failed: {e}")
            if language == 'tamil':
                return "மன்னிக்கவும், ஒரு பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்."
            else:
                return "I apologize, but I encountered an issue. Please try again."

    def generate_enhanced_response_with_analysis(self, user_input: str, query_analysis: Dict) -> str:
        """Generate enhanced response with better language and user type support"""
        try:
            intent = query_analysis.get('intent', {}).get('primary', 'general_query')
            user_profile = st.session_state.user_profile
            user_type = user_profile.get('basic_info', {}).get('user_type', 'beginner')
            language = query_analysis.get('language', 'english')

            # Check if query requires data analysis
            if query_analysis.get('requires_data', {}).get('requires_data'):
                if not st.session_state.transactions_df.empty:
                    return self.generate_data_driven_response(user_input, query_analysis)
                else:
                    return self.generate_no_data_response(intent, user_type, language)

            # Generate contextual response using enhanced demographic adapter
            if intent in ['budget_management', 'savings_advice', 'investment_guidance', 'tax_advice']:
                response = self.demographic_adapter.adapt_response(
                    "", user_type, intent
                )
            else:
                response = self.generate_general_response(user_input, query_analysis)

            # Add follow-up questions based on user type
            followups = self.get_user_type_followups(user_type, intent, language)
            if followups:
                response += f"\n\n🤔 **{self.language_support.get_text('help') if language == 'tamil' else 'You might also want to know'}:**\n"
                for i, followup in enumerate(followups[:2]):
                    response += f"{i+1}. {followup}\n"

            return response

        except Exception as e:
            logger.error(f"Error generating enhanced response: {e}")
            error_msg = "மன்னிக்கவும், ஒரு பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்." if query_analysis.get('language') == 'tamil' else "I apologize, but I encountered an issue processing your request. Could you please try rephrasing your question?"
            return error_msg

    def generate_no_data_response(self, intent: str, user_type: str, language: str) -> str:
        """Generate response when data is required but not available"""
        if language == 'tamil':
            response = "உங்கள் நிதி தரவின் அடிப்படையில் தனிப்பட்ட நுண்ணறிவுகளை வழங்க விரும்புகிறேன்! "

            if user_type == 'student':
                response += "அடிப்படை செலவு கண்காணிப்பு கூட உங்களுக்கு அதிக பணம் சேமிக்க உதவும்! 💰"
            else:
                response += "தரவு அடிப்படையிலான நிதி திட்டமிடல் மிகவும் சிறந்த முடிவுகளுக்கு வழிவகுக்கிறது. 📊"

            response += "\n\nதொடங்க:\n"
            response += "1. 📤 'தரவு பதிவேற்றம்' பிரிவில் உங்கள் பரிவர்த்தனை தரவைப் பதிவேற்றவும்\n"
            response += "2. 📊 உங்கள் செலவு முறைகளை பகுப்பாய்வு செய்வேன்\n"
            response += "3. 💡 உங்கள் தரவின் அடிப்படையில் தனிப்பட்ட பரிந்துரைகளைப் பெறுங்கள்\n\n"
            response += f"இதற்கிடையில், {intent.replace('_', ' ')} பற்றி பொதுவான ஆலோசனை வழங்க முடியும்!"
        else:
            response = "I'd love to give you personalized insights based on your financial data! "

            if user_type == 'student':
                response += "Even basic expense tracking can help you save more money for the things you want! 💰"
            elif user_type == 'beginner':
                response += "Don't worry, we'll start with simple steps to understand your finances better! 🌟"
            else:
                response += "Data-driven financial planning leads to much better outcomes. 📊"

            response += "\n\nTo get started:\n"
            response += "1. 📤 Upload your transaction data in the 'Data Upload' section\n"
            response += "2. 📊 I'll analyze your spending patterns\n"
            response += "3. 💡 Get personalized recommendations based on your data\n\n"
            response += "In the meantime, I can provide general advice about " + intent.replace('_', ' ') + "!"

        return response

    def get_user_type_followups(self, user_type: str, intent: str, language: str) -> List[str]:
        """Get follow-up questions based on user type"""
        followups = {
            'english': {
                'student': {
                    'budget_management': ["How to track expenses as a student?", "Best budgeting apps for students?"],
                    'savings_advice': ["How much should students save monthly?", "Student-friendly investment options?"],
                    'investment_guidance': ["Safe investment options for students?", "How to start investing with small amounts?"]
                },
                'professional': {
                    'budget_management': ["Advanced budgeting strategies?", "How to optimize tax-efficient spending?"],
                    'savings_advice': ["Optimal savings rate for professionals?", "Emergency fund calculation?"],
                    'investment_guidance': ["Portfolio diversification strategies?", "Tax-saving investment options?"]
                },
                'beginner': {
                    'budget_management': ["What is the 50/30/20 rule?", "How to create my first budget?"],
                    'savings_advice': ["What is an emergency fund?", "How to start saving with low income?"],
                    'investment_guidance': ["What are mutual funds?", "Difference between stocks and bonds?"]
                },
                'intermediate': {
                    'budget_management': ["Zero-based budgeting techniques?", "How to track irregular income?"],
                    'savings_advice': ["Goal-based savings strategies?", "High-yield savings options?"],
                    'investment_guidance': ["Asset allocation strategies?", "How to rebalance portfolio?"]
                }
            },
            'tamil': {
                'student': {
                    'budget_management': ["மாணவராக செலவுகளை எப்படி கண்காணிப்பது?", "மாணவர்களுக்கான சிறந்த பட்ஜெட்டிங் ஆப்ஸ்?"],
                    'savings_advice': ["மாணவர்கள் மாதம் எவ்வளவு சேமிக்க வேண்டும்?", "மாணவர் நட்பு முதலீட்டு விருப்பங்கள்?"],
                    'investment_guidance': ["மாணவர்களுக்கான பாதுகாப்பான முதலீட்டு விருப்பங்கள்?", "சிறிய தொகையில் முதலீடு எப்படி தொடங்குவது?"]
                },
                'professional': {
                    'budget_management': ["மேம்பட்ட பட்ஜெட்டிங் உத்திகள்?", "வரி-திறமையான செலவுகளை எப்படி மேம்படுத்துவது?"],
                    'savings_advice': ["தொழில்முறையாளர்களுக்கான உகந்த சேமிப்பு விகிதம்?", "அவசர நிதி கணக்கீடு?"],
                    'investment_guidance': ["போர்ட்ஃபோலியோ பல்வகைப்படுத்தல் உத்திகள்?", "வரி சேமிப்பு முதலீட்டு விருப்பங்கள்?"]
                }
            }
        }

        return followups.get(language, followups['english']).get(user_type, {}).get(intent, [])

def main():
    """Main function to run the application"""
    try:
        app = PersonalFinanceChatbot()
        app.run()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        logger.error(f"Application error: {e}")

if __name__ == "__main__":
    main()