import os


class Config:
    SECRET_KEY = 'test_secret_123_654'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'streetartapad@gmail.com'
    MAIL_PASSWORD = 'use own password'
#    SERVER_NAME = '127.0.0.1:5000'
