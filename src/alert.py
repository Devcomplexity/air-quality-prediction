import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client

def send_alert_email(area, aqi_value):
    recipient = "authority@example.com"
    subject = f"URGENT: Hazardous AQI Alert for {area}, Delhi"
    body = f"""
    Dear Authority,

    Predicted AQI for {area} is {aqi_value}, which is Hazardous.
    Immediate action is recommended.

    Regards,
    Delhi Air Quality Prediction System
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "your_email@example.com"
    msg["To"] = recipient

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_email@example.com", "your_app_password")
        server.send_message(msg)

def send_sms_alert(area, aqi_value):
    account_sid = "your_twilio_sid"
    auth_token = "your_twilio_token"
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=f"Hazardous AQI {aqi_value} detected in {area}. Stay indoors!",
        from_="whatsapp:+14155238886",
        to="whatsapp:+91XXXXXXXXXX"
    )
