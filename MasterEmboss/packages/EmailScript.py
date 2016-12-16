import smtplib
import base64

def AutomateEmail():
	sender = 'joescull1@gmail.com'
	receivers = ['joescull1@gmail.com']

	message = """From: From Person <nidrelunep@throya.com>
	To: To Person <joescull1@gmail.com>
	Subject: SMTP e-mail test

	This is a script . Beep boop.
	"""
	try:
		smtpObj = smtplib.SMTP('localhost',1025)
		smtpObj.sendmail(sender,receivers,message)
		print("Sent Email!")
	except SMTPException:
		print("Error: Unable to send Email")