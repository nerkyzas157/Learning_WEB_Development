import requests  # type: ignore
from twilio.rest import Client  # type: ignore
from dotenv import dotenv_values  # type: ignore
import smtplib

config = dotenv_values(".env")

# Created a class to send notifications about cheap flights
# class NotificationManager:
#     def __init__(self):
#         ACCOUNT_SID = config["TWILIO_ACC_SID"]
#         AUTH_TOKEN = config["TWILIO_AUTH_TOKEN"]
#         self.twilio_ph_num = config["TWILIO_PHONE"]
#         self.target_ph_num = config["TARGET_PHONE"]
#         self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

#     def send_sms(self, msg_body):
#         self.client.messages.create(
#             from_=self.twilio_ph_num, body=msg_body, to=self.target_ph_num
#         )


# Created a class to send emails to everyone who filled out the form
class NotificationManager:
    def __init__(self):
        self.smtp_email = config["SMTP_EMAIL"]
        self.smtp_pass = config["SMTP_APP_PASS"]

    def send_email(self, email, email_text):
        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=self.smtp_email, password=self.smtp_pass)
        connection.sendmail(
            from_addr=self.smtp_email,
            to_addrs=email,
            msg=email_text,
        )
