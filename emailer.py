import smtplib
from email.message import EmailMessage
from time import sleep
import imghdr
from typing import List

class Emailer:
    def __init__(self, sender_email: str, email_password: str):
        self.sender_email = sender_email
        self.email_password = email_password
        self.mail = EmailMessage()

    def set_content(self, subject: str, sender_email: str, recipient_emails: List[str], email_content: str):
        self.mail['Subject'] = subject
        self.mail['From'] = sender_email
        self.mail['To'] = ', '.join(recipient_emails)
        self.mail.add_header('Content-Type', 'text/html')
        self.mail.set_payload(email_content.encode('utf-8'))

    def attach_images(self, image_list: List[str]):
        for image in image_list:
            with open(image, 'rb') as file:
                data = file.read()
                image_type = imghdr.what(file.name)
                file_name = file.name
            self.mail.add_attachment(data, maintype='image', subtype=image_type, filename=file_name)

    def attach_files(self, file_list: List[str]):
        for file in file_list:
            with open(file, 'rb') as a:
                data = a.read()
                file_name = a.name
            self.mail.add_attachment(data, maintype='application', subtype='octet-stream', filename=file_name)

    def send_email(self, seconds_interval: int = 0):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user=self.sender_email, password=self.email_password)
            smtp.send_message(self.mail)
            if seconds_interval:
                sleep(seconds_interval)

# Example Usage:
emailer = Emailer('your_email@gmail.com', 'your_app_password')
emailer.set_content('Hello', 'your_email@gmail.com', ['recipient1@example.com'], '<p>This is the email body.</p>')
emailer.attach_images(['image1.jpg', 'image2.png'])
emailer.attach_files(['document1.pdf', 'document2.txt'])
emailer.send_email()
