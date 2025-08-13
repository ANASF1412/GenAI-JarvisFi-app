# 🤖 JarvisFi - Your AI-Powered Financial Genius

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](docker-compose-comprehensive.yml)

## 🌟 Overview

JarvisFi is a comprehensive, multilingual AI-powered personal finance chatbot designed specifically for Indian users. It provides personalized financial guidance, supports multiple languages (English, Tamil, Hindi, Telugu), and includes specialized tools for different user types including farmers, students, professionals, and senior citizens.

### ✨ Key Features

#### 🤖 **AI-Powered Financial Advice**
- Personalized financial guidance using IBM Watson and Hugging Face models
- Context-aware responses based on user profile and financial situation
- Explainable AI with confidence scores and source citations
- RAG integration with RBI/SEBI documents for accurate information

#### 🌐 **Multilingual Support**
- **4 Languages:** English, Tamil (தமிழ்), Hindi (हिंदी), Telugu (తెలుగు)
- Real-time translation using advanced NLP models
- Cultural adaptation for different regions
- Voice interface in multiple languages

#### 🎤 **Voice Interface**
- Speech-to-Text (STT) for voice input
- Text-to-Speech (TTS) for audio responses
- Offline voice processing using Coqui AI
- Voice-activated navigation for accessibility

#### 👥 **User-Centric Design**
- **5 User Types:** Student, Professional, Farmer, Senior Citizen, Beginner/Intermediate
- Demographic-aware communication styles
- Personalized dashboards and recommendations
- Accessibility features for all users

#### 🧮 **Comprehensive Financial Tools**
- Budget calculators and expense tracking
- Investment planning and SIP calculators
- Tax planning and optimization tools
- Credit score tracking (CIBIL/Experian integration)
- Debt management and restructuring guidance

#### 👨‍🌾 **Farmer-Specific Features**
- Crop loan calculators
- MSP (Minimum Support Price) alerts
- Government subsidy information
- Weather-based financial planning
- Agro-insurance calculators

#### 🔒 **Enterprise-Grade Security**
- AES-256 encryption for sensitive data
- OAuth 2.0 authentication
- GDPR and HIPAA compliance
- Biometric authentication support
- Fraud detection and prevention

#### 🎮 **Gamification & Engagement**
- Points and badges system
- Financial literacy challenges
- Progress tracking and achievements
- Community forums and peer learning

## 🏗️ Architecture

### **Modular MVP Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │   FastAPI API   │    │   AI Services   │
│   (Streamlit)   │◄──►│   (Backend)     │◄──►│  (IBM Watson)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Redis       │    │   MongoDB       │
│   (Main DB)     │    │    (Cache)      │    │  (Documents)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Technology Stack**

#### **Backend**
- **FastAPI** - High-performance API framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Primary database
- **Redis** - Caching and session management
- **MongoDB** - Document storage for RAG
- **Celery** - Background task processing

#### **AI/ML**
- **IBM Watson** - Primary AI service
- **Hugging Face Transformers** - NLP models
- **Sentence Transformers** - Embeddings
- **Coqui TTS** - Offline text-to-speech
- **OpenAI Whisper** - Speech recognition

#### **Frontend**
- **Streamlit** - Interactive web interface
- **Plotly** - Interactive charts and visualizations
- **Custom CSS** - Responsive design
- **Progressive Web App** - Mobile-first approach

#### **Infrastructure**
- **Docker** - Containerization
- **Nginx** - Reverse proxy and load balancing
- **Prometheus** - Monitoring and metrics
- **Grafana** - Dashboards and alerting

## 🚀 Quick Start

### **Prerequisites**
- Python 3.9+
- Docker and Docker Compose
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space

### **1. Clone Repository**
```bash
git clone https://github.com/your-org/jarvisfi.git
cd jarvisfi
```

### **2. Environment Setup**
```bash
# Copy environment template
cp .env.comprehensive .env

# Edit environment variables
nano .env
```

### **3. Docker Deployment (Recommended)**
```bash
# Start all services
docker-compose -f docker-compose-comprehensive.yml up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### **4. Manual Installation**
```bash
# Install dependencies
pip install -r requirements_comprehensive.txt

# Setup database
python scripts/setup.py

# Start backend
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start frontend (new terminal)
cd ui
streamlit run main_app.py --server.port 8501
```

### **5. Access Application**
- **Frontend:** http://localhost:8501
- **API Documentation:** http://localhost:8000/docs
- **Monitoring:** http://localhost:5555 (Flower)

## 📱 Usage Guide

### **Getting Started**
1. **Profile Setup:** Complete your financial profile
2. **Language Selection:** Choose your preferred language
3. **User Type:** Select your category (Student/Professional/Farmer/etc.)
4. **Financial Goals:** Set your objectives

### **Core Features**

#### **💬 Chat Interface**
- Ask questions in natural language
- Get personalized financial advice
- Voice input/output support
- Multi-turn conversations

#### **📊 Dashboard**
- Personalized financial overview
- Income/expense tracking
- Investment portfolio summary
- Goal progress monitoring

#### **🧮 Financial Calculators**
- **SIP Calculator:** Plan systematic investments
- **Budget Planner:** Track income and expenses
- **Loan Calculator:** EMI and interest calculations
- **Tax Calculator:** Optimize tax planning
- **Retirement Planner:** Long-term financial planning

#### **👨‍🌾 Farmer Tools**
- **Crop Loan Calculator:** Agricultural financing
- **MSP Tracker:** Market price monitoring
- **Subsidy Checker:** Government scheme eligibility
- **Weather Integration:** Climate-based planning

### **Voice Commands**
- "Hey JarvisFi, what's my budget status?"
- "Calculate SIP for ₹5000 monthly"
- "Show me tax-saving options"
- "What are the best mutual funds?"

## 🔧 Configuration

### **Environment Variables**
Key configuration options in `.env`:

```bash
# Application
APP_NAME=JarvisFi
DEBUG=False
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/jarvisfi
REDIS_URL=redis://localhost:6379/0
MONGODB_URL=mongodb://localhost:27017/jarvisfi_docs

# AI Services
IBM_WATSON_API_KEY=your_watson_key
HUGGINGFACE_API_KEY=your_hf_key
OPENAI_API_KEY=your_openai_key

# External APIs
CIBIL_API_KEY=your_cibil_key
ALPHA_VANTAGE_API_KEY=your_av_key
WEATHER_API_KEY=your_weather_key

# Security
SECRET_KEY=your_secret_key
AES_KEY=your_aes_key
JWT_SECRET_KEY=your_jwt_key

# Features
VOICE_INTERFACE_ENABLED=True
MULTILINGUAL_ENABLED=True
FARMER_TOOLS_ENABLED=True
COMMUNITY_FORUM_ENABLED=True
```

### **Language Configuration**
Supported languages and models:
- **English (en):** Primary language
- **Tamil (ta):** Helsinki-NLP/opus-mt-en-mul
- **Hindi (hi):** Helsinki-NLP/opus-mt-en-hi  
- **Telugu (te):** Helsinki-NLP/opus-mt-en-mul

## 🧪 Testing

### **Run Test Suite**
```bash
# Unit tests
pytest api/tests/ -v

# Integration tests
pytest tests/test_integration.py -v

# Frontend tests
pytest ui/tests/ -v

# Performance tests
pytest tests/test_performance.py -v

# Security tests
pytest tests/test_security.py -v
```

### **Test Coverage**
```bash
# Generate coverage report
pytest --cov=api --cov=ui --cov-report=html

# View coverage
open htmlcov/index.html
```

## 📊 Monitoring & Performance

### **Key Metrics**
- **Response Time:** <2s (P99)
- **Memory Usage:** <500MB
- **Uptime:** 99.9%
- **API Rate Limit:** 1000 requests/hour/user

### **Monitoring Stack**
- **Prometheus:** Metrics collection
- **Grafana:** Visualization and alerting
- **Flower:** Celery task monitoring
- **Custom Dashboards:** Business metrics

### **Performance Optimization**
- Redis caching for frequent queries
- Database query optimization
- CDN for static assets
- Horizontal scaling support

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run linting
black . && flake8 . && mypy .

# Run tests before committing
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/your-org/jarvisfi/issues)
- **Discussions:** [GitHub Discussions](https://github.com/your-org/jarvisfi/discussions)
- **Email:** support@jarvisfi.com

## 🗺️ Roadmap

### **Phase 1 (Current)**
- ✅ Core chat interface
- ✅ Multilingual support
- ✅ Basic financial calculators
- ✅ User profile management

### **Phase 2 (Q2 2024)**
- 🔄 Advanced AI integration
- 🔄 Voice interface enhancement
- 🔄 Mobile app development
- 🔄 Community features

### **Phase 3 (Q3 2024)**
- 📋 Advanced farmer tools
- 📋 Credit score integration
- 📋 Investment portfolio tracking
- 📋 Regulatory compliance tools

### **Phase 4 (Q4 2024)**
- 📋 Blockchain integration
- 📋 Advanced analytics
- 📋 Enterprise features
- 📋 International expansion

## 🙏 Acknowledgments

- **IBM Watson** for AI capabilities
- **Hugging Face** for NLP models
- **Streamlit** for rapid UI development
- **FastAPI** for high-performance backend
- **Open Source Community** for various libraries and tools

---

**Made with ❤️ for the Indian financial ecosystem**

*JarvisFi - Empowering financial literacy through AI*
