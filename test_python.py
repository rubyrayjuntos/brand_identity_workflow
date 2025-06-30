#!/usr/bin/env python3
"""
Test script to verify Python 3.12 installation and basic functionality
"""

import sys
import platform

def main():
    print("=== Python Installation Test ===")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")
    print(f"Python Executable: {sys.executable}")
    
    # Test basic imports
    try:
        import streamlit
        print(f"✓ Streamlit imported successfully: {streamlit.__version__}")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
    
    try:
        import langchain_openai
        print(f"✓ LangChain OpenAI imported successfully")
    except ImportError as e:
        print(f"✗ LangChain OpenAI import failed: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main() 