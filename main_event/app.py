from flask import Flask
from config import Config
from models.pass_system import EventPassSystem
from routes.main import main_bp
from routes.pass_routes import pass_bp
from routes.sponsor_routes import sponsor_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize directories
Config.init_app()

# Initialize pass system
pass_system = EventPassSystem()

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(pass_bp)
app.register_blueprint(sponsor_bp)

if __name__ == '__main__':
    print("=" * 50)
    print("Event Pass System Starting...")
    print("=" * 50)
    print(f"Access the application at: http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)