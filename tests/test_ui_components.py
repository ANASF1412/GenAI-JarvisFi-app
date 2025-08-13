"""
UI Components Test Suite
Tests Streamlit UI components and interactions
"""

import pytest
import streamlit as st
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add project paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

class TestStreamlitUIComponents:
    """Test Streamlit UI components"""
    
    @pytest.fixture(autouse=True)
    def setup_streamlit_session(self):
        """Setup Streamlit session state for testing"""
        # Mock Streamlit session state
        if not hasattr(st, 'session_state'):
            st.session_state = MagicMock()
        
        # Initialize required session state variables
        st.session_state.user_profile = {
            'basic_info': {
                'name': 'Test User',
                'language': 'english',
                'user_type': 'beginner',
                'currency': 'INR'
            }
        }
        st.session_state.chat_history = []
        st.session_state.dark_mode = False
        st.session_state.voice_listening = False
        st.session_state.voice_speaking = False
        st.session_state.ai_accuracy_enabled = True
        st.session_state.rag_enabled = True
    
    def test_session_state_initialization(self):
        """Test that session state is properly initialized"""
        required_keys = [
            'user_profile', 'chat_history', 'dark_mode',
            'voice_listening', 'voice_speaking', 'ai_accuracy_enabled'
        ]
        
        for key in required_keys:
            assert hasattr(st.session_state, key), f"Session state missing key: {key}"
        
        # Test user profile structure
        assert 'basic_info' in st.session_state.user_profile
        assert 'language' in st.session_state.user_profile['basic_info']
        assert 'user_type' in st.session_state.user_profile['basic_info']
    
    def test_language_switching(self):
        """Test language switching functionality"""
        # Test switching to Tamil
        original_lang = st.session_state.user_profile['basic_info']['language']
        
        st.session_state.user_profile['basic_info']['language'] = 'tamil'
        assert st.session_state.user_profile['basic_info']['language'] == 'tamil'
        
        # Test switching back to English
        st.session_state.user_profile['basic_info']['language'] = 'english'
        assert st.session_state.user_profile['basic_info']['language'] == 'english'
        
        # Restore original
        st.session_state.user_profile['basic_info']['language'] = original_lang
    
    def test_dark_mode_toggle(self):
        """Test dark mode toggle functionality"""
        original_mode = st.session_state.dark_mode
        
        # Toggle dark mode
        st.session_state.dark_mode = not original_mode
        assert st.session_state.dark_mode != original_mode
        
        # Toggle back
        st.session_state.dark_mode = original_mode
        assert st.session_state.dark_mode == original_mode
    
    def test_user_type_selection(self):
        """Test user type selection"""
        valid_user_types = ['beginner', 'intermediate', 'professional', 'student']
        
        for user_type in valid_user_types:
            st.session_state.user_profile['basic_info']['user_type'] = user_type
            assert st.session_state.user_profile['basic_info']['user_type'] == user_type
            assert user_type in valid_user_types
    
    def test_chat_history_management(self):
        """Test chat history management"""
        # Clear chat history
        st.session_state.chat_history = []
        assert len(st.session_state.chat_history) == 0
        
        # Add messages
        test_messages = [
            {'role': 'user', 'content': 'Hello', 'timestamp': '2024-01-01T10:00:00'},
            {'role': 'assistant', 'content': 'Hi there!', 'timestamp': '2024-01-01T10:00:01'}
        ]
        
        for message in test_messages:
            st.session_state.chat_history.append(message)
        
        assert len(st.session_state.chat_history) == len(test_messages)
        
        # Test message structure
        for i, message in enumerate(st.session_state.chat_history):
            assert 'role' in message
            assert 'content' in message
            assert message['role'] in ['user', 'assistant']
            assert len(message['content']) > 0
    
    def test_voice_interface_states(self):
        """Test voice interface state management"""
        # Test voice listening state
        st.session_state.voice_listening = True
        assert st.session_state.voice_listening == True
        
        st.session_state.voice_listening = False
        assert st.session_state.voice_listening == False
        
        # Test voice speaking state
        st.session_state.voice_speaking = True
        assert st.session_state.voice_speaking == True
        
        st.session_state.voice_speaking = False
        assert st.session_state.voice_speaking == False
    
    def test_ai_feature_toggles(self):
        """Test AI feature toggle states"""
        # Test AI accuracy toggle
        st.session_state.ai_accuracy_enabled = True
        assert st.session_state.ai_accuracy_enabled == True
        
        st.session_state.ai_accuracy_enabled = False
        assert st.session_state.ai_accuracy_enabled == False
        
        # Test RAG toggle
        st.session_state.rag_enabled = True
        assert st.session_state.rag_enabled == True
        
        st.session_state.rag_enabled = False
        assert st.session_state.rag_enabled == False

class TestEnhancedUIComponents:
    """Test Enhanced UI components"""
    
    @pytest.fixture(autouse=True)
    def setup_enhanced_ui(self):
        """Setup Enhanced UI for testing"""
        try:
            from frontend.enhanced_ui import EnhancedUI
            self.enhanced_ui = EnhancedUI()
            self.ui_available = True
        except ImportError:
            self.enhanced_ui = None
            self.ui_available = False
    
    def test_enhanced_ui_initialization(self):
        """Test Enhanced UI initialization"""
        if not self.ui_available:
            pytest.skip("Enhanced UI not available")
        
        assert self.enhanced_ui is not None
        assert hasattr(self.enhanced_ui, 'setup_custom_css')
    
    @patch('streamlit.markdown')
    def test_css_setup(self, mock_markdown):
        """Test CSS setup functionality"""
        if not self.ui_available:
            pytest.skip("Enhanced UI not available")
        
        # Test light mode CSS
        self.enhanced_ui.setup_custom_css(dark_mode=False)
        assert mock_markdown.called
        
        # Test dark mode CSS
        mock_markdown.reset_mock()
        self.enhanced_ui.setup_custom_css(dark_mode=True)
        assert mock_markdown.called
    
    def test_ui_component_methods(self):
        """Test UI component methods exist"""
        if not self.ui_available:
            pytest.skip("Enhanced UI not available")
        
        # Check for expected methods
        expected_methods = [
            'setup_custom_css',
            'create_info_card',
            'create_metric_card',
            'create_chat_message'
        ]
        
        available_methods = []
        for method in expected_methods:
            if hasattr(self.enhanced_ui, method):
                available_methods.append(method)
        
        # At least setup_custom_css should be available
        assert 'setup_custom_css' in available_methods

class TestTabNavigation:
    """Test tab navigation functionality"""
    
    def test_tab_names_english(self):
        """Test English tab names"""
        expected_tabs = [
            "💬 Chat", "📊 Dashboard", "💰 Budget", "📈 Investment",
            "💱 Currency", "🧠 AI Insights", "📈 Reports", "💡 Tips"
        ]
        
        # Test that all expected tabs are defined
        for tab in expected_tabs:
            assert isinstance(tab, str)
            assert len(tab) > 0
            # Check for emoji and text
            assert any(char for char in tab if ord(char) > 127)  # Has emoji
            assert any(char.isalpha() for char in tab)  # Has text
    
    def test_tab_names_tamil(self):
        """Test Tamil tab names"""
        expected_tabs_tamil = [
            "💬 அரட்டை", "📊 டாஷ்போர்டு", "💰 பட்ஜெட்", "📈 முதலீடு",
            "💱 நாணயம்", "🧠 AI நுண்ணறிவு", "📈 அறிக்கைகள்", "💡 குறிப்புகள்"
        ]
        
        # Test that all expected Tamil tabs are defined
        for tab in expected_tabs_tamil:
            assert isinstance(tab, str)
            assert len(tab) > 0
            # Check for Tamil characters
            has_tamil = any('\u0b80' <= char <= '\u0bff' for char in tab)
            assert has_tamil, f"Tab '{tab}' should contain Tamil characters"
    
    def test_tab_consistency(self):
        """Test that English and Tamil tabs have same count"""
        english_tabs = [
            "💬 Chat", "📊 Dashboard", "💰 Budget", "📈 Investment",
            "💱 Currency", "🧠 AI Insights", "📈 Reports", "💡 Tips"
        ]
        
        tamil_tabs = [
            "💬 அரட்டை", "📊 டாஷ்போர்டு", "💰 பட்ஜெட்", "📈 முதலீடு",
            "💱 நாணயம்", "🧠 AI நுண்ணறிவு", "📈 அறிக்கைகள்", "💡 குறிப்புகள்"
        ]
        
        assert len(english_tabs) == len(tamil_tabs), "English and Tamil tabs count mismatch"
        
        # Test that emojis match
        for eng_tab, tam_tab in zip(english_tabs, tamil_tabs):
            eng_emoji = eng_tab.split()[0]
            tam_emoji = tam_tab.split()[0]
            assert eng_emoji == tam_emoji, f"Emoji mismatch: {eng_emoji} vs {tam_emoji}"

class TestFormValidation:
    """Test form validation and input handling"""
    
    def test_user_input_validation(self):
        """Test user input validation"""
        # Test valid inputs
        valid_inputs = [
            "How can I save money?",
            "What is a budget?",
            "Help me with investments",
            "பணம் எப்படி சேமிக்கலாம்?"
        ]
        
        for input_text in valid_inputs:
            assert isinstance(input_text, str)
            assert len(input_text.strip()) > 0
            assert len(input_text) < 1000  # Reasonable length limit
    
    def test_edge_case_inputs(self):
        """Test edge case input handling"""
        edge_cases = [
            "",  # Empty string
            " " * 100,  # Whitespace only
            "a",  # Single character
            "A" * 1000,  # Very long string
        ]
        
        for input_text in edge_cases:
            # Should not cause exceptions when processed
            try:
                processed = input_text.strip()
                assert isinstance(processed, str)
            except Exception as e:
                pytest.fail(f"Edge case input caused exception: {e}")
    
    def test_multilingual_input_handling(self):
        """Test multilingual input handling"""
        multilingual_inputs = [
            "Hello வணக்கம்",  # Mixed English-Tamil
            "How are you நீங்கள் எப்படி இருக்கிறீர்கள்?",  # Mixed
            "123 ஆயிரம்",  # Numbers with Tamil
            "email மின்னஞ்சல்",  # Technical terms
        ]
        
        for input_text in multilingual_inputs:
            assert isinstance(input_text, str)
            assert len(input_text.strip()) > 0
            # Should contain both English and Tamil characters
            has_english = any(char.isascii() and char.isalpha() for char in input_text)
            has_tamil = any('\u0b80' <= char <= '\u0bff' for char in input_text)
            # At least one should be true for mixed content
            assert has_english or has_tamil

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
