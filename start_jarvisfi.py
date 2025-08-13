#!/usr/bin/env python3
"""
JarvisFi - Quick Start Script
Launch JarvisFi with all features
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_banner():
    """Print JarvisFi banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🤖 JarvisFi - Your AI-Powered Financial Genius       ║
    ║                    Comprehensive Edition v2.0               ║
    ║                                                              ║
    ║  ✨ Features:                                                ║
    ║  • 🌍 Multi-language Support (EN, TA, HI, TE)              ║
    ║  • 🤖 Advanced AI Integration                               ║
    ║  • 🎤 Voice Interface                                       ║
    ║  • 👨‍🌾 Farmer Tools                                        ║
    ║  • 💳 Credit Score Tracking                                ║
    ║  • 📈 Investment Portfolio                                  ║
    ║  • 🛡️ Enterprise Security                                   ║
    ║  • 🎮 Gamification                                          ║
    ║  • 🧮 15+ Calculators                                       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def install_basic_requirements():
    """Install basic requirements"""
    basic_packages = [
        'streamlit>=1.28.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'plotly>=5.17.0'
    ]
    
    try:
        logger.info("📦 Installing basic requirements...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install'
        ] + basic_packages, check=True, capture_output=True)
        logger.info("✅ Basic requirements installed")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install requirements: {e}")
        return False

def run_application():
    """Run the JarvisFi application"""
    print_banner()
    
    # Check for comprehensive app first
    comprehensive_app = Path(__file__).parent / 'frontend' / 'comprehensive_app.py'
    clean_app = Path(__file__).parent / 'frontend' / 'clean_app.py'
    basic_app = Path(__file__).parent / 'frontend' / 'app.py'
    
    app_to_run = None
    
    if comprehensive_app.exists():
        app_to_run = comprehensive_app
        logger.info("🚀 Starting Comprehensive JarvisFi...")
    elif clean_app.exists():
        app_to_run = clean_app
        logger.info("🚀 Starting Clean JarvisFi...")
    elif basic_app.exists():
        app_to_run = basic_app
        logger.info("🚀 Starting Basic JarvisFi...")
    else:
        logger.error("❌ No JarvisFi application found!")
        return False
    
    # Install basic requirements
    install_basic_requirements()
    
    # Run the application
    try:
        logger.info("🌐 Starting server on http://localhost:8501")
        logger.info("📱 Open your web browser and go to the URL above")
        logger.info("⏹️ Press Ctrl+C to stop the server")
        
        cmd = [
            sys.executable, '-m', 'streamlit', 'run',
            str(app_to_run),
            '--server.port', '8501',
            '--server.address', '0.0.0.0',
            '--browser.gatherUsageStats', 'false'
        ]
        
        subprocess.run(cmd, check=True)
        return True
        
    except KeyboardInterrupt:
        logger.info("⏹️ JarvisFi stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to start JarvisFi: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

if __name__ == '__main__':
    try:
        success = run_application()
        if success:
            logger.info("✅ JarvisFi session completed")
        else:
            logger.error("❌ JarvisFi failed to start")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("⏹️ Startup interrupted")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        sys.exit(1)
