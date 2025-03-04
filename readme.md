# TimeTracker Web Application

A web application to track time in 30-minute segments. Users can register, log in, and track their time entries throughout the day with a visual timeline interface.

## Features

- User registration and authentication with hashed passwords
- Create, read, update, and delete time entries
- Track time in 30-minute segments with visual timeline
- Drag-and-drop interface for creating and modifying time entries
- Multi-day entries that span across midnight
- Categorize entries with emoji-enhanced categories for quick recognition
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
- **Database Migrations**: Flask-Migrate

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd time_tracker
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
   python app.py
   # The database will be automatically created on first run
   ```

## Usage

1. Start the application:
   ```
   python app.py [--port PORT] [--host HOST]
   ```
   
   By default, the application runs on `127.0.0.1:5000`. On macOS, port 5000 may be used by AirPlay Receiver. 
   You can specify a different port:
   ```
   python app.py --port 8080
   ```

2. Open your browser and navigate to the URL shown in the terminal (e.g., `http://127.0.0.1:8080`)

3. Register a new account and start tracking your time!

## Using the Timeline

1. **Creating Entries**: Click and drag on the timeline to create a new time entry
2. **Moving Entries**: Drag an existing entry to move it to a different time
3. **Resizing Entries**: Drag the top or bottom handle of an entry to change its duration
4. **Multi-day Entries**: Drag the bottom handle past midnight to create entries that span multiple days
5. **Categorizing**: Select a category from the dropdown when creating or editing an entry
6. **Editing Details**: Click on an entry to open the edit modal with additional options

## Available Categories

The application includes the following emoji-enhanced categories:

- 💼 Work
- 🏠 Personal
- 👥 Meeting
- ☕ Break
- 📋 Administrative
- 💻 Development
- 🎨 Design
- 🔍 Research
- 📅 Planning
- 📚 Learning
- 🏋️ Exercise
- 📖 Reading
- ✍️ Writing
- ✈️ Travel

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

## Troubleshooting

- **Port 5000 in use**: On macOS, port 5000 is used by AirPlay Receiver. Use `--port 8080` to run on a different port.
- **Database errors**: If you encounter database errors, try deleting the `instance/timetracker.db` file and restart the application to recreate it.
- **Missing dependencies**: Ensure all dependencies are installed with `pip install -r requirements.txt`.

## Future Enhancements

- More detailed analytics and reports
- Additional category customization
- Export data to CSV/PDF
- Team/project tracking capabilities
- Mobile app integration

## License

This project is licensed under the MIT License - see the LICENSE file for details.