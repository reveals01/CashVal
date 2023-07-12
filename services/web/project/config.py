import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SECRET_KEY = 'secret-key-goes-here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
    UPLOAD_FOLDER = 'FILES/UPLOADS'
    DB_DOCUMENTS='FILES/DB_DOCUMENTS'
    EXPORTS='FILES/EXPORTS'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    SITE_NAME = 'Produits structurés'

