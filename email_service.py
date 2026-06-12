# email_service.py
# Sends confirmation emails when users register

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# ── Email settings from .env ───────────────────────────────────────────────────
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")


def send_confirmation_email(to_email: str, full_name: str, role: str):
    """
    Sends a welcome confirmation email after registration.
    Called automatically when a user or admin registers.
    """

    if not SMTP_EMAIL or not SMTP_PASSWORD:
        print(f"[EMAIL] Email not configured — skipping email to {to_email}")
        return

    try:
        # ── Build the email ────────────────────────────────────────────────────
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Welcome to Clinic Service API — Registration Confirmed ✅"
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email

        role_label = "Admin" if role == "admin" else "Patient"
        role_color = "#00c896" if role == "admin" else "#0ea5e9"

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #f4f4f4; padding: 30px;">
          <div style="max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08);">

            <!-- Header -->
            <div style="background: {role_color}; padding: 28px 32px; text-align: center;">
              <h1 style="color: {'#000' if role == 'admin' else '#fff'}; margin: 0; font-size: 22px;">
                🏥 Clinic Service API
              </h1>
              <p style="color: {'rgba(0,0,0,0.7)' if role == 'admin' else 'rgba(255,255,255,0.85)'}; margin: 6px 0 0; font-size: 14px;">
                Group H — Limkokwing University Sierra Leone
              </p>
            </div>

            <!-- Body -->
            <div style="padding: 32px;">
              <h2 style="color: #1a1a2e; margin: 0 0 12px;">Hello, {full_name}! 👋</h2>
              <p style="color: #555; font-size: 15px; line-height: 1.6;">
                Your account has been successfully created. Welcome to the
                <strong>Clinic Service API</strong> — Sierra Leone's clinic directory system.
              </p>

              <!-- Role Badge -->
              <div style="background: {role_color}15; border: 1px solid {role_color}40; border-radius: 8px; padding: 14px 18px; margin: 20px 0;">
                <p style="margin: 0; font-size: 14px; color: #333;">
                  <strong>Account Type:</strong>
                  <span style="color: {role_color}; font-weight: 700; margin-left: 8px;">
                    {role_label}
                  </span>
                </p>
                <p style="margin: 6px 0 0; font-size: 14px; color: #333;">
                  <strong>Email:</strong> {to_email}
                </p>
              </div>

              <!-- What they can do -->
              <p style="color: #555; font-size: 14px; margin-bottom: 8px;"><strong>What you can do:</strong></p>
              {''.join([f'<p style="color:#555;font-size:13px;margin:4px 0;">✅ ' + item + '</p>' for item in (
                  ["Add and manage clinics", "Add services to clinics", "Accept or decline appointments", "View system analytics", "See patient reviews"]
                  if role == "admin" else
                  ["Search and find clinics", "See clinic services and prices", "Write reviews for clinics", "Book doctor appointments", "View top rated clinics"]
              )])}

              <div style="margin: 24px 0; text-align: center;">
                <a href="http://127.0.0.1:8000/docs"
                   style="background: {role_color}; color: {'#000' if role == 'admin' else '#fff'}; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-weight: 700; font-size: 14px;">
                  Open Swagger UI →
                </a>
              </div>

              <p style="color: #999; font-size: 12px; text-align: center; margin-top: 24px; border-top: 1px solid #eee; padding-top: 16px;">
                This email was sent by Group H Clinic Service API<br/>
                PROG315 — Limkokwing University of Creative Technology, Sierra Leone<br/>
                Supporting SDG 3 — Good Health and Well-Being 🌍
              </p>
            </div>
          </div>
        </body>
        </html>
        """

        plain = f"""
Hello {full_name},

Your account has been successfully created on the Clinic Service API.

Account Type: {role_label}
Email: {to_email}

Welcome to Sierra Leone's clinic directory system!

Group H — PROG315 — Limkokwing University Sierra Leone
        """

        msg.attach(MIMEText(plain, "plain"))
        msg.attach(MIMEText(html, "html"))

        # ── Send email ─────────────────────────────────────────────────────────
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, msg.as_string())

        print(f"[EMAIL] Confirmation email sent to {to_email}")

    except Exception as e:
        # Don't crash the registration if email fails
        print(f"[EMAIL] Failed to send email to {to_email}: {str(e)}")
