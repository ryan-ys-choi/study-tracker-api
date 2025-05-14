import os
from flask import Flask
from app.routes.session_routes import session_bp
from app.db import close_db


def create_app(test_config=None):
    # create the Flask instance and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_mapping(
            SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
            DATABASE_HOST=os.getenv('DB_HOST'),
            DATABASE_USER=os.getenv('DB_USER'),
            DATABASE_PASSWORD=os.getenv('DB_PASSWORD'),
            DATABASE_NAME=os.getenv('DB_NAME'),
        )
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register database cleanup
    app.teardown_appcontext(close_db)
    
    # Register session blueprint with the app
    app.register_blueprint(session_bp, url_prefix='/api/v1')
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World'
    
    return app