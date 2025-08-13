#!/usr/bin/env python3
"""
Complete Setup and Test Script for Personal Finance Chatbot
Sets up environment and runs comprehensive tests on new devices
"""

import os
import sys
import subprocess
import platform
import json
from datetime import datetime

class SetupAndTestRunner:
    """Complete setup and test runner for new devices"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.python_version = sys.version_info
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.setup_log = []
        
    def log(self, message, level="INFO"):
        """Log setup messages"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        print(log_entry)
        self.setup_log.append(log_entry)
    
    def run_command(self, command, description, critical=True):
        """Run a command and handle errors"""
        self.log(f"Running: {description}")
        self.log(f"Command: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.project_dir
            )
            
            if result.returncode == 0:
                self.log(f"✅ {description} - SUCCESS")
                return True, result.stdout, result.stderr
            else:
                self.log(f"❌ {description} - FAILED", "ERROR")
                self.log(f"Error: {result.stderr}", "ERROR")
                if critical:
                    raise Exception(f"{description} failed: {result.stderr}")
                return False, result.stdout, result.stderr
                
        except Exception as e:
            self.log(f"💥 {description} - EXCEPTION: {e}", "ERROR")
            if critical:
                raise
            return False, "", str(e)
    
    def check_python_version(self):
        """Check Python version compatibility"""
        self.log("🐍 Checking Python Version...")
        
        if self.python_version < (3, 8):
            raise Exception(f"Python 3.8+ required. Current: {sys.version}")
        
        self.log(f"✅ Python {sys.version} is compatible")
        return True
    
    def setup_virtual_environment(self):
        """Setup virtual environment"""
        self.log("📦 Setting up Virtual Environment...")
        
        venv_path = os.path.join(self.project_dir, "venv")
        
        if os.path.exists(venv_path):
            self.log("Virtual environment already exists")
            return True
        
        # Create virtual environment
        success, stdout, stderr = self.run_command(
            f"{sys.executable} -m venv venv",
            "Create Virtual Environment"
        )
        
        if success:
            self.log("✅ Virtual environment created")
            return True
        
        return False
    
    def install_dependencies(self):
        """Install required dependencies"""
        self.log("📥 Installing Dependencies...")
        
        # Determine pip command based on OS
        if self.system == "windows":
            pip_cmd = "venv\\Scripts\\pip"
            python_cmd = "venv\\Scripts\\python"
        else:
            pip_cmd = "venv/bin/pip"
            python_cmd = "venv/bin/python"
        
        # Upgrade pip first
        self.run_command(
            f"{pip_cmd} install --upgrade pip",
            "Upgrade pip"
        )
        
        # Install requirements
        requirements_file = os.path.join(self.project_dir, "requirements.txt")
        
        if os.path.exists(requirements_file):
            success, stdout, stderr = self.run_command(
                f"{pip_cmd} install -r requirements.txt",
                "Install requirements.txt"
            )
        else:
            # Install essential packages manually
            essential_packages = [
                "streamlit>=1.28.0",
                "pandas>=1.5.0",
                "plotly>=5.15.0",
                "transformers>=4.30.0",
                "torch>=2.0.0",
                "pytest>=7.4.0",
                "psutil>=5.9.0",
                "requests>=2.31.0"
            ]
            
            for package in essential_packages:
                self.run_command(
                    f"{pip_cmd} install {package}",
                    f"Install {package}",
                    critical=False
                )
        
        # Install additional ML packages
        ml_packages = [
            "sentence-transformers",
            "huggingface-hub",
            "SpeechRecognition",
            "pyttsx3"
        ]
        
        for package in ml_packages:
            self.run_command(
                f"{pip_cmd} install {package}",
                f"Install {package}",
                critical=False
            )
        
        self.log("✅ Dependencies installation completed")
        return True
    
    def download_language_models(self):
        """Download required language models"""
        self.log("🧠 Downloading Language Models...")
        
        # Determine python command
        if self.system == "windows":
            python_cmd = "venv\\Scripts\\python"
        else:
            python_cmd = "venv/bin/python"
        
        # Download spaCy model
        self.run_command(
            f"{python_cmd} -m spacy download en_core_web_sm",
            "Download spaCy English model",
            critical=False
        )
        
        # Download NLTK data
        nltk_downloads = [
            "punkt", "stopwords", "wordnet", "averaged_perceptron_tagger"
        ]
        
        for dataset in nltk_downloads:
            self.run_command(
                f"{python_cmd} -c \"import nltk; nltk.download('{dataset}')\"",
                f"Download NLTK {dataset}",
                critical=False
            )
        
        self.log("✅ Language models download completed")
        return True
    
    def create_environment_file(self):
        """Create .env file template"""
        self.log("⚙️ Creating Environment Configuration...")
        
        env_file = os.path.join(self.project_dir, ".env")
        
        if os.path.exists(env_file):
            self.log(".env file already exists")
            return True
        
        env_template = """# Personal Finance Chatbot Environment Configuration
# Copy this file and update with your actual credentials

# IBM Watson Credentials
WATSON_ASSISTANT_API_KEY=your_watson_api_key_here
WATSON_ASSISTANT_URL=your_watson_url_here
WATSON_NLU_API_KEY=your_nlu_api_key_here
WATSON_NLU_URL=your_nlu_url_here

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=finance_chatbot
MONGODB_ENCRYPTION_KEY=your_32_character_encryption_key_here

# Firebase Configuration (Optional)
FIREBASE_CREDENTIALS_PATH=path/to/firebase-credentials.json

# API Keys
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
GOOGLE_TRANSLATE_API_KEY=your_google_translate_key_here

# Security
SECRET_KEY=your_secret_key_for_encryption_here
JWT_SECRET=your_jwt_secret_key_here

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
"""
        
        try:
            with open(env_file, "w") as f:
                f.write(env_template)
            self.log("✅ .env template created")
            return True
        except Exception as e:
            self.log(f"❌ Failed to create .env file: {e}", "ERROR")
            return False
    
    def run_comprehensive_tests(self):
        """Run comprehensive test suite"""
        self.log("🧪 Running Comprehensive Tests...")
        
        # Determine python command
        if self.system == "windows":
            python_cmd = "venv\\Scripts\\python"
        else:
            python_cmd = "venv/bin/python"
        
        # Run test runner
        success, stdout, stderr = self.run_command(
            f"{python_cmd} run_tests.py",
            "Run Comprehensive Test Suite",
            critical=False
        )
        
        if success:
            self.log("✅ All tests completed successfully")
        else:
            self.log("⚠️ Some tests failed - check test_report.json for details", "WARNING")
        
        return success
    
    def generate_setup_report(self):
        """Generate setup completion report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "system_info": {
                "os": platform.system(),
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "architecture": platform.architecture()[0]
            },
            "setup_log": self.setup_log,
            "status": "completed"
        }
        
        try:
            with open("setup_report.json", "w") as f:
                json.dump(report, f, indent=2)
            self.log("📄 Setup report saved to setup_report.json")
        except Exception as e:
            self.log(f"❌ Failed to save setup report: {e}", "ERROR")
        
        return report
    
    def print_final_instructions(self):
        """Print final setup instructions"""
        print("\n" + "="*70)
        print("🎉 SETUP COMPLETED!")
        print("="*70)
        
        print("\n📋 NEXT STEPS:")
        print("1. Update .env file with your actual API credentials")
        print("2. Run the application:")
        
        if self.system == "windows":
            print("   venv\\Scripts\\streamlit run frontend/simple_app.py")
        else:
            print("   source venv/bin/activate")
            print("   streamlit run frontend/simple_app.py")
        
        print("\n3. Access the application at: http://localhost:8501")
        
        print("\n🧪 TO RUN TESTS:")
        if self.system == "windows":
            print("   venv\\Scripts\\python run_tests.py")
        else:
            print("   source venv/bin/activate")
            print("   python run_tests.py")
        
        print("\n📚 DOCUMENTATION:")
        print("   - Check setup_report.json for setup details")
        print("   - Check test_report.json for test results")
        print("   - Update .env file with your API keys")
        
        print("\n💡 TROUBLESHOOTING:")
        print("   - If tests fail, check missing dependencies")
        print("   - Ensure Python 3.8+ is installed")
        print("   - Check internet connection for model downloads")
    
    def run_complete_setup(self):
        """Run complete setup process"""
        try:
            self.log("🚀 Starting Complete Setup Process")
            self.log(f"System: {platform.system()} {platform.architecture()[0]}")
            self.log(f"Python: {sys.version}")
            
            # Step 1: Check Python version
            self.check_python_version()
            
            # Step 2: Setup virtual environment
            self.setup_virtual_environment()
            
            # Step 3: Install dependencies
            self.install_dependencies()
            
            # Step 4: Download language models
            self.download_language_models()
            
            # Step 5: Create environment file
            self.create_environment_file()
            
            # Step 6: Run tests
            self.run_comprehensive_tests()
            
            # Step 7: Generate report
            self.generate_setup_report()
            
            # Step 8: Print instructions
            self.print_final_instructions()
            
            self.log("✅ Complete setup process finished successfully!")
            return True
            
        except Exception as e:
            self.log(f"💥 Setup failed: {e}", "ERROR")
            print(f"\n❌ SETUP FAILED: {e}")
            print("Check setup_report.json for detailed logs")
            return False

def main():
    """Main setup function"""
    print("🔧 PERSONAL FINANCE CHATBOT - COMPLETE SETUP")
    print("="*70)
    
    runner = SetupAndTestRunner()
    success = runner.run_complete_setup()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
