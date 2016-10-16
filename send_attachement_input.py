import sys
import smtplib

#All EMAIL imports adjusted for Python 3 libraries
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

import os

#Authentication info for the account sending the emails
USERNAME = "username"
PASSWORD = "password"

def sendMail(to, subject, text, files=[]):
    assert type(to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = USERNAME
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    
    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com:587') #Using the gmail smtp server
        server.ehlo_or_helo_if_needed()
        server.starttls()
        server.ehlo_or_helo_if_needed()
        server.login(USERNAME,PASSWORD)
        server.sendmail(USERNAME, to, msg.as_string())
        server.quit()

#sendmail function structured as sendMail([destination email], "Email Subject", "Email body text", [list of files to attach])
sendMail( ["recipient@email.com"],
        "Fridge under attack!",
        "Here's a picture of the perp!",
        [str(sys.argv[1])] )#Using sys.argv to pull in a file name passed through command line
