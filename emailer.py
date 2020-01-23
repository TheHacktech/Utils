import email.utils
import smtplib
import sys
import time
import math
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
import numpy as np
import pandas as pd


LOGFILE = 'email_log.txt'
URL = 'http://santa.servebeer.com'
sender = 'team@hacktech.io'
passwd = 'pw here'

class User():
    # Ditto on fields
    def __init__(self, school, name, email, club, recipient_email=None):
        self.name = None if pd.isnull(name) else name
        # Your fields here!!
        self.email = email
        self.schoo = school
        self.club = club

def LOG(obj):
  with open(LOGFILE, 'a') as f:
    f.write('[' + time.strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(obj) + '\n')

def _getdate():
  return email.utils.formatdate(localtime=True)


def _sendemail(email):
  LOG('emailing ' + str(email[0]))
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()
  server.login(sender, passwd)
  server.sendmail(sender, email[0], email[1].as_string())
  server.quit()


def _getemails(allusers):
  emails = []
  for i in range(len(allusers)):
    person = allusers[i]
    
    name = person.name
    
    # MESSAGE HERE
    body = "Hi {}, ".format(name)

    body += """\n
My name is Ziyan and I am one of the head organizers at Hacktech.  We're really excited to hold Hacktech this year and would love to see more {} students attend! If you could pass on the following message, we'd really appreciate it.
Cheers,
Ziyan
--
Hi all,

We are excited to announce that Hacktech 2020, Caltech's annual interdisciplinary hackathon is accepting applications! You can find out more information and apply at http://hacktech.io/ !
The deadline to apply is Feburary 1st, and this year we have rolling admissions so apply as soon as possible!

Hacktech 2020 will be held at Caltech on March 6-8. Check out the FAQs on our website, https://hacktech.io/ or email us at team@hacktech.io if you have any questions.

Cheers,
Hacktech Team
        """.format(person.school)
    body = body.encode('ascii', 'ignore').decode('ascii')
    subj = 'Apply to Hacktech 2020!'

    email = [person.email1]

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email[0]
    msg['Subject'] = subj
    msg.attach(MIMEText(body))
    print("Sending msg to emails "+str(email)+" at company " + person.school)
    
    ### Here is an example of attaching something
    '''
     for f in ["SponsorshipPackage2020.pdf"]:
        with open(f, "rb") as fil:
            ext = f.split('.')[-1:]
            attachedfile = MIMEApplication(fil.read(), _subtype = ext)
            attachedfile.add_header(
                                    'content-disposition', 'attachment', filename=basename(f) )
    msg.attach(attachedfile)
    '''
    emails.append((email, msg))
  return emails

def _initialparse(infile):
    allusers = []
    # The specific names
    contact1 = df['Name'].values
    email1 = df['Email'].values
    school   = df['School'].values
    club      = df['Club'].values
    for i in range(df['School'].values.shape[0]):
        allusers.append(User(school[i], contact1[i], email1[i], club[i]))
    return allusers

if __name__ == '__main__':
    df = pd.read_csv('dump.csv', comment='#', encoding="ISO-8859-1")
    allusers = _initialparse('parse_out.txt')
    allemails = _getemails(allusers)
    for email in allemails:
        _sendemail(email)
        time.sleep(5)
