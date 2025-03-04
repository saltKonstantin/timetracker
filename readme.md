# TimeTracker Web Application

A simple web application to track time in 15-minute segments. Users can register, log in, and track their time entries throughout the day.

## Features

- User registration and authentication with hashed passwords
- Create, read, update, and delete time entries
- Track time in 15-minute segments or custom durations
- Weekly timeline view to visualize your time entries
- Analytics dashboard with charts and statistics
- Date navigation to view entries from different periods
- Responsive design that works on desktop and mobile

## Technology Stack

- **Backend**: Python with Flask framework
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login
- **Form Handling**: Flask-WTF

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd timetracker
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables (optional):
   ```
   # For development
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export SECRET_KEY=your-secret-key
   ```

5. Initialize the database:
   ```
   flask run
   # The database will be automatically created on first run
   ```

## Usage

1. Start the application:
   ```
   flask run
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000`

3. Register a new account and start tracking your time!

## Project Structure

```
time_tracker/
│
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── models.py              # Database models
├── forms.py               # Form classes for validation
├── routes/                # Route handlers
│   ├── __init__.py
│   ├── auth.py            # Authentication routes
│   └── time_entries.py    # Time tracking routes
│
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── time_entries/
│       ├── timeline.html      # Weekly timeline view
│       ├── analytics.html     # Analytics dashboard
│       └── entry_form.html    # Form for editing entries
│
├── static/                # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── instance/              # Instance-specific files
    └── timetracker.db     # SQLite database
```

## Future Enhancements

- More detailed analytics and reports
- Time entry categories/tags
- Export data to CSV/PDF
- Team/project tracking capabilities
- Mobile app integration

## License

This project is licensed under the MIT License - see the LICENSE file for details.