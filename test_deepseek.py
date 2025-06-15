#!/usr/bin/env python3
"""
Test script for DeepSeek Coder integration
"""

import sys
import os

def test_imports():
    """Test if required packages are available"""
    try:
        import streamlit
        print("✅ Streamlit available")
    except ImportError:
        print("❌ Streamlit not available")
        return False
    
    try:
        import transformers
        print(f"✅ Transformers available (version: {transformers.__version__})")
    except ImportError:
        print("❌ Transformers not available")
        return False
    
    try:
        import torch
        print(f"✅ PyTorch available (version: {torch.__version__})")
    except ImportError:
        print("❌ PyTorch not available")
        return False
    
    return True

def test_generator():
    """Test the HTMLGenerator class"""
    try:
        from generator import HTMLGenerator
        print("✅ HTMLGenerator imported successfully")
        
        gen = HTMLGenerator()
        print(f"✅ HTMLGenerator initialized (model: {gen.model_name})")
        
        # Test generation
        html = gen.generate_html("simple calculator")
        print(f"✅ HTML generated successfully ({len(html)} characters)")
        
        return True
    except Exception as e:
        print(f"❌ Generator test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing DeepSeek Coder integration...")
    print("=" * 50)
    
    if test_imports():
        print("\n📦 All dependencies available!")
        if test_generator():
            print("\n🎉 DeepSeek integration test successful!")
        else:
            print("\n⚠️ Generator test failed")
    else:
        print("\n⚠️ Some dependencies missing - will use fallback mode")
