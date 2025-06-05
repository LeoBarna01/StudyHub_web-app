# StudyHub - Academic Document Sharing Platform

StudyHub is a modern web application built with Flask that enables students to share, discover, and manage academic documents in a collaborative environment. The platform provides a secure and user-friendly interface for uploading, categorizing, and searching educational resources.

## 📋 Project Description and Goals

**StudyHub** is designed as a collaboration and resource platform specifically for college students. The main goals of this project are:

- **Document Sharing**: Enable university students to share notes, learning materials, and exam preparation resources
- **Collaborative Learning**: Enhance both individual and collaborative study organization and effectiveness
- **Academic Resource Management**: Provide a centralized platform for organizing and accessing educational content
- **User-Friendly Experience**: Offer an intuitive interface with responsive design for optimal user experience

### Target Audience
University students aged 18-30, enrolled in bachelor's and master's degree programs.

### Key Features
- Secure user authentication and profile management
- Document upload with comprehensive validation
- Advanced search functionality with filters
- Favorites system for frequently accessed documents
- Contact forms for support and feedback
- Mobile-responsive design using Bootstrap 5

## 🚀 Instructions for Running the Web Application

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Installation and Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StudyHub_web-app
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
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

### Configuration
The application uses environment variables for configuration. Make sure to set up your environment properly before running the application.

## 👥 Team Contributions

**Leonardo** and **Cesare** developed this web application collaboratively, working together on all aspects of the project:

- **Shared Development**: Both team members contributed equally to the entire development process
- **Backend Development**: Joint work on Flask application structure, database models, routing, and business logic
- **Frontend Development**: Collaborative effort on HTML templates, CSS styling, JavaScript functionality, and responsive design
- **Full-Stack Integration**: Combined efforts in connecting frontend and backend components
- **Testing and Debugging**: Shared responsibility for quality assurance and bug fixes

The development approach emphasized pair programming and collaborative problem-solving, ensuring both team members gained comprehensive experience across all aspects of web development.

## 🛠️ Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite (development)
- **Development Tools**: Python 3.11, Flask CLI, Git

## 📁 Project Structure

```
StudyHub_web-app/
├── .flaskenv              # Flask environment configuration
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
├── Description_Project_LWT.md # Course project description
├── check_uploads.py       # Upload validation utility script
├── config.py              # Application configuration
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── run.py                 # Application entry point
├── app/                   # Main application package
│   ├── __init__.py        # Package initialization
│   ├── models.py          # Database models
│   ├── check_db_content.py # Database content checker
│   ├── populate_sample_data.py # Sample data population script
│   ├── auth/              # Authentication module
│   │   ├── __init__.py
│   │   ├── form.py
│   │   └── routes.py
│   ├── form/              # Forms module
│   │   ├── __init__.py
│   │   ├── form.py
│   │   └── forms.py
│   ├── main/              # Main application routes
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   └── main.py
│   ├── upload/            # File upload functionality
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── upload.py
│   │   └── utils.py
│   └── view/              # View-related functionality
│       ├── __init__.py
│       ├── utils.py
│       └── view.py
├── static/                # Static files (CSS, JS, images)
│   ├── css/               # Stylesheets
│   │   ├── authenticated_styles.css
│   │   ├── custom.css
│   │   └── style.css
│   ├── images/            # Image assets
│   │   ├── Ask&Discuss.jpg
│   │   ├── Browse&Discover.jpg
│   │   ├── hero-illustration.webp
│   │   ├── logo.png
│   │   ├── logo.svg
│   │   └── Upload_Resources.jpg
│   ├── js/                # JavaScript files
│   │   ├── custom.js
│   │   ├── main.js
│   │   └── script.js
│   └── profile_pics/      # Default profile pictures
│       └── default_avatar.jpg
├── templates/             # HTML templates
│   ├── auth/              # Authentication templates
│   │   ├── login.html
│   │   ├── profile.html
│   │   └── register.html
│   ├── errors/            # Error page templates
│   │   ├── 404.html
│   │   └── 500.html
│   ├── form/              # Form templates
│   │   └── question_form.html
│   ├── main/              # Main page templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── home.html
│   ├── upload/            # Upload templates
│   │   └── upload.html
│   └── view/              # View templates
│       ├── favorites.html
│       ├── search.html
│       ├── uploaded.html
│       └── partials/
│           ├── footer.html
│           └── navbar.html
├── uploads/               # User uploaded files
│   ├── documents/         # Document uploads
│   └── profile_pics/      # User profile pictures
└── migrations/            # Database migration files
    ├── alembic.ini
    ├── env.py
    ├── README
    └── script.py.mako
```

## 🔧 Development Features

- **User Authentication**: Secure login and registration system
- **File Upload**: Support for various document formats with validation
- **Search Functionality**: Advanced search with filtering options
- **Responsive Design**: Mobile-friendly interface
- **Database Management**: SQLAlchemy ORM with migration support
- **Error Handling**: Custom error pages and validation

## 📄 License

This project is developed for academic purposes as part of the Web Technologies Laboratory course.