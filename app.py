from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from models import db, User
import argparse

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.time_entries import entries_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(entries_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the Flask application')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the application on')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to run the application on')
    args = parser.parse_args()
    
    app = create_app()
    app.run(debug=True, host=args.host, port=args.port)