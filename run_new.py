"""
StudyHub Alternative Application Launcher

This file provides an alternative way to launch the StudyHub Flask application
with command-line argument support for custom host and port configuration.
While the standard approach is to use 'flask run' with .flaskenv configuration,
this launcher offers more flexibility for development scenarios.

Key Features:
    - Command-line argument parsing for host and port
    - Custom development server configuration
    - Enhanced logging and startup messages
    - Environment variable override capabilities
    - Error handling and graceful shutdown

Usage Examples:
    python run_new.py                    # Default: 127.0.0.1:5000
    python run_new.py --port 8080        # Custom port
    python run_new.py --host 0.0.0.0     # Accept external connections
    python run_new.py --host 0.0.0.0 --port 3000  # Custom host and port

Comparison with Standard Launch:
    Standard:    flask run
    Alternative: python run_new.py

When to Use:
    - Custom development configurations
    - Testing different host/port combinations
    - Educational purposes to understand Flask deployment
    - Scenarios requiring programmatic server control

Production Note:
    This launcher is for development only. For production deployment,
    use proper WSGI servers like Gunicorn with the main run.py file.

Author: StudyHub Development Team
License: MIT
"""

# =============================================================================
# CORE IMPORTS AND DEPENDENCIES
# =============================================================================

# Flask application factory
from app import create_app

# Standard library imports for system operations
import argparse  # Command-line argument parsing and validation
import os       # Operating system interface for environment variables
import sys      # System-specific parameters and functions

# =============================================================================
# APPLICATION INSTANCE CREATION
# =============================================================================

def create_application_instance():
    """
    Create and configure the Flask application instance.
    
    This function uses the Application Factory pattern to create
    a properly configured Flask application with all extensions
    and blueprints properly initialized.
    
    Returns:
        Flask: Configured Flask application instance
        
    Note:
        This approach allows for consistent application configuration
        regardless of how the application is launched.
    """
    try:
        app = create_app()
        print("✅ Flask application instance created successfully")
        return app
    except Exception as e:
        print(f"❌ Error creating Flask application: {e}")
        sys.exit(1)

# Create the application instance
app = create_application_instance()

# =============================================================================
# COMMAND-LINE INTERFACE CONFIGURATION
# =============================================================================

def setup_argument_parser():
    """
    Configure and return the command-line argument parser.
    
    This function sets up comprehensive argument parsing with
    helpful descriptions, examples, and validation.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description='Launch the StudyHub Flask web application with custom configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Configuration Examples:
  python run_new.py                           # Default settings (127.0.0.1:5000)
  python run_new.py --port 8080               # Custom port
  python run_new.py --host 0.0.0.0            # Accept external connections  
  python run_new.py --host 0.0.0.0 --port 3000  # Full custom configuration

Network Configuration Notes:
  • 127.0.0.1 (localhost): Local development only
  • 0.0.0.0: Accept connections from any network interface
  • Custom ports: Useful for running multiple instances

Security Warning:
  Using --host 0.0.0.0 makes the application accessible from other computers
  on your network. Only use this in trusted development environments.
        """
    )
    
    # Port configuration with validation
    parser.add_argument(
        '--port', 
        type=int, 
        default=5000,
        metavar='PORT',
        help='Port number for the Flask application (1024-65535, default: 5000)'
    )
    
    # Host configuration with common options
    parser.add_argument(
        '--host', 
        type=str, 
        default='127.0.0.1',
        metavar='HOST', 
        help='Host address to bind the application (default: 127.0.0.1 for localhost)'
    )
    
    # Verbose output option
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    
    return parser

def validate_arguments(args):
    """
    Validate command-line arguments for security and correctness.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        bool: True if arguments are valid, False otherwise
    """
    # Validate port range
    if not (1024 <= args.port <= 65535):
        print(f"❌ Error: Port {args.port} is outside valid range (1024-65535)")
        print("   Ports below 1024 require administrator privileges")
        return False
    
    # Validate host address format (basic check)
    if not args.host.replace('.', '').replace(':', '').isalnum():
        # Allow localhost and numeric IPs
        valid_hosts = ['127.0.0.1', 'localhost', '0.0.0.0']
        if args.host not in valid_hosts:
            print(f"❌ Error: Invalid host address '{args.host}'")
            print(f"   Valid examples: {', '.join(valid_hosts)}")
            return False
    
    return True

# =============================================================================
# DEVELOPMENT SERVER CONFIGURATION
# =============================================================================

def configure_development_environment(verbose=False):
    """
    Configure the development environment with appropriate settings.
    
    Args:
        verbose (bool): Enable detailed logging
    """
    # Set Flask environment variables for development
    env_vars = {
        'FLASK_ENV': 'development',
        'FLASK_DEBUG': '1',
        'PYTHONPATH': os.getcwd()  # Ensure current directory is in Python path
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        if verbose:
            print(f"🔧 Set {key}={value}")

def display_startup_banner(host, port, verbose=False):
    """
    Display an informative startup banner with configuration details.
    
    Args:
        host (str): Host address
        port (int): Port number
        verbose (bool): Show additional details
    """
    banner_width = 80
    print("=" * banner_width)
    print("🎓 STUDYHUB WEB APPLICATION LAUNCHER".center(banner_width))
    print("=" * banner_width)
    
    # Basic configuration
    print(f"🌐 Host Address:    {host}")
    print(f"🔌 Port Number:     {port}")
    print(f"🌍 Access URL:      http://{host}:{port}")
    
    # Development settings
    print(f"🛠️  Environment:     Development")
    print(f"🐛 Debug Mode:      Enabled")
    print(f"🔄 Auto-reload:     Enabled")
    print(f"🧵 Threading:       Enabled")
    
    if verbose:
        print(f"📂 Working Dir:     {os.getcwd()}")
        print(f"🐍 Python Version:  {sys.version.split()[0]}")
    
    # Security warning for external access
    if host == '0.0.0.0':
        print("⚠️  WARNING: Application accessible from external networks")
    
    print("=" * banner_width)
    print("Press Ctrl+C to stop the server")
    print("=" * banner_width)

# =============================================================================
# MAIN EXECUTION LOGIC
# =============================================================================

def main():
    """
    Main execution function that orchestrates the application startup.
    
    This function handles the complete application launch process including
    argument parsing, validation, environment setup, and server startup.
    """
    try:
        # Parse and validate command-line arguments
        parser = setup_argument_parser()
        args = parser.parse_args()
        
        if not validate_arguments(args):
            parser.print_help()
            sys.exit(1)
        
        # Configure development environment
        configure_development_environment(verbose=args.verbose)
        
        # Display startup information
        display_startup_banner(args.host, args.port, args.verbose)
        
        # Start the Flask development server
        app.run(
            host=args.host,                # Bind to specified host
            port=args.port,                # Listen on specified port
            debug=True,                    # Enable debug mode and error pages
            use_reloader=True,             # Auto-reload on file changes
            reloader_type='stat',          # File change detection method
            threaded=True,                 # Enable concurrent request handling
            use_debugger=True              # Enable interactive debugger
        )
        
    except KeyboardInterrupt:
        # Handle graceful shutdown
        print("\n" + "=" * 80)
        print("🛑 STUDYHUB APPLICATION SHUTDOWN".center(80))
        print("=" * 80)
        print("Thank you for using StudyHub!")
        
    except OSError as e:
        # Handle network-related errors
        if "Address already in use" in str(e):
            print(f"\n❌ Error: Port {args.port} is already in use")
            print(f"   Try a different port with: python run_new.py --port {args.port + 1}")
        else:
            print(f"\n❌ Network error: {e}")
        sys.exit(1)
        
    except Exception as e:
        # Handle unexpected errors
        print(f"\n❌ Unexpected error starting StudyHub: {e}")
        print("Please check your configuration and try again.")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

# =============================================================================
# SCRIPT EXECUTION ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    main()
