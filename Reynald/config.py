from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Application configuration loaded from environment variables."""

    SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))

    SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD").replace(
        " ", ""
    ) 
    SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes")
    SMTP_FROM_ADDRESS = os.environ.get("SMTP_FROM_ADDRESS") or SMTP_USERNAME
    SMTP_FROM_NAME = os.environ.get("SMTP_FROM_NAME")

    USE_CUSTOM_SMTP = os.environ.get('USE_CUSTOM_SMTP', 'false').lower() == 'true'
    SMTP_HOST = SMTP_SERVER
    SMTP_PORT = SMTP_PORT
    SMTP_SECURE = SMTP_USE_TLS
    SMTP_USER = SMTP_USERNAME.strip() if SMTP_USERNAME else ''
    SMTP_PASS = SMTP_PASSWORD.replace(' ', '').strip() if SMTP_PASSWORD else ''
    OWNER_EMAIL = os.environ.get('OWNER_EMAIL', SMTP_FROM_ADDRESS)

