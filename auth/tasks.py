from celery_config import app
from .email_sender import send_email


@app.task
def send_registration_email(user_email):
    send_email(user_email, "Welcome to NovaNatter!", "Thank you for registering.")