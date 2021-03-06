import email
import email.mime
import email.mime.base
import email.mime.multipart
import email.mime.text
import smtplib
from email import encoders
from typing import List
import os
import configparser



def send_mail(to_address:str, subject:str, body:str, attach:List[str]=None) -> None:
    """Send an email using the given confiuration file

    Arguments:
        to_address {str} -- The recipient of the email
        subject {str} -- The subject of the email
        body {str} -- The body of the email

    Keyword Arguments:
        attach {List[str]} -- List of filenames to attach (default: {None})
        sendmail_config_file {str} -- Configuration file containing API keys etc. (default: {'/home/david/Code/pyutils/mail_config.txt'})

    Returns:
        None -- [description]
    """

    sendmail_config_file = os.path.join(os.path.dirname(__file__), 'sendmail_config.ini')

    with open(sendmail_config_file,'r') as cf:
        config = configparser.ConfigParser()
        config.read_file(cf)

    # Get the mail config from a file
    from_address = config['gmail']['email'].strip()
    from_password = config['gmail']['token'].strip()

    # Construct the message
    msg = email.mime.multipart.MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(email.mime.text.MIMEText(body, 'plain'))

    # Handle attachments
    if attach is not None:
        for attach_file in attach:
            attachment = open(attach_file, 'rb')
            part = email.mime.base.MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename={}'.format(attach_file))
            msg.attach(part)

    # Send the mail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, from_password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()
