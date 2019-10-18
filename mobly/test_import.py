
print("---import section test_contacts----1")
import logging
import time
import contacts_selectors
import subprocess
from mobly import base_test
from mobly import test_runner
from mobly.config_parser import dev_li as device_list
from mobly.controllers import android_device
import gTAF_config

class imp(base_test.BaseTestClass):

    def setup_class(self):

        android_version_cmd = "adb -s " + device_list[0] + " shell getprop ro.build.version.release"
        android_version = subprocess.check_output(android_version_cmd, shell=True)
        android_version = android_version.strip()
        logging.info("android_version : %s", android_version)

        device_model_cmd = "adb  -s " + device_list[0] + " shell getprop ro.product.model"
        device_model = subprocess.check_output(device_model_cmd, shell=True)
        device_model = device_model.strip()
        logging.info("device_model : %s", device_model)
        logging.info("Loading device configuration for %s device[Android version-%s]", device_model, android_version)
        gTAF_config.load_device_config(dev_model=device_model, android_version=android_version)
        uiElement = gTAF_config.uiElement
        surname = uiElement['DEVICE_DETAIL']

        surname = uiElement['CONTACT_SURNAME_TEXT']
        phonetic_last_name = uiElement['PHONETIC_LAST_NAME']
        pop_up_deny = uiElement['POP_UP_DENY']
        pop_up_cancel = uiElement['POP_UP_CANCEL']
        save_btn = uiElement['SAVE_BTN']

        global surname
        global phonetic_last_name
        global pop_up_deny
        global pop_up_cancel
        global save_btn


        self.ads = self.register_controller(android_device)
        self.dut = self.ads[0]
        self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.example4')

    def test_imprt(self):

        for i in range(0, 5):
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            time.sleep(2)
            self.dut.mbs.pressBack()


if __name__ == '__main__':
    test_runner.main()


