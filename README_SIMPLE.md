# StudyHub Web Application

A Flask-based web application for academic document sharing and collaboration.

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**
   ```bash
   flask run
   ```

3. **Open your browser** to http://localhost:5000

That's it! 🎉

## What is StudyHub?

StudyHub is a web platform that allows students to:
- Upload and share academic documents
- Search and discover resources
- Ask questions and get answers
- Manage their academic materials

## Development

- **Start server**: `flask run`
- **View routes**: `flask routes` 
- **Interactive shell**: `flask shell`
- **Stop server**: Ctrl+C

The server automatically reloads when you make code changes.

## Configuration

All configuration is handled automatically via `.flaskenv`:
- Default port: 5000
- Debug mode: Enabled
- Auto-reload: Enabled

## Production Deployment

For production, use a WSGI server:

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 run:app
```

## Project Structure

```
StudyHub_web-app/
├── app/                    # Main application package
│   ├── auth/              # Authentication module  
│   ├── main/              # Main routes and pages
│   ├── upload/            # File upload functionality
│   ├── view/              # Document viewing and search
│   └── models.py          # Database models
├── templates/             # HTML templates
├── static/               # CSS, JS, images
├── run.py                # Flask application entry point
├── config.py             # Application configuration
└── requirements.txt      # Python dependencies
```

## Need Help?

- Check `DEPLOYMENT.md` for detailed setup information
- Run `flask routes` to see all available endpoints
- Use `flask shell` for interactive debugging

---

**Remember**: Always use `flask run` to start the application!
