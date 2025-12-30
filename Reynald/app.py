from config import Config
import os
import re
import logging

# Base directory (absolute) — helps when running under PythonAnywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import ssl
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

# configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load config from Config
USE_CUSTOM_SMTP = Config.USE_CUSTOM_SMTP
SMTP_HOST = Config.SMTP_HOST
SMTP_PORT = Config.SMTP_PORT
SMTP_SECURE = Config.SMTP_SECURE
SMTP_USER = Config.SMTP_USER
SMTP_PASS = Config.SMTP_PASS
OWNER_EMAIL = Config.OWNER_EMAIL

# Basic sanitizers
def sanitize_header(v):
    return re.sub(r'[\r\n]+', ' ', str(v or '')).strip()

def sanitize_body(v):
    return re.sub(r'<script[\s\S]*?>[\s\S]*?<\/script>', '', str(v or ''), flags=re.I).strip()

def send_smtp_message(message: EmailMessage, envelope_from=None, to_addrs=None):
    if to_addrs is None:
        to_addrs = [message['To']]
    # Ensure credentials are present
    if not SMTP_USER or not SMTP_PASS:
        raise RuntimeError('SMTP_USER or SMTP_PASS not configured')
    if SMTP_SECURE and SMTP_PORT == 465:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as smtp:
            try:
                smtp.login(SMTP_USER, SMTP_PASS)
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.exception('SMTP login failed (SSL)')
                raise
            smtp.send_message(message, from_addr=envelope_from or message['From'], to_addrs=to_addrs)
    else:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            if not SMTP_SECURE:
                # no TLS
                pass
            else:
                smtp.starttls()
            try:
                smtp.login(SMTP_USER, SMTP_PASS)
            except Exception:
                logger = logging.getLogger(__name__)
                logger.exception('SMTP login failed (STARTTLS)')
                raise
            smtp.send_message(message, from_addr=envelope_from or message['From'], to_addrs=to_addrs)

@app.route('/')
def serve_main():
    return app.send_static_file('main.html')

# Fallback for SPA routes -> serve index.html
@app.route('/<path:unused>')
def fallback(unused):
    # If path maps to an existing file, let Flask static serve it automatically.
    # Otherwise, return index.html for SPA behavior.
    requested = os.path.join(app.static_folder, unused)
    if os.path.exists(requested) and os.path.isfile(requested):
        return app.send_static_file(unused)
    return app.send_static_file('index.html')

@app.route('/api/send-email', methods=['POST'])
def send_email():
    data = request.get_json() or {}
    fullname = data.get('fullname')
    email = data.get('email')
    message = data.get('message')

    if not fullname or not email or not message:
        return jsonify({'error': 'Missing fields'}), 400

    safe_fullname = sanitize_header(fullname)
    safe_email = sanitize_header(email)
    safe_message = sanitize_body(message)

    owner_addr = OWNER_EMAIL

    # Prepare owner email
    owner_msg = EmailMessage()
    owner_msg['To'] = owner_addr
    owner_msg['Subject'] = f"Contact Form: {safe_fullname} <{safe_email}>"

    if USE_CUSTOM_SMTP:
        owner_msg['From'] = f"{safe_fullname} <{safe_email}>"
        envelope_from = safe_email
    else:
        # Authenticated user as From; put visitor as Reply-To
        owner_msg['From'] = f"{safe_fullname} via {SMTP_USER} <{SMTP_USER}>"
        owner_msg['Reply-To'] = safe_email
        envelope_from = SMTP_USER

    owner_text = f"Name: {safe_fullname}\nEmail: {safe_email}\n\n{safe_message}"
    owner_html = f"<p><strong>Name:</strong> {safe_fullname}</p><p><strong>Email:</strong> <a href=\"mailto:{safe_email}\">{safe_email}</a></p><p>{safe_message.replace('\n','<br>')}</p>"

    owner_msg.set_content(owner_text)
    owner_msg.add_alternative(owner_html, subtype='html')

    try:
        send_smtp_message(owner_msg, envelope_from=envelope_from, to_addrs=[owner_addr])
        logger.info('Owner mail sent')
    except Exception as e:
        logger.exception('Owner mail failed')
        return jsonify({'error': 'Failed to send owner email'}), 500

    # Send auto-reply to visitor (does not include original message)
    try:
        conf_msg = EmailMessage()
        conf_msg['To'] = safe_email
        conf_msg['From'] = f"{SMTP_USER} <{SMTP_USER}>"
        conf_msg['Subject'] = 'Thank you for reaching out!'
        conf_text = f"Hi {safe_fullname},\n\nThank you for reaching out! I've received your message and will get back to you soon."
        conf_html = f"<p>Hi {safe_fullname},</p><p><strong>Thank you for reaching out!</strong> I've received your message and will get back to you soon.</p>"
        conf_msg.set_content(conf_text)
        conf_msg.add_alternative(conf_html, subtype='html')
        send_smtp_message(conf_msg, envelope_from=SMTP_USER, to_addrs=[safe_email])
        logger.info('Confirmation sent')
    except Exception as e:
        logger.warning('Confirmation failed: %s', e)

    return jsonify({'ok': True})

if __name__ == '__main__':
    port = int(os.getenv('PORT', '3000'))
    app.run(host='0.0.0.0', port=port)

# When deploying to PythonAnywhere, create a WSGI file that exposes the `app` object.
# Example `wsgi.py` content (set web app source folder to this project):
#
# import sys
# import os
# project_home = os.path.dirname(os.path.abspath(__file__))
# if project_home not in sys.path:
#     sys.path.insert(0, project_home)
# from app import app as application

