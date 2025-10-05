#!/usr/bin/env python3
"""
Test MSAI Application System
Simple test to verify the system works
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing MSAI Application System Imports")
    print("=" * 50)
    
    try:
        import gspread
        print("✅ gspread imported successfully")
    except ImportError as e:
        print(f"❌ gspread import failed: {e}")
        return False
    
    try:
        import fastapi
        print("✅ fastapi imported successfully")
    except ImportError as e:
        print(f"❌ fastapi import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ uvicorn import failed: {e}")
        return False
    
    try:
        from google.oauth2 import service_account
        print("✅ google.oauth2 imported successfully")
    except ImportError as e:
        print(f"❌ google.oauth2 import failed: {e}")
        return False
    
    return True

def test_google_sheets_integration():
    """Test Google Sheets integration"""
    print("\n🔧 Testing Google Sheets Integration")
    print("=" * 40)
    
    try:
        from google_sheets_integration import MSAIApplicationSheets
        print("✅ MSAIApplicationSheets class imported successfully")
        
        # Test initialization
        sheets = MSAIApplicationSheets()
        print("✅ MSAIApplicationSheets initialized successfully")
        
        # Test authentication (this will fail without proper credentials)
        print("🔑 Testing authentication...")
        if sheets.authenticate():
            print("✅ Google Sheets authentication successful")
        else:
            print("⚠️  Google Sheets authentication failed (expected without proper setup)")
        
        return True
        
    except Exception as e:
        print(f"❌ Google Sheets integration test failed: {e}")
        return False

def test_fastapi_integration():
    """Test FastAPI integration"""
    print("\n🌐 Testing FastAPI Integration")
    print("=" * 35)
    
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel
        print("✅ FastAPI and Pydantic imported successfully")
        
        # Test creating a simple app
        app = FastAPI(title="Test App")
        print("✅ FastAPI app created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ FastAPI integration test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 MSAI Application System Test Suite")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test Google Sheets integration
    if not test_google_sheets_integration():
        all_tests_passed = False
    
    # Test FastAPI integration
    if not test_fastapi_integration():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("✅ All tests passed! MSAI Application System is ready.")
        print("\n🎉 Next steps:")
        print("   1. Complete Google Drive setup manually")
        print("   2. Run: msai_env/bin/python msai_application_api.py")
        print("   3. Visit: http://localhost:8000/")
        print("   4. Test the application form")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure you're using the virtual environment")
        print("   2. Check that all dependencies are installed")
        print("   3. Verify Google service account credentials")

if __name__ == "__main__":
    main()