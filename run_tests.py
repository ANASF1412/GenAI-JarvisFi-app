#!/usr/bin/env python3
"""
Test Runner for Personal Finance Chatbot
Runs comprehensive tests and generates detailed reports
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
import argparse

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔄 {description}")
    print(f"Command: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout:
                print("Output:", result.stdout[:500])  # First 500 chars
            return True, result.stdout, result.stderr
        else:
            print(f"❌ {description} - FAILED")
            print("Error:", result.stderr)
            return False, result.stdout, result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False, "", "Command timed out"
    except Exception as e:
        print(f"💥 {description} - EXCEPTION: {e}")
        return False, "", str(e)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking Dependencies...")
    
    required_packages = [
        "streamlit", "pandas", "plotly", "transformers", 
        "torch", "pytest", "psutil", "requests"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ All dependencies available")
    return True

def run_comprehensive_tests():
    """Run the comprehensive test suite"""
    print("\n" + "="*70)
    print("🚀 RUNNING COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Run comprehensive test suite
    success, stdout, stderr = run_command(
        "python tests/comprehensive_test_suite.py",
        "Comprehensive Test Suite"
    )
    
    return success, stdout, stderr

def run_translation_tests():
    """Run translation model specific tests"""
    print("\n" + "="*70)
    print("🔤 RUNNING TRANSLATION MODEL TESTS")
    print("="*70)
    
    # Run translation tests with pytest
    success, stdout, stderr = run_command(
        "python -m pytest tests/test_translation_model.py -v --tb=short",
        "Translation Model Tests"
    )
    
    return success, stdout, stderr

def run_streamlit_app_test():
    """Test if Streamlit app starts without errors"""
    print("\n" + "="*70)
    print("🌐 TESTING STREAMLIT APPLICATION STARTUP")
    print("="*70)
    
    # Test app startup (run for 10 seconds then kill)
    success, stdout, stderr = run_command(
        "timeout 10s streamlit run frontend/simple_app.py --server.headless true --server.port 8502 || true",
        "Streamlit App Startup Test"
    )
    
    # Check if app started successfully (look for "You can now view" in output)
    app_started = "You can now view" in stdout or "Network URL" in stdout
    
    if app_started:
        print("✅ Streamlit app started successfully")
        return True, stdout, stderr
    else:
        print("❌ Streamlit app failed to start")
        return False, stdout, stderr

def test_file_structure():
    """Test if all required files exist"""
    print("\n🗂️ TESTING FILE STRUCTURE")
    print("-" * 30)
    
    required_files = [
        "frontend/simple_app.py",
        "frontend/enhanced_ui.py",
        "backend/language_support.py",
        "tests/comprehensive_test_suite.py",
        "tests/test_translation_model.py",
        "requirements.txt"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def generate_test_report(results):
    """Generate comprehensive test report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "test_summary": {
            "total_test_categories": len(results),
            "passed_categories": sum(1 for r in results.values() if r["success"]),
            "failed_categories": sum(1 for r in results.values() if not r["success"]),
        },
        "test_results": results,
        "recommendations": []
    }
    
    # Add recommendations based on results
    if not results.get("dependencies", {}).get("success", False):
        report["recommendations"].append("Install missing dependencies with pip install -r requirements.txt")
    
    if not results.get("file_structure", {}).get("success", False):
        report["recommendations"].append("Ensure all required files are present in the project")
    
    if not results.get("translation_tests", {}).get("success", False):
        report["recommendations"].append("Check translation model installation and configuration")
    
    if not results.get("streamlit_app", {}).get("success", False):
        report["recommendations"].append("Fix Streamlit application startup issues")
    
    # Calculate overall success rate
    success_rate = (report["test_summary"]["passed_categories"] / 
                   max(report["test_summary"]["total_test_categories"], 1)) * 100
    report["overall_success_rate"] = f"{success_rate:.1f}%"
    
    # Save report
    with open("comprehensive_test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    return report

def print_final_summary(report):
    """Print final test summary"""
    print("\n" + "="*70)
    print("📊 FINAL TEST SUMMARY")
    print("="*70)
    
    print(f"Timestamp: {report['timestamp']}")
    print(f"Total Test Categories: {report['test_summary']['total_test_categories']}")
    print(f"Passed Categories: {report['test_summary']['passed_categories']}")
    print(f"Failed Categories: {report['test_summary']['failed_categories']}")
    print(f"Overall Success Rate: {report['overall_success_rate']}")
    
    print(f"\n📋 DETAILED RESULTS:")
    for category, result in report["test_results"].items():
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"  {status} {category.replace('_', ' ').title()}")
        if not result["success"] and result.get("error"):
            print(f"    Error: {result['error'][:100]}...")
    
    if report["recommendations"]:
        print(f"\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(report["recommendations"], 1):
            print(f"  {i}. {rec}")
    
    print(f"\n📄 Detailed report saved to: comprehensive_test_report.json")
    
    # Final status
    if report["test_summary"]["failed_categories"] == 0:
        print(f"\n🎉 ALL TESTS PASSED! Your application is ready to use.")
        return 0
    else:
        print(f"\n⚠️ Some tests failed. Please check the issues above.")
        return 1

def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description="Run comprehensive tests for Personal Finance Chatbot")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency check")
    parser.add_argument("--skip-app", action="store_true", help="Skip Streamlit app test")
    parser.add_argument("--quick", action="store_true", help="Run only essential tests")
    
    args = parser.parse_args()
    
    print("🧪 PERSONAL FINANCE CHATBOT - COMPREHENSIVE TEST RUNNER")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # 1. Check dependencies
    if not args.skip_deps:
        deps_ok = check_dependencies()
        results["dependencies"] = {"success": deps_ok, "error": None if deps_ok else "Missing dependencies"}
    
    # 2. Test file structure
    files_ok = test_file_structure()
    results["file_structure"] = {"success": files_ok, "error": None if files_ok else "Missing files"}
    
    # 3. Run comprehensive tests
    if not args.quick:
        comp_success, comp_stdout, comp_stderr = run_comprehensive_tests()
        results["comprehensive_tests"] = {
            "success": comp_success, 
            "error": comp_stderr if not comp_success else None,
            "output": comp_stdout[:500] if comp_stdout else None
        }
    
    # 4. Run translation tests
    trans_success, trans_stdout, trans_stderr = run_translation_tests()
    results["translation_tests"] = {
        "success": trans_success,
        "error": trans_stderr if not trans_success else None,
        "output": trans_stdout[:500] if trans_stdout else None
    }
    
    # 5. Test Streamlit app
    if not args.skip_app:
        app_success, app_stdout, app_stderr = run_streamlit_app_test()
        results["streamlit_app"] = {
            "success": app_success,
            "error": app_stderr if not app_success else None,
            "output": app_stdout[:500] if app_stdout else None
        }
    
    # Generate and display report
    report = generate_test_report(results)
    exit_code = print_final_summary(report)
    
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
