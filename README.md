# 🤖 JarvisFi - Multilingual AI Personal Finance Chatbot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-Powered-purple.svg)](https://huggingface.co)

> **Your AI-Powered Financial Genius** - A comprehensive multilingual personal finance chatbot with advanced features for financial planning, investment advice, and agricultural finance tools.

## 🌟 **Key Features**

### 🌍 **Multilingual Support**
- **4 Languages**: English, Tamil (தமிழ்), Hindi (हिंदी), Telugu (తెలుగు)
- **Real-time Translation**: Seamless language switching
- **Demographic Awareness**: Student/Professional/Farmer/Senior Citizen modes
- **Cultural Adaptation**: Localized financial advice and examples

### 🎤 **Advanced Voice Interface**
- **Speech-to-Text (STT)**: Multilingual voice recognition
- **Text-to-Speech (TTS)**: Natural voice responses
- **Offline Capabilities**: Coqui TTS for offline voice processing
- **Voice Navigation**: Hands-free interaction for accessibility

### 🧠 **AI-Powered Intelligence**
- **RAG Integration**: Enhanced with RBI/SEBI documents
- **IBM Watsonx**: Enterprise-grade AI integration
- **Hugging Face Models**: Advanced multilingual transformers
- **Explainable AI**: Confidence scores and source attribution

### 👨‍🌾 **Farmer-Specific Tools**
- **Crop Loan Calculator**: Interest rates and eligibility
- **MSP Tracking**: Real-time Minimum Support Price alerts
- **Government Schemes**: PM-KISAN, PMFBY, subsidies
- **Weather Integration**: Financial impact of weather conditions
- **Agro-Insurance**: Comprehensive insurance calculators

### 💳 **Financial Services**
- **Credit Score Tracking**: CIBIL/Experian integration ready
- **Debt Management**: Restructuring and consolidation advice
- **Investment Portfolio**: Personalized recommendations
- **Tax Optimization**: Old vs New regime comparison
- **15+ Calculators**: SIP, EMI, Budget, Retirement, etc.

### 🛡️ **Security & Compliance**
- **AES-256 Encryption**: Secure data protection
- **GDPR/HIPAA Ready**: Privacy compliance framework
- **Data Retention**: Configurable storage periods
- **Biometric Support**: Authentication framework

### 🎮 **Gamification**
- **Points & Badges**: Achievement system
- **Financial Challenges**: Interactive learning
- **Progress Tracking**: Goal achievement monitoring
- **Community Features**: Peer-to-peer learning framework

## 🚀 **Quick Start**

### **Option 1: One-Click Launch (Recommended)**
```bash
python launch_complete_jarvisfi.py
```

### **Option 2: Manual Setup**
```bash
# Clone the repository
git clone https://github.com/ANASF1412/GenAI-JarvisFi-app.git
cd GenAI-JarvisFi-app

# Install dependencies
pip install -r requirements_complete.txt

# Run the application
streamlit run frontend/complete_jarvisfi_app.py
```

### **Option 3: Docker (Coming Soon)**
```bash
docker build -t jarvisfi .
docker run -p 8501:8501 jarvisfi
```

## 📁 **Project Structure**

```
GenAI-JarvisFi-app/
├── 🎯 launch_complete_jarvisfi.py    # Main launcher script
├── 📋 requirements_complete.txt      # Comprehensive dependencies
├── 🏗️ backend/                      # Backend services
│   ├── core_ai_engine.py            # AI engine with RAG
│   ├── financial_services.py        # Financial calculations
│   └── voice_processor.py           # Voice processing
├── 🎨 frontend/                     # Frontend applications
│   ├── complete_jarvisfi_app.py     # Main comprehensive app
│   ├── comprehensive_app.py         # Enhanced features
│   └── clean_app.py                 # Clean version
├── 📊 data/                         # Data files
├── 🧪 tests/                        # Test suites
├── 📚 docs/                         # Documentation
└── 🐳 docker/                       # Docker configurations
```

## 🌐 **Supported Languages**

| Language | Code | Status | Features |
|----------|------|--------|----------|
| English | `en` | ✅ Complete | All features |
| Tamil | `ta` | ✅ Complete | Full localization |
| Hindi | `hi` | ✅ Complete | Full localization |
| Telugu | `te` | ✅ Complete | Full localization |

## 🎯 **User Types & Features**

### 🎓 **Students**
- Small SIP recommendations (₹500-1000)
- Education loan guidance
- Budget planning for limited income
- Scholarship and grant information

### 💼 **Professionals**
- Tax optimization (80C deductions)
- Investment portfolio management
- Home loan planning
- Retirement corpus building

### 👨‍🌾 **Farmers**
- Crop loan calculators
- MSP price tracking
- Government scheme alerts
- Weather-based financial planning
- Agricultural insurance

### 👴 **Senior Citizens**
- Fixed deposit recommendations
- Healthcare expense planning
- Senior citizen schemes (SCSS)
- Conservative investment options

## 🧮 **Financial Calculators**

1. **SIP Calculator** - Systematic Investment Planning
2. **EMI Calculator** - Loan EMI calculations
3. **Tax Calculator** - Income tax optimization
4. **Retirement Calculator** - Retirement corpus planning
5. **Budget Planner** - 50/30/20 rule implementation
6. **Emergency Fund Calculator** - Emergency corpus planning
7. **Debt Payoff Calculator** - Debt elimination strategies
8. **Investment Growth Calculator** - Portfolio growth projections
9. **Crop Loan Calculator** - Agricultural finance
10. **Insurance Calculator** - Coverage planning
11. **Currency Converter** - Real-time exchange rates
12. **Goal Planning Calculator** - Financial goal tracking
13. **Credit Score Simulator** - Score improvement planning
14. **Mutual Fund Calculator** - Fund performance analysis
15. **Fixed Deposit Calculator** - FD returns calculation

## 🔧 **Technical Architecture**

### **Frontend**
- **Streamlit**: Modern web interface
- **Plotly**: Interactive visualizations
- **Responsive Design**: Mobile-first approach
- **Accessibility**: WCAG compliant

### **Backend**
- **FastAPI**: High-performance API framework
- **SQLAlchemy**: Database ORM
- **Redis**: Caching layer
- **Celery**: Background task processing

### **AI/ML Stack**
- **Transformers**: Hugging Face models
- **Sentence Transformers**: Multilingual embeddings
- **IBM Watsonx**: Enterprise AI platform
- **Coqui TTS**: Offline voice synthesis

### **Security**
- **Cryptography**: AES-256 encryption
- **OAuth 2.0**: Authentication framework
- **JWT**: Secure token management
- **Rate Limiting**: API protection

## 📊 **Performance Metrics**

- **Response Time**: <2 seconds average
- **Memory Usage**: <500MB (P99)
- **Uptime**: 99.9% target
- **Languages**: 4 supported
- **Features**: 50+ financial tools
- **User Types**: 6 specialized modes

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **How to Contribute**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Hugging Face** for multilingual AI models
- **IBM Watsonx** for enterprise AI platform
- **Streamlit** for the amazing web framework
- **RBI & SEBI** for financial guidelines and documentation
- **Open Source Community** for various libraries and tools

## 📞 **Support**

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/ANASF1412/GenAI-JarvisFi-app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ANASF1412/GenAI-JarvisFi-app/discussions)
- **Email**: support@jarvisfi.com

---

<div align="center">

**Made with ❤️ for the financial inclusion of everyone**

[🌐 Website](https://jarvisfi.com) • [📱 Demo](https://jarvisfi-demo.streamlit.app) • [📚 Docs](https://docs.jarvisfi.com) • [💬 Community](https://discord.gg/jarvisfi)

</div>
