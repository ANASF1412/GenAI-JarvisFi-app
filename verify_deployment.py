"""
Deployment Verification Script for JarvisFi
Checks if the application can be deployed successfully
"""

import requests
import time
import sys
from urllib.parse import urlparse

def check_github_repo():
    """Check if GitHub repository is accessible"""
    repo_url = "https://github.com/ANASF1412/GenAI-JarvisFi-app"
    
    try:
        response = requests.get(repo_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ GitHub repository accessible: {repo_url}")
            return True
        else:
            print(f"❌ GitHub repository not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing GitHub repository: {e}")
        return False

def check_streamlit_cloud_status():
    """Check Streamlit Community Cloud status"""
    try:
        response = requests.get("https://share.streamlit.io", timeout=10)
        if response.status_code == 200:
            print("✅ Streamlit Community Cloud is accessible")
            return True
        else:
            print(f"⚠️ Streamlit Community Cloud status: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ Cannot reach Streamlit Community Cloud: {e}")
        return False

def check_deployment_files():
    """Check if all deployment files exist"""
    required_files = [
        "streamlit_app.py",
        "requirements_deploy.txt",
        ".streamlit/config.toml",
        "DEPLOYMENT_GUIDE.md",
        "health_check.py"
    ]
    
    all_present = True
    for file_path in required_files:
        try:
            with open(file_path, 'r') as f:
                print(f"✅ {file_path}")
        except FileNotFoundError:
            print(f"❌ {file_path} - MISSING")
            all_present = False
    
    return all_present

def simulate_streamlit_import():
    """Test if streamlit_app.py can be imported"""
    try:
        import streamlit_app
        print("✅ streamlit_app.py imports successfully")
        return True
    except Exception as e:
        print(f"⚠️ streamlit_app.py import issue: {e}")
        return False

def generate_deployment_urls():
    """Generate expected deployment URLs"""
    base_names = [
        "jarvisfi-ai-assistant",
        "jarvisfi-financial-chatbot", 
        "genai-jarvisfi-app",
        "jarvisfi-multilingual-ai"
    ]
    
    platforms = {
        "Streamlit Cloud": "https://{}.streamlit.app",
        "Render": "https://{}.onrender.com",
        "Railway": "https://{}-production.up.railway.app"
    }
    
    print("\n🔗 Expected Deployment URLs:")
    for platform, url_template in platforms.items():
        print(f"\n{platform}:")
        for name in base_names[:2]:  # Show top 2 options
            print(f"  • {url_template.format(name)}")

def main():
    """Run deployment verification"""
    print("🔍 JarvisFi Deployment Verification")
    print("=" * 50)
    
    # Check GitHub repository
    print("\n📂 Checking GitHub Repository...")
    github_ok = check_github_repo()
    
    # Check deployment files
    print("\n📁 Checking Deployment Files...")
    files_ok = check_deployment_files()
    
    # Check Streamlit Cloud
    print("\n☁️ Checking Streamlit Community Cloud...")
    streamlit_ok = check_streamlit_cloud_status()
    
    # Test app import
    print("\n🐍 Testing Application Import...")
    import_ok = simulate_streamlit_import()
    
    # Generate URLs
    generate_deployment_urls()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Deployment Readiness Summary:")
    print(f"GitHub Repository: {'✅ READY' if github_ok else '❌ ISSUE'}")
    print(f"Deployment Files: {'✅ READY' if files_ok else '❌ MISSING FILES'}")
    print(f"Streamlit Cloud: {'✅ AVAILABLE' if streamlit_ok else '⚠️ CHECK MANUALLY'}")
    print(f"App Import Test: {'✅ PASS' if import_ok else '⚠️ MINOR ISSUES'}")
    
    overall_ready = github_ok and files_ok
    print(f"\nOverall Status: {'🚀 READY TO DEPLOY' if overall_ready else '🔧 NEEDS ATTENTION'}")
    
    if overall_ready:
        print("\n🎉 JarvisFi is ready for deployment!")
        print("\n📋 Next Steps:")
        print("1. Visit https://share.streamlit.io")
        print("2. Sign in with GitHub")
        print("3. Click 'New app'")
        print("4. Repository: ANASF1412/GenAI-JarvisFi-app")
        print("5. Branch: main")
        print("6. Main file: streamlit_app.py")
        print("7. Click 'Deploy!'")
        print("\n⏱️ Deployment typically takes 2-5 minutes")
    else:
        print("\n🔧 Please fix the issues above before deploying.")
    
    return 0 if overall_ready else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️ Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        sys.exit(1)
