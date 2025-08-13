"""
JarvisFi - Chat Interface Component
Advanced chat interface with AI responses, voice support, and multilingual capabilities
"""

import streamlit as st
import time
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

def render_chat_interface():
    """Render the main chat interface"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    # Chat header
    if current_language == 'en':
        st.markdown("### 💬 Chat with JarvisFi")
        st.markdown("Ask me anything about personal finance, investments, budgeting, and more!")
    elif current_language == 'ta':
        st.markdown("### 💬 JarvisFi உடன் அரட்டையடிக்கவும்")
        st.markdown("தனிப்பட்ட நிதி, முதலீடுகள், பட்ஜெட் மற்றும் பலவற்றைப் பற்றி என்னிடம் எதையும் கேளுங்கள்!")
    elif current_language == 'hi':
        st.markdown("### 💬 JarvisFi के साथ चैट करें")
        st.markdown("व्यक्तिगत वित्त, निवेश, बजट और अधिक के बारे में मुझसे कुछ भी पूछें!")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        display_chat_history()
        
        # Chat input area
        render_chat_input()
        
        # Quick action buttons
        render_quick_actions()
        
        # Voice controls
        render_voice_controls()


def display_chat_history():
    """Display chat message history"""
    if not st.session_state.chat_history:
        # Show welcome message
        show_welcome_message()
    else:
        # Display all messages
        for message in st.session_state.chat_history:
            display_message(message)


def show_welcome_message():
    """Show welcome message for new users"""
    current_language = st.session_state.user_profile['basic_info']['language']
    user_type = st.session_state.user_profile['basic_info']['user_type']
    user_name = st.session_state.user_profile['basic_info']['name']
    
    # Personalized welcome based on user type and language
    welcome_messages = {
        'en': {
            'beginner': f"👋 Hello {user_name or 'there'}! I'm JarvisFi, your AI financial genius. I'm here to help you start your financial journey. You can ask me about:\n\n💰 **Basic budgeting tips**\n📊 **Simple investment options**\n🏦 **Savings strategies**\n📱 **Financial apps and tools**\n\nWhat would you like to learn about first?",
            'intermediate': f"👋 Welcome back {user_name or 'there'}! I'm JarvisFi, ready to help you optimize your finances. I can assist with:\n\n📈 **Investment portfolio analysis**\n💼 **Tax planning strategies**\n🎯 **Goal-based financial planning**\n📊 **Market insights and trends**\n\nWhat financial topic interests you today?",
            'professional': f"👋 Hello {user_name or 'there'}! I'm JarvisFi, your advanced financial advisor. I can help with:\n\n🏢 **Corporate finance strategies**\n💹 **Advanced investment analysis**\n📋 **Risk management**\n🌐 **International finance**\n\nHow can I assist you today?",
            'student': f"👋 Hi {user_name or 'there'}! I'm JarvisFi, here to help you build smart money habits. Let's explore:\n\n🎓 **Student budgeting**\n💳 **Building credit history**\n📚 **Education loan management**\n💰 **Part-time income optimization**\n\nWhat would you like to know?",
            'farmer': f"👋 Namaste {user_name or 'there'}! I'm JarvisFi, your agricultural finance expert. I can help with:\n\n🌾 **Crop loan guidance**\n📊 **MSP and market prices**\n🏛️ **Government subsidies**\n🌧️ **Weather-based planning**\n\nHow can I support your farming business?",
            'senior_citizen': f"👋 Hello {user_name or 'there'}! I'm JarvisFi, here to help with your retirement planning. I can assist with:\n\n🏥 **Healthcare financial planning**\n💰 **Pension optimization**\n🏠 **Estate planning basics**\n📊 **Safe investment options**\n\nWhat would you like to discuss?"
        },
        'ta': {
            'beginner': f"👋 வணக்கம் {user_name or 'நண்பரே'}! நான் JarvisFi, உங்கள் AI நிதி மேதை. உங்கள் நிதி பயணத்தைத் தொடங்க உதவ நான் இங்கே இருக்கிறேன். நீங்கள் என்னிடம் கேட்கலாம்:\n\n💰 **அடிப்படை பட்ஜெட் குறிப்புகள்**\n📊 **எளிய முதலீட்டு விருப்பங்கள்**\n🏦 **சேமிப்பு உத்திகள்**\n📱 **நிதி பயன்பாடுகள் மற்றும் கருவிகள்**\n\nமுதலில் எதைப் பற்றி அறிய விரும்புகிறீர்கள்?",
            'intermediate': f"👋 மீண்டும் வரவேற்கிறோம் {user_name or 'நண்பரே'}! நான் JarvisFi, உங்கள் நிதியை மேம்படுத்த உதவ தயாராக இருக்கிறேன். நான் உதவ முடியும்:\n\n📈 **முதலீட்டு போர்ட்ஃபோலியோ பகுப்பாய்வு**\n💼 **வரி திட்டமிடல் உத்திகள்**\n🎯 **இலக்கு அடிப்படையிலான நிதி திட்டமிடல்**\n📊 **சந்தை நுண்ணறிவு மற்றும் போக்குகள்**\n\nஇன்று எந்த நிதி தலைப்பு உங்களுக்கு ஆர்வமாக உள்ளது?",
            'student': f"👋 வணக்கம் {user_name or 'நண்பரே'}! நான் JarvisFi, புத்திசாலித்தனமான பண பழக்கங்களை உருவாக்க உதவ இங்கே இருக்கிறேன். ஆராய்வோம்:\n\n🎓 **மாணவர் பட்ஜெட்**\n💳 **கிரெடிட் வரலாற்றை உருவாக்குதல்**\n📚 **கல்விக் கடன் மேலாண்மை**\n💰 **பகுதி நேர வருமான மேம்பாடு**\n\nநீங்கள் என்ன தெரிந்து கொள்ள விரும்புகிறீர்கள்?"
        },
        'hi': {
            'beginner': f"👋 नमस्ते {user_name or 'दोस्त'}! मैं JarvisFi हूं, आपका AI वित्तीय प्रतिभा। मैं आपकी वित्तीय यात्रा शुरू करने में मदद के लिए यहां हूं। आप मुझसे पूछ सकते हैं:\n\n💰 **बुनियादी बजट टिप्स**\n📊 **सरल निवेश विकल्प**\n🏦 **बचत रणनीतियां**\n📱 **वित्तीय ऐप्स और टूल्स**\n\nआप पहले किस बारे में जानना चाहेंगे?",
            'student': f"👋 नमस्ते {user_name or 'दोस्त'}! मैं JarvisFi हूं, स्मार्ट पैसे की आदतें बनाने में आपकी मदद के लिए यहां हूं। आइए जानें:\n\n🎓 **छात्र बजट**\n💳 **क्रेडिट हिस्ट्री बनाना**\n📚 **शिक्षा ऋण प्रबंधन**\n💰 **पार्ट-टाइम आय अनुकूलन**\n\nआप क्या जानना चाहेंगे?"
        }
    }
    
    # Get appropriate welcome message
    lang_messages = welcome_messages.get(current_language, welcome_messages['en'])
    welcome_text = lang_messages.get(user_type, lang_messages.get('beginner', ''))
    
    # Display welcome message
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(welcome_text)
    
    # Add to chat history
    if not st.session_state.chat_history:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": welcome_text,
            "timestamp": datetime.now().isoformat(),
            "type": "welcome"
        })


def display_message(message: Dict[str, Any]):
    """Display a single chat message"""
    role = message.get("role", "user")
    content = message.get("content", "")
    timestamp = message.get("timestamp", "")
    message_type = message.get("type", "text")
    
    # Choose avatar
    avatar = "🤖" if role == "assistant" else "👤"
    
    with st.chat_message(role, avatar=avatar):
        # Display content
        st.markdown(content)
        
        # Display additional info for assistant messages
        if role == "assistant" and message_type != "welcome":
            display_message_metadata(message)
        
        # Display timestamp
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime("%H:%M")
                st.caption(f"⏰ {time_str}")
            except:
                pass


def display_message_metadata(message: Dict[str, Any]):
    """Display metadata for assistant messages"""
    metadata = message.get("metadata", {})
    
    if metadata:
        with st.expander("📊 Response Details", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                confidence = metadata.get("confidence", 0.5)
                st.metric("Confidence", f"{confidence:.1%}")
            
            with col2:
                intent = metadata.get("intent", "general")
                st.metric("Intent", intent.title())
            
            with col3:
                sentiment = metadata.get("sentiment", {})
                sentiment_label = sentiment.get("label", "NEUTRAL")
                st.metric("Sentiment", sentiment_label)
            
            # Sources
            sources = metadata.get("sources", [])
            if sources:
                st.markdown("**Sources:**")
                for source in sources:
                    st.markdown(f"• {source}")


def render_chat_input():
    """Render chat input area"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    # Chat input
    placeholder_text = {
        'en': "Ask JarvisFi about budgets, investments, savings, taxes...",
        'ta': "பட்ஜெட், முதலீடுகள், சேமிப்பு, வரிகள் பற்றி JarvisFi-யிடம் கேளுங்கள்...",
        'hi': "बजट, निवेश, बचत, कर के बारे में JarvisFi से पूछें..."
    }
    
    user_input = st.chat_input(
        placeholder_text.get(current_language, placeholder_text['en'])
    )
    
    if user_input:
        process_user_message(user_input)


def process_user_message(user_input: str):
    """Process user message and generate AI response"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    # Add user message to history
    user_message = {
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat(),
        "type": "text"
    }
    st.session_state.chat_history.append(user_message)
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Generate AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("JarvisFi is thinking..." if current_language == 'en' else 
                       "JarvisFi யோசித்துக்கொண்டிருக்கிறது..." if current_language == 'ta' else 
                       "JarvisFi सोच रहा है..."):
            
            # Simulate AI processing
            time.sleep(1)
            
            # Generate response based on user input
            ai_response = generate_ai_response(user_input, current_language)
            
            # Display response
            st.markdown(ai_response["content"])
            
            # Display metadata
            if ai_response.get("metadata"):
                display_message_metadata(ai_response)
    
    # Add AI response to history
    st.session_state.chat_history.append(ai_response)


def generate_ai_response(user_input: str, language: str) -> Dict[str, Any]:
    """Generate AI response based on user input"""
    user_context = {
        'user_type': st.session_state.user_profile['basic_info']['user_type'],
        'monthly_income': st.session_state.user_profile['basic_info']['monthly_income'],
        'age': st.session_state.user_profile['basic_info'].get('age', 25),
        'location': st.session_state.user_profile['basic_info'].get('location', 'India'),
        'risk_tolerance': st.session_state.user_profile['financial_profile']['risk_tolerance'],
        'investment_experience': st.session_state.user_profile['financial_profile']['investment_experience']
    }
    
    # Simple rule-based response generation (in production, this would call the AI service)
    response_content = generate_rule_based_response(user_input, user_context, language)
    
    # Calculate metadata
    intent = classify_intent(user_input)
    confidence = calculate_confidence(user_input, response_content)
    sentiment = analyze_sentiment(response_content)
    sources = get_relevant_sources(intent)
    
    return {
        "role": "assistant",
        "content": response_content,
        "timestamp": datetime.now().isoformat(),
        "type": "ai_response",
        "metadata": {
            "intent": intent,
            "confidence": confidence,
            "sentiment": sentiment,
            "sources": sources,
            "language": language
        }
    }


def generate_rule_based_response(user_input: str, user_context: Dict[str, Any], language: str) -> str:
    """Generate rule-based response (fallback when AI service is unavailable)"""
    user_input_lower = user_input.lower()
    monthly_income = user_context['monthly_income']
    user_type = user_context['user_type']
    
    # Budget-related queries
    if any(word in user_input_lower for word in ['budget', 'budgeting', 'expense', 'spending']):
        if language == 'en':
            return f"""Great question about budgeting! Based on your monthly income of ₹{monthly_income:,}, here's my personalized advice:

**50/30/20 Rule for You:**
• **Needs (50%):** ₹{int(monthly_income * 0.5):,} for rent, food, utilities
• **Wants (30%):** ₹{int(monthly_income * 0.3):,} for entertainment, dining out
• **Savings (20%):** ₹{int(monthly_income * 0.2):,} for emergency fund and investments

**Quick Tips:**
1. Track every expense for one month
2. Use apps like Money Manager or Walnut
3. Set up automatic transfers to savings
4. Review and adjust monthly

Would you like me to help you create a detailed budget breakdown?"""
        
        elif language == 'ta':
            return f"""பட்ஜெட் பற்றிய சிறந்த கேள்வி! உங்கள் மாதாந்திர வருமானம் ₹{monthly_income:,} அடிப்படையில், இதோ எனது தனிப்பயனாக்கப்பட்ட ஆலோசனை:

**உங்களுக்கான 50/30/20 விதி:**
• **தேவைகள் (50%):** ₹{int(monthly_income * 0.5):,} வாடகை, உணவு, பயன்பாடுகளுக்கு
• **விருப்பங்கள் (30%):** ₹{int(monthly_income * 0.3):,} பொழுதுபோக்கு, வெளியில் சாப்பிடுவதற்கு
• **சேமிப்பு (20%):** ₹{int(monthly_income * 0.2):,} அவசரகால நிதி மற்றும் முதலீடுகளுக்கு

**விரைவு குறிப்புகள்:**
1. ஒரு மாதத்திற்கு ஒவ்வொரு செலவையும் கண்காணிக்கவும்
2. Money Manager அல்லது Walnut போன்ற பயன்பாடுகளைப் பயன்படுத்துங்கள்
3. சேமிப்புக்கு தானியங்கு பரிமாற்றங்களை அமைக்கவும்
4. மாதந்தோறும் மதிப்பாய்வு செய்து சரிசெய்யுங்கள்

விரிவான பட்ஜெட் பிரிவை உருவாக்க உதவ வேண்டுமா?"""
    
    # Investment-related queries
    elif any(word in user_input_lower for word in ['invest', 'investment', 'sip', 'mutual fund']):
        if language == 'en':
            suggested_sip = max(1000, int(monthly_income * 0.15))
            return f"""Excellent! Let's talk investments. Based on your profile as a {user_type} with ₹{monthly_income:,} monthly income:

**Recommended SIP Amount:** ₹{suggested_sip:,}/month (15% of income)

**Investment Strategy:**
1. **Emergency Fund First:** Build 6 months expenses (₹{int(monthly_income * 0.7 * 6):,})
2. **Start SIPs:** Begin with diversified equity funds
3. **Tax Saving:** Consider ELSS funds for 80C benefits
4. **Long-term Focus:** Invest for 5+ years minimum

**Beginner-Friendly Options:**
• Index Funds (Nifty 50, Sensex)
• Large Cap Mutual Funds
• Balanced Advantage Funds

**Next Steps:**
1. Complete KYC with any AMC
2. Start with ₹1,000 SIP
3. Increase by 10% annually

Would you like specific fund recommendations?"""
        
        elif language == 'ta':
            suggested_sip = max(1000, int(monthly_income * 0.15))
            return f"""அருமை! முதலீடுகளைப் பற்றி பேசுவோம். ₹{monthly_income:,} மாதாந்திர வருமானம் கொண்ட {user_type} என்ற உங்கள் சுயவிவரத்தின் அடிப்படையில்:

**பரிந்துரைக்கப்பட்ட SIP தொகை:** ₹{suggested_sip:,}/மாதம் (வருமானத்தின் 15%)

**முதலீட்டு உத்தி:**
1. **முதலில் அவசரகால நிதி:** 6 மாத செலவுகளை உருவாக்குங்கள் (₹{int(monthly_income * 0.7 * 6):,})
2. **SIP களைத் தொடங்குங்கள்:** பல்வகைப்படுத்தப்பட்ட ஈக்விட்டி நிதிகளுடன் தொடங்குங்கள்
3. **வரி சேமிப்பு:** 80C நன்மைகளுக்கு ELSS நிதிகளைக் கருத்தில் கொள்ளுங்கள்
4. **நீண்ட கால கவனம்:** குறைந்தபட்சம் 5+ ஆண்டுகளுக்கு முதலீடு செய்யுங்கள்

அடுத்த படிகள் என்ன தெரிய வேண்டுமா?"""
    
    # Savings-related queries
    elif any(word in user_input_lower for word in ['save', 'saving', 'savings']):
        if language == 'en':
            target_savings = int(monthly_income * 0.2)
            return f"""Smart thinking about savings! Here's a personalized savings plan for your ₹{monthly_income:,} income:

**Monthly Savings Target:** ₹{target_savings:,} (20% of income)

**Savings Breakdown:**
• **Emergency Fund:** ₹{int(target_savings * 0.4):,} (until you have 6 months expenses)
• **Short-term Goals:** ₹{int(target_savings * 0.3):,} (vacation, gadgets)
• **Long-term Investments:** ₹{int(target_savings * 0.3):,} (retirement, wealth building)

**Best Savings Options:**
1. **High-yield Savings:** 6-7% annual returns
2. **Fixed Deposits:** 6.5-7.5% for 1-3 years
3. **PPF:** 7.1% tax-free (15-year lock-in)
4. **NSC:** 6.8% with tax benefits

**Automation Tips:**
• Set up auto-transfer on salary day
• Use separate accounts for different goals
• Round up purchases and save the change

Want help setting up automatic savings?"""
    
    # Default response
    else:
        if language == 'en':
            return f"""Hello! I'm JarvisFi, your AI financial genius. I can help you with:

💰 **Budgeting & Expense Management**
📈 **Investment Planning & SIPs**
🏦 **Savings Strategies**
💳 **Credit & Debt Management**
🎯 **Financial Goal Planning**
📊 **Tax Planning**

Based on your profile:
• Monthly Income: ₹{monthly_income:,}
• User Type: {user_type.title()}
• Risk Tolerance: {user_context['risk_tolerance'].title()}

What specific financial topic would you like to explore today?"""
        
        elif language == 'ta':
            return f"""வணக்கம்! நான் JarvisFi, உங்கள் AI நிதி மேதை. நான் உங்களுக்கு உதவ முடியும்:

💰 **பட்ஜெட் & செலவு மேலாண்மை**
📈 **முதலீட்டு திட்டமிடல் & SIP கள்**
🏦 **சேமிப்பு உத்திகள்**
💳 **கிரெடிட் & கடன் மேலாண்மை**
🎯 **நிதி இலக்கு திட்டமிடல்**
📊 **வரி திட்டமிடல்**

உங்கள் சுயவிவரத்தின் அடிப்படையில்:
• மாதாந்திர வருமானம்: ₹{monthly_income:,}
• பயனர் வகை: {user_type.title()}

இன்று எந்த குறிப்பிட்ட நிதி தலைப்பை ஆராய விரும்புகிறீர்கள்?"""
    
    return "I'm here to help with your financial questions!"


def classify_intent(user_input: str) -> str:
    """Classify user intent from input"""
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ['budget', 'expense', 'spending']):
        return 'budgeting'
    elif any(word in user_input_lower for word in ['invest', 'investment', 'sip', 'mutual fund']):
        return 'investment'
    elif any(word in user_input_lower for word in ['save', 'saving', 'savings']):
        return 'savings'
    elif any(word in user_input_lower for word in ['loan', 'debt', 'credit']):
        return 'debt_management'
    elif any(word in user_input_lower for word in ['tax', 'taxation']):
        return 'tax_planning'
    elif any(word in user_input_lower for word in ['insurance', 'policy']):
        return 'insurance'
    else:
        return 'general_financial'


def calculate_confidence(user_input: str, response: str) -> float:
    """Calculate confidence score for response"""
    # Simple confidence calculation
    confidence = 0.7  # Base confidence
    
    # Increase confidence for longer, more detailed responses
    if len(response) > 200:
        confidence += 0.1
    
    # Increase confidence if response contains specific financial terms
    financial_terms = ['investment', 'savings', 'budget', 'SIP', 'mutual fund', 'PPF', 'ELSS']
    term_count = sum(1 for term in financial_terms if term.lower() in response.lower())
    confidence += min(term_count * 0.05, 0.2)
    
    return min(confidence, 1.0)


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """Analyze sentiment of text"""
    # Simple sentiment analysis
    positive_words = ['good', 'great', 'excellent', 'smart', 'wise', 'beneficial']
    negative_words = ['bad', 'poor', 'risky', 'dangerous', 'avoid']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return {"label": "POSITIVE", "score": 0.8}
    elif negative_count > positive_count:
        return {"label": "NEGATIVE", "score": 0.8}
    else:
        return {"label": "NEUTRAL", "score": 0.6}


def get_relevant_sources(intent: str) -> List[str]:
    """Get relevant sources for financial advice"""
    sources = {
        'investment': ['SEBI Guidelines', 'Mutual Fund Fact Sheets', 'RBI Investment Guidelines'],
        'tax_planning': ['Income Tax Act 1961', 'CBDT Circulars', 'Tax Planning Guidelines'],
        'savings': ['RBI Savings Guidelines', 'Bank Interest Rate Policies', 'Government Savings Schemes'],
        'insurance': ['IRDAI Guidelines', 'Insurance Product Comparisons', 'Claim Settlement Ratios'],
        'budgeting': ['Personal Finance Best Practices', 'Financial Planning Guidelines'],
        'debt_management': ['RBI Debt Guidelines', 'Credit Bureau Reports', 'Debt Management Strategies']
    }
    
    return sources.get(intent, ['General Financial Guidelines', 'RBI Publications'])


def render_quick_actions():
    """Render quick action buttons"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    st.markdown("---")
    if current_language == 'en':
        st.markdown("**💡 Quick Questions:**")
    elif current_language == 'ta':
        st.markdown("**💡 விரைவு கேள்விகள்:**")
    elif current_language == 'hi':
        st.markdown("**💡 त्वरित प्रश्न:**")
    
    # Quick action buttons
    col1, col2, col3 = st.columns(3)
    
    quick_questions = {
        'en': [
            "How to start investing?",
            "Create a budget plan",
            "Best savings options?"
        ],
        'ta': [
            "முதலீடு எப்படி தொடங்குவது?",
            "பட்ஜெட் திட்டம் உருவாக்கு",
            "சிறந்த சேமிப்பு விருப்பங்கள்?"
        ],
        'hi': [
            "निवेश कैसे शुरू करें?",
            "बजट योजना बनाएं",
            "सर्वोत्तम बचत विकल्प?"
        ]
    }
    
    questions = quick_questions.get(current_language, quick_questions['en'])
    
    with col1:
        if st.button(questions[0], key="quick_1"):
            process_user_message(questions[0])
    
    with col2:
        if st.button(questions[1], key="quick_2"):
            process_user_message(questions[1])
    
    with col3:
        if st.button(questions[2], key="quick_3"):
            process_user_message(questions[2])


def render_voice_controls():
    """Render voice interface controls"""
    current_language = st.session_state.user_profile['basic_info']['language']
    
    if st.session_state.user_profile['preferences']['voice_enabled']:
        st.markdown("---")
        if current_language == 'en':
            st.markdown("**🎤 Voice Controls:**")
        elif current_language == 'ta':
            st.markdown("**🎤 குரல் கட்டுப்பாடுகள்:**")
        elif current_language == 'hi':
            st.markdown("**🎤 आवाज़ नियंत्रण:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎙️ " + ("Voice Input" if current_language == 'en' else "குரல் உள்ளீடு" if current_language == 'ta' else "आवाज़ इनपुट"), key="voice_input_chat"):
                st.info("Voice input feature coming soon!")
        
        with col2:
            if st.button("🔊 " + ("Read Aloud" if current_language == 'en' else "சத்தமாக படிக்கவும்" if current_language == 'ta' else "जोर से पढ़ें"), key="voice_output_chat"):
                st.info("Text-to-speech feature coming soon!")
