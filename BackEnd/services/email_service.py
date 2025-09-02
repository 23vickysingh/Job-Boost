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

    def send_contact_confirmation(self, to_email: str, name: str, subject: str, contact_type: str) -> bool:
        """Send contact form submission confirmation via Brevo. Returns True on success."""
        if not self.api_key:
            return False

        # Create a professional confirmation email
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8f9fa;">
            <div style="background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2563eb; margin: 0; font-size: 28px;">JobBoost</h1>
                    <p style="color: #6b7280; margin: 5px 0 0 0;">Your Smart Job-Hunting Assistant</p>
                </div>
                
                <h2 style="color: #1f2937; margin-bottom: 20px;">Thank You for Contacting Us!</h2>
                
                <p style="color: #4b5563; line-height: 1.6; margin-bottom: 20px;">Dear {name},</p>
                
                <p style="color: #4b5563; line-height: 1.6; margin-bottom: 20px;">
                    Thank you for reaching out to us regarding your <strong>{contact_type}</strong> inquiry. 
                    We have successfully received your message about "<strong>{subject}</strong>" and our team will review it carefully.
                </p>
                
                <div style="background-color: #f3f4f6; padding: 20px; border-radius: 6px; margin: 20px 0;">
                    <h3 style="color: #1f2937; margin: 0 0 10px 0; font-size: 16px;">What happens next?</h3>
                    <ul style="color: #4b5563; margin: 0; padding-left: 20px; line-height: 1.6;">
                        <li>Our support team will review your message within 24 hours</li>
                        <li>You'll receive a personalized response based on your inquiry type</li>
                        <li>For urgent matters, we typically respond within 4-6 hours</li>
                    </ul>
                </div>
                
                <p style="color: #4b5563; line-height: 1.6; margin-bottom: 20px;">
                    We appreciate your interest in JobBoost and look forward to helping you with your job search journey.
                </p>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                    <p style="color: #6b7280; font-size: 14px; margin: 0;">
                        Best regards,<br>
                        <strong>The JobBoost Team</strong>
                    </p>
                </div>
                
                <div style="text-align: center; margin-top: 20px;">
                    <p style="color: #9ca3af; font-size: 12px; margin: 0;">
                        This is an automated confirmation email. Please do not reply directly to this message.
                    </p>
                </div>
            </div>
        </div>
        """

        payload = {
            "sender": {"name": "JobBoost Support", "email": "support@jobboost.com"},
            "to": [{"email": to_email, "name": name}],
            "subject": f"Thank you for contacting JobBoost - We've received your {contact_type} inquiry",
            "htmlContent": html_content,
        }
        headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Brevo contact confirmation send failed: {e}")
            return False
