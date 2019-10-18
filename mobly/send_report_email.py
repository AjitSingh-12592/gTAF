import smtplib
import email.message
from email.mime.base import MIMEBase
from email import encoders
import cgi
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import os
import sys
import re
import gTAF_config
import pandas as pd
import logging
import csv
import time

def csv_to_html():
    """
    csv to html conversion.
    :return:
    """
    logging.info("Converting csv to html..")
    df = pd.read_csv(gTAF_config.execution_summary_csv_file)
    df.to_html(gTAF_config.html_report_file)
    htmTable = df.to_html()

def send_report_email(j_id=None):
    """
    Send execution report to configured email ids.
    :return: None
    """

    if j_id is not None and os.path.exists(gTAF_config.html_updated_report):
        copy_report = "cp " + gTAF_config.html_updated_report + " " + gTAF_config.bkp_log_path + "/gTAF_report_updated_" + str(j_id) + ".html"
        print(copy_report)
        os.system(copy_report)

    logging.info("Sending report email...")

    # Get total number of test cases entries in table
    filer_th_tags_cmd = "cat " + gTAF_config.html_report_file + " | grep '<th>[0-9]*[0-9]</th>'"
    sr_num, src_file = [], []
    th_tags = subprocess.check_output(filer_th_tags_cmd, shell=True)
    th_tags = th_tags.strip()
    th_tags = th_tags.split("\n")


    for i in range(0, len(th_tags)):
        tmp = th_tags[i]
        numbers = re.findall('\d+', tmp)
        index = int(numbers[0])
        sr_num.append(index + 1)

    # Increase cell number by 1 in html source
    f = open(gTAF_config.html_report_file, "r")
    for line in f:
        tag = re.findall('<th>\d+</th>', line)
        if len(tag) != 0:
            num = re.findall('\d+', tag[0])
            n = int(num[0])
            tmp = '<th>' + str((n + 1)) + '</th>'
            src_file.append(tmp)
        else:
            src_file.append(line)
    f.close()

    rm_cmd = "rm " + gTAF_config.html_updated_report
    os.system(rm_cmd)

    # Update 'FAIL' color code and add Sr. No. in html file and write update html source code
    for ln in src_file:
        fh = open(gTAF_config.html_updated_report, 'a')
        if '<td>FAIL</td>' in ln:
            ln = ln.replace('<td>FAIL</td>', '<td style="color: red">FAIL</td>')
        if '<th></th>' in ln:
            ln = ln.replace('<th></th>', '<th>Sr No.</th>')
        fh.write(ln)
        fh.write("\n")
    fh.close()

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
        print("Sending email to : ", gTAF_config.report_mail_to_list[i])
        s.login(msg['From'], password)
        s.sendmail(msg['From'], gTAF_config.report_mail_to_list[i], msg.as_string())
        print('Mail Successfully Sent, Please check it !!!!!')
    s.quit()

def execution_summary_dump():
    file_name = gTAF_config.execution_summary_csv_file
    fields = []
    rows = []
    pass_count = 0
    fail_count = 0
    skip_count = 0

    with open(file_name, 'r') as fl:
        data = csv.reader(fl)
        fields = data.next()
        for row in data:
            rows.append(row)

    for i in range(0, len(rows)):

        if rows[i][2] == 'PASS':
            pass_count += 1

        if rows[i][2] == 'FAIL':
            fail_count += 1

        if rows[i][2] == 'ERROR':
            skip_count += 1

    if pass_count + fail_count + skip_count == len(rows):
        pass
    else:
        print("\nError...Pass, Fail and skip test count mismatched with Total")

    print("\n####################################### Execution Summary #################################\n")
    print("TOTAL TEST EXECUTED:" + str(len(rows)))
    print("PASSED :" + str(pass_count))
    print("FAILED :" + str(fail_count))
    print("SKIPPED:" + str(skip_count))

    print("\n######################################## Detailed Summary ##################################\n")

    for i in range(0, len(rows)):
        print(str(i + 1) + ". " + rows[i][1] + ":" + rows[i][2])

def _send_mail():
    fromaddr = "pythontestmail527@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['Subject'] = "Automation Report attached !!"

    body_1 = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><META http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body><table border="1">
      <thead>
        <tr style="text-align:right">
          <th></th>
          <th>Jenkins ID</th>
          <th>Test Case</th>
          <th>Result</th>
          <th>Device Type</th>
          <th>Device Serial</th>
          <th>Date &amp; Time</th>
          <th>Log Path</th>
          <th>Exception</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>54</td>
          <td>test_merge_duplicates</td>
          <td>PASS</td>
          <td>AndroidDevice</td>
          <td>FA6BA0300749</td>
          <td>2019-07-24 16:46:50</td>
          <td>/gtaflog/test_merge_<wbr>duplicates/54</td>
          <td>No_Exception</td>
        </tr>
        <tr>
          <th>1</th>
          <td>54</td>
          <td>test_strong_match_for_<wbr>duplicates</td>
          <td>PASS</td>
          <td>AndroidDevice</td>
          <td>FA6BA0300749</td>
          <td>2019-07-24 16:48:09</td>
          <td>/gtaflog/test_strong_match_<wbr>for_duplicates/54</td>
          <td>No_Exception</td>
        </tr>
        <tr>
          <th>2</th>
          <td>54</td>
          <td>test_favourite_in_all_contact</td>
          <td>PASS</td>
          <td>AndroidDevice</td>
          <td>FA6BA0300749</td>
          <td>2019-07-24 16:49:06</td>
          <td>/gtaflog/test_favourite_in_<wbr>all_contact/54</td>
          <td>No_Exception</td>
        </tr>
        <tr>
          <th>3</th>
          <td>54</td>
          <td>test_google_play_service_<wbr>permission_revoke</td>
          <td>PASS</td>
          <td>AndroidDevice</td>
          <td>FA6BA0300749</td>
          <td>2019-07-24 16:50:37</td>
          <td>/gtaflog/test_google_play_<wbr>service_permission_r...</td>
          <td>No_Exception</td>
        </tr>
        <tr>
          <th>4</th>
          <td>54</td>
          <td>test_share_contacts</td>
          <td>PASS</td>
          <td>AndroidDevice</td>
          <td>FA6BA0300749</td>
          <td>2019-07-24 16:52:42</td>
          <td>/gtaflog/test_share_contacts/<wbr>54</td>
          <td>No_Exception</td>
        </tr>
      </tbody>
    </table></body></html>
    """

    body = cgi.escape(body_1).encode('ascii', 'xmlcharrefreplace')
    msg.attach(MIMEText(body, 'plain'))


    filename = "gTAF_Report.html"
    attachment = open('/gtaflog/gTAF_report.html', "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    to = ["aiytest11111@gmail.com"]

    for i in range(len(to)):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "Python@123")
        text = msg.as_string()
        s.sendmail(fromaddr, to[i], text)
        s.quit()
        print('Mail Successfully Sent, Please check it !!!!!')

if __name__ == '__main__':

    id = None
    csv_to_html()
    execution_summary_dump()
    js_id = sys.argv

    if len(js_id) > 1:
        id = js_id[1]
        print("Jenkins Run ID: ", id)

    if id is not None:
        send_report_email(id)
    else:
        send_report_email()