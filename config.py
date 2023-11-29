import os

from decouple import config
from dotenv import load_dotenv


load_dotenv()


JWT_SECRET = config('SECRET_KEY')
JWT_ALGORITHM = config('ALGORITHM')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')