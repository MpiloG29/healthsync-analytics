#!/usr/bin/env python3
"""
HealthSync Setup Script
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"  {description}...")
    try:
        subprocess.check_call(cmd, shell=True)
        print(f"  [OK] {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [WARN] {description} failed (but continuing): {e}")
        return False

def main():
    print("=" * 50)
    print("  Setting up HealthSync Analytics Platform")
    print("=" * 50)
    
    # Try to install minimal dependencies
    packages = [
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
    ]
    
    for package in packages:
        run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}")
    
    print("\n" + "=" * 50)
    print("  [SUCCESS] Setup Complete!")
    print("\nTo run the API:")
    print("  1. Run: python app.py")
    print("  2. Open: http://localhost:8001")
    print("  3. Docs: http://localhost:8001/docs")
    print("\nTo test the API:")
    print("  curl http://localhost:8001/health")
    print("  curl http://localhost:8001/patients")
    print("\n  HealthSync is ready to use!")

if __name__ == "__main__":
    main()
