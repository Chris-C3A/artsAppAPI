import os

class Config:
    SECRET_KEY = os.urandom(32)
    UPLOAD_FOLDER = 'app/uploads/'
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
