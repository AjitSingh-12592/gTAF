from mobly import base_test
from mobly import test_runner
from mobly.controllers import android_device
import time
import logging
import os
import cv2 as cv
import gTAF_config
import subprocess
from subprocess import check_call
import unicodedata


class BluetoothPairing(base_test.BaseTestClass):


  def setup_class(self):
    self.ads = self.register_controller(android_device)
    # The device used to discover Bluetooth devices.
    self.discoverer = android_device.get_device(self.ads, label='discoverer')
    # Sets the tag that represents this device in logs.
    self.discoverer.debug_tag = 'discoverer'
    # The device that is expected to be discovered
    self.target = android_device.get_device(self.ads, label='target')
    self.target.debug_tag = 'target'
    self.target.load_snippet('mbs', 'com.google.android.mobly.snippet.example4')
    self.discoverer.load_snippet('mbs', 'com.google.android.mobly.snippet.example4')


  def test_bt_pair(self):
    try:
      target_bt_dump = self.target.mbs.getCommandOutput("dumpsys bluetooth_manager")
      target_bt_name = target_bt_dump.split("\n")

      #bt_pair_status = self._device_bluetooth_paired_status(target_bt_name, target_bt_dump)
      #logging.info("Bluetooth pair status initially: %s", bt_pair_status)
      # Removice images from target and dicoverer devices

      bt_del_cmd = "sudo adb -s " + gTAF_config.YT_BT_TARGET_SERIAL + " shell rm /mnt/sdcard/bluetooth/*"
      camera_del_cmd = "sudo adb -s " + gTAF_config.YT_BT_DISCOVERER_SERIAL + " shell rm /mnt/sdcard/DCIM/Camera/*"
      logging.info(bt_del_cmd)
      logging.info(camera_del_cmd)
      os.system(bt_del_cmd)
      os.system(camera_del_cmd)
      os.system("rm -rf bluetooth")
      os.system("rm -rf Camera")

      # BT Status true/false when enabled/disabled
      for val in target_bt_name:
        if "  enabled:" in val:
          target_bt_status = val.split(":")
          target_bt_state = target_bt_status[1].strip()
          target_bt_state = target_bt_state.encode("ascii")
          logging.info("Target Bluetooth status is : %s ", target_bt_state)

        if "name:" in val:
          target_bt_name = val.split(":")
          target_bt_name[1] = target_bt_name[1].strip()
          targate_name = target_bt_name[1].encode("ascii")
          logging.info("Target Bluetooth name : %s ", targate_name)

      #Unpair device if paired already
      self._unpair_bluetooth_devices(targate_name)

      '''
      discv_bt_dump_cmd = "adb -s " + gTAF_config.YT_BT_DISCOVERER_SERIAL + " shell dumpsys bluetooth_manager "
      logging.info(discv_bt_dump_cmd)
      disc_dump = subprocess.check_output(discv_bt_dump_cmd, shell=True)
      if targate_name in disc_dump:
        logging.info("un-pairing the device's bluetooth")
        logging.info(disc_dump)
        self._unpair_bluetooth()
      else:
        logging.info("Devices not paired ")
      '''

      discv_bt_dump = self.discoverer.mbs.getCommandOutput("dumpsys bluetooth_manager")
      discv_bt_name = discv_bt_dump.split("\n")
      for val in discv_bt_name:
        if "  enabled:" in val:
          dscvr_bt_status = val.split(":")
          dscvr_bt_state = dscvr_bt_status[1].strip()
          dscvr_bt_state = dscvr_bt_state.encode("ascii")
          logging.info("Discoverer Bluetooth status is : %s ", dscvr_bt_state)

        if "name:" in val:
          dscvr_bt_name = val.split(":")
          dscvr_bt_name[1] = dscvr_bt_name[1].strip()
          logging.info("Discoverer Bluetooth name : %s ", dscvr_bt_name[1].encode("ascii"))

      '''
      if_prd = self._device_bluetooth_paired_status(targate_name, discv_bt_dump)
      logging.info("Bluetooth pair status :: %s", if_prd)

      if if_prd:
        logging.info("un-pairing the device's bluetooth")
        self._unpair_bluetooth()
      else:
        logging.info("Devices not paired ")
      '''

      self._unlock_screen()
      logging.info(target_bt_state)
      logging.info(dscvr_bt_state)
      if target_bt_state == "true":
        self.target.mbs.executeCommandOnDevice("am start -a android.bluetooth.adapter.action.REQUEST_DISABLE")
        self.target.mbs.clickOnText("Allow")
        time.sleep(3)

      if dscvr_bt_state == "true":
        self.discoverer.mbs.executeCommandOnDevice("am start -a android.bluetooth.adapter.action.REQUEST_DISABLE")
        self.discoverer.mbs.clickOnText("Allow")
        time.sleep(3)

      logging.info("Launching settings")
      self.target.mbs.launchSettings()
      self.discoverer.mbs.launchSettings()
      logging.info("Opening Bluetooth menu")
      self.target.mbs.clickOnText("Connected devices")
      self.discoverer.mbs.clickOnText("Connected devices")
      self.target.mbs.clickOnText("Pair new device")
      logging.info("Enabling Bluetooth")
      time.sleep(2)
      logging.info("Searching for available Bluetooth device to pair")
      self.discoverer.mbs.clickOnText("Pair new device")
      time.sleep(10)
      self.discoverer.mbs.clickOnText(targate_name)
      time.sleep(10)
      self.discoverer.mbs.clickOnText("Pair")
      self.target.mbs.clickOnText("Pair")
      time.sleep(10)

      # Verification for paired BT devices
      #logging.info("Verifying Bluetooth pair status in dump")
      #discv_bt_pair_dump = self.discoverer.mbs.getCommandOutput("dumpsys bluetooth_manager")
      #discv_bt_pair_dumps = discv_bt_pair_dump.split("\n")


      '''
      ifpaired = self._device_bluetooth_paired_status(targate_name, discv_bt_dump)
      logging.info("Bluetooth pair status : %s", ifpaired)

      if ifpaired:
        logging.info("Devices paired already, un-pairing it")
        self._unpair_bluetooth()
      '''

      '''
      for i in range(0, len(discv_bt_pair_dumps)):
        if "Bonded devices:" in str(discv_bt_pair_dumps[i]):
          print(str(discv_bt_pair_dumps[i]))
          print(str(discv_bt_pair_dumps[i+1]))
          if (targate_name in str(discv_bt_pair_dumps[i+1])) or (targate_name in str(discv_bt_pair_dumps[i+2])) :
            logging.info("Target bluetooth name found in bonded BT devices list of discoverer device %s", str(discv_bt_pair_dumps[i+1]))
            logging.info("Target bluetooth name found in bonded BT devices list of discoverer device %s", str(discv_bt_pair_dumps[i+2]))
            bt_paired = True
          else:
            logging.info("Target bluetooth name not found in bonded BT devices list of discoverer device %s",str(discv_bt_pair_dumps[i + 1]))
            assert False
      '''
      is_bt_paired = self._device_bluetooth_paired_status(targate_name)
      logging.info(is_bt_paired)
      if is_bt_paired:
        self._bt_file_share(targate_name)
        time.sleep(5)
        logging.info("File Shared over bluetooth")
        self.verify_shared_bt_image()
      else:
        logging.info("Discoverer bluetooth device not paired with target device")
    finally:
      logging.info("Executing cleanup..")
      self._unpair_bluetooth_devices(targate_name)
      self._teardown()

  def _unpair_bluetooth_devices(self, targate_name):
    discv_bt_dump_cmd = "adb -s " + gTAF_config.YT_BT_DISCOVERER_SERIAL + " shell dumpsys bluetooth_manager "
    logging.info(discv_bt_dump_cmd)
    disc_dump = subprocess.check_output(discv_bt_dump_cmd, shell=True)
    if targate_name in disc_dump:
      logging.info("un-pairing the device's bluetooth")
      #logging.info(disc_dump)
      self._unpair_bluetooth()
    else:
      logging.info("Devices not paired ")


  def _device_bluetooth_paired_status(self, bluetooth_name):
    bt_paired = False
    discv_bt_dump_cmd = "adb -s " + gTAF_config.YT_BT_DISCOVERER_SERIAL + " shell dumpsys bluetooth_manager "
    logging.info(discv_bt_dump_cmd)
    disc_dump = subprocess.check_output(discv_bt_dump_cmd, shell=True)
    if bluetooth_name in disc_dump:
      logging.info("Discoverer bluetooth device paired with target device")
      bt_paired = True
    else:
      logging.info("Discoverer bluetooth device not paired with target device")

    return bt_paired

  def verify_shared_bt_image(self):

    bt_pull_cmd = "adb -s " + gTAF_config.YT_BT_TARGET_SERIAL + " pull /mnt/sdcard/bluetooth/ ."
    camera_pull_cmd = "adb -s " + gTAF_config.YT_BT_DISCOVERER_SERIAL + " pull /mnt/sdcard/DCIM/Camera ."
    logging.info(bt_pull_cmd)
    logging.info(camera_pull_cmd)
    os.system(bt_pull_cmd)
    os.system(camera_pull_cmd)
    if os.path.exists(os.getcwd() + "/Camera") and os.path.exists(os.getcwd() + "/bluetooth"):
      print("----------------------------------------------")
      logging.info("bluetooth and Camera folders found")
      _bluetooth_img = subprocess.check_output("ls bluetooth", shell=True)
      _bluetooth_img = _bluetooth_img.strip()
      _camera_img = subprocess.check_output("ls bluetooth", shell=True)
      _camera_img = _camera_img.strip()
      os.system("ls -l bluetooth/")
      os.system("ls -l Camera/")
      logging.info(_bluetooth_img)
      logging.info(_camera_img)
      assert _bluetooth_img == _camera_img, "sent and received images names mismatched!"
      bt_image = "bluetooth/" + _bluetooth_img
      camera_image = "Camera/" + _camera_img
      result = self._image_cmp(bt_image, camera_image)
      assert result is True, "Incorrect image is being shared"
    else:
      logging.info("bluetooth and Camera folders not found")
      assert False

  def _image_cmp(self, bt_img, camera_img):
    logging.info(bt_img)
    logging.info(camera_img)
    bt_img = cv.imread(bt_img)
    camera_img = cv.imread(camera_img)

    if bt_img.shape == camera_img.shape:
      logging.info("The images have same size and channels")
      difference = cv.subtract(bt_img, camera_img)
      b, g, r = cv.split(difference)
      logging.info("r, g, b differences values of captured screenshots")
      logging.info("Diff for r component : %s", cv.countNonZero(r))
      logging.info("Diff for g component : %s", cv.countNonZero(g))
      logging.info("Diff for b component : %s", cv.countNonZero(b))

      if cv.countNonZero(b) == 0 and cv.countNonZero(g) == 0 and cv.countNonZero(r) == 0:
        logging.info("Correct image is being shared by bluetooth")
        return True
      else:
        logging.info("Incorrect image is being shared")
        return False


  def _bt_file_share(self, target_bt_name):
    logging.info("Sharing file to target device")
    self.discoverer.mbs.executeCommandOnDevice(
      " am start -n com.google.android.GoogleCamera/com.android.camera.CameraLauncher")
    time.sleep(3)
    self.discoverer.mbs.waitAndClickUsingContentDesc("Take photo")
    time.sleep(3)
    self.discoverer.mbs.waitAndClickUsingContentDesc("Photo gallery")
    time.sleep(2)
    self.discoverer.mbs.waitAndClickUsingContentDesc("Share")
    self.discoverer.mbs.clickOnText("Bluetooth")
    time.sleep(5)
    self.discoverer.mbs.clickOnText(target_bt_name)
    time.sleep(3)
    self.target.mbs.clickOnText("Accept")
    logging.info("Accept click")
    time.sleep(10)

  def _bt_file_count_in_device(self, dev_id):
    os.system("rm -rf bluetooth")
    bt_pull_cmd = "adb -s " + dev_id + " pull /mnt/sdcard/bluetooth/ ."
    bt_file_count = "ls -l bluetooth/ | wc -l"
    os.system(bt_pull_cmd)
    _response = subprocess.check_output(bt_file_count, shell=True)
    return int(_response.strip())

  def _unpair_bluetooth(self):
    self._unlock_screen()
    self._teardown()
    self.target.mbs.pressBack()
    time.sleep(1)
    self.target.mbs.launchSettings()
    self.discoverer.mbs.launchSettings()
    logging.info("Opening Bluetooth menu")
    self.target.mbs.clickOnText("Connected devices")
    time.sleep(1)
    self.target.mbs.pressBack()
    time.sleep(1)
    self.target.mbs.clickOnText("Connected devices")
    time.sleep(1)
    self.discoverer.mbs.clickOnText("Connected devices")
    time.sleep(1)
    self.discoverer.mbs.pressBack()
    time.sleep(1)
    self.discoverer.mbs.clickOnText("Connected devices")
    self.target.mbs.clickOnText("Previously connected devices")
    self.discoverer.mbs.clickOnText("Previously connected devices")
    time.sleep(1)

    self.target.mbs.clickUsingResourceId("com.android.settings:id/settings_button")
    self.discoverer.mbs.clickUsingResourceId("com.android.settings:id/settings_button")
    time.sleep(1)
    self.target.mbs.clickOnText("Forget")
    self.discoverer.mbs.clickOnText("Forget")
    time.sleep(1)
    self.target.mbs.clickOnText("Forget device")
    self.discoverer.mbs.clickOnText("Forget device")
    time.sleep(1)
    logging.info("Disable Bluetooth in both devices")
    self.target.mbs.executeCommandOnDevice("am start -a android.bluetooth.adapter.action.REQUEST_DISABLE")
    self.target.mbs.clickOnText("Allow")
    self.discoverer.mbs.executeCommandOnDevice("am start -a android.bluetooth.adapter.action.REQUEST_DISABLE")
    self.discoverer.mbs.clickOnText("Allow")
    time.sleep(1)
    self._teardown()

  def _unlock_screen(self):
    self.target.mbs.inputKeyEvent(224)
    self.target.mbs.inputKeyEvent(82)
    self.discoverer.mbs.inputKeyEvent(224)
    self.discoverer.mbs.inputKeyEvent(82)

  def _teardown(self):
    self.target.mbs.pressBack()
    self.target.mbs.pressBack()
    self.target.mbs.pressHome()
    self.discoverer.mbs.pressBack()
    self.discoverer.mbs.pressBack()
    self.discoverer.mbs.pressHome()

if __name__ == '__main__':
    test_runner.main()