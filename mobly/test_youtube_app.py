from mobly import base_test
from mobly import test_runner
from mobly.controllers import android_device
import time
import os
import cv2 as cv
import logging
import yt_selectors
import gTAF_config


class Youtube_App_Test(base_test.BaseTestClass):
  def setup_class(self):
    # Registering android_device controller module declares the test's
    # dependency on Android device hardware. By default, we expect at
    # least one object is created from this.
    self.ads = self.register_controller(android_device)
    self.dut = self.ads[0]
    # Start Mobly Bundled Snippets (MBS).
    #self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.bundled')
    self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.example4')


  def test_Settings_About_Items(self):

    ABOUT_ITEMS = ['Help', 'Send feedback', 'YouTube Terms of Service', 'Google Privacy Policy', 'Open source licenses',
                  'App version', 'YouTube, a Google company']
    self.dut.mbs.pressHome()
    self.dut.mbs.launchYTApp()
    self.dut.mbs.waitAndClickUsingResourceId(yt_selectors.AVATAR_SELCTOR)
    self.dut.mbs.clickOnText(yt_selectors.SETTINGS)
    self.dut.mbs.clickOnText(yt_selectors.ABOUT)
    for items in range(0, len(ABOUT_ITEMS)):
      if ABOUT_ITEMS[items] in self.dut.mbs.getMenuItemDescription(ABOUT_ITEMS[items]):
        logging.info("Item found and matched for About option :%s", ABOUT_ITEMS[items])
      else:
        logging.info("Item not matched for About option :%s", ABOUT_ITEMS[items])
        assert False
    self._teardown()

  def test_Video_Not_Available(self):

    self.dut.mbs.play_YT_Video(yt_selectors.NOT_AVAILABLE_VID)
    time.sleep(2)
    ACTUAL_ERROR_MESSAGE = self.dut.mbs.getTextByResourceId(yt_selectors.VIDEO_NOT_AVAILABLE_TEXT_SELECTOR)
    logging.info("Actual player error message : \'%s\'", ACTUAL_ERROR_MESSAGE)
    if yt_selectors.VIDEO_NOT_AVAILABLE_ERROR in ACTUAL_ERROR_MESSAGE:
       logging.info("Correct player error message found")
    else:
       logging.info("Incorrect player error message found")
    self._teardown()

  def test_caption(self):
    try:
      self._unlock_screen()
      self.dut.mbs.play_YT_Video(yt_selectors.CAPTION_VIDEO_ID)
      self._skipAd_If_Displayed()
      self.dut.mbs.waitForexistText("Share", 10)
      #self._disableCaptions()
      #time.sleep(8000)
      count = 0
      CAPTION_TEXT = None
      self._enableCaptions()
      while CAPTION_TEXT is None and count <= 20:
        CAPTION_TEXT = self.dut.mbs.getTextByResourceId(yt_selectors.CAPTION_TEXT_SELECTOR)
        logging.info("Caption text found : %s", CAPTION_TEXT)
        time.sleep(1)
        count += 1
      self._disableCaptions()
      count = 0
      CAPTION_TEXT = None
      while CAPTION_TEXT is None and count <= 10:
        CAPTION_TEXT = self.dut.mbs.getTextByResourceId(yt_selectors.CAPTION_TEXT_SELECTOR)
        logging.info("Caption text after Captions disabled : %s", CAPTION_TEXT)
        time.sleep(1)
        count += 1
    finally:
      self._teardown()

  def test_Settings_Trending_Test(self):
    self.dut.mbs.launchYTApp()
    self.dut.mbs.clickOnText("Trending")
    self._teardown()

  def test_YouTube_Video_Playback(self):
    try:
      self._unlock_screen()
      logging.info("Youtube video playback test")
      self._delete_previous_screenshots()
      self.dut.mbs.pressHome()
      if (self.dut.mbs.isOnline()):
        logging.info("Internet is working in device..")
        self.dut.mbs.play_YT_Video(yt_selectors.CAPTION_VIDEO_ID)
        self._skipAd_If_Displayed()
        logging.info("Waiting for few seconds")
        time.sleep(5)
        self.dut.mbs.display_YT_Media_Player_Controls()
        time.sleep(5)
        if(self.dut.mbs.isVideoPlaying()):
          logging.info("Youtube media play-bar button found")
          self._capture_screenshot(screenshots_gap=10)
          logging.info("Going to verify video playback by image comparison")
          result = self._yt_vedio_image_cmp()
          assert result is False, "Both screenshots found same, seems video is not playing or stucked"
        else:
          logging.info("Youtube media play-bar button not found, seems youtube video player not launched.")
      else:
        logging.info("Internet is not working in connected device")
        assert False
    finally:
      self._teardown()


  def test_YouTube_Play_Pause(self):
    try:
      self._unlock_screen()
      self.dut.mbs.pressHome()
      if (self.dut.mbs.isOnline()):
        logging.info("Internet is working in device..")
        self.dut.mbs.launchYTApp()
        self.dut.mbs.clickUsingResourceId(yt_selectors.VIDEO_SELECTOR)
        self._skipAd_If_Displayed()
        logging.info("Waiting for 3 sec.")
        time.sleep(3)
        self.dut.mbs.display_YT_Media_Player_Controls()
        if (self.dut.mbs.isVideoPlaying()):
          logging.info("Video is Playing currently")
          self._get_current_seekbar_time()
          logging.info("Clicking to pause")
          self.dut.mbs.pauseVideo()
          time.sleep(3)
          logging.info("Clicking to play")
          self.dut.mbs.playVideo()
        else:
          logging.info("Video is paused, playing now")
          self._get_current_seekbar_time()
          logging.info("Clicking to  play")
          self.dut.mbs.playVideo()
          time.sleep(3)
          logging.info("Clicking to pause")
          self.dut.mbs.pauseVideo()
          self._get_current_seekbar_time()
      else:
        logging.info("Internet is not working in device.")
        assert False
    finally:
      self._teardown()


  def test_Get_Video_Seek_Bar_Time(self):
    self._unlock_screen()
    self.dut.mbs.pressHome()
    self.dut.mbs.launchYTApp()
    self.dut.mbs.clickUsingResourceId(yt_selectors.VIDEO_SELECTOR)
    self._skipAd_If_Displayed()
    logging.info("Waiting for 3 sec.")
    time.sleep(3)
    self.dut.mbs.display_YT_Media_Player_Controls()
    self.dut.mbs.clickUsingResourceId(yt_selectors.PLAY_PAUSE_BUTTON_SELECTOR)
    time.sleep(3)
    self.dut.mbs.clickUsingResourceId(yt_selectors.PLAY_PAUSE_BUTTON_SELECTOR)
    self._get_current_seekbar_time()
    self._teardown()

  def _yt_vedio_image_cmp(self):
    img_1 = cv.imread("img1.png")
    img_2 = cv.imread("img2.png")

    if img_1.shape == img_2.shape:
      logging.info("The images have same size and channels")
      difference = cv.subtract(img_1, img_2)
      b, g, r = cv.split(difference)
      logging.info("r, g, b differences values of captured screenshots")
      logging.info("Diff for r component : %s", cv.countNonZero(r))
      logging.info("Diff for g component : %s", cv.countNonZero(g))
      logging.info("Diff for b component : %s", cv.countNonZero(b))

      if cv.countNonZero(b) == 0 and cv.countNonZero(g) == 0 and cv.countNonZero(r) == 0:
        logging.info("Captured screenshots are completely Equal")
        return True
      else:
        logging.info("Captured screenshots are not equal, which is expected")
        return False

  def _delete_previous_screenshots(self):
    image_1 = os.path.isfile('img1.png')
    image_2 = os.path.isfile('img2.png')
    if image_1:
      os.system("rm img1.png")
    if image_2:
      os.system("rm img2.png")

  def _capture_screenshot(self, screenshots_gap):
    logging.info("Capturing 1st screenshot for Youtube video playback verification")
    self.dut.mbs.executeCommandOnDevice(" screencap -p /sdcard/img1.png")
    cmd1 = "adb -s "  + gTAF_config.YT_TEST_DEVICE_SERIAL + " pull /sdcard/img1.png ."
    logging.info(cmd1)
    os.system(cmd1)
    self.dut.mbs.executeCommandOnDevice(" rm /sdcard/img1.png")
    time.sleep(screenshots_gap)
    logging.info("Capturing 2nd screenshot for Youtube video playback verification")
    self.dut.mbs.executeCommandOnDevice(" screencap -p /sdcard/img2.png")
    cmd2 = "adb -s " + gTAF_config.YT_TEST_DEVICE_SERIAL + " pull /sdcard/img2.png ."
    os.system(cmd2)
    self.dut.mbs.executeCommandOnDevice(" rm /sdcard/img2.png")


  def _skipAd_If_Displayed(self):
    logging.info("Verifying if add displayed")
    ADD_DURATION = self.dut.mbs.getAdRemainingDuration()
    logging.info("Add duration time : %s ", ADD_DURATION)
    self.dut.mbs.playVideo()
    time.sleep(int(ADD_DURATION) + 2)
    self.dut.mbs.skipAddIfDisplayed()

  def _get_current_seekbar_time(self):
    seek_bar_time = self.dut.mbs.getContentDescByClass(yt_selectors.SEEK_BAR_SELECTOR)
    seek_bar_time = seek_bar_time.split(yt_selectors.OF)
    seek_bar_time[0] = seek_bar_time[0].strip().encode(yt_selectors.UTF)
    seek_bar_time[1] = seek_bar_time[1].strip().encode(yt_selectors.UTF)
    logging.info("Current seek bar time : %s", seek_bar_time[0])
    logging.info("Total video length : %s",seek_bar_time[1])

  def _teardown(self):
    self.dut.mbs.pressBack()
    self.dut.mbs.pressBack()
    self.dut.mbs.pressBack()
    self.dut.mbs.pressBack()
    self.dut.mbs.pressHome()

  def _enableCaptions(self):
    self.dut.mbs.display_YT_Media_Player_Controls()
    self.dut.mbs.waitAndClickUsingResourceId(yt_selectors.YT_CAPTION_THREE_DOT_BUTTON)
    CURRENT_CAPTION_SELECTION = self.dut.mbs.getCaptionSelected(yt_selectors.CAPTIONS)
    logging.info("Current caption selection text : %s",CURRENT_CAPTION_SELECTION)
    #self.dut.mbs.pressBack()
    if yt_selectors.LANGUAGE in CURRENT_CAPTION_SELECTION:
      logging.info("Captions already enabled.")
      self.dut.mbs.pressBack()
    else:
      logging.info("Captions is disabled, enabling.")
      #self.dut.mbs.display_YT_Media_Player_Controls()
      #self.dut.mbs.waitAndClickUsingResourceId(yt_selectors.YT_CAPTION_THREE_DOT_BUTTON)
      self.dut.mbs.clickOnText(yt_selectors.CAPTIONS)
      self.dut.mbs.clickOnText(yt_selectors.CAPTION_LANGUAGE)
      time.sleep(2)

  def _disableCaptions(self):
    self.dut.mbs.display_YT_Media_Player_Controls()
    logging.info("Disabling captions")
    self.dut.mbs.clickUsingResourceId(yt_selectors.YT_CAPTION_THREE_DOT_BUTTON)
    logging.info("Clicked on more options button")
    CURRENT_CAPTION_SELECTION = self.dut.mbs.getCaptionSelected(yt_selectors.CAPTIONS)
    logging.info("Current caption : %s",CURRENT_CAPTION_SELECTION)
    #self.dut.mbs.pressBack()
    if yt_selectors.LANGUAGE in CURRENT_CAPTION_SELECTION:
      logging.info("Captions enabled, disabling it.")
      #self.dut.mbs.display_YT_Media_Player_Controls()
      #self.dut.mbs.waitAndClickUsingResourceId(yt_selectors.YT_CAPTION_THREE_DOT_BUTTON)
      self.dut.mbs.clickOnText(yt_selectors.CAPTIONS)
      self.dut.mbs.clickOnText("Turn off captions")
      time.sleep(2)
    else:
      logging.info("Captions is disabled already.")

  def _unlock_screen(self):
    self.dut.mbs.inputKeyEvent(224)
    self.dut.mbs.inputKeyEvent(82)

  def _favorite_food(self):
    food = self.user_params.get('favorite_food')
    drink = self.user_params.get('favorite_drink')
    if food:
      self.dut.mbs.makeToast("I'd like to eat %s." % food)
      time.sleep(5)
    else:
      self.dut.mbs.makeToast("I'm not hungry.")
    if drink:
      self.dut.mbs.makeToast("I'd like to drink %s." % food)
    else:
      self.dut.mbs.makeToast("I'm not hungry.")


if __name__ == '__main__':
  test_runner.main()
