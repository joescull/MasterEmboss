import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def AutoEmail(ra,n,bn,dr,exception,msl,mel):
	fromaddr = 'joe.master.embot@gmail.com'
	toaddr = ra
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Build Processed"

	body = """Hi %s,

	Build %s has been completed and the images have been processed.
	The images and timelapses can be found at %s.

	"""%(n,bn,dr)
	if exception:
		body += """Please note, there are missing layers from the recording.
		Layers missing are pictures: %s through %s. Sorry for any trouble this may cause.

		"""%(msl,mel)
	body += """
	From Joseph Scull

	This was sent via script. If there are any issues with this please speak to me or drop me an email on joescull@hieta.biz"""
	
	msg.attach(MIMEText(body,'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr,'Botpasswordpleasedonthackme')
	text = msg.as_string()
	server.sendmail(fromaddr,toaddr,text)
	server.quit()