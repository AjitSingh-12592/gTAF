import subprocess
import sys
import os
import yaml
import gTAF_config
import gTAF_ui_config


class Execu:

    def start(self):
        print(sys.argv, len(sys.argv))
        if len(sys.argv) == 6:
            serial = sys.argv[1]
            test_case = sys.argv[2]
            job_id = sys.argv[3]
            test_suite = sys.argv[4]
            print(test_suite, ':', test_case)
            device_type = sys.argv[5]
            test_bed = self._get_test_bed(device_id=serial, module=test_suite, device_type=device_type + 'Device')
            rc = self.run_command(serial, test_case, job_id, test_suite, device_type, test_bed)
            print(rc)

    def run_command(self, device_id, _test_case, _job_id, _test_suite, _device_type, test_bed):
        mkdir = 'mkdir -p '
        print("PAth checking----------------------")
        print(os.path.exists(gTAF_config.log_path + test_bed + '/' + _test_case + '/' + _job_id + '/'))
        if os.path.exists(gTAF_config.log_path + test_bed + '/' + _test_case + '/' + _job_id + '/'):
            print("Path already exists")
        else:
            print("PAth creating----------------------")
            print("creating " + gTAF_config.log_path + test_bed + '/' + _test_case + '/' + _job_id + '/')
            os.system(mkdir + gTAF_config.log_path + test_bed + '/' + _test_case + '/' + _job_id)

        command = 'python3 '+gTAF_ui_config.mobly_path+'execute.py ' + device_id + \
                  ' ' + _test_case + ' ' + _job_id + ' ' + _test_suite + ' ' + _device_type + ' ' + test_bed
        output_file = gTAF_ui_config.output_log_path + str(_job_id) + '.html'
        dst_path = gTAF_config.log_path + test_bed + "/" + _test_case + "/" + _job_id + "/console.log"
        mode = 'w+'
        if os.path.exists(output_file):
            mode = 'a'
        print()
        with open(dst_path, 'w+') as console:
            with open(output_file, mode) as f:
                f.write("<html onload=\"window.scrollTo(0,document.body.scrollHeight);\">"
                        "<head><meta http-equiv=\"refresh\" content=\"1\">"
                        "</head><body onload=\"window.scrollTo(0,document.body.scrollHeight);\">"
                        "<p>")
                process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                while True:
                    if process.poll() is not None:
                        break
                    output = process.stdout.readline()
                    if output:
                        print(output.strip().decode('utf-8'))
                        # soc.send(output.strip())
                        console.write(output.strip().decode('utf-8') + '\n')
                        f.write(output.strip().decode('utf-8') + '<br>')
                        f.flush()
                f.write("</p></body></html")
                f.close()
            console.close()
        rc = process.poll()
        return rc

    def _get_test_bed(self, device_id, module, device_type):
        """
        :return:
        :param device_id:
        :param module:
        :return:
        """
        file = gTAF_ui_config.mobly_path+"gtaf_config.yml"
        with open(file) as file:
            document = yaml.load(file)
            bed_list = document['TestBeds']
            for bed in bed_list:
                bed_name = bed['Name']
                if str(bed_name).__contains__(module+"_"+device_id):
                    return bed_name
            return self._generate_bed(module, device_id, device_type)

    """
                    controller_info = bed['Controllers']
                    AndroidDevice = controller_info['AndroidDevice']
                    if len(AndroidDevice) == 1:
                        serial = AndroidDevice[0]['serial']
                        if serial == device_id:
                            if str(bed_name).__contains__(module):
                                return bed_name"""

    # print(len(AndroidDevice), "\n")
    # print(document['TestBeds'][0]['Controllers']['AndroidDevice'][0]['serial'])

    def _generate_bed(self, suit_name, device_id, device_type):

        bed = {'Controllers': {device_type: [{'serial': device_id}]}}
        be = "Controllers:\n       " + device_type + ":\n          - serial: " + device_id
        bed_name = {'Name': 'GTAF_TEST_BED_' + suit_name + '_' + device_id}
        file = gTAF_ui_config.mobly_path+"gtaf_config.yml"

        with open(file, 'a') as yfile:
            # 2 & 1 sp
            yfile.write("\n  - ")
            yfile.write('Name: GTAF_TEST_BED_' + suit_name + '_' + device_id+'\n')
            # 4 spaces
            yfile.write("    ")
            yfile.write(be)
        return bed_name['Name']


if __name__ == '__main__':
    execute = Execu()
    execute.start()

