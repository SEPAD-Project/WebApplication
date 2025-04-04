from app import create_app

# Initialize the Flask application
app = create_app()

if __name__ == '__main__':
    """
    If the script is run directly, the Flask application will start 
    in debug mode for easier development and debugging.
    
    - `debug=True` enables Flask's debug mode, which provides detailed error pages 
      and automatically reloads the app when code changes.
    """
    app.run(debug=True)
