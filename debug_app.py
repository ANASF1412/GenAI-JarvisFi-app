#!/usr/bin/env python3
"""
Debug script to test JarvisFi application functionality
"""

import streamlit as st
import sys
import os
import traceback

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test all imports"""
    st.write("🔍 Testing imports...")
    
    try:
        import pandas as pd
        st.success("✅ pandas imported successfully")
    except Exception as e:
        st.error(f"❌ pandas import failed: {e}")
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        st.success("✅ plotly imported successfully")
    except Exception as e:
        st.error(f"❌ plotly import failed: {e}")
    
    try:
        from frontend.complete_jarvisfi_app import CompleteJarvisFiApp
        st.success("✅ CompleteJarvisFiApp imported successfully")
        return True
    except Exception as e:
        st.error(f"❌ CompleteJarvisFiApp import failed: {e}")
        st.code(traceback.format_exc())
        return False

def test_session_state():
    """Test session state functionality"""
    st.write("🔍 Testing session state...")
    
    # Initialize test values
    if 'test_income' not in st.session_state:
        st.session_state.test_income = 50000
    
    # Test income update
    new_income = st.number_input(
        "Test Monthly Income (₹)",
        min_value=5000,
        max_value=1000000,
        value=st.session_state.test_income,
        step=5000
    )
    
    if new_income != st.session_state.test_income:
        st.session_state.test_income = new_income
        st.success(f"✅ Income updated to ₹{new_income:,}")
        st.rerun()
    
    st.info(f"Current test income: ₹{st.session_state.test_income:,}")

def test_basic_functionality():
    """Test basic app functionality"""
    st.write("🔍 Testing basic functionality...")
    
    # Test basic calculations
    income = 50000
    expenses = 30000
    savings = income - expenses
    savings_rate = (savings / income) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Income", f"₹{income:,}")
    with col2:
        st.metric("Expenses", f"₹{expenses:,}")
    with col3:
        st.metric("Savings Rate", f"{savings_rate:.1f}%")
    
    # Test chart
    try:
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=['Income', 'Expenses', 'Savings'], 
                            y=[income, expenses, savings],
                            marker_color=['green', 'red', 'blue']))
        fig.update_layout(title='Financial Overview', height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.success("✅ Chart rendering works")
    except Exception as e:
        st.error(f"❌ Chart rendering failed: {e}")

def main():
    """Main debug function"""
    st.set_page_config(
        page_title="JarvisFi Debug",
        page_icon="🔧",
        layout="wide"
    )
    
    st.title("🔧 JarvisFi Debug Tool")
    st.markdown("This tool helps debug issues with the JarvisFi application.")
    
    # Test imports
    st.header("1. Import Tests")
    imports_ok = test_imports()
    
    # Test session state
    st.header("2. Session State Tests")
    test_session_state()
    
    # Test basic functionality
    st.header("3. Basic Functionality Tests")
    test_basic_functionality()
    
    # Try to run the main app
    if imports_ok:
        st.header("4. Main Application Test")
        if st.button("🚀 Test Main Application"):
            try:
                from frontend.complete_jarvisfi_app import CompleteJarvisFiApp
                app = CompleteJarvisFiApp()
                st.success("✅ Main application initialized successfully")
                
                # Test a simple method
                if hasattr(app, 'initialize_session_state'):
                    app.initialize_session_state()
                    st.success("✅ Session state initialized")
                
                # Show current session state
                st.write("**Current Session State:**")
                if 'user_profile' in st.session_state:
                    profile = st.session_state.user_profile
                    st.json({
                        'monthly_income': profile['basic_info']['monthly_income'],
                        'user_type': profile['basic_info']['user_type'],
                        'language': profile['basic_info']['language']
                    })
                
            except Exception as e:
                st.error(f"❌ Main application test failed: {e}")
                st.code(traceback.format_exc())
    
    # System information
    st.header("5. System Information")
    st.write(f"**Python Version:** {sys.version}")
    st.write(f"**Streamlit Version:** {st.__version__}")
    
    # Show environment
    st.write("**Environment Variables:**")
    env_vars = ['PATH', 'PYTHONPATH', 'STREAMLIT_SERVER_PORT']
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        st.write(f"- {var}: {value[:100]}..." if len(str(value)) > 100 else f"- {var}: {value}")

if __name__ == "__main__":
    main()
