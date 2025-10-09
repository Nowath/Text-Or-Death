"""
Text or Death - Quick Start Script
Run this to start the client directly
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client.main import main

if __name__ == "__main__":
    main()
