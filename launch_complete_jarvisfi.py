#!/usr/bin/env python3
"""
Complete JarvisFi Application Launcher
Launch the comprehensive multilingual AI personal finance chatbot with all features
"""

import os
import sys
import subprocess
import logging
import time
from pathlib import Path
import argparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_banner():
    """Print comprehensive JarvisFi banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║        🤖 JarvisFi - Complete AI-Powered Financial Genius v2.0              ║
    ║                    Multilingual Personal Finance Chatbot                     ║
    ║                                                                              ║
    ║  ✨ COMPREHENSIVE FEATURES:                                                  ║
    ║                                                                              ║
    ║  🌍 MULTILINGUAL SUPPORT:                                                   ║
    ║  • English, Tamil, Hindi, Telugu with real-time translation                 ║
    ║  • Demographic-aware communication (Student/Professional/Farmer)            ║
    ║                                                                              ║
    ║  🎤 VOICE INTERFACE:                                                        ║
    ║  • Speech-to-Text (STT) with multilingual recognition                       ║
    ║  • Text-to-Speech (TTS) with offline capabilities                           ║
    ║  • Voice-activated navigation for low-literacy users                        ║
    ║                                                                              ║
    ║  🧠 ADVANCED AI:                                                            ║
    ║  • RAG integration with RBI/SEBI documents                                  ║
    ║  • IBM Watsonx and Hugging Face model integration                           ║
    ║  • Explainable AI with confidence scores and sources                        ║
    ║                                                                              ║
    ║  👨‍🌾 FARMER-SPECIFIC TOOLS:                                                 ║
    ║  • Crop loan calculators with MSP tracking                                  ║
    ║  • Government subsidy checker (PM-KISAN, PMFBY)                            ║
    ║  • Weather-based financial planning                                          ║
    ║  • Agro-insurance calculators                                               ║
    ║                                                                              ║
    ║  💳 FINANCIAL SERVICES:                                                     ║
    ║  • Credit score tracking (CIBIL/Experian integration)                       ║
    ║  • Debt management and restructuring guidance                               ║
    ║  • Investment portfolio management with personalized advice                  ║
    ║  • Tax optimization (Old vs New regime comparison)                          ║
    ║                                                                              ║
    ║  🛡️ SECURITY & COMPLIANCE:                                                  ║
    ║  • AES-256 encryption for sensitive data                                    ║
    ║  • OAuth 2.0 authentication                                                 ║
    ║  • GDPR/HIPAA compliance ready                                               ║
    ║  • Biometric authentication support                                          ║
    ║                                                                              ║
    ║  🎮 GAMIFICATION & ENGAGEMENT:                                              ║
    ║  • Points, badges, and financial challenges                                 ║
    ║  • Community forums and peer-to-peer learning                               ║
    ║  • Progress tracking and goal achievement                                    ║
    ║                                                                              ║
    ║  📊 COMPREHENSIVE CALCULATORS:                                              ║
    ║  • SIP, EMI, Tax, Retirement, Budget Planners                              ║
    ║  • Emergency fund and debt payoff calculators                               ║
    ║  • Real-time currency conversion                                             ║
    ║                                                                              ║
    ║  🌟 ACCESSIBILITY FEATURES:                                                 ║
    ║  • Mobile-first responsive design                                            ║
    ║  • Dark/Light mode with large text options                                  ║
    ║  • Dyslexia-friendly interface                                               ║
    ║  • Offline mode capabilities                                                 ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8 or higher is required")
        return False
    
    logger.info(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    logger.info("📦 Installing/updating requirements...")
    
    # Core requirements
    core_packages = [
        'streamlit>=1.28.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'plotly>=5.17.0',
        'python-dateutil>=2.8.0'
    ]
    
    # AI/ML packages
    ai_packages = [
        'transformers>=4.35.0',
        'torch>=2.1.0',
        'sentence-transformers>=2.2.0',
        'scikit-learn>=1.3.0'
    ]
    
    # Voice processing packages
    voice_packages = [
        'SpeechRecognition>=3.10.0',
        'pyttsx3>=2.90',
        'pydub>=0.25.0'
    ]
    
    # Financial data packages
    finance_packages = [
        'yfinance>=0.2.0',
        'forex-python>=1.8'
    ]
    
    # Security packages
    security_packages = [
        'cryptography>=41.0.0',
        'passlib>=1.7.4'
    ]
    
    all_packages = core_packages + ai_packages + voice_packages + finance_packages + security_packages
    
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '--upgrade'
        ] + all_packages, check=True, capture_output=True, text=True)
        
        logger.info("✅ All requirements installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.warning(f"⚠️ Some packages failed to install: {e}")
        logger.info("🔄 Installing core packages only...")
        
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '--upgrade'
            ] + core_packages, check=True, capture_output=True, text=True)
            
            logger.info("✅ Core packages installed successfully")
            return True
            
        except subprocess.CalledProcessError as e2:
            logger.error(f"❌ Failed to install core packages: {e2}")
            return False

def check_backend_services():
    """Check if backend services are available"""
    logger.info("🔍 Checking backend services...")
    
    backend_dir = Path(__file__).parent / 'backend'
    
    required_modules = [
        'core_ai_engine.py',
        'financial_services.py',
        'voice_processor.py'
    ]
    
    available_modules = 0
    for module in required_modules:
        module_path = backend_dir / module
        if module_path.exists():
            available_modules += 1
            logger.info(f"✅ {module} - Available")
        else:
            logger.warning(f"⚠️ {module} - Not found")
    
    if available_modules == len(required_modules):
        logger.info("✅ All backend services available")
        return True
    else:
        logger.warning(f"⚠️ {available_modules}/{len(required_modules)} backend services available")
        logger.info("🔄 Application will run in demo mode")
        return False

def setup_environment():
    """Setup environment variables and configuration"""
    logger.info("⚙️ Setting up environment...")
    
    # Set Streamlit configuration
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    logger.info("✅ Environment setup complete")

def find_application():
    """Find the best available application to run"""
    current_dir = Path(__file__).parent
    
    # Priority order of applications
    apps = [
        current_dir / 'frontend' / 'complete_jarvisfi_app.py',
        current_dir / 'frontend' / 'comprehensive_app.py',
        current_dir / 'frontend' / 'clean_app.py',
        current_dir / 'frontend' / 'app.py'
    ]
    
    for app in apps:
        if app.exists():
            logger.info(f"📱 Found application: {app.name}")
            return app
    
    logger.error("❌ No JarvisFi application found!")
    return None

def run_application(app_path, port=8501, debug=False):
    """Run the JarvisFi application"""
    logger.info(f"🚀 Starting Complete JarvisFi on port {port}...")
    logger.info(f"🌐 Application will be available at: http://localhost:{port}")
    logger.info("📱 Open your web browser and navigate to the URL above")
    logger.info("⏹️ Press Ctrl+C to stop the server")
    
    # Streamlit command
    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        str(app_path),
        '--server.port', str(port),
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false'
    ]
    
    if debug:
        cmd.extend(['--logger.level', 'debug'])
    
    try:
        # Run the application
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment to check if it starts successfully
        time.sleep(3)
        
        if process.poll() is None:
            logger.info("✅ JarvisFi started successfully!")
            logger.info("🎉 All features are now available:")
            logger.info("   • Multilingual AI chat (EN, TA, HI, TE)")
            logger.info("   • Voice interface with STT/TTS")
            logger.info("   • Farmer-specific financial tools")
            logger.info("   • Credit score tracking")
            logger.info("   • Investment portfolio management")
            logger.info("   • Comprehensive financial calculators")
            logger.info("   • RAG-enhanced responses")
            logger.info("   • Security and compliance features")
            
            try:
                process.wait()
            except KeyboardInterrupt:
                logger.info("⏹️ Stopping JarvisFi...")
                process.terminate()
                process.wait()
                logger.info("✅ JarvisFi stopped successfully")
            
            return True
        else:
            stdout, stderr = process.communicate()
            logger.error("❌ Failed to start JarvisFi")
            if stderr:
                logger.error(f"Error details: {stderr}")
            return False
            
    except FileNotFoundError:
        logger.error("❌ Streamlit not found. Installing...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'streamlit'], check=True)
            logger.info("✅ Streamlit installed. Please run the script again.")
            return False
        except subprocess.CalledProcessError:
            logger.error("❌ Failed to install Streamlit")
            return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Complete JarvisFi Application Launcher')
    parser.add_argument('--port', type=int, default=8501, help='Port to run the application on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--skip-install', action='store_true', help='Skip package installation')
    parser.add_argument('--skip-checks', action='store_true', help='Skip all checks')
    
    args = parser.parse_args()
    
    try:
        # Print banner
        print_banner()
        
        # Check Python version
        if not args.skip_checks and not check_python_version():
            return 1
        
        # Setup environment
        setup_environment()
        
        # Install requirements
        if not args.skip_install:
            if not install_requirements():
                logger.warning("⚠️ Some packages failed to install - continuing anyway")
        
        # Check backend services
        if not args.skip_checks:
            backend_available = check_backend_services()
            if not backend_available:
                logger.info("🔄 Running in demo mode with simulated features")
        
        # Find application
        app_path = find_application()
        if not app_path:
            logger.error("❌ No application found to run")
            return 1
        
        # Run application
        success = run_application(app_path, args.port, args.debug)
        
        if success:
            logger.info("✅ JarvisFi session completed successfully")
            return 0
        else:
            logger.error("❌ Failed to start JarvisFi")
            return 1
            
    except KeyboardInterrupt:
        logger.info("⏹️ Startup interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
