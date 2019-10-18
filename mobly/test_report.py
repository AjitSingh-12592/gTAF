import csv
import logging
import time
import sys
import re
import os
import subprocess
import operator
import pandas as pd
import MySQLdb
import yaml
import gTAF_config
import contacts_selectors

class Report:

    def _get_serial(self, test_bed, yaml_file):
        test_bed = test_bed
        file = yaml
        with open(file) as file:
            document = yaml.load(file)
            bed_list = document['TestBeds']
            for bed in bed_list:
                bed_name = bed['Name']
                if bed_name == test_bed:
                    print("Test bed matched..")
                    controller_info = bed['Controllers']
                    android_device = controller_info['AndroidDevice']
                    if len(android_device) == 1:
                        serial = android_device[0]['serial']
                        print("Serial : '%s'", serial)
                        return serial
                    else:
                        print("..")
                else:
                    print("Test bed not matched , looking for next test bed")

    def test_read_results(self, latest):

        TIME_STAMP = []
        RESULT = []
        TEST_NAME = []
        SERIAL = []
        DEVICE_TYPE = []

        time.sleep(5)
        test_bed = open("/home/edat/Desktop/mobly_setup/mobly_test/mobly/test_bed.txt", 'r')
        test_bed = test_bed.readlines()
        test_bed_name = test_bed[0].strip()

        file_path = "/tmp/logs/mobly/" + test_bed_name + "/latest/test_summary.yaml"

        #latest_result_dir = self.test_read_results()

        with open(file_path, 'r') as FH:
            for line in FH:
                if "Begin Time:" in line:
                    time_stamp = line.split(":")
                    time_stamp = time_stamp[1].strip()
                    '''
                    cmd = "date -d @" + str(time_stamp)
                    time_stamp = subprocess.check_output(cmd, shell=True)
                    time_stamp = str(time_stamp).strip()
                    time_stamp = time_stamp.replace(" ", "")
                    '''
                    TIME_STAMP.append(time_stamp)
                    time_stamp = None

                if "Result:" in line:
                    result = line.split(":")
                    result = result[1].strip()
                    RESULT.append(result)
                    result = None

                if "Test Name:" in line:
                    test_name = line.split(":")
                    test_name = test_name[1].strip()
                    TEST_NAME.append(test_name)
                    test_name = None

                # Controller info
                if "serial:" in line:
                    srl = line.split(":")
                    srl = srl[1].strip()
                    SERIAL.append(srl)
                    srl = None

                if "Controller Name:" in line:
                    device_type = line.split(":")
                    device_type = device_type[1].strip()
                    DEVICE_TYPE.append(device_type)
                    device_type = None

                #print(line)
                if "Requested Tests" in line:
                    print("")

        print(TEST_NAME[0])
        print(RESULT[0])
        print(DEVICE_TYPE[0])
        print(SERIAL[0])
        print(TIME_STAMP[0])


        with open("/home/edat/Desktop/mobly_setup/mobly_test/mobly/execution_summary.txt", 'w') as ex:
            ex.write("Test Name    |    ")
            ex.write("Result    |  ")
            ex.write("Device Type   |    ")
            ex.write("Device Serial    |  ")
            ex.write("Time   |   ")
            ex.write("\n")
            ex.write(TEST_NAME[0])
            ex.write(",")
            ex.write(RESULT[0])
            ex.write(",")
            ex.write(DEVICE_TYPE[0])
            ex.write(",")
            ex.write(SERIAL[0])
            ex.write(",")
            ex.write(TIME_STAMP[0])

        ex.close()

        f = open('/home/edat/Desktop/mobly_setup/mobly_test/mobly/report.html', 'w')
        code = "Mobly Test Report"
        html = """
            <html>
              <head>
              </head>
              <body bgcolor="white">
                <header>
                <h1 align="center", style="font-size:125%;">{code}</h1>
                </header>
                <table border="1", width="100%", bgcolor="grey">
                        <tr style="font-variant:small-caps;font-style:normal;color:black;font-size:15px;">
                        <th>S.No.</th>
                        <th>Test Name</th>
                        <th>Device Type</th>
                        <th>Device IDs</th>
                        <th>Result</th>
                        <th>Logs</th>
                        <th>Time</th>
                    </tr>
                    <tr style="font-size:12px;text-align:center">
                        <td>1</td>
                        <td>{TEST_NAME[0]}</td>
                        <td>{DEVICE_TYPE[0]}</td>
                        <td>{SERIAL}</td>
                        <td style="color:green;">{RESULT[0]}</td>
                        <td>
                          <a href="/home/edat/Desktop/mobly_setup/mobly_test/mobly/jenkins_logs/test_Settings_About_Items/28/console.log">
                            <div style="height:100%;width:100%"> View Logs</div>
                            </a>
                        </td>
                        <td>{TIME_STAMP[0]}</td>
                    </tr>
                </table>
              </body>
            </html>
            """.format(**locals())

        f.write(html)
        f.close()

    def _latest_subdir_result(self):

        test_bed = open("test_bed.txt",'r')
        test_bed = test_bed.readlines()
        test_bed_name = test_bed[0].strip() +  "/"
        alist = {}
        now = time.time()
        directory = os.path.join("/tmp/logs/mobly/", test_bed_name)
        os.chdir(directory)
        for file in os.listdir("."):
            if os.path.isdir(file):
                timestamp = os.path.getmtime(file)
                # get timestamp and directory name and store to dictionary
                alist[os.path.join(os.getcwd(), file)] = timestamp

        # sort the timestamp
        for i in sorted(alist.iteritems(), key=operator.itemgetter(1)):
            latest = "%s" % (i[0])
        # latest=sorted(alist.iteritems(), key=operator.itemgetter(1))[-1]
        print("Latest result folder : %s ", latest)
        return latest

    def _get_execution_results(self, jenkins_run_id=None, test_bed_name=None, test_case_name=None, jenkins_job_name=None):

        # Create dir for logs and copy logs
        os.chdir(gTAF_config.gTAF_home)
        create_log_dir_cmd = "sudo mkdir -p jenkins_logs/" + test_bed_name + "/" + \
                             test_case_name + "/" + jenkins_run_id
        permission_log_dir_cmd = "sudo chmod 777 -R jenkins_logs/" + test_bed_name + "/" + \
                             test_case_name + "/" + jenkins_run_id
        self._createdir_ifnotexist(create_log_dir_cmd)
        os.system(permission_log_dir_cmd)

        cat_log = "sudo cat " + gTAF_config.jenkins_home + "/jobs/" + jenkins_job_name + "/builds/" + jenkins_run_id + "/log >> jenkins_logs/" + test_bed_name + "/" + test_case_name + "/" + jenkins_run_id + "/console.log"
        os.system(cat_log)

        copy_log_cmd = "sudo cp -r /tmp/logs/mobly/" + test_bed_name + "/latest/* " + "jenkins_logs/" + test_bed_name + "/"  + test_case_name + "/" + jenkins_run_id
        os.system(copy_log_cmd)

        print("####################################### Jenkins command ##################################")
        print(create_log_dir_cmd)
        print(permission_log_dir_cmd)
        print(cat_log)
        print(copy_log_cmd)
        print("###########################################################################################\n")

        results_csv_file_path = gTAF_config.execution_summary_csv_file
        i = 0
        test_name = "default"

        JENKINS_ID = []
        TIME_STAMP = []
        RESULT = []
        TEST_NAME = []
        SERIAL = []
        DEVICE_TYPE = []
        STACKTRACE = []
        PATH = []
        OS_BUILD_VERSION = []

        #os.system("rm " + full_results_csv_file_path)
        ch_cmd = 'cd jenkins_logs/' + test_bed_name
        os.system(ch_cmd)
        log_home = os.getcwd()
        print("Current dir: ", log_home)

        flag = 0
        while flag == 0:
            del_path = log_home + "/jenkins_logs/" + test_bed_name + "/" + test_case_name + "/" + jenkins_run_id
            time.sleep(2)
            JENKINS_ID.append(jenkins_run_id)

            # copy logs to /home/edat/mobly_logs/
            src_path = log_home + "/jenkins_logs/" + test_bed_name + "/" + test_case_name + "/" + jenkins_run_id
            dst_path = gTAF_config.log_path + "/" + test_bed_name + "/" + test_case_name + "/"
            yml_file =  src_path + "/test_summary.yaml"

            print("####################################### TEST DATA #########################################")
            print("jenkins_job_name : ", jenkins_job_name)
            print("test_bed_name : ", test_bed_name)
            print("test_case_name : ", test_case_name)
            print("jenkins_run_id : ", jenkins_run_id)
            print("src_path path : ", src_path)
            print("dst_path path : ", dst_path)
            print("yml_file path : ", yml_file)
            print("del_path path :: ", del_path)
            print("###########################################################################################")

            stacktrace_logs = self._get_error_logs(yml_file)
            with open(yml_file, 'r') as FH:
                for line in FH:
                    if "Timestamp:" in line:
                        time_stamp = line.split(":")
                        time_stamp = time_stamp[1].strip()
                        #cmd = "date -d @" + str(time_stamp)
                        #time_stamp = subprocess.check_output(cmd, shell=True)
                        #time_stamp = str(time_stamp).strip()
                        #time_stamp = time_stamp.replace(" ", "")
                        time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(time_stamp)))
                        TIME_STAMP.append(time_stamp)
                        time_stamp = None

                    if "Result:" in line:
                        result = line.split(":")
                        result = result[1].strip()
                        if "ERROR" in result:
                            RESULT.append("FAIL")
                        else:
                            RESULT.append(result)
                        result = None

                    if "Requested Tests:" in line:
                        test_name = line.split(":")
                        test_name = test_name[1].strip()
                        test_name = test_name.replace("[","")
                        test_name = test_name.replace("]", "")
                        TEST_NAME.append(test_name)
                        test_name = None

                    # Controller info
                    if "serial:" in line:
                        srl = line.split(":")
                        srl = srl[1].strip()
                        SERIAL.append(srl)
                        srl = None

                    if "Controller Name:" in line:
                        device_type = line.split(":")
                        device_type = device_type[1].strip()
                        DEVICE_TYPE.append(device_type)
                        device_type = None

                    # print(line)
                    if "build_info:" in line:
                        r = re.findall('{.*:(.*),}*', line)
                        os_build_version = r[0].strip()
                        OS_BUILD_VERSION.append(os_build_version)
                        print("os_build_version :", os_build_version)
                        os_build_version = None

            print(TEST_NAME[i])
            print(RESULT[i])
            print(DEVICE_TYPE[i])
            print(SERIAL[i])
            print(TIME_STAMP[i])
            print(JENKINS_ID[i])
            print(OS_BUILD_VERSION[i])

            src_path = src_path.strip()
            dst_path = dst_path.strip()
            path_to_write = dst_path + jenkins_run_id
            PATH.append(path_to_write)
            time.sleep(1)
            with open(results_csv_file_path, 'a') as ex:
                ex.write(str(jenkins_run_id))
                ex.write(",")
                ex.write(TEST_NAME[i])
                ex.write(",")
                ex.write(RESULT[i])
                ex.write(",")
                ex.write(DEVICE_TYPE[i])
                ex.write(",")
                ex.write(SERIAL[i])
                ex.write(",")
                ex.write(TIME_STAMP[i])
                ex.write(",")
                ex.write(PATH[i])
                if "Stacktrace: nullTest Class:" not in stacktrace_logs:
                    ex.write(",")
                    STACKTRACE.append("Exception")
                    ex.write("Exception")
                else:
                    ex.write(",")
                    STACKTRACE.append("No Exception")
                    ex.write("No Exception")
                #ex.write(",")
                #ex.write(OS_BUILD_VERSION[i])
                ex.write("\n")

            ex.close()
            print(path_to_write)

            #################################
            # Insert test results to DB
            db = MySQLdb.connect(host=gTAF_config.sql_db_host, port=3306, user='root', passwd='password', db=gTAF_config.sql_db_name)
            cur = db.cursor()
            CSV_DATA= []

            CSV_DATA.append(jenkins_run_id)
            CSV_DATA.append(TEST_NAME[i])
            CSV_DATA.append(RESULT[i])
            CSV_DATA.append(DEVICE_TYPE[i])
            CSV_DATA.append(SERIAL[i])
            CSV_DATA.append(TIME_STAMP[i])
            CSV_DATA.append(PATH[i])
            CSV_DATA.append(STACKTRACE[i])

            print("Data to be inserted in DB :")
            print(CSV_DATA)
            sqlinsert = "INSERT INTO "+ gTAF_config.sql_db_table_name+" (JENKINS_ID,TEST_NAME, RESULT, DEVICE_TYPE, SERIAL, " \
                        "TIME_STAMP, PATH, STACKTRACE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sqlinsert, CSV_DATA)
            db.commit()
            # disconnect from server
            db.close()
            print('Test results inserted to DB successfully, closing the connection.')
            #################################
            # Insert test results to DB end

            if os.path.exists(dst_path):
                print("path exist already")
            else:
                print("creating path :", dst_path)
                os.system("mkdir -p " + dst_path)

            copy_cmd = "cp -r " + src_path + " " + dst_path
            print("copy_cmd : ", copy_cmd)
            os.system(copy_cmd)

            os.system("rm -rf " + del_path)
            i = i + 1
            time.sleep(1)
            flag = 1
        print("###########################################################################################")
        print(JENKINS_ID)
        print(TEST_NAME)
        print(RESULT)
        print(DEVICE_TYPE)
        print(SERIAL)
        print(TIME_STAMP)
        print(STACKTRACE)
        print(PATH)
        print("###########################################################################################")

    def _get_error_logs(self, file_path):

        stacktrace = ''
        error = ''
        with open(file_path) as file:
            content = file.read()
        #error = re.search(r'Details:.*?End Time:', content, re.DOTALL).group()
        stacktrace = re.search(r'Stacktrace:.*?Test Class:', content, re.DOTALL).group()

        if stacktrace !='':
            stacktrace = stacktrace.replace("\\n", '')
            stacktrace = stacktrace.replace("\\", '')
            stacktrace = stacktrace.replace("'\'", '')
            stacktrace = stacktrace.replace("\n", '')
            #error = error.replace("\\n", '')
            #error = error.replace("\\", '')
            #error = error.replace("'\'", '')
            #error = error.replace("\n", '')

            return stacktrace
        else:
            return ''

    def _createdir_ifnotexist(self, cmd):
        if os.path.exists(cmd):
            print("path exist already")
        else:
            print("creating path :", cmd)
            os.system(cmd)

    def _create_html_report(self, csv_file_path, html_file_path):
        logging.info("Creating html report for %s  at %s", csv_file_path, html_file_path)
        logging.info("Deleting %s", html_file_path)
        os.system("rm " + html_file_path)
        df = pd.read_csv(csv_file_path)
        # Save to file
        df.to_html(html_file_path)
        # Assign to string
        htmTable = df.to_html()

    def csv_to_html(self):
        """
        csv to html conversion.
        :return:
        """
        logging.info("Converting csv to html..")
        df = pd.read_csv(gTAF_config.execution_summary_csv_file)
        df.to_html(gTAF_config.html_report_file)
        htmTable = df.to_html()

    def update_html_report(self, j_id=None):
        """
        Send execution report to configured email ids.
        :return: None
        """

        if j_id is not None and os.path.exists(gTAF_config.html_updated_report):
            copy_report = "cp " + gTAF_config.html_updated_report + " " + gTAF_config.bkp_log_path + "/gTAF_report_updated_" + str(
                j_id) + ".html"
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

        '''
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
        '''

    def execution_summary_dump(self):
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
        print("\n############################################################################################\n\n")

    def get_contact_app_version(self, dev_id):
        contact_app_get_cmd = "adb -s " + dev_id + " shell dumpsys package " + \
                              contacts_selectors.CONTACTS_PKG + " | grep versionName"
        contact_app_version = subprocess.check_output(contact_app_get_cmd, shell=True)
        contact_app_version = contact_app_version.split("\n")
        contact_app_version[0] = contact_app_version[0].strip()
        #print("---:", contact_app_version[0])
        if 'versionName=' in contact_app_version[0]:
            contact_app_version = contact_app_version[0].split("=")
            #print("Contact app version : ", contact_app_version[1])

        return contact_app_version[1]

    def get_build_number(self, dev_id):

        android_build_number_cmd = "adb -s " + dev_id + " shell getprop ro.product.build.id"
        build_version = subprocess.check_output(android_build_number_cmd, shell=True)
        build_version = build_version.strip()
        print("build_version:", build_version)
        return build_version

    def get_android_version(self, dev_id):

        android_version_cmd = "adb -s " + dev_id + " shell getprop ro.build.version.release"
        android_version = subprocess.check_output(android_version_cmd, shell=True)
        android_version = android_version.strip()
        android_version = android_version.encode("ascii")
        print("android_version : ", android_version)
        return android_version



if __name__ == '__main__':
    """
    Steps:
    1. Get args from command line Jenkins
    2. Extract test name, test bed name, jenkins id, job name etc.
    3. Get execution results from default mobly logs, read logs, 
        parse logs, extract logs, insert to Db, write to csv file
    4. csv to html conversion.
    
    5. Print execution summary on console from csv file
    6. Modify html file to updated one, read it and send email to configured email ids
    command : sudo python test_report.py ${BUILD_NUMBER} ${JOB_NAME} 
    GTAF_TEST_BED_CONTACT test_strong_match_for_duplicates
    """


    id = None
    js_id = sys.argv

    if len(js_id) > 1:
        id = js_id[1]
        jenkins_job_name = js_id[2]

        test_bed_name = js_id[3]
        test_case_name = js_id[4]
    else:
        print("Insufficient arguments !!!!")
        exit()

    report = Report()
    if id is not None and test_case_name is not None and test_bed_name is not None and jenkins_job_name is not None:
        report._get_execution_results(id, test_bed_name, test_case_name, jenkins_job_name)
    else:
        print("Please provide valid arguments in test_report.py !!!")
        exit()

    report.csv_to_html()

    #report.execution_summary_dump()

    if len(js_id) > 1:
        print("Jenkins Run ID: " + str(id))

    if id is not None:
        report.update_html_report(id)
    else:
        report.update_html_report()
