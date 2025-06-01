from app import create_app
import argparse

app = create_app()

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run the StudyHub Flask application')
    parser.add_argument('--port', type=int, default=5001, help='Port to run the Flask app on (default: 5001)')
    args = parser.parse_args()
    
    # Launch in debug mode for development
    app.run(debug=True, port=args.port)