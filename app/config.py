class Config:
    """
    Configuration class for the Flask application.
    
    This class holds all the necessary configurations to set up the Flask
    application, including database settings, session secret key, and 
    compression settings.
    """

    # URI for the MySQL database (change the username, password, and host as needed)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:sapprogram2583@185.4.28.110:5000/sap'
    
    # Disables Flask-SQLAlchemy event system to reduce overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configures the size of the database connection pool (maximum number of connections)
    SQLALCHEMY_POOL_SIZE = 10
    
    # Configures the number of connections that can be created beyond the pool size
    SQLALCHEMY_MAX_OVERFLOW = 20
    
    # Configures the timeout (in seconds) before a connection is considered expired.
    SQLALCHEMY_POOL_TIMEOUT = 30
    
    # Configures the recycle time (in seconds) for database connections to prevent 
    # long-lived connections from becoming stale.
    SQLALCHEMY_POOL_RECYCLE = 1800
    
    # Secret key used by Flask for signing sessions and cookies.
    SECRET_KEY = 'your_secret_key'
    
    # Compression level for Flask-Compress. 9 is the highest compression (most CPU-intensive).
    COMPRESS_LEVEL = 9
