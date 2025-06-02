from app import create_app
import argparse
import os

app = create_app()

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run the StudyHub Flask application')
    parser.add_argument('--port', type=int, default=5001, help='Port to run the Flask app on (default: 5001)')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to run the Flask app on (default: 127.0.0.1)')
    args = parser.parse_args()
    
    # Configure environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    # Launch in debug mode for development with optimized reloader
    app.run(
        host=args.host,
        port=args.port,
        debug=True,
        use_reloader=True,
        reloader_type='stat',
        threaded=True
    )