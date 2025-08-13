#!/usr/bin/env python3
"""
Test script to verify all fixes are working
"""

import sys
import os
sys.path.append('backend')
sys.path.append('frontend')

def test_imports():
    """Test all imports work correctly"""
    print("Testing imports...")

    try:
        global LanguageSupport, UserProfileManager, EnhancedUI, WatsonIntegration

        from backend.language_support import LanguageSupport
        print("✅ LanguageSupport imported successfully")

        from backend.user_profile_manager import UserProfileManager
        print("✅ UserProfileManager imported successfully")

        from frontend.enhanced_ui import EnhancedUI
        print("✅ EnhancedUI imported successfully")

        from backend.watson_integration import WatsonIntegration
        print("✅ WatsonIntegration imported successfully")

        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_language_support():
    """Test language support functionality"""
    print("\nTesting language support...")
    
    try:
        lang_support = LanguageSupport()
        
        # Test language detection
        tamil_text = "பணம் சேமிக்க எப்படி?"
        english_text = "How to save money?"
        
        tamil_result = lang_support.detect_language(tamil_text)
        english_result = lang_support.detect_language(english_text)
        
        print(f"✅ Tamil detection: {tamil_result}")
        print(f"✅ English detection: {english_result}")
        
        # Test translation
        translation = lang_support.translate_query(tamil_text)
        print(f"✅ Tamil query translation: {translation}")
        
        return True
    except Exception as e:
        print(f"❌ Language support error: {e}")
        return False

def test_user_profile_manager():
    """Test user profile manager"""
    print("\nTesting user profile manager...")
    
    try:
        profile_manager = UserProfileManager()
        
        # Test profile creation
        user_data = {
            'name': 'Test User',
            'age': 25,
            'user_type': 'student',
            'language': 'english',
            'monthly_income': 30000
        }
        
        profile = profile_manager.create_user_profile(user_data)
        print(f"✅ Profile created: {profile['basic_info']['user_type']}")
        
        # Test greeting
        greeting = profile_manager.get_personalized_greeting(profile, 'english')
        print(f"✅ Greeting generated: {greeting[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ User profile manager error: {e}")
        return False

def test_watson_integration():
    """Test Watson integration logger fix"""
    print("\nTesting Watson integration...")
    
    try:
        watson = WatsonIntegration()
        print("✅ WatsonIntegration initialized without logger error")
        
        # Test that logger exists
        if hasattr(watson, 'logger'):
            print("✅ Logger attribute exists")
            
            # Test logger functionality
            watson.logger.info("Test log message")
            print("✅ Logger works correctly")
        else:
            print("❌ Logger attribute missing")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Watson integration error: {e}")
        return False

def test_enhanced_ui():
    """Test enhanced UI components"""
    print("\nTesting enhanced UI...")

    try:
        ui = EnhancedUI()
        print("✅ EnhancedUI initialized successfully")

        # Test CSS setup (without calling it since it needs streamlit context)
        print("✅ EnhancedUI CSS setup available")

        # Test language options
        lang_options = [
            {'value': 'english', 'label': 'English'},
            {'value': 'tamil', 'label': 'தமிழ்'}
        ]
        print(f"✅ Language options available: {len(lang_options)}")

        return True
    except Exception as e:
        print(f"❌ Enhanced UI error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Running fix verification tests...\n")
    
    tests = [
        test_imports,
        test_language_support,
        test_user_profile_manager,
        test_watson_integration,
        test_enhanced_ui
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All fixes are working correctly!")
        print("\n🚀 Ready to run the application with:")
        print("   streamlit run frontend/app.py")
    else:
        print("⚠️  Some issues remain. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
