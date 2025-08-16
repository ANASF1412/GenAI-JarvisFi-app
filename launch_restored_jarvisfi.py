#!/usr/bin/env python3
"""
JarvisFi 2.0 Restored Application Launcher
Launch the complete restored version with all advanced features and UI designs
"""

import os
import sys
import subprocess
import logging
import time
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_restored_banner():
    """Print JarvisFi Restored banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║                            🤖 JarvisFi                                       ║
    ║              Your Ultimate Multilingual Finance Chat Assistant              ║
    ║                                                                              ║
    ║  🌟 RESTORED ADVANCED FEATURES:                                             ║
    ║                                                                              ║
    ║  🎨 ADVANCED UI & DESIGN:                                                   ║
    ║  • ✅ Custom CSS with gradients, animations, and modern styling             ║
    ║  • ✅ Advanced metric cards with hover effects and transitions              ║
    ║  • ✅ Animated progress indicators and visual feedback                       ║
    ║  • ✅ Professional color schemes and responsive design                       ║
    ║  • ✅ Interactive charts with enhanced styling                               ║
    ║                                                                              ║
    ║  🚀 COMPREHENSIVE FEATURES:                                                 ║
    ║  • ✅ Advanced sidebar with profile management                               ║
    ║  • ✅ Comprehensive session state with all data structures                   ║
    ║  • ✅ Advanced gamification system with points, levels, badges              ║
    ║  • ✅ Sophisticated data save options with encryption                        ║
    ║  • ✅ Multi-format data export (JSON, CSV, Excel, PDF)                      ║
    ║  • ✅ Advanced notification system                                           ║
    ║  • ✅ Voice settings and AI configuration                                    ║
    ║  • ✅ Analytics tracking and user behavior monitoring                        ║
    ║                                                                              ║
    ║  💡 INTELLIGENT RECOMMENDATIONS:                                            ║
    ║  • ✅ User-type specific financial advice                                    ║
    ║  • ✅ Age and income-based recommendations                                   ║
    ║  • ✅ Dynamic financial goals with progress tracking                         ║
    ║  • ✅ Advanced recent activity feed                                          ║
    ║                                                                              ║
    ║  🔒 SECURITY & PRIVACY:                                                     ║
    ║  • ✅ AES-256 encryption simulation                                          ║
    ║  • ✅ Configurable data retention policies                                   ║
    ║  • ✅ GDPR compliance warnings and controls                                  ║
    ║  • ✅ Advanced backup and recovery options                                   ║
    ║                                                                              ║
    ║  🌍 MULTILINGUAL EXCELLENCE:                                                ║
    ║  • ✅ Complete UI translation for 4 languages                               ║
    ║  • ✅ Cultural adaptation and localized content                              ║
    ║  • ✅ Language-specific financial recommendations                            ║
    ║                                                                              ║
    ║  📊 ADVANCED ANALYTICS:                                                     ║
    ║  • ✅ Comprehensive user behavior tracking                                   ║
    ║  • ✅ Session management and time tracking                                   ║
    ║  • ✅ Feature usage analytics                                                ║
    ║  • ✅ Performance metrics and optimization                                   ║
    ║                                                                              ║
    ║  🎯 SPECIALIZED TOOLS:                                                      ║
    ║  • ✅ Farmer-specific data structures and tools                              ║
    ║  • ✅ Investment tracking with portfolio management                          ║
    ║  • ✅ Credit score monitoring and improvement                                ║
    ║  • ✅ Advanced financial goal setting and tracking                           ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_advanced_dependencies():
    """Check if all advanced dependencies are available"""
    logger.info("🔍 Checking advanced dependencies...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'datetime'
    ]
    
    optional_packages = [
        'asyncio',
        'json',
        'logging',
        'time',
        'typing'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} - Available")
        except ImportError:
            missing_packages.append(package)
            logger.warning(f"❌ {package} - Missing")
    
    for package in optional_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} - Available (Optional)")
        except ImportError:
            logger.info(f"ℹ️ {package} - Not available (Optional)")
    
    if missing_packages:
        logger.warning(f"⚠️ Missing required packages: {', '.join(missing_packages)}")
        logger.info("🔄 Installing missing packages...")
        
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages, check=True, capture_output=True, text=True)
            
            logger.info("✅ Missing packages installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install packages: {e}")
            return False
    
    logger.info("✅ All required dependencies available")
    return True

def run_restored_application(port=8505):
    """Run the restored JarvisFi 2.0 application"""
    logger.info(f"🚀 Starting JarvisFi on port {port}...")
    logger.info("🤖 Your Ultimate Multilingual Finance Chat Assistant")
    logger.info(f"🌐 Application will be available at: http://localhost:{port}")
    logger.info("📱 Open your web browser and navigate to the URL above")
    logger.info("⏹️ Press Ctrl+C to stop the server")
    
    # Find the restored application
    current_dir = Path(__file__).parent
    app_path = current_dir / 'frontend' / 'restored_jarvisfi_app.py'
    
    if not app_path.exists():
        logger.error(f"❌ Restored application not found at: {app_path}")
        return False
    
    # Streamlit command with advanced configuration
    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        str(app_path),
        '--server.port', str(port),
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false',
        '--theme.primaryColor', '#667eea',
        '--theme.backgroundColor', '#ffffff',
        '--theme.secondaryBackgroundColor', '#f0f2f6',
        '--theme.textColor', '#262730'
    ]
    
    try:
        # Run the application
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment to check if it starts successfully
        time.sleep(3)
        
        if process.poll() is None:
            logger.info("✅ JarvisFi started successfully!")
            logger.info("🤖 Your Ultimate Multilingual Finance Chat Assistant is ready!")
            logger.info("🎉 All advanced features and UI designs are now available:")
            logger.info("   • ✅ Advanced CSS styling with animations")
            logger.info("   • ✅ Comprehensive session state management")
            logger.info("   • ✅ Advanced gamification system")
            logger.info("   • ✅ Sophisticated data save options")
            logger.info("   • ✅ Multi-language support with cultural adaptation")
            logger.info("   • ✅ Advanced analytics and user tracking")
            logger.info("   • ✅ Professional UI with modern design")
            logger.info("   • ✅ Interactive charts and visualizations")
            logger.info("   • ✅ Comprehensive notification system")
            logger.info("   • ✅ Advanced security and privacy controls")
            
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
    try:
        # Print banner
        print_restored_banner()
        
        # Check dependencies
        if not check_advanced_dependencies():
            logger.error("❌ Dependency check failed")
            return 1
        
        # Run restored application
        success = run_restored_application()
        
        if success:
            logger.info("✅ JarvisFi session completed successfully")
            logger.info("🤖 Your Ultimate Multilingual Finance Chat Assistant served you well!")
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
