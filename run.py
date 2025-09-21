#!/usr/bin/env python3
"""
CementAI Platform - Easy Setup and Run Script
This script handles the complete setup and launch of the CementAI platform.
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_header():
    """Print application header"""
    print("=" * 60)
    print("🏭 CementAI Platform - Smart Plant Operations")
    print("=" * 60)
    print("🤖 AI-Driven Autonomous Cement Plant Management")
    print("🛡️  Enhanced Worker Safety & Compliance Monitoring")
    print("📊 Real-time Operations Optimization")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def create_project_structure():
    """Create necessary project directories"""
    directories = [
        'frontend',
        'backend/api',
        'backend/routes',
        'backend/models',
        'ai-services',
        'database',
        'config',
        'tests',
        'docs',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Project structure created")

def install_requirements():
    """Install Python requirements"""
    if not Path('requirements.txt').exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        print("📦 Installing Python dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_env_file():
    """Create environment file with default values"""
    env_content = """# CementAI Platform Configuration
# API Keys (Replace with your actual keys)
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///cement_plant.db

# Security
SECRET_KEY=cement_ai_secret_key_2024
JWT_SECRET=jwt_secret_for_cement_ai

# Plant Configuration
PLANT_ID=CP001
PLANT_LOCATION=Mumbai, India
MAX_WORKERS_PER_SHIFT=50
SAFETY_CHECK_INTERVAL=30

# AI Configuration
AI_MODEL=gemini-pro
OPTIMIZATION_INTERVAL=300
SAFETY_ALERT_THRESHOLD=0.8

# Development Settings
DEBUG=True
FLASK_ENV=development
"""
    
    if not Path('.env').exists():
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Environment file created (.env)")
    else:
        print("✅ Environment file exists")

def save_frontend_file():
    """Save the frontend HTML file"""
    # The frontend HTML is already created in the artifact above
    # This function ensures it exists in the right location
    frontend_dir = Path('frontend')
    frontend_dir.mkdir(exist_ok=True)
    
    if not Path('frontend/index.html').exists():
        print("ℹ️  Please ensure the frontend/index.html file from the artifact is saved")
        print("   You can copy it from the generated HTML artifact above")
    else:
        print("✅ Frontend file exists")

def save_backend_file():
    """Save the backend Python file"""
    backend_dir = Path('backend')
    backend_dir.mkdir(exist_ok=True)
    
    if not Path('backend/app.py').exists():
        print("ℹ️  Please ensure the backend/app.py file from the artifact is saved")
        print("   You can copy it from the generated Python artifact above")
    else:
        print("✅ Backend file exists")

def run_application():
    """Run the CementAI application"""
    try:
        print("\n🚀 Starting CementAI Platform...")
        print("📡 Backend API starting on http://localhost:5000")
        print("🌐 Dashboard will be available at http://localhost:5000")
        print("\n⏳ Please wait while the system initializes...")
        
        # Change to the directory containing app.py
        backend_file = Path('backend/app.py')
        if backend_file.exists():
            os.chdir('backend')
            subprocess.check_call([sys.executable, 'app.py'])
        else:
            print("❌ Backend application file not found")
            print("   Please ensure backend/app.py exists")
            return False
            
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")
        return False

def show_quick_start_info():
    """Show quick start information"""
    print("\n" + "="*60)
    print("🎯 QUICK START GUIDE")
    print("="*60)

def main():
    """Main execution function"""
    print_header()
    
    # Step 1: Check Python version
    check_python_version()
    
    # Step 2: Create project structure
    create_project_structure()
    
    # Step 3: Create environment file
    create_env_file()
    
    # Step 4: Check for required files
    frontend_exists = Path('frontend/index.html').exists()
    backend_exists = Path('backend/app.py').exists()
    
    if not frontend_exists or not backend_exists:
        print("\n⚠️  Missing required files:")
        if not frontend_exists:
            print("   ❌ frontend/index.html")
        if not backend_exists:
            print("   ❌ backend/app.py")
        
        show_quick_start_info()
        return
    
    # Step 5: Install requirements if needed
    print("\n🔍 Checking dependencies...")
    try:
        import flask
        print("✅ Dependencies already installed")
    except ImportError:
        print("📦 Installing dependencies...")
        if not install_requirements():
            print("❌ Failed to install dependencies. Please run:")
            print("   pip install -r requirements.txt")
            return
    
    # Step 6: Run the application
    print("\n🎉 All checks passed! Starting CementAI Platform...")
    time.sleep(2)
    
    # Try to open browser after a short delay
    import threading
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:5000')
        except:
            pass
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run the application
    run_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using CementAI Platform!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check the setup and try again."))
    print("\n📋 What you need to do:")
    print("1. Copy the HTML code from the first artifact to 'frontend/index.html'")
    print("2. Copy the Python code from the backend artifact to 'backend/app.py'")
    print("3. Run this script again: python run.py")
    print("\n🔧 Optional Configuration:")
    print("• Edit .env file to add your Gemini API key")
    print("• Customize plant settings in .env file")
    print("\n🌐 After setup:")
    print("• Dashboard: http://localhost:5000")
    print("• API docs: http://localhost:5000/api/health")
    print("\n🆘 Need help?")
    print("• Check README.md for detailed instructions")
    print("• Ensure all files are in the correct directories")
    print("="*60)