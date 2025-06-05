# StudyHub - Academic Document Sharing Platform

[![Flask](https://img.shields.io/badge/Flask-2.3.0-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.11-green.svg)](https://python.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)](https://sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)

**StudyHub** is a modern web application built with Flask that enables students to share, discover, and manage academic documents in a collaborative environment. The platform provides a secure and user-friendly interface for uploading, categorizing, and searching educational resources.

## 🚀 Features

### Core Functionality
- **Document Management**: Upload, categorize, and organize academic documents
- **Smart Search**: Advanced search with filters for categories, tags, and content
- **User Authentication**: Secure registration, login, and profile management
- **Favorites System**: Save and organize frequently accessed documents
- **Contact System**: Support and feedback forms for user assistance

### Technical Features
- **Responsive Design**: Mobile-first Bootstrap 5 interface
- **File Validation**: Comprehensive upload security and validation
- **Database Relationships**: Optimized SQLAlchemy models with proper relationships
- **Error Handling**: Comprehensive error pages and user feedback
- **Security**: CSRF protection, input validation, and secure file handling

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3.0 (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite (development) / PostgreSQL (production)
- **Authentication**: Flask-Login with secure password hashing
- **Forms**: Flask-WTF with comprehensive validation
- **Migrations**: Flask-Migrate for database schema management

### Frontend
- **UI Framework**: Bootstrap 5.3 for responsive design
- **Icons**: Font Awesome for consistent iconography
- **Fonts**: Google Fonts (Inter) for modern typography
- **JavaScript**: Vanilla JS for enhanced user interactions

### Development Tools
- **Environment**: Flask CLI with auto-reload
- **Configuration**: Environment-based configuration management
- **File Structure**: Modular blueprint architecture
- **Documentation**: Comprehensive inline documentation

## 📁 Project Structure

```
StudyHub_web-app/
├── app/                          # Main application package
│   ├── __init__.py              # Application factory
│   ├── models.py                # Database models
│   ├── auth/                    # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── routes.py           # Auth routes and logic
│   │   └── form.py             # Authentication forms
│   ├── main/                    # Main pages blueprint
│   │   ├── __init__.py
│   │   ├── main.py             # Main routes
│   │   └── errors.py           # Error handlers
│   ├── upload/                  # Document upload blueprint
│   │   ├── __init__.py
│   │   ├── upload.py           # Upload routes
│   │   ├── forms.py            # Upload forms
│   │   └── utils.py            # Upload utilities
│   ├── view/                    # Document viewing blueprint
│   │   ├── __init__.py
│   │   ├── view.py             # View routes
│   │   └── utils.py            # View utilities
│   └── form/                    # Contact forms blueprint
│       ├── __init__.py
│       ├── form.py             # Contact routes
│       └── forms.py            # Contact forms
├── templates/                   # Jinja2 templates
│   ├── main/                   # Main page templates
│   ├── auth/                   # Authentication templates
│   ├── upload/                 # Upload templates
│   ├── view/                   # Document view templates
│   ├── form/                   # Contact form templates
│   └── errors/                 # Error page templates
├── static/                     # Static assets
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript files
│   ├── images/                # Application images
│   └── profile_pics/          # User profile pictures
├── uploads/                    # User uploaded documents
├── migrations/                 # Database migration files
├── config.py                  # Application configuration
├── run.py                     # Application entry point
└── requirements.txt           # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StudyHub_web-app
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Start the application**
   ```bash
   flask run
   ```

6. **Access the application**
   Open your browser and navigate to: `http://127.0.0.1:5000`

### Optional: Populate Sample Data
```bash
python app/populate_sample_data.py
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root for production:

```bash
# Security
SECRET_KEY=your-very-long-random-secret-key

# Database
DATABASE_URL=postgresql://user:password@localhost/studyhub

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Development Configuration
The application uses `.flaskenv` for development settings:
- **FLASK_APP**: `run.py`
- **FLASK_ENV**: `development`
- **FLASK_DEBUG**: `1`
- **FLASK_RUN_PORT**: `5000`
- **FLASK_RUN_HOST**: `127.0.0.1`

## 📚 Usage Guide

### For Students

1. **Registration**: Create an account with your academic email
2. **Upload Documents**: Share your notes, assignments, and study materials
3. **Search & Discover**: Find relevant documents using advanced search filters
4. **Organize**: Use categories and tags to organize content
5. **Favorites**: Save frequently accessed documents for quick access

### For Administrators

- **User Management**: Monitor user accounts and activity
- **Content Moderation**: Review and manage uploaded documents
- **System Maintenance**: Use utility scripts for database management

## 🔒 Security Features

- **Authentication**: Secure login with password hashing (Werkzeug)
- **Authorization**: Role-based access control
- **CSRF Protection**: Cross-site request forgery protection
- **File Validation**: Comprehensive upload security
- **Input Sanitization**: XSS prevention and data validation
- **Secure Sessions**: Flask-Login session management

## 🧰 Utility Scripts

- **`init_db.py`**: Initialize database schema
- **`app/populate_sample_data.py`**: Create sample data for testing
- **`app/check_db_content.py`**: Inspect database content
- **`check_uploads.py`**: Validate file integrity and clean orphaned records

## 🚀 Deployment

### Production Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment instructions including:
- WSGI server configuration (Gunicorn)
- Database setup (PostgreSQL)
- Environment configuration
- Security considerations

### Quick Deployment with Gunicorn
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 run:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Add comments for complex logic
- Test all new features thoroughly
- Update documentation for new features

## 📄 License

This project is developed for academic purposes as part of the Web Technologies Laboratory course.

## 👥 Authors

StudyHub Development Team

## 🆘 Support

- **Documentation**: Check the inline code documentation
- **Issues**: Use the contact form within the application
- **Development**: Review the comprehensive code comments

## 🔄 Version History

- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Enhanced security and documentation
- **v1.2.0**: Production-ready with comprehensive restructuring

---

**Made with ❤️ for the academic community** 
