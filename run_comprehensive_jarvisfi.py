#!/usr/bin/env python3
"""
JarvisFi - Comprehensive Application Launcher
Launch the complete JarvisFi application with all advanced features
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
    """Print JarvisFi banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🤖 JarvisFi - Your AI-Powered Financial Genius       ║
    ║                    Comprehensive Edition v2.0               ║
    ║                                                              ║
    ║  ✨ Features:                                                ║
    ║  • 🌍 Multi-language Support (EN, TA, HI, TE)              ║
    ║  • 🤖 Advanced AI Integration (IBM Watson + Hugging Face)   ║
    ║  • 🎤 Voice Interface with Offline Processing              ║
    ║  • 👨‍🌾 Specialized Farmer Tools                            ║
    ║  • 💳 Credit Score Tracking                                ║
    ║  • 📈 Investment Portfolio Management                       ║
    ║  • 🛡️ Enterprise-Grade Security                            ║
    ║  • 🎮 Gamification & Community Features                    ║
    ║  • 🧮 15+ Financial Calculators                            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_dependencies():
    """Check if required dependencies are installed"""
    logger.info("🔍 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            logger.error(f"❌ {package} - Missing")
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.info("Installing missing packages...")
        
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages, check=True)
            logger.info("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install dependencies: {e}")
            return False
    
    return True


def check_backend_services():
    """Check if backend services are available"""
    logger.info("🔍 Checking backend services...")
    
    backend_path = Path(__file__).parent / 'backend'
    
    if not backend_path.exists():
        logger.warning("⚠️ Backend directory not found - Some features may be limited")
        return False
    
    required_modules = [
        'watson_integration.py',
        'language_support.py',
        'voice_interface.py',
        'user_profile_manager.py'
    ]
    
    available_modules = 0
    for module in required_modules:
        if (backend_path / module).exists():
            available_modules += 1
            logger.info(f"✅ {module} - Available")
        else:
            logger.warning(f"⚠️ {module} - Not found")
    
    if available_modules == len(required_modules):
        logger.info("✅ All backend services available")
        return True
    else:
        logger.warning(f"⚠️ {available_modules}/{len(required_modules)} backend services available")
        return False


def setup_environment():
    """Setup environment variables and paths"""
    logger.info("⚙️ Setting up environment...")
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    # Set environment variables for Streamlit
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'
    
    logger.info("✅ Environment setup complete")


def run_comprehensive_app(port=8501, debug=False):
    """Run the comprehensive JarvisFi application"""
    logger.info("🚀 Starting JarvisFi Comprehensive Edition...")
    
    # Path to the comprehensive app
    app_path = Path(__file__).parent / 'frontend' / 'comprehensive_app.py'
    
    if not app_path.exists():
        logger.error(f"❌ Application file not found: {app_path}")
        return False
    
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
        logger.info(f"🌐 Starting server on http://localhost:{port}")
        logger.info("📱 Access JarvisFi in your web browser")
        logger.info("⏹️ Press Ctrl+C to stop the server")
        
        # Run the application
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        logger.info("⏹️ Application stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to start application: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False


def run_fallback_app(port=8501):
    """Run the fallback application if comprehensive app fails"""
    logger.info("🔄 Starting fallback application...")
    
    # Try the clean app first
    fallback_apps = [
        Path(__file__).parent / 'frontend' / 'clean_app.py',
        Path(__file__).parent / 'frontend' / 'app.py'
    ]
    
    for app_path in fallback_apps:
        if app_path.exists():
            logger.info(f"📱 Using fallback app: {app_path.name}")
            
            cmd = [
                sys.executable, '-m', 'streamlit', 'run',
                str(app_path),
                '--server.port', str(port),
                '--server.address', '0.0.0.0'
            ]
            
            try:
                subprocess.run(cmd, check=True)
                return True
            except KeyboardInterrupt:
                logger.info("⏹️ Fallback application stopped by user")
                return True
            except Exception as e:
                logger.error(f"❌ Fallback app failed: {e}")
                continue
    
    logger.error("❌ No working application found")
    return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='JarvisFi Comprehensive Application Launcher')
    parser.add_argument('--port', type=int, default=8501, help='Port to run the application on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--fallback', action='store_true', help='Force use fallback application')
    parser.add_argument('--skip-checks', action='store_true', help='Skip dependency checks')
    
    args = parser.parse_args()
    
    try:
        # Print banner
        print_banner()
        
        # Setup environment
        setup_environment()
        
        # Check dependencies unless skipped
        if not args.skip_checks:
            if not check_dependencies():
                logger.error("❌ Dependency check failed")
                return 1
            
            # Check backend services
            backend_available = check_backend_services()
            if not backend_available:
                logger.warning("⚠️ Some backend services unavailable - Limited functionality")
        
        # Run application
        if args.fallback:
            logger.info("🔄 Using fallback application as requested")
            success = run_fallback_app(args.port)
        else:
            logger.info("🚀 Attempting to run comprehensive application")
            success = run_comprehensive_app(args.port, args.debug)
            
            if not success:
                logger.warning("⚠️ Comprehensive app failed, trying fallback...")
                success = run_fallback_app(args.port)
        
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
