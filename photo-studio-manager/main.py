
import sys
import os

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """Main application entry point"""
    try:
        # Import after path setup
        from views.main_window import main as run_app
        
        print("=" * 60)
        print("Photo Studio Management System")
        print("=" * 60)
        print("Initializing application...")
        print(f"Working directory: {current_dir}")
        print("Loading modules...")
        
        # Run the application
        run_app()
        
    except ImportError as e:
        print(f"Import Error: {e}")
        print("\nMissing dependencies. Please install required packages:")
        print("pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"Application Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()