#!/usr/bin/env python
"""Quick test to verify app imports successfully"""
try:
    from app import app
    print("=" * 60)
    print("SUCCESS: App imported successfully!")
    print("=" * 60)
    print("\nYou can now run the app with:")
    print("  python app.py")
    print("\nThen open your browser to: http://localhost:5000")
    print("=" * 60)
except Exception as e:
    print("=" * 60)
    print("ERROR: Failed to import app")
    print("=" * 60)
    print(f"Error: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()

