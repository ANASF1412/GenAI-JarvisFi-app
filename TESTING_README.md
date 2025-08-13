# 🧪 Comprehensive Testing Guide for Personal Finance Chatbot

This guide provides complete testing instructions for verifying all menus, tasks, and the English-to-Tamil translation model in the Personal Finance Chatbot application.

## 🎯 Testing Objectives

**Primary Goal**: Verify all UI menus, functional tasks, and the English-to-Tamil translation model work correctly with comprehensive error handling.

## 📋 Dependencies for Testing

### Required Python Packages
```txt
# Core Testing Dependencies
pytest>=7.4.0
pytest-mock>=3.11.0
psutil>=5.9.0

# Application Dependencies
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
transformers>=4.30.0
torch>=2.0.0
sentence-transformers>=2.2.0
huggingface-hub>=0.16.0

# Language Processing
spacy>=3.6.0
nltk>=3.8.0
googletrans>=4.0.0

# Voice Interface
SpeechRecognition>=3.10.0
pyttsx3>=2.90

# Database & Security
pymongo>=4.4.0
cryptography>=41.0.0

# Additional Utilities
requests>=2.31.0
python-dotenv>=1.0.0
```

### System Dependencies

#### Windows
```bash
# Install Python 3.9+ from python.org
# Install Git from git-scm.com
# For PyAudio (voice features):
pip install pipwin
pipwin install pyaudio
```

#### macOS
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.9 portaudio git
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.9 python3-pip python3-dev portaudio19-dev git build-essential
```

## 🚀 Quick Setup for Testing

### Automated Setup (Recommended)
```bash
# Clone repository
git clone <your-repo-url>
cd personal-finance-chatbot

# Run automated setup and tests
python setup_and_test.py
```

### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download language models
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 🧪 Test Execution

### 1. Run Complete Test Suite
```bash
# Run all tests with detailed reporting
python run_tests.py

# Quick essential tests only
python run_tests.py --quick

# Skip dependency checks
python run_tests.py --skip-deps

# Skip Streamlit app startup test
python run_tests.py --skip-app
```

### 2. Individual Test Categories

#### Menu Validation Tests
```bash
python -m pytest tests/test_ui_components.py::TestStreamlitUIComponents::test_streamlit_tabs_navigation -v
python -m pytest tests/test_ui_components.py::TestStreamlitUIComponents::test_language_selection_menu -v
```

#### Translation Model Tests
```bash
# Run all translation tests
python -m pytest tests/test_translation_model.py -v

# Specific translation test categories
python -m pytest tests/test_translation_model.py::TestEnglishToTamilModel::test_basic_greetings -v
python -m pytest tests/test_translation_model.py::TestEnglishToTamilModel::test_financial_terms -v
python -m pytest tests/test_translation_model.py::TestEnglishToTamilModel::test_complete_sentences -v
```

#### Performance Tests
```bash
python -m pytest tests/test_translation_model.py::TestEnglishToTamilModel::test_translation_performance -v
python -m pytest tests/comprehensive_test_suite.py::TestPerformanceAndErrorHandling -v
```

### 3. Comprehensive Test Suite
```bash
# Run the complete comprehensive test suite
python tests/comprehensive_test_suite.py
```

## 📊 Test Categories & Expected Results

### 1. **Menu Validation Tests** ✅

#### Navigation Menu Tests
- **Test**: Click all top-level tabs
- **Expected Tabs**: 
  - English: `["💬 Chat", "📊 Dashboard", "💰 Budget", "📈 Investment", "💱 Currency", "🧠 AI Insights", "📈 Reports", "💡 Tips"]`
  - Tamil: `["💬 அரட்டை", "📊 டாஷ்போர்டு", "💰 பட்ஜெட்", "📈 முதலீடு", "💱 நாணயம்", "🧠 AI நுண்ணறிவு", "📈 அறிக்கைகள்", "💡 குறிப்புகள்"]`
- **Success Criteria**: All tabs accessible, no crashes

#### Language Selection Menu Tests
- **Test**: Switch between English/Tamil
- **Expected**: Instant UI language change, all labels translate
- **Success Criteria**: Language switching works without page reload

### 2. **Translation Model Tests** 🔤

#### Basic Translation Cases
```python
test_cases = [
    ("Hello", "வணக்கம்"),
    ("Good morning", "காலை வணக்கம்"),
    ("How are you?", "நீங்கள் எப்படி இருக்கிறீர்கள்?"),
    ("hard work never fails", "கடின உழைப்பு ஒருபோதும் தோல்வியடையாது"),
    ("Success comes to those who work hard", "வெற்றி கடினமாக உழைப்பவர்களுக்கு கிடைக்கும்")
]
```
- **Success Criteria**: ≥80% accuracy, Tamil characters present

#### Financial Terms Translation
```python
financial_terms = [
    ("money", "பணம்"), ("bank", "வங்கி"), ("investment", "முதலீடு"),
    ("savings", "சேமிப்பு"), ("budget", "பட்ஜெட்"), ("loan", "கடன்")
]
```
- **Success Criteria**: ≥70% accuracy for financial terminology

#### Edge Cases
```python
edge_cases = [
    ("42", "நாற்பத்தி இரண்டு"),  # Numbers
    ("ATM machine", "ATM இயந்திரம்"),  # Mixed language
    ("@#$%", "@#$%"),  # Special characters (graceful handling)
    ("", ""),  # Empty string
    ("A" * 500, "Long text handling")  # Very long text
]
```
- **Success Criteria**: No crashes, graceful error handling

### 3. **Performance & Error Handling Tests** ⚡

#### Performance Benchmarks
- **Response Time**: <5s for 50-word input
- **Memory Usage**: <1GB during translation
- **Concurrent Translations**: Handle 5 simultaneous requests
- **Success Criteria**: All benchmarks met

#### Error Handling
```python
error_test_cases = [
    "",  # Empty input
    " " * 100,  # Whitespace only
    "🚀🎉💰" * 50,  # Emoji overload
    None,  # Null input
]
```
- **Success Criteria**: Graceful error messages, no crashes

### 4. **UI Integration Tests** 🖥️

#### Session State Tests
```python
required_session_vars = [
    'user_profile', 'chat_history', 'dark_mode',
    'voice_listening', 'voice_speaking', 'ai_accuracy_enabled'
]
```
- **Success Criteria**: All variables initialized correctly

#### Chat Functionality Tests
```python
test_messages = [
    "How can I save money?",
    "What is a budget?",
    "Help me with investments",
    "பணம் எப்படி சேமிக்கலாம்?"
]
```
- **Success Criteria**: ≥75% response success rate

### 5. **File Operations Tests** 📁

#### Data Persistence Tests
- **JSON Export/Import**: User profile and chat history
- **Text File Operations**: Tamil character preservation
- **Configuration Files**: .env file handling
- **Success Criteria**: Data integrity maintained

## 📈 Test Reports & Monitoring

### Automated Report Generation
```python
# Test reports are automatically generated:
test_report.json           # Comprehensive test results
setup_report.json         # Setup process log
comprehensive_test_report.json  # Detailed analysis
```

### Report Structure
```json
{
  "timestamp": "2024-01-01T10:00:00",
  "test_summary": {
    "total_test_categories": 5,
    "passed_categories": 4,
    "failed_categories": 1
  },
  "translation_accuracy": 85.5,
  "ui_components_tested": 15,
  "performance_metrics": {
    "avg_translation_time": 1.2,
    "memory_usage_mb": 450
  },
  "failures": [],
  "recommendations": []
}
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Translation Model Not Loading
```bash
# Solution: Install transformers and torch
pip install transformers torch
# Download model manually
python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; AutoTokenizer.from_pretrained('suriya7/English-to-Tamil'); AutoModelForSeq2SeqLM.from_pretrained('suriya7/English-to-Tamil')"
```

#### Streamlit App Won't Start
```bash
# Check port availability
netstat -an | grep 8501
# Use different port
streamlit run frontend/simple_app.py --server.port 8502
```

#### Voice Interface Issues
```bash
# Install audio dependencies
# Windows:
pip install pipwin && pipwin install pyaudio
# macOS:
brew install portaudio && pip install pyaudio
# Linux:
sudo apt install portaudio19-dev && pip install pyaudio
```

#### Memory Issues During Testing
```bash
# Reduce test scope
python run_tests.py --quick
# Or run individual test categories
python -m pytest tests/test_ui_components.py -v
```

## 🎯 Success Criteria Summary

| Test Category | Success Threshold | Key Metrics |
|---------------|------------------|-------------|
| Menu Navigation | 100% | All tabs accessible |
| Language Switching | 100% | Instant translation |
| Basic Translation | ≥80% accuracy | Tamil characters present |
| Financial Terms | ≥70% accuracy | Domain-specific terms |
| Edge Cases | 100% | No crashes |
| Performance | <5s response | <1GB memory |
| UI Integration | ≥75% | Session state intact |
| File Operations | 100% | Data integrity |

## 📞 Support & Debugging

### Debug Mode
```bash
# Enable debug logging
export DEBUG=True
python run_tests.py

# Verbose pytest output
python -m pytest tests/ -v -s --tb=long
```

### Log Files
- `setup_report.json`: Setup process details
- `test_report.json`: Test execution results
- `streamlit.log`: Application runtime logs

### Getting Help
1. Check test reports for specific error details
2. Verify all dependencies are installed correctly
3. Ensure .env file is properly configured
4. Test with minimal configuration first

---

**🎉 Ready to Test!** Run `python setup_and_test.py` to get started with automated setup and comprehensive testing.
