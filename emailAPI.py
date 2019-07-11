import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from setting import *

from dataAnalysis import *

def emailSend(receiver, title, message):
    sender = adminSender
    receivers = ""
    for singleReceiver in receiver:
        receivers += singleReceiver + ";"  # receivers' email list
    receivers = receivers[:-1]

    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = formataddr(["IEWS_CA", sender])
    msgRoot['To'] = formataddr(["You", receivers])
    msgRoot['Subject'] = Header(title, 'utf-8')

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgAlternative.attach(MIMEText(message, 'html'))

    fp = open('latest_CI.SLA..BHZ.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.set_debuglevel(True)
        smtpObj.ehlo(adminDomain)
        smtpObj.helo(adminDomain)
        smtpObj.starttls()
        smtpObj.ehlo(adminDomain)
        smtpObj.sendmail(sender, receiver, msgRoot.as_string())
        print("Email Sent")
    except smtplib.SMTPException:
        print("Error: EMAIL FAILED.")

def emailNotification(mag, startStr):
    if (mag >= 5.5):
        print("Strong Shake possible now or in the near future.")
        msg = '<h2>TAKE COVER NOW! Strong Shake Possible now or in the near future</h2><br>Detail from SLA Station<br>'
        title = "TAKE_COVER_NOW_IEWS_QUAKWARNING"
    elif (mag >= 4.5):
        print("Medium Shake possible now or in the near future.")
        msg = '<h2>BE CALM AND TAKE COVER! Medium Shake Possible now or in the near future</h2><br>Detail from SLA Station<br>'
        title = "IEWS_MEDIUM_QUAKEWATCH"
    elif (mag >= 3.0):
        print("Shake possible now or in the near future.")
        msg = '<h2>Shake Possible now or in the near future</h2><br>Detail from SLA Station<br>'
        title = "IEWS_GENTLE_QUAKEADVISORY"
    elif (mag >= 0.5):
        print("Gentle Earthquake.")
        msg = '<h2>Gentle Earthquake Possible now or in the near future</h2><br>Detail from SLA Station<br>'
        title = "IEWS_GENTLE_QUAKEINFO"

    if (mag >= 1.0):
        timeSent = UTCDateTime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        msg += 'Start Time: ' + startStr + ' UTC<br>'
        msg += 'station Magnitude: ' + str(mag) + '<br>'
        msg += '<br>NOT verified by any human. Only for reference. DO NOT make life and death decision based on this message.<br>'
        msg += 'AlertTime: ' + timeSent + '<br>Sent from Immediate Earthquake Warning System<br>'
        msg += '<img src="cid:image1"><br>'
        msg += '©Louis_He ©IEWS_CA<br><br>'

        msg += '<br>### END OF MESSAGE ###<br>'

        ###################################################
        #  emailSend: set everything at /* setting.py */  #
        ###################################################

        if (mag >= 3.0):
            emailSend(emailReceivers, title, msg)
        else:
            emailSend(admin, title, msg)
        return msg