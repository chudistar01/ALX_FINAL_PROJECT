import os
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI='mongodb://localhost:27017/voter_database',
    )



    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    mongo.init_app(app)

    
    from .admin import admin_bp  
    from .voters import voters_bp  

  
    app.register_blueprint(admin_bp) 
    app.register_blueprint(voters_bp)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def say_hello():
        return "Hello, World!"


    @app.route('/test_db')
    def test_db():
        voter_count = mongo.db.voters.count_documents({})
        return f'Total registered voters: {voter_count}'

    return app
