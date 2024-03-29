import time
import operator
import MySQLdb
import subprocess
import os
import re
import gTAF_config
import pandas as pd
import logging
import sys

class Report:


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
                    if "Requested Tests" in line:
                        print("")

            print(TEST_NAME[i])
            print(RESULT[i])
            print(DEVICE_TYPE[i])
            print(SERIAL[i])
            print(TIME_STAMP[i])
            print(JENKINS_ID[i])

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

    def _create_html_report(self,csv_file_path, html_file_path):
        logging.info("Creating html report for %s  at %s", csv_file_path, html_file_path)
        logging.info("Deleting %s", html_file_path)
        os.system("rm " + html_file_path)
        df = pd.read_csv(csv_file_path)
        # Save to file
        df.to_html(html_file_path)
        # Assign to string
        htmTable = df.to_html()

if __name__ == '__main__':
    id = None
    js_id = sys.argv

    if len(js_id) > 1:
        id = js_id[1]
        jenkins_job_name = js_id[2]
        test_bed_name = js_id[3]
        test_case_name = js_id[4]
    if id is not None and test_case_name is not None and test_bed_name is not None and jenkins_job_name is not None:
        report = Report()
        report._get_execution_results(id, test_bed_name, test_case_name, jenkins_job_name)
    else:
        print("Please pass the jenkins id in parameter!!!")
        exit()






