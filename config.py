import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyArX83NY8DfVlIOr2rw2eL5ift7A5R_98c")
    BASE_DIR = BASE_DIR
    DATABASE = os.path.join(BASE_DIR, "instance", "interview.db")
    ADMIN_USER = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASS = os.getenv("ADMIN_PASS", "admin123")

    # misc (we don’t save media since no webcam/video required)
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    os.makedirs(INSTANCE_DIR, exist_ok=True)
