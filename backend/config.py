import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/news_books_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
