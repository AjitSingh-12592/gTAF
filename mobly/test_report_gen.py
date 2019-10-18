import time
import MySQLdb
import os
import re
import gTAF_config
import sys



class Report:

    def get_execution_results(self, test_bed_name=None, test_case_name=None, job_id=None):
        mkdir = 'mkdir -p '
        print("PAth checking----------------------")
        print(os.path.exists(gTAF_config.log_path + test_bed_name + '/' + test_case_name+'/' + job_id + '/'))
        if os.path.exists(gTAF_config.log_path + test_bed_name + '/' + test_case_name+'/' + job_id + '/'):
            print("Path already exists")
        else:
            print("PAth creating----------------------")
            print("creating "+gTAF_config.log_path + test_bed_name + '/' + test_case_name+'/' + job_id + '/')
            os.system(mkdir + gTAF_config.log_path + test_bed_name + '/' + test_case_name+'/' + job_id)

        log_home = os.getcwd()

        results_csv_file_path = log_home + '/execution_summary.csv'

        i = 0

        TIME_STAMP = []
        RESULT = []
        TEST_NAME = []
        SERIAL = []
        DEVICE_TYPE = []
        STACKTRACE = []
        PATH = []
        OS_BUILD_VERSION = []

        print("Current dir: ", log_home)

        flag = 0
        while flag == 0:
            time.sleep(2)

            src_path = '/tmp/logs/mobly/'+test_bed_name+'/latest'
            dst_path = gTAF_config.log_path + test_bed_name + "/" + test_case_name + "/"+job_id+"/"
            yml_file = src_path + "/test_summary.yaml"

            print("####################################### TEST DATA #########################################")
            print("test_bed_name : ", test_bed_name)
            print("test_case_name : ", test_case_name)
            print("src_path path : ", src_path)
            print("dst_path path : ", dst_path)
            print("yml_file path : ", yml_file)
            print("###########################################################################################")

            stacktrace_logs = self._get_error_logs(yml_file)
            with open(yml_file, 'r') as FH:
                for line in FH:
                    if "Timestamp:" in line:
                        time_stamp = line.split(":")
                        time_stamp = float(time_stamp[1].strip())-19800.0
                        # cmd = "date -d @" + str(time_stamp)
                        # time_stamp = subprocess.check_output(cmd, shell=True)
                        # time_stamp = str(time_stamp).strip()
                        # time_stamp = time_stamp.replace(" ", "")
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
                        os_build_version = None

            print(job_id)
            print(TEST_NAME[i])
            print(RESULT[i])
            print(DEVICE_TYPE[i])
            print(SERIAL[i])
            print(TIME_STAMP[i])
            print(OS_BUILD_VERSION[i])

            src_path = src_path.strip()
            dst_path = dst_path.strip()
            path_to_write = dst_path
            PATH.append(path_to_write)
            time.sleep(1)
            mode = 'w+'
            if os.path.exists(results_csv_file_path):
                mode = 'a'
            print(os.path.exists(results_csv_file_path))
            print("Mode:" + mode)
            with open(results_csv_file_path, mode) as ex:
                ex.write(str(job_id))
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
                ex.write(",")
                ex.write(OS_BUILD_VERSION[i])
                ex.write("\n")

            ex.close()
            print(path_to_write)

            #################################
            # Insert test results to DB
            db = MySQLdb.connect(host=gTAF_config.sql_db_host, port=3306, user='root', passwd='password', db=gTAF_config.sql_db_name)
            cur = db.cursor()
            CSV_DATA= []

            CSV_DATA.append(job_id)
            CSV_DATA.append(TEST_NAME[i])
            CSV_DATA.append(RESULT[i])
            CSV_DATA.append(DEVICE_TYPE[i])
            CSV_DATA.append(SERIAL[i])
            CSV_DATA.append(TIME_STAMP[i])
            CSV_DATA.append(PATH[i])
            CSV_DATA.append(STACKTRACE[i])

            print("Data to be inserted in DB :")
            print(CSV_DATA)
            sqlinsert = "INSERT INTO " +\
                        gTAF_config.sql_db_table_name+" (JENKINS_ID,TEST_NAME, RESULT, DEVICE_TYPE, SERIAL, " \
                        "TIME_STAMP, PATH, STACKTRACE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sqlinsert, CSV_DATA)
            db.commit()
            # disconnect from server
            db.close()
            print('Test results inserted to DB successfully, closing the connection.')
            #################################
            # Insert test results to DB end

            copy_cmd = "cp -r " + src_path + "/*" + " " + dst_path
            print("copy_cmd : ", copy_cmd)
            os.system(copy_cmd)

            i = i + 1
            time.sleep(1)
            flag = 1
        print("###########################################################################################")
        print(job_id)
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
        # error = re.search(r'Details:.*?End Time:', content, re.DOTALL).group()
        stacktrace = re.search(r'Stacktrace:.*?Test Class:', content, re.DOTALL).group()

        if stacktrace != '':
            stacktrace = stacktrace.replace("\\n", '')
            stacktrace = stacktrace.replace("\\", '')
            stacktrace = stacktrace.replace("'\'", '')
            stacktrace = stacktrace.replace("\n", '')
            # error = error.replace("\\n", '')
            # error = error.replace("\\", '')
            # error = error.replace("'\'", '')
            # error = error.replace("\n", '')

            return stacktrace
        else:
            return ''


if __name__ == '__main__':
    job = None
    arg = sys.argv

    if len(arg) > 1:
        job = arg[1]
        test_bed = arg[2]
        test_case = arg[3]
        if job is not None and test_case is not None and test_bed is not None:
            report = Report()
            report.get_execution_results(test_bed, test_case, job)
    else:
        print("Please pass the jenkins id in parameter!!!")
        exit()
