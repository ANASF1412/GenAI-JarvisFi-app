#!/usr/bin/env python3
"""
Comprehensive Test Suite for Personal Finance Chatbot
Tests all major components and functionality
"""

import os
import sys
import pandas as pd
import json
from datetime import datetime
import logging

# Add backend to path for testing
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_data_files():
    """Test if data files are properly formatted"""
    print("🔍 Testing Data Files...")
    
    try:
        # Test user profiles JSON
        with open('data/user_profiles.json', 'r') as f:
            profiles = json.load(f)
        print("✅ User profiles JSON is valid")
        
        # Test transactions CSV
        transactions_df = pd.read_csv('data/transactions.csv')
        print(f"✅ Transactions CSV loaded: {len(transactions_df)} records")
        
        # Check required columns
        required_cols = ['date', 'description', 'amount', 'category', 'payment_method']
        missing_cols = [col for col in required_cols if col not in transactions_df.columns]
        
        if missing_cols:
            print(f"❌ Missing columns in transactions: {missing_cols}")
            return False
        else:
            print("✅ All required columns present in transactions")
        
        return True
        
    except Exception as e:
        print(f"❌ Data files test failed: {e}")
        return False

def test_backend_modules():
    """Test all backend modules can be imported"""
    print("\n🔍 Testing Backend Modules...")
    
    modules_to_test = [
        'watson_integration',
        'budget_analyzer', 
        'demographic_adapter',
        'nlp_processor',
        'currency_converter',
        'pdf_generator',
        'smart_alerts'
    ]
    
    failed_imports = []
    
    for module_name in modules_to_test:
        try:
            module = __import__(module_name)
            print(f"✅ {module_name} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {module_name}: {e}")
            failed_imports.append(module_name)
        except Exception as e:
            print(f"⚠️ {module_name} imported but has issues: {e}")
    
    return len(failed_imports) == 0

def test_core_functionality():
    """Test core functionality of major components"""
    print("\n🔍 Testing Core Functionality...")
    
    try:
        # Test Budget Analyzer
        from budget_analyzer import BudgetAnalyzer
        analyzer = BudgetAnalyzer()
        
        # Load sample data
        df = pd.read_csv('data/transactions.csv')
        df['date'] = pd.to_datetime(df['date'])
        
        # Test analysis
        profile = {"demographic": "professional", "monthly_income": 75000}
        analysis = analyzer.analyze_transactions(df, profile)
        
        print(f"✅ Budget analysis completed: {len(analysis)} sections")
        
        # Test Demographic Adapter
        from demographic_adapter import DemographicAdapter
        adapter = DemographicAdapter()
        
        response = adapter.adapt_response("Test content", "student", "budget_management")
        print("✅ Demographic adaptation working")
        
        # Test Smart Alerts
        from smart_alerts import SmartAlerts
        alert_system = SmartAlerts()
        
        alerts = alert_system.generate_all_alerts(df, profile, analysis)
        print(f"✅ Smart alerts generated: {len(alerts)} alerts")
        
        # Test Currency Converter
        from currency_converter import CurrencyConverter
        converter = CurrencyConverter()
        
        rate = converter._get_fallback_rate('USD', 'INR')  # Using fallback to avoid API calls in test
        print(f"✅ Currency converter working: 1 USD = {rate} INR")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        return False

def test_ui_components():
    """Test if UI components load properly"""
    print("\n🔍 Testing UI Components...")
    
    try:
        # Check if CSS file exists
        if os.path.exists('frontend/styles.css'):
            print("✅ Custom CSS file found")
        else:
            print("⚠️ Custom CSS file not found")
        
        # Test if frontend app compiles
        import subprocess
        result = subprocess.run([
            'python', '-m', 'py_compile', 'frontend/app.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Frontend app compiles successfully")
            return True
        else:
            print(f"❌ Frontend compilation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ UI components test failed: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("\n🔍 Testing Dependencies...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'requests',
        'fpdf2',
        'ibm-watson'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            # Special handling for fpdf2 which imports as 'fpdf'
            import_name = 'fpdf' if package == 'fpdf2' else package.replace('-', '_')
            __import__(import_name)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
        except Exception as e:
            print(f"⚠️ {package} - Issue: {e}")
    
    if missing_packages:
        print(f"\n📦 To install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def run_full_test_suite():
    """Run complete test suite"""
    print("🚀 Starting Personal Finance Chatbot Test Suite")
    print("=" * 60)
    
    tests = [
        ("Data Files", test_data_files),
        ("Backend Modules", test_backend_modules), 
        ("Dependencies", test_dependencies),
        ("Core Functionality", test_core_functionality),
        ("UI Components", test_ui_components)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your chatbot is ready to run!")
        print("\n🚀 To start the application:")
        print("streamlit run frontend/app.py")
    else:
        print("⚠️ Some tests failed. Please fix the issues before running the application.")
    
    return passed == total

if __name__ == "__main__":
    # Configure logging for tests
    logging.basicConfig(level=logging.ERROR)  # Suppress non-critical logs during testing
    
    success = run_full_test_suite()
    sys.exit(0 if success else 1)#!/usr/bin/env python3
"""
Comprehensive Test Suite for Personal Finance Chatbot
Tests all major components and functionality
"""

import os
import sys
import pandas as pd
import json
from datetime import datetime
import logging

# Add backend to path for testing
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_data_files():
    """Test if data files are properly formatted"""
    print("🔍 Testing Data Files...")
    
    try:
        # Test user profiles JSON
        with open('data/user_profiles.json', 'r') as f:
            profiles = json.load(f)
        print("✅ User profiles JSON is valid")
        
        # Test transactions CSV
        transactions_df = pd.read_csv('data/transactions.csv')
        print(f"✅ Transactions CSV loaded: {len(transactions_df)} records")
        
        # Check required columns
        required_cols = ['date', 'description', 'amount', 'category', 'payment_method']
        missing_cols = [col for col in required_cols if col not in transactions_df.columns]
        
        if missing_cols:
            print(f"❌ Missing columns in transactions: {missing_cols}")
            return False
        else:
            print("✅ All required columns present in transactions")
        
        return True
        
    except Exception as e:
        print(f"❌ Data files test failed: {e}")
        return False

def test_backend_modules():
    """Test all backend modules can be imported"""
    print("\n🔍 Testing Backend Modules...")
    
    modules_to_test = [
        'watson_integration',
        'budget_analyzer', 
        'demographic_adapter',
        'nlp_processor',
        'currency_converter',
        'pdf_generator',
        'smart_alerts'
    ]
    
    failed_imports = []
    
    for module_name in modules_to_test:
        try:
            module = __import__(module_name)
            print(f"✅ {module_name} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {module_name}: {e}")
            failed_imports.append(module_name)
        except Exception as e:
            print(f"⚠️ {module_name} imported but has issues: {e}")
    
    return len(failed_imports) == 0

def test_core_functionality():
    """Test core functionality of major components"""
    print("\n🔍 Testing Core Functionality...")
    
    try:
        # Test Budget Analyzer
        from budget_analyzer import BudgetAnalyzer
        analyzer = BudgetAnalyzer()
        
        # Load sample data
        df = pd.read_csv('data/transactions.csv')
        df['date'] = pd.to_datetime(df['date'])
        
        # Test analysis
        profile = {"demographic": "professional", "monthly_income": 75000}
        analysis = analyzer.analyze_transactions(df, profile)
        
        print(f"✅ Budget analysis completed: {len(analysis)} sections")
        
        # Test Demographic Adapter
        from demographic_adapter import DemographicAdapter
        adapter = DemographicAdapter()
        
        response = adapter.adapt_response("Test content", "student", "budget_management")
        print("✅ Demographic adaptation working")
        
        # Test Smart Alerts
        from smart_alerts import SmartAlerts
        alert_system = SmartAlerts()
        
        alerts = alert_system.generate_all_alerts(df, profile, analysis)
        print(f"✅ Smart alerts generated: {len(alerts)} alerts")
        
        # Test Currency Converter
        from currency_converter import CurrencyConverter
        converter = CurrencyConverter()
        
        rate = converter._get_fallback_rate('USD', 'INR')  # Using fallback to avoid API calls in test
        print(f"✅ Currency converter working: 1 USD = {rate} INR")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        return False

def test_ui_components():
    """Test if UI components load properly"""
    print("\n🔍 Testing UI Components...")
    
    try:
        # Check if CSS file exists
        if os.path.exists('frontend/styles.css'):
            print("✅ Custom CSS file found")
        else:
            print("⚠️ Custom CSS file not found")
        
        # Test if frontend app compiles
        import subprocess
        result = subprocess.run([
            'python', '-m', 'py_compile', 'frontend/app.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Frontend app compiles successfully")
            return True
        else:
            print(f"❌ Frontend compilation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ UI components test failed: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("\n🔍 Testing Dependencies...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'requests',
        'fpdf2',
        'ibm-watson'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
        except Exception as e:
            print(f"⚠️ {package} - Issue: {e}")
    
    if missing_packages:
        print(f"\n📦 To install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def run_full_test_suite():
    """Run complete test suite"""
    print("🚀 Starting Personal Finance Chatbot Test Suite")
    print("=" * 60)
    
    tests = [
        ("Data Files", test_data_files),
        ("Backend Modules", test_backend_modules), 
        ("Dependencies", test_dependencies),
        ("Core Functionality", test_core_functionality),
        ("UI Components", test_ui_components)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your chatbot is ready to run!")
        print("\n🚀 To start the application:")
        print("streamlit run frontend/app.py")
    else:
        print("⚠️ Some tests failed. Please fix the issues before running the application.")
    
    return passed == total

if __name__ == "__main__":
    # Configure logging for tests
    logging.basicConfig(level=logging.ERROR)  # Suppress non-critical logs during testing
    
    success = run_full_test_suite()
    sys.exit(0 if success else 1)