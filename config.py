import os 
from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY = "CLAVE SECRETA"
    SESSION_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://EdwinRivera:Yovani2002@localhost/DBidgs802'