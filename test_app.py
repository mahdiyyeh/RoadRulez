#!/usr/bin/env python3
"""Test script to verify the app can start and display a window."""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Starting app...")
    print("This will open a window. Please check your screen.")
    
    # Import and run the main app
    import road_rulez_app
    
    print("App imported successfully!")
    print("If you see this message but no window, the window might be hidden.")
    print("Check your taskbar/dock for the app window.")
    
except Exception as e:
    print(f"Error starting app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

