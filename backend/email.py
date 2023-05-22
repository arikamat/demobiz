import smtplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

from dotenv import load_dotenv

import os

load_dotenv()

EMAIL_ADD = os.environ.get("EMAIL_ADD")
EMAIL_PWD = os.environ.get("EMAIL_PWD")


class Emailer:
	_instance = None
	

	def __init__():
		raise RuntimeError("Call instance() instead")

	@classmethod
	def instance(cls):
		if cls._instance is None:
			cls._instance = cls.__new__(cls)
			# Put any initialization here.
	
		return cls._instance

	def send_email_2_df(self, receiver_email, subject, df1, df2, df3 ):
		# Implement your email sending logic here
		# For example, using smtplib to send the email
		# smtp_server = 'smtp.gmail.com'
		# smtp_port = 587
		smtp_server = 'smtp.office365.com'
		smtp_port = 587
		sender_email = EMAIL_ADD
		sender_password = EMAIL_PWD
		body = 'Attached are the CSV files.'
		csv1 = df1.to_csv(index = False)
		csv2 = df2.to_csv()
		csv3 = df3.to_csv(index = False)
  
		message = MIMEMultipart()
		message['From'] = sender_email
		message['To'] = receiver_email
		message['Subject'] = subject
  
		attachment1 = MIMEBase('application', 'octet-stream')
		attachment1.set_payload(csv1)
		encoders.encode_base64(attachment1)
		attachment1.add_header('Content-Disposition', 'attachment', filename='businesses.csv')
		message.attach(attachment1)
  
		attachment2 = MIMEBase('application', 'octet-stream')
		attachment2.set_payload(csv2)
		encoders.encode_base64(attachment2)
		attachment2.add_header('Content-Disposition', 'attachment', filename='summary.csv')
		message.attach(attachment2)
  
		attachment3 = MIMEBase('application', 'octet-stream')
		attachment3.set_payload(csv3)
		encoders.encode_base64(attachment3)
		attachment3.add_header('Content-Disposition', 'attachment', filename='demographics.csv')
		message.attach(attachment3)

		message.attach(MIMEText(body, 'plain'))
		# Connect to the SMTP server
		t = time.time()
		status = False
		while not status and time.time() < t + 60:
			try:
				with smtplib.SMTP(smtp_server, smtp_port) as server:
					server.starttls()
					server.login(sender_email, sender_password)

					# Send the email
					server.send_message(message)
					return
			except:
				continue
		print("Email was not able to sent")
