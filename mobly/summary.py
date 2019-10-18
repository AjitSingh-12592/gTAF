import csv
import gTAF_config
import yaml

# file_name = gTAF_config.execution_summary_csv_file
# fields = []
# rows = []
# pass_count = 0
# fail_count = 0
# skip_count = 0
#
# with open(file_name, 'r') as fl:
#     data = csv.reader(fl)
#     fields = data.next()
#     for row in data:
#         rows.append(row)
#
# for i in range(0, len(rows)):
#
#     if rows[i][2] == 'PASS':
#         pass_count += 1
#
#     if rows[i][2] == 'FAIL':
#         fail_count += 1
#
#     if rows[i][2] == 'ERROR':
#         skip_count += 1
#
# if pass_count + fail_count + skip_count == len(rows):
#     pass
# else:
#     print("\nError...Pass, Fail and skip test count mismatched with Total")
#
# print("\n####################################### Execution Summary #################################\n")
# print("TOTAL TEST EXECUTED:" + str(len(rows)))
# print("PASSED :" + str(pass_count))
# print("FAILED :" + str(fail_count))
# print("SKIPPED:" + str(skip_count))
#
# print("\n######################################## Detailed Summary ##################################\n")
#
# for i in range(0, len(rows)):
#     print(rows[i][1] + ":" + rows[i][2])


def _get_serial():
    test_bed = 'GTAF_TEST_BED_CONTACT'
    file = "/home/edat/Desktop/gTAF/mobly/gtaf_config.yml"
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

_get_serial()