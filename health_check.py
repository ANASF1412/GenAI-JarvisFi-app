"""
Health Check Script for JarvisFi Application
Verifies that all critical components are working
"""

import sys
import os
import importlib
from pathlib import Path

def check_dependencies():
    """Check if critical dependencies are available"""
    critical_deps = [
        'streamlit',
        'pandas',
        'plotly',
        'numpy'
    ]
    
    missing_deps = []
    for dep in critical_deps:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep}")
        except ImportError:
            missing_deps.append(dep)
            print(f"❌ {dep} - MISSING")
    
    return len(missing_deps) == 0

def check_file_structure():
    """Check if required files exist"""
    required_files = [
        'streamlit_app.py',
        'requirements_deploy.txt',
        '.streamlit/config.toml',
        'frontend/complete_jarvisfi_app.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path} - MISSING")
    
    return len(missing_files) == 0

def check_backend_modules():
    """Check if backend modules can be imported"""
    # Add backend to path
    backend_path = Path(__file__).parent / 'backend'
    sys.path.insert(0, str(backend_path))
    
    backend_modules = [
        'budget_analyzer',
        'demographic_adapter',
        'currency_converter',
        'smart_alerts'
    ]
    
    working_modules = 0
    for module in backend_modules:
        try:
            importlib.import_module(module)
            print(f"✅ backend.{module}")
            working_modules += 1
        except ImportError as e:
            print(f"⚠️ backend.{module} - {str(e)}")
    
    return working_modules >= len(backend_modules) // 2  # At least half should work

def main():
    """Run all health checks"""
    print("🏥 JarvisFi Health Check")
    print("=" * 50)
    
    print("\n📦 Checking Dependencies...")
    deps_ok = check_dependencies()
    
    print("\n📁 Checking File Structure...")
    files_ok = check_file_structure()
    
    print("\n🔧 Checking Backend Modules...")
    backend_ok = check_backend_modules()
    
    print("\n" + "=" * 50)
    print("📊 Health Check Summary:")
    print(f"Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    print(f"File Structure: {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"Backend Modules: {'✅ PASS' if backend_ok else '⚠️ PARTIAL'}")
    
    overall_health = deps_ok and files_ok and backend_ok
    print(f"\nOverall Health: {'✅ HEALTHY' if overall_health else '⚠️ NEEDS ATTENTION'}")
    
    if overall_health:
        print("\n🎉 JarvisFi is ready for deployment!")
    else:
        print("\n🔧 Please fix the issues above before deploying.")
    
    return 0 if overall_health else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
