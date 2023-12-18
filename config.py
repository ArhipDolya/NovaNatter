import os

from decouple import config
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = config('SECRET_KEY')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')