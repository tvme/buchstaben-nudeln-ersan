from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SERVER_NAME = 'localhost:5000'
    PREFERRED_URL_SCHEME = 'http'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///nuudel.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ('Nuudel Game', os.getenv("MAIL_USERNAME"))
    # Время жизни токена для подтверждения email (например, 1 час)
    TOKEN_MAX_AGE_SECONDS = 3600