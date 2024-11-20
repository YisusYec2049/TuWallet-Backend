import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'jEspinosa2077')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'mysql+pymysql://root@localhost/tuwallet'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
