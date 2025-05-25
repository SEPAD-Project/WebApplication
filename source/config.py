import os

class Config:
    """
    Base configuration for the Flask application.

    Contains database settings, session management, and compression level.
    """

    # Database connection URI (update credentials as needed)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:sapprogram2583@185.4.28.110:5000/sap'

    # Disable SQLAlchemy event system for performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLAlchemy connection pool settings
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 1800

    # Flask session and cookie signing key (⚠️ use env var in production)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')

    # Flask-Compress compression level (1-9)
    COMPRESS_LEVEL = 9

    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

