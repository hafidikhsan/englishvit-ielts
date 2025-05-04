from app import create_app
from config import EvIELTSConfig

# Create Flask app
app = create_app()

# Main entry point for the application
if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = EvIELTSConfig.flask_run_port,
        debug = EvIELTSConfig.flask_debug == 1,
    )