import os

from flask import Flask

def create_app(test_config=None):
    # create the Flask instance and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # raw SQL approach: set default configuration that the app will use
    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_HOST='localhost',
        DB_USER='youruser',
        DB_PASSWORD='yourpassword',
        DB_NAME='study_tracker'
    )
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World'
    
    return app