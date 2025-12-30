Gmail SMTP setup (Express + Nodemailer) — now includes Flask instructions

1) Create Gmail App Password (recommended)
   - Enable 2-Step Verification on your Google account
   - Go to: https://myaccount.google.com/security -> App passwords
   - Create a new app password (select Mail or Other) and copy the 16-character password

2) Add env vars
   - Copy `.env.example` to `.env` in the `Reynald/` folder
   - Fill values (for Flask):
     GMAIL_USER=your.email@gmail.com
     GMAIL_PASS=the_16_char_app_password
     # Optional custom SMTP
     USE_CUSTOM_SMTP=false
     SMTP_HOST=smtp.example.com
     SMTP_PORT=465
     SMTP_SECURE=true
     SMTP_USER=smtp_user@example.com
     SMTP_PASS=smtp_password
     OWNER_EMAIL=your.email@gmail.com
     PORT=3000

3) Install dependencies
   - Open terminal in `Reynald/` folder
   - Run: `pip install -r requirements.txt`

4) Start server (Flask)
   - Run: `python app.py`
   - Visit: http://localhost:3000/ (will serve `main.html` at root)

5) Test locally
   - Fill contact form and submit
   - If everything is correct, you'll receive the email in `OWNER_EMAIL` inbox and the sender receives an auto-reply.

6) Troubleshooting
   - Check server logs (console) for SMTP errors and messages like "Owner mail sent" or "Confirmation sent".
   - If your provider rejects the visitor `From` address, use a provider that allows arbitrary From/envelope settings or keep Reply-To behavior.

Notes
   - This repo now contains a Flask backend (`app.py`) which serves the site and provides `/api/send-email`.
   - Netlify cannot run the Flask server — host the Flask app on Render/Heroku/your VPS and deploy the static site separately (Netlify).
