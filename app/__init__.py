import os
from dotenv import load_dotenv # need this cause .evn files are not automatically loaded by Python
load_dotenv() 

from flask import Flask
from app.routes.session_routes import session_bp

def create_app(test_config=None):
    # create the Flask instance and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # raw SQL approach: set default configuration that the app will use
    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_HOST='localhost',
        DB_USER='root',
        DB_PASSWORD='23456',
        DB_NAME='study_tracker'
    )
    
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