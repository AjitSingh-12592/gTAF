import sys
import os
import subprocess

class DeviceDetails:

    def get_dev_detail(self, test_bed=None):

        android_version_cmd = "adb shell getprop ro.build.version.release"
        android_version = subprocess.check_output(android_version_cmd, shell=True)
        print("android_version : ", android_version.strip())

        device_model_cmd = "adb shell getprop ro.product.model"
        device_model = subprocess.check_output(device_model_cmd, shell=True)
        print("device_model : ", device_model.strip())


if __name__ == '__main__':
    test_bed = None
    args = sys.argv

    if len(args) > 1:
        test_bed = args[1]
    else:
        print("Insufficient arguments !!!!")
        exit()
    if test_bed is not None:
        dev_details = DeviceDetails()
        dev_details.get_dev_detail(test_bed)
    else:
        print("Please provide correct parameters in get_device_details.py !!!")
        exit()
