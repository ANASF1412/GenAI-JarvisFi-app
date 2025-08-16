# 🔑 JarvisFi - API Keys and Models Configuration Report

## 📋 **OVERVIEW**

This document provides a comprehensive overview of all API keys, models, and important configuration keys used in the JarvisFi application.

---

## 🤖 **AI MODELS USED**

### **🔹 IBM WatsonX Foundation Models**
- **Primary Model**: `meta-llama/llama-2-70b-chat` (NOT Granite)
- **Location**: `api/services/ai_service.py` (lines 102-112)
- **Configuration**:
  ```python
  self.watsonx_model = Model(
      model_id="meta-llama/llama-2-70b-chat",
      params={
          "decoding_method": "greedy",
          "max_new_tokens": 500,
          "temperature": 0.7,
          "top_p": 0.9
      }
  )
  ```

### **🔹 Hugging Face Models**
- **Sentence Transformer**: `all-MiniLM-L6-v2`
- **Financial Classifier**: `ProsusAI/finbert`
- **Sentiment Analyzer**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Translation Models**:
  - English to Tamil: `Helsinki-NLP/opus-mt-en-mul`
  - English to Hindi: `Helsinki-NLP/opus-mt-en-hi`
  - English to Telugu: `Helsinki-NLP/opus-mt-en-mul`

### **🔹 Voice Processing Models**
- **TTS Model**: `tts_models/multilingual/multi-dataset/xtts_v2`
- **STT Model**: `openai/whisper-base`

### **🔹 OpenAI Models (Fallback)**
- **Default Model**: `gpt-3.5-turbo`
- **Usage**: Fallback when IBM Watson is unavailable

---

## 🔑 **API KEYS REQUIRED**

### **🔹 IBM Watson/WatsonX Keys**
```env
# IBM Watson Configuration
IBM_WATSON_API_KEY=your_watson_api_key_here
IBM_WATSON_URL=your_watson_url_here
IBM_WATSON_ASSISTANT_ID=your_assistant_id_here
IBM_WATSONX_PROJECT_ID=your_watsonx_project_id_here
IBM_WATSONX_API_KEY=your_watsonx_api_key_here
```
**Location**: `.env.comprehensive`, `api/core/config.py`

### **🔹 OpenAI Keys (Optional)**
```env
# OpenAI Configuration (Backup)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### **🔹 Hugging Face Keys (Optional)**
```env
# Hugging Face Configuration
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
HUGGINGFACE_MODEL_CACHE_DIR=./models/huggingface
```

### **🔹 Financial Data APIs**
```env
# Financial APIs
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
XE_CURRENCY_API_KEY=your_xe_currency_api_key_here
YAHOO_FINANCE_ENABLED=True
```

### **🔹 Credit Score APIs**
```env
# Credit Score APIs
CIBIL_API_KEY=your_cibil_api_key_here
CIBIL_API_URL=https://api.cibil.com/v1
EXPERIAN_API_KEY=your_experian_api_key_here
EXPERIAN_API_URL=https://api.experian.com/v1
```

### **🔹 Weather API (For Farmers)**
```env
# Weather API (for Farmers)
WEATHER_API_KEY=your_weather_api_key_here
WEATHER_API_URL=https://api.openweathermap.org/data/2.5
```

### **🔹 Geolocation APIs**
```env
# Geolocation
GEOLOCATION_API_KEY=your_geolocation_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### **🔹 OAuth Configuration**
```env
# OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
FACEBOOK_CLIENT_ID=your_facebook_client_id_here
FACEBOOK_CLIENT_SECRET=your_facebook_client_secret_here
```

---

## 🗂️ **CONFIGURATION FILES LOCATIONS**

### **🔹 Main Configuration Files**
1. **`api/core/config.py`** - Main configuration class with all settings
2. **`.env.comprehensive`** - Comprehensive environment variables template
3. **`.env.example`** - Basic environment variables template
4. **`.streamlit/secrets.toml.example`** - Streamlit secrets template

### **🔹 Model Cache Directories**
- **Hugging Face Models**: `./models/huggingface/`
- **Voice Cache**: `./cache/voice/`
- **Translation Cache**: In-memory with configurable size

---

## 🔐 **SECURITY KEYS**

### **🔹 Application Security**
```env
# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
ENCRYPTION_KEY=your_encryption_key_here
AES_KEY=your_aes_key_here
```

### **🔹 Database Configuration**
```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/jarvisfi
POSTGRES_DB=jarvisfi
POSTGRES_USER=jarvisfi_user
POSTGRES_PASSWORD=your_postgres_password_here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis Configuration
REDIS_URL=redis://:redis_password@localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password_here
REDIS_DB=0

# MongoDB Configuration
MONGODB_URL=mongodb://mongo_user:mongo_password@localhost:27017/jarvisfi_docs
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USERNAME=mongo_user
MONGODB_PASSWORD=mongo_password
MONGODB_DATABASE=jarvisfi_docs
```

---

## 📧 **COMMUNICATION APIS**

### **🔹 Email Configuration**
```env
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=noreply@jarvisfi.com
```

### **🔹 SMS Configuration**
```env
# SMS Configuration
SMS_API_KEY=your_sms_api_key_here
SMS_API_URL=your_sms_api_url_here
```

---

## 📊 **ANALYTICS KEYS**

### **🔹 Analytics Configuration**
```env
# Analytics
GOOGLE_ANALYTICS_ID=your_google_analytics_id_here
MIXPANEL_TOKEN=your_mixpanel_token_here
ANALYTICS_ENABLED=True
```

---

## ❌ **GRANITE MODEL STATUS**

### **🔍 Search Results:**
- **No IBM Granite models found** in the codebase
- **Primary model used**: `meta-llama/llama-2-70b-chat` via IBM WatsonX
- **No references to**: `granite`, `Granite`, `granite-13b`, `granite-7b`

### **🤖 Current AI Architecture:**
1. **Primary**: IBM WatsonX with Llama-2-70B model
2. **Secondary**: Hugging Face transformers for specific tasks
3. **Fallback**: OpenAI GPT-3.5-turbo
4. **Local**: Rule-based responses when AI services unavailable

---

## 🚀 **SETUP INSTRUCTIONS**

### **🔹 Required Steps:**
1. **Copy environment template**:
   ```bash
   cp .env.comprehensive .env
   ```

2. **Fill in your API keys** in the `.env` file

3. **For Streamlit secrets**:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements_comprehensive.txt
   ```

### **🔹 Minimum Required Keys for Basic Functionality:**
- No API keys required for basic functionality
- Application works with fallback responses
- Enhanced features require respective API keys

### **🔹 Recommended Keys for Full Functionality:**
- **IBM Watson API keys** for advanced AI features
- **Weather API key** for farmer tools
- **Financial API keys** for real-time data

---

## 🔧 **CONFIGURATION PRIORITY**

### **🔹 Configuration Loading Order:**
1. Environment variables (`.env` file)
2. System environment variables
3. Default values in `config.py`

### **🔹 Model Loading Priority:**
1. IBM WatsonX (if configured)
2. Hugging Face models (if available)
3. OpenAI (if configured)
4. Rule-based fallbacks

---

## 📝 **IMPORTANT NOTES**

### **✅ Security Best Practices:**
- Never commit `.env` files to version control
- Use strong, unique keys for production
- Rotate API keys regularly
- Use environment-specific configurations

### **✅ Model Performance:**
- Hugging Face models cached locally for faster inference
- Translation models support 4 languages (EN, TA, HI, TE)
- Voice models support multilingual TTS/STT

### **✅ Fallback Strategy:**
- Application gracefully degrades when APIs unavailable
- Local models used when possible
- Rule-based responses as final fallback

---

## 🎯 **SUMMARY**

**JarvisFi uses:**
- ❌ **No IBM Granite models**
- ✅ **IBM WatsonX with Llama-2-70B** as primary AI
- ✅ **Multiple Hugging Face models** for specialized tasks
- ✅ **Comprehensive API integration** for financial data
- ✅ **Robust fallback mechanisms** for reliability

**All configuration is centralized in `api/core/config.py` with environment variable support.**
