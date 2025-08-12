import os
import requests
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    """
    A service for handling external email APIs like Brevo.
    """
    def __init__(self):
        self.api_key = os.getenv("BREVO_API_KEY")
        if not self.api_key:
            print("Warning: Brevo API key (BREVO_API_KEY) not configured.")
        self.api_url = "https://api.brevo.com/v3/smtp/email"

    def send_otp(self, to_email: str, otp: str) -> bool:
        """Send OTP via Brevo. Returns True on success."""
        if not self.api_key:
            return False

        payload = {
            "sender": {"name": "JobBoost", "email": "no-reply@jobboost.com"},
            "to": [{"email": to_email}],
            "subject": "Your JobBoost OTP",
            "htmlContent": f"<p>Your verification code is <strong>{otp}</strong></p>",
        }
        headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Brevo send failed: {e}")
            return False
