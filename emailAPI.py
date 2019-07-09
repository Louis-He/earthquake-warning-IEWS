import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

from dataAnalysis import *

def emailSend(receiver, title, message):
    sender = 'root@siweihe.tech'
    receivers = receiver  # receivers' email list

    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = formataddr(["IEWS_CA", sender])
    msgRoot['To'] = formataddr(["You", receivers])
    msgRoot['Subject'] = Header(title, 'utf-8')

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgAlternative.attach(MIMEText(message, 'html'))

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.set_debuglevel(True)
        smtpObj.ehlo('siweihe.tech')
        smtpObj.helo('siweihe.tech')
        smtpObj.starttls()
        smtpObj.ehlo('siweihe.tech')
        smtpObj.sendmail(sender, receivers, msgRoot.as_string())
        print("Email Sent")
    except smtplib.SMTPException:
        print("Error: EMAIL FAILED.")

def emailNotification(mag, startStr):
    if (mag >= 0.1):
        print("Gentle Earthquake.")
        msg = '<h2>Gentle Earthquake Possible now or in the near future</h2><br>Detail from SLA Station<br>'
        msg += 'Start Time: ' + startStr + '<br>'
        msg += 'station Magnitude: ' + str(mag) + '<br>'
        msg += '<br>### END OF MESSAGE ###<br>'
        msg += 'NOT verified by any human. Only for reference. DO NOT make life and death decision based on this message.<br>'
        title = "IEWS_GENTLE_QUAKEINFO"
    elif (mag >= 3.0):
        print("Shake possible now or in the near future.")
        msg = '<h2>Gentle Shake Possible now or in the near future</h2><br>Detail from SLA Station<br>'
        msg += 'Start Time: ' + startStr + '<br>'
        msg += 'station Magnitude: ' + str(mag) + '<br>'
        msg += '<br>### END OF MESSAGE ###<br>'
        msg += 'NOT verified by any human. Only for reference. DO NOT make life and death decision based on this message.<br>'
        title = "IEWS_GENTLE_QUAKEINFO"
    elif (mag >= 4.5):
        print("Medium Shake possible now or in the near future.")
        msg = '<h2>BE CALM AND TAKE COVER! Medium Shake Possible now or in the near future</h2><br>Detail from SLA Station<br>'
        msg += 'Start Time: ' + startStr + '<br>'
        msg += 'station Magnitude: ' + str(mag) + '<br>'
        msg += '<br>### END OF MESSAGE ###<br>'
        msg += 'NOT verified by any human. Only for reference. DO NOT make life and death decision based on this message.<br>'
        title = "IEWS_MEDIUM_QUAKEWATCH"
    elif (mag >= 6.0):
        print("Strong Shake possible now or in the near future.")
        msg = '<h2>TAKE COVER NOW! Strong Shake Possible now or in the near future</h2><br>Detail from SLA Station<br>'
        msg += 'Start Time: ' + startStr + '<br>'
        msg += 'station Magnitude: ' + str(mag) + '<br>'
        msg += '<br>###END OF MESSAGE ###<br>'
        msg += 'NOT verified by any human. Only for reference. DO NOT make life and death decision based on this message.<br><br>'
        title = "TAKE_COVER_NOW_IEWS_QUAKWARNING"

    if (mag >= 1.0):
        timeSent = UTCDateTime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        msg += 'AlertTime: ' + timeSent + '<br>Sent from Immediate Earthquake Warning System<br>'
        msg += '©Louis_He ©IEWS_CA<br>'

        ###
        #  emailSend(/* Receiver's email address here if you want to send notification */, title, msg)
        ###
        return msg