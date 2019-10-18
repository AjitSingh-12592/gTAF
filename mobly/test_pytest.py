
import smtplib

print("1")
s = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
#s = smtplib.SMTP('pop.gmail.com', 995)
print("2")
s.starttls()
print("4")
    # ...send emails


'''
from mobly import base_test
from mobly import test_runner
from mobly.controllers import android_device
import time
from collections import OrderedDict
import logging
import contacts_selectors
from PIL import Image
import os
import gTAF_config
import allure
import pytest

class Contacts(base_test.BaseTestClass):


    def setup_class(self):

      # Registering android_device controller module declares the test's
      # dependency on Android device hardware. By default, we expect at least one object is created from this
      self.ads = self.register_controller(android_device)
      self.dut = self.ads[0]
      # Start Mobly Bundled Snippets (MBS).
      #self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.bundled')
      self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.example4')

    def test1(self):
        print("test1")
        assert True

    def test1(self):
        print("test1")
        assert True

    def test1(self):
        print("test1")
        assert False

if __name__ == '__main__':
    test_runner.main()
'''