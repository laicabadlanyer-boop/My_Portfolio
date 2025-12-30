from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Application configuration loaded from environment variables."""

    # SMTP configuration (defaults set for Gmail App Password usage)
    SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
    # Gmail credentials - can be overridden via environment variables
    SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "abacialreynald5@gmail.com")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "wuub zrru bhog rgxh").replace(
        " ", ""
    )  # Gmail App Password (remove spaces)
    SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes")
    SMTP_FROM_ADDRESS = os.environ.get("SMTP_FROM_ADDRESS", "abacialreynald5@gmail.com") or SMTP_USERNAME
    SMTP_FROM_NAME = os.environ.get("SMTP_FROM_NAME", "Reynald Abacial")
    # Backwards-compatible names expected by app.py
    USE_CUSTOM_SMTP = os.environ.get('USE_CUSTOM_SMTP', 'false').lower() == 'true'
    SMTP_HOST = SMTP_SERVER
    SMTP_PORT = SMTP_PORT
    SMTP_SECURE = SMTP_USE_TLS
    SMTP_USER = SMTP_USERNAME.strip() if SMTP_USERNAME else ''
    SMTP_PASS = SMTP_PASSWORD.replace(' ', '').strip() if SMTP_PASSWORD else ''
    OWNER_EMAIL = os.environ.get('OWNER_EMAIL', SMTP_FROM_ADDRESS)
