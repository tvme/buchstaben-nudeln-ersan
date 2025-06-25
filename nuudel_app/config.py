import os

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///nuudel.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False