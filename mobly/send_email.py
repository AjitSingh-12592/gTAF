import smtplib
import email.message
import subprocess
import gTAF_config
import time

# Fetch date
date_time = subprocess.check_output('date', shell=True)
date_time = date_time.split(' ')
tmp = date_time[0] + '_' + date_time[2] + '_' + date_time[1]

# Read html source and send email
with open(gTAF_config.html_updated_report) as input_file:
    html_src = input_file.read()
msg = email.message.Message()
msg['Subject'] = 'gTAF_Test_Automation_Report_' + tmp
msg['From'] = gTAF_config.sender_mail
password = gTAF_config.sender_mail_pwd
msg.add_header('Content-Type', 'text/html')
msg.set_payload(html_src)
s = smtplib.SMTP(gTAF_config.smtp_server)
s.starttls()
for i in range(len(gTAF_config.report_mail_to_list)):
    # Login Credentials for sending the mail
    print("Sending email to : " + gTAF_config.report_mail_to_list[i])
    s.login(msg['From'], password)
    s.sendmail(msg['From'], gTAF_config.report_mail_to_list[i], msg.as_string())
    print('Mail Successfully Sent, Please check it !!!!!')
s.quit()
