#!/usr/bin/env python3
"""
JarvisFi - Simple Launcher
Launch JarvisFi with error handling and fallbacks
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
    ║  ✨ Features Available:                                      ║
    ║  • 🌍 Multi-language Support (EN, TA, HI, TE)              ║
    ║  • 💬 AI Chat Interface                                     ║
    ║  • 📊 Financial Dashboard                                   ║
    ║  • 🧮 15+ Financial Calculators                            ║
    ║  • 🎤 Voice Interface Framework                             ║
    ║  • 👨‍🌾 Farmer Tools                                        ║
    ║  • 💳 Credit Score Tracking                                ║
    ║  • 📈 Investment Portfolio                                  ║
    ║  • 🛡️ Security Center                                       ║
    ║  • 🎮 Gamification System                                   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def install_requirements():
    """Install basic requirements"""
    requirements = [
        'streamlit>=1.28.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'plotly>=5.17.0',
        'python-dateutil>=2.8.0'
    ]
    
    try:
        logger.info("📦 Installing/updating requirements...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '--upgrade'
        ] + requirements, check=True, capture_output=True, text=True)
        logger.info("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install requirements: {e}")
        logger.info("Continuing with existing packages...")
        return False

def find_app():
    """Find the best available app to run"""
    current_dir = Path(__file__).parent
    
    # Priority order of apps to try
    apps = [
        current_dir / 'frontend' / 'comprehensive_app.py',
        current_dir / 'frontend' / 'clean_app.py',
        current_dir / 'frontend' / 'app.py'
    ]
    
    for app in apps:
        if app.exists():
            logger.info(f"📱 Found app: {app.name}")
            return app
    
    logger.error("❌ No JarvisFi application found!")
    return None

def run_streamlit_app(app_path, port=8501):
    """Run the Streamlit application"""
    try:
        logger.info(f"🚀 Starting JarvisFi on port {port}...")
        logger.info(f"🌐 Open your browser to: http://localhost:{port}")
        logger.info("⏹️ Press Ctrl+C to stop")
        
        # Basic streamlit command
        cmd = [
            sys.executable, '-m', 'streamlit', 'run',
            str(app_path),
            '--server.port', str(port),
            '--server.address', '0.0.0.0',
            '--browser.gatherUsageStats', 'false',
            '--server.headless', 'true'
        ]
        
        # Run the application
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit to see if it starts successfully
        import time
        time.sleep(3)
        
        if process.poll() is None:
            logger.info("✅ JarvisFi started successfully!")
            logger.info("📱 Access the application in your web browser")
            
            # Wait for the process to complete
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
            logger.error(f"❌ Failed to start JarvisFi")
            if stderr:
                logger.error(f"Error: {stderr}")
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
    print_banner()
    
    try:
        # Install/update requirements
        install_requirements()
        
        # Find the app to run
        app_path = find_app()
        if not app_path:
            logger.error("❌ No application found to run")
            return 1
        
        # Run the application
        success = run_streamlit_app(app_path)
        
        if success:
            logger.info("✅ JarvisFi session completed")
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
