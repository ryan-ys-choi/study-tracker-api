import os
from flask import Flask
from app.routes.session_routes import session_bp


def create_app(test_config=None):
    # create the Flask instance and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register session blueprint with the app
    app.register_blueprint(session_bp, url_prefix='/api')
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World'
    
    return app