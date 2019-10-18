import logging
import subprocess
import sys
import gTAF_ui_config


class Execute:
    def execute(self):
        module = {
            'Android': {'CONTACT': 'test_contacts_app.py',
                        'YOUTUBE': 'test_youtube_app.py',
                        'MAP': 'test_google_map.py',
                        'TWILIGHT': 'test_twilight_app.py'},
            'IOS': {}}
        if len(sys.argv) == 7:
            serial = sys.argv[1]
            test_case = sys.argv[2]
            job_id = sys.argv[3]
            test_suite = sys.argv[4]
            print(test_suite, ':', test_case)
            device_type = sys.argv[5]
            test_bed = sys.argv[6]

            module_name = module[device_type][test_suite]
            try:
                cmd = "cd "+gTAF_ui_config.mobly_path+"; sudo python " + module_name \
                      + " -c gtaf_config.yml --test_case " + test_case + " --test_bed " + test_bed + \
                      " |tail -1 |awk '{ for (i = 10; i <= 20; i+=2) print $i,\":\", $(i+1) }'"
                cmd_report = "cd "+gTAF_ui_config.mobly_path+"; sudo python test_report_gen.py " +\
                             job_id + " " + test_bed + " " + test_case + "| grep shivang"
                cmd_test = "cd "+gTAF_ui_config.mobly_path+"; sudo python " + module_name \
                           + " -c gtaf_config.yml --test_case " + test_case + " --test_bed " + test_bed +\
                           " |tee execute.txt"
                output_test = "cat execute.txt |tail -1 |awk '{ for (i = 10; i <= 20; i+=2) print $i,\":\", $(i+1) }'"
                cmd_report_test = "cd "+gTAF_ui_config.mobly_path+"; sudo python test_report_gen.py "\
                                  + job_id + " " + test_bed + " " + test_case
                # print(cmd, "\n")
                test_output = subprocess.call(str(cmd_test), shell=True)
                # output = subprocess.call(str(output_test), shell=True)

                # print(cmd_report, "\n")
                report_output = subprocess.call(str(cmd_report), shell=True)
            finally:
                logging.info("")


if __name__ == '__main__':
    execute = Execute()
    execute.execute()
