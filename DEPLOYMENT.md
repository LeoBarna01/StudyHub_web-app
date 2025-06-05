# StudyHub Web Application - Quick Start Guide

This document explains how to run the StudyHub web application using the standard Flask workflow.

## Quick Start (Recommended Method)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
flask run
```

That's it! The application will start at http://localhost:5000

## Why Only One Method?

We use **only** the Flask CLI (`flask run`) because:
- It's the **official Flask standard**
- Automatically reads configuration from `.flaskenv`
- Provides consistent behavior across different environments
- Integrates perfectly with Flask's ecosystem
- Simpler and less confusing than multiple methods

## Configuration

The application is configured via the `.flaskenv` file:

```
FLASK_APP=run.py              # Entry point
FLASK_ENV=development         # Development mode
FLASK_DEBUG=1                 # Debug enabled
FLASK_RUN_PORT=5000          # Default port
FLASK_RUN_HOST=127.0.0.1     # Localhost only
```

## Flask CLI Commands

```bash
# Start development server
flask run

# Custom port and host  
flask run --port 8080 --host 0.0.0.0

# Show all application routes
flask routes

# Open interactive shell with app context
flask shell

# Database commands (if Flask-Migrate is configured)
flask db init     # Initialize migrations
flask db migrate  # Create migration
flask db upgrade  # Apply migrations
```

## Development Workflow

1. **Start the server**: `flask run`
2. **Make changes** - Server reloads automatically
3. **Test at**: http://localhost:5000  
4. **Stop server**: Ctrl+C

## Environment Variables

You can override `.flaskenv` settings with environment variables:

```bash
# Temporary port change
FLASK_RUN_PORT=8080 flask run

# External access
FLASK_RUN_HOST=0.0.0.0 flask run

# Disable debug
FLASK_DEBUG=0 flask run
```

## Production Deployment

For production, use a proper WSGI server:

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 run:app
```

### Production Environment
```bash
# Set production mode
export FLASK_ENV=production
export FLASK_DEBUG=0

# Or create a .env file for production
echo "FLASK_ENV=production" > .env
echo "FLASK_DEBUG=0" >> .env
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   flask run --port 5001
   ```

2. **Module not found**
   ```bash
   # Check you're in the project root
   ls -la run.py  # Should exist
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **External access needed**
   ```bash
   flask run --host 0.0.0.0
   ```

4. **Database issues**
   ```bash
   flask db upgrade  # Apply migrations
   ```

### Debug Information

When you run `flask run`, you'll see:
- Server address and port
- Debug mode status  
- Auto-reload status
- Any startup errors

---

**Bottom line**: Just use `flask run` - it's simple, standard, and works perfectly!
