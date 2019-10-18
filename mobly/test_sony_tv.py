import logging
import os
import random
import time
import subprocess
from collections import OrderedDict
import cv2
import re
import pytesseract
from PIL import Image
import gTAF_config
import tv_selectors
from mobly.config_parser import dev_li as device_list
from mobly import base_test
from mobly import config_parser
from mobly import test_runner
from mobly.controllers import android_device


class SonyTV(base_test.BaseTestClass):

    def setup_class(self):
        global home
        android_version_cmd = "adb -s " + device_list[0] + " shell getprop ro.build.version.release"
        android_version = subprocess.check_output(android_version_cmd, shell=True)
        android_version = android_version.strip()
        logging.info("android_version : %s", android_version)

        device_model_cmd = "adb  -s " + device_list[0] + " shell getprop ro.product.model"
        device_model = subprocess.check_output(device_model_cmd, shell=True)
        device_model = device_model.strip()
        logging.info("device_model : %s", device_model)

        logging.info(
            "Loading device configuration for %s device[Android version-%s]",
            device_model, android_version)
        gTAF_config.load_device_config(dev_model=device_model, android_version=android_version)
        uiElement = gTAF_config.uiElement
        home = uiElement['HOME']

        self.ads = self.register_controller(android_device)
        self.dut = self.ads[0]
        logging.info("List of device found in test bed : %s", config_parser.dev_li)
        self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.example4')
        logging.info("Launching contact app on device with device id :%s ", device_list[0])

    def test_tv_youtube_video_playback(self):
        try:
            # self.add_account()

            if self.dut.mbs.isOnline():

                print("1111")
                os.system("adb shell am start -a android.intent.action.VIEW -d https://www.youtube.com/watch?v=vZYmVNinG4k")
                time.sleep(5)

                if self.dut.mbs.assertTextDisplayed("YouTube"):
                    logging.info("Clicking on YouTube")
                    self.dut.mbs.clickOnText("YouTube")
                if self.dut.mbs.assertTextDisplayed("JUST ONCE"):
                    logging.info("Clicking on JUST ONCE")
                    self.dut.mbs.clickOnText("JUST ONCE")

                logging.info("Playing video")
                time.sleep(5)
                self.dut.mbs.inputKeyEvent(66)
                time.sleep(1)
                self.dut.mbs.inputKeyEvent(66)
                time.sleep(5)
                self.capture_screen_shot(image_name='yt_tv.png')
                time.sleep(1000)

                # com.google.android.youtube.tv:id/title_badge   yt icon on home yt screen assert
                # search button - com.google.android.youtube.tv:id/search_orb
                self.dut.mbs.launchApp(tv_selectors.YOUTUBE_TV_LAUNCH_ACTIVITY)
                time.sleep(2)

                logging.info("Verifying Youtube badge icon")
                assert self.dut.mbs.waitUntillDisplayElementWithResID(tv_selectors.YOUTUBE_TITLE_BADGE_RES_ID) is True, "Youtube badge icon not displayed"
                logging.info("Verifying Youtube Home text")
                self.dut.mbs.assertTextDisplayed("Home")
    
                logging.info("Verifying Youtube search button")
                assert self.dut.mbs.waitUntillDisplayElementWithResID(tv_selectors.YOUTUBE_HOME_SEARCH_BUTTON_RES_ID) is True, "Search button not displayed"
                time.sleep(3)

                logging.info("Right key event")
                self.dut.mbs.inputKeyEvent(22)
                logging.info("Right key event")
                self.dut.mbs.inputKeyEvent(22)
                time.sleep(2)

                logging.info("Playing video")
                self.dut.mbs.inputKeyEvent(66)
                time.sleep(10)
                logging.info("Youtube Media play-bar display")
                self.dut.mbs.inputKeyEvent(66)
                logging.info("Searching for play button")
                time.sleep(5)
                assert self.dut.mbs.waitUntillDisplayElementWithContentDesc(tv_selectors.YOUTUBE_TV_PLAY_BUTTON) is True, "Play button not found on screen"
                logging.info("Searching for rewind button")
                assert self.dut.mbs.waitUntillDisplayElementWithContentDesc(tv_selectors.YOUTUBE_TV_REWIND_BUTTON) is True, "Rewind button not found on screen"
                logging.info("Searching for fast forward button")
                assert self.dut.mbs.waitUntillDisplayElementWithContentDesc(tv_selectors.YOUTUBE_TV_FAST_FWD_BUTTON) is True, "Fast-Forward button not found on screen"
                logging.info("Youtube Media play-bar displayed")

                logging.info("Searching for 'High Quality button' on player-bar")
                assert self.dut.mbs.waitUntillDisplayElementWithContentDesc(tv_selectors.VIDEO_QUALITY_TOGGLE_BUTTON_DESC) is True, "Disable High Quality button not found on screen"
                logging.info("Disable High Quality button found on player-bar")
                self.dut.mbs.waitAndClickUsingContentDesc(tv_selectors.VIDEO_QUALITY_TOGGLE_BUTTON_DESC)
                self.dut.mbs.waitAndClickUsingContentDesc(tv_selectors.VIDEO_QUALITY_TOGGLE_BUTTON_DESC)

    
                #self.dut.mbs.assertTextDisplayed("720p")
                #time.sleep(2)
                #self.dut.mbs.clickOnText("720p")
                #self.capture_screen_shot(image_name='tvsnap.png')
    
    
                # adb shell am start -n com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.TvGuideActivity
                # self.dut.mbs.executeShellCommand(" am start -n com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.TvGuideActivity")
                # os.system("adb shell am start -n com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.TvGuideActivity")
                #self.dut.mbs.waitAndClickUsingResourceId("com.google.android.youtube.tv:id/search_orb")
            else:
                logging.info("Device is offline")
        finally:
            self.dut.mbs.inputKeyEvent(4)
            self.dut.mbs.inputKeyEvent(4)
            self.dut.mbs.inputKeyEvent(4)
            self.dut.mbs.inputKeyEvent(3)

    def test_tv_google_play_movie_playback(self):
        pass

    def test_tv_hdmi_video_playback(self):
        pass

    def add_account(self):
        self.dut.mbs.launchApp(tv_selectors.YOUTUBE_TV_LAUNCH_SETTINGS)
        self.dut.mbs.waitUntillDisplayElementWithText("Settings")
        logging.info("Settings displayed")
        logging.info("Click on Add account")
        self.dut.mbs.clickOnTextScrollDown("Add account")
        self.dut.mbs.waitUntillDisplayElementWithText("Choose account type")
        logging.info("Assert 'Choose account type'")
        self.dut.mbs.assertTextDisplayed("Choose account type")
        logging.info("Assert 'Google'")
        self.dut.mbs.assertTextDisplayed("Google")
        logging.info("click on 'Google'")
        self.dut.mbs.clickOnText("Google")
        self.dut.mbs.waitUntillDisplayElementWithText("Use your password")
        logging.info("click on 'Use your password'")
        self.dut.mbs.clickOnText("Use your password")
        self.dut.mbs.waitUntillDisplayElementWithText("Enter your account email address")
        self.dut.mbs.inputKeyEvent(66)
        logging.info("Enter email id")
        self.dut.mbs.inputText("aiytest11111@gmail.com")
        self.dut.mbs.inputKeyEvent(66)
        self.dut.mbs.waitUntillDisplayElementWithText("Enter your account password")
        logging.info("Enter login password")
        self.dut.mbs.inputText("Testing@123")
        self.dut.mbs.inputKeyEvent(66)
        logging.info("Signing in account...")
        time.sleep(10)
        self.dut.mbs.waitUntillDisplayElementWithText("Settings")

        self.dut.mbs.clickOnTextScrollDown("aiytest11111@gmail.com")

        assert self.dut.mbs.assertTextDisplayed("aiytest11111@gmail.com") is True, "Could not Signed In.."

        logging.info("Account logged in successfully...")







    def capture_screen_shot(self, image_name):
        """
        To capture screen shot of the screen
        :param image_name:
        :return:
        """
        logging.info("Capturing screenshot...")
        self.dut.mbs.executeCommandOnDevice(" screencap -p /sdcard/" + image_name)
        cmd = "adb -s " + config_parser.dev_li[0] + " pull /sdcard/" + image_name + " ."
        logging.info(cmd)
        os.system(cmd)
        self.dut.mbs.executeCommandOnDevice(" rm /sdcard/" + image_name)

if __name__ == '__main__':
    test_runner.main()

