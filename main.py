import json
import io
import os.path
import urllib.request
import smtplib
from email.mime.text import MIMEText
from ssl import SSLContext
from apscheduler.schedulers.blocking import BlockingScheduler

options_file = io.open('options.json')
options = json.loads(''.join(options_file.readlines()))
options_file.close()

scheduler = BlockingScheduler()
#load ssl context for emails
ssl_context = SSLContext()
ssl_context.load_default_certs()

def notify():
    if 'email' in options['notify']:
        msg = MIMEText("CK's page has updated!\n Check it out: %s" % options['ck_page'])
        msg['Subject'] = "CK's wepbages has updated!"
        msg['From'] = options['EMAILFrom']
        msg['To'] = options['EMAILTo']

        smtp = smtplib.SMTP_SSL(host=options['SMTPHost'], port=options['SMTPPort'], context=ssl_context)
        if options['SMTPUsername'] != '':
            try:
                smtp.login(options['SMTPUsername'], options['SMTPPassword'])
            except smtplib.SMTPAuthenticationError:
                print("Unable to auth to smtp server!")
        smtp.sendmail(options['EMAILFrom'], [options['EMAILTo']], msg.as_string())
        smtp.quit()

def timed_job():
    #first, let's get the page
    page = urllib.request.urlopen(options['ck_page'])
    page_text = page.read().decode('ascii')
    page.close()

    #Here, we check whether the cached scheduler exists or not
    if os.path.isfile(options['cached_page_name']):
        #check if the update webpage is the same, if not, notify the user somehow, then update it
        cached_page_file = io.open(options['cached_page_name'], mode='r+t')
        cached_page_text = ''.join(cached_page_file.readlines())

        if page_text != cached_page_text:
            notify()
            cached_page_file.seek(0)
            cached_page_file.truncate()
            cached_page_file.write(page_text)
        #otherwise, do nothing
        cached_page_file.close()
    else:
        #page does not exist, grab it and notify the user
        cached_page_file = io.open(options['cached_page_name'], mode='wt')
        cached_page_file.writelines(page_text)
        notify()

scheduler.add_job(timed_job, 'interval', seconds=int(options['interval_seconds']))

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass
