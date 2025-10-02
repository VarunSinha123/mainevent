import os
from pathlib import Path

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # File paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / 'data'
    STATIC_DIR = BASE_DIR / 'static'
    PASSES_DIR = STATIC_DIR / 'passes'
    SPONSORS_DIR = STATIC_DIR / 'sponsors'
    POWERED_BY_DIR = STATIC_DIR / 'powered_by'
    
    # Database
    DATABASE_FILE = DATA_DIR / 'passes_database.json'
    
    # Event settings
    DEFAULT_EVENT_NAME = 'SAVORA'
    DEFAULT_EVENT_DATE = 'DECEMBER 31ST'
    DEFAULT_VENUE = 'Swagatam Banquet Hall, Harmu, Ranchi'
    
    # Pass design settings
    PASS_WIDTH = 1200
    PASS_HEIGHT = 400
    
    # Powered by settings
    POWERED_BY_NAME = 'rave.live'
    POWERED_BY_LOGO = 'rave_logo.png'  # Place in static/powered_by/
    
    @classmethod
    def init_app(cls):
        """Initialize application directories"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.PASSES_DIR.mkdir(parents=True, exist_ok=True)
        cls.SPONSORS_DIR.mkdir(parents=True, exist_ok=True)
        cls.POWERED_BY_DIR.mkdir(parents=True, exist_ok=True)