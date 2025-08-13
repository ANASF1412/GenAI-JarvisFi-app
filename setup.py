#!/usr/bin/env python3
"""
JarvisFi - Setup Script
Automated setup for JarvisFi development and deployment
"""

import os
import sys
import subprocess
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Any
import argparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class JarvisFiSetup:
    """JarvisFi setup and installation manager"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.required_python_version = (3, 9)
        self.required_tools = ['docker', 'docker-compose', 'git']
        
    def check_python_version(self) -> bool:
        """Check if Python version meets requirements"""
        current_version = sys.version_info[:2]
        if current_version < self.required_python_version:
            logger.error(f"Python {self.required_python_version[0]}.{self.required_python_version[1]}+ required. Current: {current_version[0]}.{current_version[1]}")
            return False
        logger.info(f"✅ Python version check passed: {current_version[0]}.{current_version[1]}")
        return True
    
    def check_system_requirements(self) -> bool:
        """Check system requirements"""
        logger.info("🔍 Checking system requirements...")
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Check required tools
        missing_tools = []
        for tool in self.required_tools:
            if not shutil.which(tool):
                missing_tools.append(tool)
        
        if missing_tools:
            logger.error(f"❌ Missing required tools: {', '.join(missing_tools)}")
            logger.info("Please install the missing tools and try again.")
            return False
        
        logger.info("✅ All system requirements met")
        return True
    
    def create_directories(self):
        """Create necessary directories"""
        logger.info("📁 Creating project directories...")
        
        directories = [
            'api/core',
            'api/models',
            'api/schemas',
            'api/services',
            'api/api',
            'api/integrations',
            'api/ml',
            'api/utils',
            'api/tests',
            'ui/components',
            'ui/pages',
            'ui/styles',
            'ui/assets/images',
            'ui/assets/icons',
            'ui/assets/audio',
            'ui/assets/fonts',
            'ui/utils',
            'ui/tests',
            'shared',
            'database/migrations',
            'database/seeds',
            'nginx',
            'docs/api',
            'docs/user_guide',
            'docs/deployment',
            'docs/development',
            'tests',
            'scripts',
            'monitoring/grafana',
            'monitoring/alerts',
            'logs',
            'uploads',
            'cache/voice',
            'models/huggingface',
            'backups'
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py for Python packages
            if any(directory.startswith(pkg) for pkg in ['api/', 'ui/', 'shared/']):
                init_file = dir_path / '__init__.py'
                if not init_file.exists():
                    init_file.touch()
        
        logger.info("✅ Project directories created")
    
    def setup_environment(self):
        """Setup environment configuration"""
        logger.info("⚙️ Setting up environment configuration...")
        
        env_file = self.project_root / '.env'
        env_template = self.project_root / '.env.comprehensive'
        
        if not env_file.exists() and env_template.exists():
            shutil.copy(env_template, env_file)
            logger.info("✅ Environment file created from template")
            logger.warning("⚠️ Please edit .env file with your actual API keys and configuration")
        else:
            logger.info("ℹ️ Environment file already exists")
    
    def install_python_dependencies(self, dev: bool = False):
        """Install Python dependencies"""
        logger.info("📦 Installing Python dependencies...")
        
        requirements_file = 'requirements_comprehensive.txt'
        if dev:
            requirements_file = 'requirements-dev.txt'
        
        requirements_path = self.project_root / requirements_file
        
        if not requirements_path.exists():
            logger.error(f"❌ Requirements file not found: {requirements_file}")
            return False
        
        try:
            # Upgrade pip first
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
            
            # Install requirements
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_path)
            ], check=True)
            
            logger.info("✅ Python dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install dependencies: {e}")
            return False
    
    def setup_database(self):
        """Setup database"""
        logger.info("🗄️ Setting up database...")
        
        try:
            # Check if Docker is running
            subprocess.run(['docker', 'ps'], check=True, capture_output=True)
            
            # Start database services
            compose_file = self.project_root / 'docker-compose-comprehensive.yml'
            if compose_file.exists():
                subprocess.run([
                    'docker-compose', '-f', str(compose_file),
                    'up', '-d', 'postgres', 'redis', 'mongodb'
                ], check=True)
                
                logger.info("✅ Database services started")
                return True
            else:
                logger.warning("⚠️ Docker compose file not found, skipping database setup")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to setup database: {e}")
            return False
    
    def download_ai_models(self):
        """Download required AI models"""
        logger.info("🤖 Downloading AI models...")
        
        try:
            # Download spaCy models
            subprocess.run([
                sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'
            ], check=True)
            
            logger.info("✅ AI models downloaded successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️ Failed to download some AI models: {e}")
            logger.info("Models will be downloaded automatically when needed")
            return True
    
    def create_sample_data(self):
        """Create sample data for development"""
        logger.info("📊 Creating sample data...")
        
        # This would typically involve running database migrations
        # and seeding with sample data
        logger.info("ℹ️ Sample data creation skipped (implement as needed)")
    
    def run_tests(self):
        """Run basic tests to verify installation"""
        logger.info("🧪 Running basic tests...")
        
        try:
            # Test imports
            test_imports = [
                'fastapi',
                'streamlit',
                'sqlalchemy',
                'redis',
                'transformers',
                'torch'
            ]
            
            for module in test_imports:
                try:
                    __import__(module)
                    logger.info(f"✅ {module} import successful")
                except ImportError as e:
                    logger.error(f"❌ {module} import failed: {e}")
                    return False
            
            logger.info("✅ All basic tests passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Tests failed: {e}")
            return False
    
    def create_startup_scripts(self):
        """Create startup scripts"""
        logger.info("📝 Creating startup scripts...")
        
        # Create start script
        start_script = self.project_root / 'start.sh'
        start_script_content = """#!/bin/bash
# JarvisFi Startup Script

echo "🚀 Starting JarvisFi..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.comprehensive to .env and configure it."
    exit 1
fi

# Start with Docker Compose
if command -v docker-compose &> /dev/null; then
    echo "🐳 Starting with Docker Compose..."
    docker-compose -f docker-compose-comprehensive.yml up -d
    echo "✅ JarvisFi started successfully!"
    echo "📱 Frontend: http://localhost:8501"
    echo "🔧 API: http://localhost:8000"
    echo "📊 Monitoring: http://localhost:5555"
else
    echo "❌ Docker Compose not found. Please install Docker and Docker Compose."
    exit 1
fi
"""
        
        with open(start_script, 'w') as f:
            f.write(start_script_content)
        
        # Make executable
        os.chmod(start_script, 0o755)
        
        # Create stop script
        stop_script = self.project_root / 'stop.sh'
        stop_script_content = """#!/bin/bash
# JarvisFi Stop Script

echo "🛑 Stopping JarvisFi..."

if command -v docker-compose &> /dev/null; then
    docker-compose -f docker-compose-comprehensive.yml down
    echo "✅ JarvisFi stopped successfully!"
else
    echo "❌ Docker Compose not found."
    exit 1
fi
"""
        
        with open(stop_script, 'w') as f:
            f.write(stop_script_content)
        
        # Make executable
        os.chmod(stop_script, 0o755)
        
        logger.info("✅ Startup scripts created")
    
    def setup_development_environment(self):
        """Setup development environment"""
        logger.info("🛠️ Setting up development environment...")
        
        try:
            # Install pre-commit hooks if available
            if shutil.which('pre-commit'):
                subprocess.run(['pre-commit', 'install'], check=True)
                logger.info("✅ Pre-commit hooks installed")
            
            # Setup IDE configuration (VS Code)
            vscode_dir = self.project_root / '.vscode'
            vscode_dir.mkdir(exist_ok=True)
            
            # Create settings.json
            settings_json = vscode_dir / 'settings.json'
            settings_content = {
                "python.defaultInterpreterPath": "./venv/bin/python",
                "python.linting.enabled": True,
                "python.linting.flake8Enabled": True,
                "python.formatting.provider": "black",
                "python.testing.pytestEnabled": True,
                "files.exclude": {
                    "**/__pycache__": True,
                    "**/*.pyc": True,
                    ".pytest_cache": True,
                    ".coverage": True,
                    "htmlcov": True
                }
            }
            
            import json
            with open(settings_json, 'w') as f:
                json.dump(settings_content, f, indent=2)
            
            logger.info("✅ Development environment configured")
            
        except Exception as e:
            logger.warning(f"⚠️ Development environment setup partially failed: {e}")
    
    def print_next_steps(self):
        """Print next steps for the user"""
        logger.info("\n🎉 JarvisFi setup completed successfully!")
        
        print("\n" + "="*60)
        print("🚀 NEXT STEPS:")
        print("="*60)
        print("1. Edit .env file with your API keys and configuration")
        print("2. Start JarvisFi: ./start.sh")
        print("3. Access the application:")
        print("   • Frontend: http://localhost:8501")
        print("   • API Docs: http://localhost:8000/docs")
        print("   • Monitoring: http://localhost:5555")
        print("\n📚 Documentation: README_COMPREHENSIVE.md")
        print("🆘 Support: https://github.com/your-org/jarvisfi/issues")
        print("="*60)
    
    def full_setup(self, dev: bool = False, skip_models: bool = False):
        """Run full setup process"""
        logger.info("🚀 Starting JarvisFi setup...")
        
        steps = [
            ("System Requirements", self.check_system_requirements),
            ("Project Directories", self.create_directories),
            ("Environment Configuration", self.setup_environment),
            ("Python Dependencies", lambda: self.install_python_dependencies(dev)),
            ("Database Setup", self.setup_database),
            ("Startup Scripts", self.create_startup_scripts),
        ]
        
        if not skip_models:
            steps.append(("AI Models", self.download_ai_models))
        
        if dev:
            steps.append(("Development Environment", self.setup_development_environment))
        
        steps.extend([
            ("Basic Tests", self.run_tests),
            ("Sample Data", self.create_sample_data),
        ])
        
        failed_steps = []
        
        for step_name, step_func in steps:
            try:
                logger.info(f"\n{'='*20} {step_name} {'='*20}")
                if not step_func():
                    failed_steps.append(step_name)
            except Exception as e:
                logger.error(f"❌ {step_name} failed: {e}")
                failed_steps.append(step_name)
        
        if failed_steps:
            logger.warning(f"⚠️ Some steps failed: {', '.join(failed_steps)}")
            logger.info("You may need to complete these steps manually.")
        
        self.print_next_steps()
        
        return len(failed_steps) == 0


def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description='JarvisFi Setup Script')
    parser.add_argument('--dev', action='store_true', help='Setup development environment')
    parser.add_argument('--skip-models', action='store_true', help='Skip AI model downloads')
    parser.add_argument('--quick', action='store_true', help='Quick setup (skip optional steps)')
    
    args = parser.parse_args()
    
    setup = JarvisFiSetup()
    
    try:
        success = setup.full_setup(
            dev=args.dev,
            skip_models=args.skip_models or args.quick
        )
        
        if success:
            logger.info("🎉 Setup completed successfully!")
            sys.exit(0)
        else:
            logger.warning("⚠️ Setup completed with some issues.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\n⏹️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
