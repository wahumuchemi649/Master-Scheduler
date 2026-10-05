# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}"
        f"@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    DB_SSL_CA = os.environ.get("DB_SSL_CA")  # only set in production
    if DB_SSL_CA:
        SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"ssl": {"ca": DB_SSL_CA}}}
    FRONTEND_ORIGINS = [
             o.strip().strip('"').strip("'").rstrip("/")
             for o in os.environ.get("FRONTEND_ORIGINS", "").split(",")
             if o.strip()
             ]
    # config.py, inside your Config class
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True