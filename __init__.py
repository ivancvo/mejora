from flask import Flask
import cloudinary 
import cloudinary.uploader
import cloudinary.api

def create_app(config_name):
    app = Flask(__name__)
    cloudinary.config(
        cloud_name = 'docnct4ym',
        api_key = '639257364567225',
        api_secret = 'aJWn9YkGF0Q8ITDaeij7A5_YUdE'
    )
    app.config['SECRET_KEY'] = 'ivanb1227'
    app.config['JWT_SECRET_KEY'] = 'ivancho1227'
    USER_DB = 'root'
    PASS_DB = '1227'
    URL_DB = 'localhost'
    NAME_DB = 'alquiler'
    FULL_URL_DB =  f'mysql+pymysql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'                                                                                                                                
    app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_RUN_PORT'] = 5001
    return app