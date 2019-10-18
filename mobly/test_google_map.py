from mobly import base_test
from mobly import test_runner
from mobly.controllers import android_device
import time
import logging
import map_selectors
import re
import cv2 as cv
import os
from PIL import Image, ImageEnhance
import gTAF_config
import os.path


class GTAF_MAP_TEST(base_test.BaseTestClass):

    def setup_class(self):
        # Registering android_device controller module declares the test's
        # dependency on Android device hardware. By default, we expect at
        # least one object is created from this.
        self.ads = self.register_controller(android_device)
        self.dut = self.ads[0]
        # Start Mobly Bundled Snippets (MBS).
        # self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.bundled')
        self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.example4')

    def test_place_search_by_text(self):
        """
        Test: To verify search place in google map
        :return:None
        """
        try:
            assert self.dut.mbs.isOnline() is True, "Internet is not working in device"
            self._unlock_screen()
            self.dut.mbs.pressHome()
            self._turn_ON_location_services()
            self.dut.mbs.launchGoogleMap()
            time.sleep(2)
            logging.info("Click on current location button")
            self.dut.mbs.waitAndClickUsingResourceId(map_selectors.MY_LOCATION_BUTTON)
            time.sleep(5)
            self.dut.mbs.waitAndClickUsingClass(map_selectors.SEARCH_BOX_BUTTON)
            logging.info("Entering destination")
            time.sleep(2)
            self.dut.mbs.inputText("HCL")
            self.dut.mbs.inputKeyEvent(62)
            self.dut.mbs.inputText("America")
            self.dut.mbs.inputKeyEvent(62)
            self.dut.mbs.inputText("Sunnyvale")
            time.sleep(2)
            self.dut.mbs.inputKeyEvent(map_selectors.ENTER_KEY_CODE)
            time.sleep(10)

            if os.path.exists(gTAF_config.gTAF_home + "map_actual_image.png"):
                os.system("rm map_actual_image.png")
            if os.path.exists(gTAF_config.gTAF_home + "rm map_cropped_image.png"):
                os.system("rm map_cropped_image.png")

            self._capture_screenshot() # output - map_actual_image.png

            src_img = gTAF_config.gTAF_home + "map_actual_image.png"
            enhance_img = gTAF_config.gTAF_home + "map_enhance_image.png"
            ref_img = gTAF_config.gTAF_home + "map_ref_image.png"

            assert os.path.exists(src_img) == True, "map_actual_image.png image not found"

            self._img_enhance(src_img, enhance_img) # output -map_enhance_image.png

            assert os.path.exists(ref_img) == True, "map_ref_image.png image not found"
            assert os.path.exists(enhance_img) == True, "map_enhance_image.png image not found"

            self._crop_image((0, 60, 1060, 1900), enhance_img) # output - map_cropped_image.png
            map_cropped_img = gTAF_config.gTAF_home + "map_cropped_image.png"
            assert os.path.exists(map_cropped_img) == True, "map_cropped_image.png image not found"
            cmp_result = self._yt_vedio_image_cmp(map_cropped_img, ref_img)
            assert cmp_result == True, "Images are not equal"
        finally:
            self._press_back()


    def test_place_search_by_voice(self):
        """
        Test: To verify search place in google map using voice command
        :return:None
        """
        press_home = "adb -s " + gTAF_config.GMAP_AUDIO_PALAYER_DEVICE_SERIAL + " shell input keyevent 3"
        try:
            assert self.dut.mbs.isOnline() == True, "Internet is not working in device"
            self._unlock_screen()
            self.dut.mbs.pressHome()
            self._turn_ON_location_services()
            self.dut.mbs.launchGoogleMap()
            time.sleep(2)
            logging.info("Click on current location button")
            self.dut.mbs.waitAndClickUsingResourceId(map_selectors.MY_LOCATION_BUTTON)
            time.sleep(5)
            self.dut.mbs.waitAndClickUsingClass(map_selectors.SEARCH_BOX_BUTTON)
            logging.info("Speaking voice command")
            time.sleep(2)
            self.dut.mbs.waitAndClickUsingContentDesc("Tap to speak")
            time.sleep(5)
            logging.info(press_home)
            #os.system(press_home)
            logging.info("Playing voice command to search a place")
            self._play_voice_search_command(gTAF_config.GMAP_AUDIO_PALAYER_DEVICE_SERIAL, gTAF_config.GMAP_SEARCH_AUDIO_FILE)
            time.sleep(20)
            '''
            self.dut.mbs.inputText("HCL")
            self.dut.mbs.inputKeyEvent(62)
            self.dut.mbs.inputText("America")
            self.dut.mbs.inputKeyEvent(62)
            self.dut.mbs.inputText("Sunnyvale")
            time.sleep(2)
            self.dut.mbs.inputKeyEvent(map_selectors.ENTER_KEY_CODE)
            time.sleep(10)
            
            '''
            
            if os.path.exists(gTAF_config.gTAF_home + "map_actual_image.png"):
                os.system("rm map_actual_image.png")
            if os.path.exists(gTAF_config.gTAF_home + "map_cropped_image.png"):
                os.system("rm map_cropped_image.png")
            if os.path.exists(gTAF_config.gTAF_home + "map_enhance_image.png"):
                os.system("rm map_enhance_image.png")

            self._capture_screenshot() # output - map_actual_image.png

            src_img = gTAF_config.gTAF_home + "map_actual_image.png"
            enhance_img = gTAF_config.gTAF_home + "map_enhance_image.png"
            ref_img = gTAF_config.gTAF_home + "map_ref_image.png"

            assert os.path.exists(src_img) == True, "map_actual_image.png image not found"

            self._img_enhance(src_img, enhance_img) # output -map_enhance_image.png

            assert os.path.exists(ref_img) == True, "map_ref_image.png image not found"
            assert os.path.exists(enhance_img) == True, "map_enhance_image.png image not found"

            self._crop_image((0, 60, 1060, 1900), enhance_img) # output - map_cropped_image.png
            map_cropped_img = gTAF_config.gTAF_home + "map_cropped_image.png"
            assert os.path.exists(map_cropped_img) == True, "map_cropped_image.png image not found"
            cmp_result = self._yt_vedio_image_cmp(map_cropped_img, ref_img)
            assert cmp_result == True, "Images are not equal"
        finally:
            print("")
            self._press_back()
            os.system(press_home)


    def test_route_image(self):
        """
        Test: To verify multi-way point route
        :return:None
        """
        #self._unlock_screen()
        #self.dut.mbs.pressHome()
        #self._turn_ON_location_services()
        self.dut.mbs.launchGoogleMap()
        time.sleep(2)
        logging.info("Click on current location button")
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.MY_LOCATION_BUTTON)
        time.sleep(5)
        logging.info("Click on GO button")
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.DIRECTION_BUTTON)
        time.sleep(2)
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.DESTINATION_TEXT_BOX)
        logging.info("Entering destination")
        self.dut.mbs.inputText("India")
        self.dut.mbs.inputKeyEvent(62)
        self.dut.mbs.inputText("Gate")
        time.sleep(2)
        self.dut.mbs.inputKeyEvent(map_selectors.ENTER_KEY_CODE)
        time.sleep(5)

        os.system("rm map_actual_image.png")
        os.system("rm map_cropped_image.png")
        self._capture_screenshot()

        src_img = gTAF_config.gTAF_home + "map_actual_image.png"
        ref_img = gTAF_config.gTAF_home + "map_ref_image.png"

        assert os.path.exists(src_img) == True, "map_actual_image.png image not found"
        assert os.path.exists(ref_img) == True, "map_ref_image.png image not found"

        self._crop_image((0, 60, 1060, 1900), src_img)

        map_cropped_img = gTAF_config.gTAF_home + "map_cropped_image.png"
        assert os.path.exists(map_cropped_img) == True, "map_cropped_image.png image not found"

        cmp_result = self._yt_vedio_image_cmp(ref_img, map_cropped_img)
        print(cmp_result)
        assert cmp_result == True, "Images are not equal"
        self._press_back()

    def test_search_bar_autocomplete(self):
        """
      Test: To verify search bar Autocomplete feature test.
      :return : None
      """
        self._unlock_screen()
        self.dut.mbs.pressHome()
        self.dut.mbs.launchGoogleMap()
        time.sleep(3)
        self.dut.mbs.waitAndClickUsingClass(map_selectors.SEARCH_BOX_BUTTON)
        self.dut.mbs.inputText(map_selectors.SEARCH_TEXT_FULL)
        time.sleep(3)
        searched_text = self.dut.mbs.gettext()
        logging.info("Found '%s' on searching of '%s' in search box", searched_text, map_selectors.SEARCH_TEXT_FULL)
        if map_selectors.EXPECTED_FULL_SEARCH_RESULT in searched_text:
            assert True
        else:
            assert False
        self.dut.mbs.pressBack()
        self.dut.mbs.pressBack()
        self.dut.mbs.waitAndClickUsingClass(map_selectors.SEARCH_BOX_BUTTON)
        self.dut.mbs.inputText(map_selectors.SEARCH_TEXT_PARTIAL)
        self.dut.mbs.inputKeyEvent(map_selectors.SPACE_BAR_KEY_CODE)
        self.dut.mbs.pressBack()

        searched_text = self.dut.mbs.getTextMultiple()
        for i in range(0, len(searched_text)):
            tmp = searched_text[i].split(" ")
            if tmp[0] == map_selectors.SEARCH_TEXT_PARTIAL:
                logging.info("First letter in '%s' found as : '%s' ", searched_text[i],
                             map_selectors.SEARCH_TEXT_PARTIAL)
                assert True
            else:
                logging.info("First letter in '%s' not found as : '%s' ", searched_text[i],
                             map_selectors.SEARCH_TEXT_PARTIAL)
                assert False
        self._press_back()
        self._press_back()

    def test_gmap_location_services_disabled(self):
        """
        Test: To verify pop-up in gmaps when location services disabled

        :return: None
        """
        self._unlock_screen()
        self.dut.mbs.pressHome()
        self._turn_ON_location_services()
        self.dut.mbs.launchGoogleMap()
        time.sleep(2)
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.MY_LOCATION_BUTTON)
        time.sleep(5)
        self.dut.mbs.pressBack()
        logging.info("Disabling location services")
        self._turn_OFF_location_services()
        logging.info("Launching Google maps")
        self.dut.mbs.launchGoogleMap()
        time.sleep(5)
        logging.info("Verifying pop-up")

        if (self.dut.mbs.mapPopup()):
            logging.info("Pop-up displayed")
            ACTUAL_POP_UP_TEXT = re.sub(u"(\u2018|\u2019)", "'", self.dut.mbs.getTextByResourceId("com.google.android.gms:id/message"))
            logging.info("Actual pop-up text found : '%s'", ACTUAL_POP_UP_TEXT)
            assert map_selectors.MAP_POP_UP_TEXT == ACTUAL_POP_UP_TEXT, "Pop-up text message not matched"
        else:
            logging.info("Pop-up not displayed")
            assert False
        self.dut.mbs.pressHome()

    def test_tapping_current_place_button(self):
        """
        Test: To verify tapping current place button shows current place on the map.
        :return:None
        """
        self._unlock_screen()
        self.dut.mbs.pressHome()
        self._turn_ON_location_services()
        self.dut.mbs.launchGoogleMap()
        time.sleep(2)
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.MY_LOCATION_BUTTON)
        time.sleep(2)
        self._press_back()

    def test_multiway_point_route(self):
        """
        Test: To verify multi-way point route
        :return:None
        """
        self._unlock_screen()
        self.dut.mbs.pressHome()
        self._turn_ON_location_services()
        self.dut.mbs.launchGoogleMap()
        time.sleep(2)
        logging.info("Click on current location button")
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.MY_LOCATION_BUTTON)
        time.sleep(2)
        logging.info("Click on GO button")
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.DIRECTION_BUTTON)
        time.sleep(2)
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.DESTINATION_TEXT_BOX)
        logging.info("Entering destination")
        self.dut.mbs.inputText(map_selectors.SEARCH_TEXT_FULL)
        time.sleep(2)
        self.dut.mbs.inputKeyEvent(map_selectors.ENTER_KEY_CODE)
        time.sleep(5)
        self._press_back()

    def test_accessibility_talkback_settings(self):
        """
        Test: To verify talkback accessibility test
        :return:None
        """
        self._unlock_screen()
        self.dut.mbs.pressHome()
        self._turn_ON_location_services()
        self._turn_ON_talkback_service()
        self.dut.mbs.launchGoogleMap()
        time.sleep(2)
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.MY_LOCATION_BUTTON)
        time.sleep(3)
        logging.info("Click on base compass button")
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.BASE_COMPASS_BUTTON)
        time.sleep(2)
        logging.info("Click on search box")
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.SEARCH_TEXT_BOX)
        time.sleep(2)
        self.dut.mbs.pressBack()
        self.dut.mbs.pressBack()
        time.sleep(2)
        logging.info("Click on GO button")
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.DIRECTION_BUTTON)
        time.sleep(1)
        self.dut.mbs.pressBack()
        logging.info("Click on menu button")
        self.dut.mbs.waitAndClickUsingResourceId(map_selectors.SEARCH_TEXT_BOX)
        time.sleep(1)
        self.dut.mbs.pressBack()
        time.sleep(2)
        self._press_back()
        self._turn_OFF_talkback_service()

    def _play_voice_search_command(self, dev_id, file_name):
        logging.info("Playing voice search command on %s : ", dev_id)
        file_push_cmd = "adb -s " + dev_id + " push " + file_name + "  /sdcard"
        set_player_vol = "adb -s " + dev_id + "  shell media volume --set 15"
        play_audio_cmd = "adb -s " + dev_id + " shell am start -a android.intent.action.VIEW -d file:///sdcard/" + file_name + " -t audio/wav"
        logging.info(file_push_cmd)
        logging.info(set_player_vol)
        logging.info(play_audio_cmd)

        audio_file = gTAF_config.gTAF_home + file_name
        assert os.path.exists(audio_file) == True, "Audio file not found"
        logging.info("Push file to player device")
        os.system(file_push_cmd)
        logging.info("Set volume in device")
        os.system(set_player_vol)
        logging.info("Playing audio command")
        os.system(play_audio_cmd)

    def _img_enhance(self, in_img, out_img):
        logging.info("Performing image enhancement")
        im = Image.open(in_img)
        enhancer = ImageEnhance.Brightness(im)
        enhanced_im = enhancer.enhance(1.2)
        enhanced_im.save(out_img)

    def _capture_screenshot(self):
        logging.info("Capturing screenshot of map application")
        self.dut.mbs.executeCommandOnDevice(" screencap -p /sdcard/map_actual_image.png")
        cmd = "adb -s " + gTAF_config.map_test_device_id + " pull /sdcard/map_actual_image.png ."
        logging.info(cmd)
        os.system(cmd)
        self.dut.mbs.executeCommandOnDevice(" rm /sdcard/map_actual_image.png")

    def _crop_image(self,coords, src_img):
        logging.info("Cropping image")
        image_obj = Image.open(src_img)
        cropped_image = image_obj.crop(coords)
        cropped_image.save("map_cropped_image.png")
        logging.info("Image cropped")

    def _yt_vedio_image_cmp(self,actual, ref):
        logging.info("Performing image comparison")
        logging.info(actual)
        logging.info(ref)
        img_1 = cv.imread(actual)
        img_2 = cv.imread(ref)

        if img_1.shape == img_2.shape:
            logging.info("The images have same size and channels")
            difference = cv.subtract(img_1, img_2)
            b, g, r = cv.split(difference)
            logging.info("r, g, b differences values of captured screenshots")
            logging.info("Diff for r component : %s", cv.countNonZero(r))
            logging.info("Diff for g component : %s", cv.countNonZero(g))
            logging.info("Diff for b component : %s", cv.countNonZero(b))

            if cv.countNonZero(b) < 100 and cv.countNonZero(g) < 100 and cv.countNonZero(r) < 100:
                logging.info("Captured screenshots are equal, which is expected")
                return True
            else:
                logging.info("Captured screenshots are not equal")
                return False
        else:
            logging.info("The images do not have same size and channels")
            return False

    def _turn_ON_location_services(self):
        logging.info("Turning ON location services")
        self.dut.mbs.launchSettings()
        self.dut.mbs.clickOnTextScrollDown(map_selectors.SECURITY_AND_LOCATION)
        self.dut.mbs.clickOnTextScrollDown(map_selectors.LOCATION)
        LOCATION_STATUS = self.dut.mbs.getTextByResourceId(map_selectors.TOGGLE_BUTTON)
        if 'OFF' in LOCATION_STATUS:
            logging.info("Currently location services are disabled, enabling it")
            self.dut.mbs.waitAndClickUsingResourceId(map_selectors.TOGGLE_BUTTON)
        else:
            logging.info("Location services already enabled")
        time.sleep(3)
        self._press_back()

    def _turn_OFF_location_services(self):
        logging.info("Turning OFF location services")
        self.dut.mbs.launchSettings()
        self.dut.mbs.clickOnTextScrollDown(map_selectors.SECURITY_AND_LOCATION)
        self.dut.mbs.clickOnTextScrollDown(map_selectors.LOCATION)
        _LOCATION_STATUS = self.dut.mbs.getTextByResourceId(map_selectors.TOGGLE_BUTTON)
        if 'ON' in _LOCATION_STATUS:
            logging.info("Currently location services are enabled, disabling it")
            self.dut.mbs.waitAndClickUsingResourceId(map_selectors.TOGGLE_BUTTON)
        else:
            logging.info("Location services already disabled")

        time.sleep(3)
        self._press_back()

    def _unlock_screen(self):
        self.dut.mbs.inputKeyEvent(224)
        self.dut.mbs.inputKeyEvent(82)

    def _turn_ON_talkback_service(self):
        logging.info("Turning ON talkback service")
        self.dut.mbs.launchSettings()
        self.dut.mbs.clickOnTextScrollDown(map_selectors.ACCESSIBILITY)
        _is_enabled = self.dut.mbs.clickOnTextScrollDown("Off/Speak items on screen")
        if _is_enabled is False:
            logging.info("Talkback enabled already")
        else:
            logging.info("Talkback not enabled, enabling it")
            self.dut.mbs.clickOnTextScrollDown("Off/Speak items on screen")
            self.dut.mbs.waitAndClickUsingResourceId(map_selectors.TOGGLE_BUTTON)
            time.sleep(2)
            self.dut.mbs.waitAndClickUsingResourceId(map_selectors.POP_UP_OK_BUTTON)
            logging.info("Talkback enabled now")
            time.sleep(2)
        self._press_back()

    def _turn_OFF_talkback_service(self):
        logging.info("Turning ON talkback service")
        self.dut.mbs.launchSettings()
        self.dut.mbs.clickOnTextScrollDown(map_selectors.ACCESSIBILITY)
        _is_disabled = self.dut.mbs.clickOnTextScrollDown("On/Speak items on screen")

        if _is_disabled is False:
            logging.info("Talkback disabled already")
        else:
            logging.info("Talkback not disable, disabling it")
            self.dut.mbs.clickOnTextScrollDown("On/Speak items on screen")
            self.dut.mbs.waitAndClickUsingResourceId(map_selectors.TOGGLE_BUTTON)
            time.sleep(2)
            self.dut.mbs.waitAndClickUsingResourceId(map_selectors.POP_UP_OK_BUTTON)
            logging.info("Talkback disabled now")
            time.sleep(2)
        self._press_back()

    def _press_back(self):
        self.dut.mbs.pressBack()
        self.dut.mbs.pressBack()
        self.dut.mbs.pressBack()


if __name__ == '__main__':
    test_runner.main()
