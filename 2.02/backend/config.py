import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
UPLOAD_FOLDER = os.path.join(BACKEND_DIR, 'uploads')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'bengaluru-gba-nambike-nakshe-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f"sqlite:///{os.path.join(BACKEND_DIR, 'bengaluru_sanctions.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB max upload for CAD files / PDFs
    JSON_SORT_KEYS = False
