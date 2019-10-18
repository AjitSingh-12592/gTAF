from mobly import base_test
from mobly import test_runner
from mobly.controllers import android_device
import time
import logging
import os
import pytesseract
import cv2
import subprocess
import map_selectors
import gTAF_config
import twilight_app_seletors
from mobly import config_parser

class Twilight(base_test.BaseTestClass):

    def setup_class(self):

    # Registering android_device controller module declares the test's
      self.ads = self.register_controller(android_device)
      self.dut = self.ads[0]

    # Start Mobly Bundled Snippets (MBS)
      self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.example4')

    def test_Oculus_App_Launch(self):
        """
        TC[T2057894818] :Verify that the Companion app can be launched
        :return: None
        """
        try:
            logging.info("Executing 'Twilight app launch '")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._unlock_screen()
            self.dut.mbs.pressHome()
            self.dut.mbs.launchApp(twilight_app_seletors.TWILIGHT_APP_LAUNCHER_ACTIVITY)
            self._twilight_app_login()

            logging.info("Asserting Select Headset")
            assert self.dut.mbs.assertTextDisplayed(
                twilight_app_seletors.SELECT_HEADSET) is True, "Expected element not found"

            logging.info("Asserting Oculus Go")
            assert self.dut.mbs.assertTextDisplayed(
                twilight_app_seletors.OCULUS_GO) is True, "Expected element not found"

            logging.info("Asserting Oculus Quest")
            assert self.dut.mbs.assertTextDisplayed(
                twilight_app_seletors.OCULUS_QUEST) is True, "Expected element not found"

            logging.info("Asserting Oculus Rift S")
            assert self.dut.mbs.assertTextDisplayed(
                twilight_app_seletors.OCULUS_RIFT_S) is True, self._captureScreenShot_IfassertFail(
                "Oculus Rift S not found", "oculus_rift_s.png")
            '''
            if self._is_twilight_app_logged_in():
                logging.info("User already logged in, verifying screen elements")
                assert self.dut.mbs.assertTextDisplayed(twilight_app_seletors.SELECT_HEADSET) is True, "Expected element not found"
                assert self.dut.mbs.assertTextDisplayed(twilight_app_seletors.OCULUS_GO) is True, "Expected element not found"
                assert self.dut.mbs.assertTextDisplayed(twilight_app_seletors.OCULUS_QUEST) is True, "Expected element not found"
                assert self.dut.mbs.assertTextDisplayed(twilight_app_seletors.OCULUS_RIFT_S) is True, self._captureScreenShot_IfassertFail("Oculus Rift S not found", "oculus_rift_s.png")
            else:
                assert self._twilight_app_login() is True, "Expected element not found"
            '''

        finally:
            logging.info("Execution finish")

    def test_Oculus_SignIn_Existing_Acnt(self):
        """
        TC[T2057894845]: Verify that the User can Sign-In to an existing Oculus account
        :return: None
        """
        try:
            logging.info("Executing : Verify that the User can Sign-In to an existing Oculus account")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._unlock_screen()
            self.dut.mbs.pressHome()

            if self._is_twilight_app_logged_in() is not True:
                assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.SIGN_IN) is True, " Sign in Text not found on screen"
                self.dut.mbs.clickOnText(twilight_app_seletors.SIGN_IN)
                assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.FORGOT_PASSWORD) is True, "Cross Button OR Next Button doesn't exist"
                self.dut.mbs.clickOnText(twilight_app_seletors.UNAME_TEXT)

                logging.info("Enter login username")
                self.dut.mbs.inputText(twilight_app_seletors.USERNAME)
                assert self.dut.mbs.isNextButtonEnabled() is False, "NEXT button is enabled before entering the password"

                logging.info("Enter login password")
                self.dut.mbs.inputKeyEvent('66')
                self.dut.mbs.inputText(twilight_app_seletors.PASSWORD)
                assert self.dut.mbs.isNextButtonEnabled() is True, "NEXT button is enabled before entering the password"
                self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)
            else:
                logging.info("User already logged in")

            logging.info("Assert screen elements after signIn")
            # Assert whether logged in screen found or not
            select_headset = self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.SELECT_HEADSET)
            oculus_go = self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_GO)
            oculus_rift_s = self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_RIFT_S)

            assert select_headset is True and oculus_rift_s is True and oculus_go is True, "Not landed on correct screen after login"
        finally:
            self._press_back(8)

    def test_Oculus_User_Logout(self):
        """
        TC[T2057895410]: Verify user can log out of their account.
        :return: None
        """
        try:
            logging.info("Executing : Verify user can log out of their account.")
            self._clear_app_storage_cache()
            self._unlock_screen()
            self.dut.mbs.pressHome()

            if self._is_twilight_app_logged_in():
                logging.info("User already logged In")
                logging.info("Check if select headset screen found, if found click on 'X'")
                print(self.dut.mbs.assertCrossButton())
                if self.dut.mbs.assertCrossButton():
                    logging.info("'X' button found")
                    self.dut.mbs.clickCrossButton()
            else:
                logging.info("Launching Twilight App")
                self.dut.mbs.launchApp(twilight_app_seletors.TWILIGHT_APP_LAUNCHER_ACTIVITY)
                self._twilight_app_login()
                logging.info("Check if select headset screen found, if found click on 'X'")
                if self.dut.mbs.assertCrossButton():
                    logging.info("'X' button found")
                    self.dut.mbs.clickCrossButton()

            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.SETTINGS) is True, "Settings not found"
            logging.info("Clicking on Settings")
            self.dut.mbs.clickOnText(twilight_app_seletors.SETTINGS)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.SETTINGS) is True, "Account not found on Settings tab"
            logging.info("Clicking on Log Out")
            self.dut.mbs.clickOnTextScrollDown(twilight_app_seletors.LOG_OUT)
            logging.info("Asserting Log Out Confirmation Popup")
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.CANCEL) is True, "Log Out Dialog did'nt appear"
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.POP_UP_LOGOUT) is True, "Log Out Dialog did'nt appear"
            self.dut.mbs.clickOnText(twilight_app_seletors.POP_UP_LOGOUT)
            logging.info("Verifying screen after log out")
            fb_text = self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.FACEBOOK_CONTINUE_TEXT)
            terms_login_screen = self.dut.mbs.assertTextDisplayed(twilight_app_seletors.TERMS_OF_SERVICES)
            privacy_policy_text = self.dut.mbs.assertTextDisplayed(twilight_app_seletors.PRIVACY_POLICY_LOGIN_SCREEN)
            logging.info(fb_text)
            logging.info(terms_login_screen)
            logging.info(privacy_policy_text)
            if fb_text is True and terms_login_screen is True and privacy_policy_text is True:
                logging.info("User logged out successfully")
                assert True
            else:
                logging.info("User could not logged out successfully")
                assert False
        finally:
            self._press_back(8)

    def test_Oculus_Past_Enable_Location(self):
        """
        TC[T2057901985] : Verify user can proceed past Enable Location prompt after enabling Location
        :return:None
        """
        try:
            logging.info("Executing : 'Verify user can proceed past Enable Location prompt after enabling Location'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._turn_OFF_location_services()
            self._enable_bluetooth()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.START)
            logging.info("Click on start")
            self.dut.mbs.clickOnText(twilight_app_seletors.START)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.CONTINUE)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.PLUG_IN_HEADSET_TEXT)
            logging.info("Click on continue")
            self.dut.mbs.clickOnText(twilight_app_seletors.CONTINUE)

            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.TURN_HEADSET_TEXT)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.NEXT)
            logging.info("Click on next")
            self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)

            # Assert location pop up
            logging.info("Checking for Next button on popup")
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.NEXT)

            if self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.LOCATION_ACCESS):
                logging.info("Location Access popup found")
                self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)
                assert self.dut.mbs.waitUntillDisplayElementWithText(
                    twilight_app_seletors.LOCATION_PUPUP_ACCESS_GRANT) is True, "Expected text not found"
                logging.info("Checking for popup DENY/ALLOW buttons")
                assert self.dut.mbs.waitUntillDisplayElementWithText(
                    twilight_app_seletors.DENY) is True, "Expected text not found"
                assert self.dut.mbs.waitUntillDisplayElementWithText(
                    twilight_app_seletors.ALLOW) is True, "Expected text not found"
                self.dut.mbs.clickOnText(twilight_app_seletors.ALLOW)
            else:
                logging.info("Location Access popup not found")
                assert False

            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.ENABLE_LOCATION_SERVICES), "Enable Location Services not found"
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.GO_TO_SETTINGS), "Go To Settings not found"

            logging.info("Click on Go To Settings button")
            self.dut.mbs.clickOnText(twilight_app_seletors.GO_TO_SETTINGS)

            logging.info("Enabling GPS location services")
            self.dut.mbs.waitAndClickUsingResourceId(map_selectors.TOGGLE_BUTTON)
            self._press_back(1)

            logging.info("Assert looking for headset")
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.LOOKING_FOR_HEADSET) is True, "Looking for headset screen text not found"
            logging.info("Assert pairing code screen")
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.PAIRING_CODE) is True, "Pairing screen not found"
        finally:
            self.dut.mbs.pressHome()

    def test_Oculus_PlugIn_Hset_Rdblck(self):
        """
        TC[T2057894902]: Verify "Plug in Your Headset" roadblock appears
        :return:None
        """
        try:
            logging.info("Executing : 'Verify Plug in Your Headset roadblock appears'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._turn_ON_location_services()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.START)
            logging.info("Click on start")
            self.dut.mbs.clickOnText(twilight_app_seletors.START)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.CONTINUE)
            logging.info("Verifying 'Plug in Your Headset' roadblock ")
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.PLUG_IN_HEADSET_TEXT)
            logging.info("'Plug in Your Headset' roadblock appeared")
        finally:
            self._press_back(8)

    def test_Oculus_Select_Hset_Rdblck(self):
        """
        TC[T2057898486]: Verify "Select Headset" roadblock correctly loads
        :return: None
        """
        try:
            logging.info("Executing : 'Verify Select Headset roadblock correctly loads'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._turn_ON_location_services()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            logging.info("Asserting for %s",twilight_app_seletors.SELECT_HEADSET)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.SELECT_HEADSET) is True, "Select headset not found On Screen"

            logging.info("Checking '%s' functionality", twilight_app_seletors.OCULUS_GO)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_GO) is True, "Oculus Go not found"

            logging.info("Click on Oculus Go")
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_GO)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.START_NOW), "Start now not found"
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.WELCOME_TO_OCULUS) is True, "Welcome to Oculus not found"

            logging.info("Click on start now")
            self.dut.mbs.clickOnText(twilight_app_seletors.START_NOW)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.TURN_ON_OCULUS) is True, "Turn on not found"
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.CONTINUE)  is True, "Continue not found"
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.BACK)

            logging.info("Click on back")
            self.dut.mbs.clickOnText(twilight_app_seletors.BACK)
            logging.info("Click on back")
            self.dut.mbs.clickOnText(twilight_app_seletors.BACK)

            logging.info("Checking '%s' functionality", twilight_app_seletors.OCULUS_QUEST)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_QUEST) is True, \
                twilight_app_seletors.OCULUS_QUEST+" Text not found on screen"

            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.START) is True, "Start not found"

            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT) is True, ""

            logging.info("Click on start")
            self.dut.mbs.clickOnText(twilight_app_seletors.START)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.POWER) is True, "Power screen text not found"
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.PLUG_IN_HEADSET_TEXT) is True, "Plug in your headset not found"

            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.CONTINUE) is True, "Continue not found"
            self._press_back(2)

            logging.info("Checking '%s' functionality", twilight_app_seletors.OCULUS_RIFT_S)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_RIFT_S) is True, "Oculus Rift S not found"

            logging.info("Click on Oculus Rift S")
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_RIFT_S)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.EXPLORE_RIFT_STORE) is True, "Explore Rift Store not found"
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_RIFT_S_SETUP) is True, "Oculus Rift S Setup not found"

            logging.info("Click on Explore Rift Store")
            self.dut.mbs.clickOnText(twilight_app_seletors.EXPLORE_RIFT_STORE)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.SETTINGS) is True , "Setting not found"
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.WELCOME_RIFT) is True, "Welcome to Rift not found"
            self._press_back(1)
            logging.info("Click on settings")
            self.dut.mbs.clickOnText(twilight_app_seletors.SETTINGS)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.PAIR_NEW_HEADSET)
            logging.info("click on Pair New Headset")
            self.dut.mbs.clickOnText(twilight_app_seletors.PAIR_NEW_HEADSET)

            logging.info("Checking '%s' functionality", twilight_app_seletors.OCULUS_RIFT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_RIFT) is True, twilight_app_seletors.OCULUS_RIFT+" Text not found on screen"
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_RIFT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.EXPLORE_RIFT_STORE) and self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_RIFT_SETUP) is True, "'"+twilight_app_seletors.EXPLORE_RIFT_STORE+"' and '" + twilight_app_seletors.OCULUS_RIFT_SETUP + "' text not found on screen"
            self.dut.mbs.clickOnText(twilight_app_seletors.EXPLORE_RIFT_STORE)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.SETTINGS) and self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.WELCOME_RIFT) is True, " '"+twilight_app_seletors.WELCOME_RIFT+"' and '"+twilight_app_seletors.SETTINGS+"' text not found"
            self._press_back(1)
            self.dut.mbs.clickOnText(twilight_app_seletors.SETTINGS)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.PAIR_NEW_HEADSET)
            self.dut.mbs.clickOnText(twilight_app_seletors.PAIR_NEW_HEADSET)
        finally:
            self._press_back(8)

    def test_Oculus_Hset_Start_NUX(self):
        """
        TC[T2057900492] : Verify user can select a headset to start the Twilight NUX process for that corresponding HMD unit
        :return:None
        """
        try:
            logging.info("Executing :'Verify user can select a headset to start the Twilight NUX process for that corresponding HMD unit'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._turn_ON_location_services()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.START)
            logging.info("Click on start")
            self.dut.mbs.clickOnText(twilight_app_seletors.START)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.CONTINUE)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.PLUG_IN_HEADSET_TEXT)
            logging.info("Click on continue")
            self.dut.mbs.clickOnText(twilight_app_seletors.CONTINUE)

            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.TURN_HEADSET_TEXT)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.NEXT)
            logging.info("Click on next")
            self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)

            # Assert location pop up
            logging.info("Checking for Next button on popup")
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.NEXT)

            if self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.LOCATION_ACCESS):
                logging.info("Location Access popup found")
                self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)
                assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.LOCATION_PUPUP_ACCESS_GRANT) is True, "Expected text not found"
                logging.info("Checking for popup DENY/ALLOW buttons")
                assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.DENY) is True, "Expected text not found"
                assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.ALLOW) is True, "Expected text not found"
                self.dut.mbs.clickOnText(twilight_app_seletors.ALLOW)
            else:
                logging.info("Location Access popup not found")
                assert False

            logging.info("Assert looking for headset")
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.LOOKING_FOR_HEADSET) is True, "Loogking for headset screen text not found"
            logging.info("Assert pairing code screen")
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.PAIRING_CODE) is True, "Pairing screen not found"
        finally:
            self._press_back(8)

    def test_Oculus_Continue_Next_Rdblk(self):
        """
        TC[T2057894895] : Verify pressing continue button at the headset introduction roadblock proceeds to the next roadblock
        :return:None
        """
        try:
            logging.info("Executing :'Verify pressing continue button at the headset introduction roadblock proceeds to the next roadblock'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._turn_ON_location_services()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.START)
            logging.info("Click on start")
            self.dut.mbs.clickOnText(twilight_app_seletors.START)

            logging.info("Checking for %s ", twilight_app_seletors.CONTINUE)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.CONTINUE) is True, "Continue button not found"
            logging.info("%s found", twilight_app_seletors.CONTINUE)
            logging.info("Checking for %s ", twilight_app_seletors.PLUG_IN_HEADSET_TEXT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.PLUG_IN_HEADSET_TEXT) is True, "Plugin headset text not found on screen"

            logging.info("%s found", twilight_app_seletors.PLUG_IN_HEADSET_TEXT)
            logging.info("Click on continue")
            self.dut.mbs.clickOnText(twilight_app_seletors.CONTINUE)

            logging.info("Verifying roadblock next to continue roadblock")
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.TURN_HEADSET_TEXT) is True, "Turn On Your Headset screen not displayed"
            logging.info("Found %s on screen ", twilight_app_seletors.TURN_HEADSET_TEXT)
        finally:
            self._press_back(8)

    def test_Oculus_Prcd_PlugIn_Hset_Rdblck(self):
        """
        TC[T2057894907] : Verify you can proceed past Plug in your headset roadblock
        :return:None
        """
        try:
            logging.info("Executing :'Verify you can proceed past Plug in your headset roadblock'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._turn_ON_location_services()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.START)
            logging.info("Click on start")
            self.dut.mbs.clickOnText(twilight_app_seletors.START)

            logging.info("Checking for %s ", twilight_app_seletors.CONTINUE)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.CONTINUE) is True, "Continue button not found"
            logging.info("%s found", twilight_app_seletors.CONTINUE)
            logging.info("Checking for %s ", twilight_app_seletors.PLUG_IN_HEADSET_TEXT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.PLUG_IN_HEADSET_TEXT) is True, "Plugin headset text not found on screen"

            logging.info("%s found", twilight_app_seletors.PLUG_IN_HEADSET_TEXT)
            logging.info("Click on continue")
            self.dut.mbs.clickOnText(twilight_app_seletors.CONTINUE)

            logging.info("Verifying roadblock next to continue roadblock")
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.TURN_HEADSET_TEXT) is True, "Turn On Your Headset screen not displayed"
            logging.info("Found %s on screen ", twilight_app_seletors.TURN_HEADSET_TEXT)

            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.NEXT) is True, "Next button not seen on screen"
            logging.info("Found %s on screen ", twilight_app_seletors.NEXT)

            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.PRESS_AND_HOLD_MSG) is True, "Press and hold message not found on screen"
            logging.info("Found %s on screen ", twilight_app_seletors.PRESS_AND_HOLD_MSG)

            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.POWER) is True, "Power text not found on screen"
            logging.info("Found %s on screen ", twilight_app_seletors.POWER)

        finally:
            self._press_back(8)

    def test_Oculus_Headset_Intro_Rdblck(self):
        """
        TC[T2057894889]: Verify headset introduction roadblock appears
        :return: None
        """
        try:
            logging.info("Executing :'Verify headset introduction roadblock appears'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._turn_ON_location_services()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            logging.info("Asserting for '%s'", twilight_app_seletors.OCULUS_GO)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_GO) is True, twilight_app_seletors.OCULUS_GO + "Text not found on screen"

            logging.info("Clicking On '%s'", twilight_app_seletors.OCULUS_GO)
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_GO)

            logging.info("Asserting for '%s'", twilight_app_seletors.START_NOW)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.START_NOW) is True, twilight_app_seletors.START_NOW + "text not found on screen"

            logging.info("Asserting for '%s'", twilight_app_seletors.WELCOME_TO_OCULUS)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.WELCOME_TO_OCULUS) is True, twilight_app_seletors.WELCOME_TO_OCULUS + " text not found on screen"

            logging.info("Clicking on %s", twilight_app_seletors.START_NOW)
            self.dut.mbs.clickOnText(twilight_app_seletors.START_NOW)

            logging.info("Asserting for '%s'", twilight_app_seletors.TURN_ON_OCULUS)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.TURN_ON_OCULUS) is True, twilight_app_seletors.TURN_ON_OCULUS + " not found"

            logging.info("Asserting for '%s'", twilight_app_seletors.CONTINUE)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.CONTINUE) is True, twilight_app_seletors.CONTINUE + " not found"

            logging.info("Asserting for '%s'", twilight_app_seletors.BACK)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.BACK)

            logging.info("Clicking on %s", twilight_app_seletors.BACK)
            self.dut.mbs.clickOnText(twilight_app_seletors.BACK)
            self.dut.mbs.clickOnText(twilight_app_seletors.BACK)

        finally:
            self._press_back(8)

    def test_Oculus_Quest_Pair_Screen(self):
        """
        TC[T2057901424]: Verify Quest pairing screen appears
        :return:None
        """
        try:
            logging.info("Executing :'Verify Quest pairing screen appears'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._turn_ON_location_services()
            self._disable_bluetooth()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            logging.info("Asserting for '%s'", twilight_app_seletors.OCULUS_QUEST)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST) \
                   is True, twilight_app_seletors.OCULUS_QUEST + " Text not found on screen"
            logging.info("Clicking On %s", twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)

            logging.info("Asserting for %s", twilight_app_seletors.START)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.START) is True, twilight_app_seletors.START + "text not found on screen"
            logging.info("Asserting for %s", twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT) is True, twilight_app_seletors.WELCOME_TO_OCULUS_QUEST + "text not found on screen"

            logging.info("Clicking on %s", twilight_app_seletors.START)
            self.dut.mbs.clickOnText(twilight_app_seletors.START)
            logging.info("Asserting for %s", twilight_app_seletors.POWER)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.POWER) is True, twilight_app_seletors.POWER + " text not found"

            logging.info("Asserting for %s", twilight_app_seletors.PLUGIN)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.PLUGIN) \
                   is True, twilight_app_seletors.PLUGIN + " text not found"
            logging.info("Asserting for %s", twilight_app_seletors.CONTINUE)
            assert self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.CONTINUE)

            logging.info("Clicking On %s", twilight_app_seletors.CONTINUE)
            self.dut.mbs.clickOnText(twilight_app_seletors.CONTINUE)

            logging.info("Asserting for %s", twilight_app_seletors.TURN_ON_HEADSET)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.TURN_ON_HEADSET) is True, twilight_app_seletors.TURN_ON_HEADSET + " text not found"

            logging.info("Asserting for %s", twilight_app_seletors.NEXT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.NEXT) is True, twilight_app_seletors.NEXT + " text not found"

            logging.info("Clicking on %s", twilight_app_seletors.NEXT)
            self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)

            logging.info("Asserting for %s", twilight_app_seletors.ENABLE_BLUETOOTH)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.ENABLE_BLUETOOTH) is True, twilight_app_seletors.ENABLE_BLUETOOTH + " text not found"

            self._press_back(1)

            logging.info("Asserting for %s", twilight_app_seletors.PAIRING)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.PAIRING) is True, twilight_app_seletors.PAIRING + " text Not Found"

            logging.info("Asserting for %s", twilight_app_seletors.LOOKING_FOR_HEADSET)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.LOOKING_FOR_HEADSET) is True, twilight_app_seletors.LOOKING_FOR_HEADSET + " text not found"
            logging.info("Pressing back")
        finally:
            self._press_back(6)

    def test_Oculus_Supported_platforms(self):
        """
        TC[T2057900789]: Verify selecting the Device Selector opens up a list of supported Oculus platforms.
        :return: None
        """
        try:
            logging.info("Executing :'Verify selecting the Device Selector opens up a list of supported Oculus platforms.'")
            self._unlock_screen()
            self._clear_app_storage_cache()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            logging.info("Asserting for %s", twilight_app_seletors.SELECT_HEADSET)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.SELECT_HEADSET) is True, twilight_app_seletors.SELECT_HEADSET + "Not Found On Screen"
            logging.info("Pressing Back")
            self._press_back(1)
            logging.info("Asserting for Spinner")
            assert self.dut.mbs.waitUntillDisplayElementWithResID(
                twilight_app_seletors.SPINNER_RESOURCE_ID) is True, "Spinner not found"

            logging.info("Clicking On Spinner")
            self.dut.mbs.waitAndClickUsingResourceId(twilight_app_seletors.SPINNER_RESOURCE_ID)

            logging.info("Asserting for %s", twilight_app_seletors.OCULUS_GO)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_GO) is True, twilight_app_seletors.OCULUS_GO+" not found"
            logging.info("Asserting for %s", twilight_app_seletors.OCULUS_RIFT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_RIFT) is True, twilight_app_seletors.OCULUS_RIFT + " not found"
            logging.info("Asserting for %s", twilight_app_seletors.OCULUS_QUEST)

            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_QUEST) is True, twilight_app_seletors.OCULUS_QUEST + " not found"
        finally:
            self._press_back(2)

    def test_Oculus_TurnOn_Hset_Rdblck(self):
        """
        TC[T2057894896] : Verify "Turn on Your Headset" roadblock appears
        :return:None
        """
        try:
            logging.info("Executing : 'Verify Turn on Your Headset roadblock appears'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            #self._turn_OFF_location_services()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST)
            logging.info("Click on Oculus Quest")
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.START)
            logging.info("Click on start")
            self.dut.mbs.clickOnText(twilight_app_seletors.START)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.CONTINUE)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.PLUG_IN_HEADSET_TEXT)
            logging.info("Click on continue")
            self.dut.mbs.clickOnText(twilight_app_seletors.CONTINUE)

            logging.info("Asserting 'Turn On Your Headset' roadblock screen")
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.TURN_HEADSET_TEXT) is True, "Turn On Your Headset not found"
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.NEXT) is True, "Next button not found"
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.POWER) is True, "Power text on screen not found"
            logging.info("'Turn On Your Headset' roadblock roadblock displayed as expected")
        finally:
            self._press_back(4)
            self.dut.mbs.pressHome()

    def test_Oculus_Bottom_Nav_Buttons(self):
        """
        TC[T2057895084]: Verify selecting the bottom nav buttons lead to each section: Home, Store, Events, Friends, Settings.
        :return: None
        """
        try:
            logging.info("Executing: 'Verify selecting the bottom nav buttons lead to each section: Home, Store, Events, Friends, Settings.'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._turn_ON_location_services()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            logging.info("Asserting for %s", twilight_app_seletors.SELECT_HEADSET)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.SELECT_HEADSET) is True, twilight_app_seletors.SELECT_HEADSET + "Not Found On Screen"
            logging.info("Pressing Back")
            self._press_back(1)

            # Assert for Home tab
            logging.info("Asserting for %s", twilight_app_seletors.HOME)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.HOME) is True, twilight_app_seletors.HOME + " text not found on screen"
            logging.info("Clicking on %s", twilight_app_seletors.HOME)
            self.dut.mbs.clickOnText(twilight_app_seletors.HOME)
            logging.info("Waiting for loading")
            time.sleep(4)
            logging.info("Asserting for %s", twilight_app_seletors.WELCOME_BACK)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.WELCOME_BACK) is True, twilight_app_seletors.WELCOME_BACK + "text not found"
            logging.info("Asserting for %s", twilight_app_seletors.RECOMMENDED)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.RECOMMENDED) is True, twilight_app_seletors.RECOMMENDED + "text not found"
            self.dut.mbs.scrollDown()
            logging.info("Asserting for %s", twilight_app_seletors.TOP_FREE)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.TOP_FREE) is True, twilight_app_seletors.TOP_FREE + "text not found"

            # Assert for Store tab
            logging.info("Asserting for %s", twilight_app_seletors.STORE)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.STORE) is True, twilight_app_seletors.STORE + "text not found"
            logging.info("Clicking on %s", twilight_app_seletors.STORE)
            self.dut.mbs.clickOnText(twilight_app_seletors.STORE)
            logging.info("Waiting for loading")
            time.sleep(4)
            logging.info("Asserting for %s", twilight_app_seletors.SPOTLIGHT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.SPOTLIGHT) is True, twilight_app_seletors.SPOTLIGHT + "text not found"
            logging.info("Asserting for %s", twilight_app_seletors.NEW_AND_UPDATED)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.NEW_AND_UPDATED) is True, twilight_app_seletors.NEW_AND_UPDATED + "text not found"
            logging.info("Asserting for %s", twilight_app_seletors.CATEGORIES)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.CATEGORIES) is True, twilight_app_seletors.CATEGORIES + "text not found"

            # Assert for Events tab
            logging.info("Asserting for %s", twilight_app_seletors.EVENTS)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.EVENTS) is True, twilight_app_seletors.EVENTS + "text not found"
            logging.info("Clicking on %s", twilight_app_seletors.EVENTS)
            self.dut.mbs.clickOnText(twilight_app_seletors.EVENTS)
            logging.info("Waiting for loading")
            time.sleep(4)
            logging.info("Asserting for %s", twilight_app_seletors.UPCOMING_EVENTS)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.UPCOMING_EVENTS) is True, twilight_app_seletors.UPCOMING_EVENTS + "text not found"
            logging.info("Asserting for %s", twilight_app_seletors.MY_EVENTS)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.MY_EVENTS) is True, twilight_app_seletors.MY_EVENTS + "text not found"
            logging.info("Asserting for %s", twilight_app_seletors.FRIENDS)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.FRIENDS) is True, twilight_app_seletors.FRIENDS + "text not found"

            # Assert for Friends tab
            logging.info("Clicking on %s", twilight_app_seletors.FRIENDS)
            self.dut.mbs.clickOnText(twilight_app_seletors.FRIENDS)
            logging.info("Asserting for %s", twilight_app_seletors.ADD_FRIENDS)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.ADD_FRIENDS) is True, twilight_app_seletors.ADD_FRIENDS + "text not found"
            logging.info("Asserting for %s", twilight_app_seletors.SETTINGS)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.SETTINGS) is True, twilight_app_seletors.SETTINGS + "text not found"

            # Assert for Settings tab
            logging.info("Clicking on %s", twilight_app_seletors.SETTINGS)
            self.dut.mbs.clickOnText(twilight_app_seletors.SETTINGS)
            logging.info("Waiting for loading")
            time.sleep(4)
            logging.info("Asserting for %s", twilight_app_seletors.PAIR_NEW_HEADSET)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.PAIR_NEW_HEADSET) is True, twilight_app_seletors.PAIR_NEW_HEADSET + "text not found"
            logging.info("Asserting for %s", twilight_app_seletors.CHANGE_PASSWORD)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.CHANGE_PASSWORD) is True, twilight_app_seletors.CHANGE_PASSWORD + "text not found"
        finally:
            self._press_back(3)


    def test_Oculus_Fresh_Install_Loc_Access(self):
        """
        TC[T2057894913]: Verify when user has a fresh install of Twilight, user is still prompted to allow locations even if location services is turned on.
        :return: None
        """
        try:
            logging.info("Executing :'Verify when user has a fresh install of Twilight, "
                         "user is still prompted to allow locations even if location "
                         "services is turned on.'")
            self._unlock_screen()
            self._turn_ON_location_services()
            self._enable_bluetooth()

            # Uninstall Oculus app.
            oculus_remove_cmd = "adb -s " + config_parser.dev_li[0] \
                                + " uninstall " + twilight_app_seletors.TWILIGHT_APP_PACKAGE

            logging.info(oculus_remove_cmd)

            installed_apps_cmd = "adb -s " + config_parser.dev_li[0] + " shell pm list packages"
            installed_apps = subprocess.check_output(installed_apps_cmd, shell=True)
            logging.info(installed_apps)

            if twilight_app_seletors.TWILIGHT_APP_PACKAGE in installed_apps:
                logging.info("Uninstalling Oculus application from device")
                os.system(oculus_remove_cmd)
                time.sleep(4)

            # Install Oculus app.
            logging.info("Installing Oculus application in device")
            oculus_apk_path = twilight_app_seletors.OCULUS_APK_PATH + \
                              twilight_app_seletors.OCULUS_APK_NAME

            oculus_install_cmd = "adb -s " + config_parser.dev_li[0] +\
                                 " install -r " + oculus_apk_path
            logging.info(oculus_apk_path)
            install_out = subprocess.check_output(oculus_install_cmd, shell=True)
            logging.info(install_out)
            time.sleep(4)
            self._clear_app_storage_cache()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.START)
            logging.info("Click on start")
            self.dut.mbs.clickOnText(twilight_app_seletors.START)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.CONTINUE)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.PLUG_IN_HEADSET_TEXT)
            logging.info("Click on continue")
            self.dut.mbs.clickOnText(twilight_app_seletors.CONTINUE)

            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.TURN_HEADSET_TEXT)
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.NEXT)
            logging.info("Click on next")
            self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)

            # Assert location pop up
            logging.info("Checking for Next button on popup")
            self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.NEXT)

            if self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.LOCATION_ACCESS):
                logging.info("Location Access popup found")
                self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)
                logging.info("Checking for location popup display")
                assert self.dut.mbs.waitUntillDisplayElementWithText(
                    twilight_app_seletors.LOCATION_PUPUP_ACCESS_GRANT) is True, "Expected text not found"
                logging.info("Location popup found")
                logging.info("Checking for DENY/ALLOW buttons on popup")
                assert self.dut.mbs.waitUntillDisplayElementWithText(
                    twilight_app_seletors.DENY) is True, "Expected text not found"
                logging.info("Deny button found")
                assert self.dut.mbs.waitUntillDisplayElementWithText(
                    twilight_app_seletors.ALLOW) is True, "Expected text not found"
                logging.info("Allow button found")
            else:
                logging.info("Location Access popup not found")
                assert False
        finally:
            self._press_back(4)

    def test_Oculus_Past_TurnOn_Hset_Rdblck(self):
        """
        TC[T2057894901]: Verify you can proceed past "Turn On Your Headset" roadblock
        :return: None
        """
        try:
            logging.info("Executing : 'Verify you can proceed past Turn On Your Headset roadblock'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._disable_bluetooth()
            self._turn_ON_location_services()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            logging.info("Asserting for '%s'", twilight_app_seletors.OCULUS_QUEST)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_QUEST) is True, twilight_app_seletors.OCULUS_QUEST + " Text not found on screen"
            logging.info("Clicking On %s", twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)
            logging.info("Asserting for %s", twilight_app_seletors.START)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.START) is True, twilight_app_seletors.START + "text not found on screen"
            logging.info("Asserting for %s", twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT) is True, twilight_app_seletors.WELCOME_TO_OCULUS_QUEST + "text not found on screen"
            logging.info("Clicking on %s", twilight_app_seletors.START)
            self.dut.mbs.clickOnText(twilight_app_seletors.START)
            logging.info("Asserting for %s", twilight_app_seletors.POWER)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.POWER) is True, twilight_app_seletors.POWER + " text not found"

            logging.info("Asserting for %s", twilight_app_seletors.PLUGIN)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.PLUGIN) is True, twilight_app_seletors.PLUGIN + " text not found"
            logging.info("Asserting for %s", twilight_app_seletors.CONTINUE)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.CONTINUE) is True, twilight_app_seletors.CONTINUE + "text not found"
            logging.info("Clicking On %s", twilight_app_seletors.CONTINUE)
            self.dut.mbs.clickOnText(twilight_app_seletors.CONTINUE)

            logging.info("Asserting for %s", twilight_app_seletors.TURN_ON_HEADSET)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.TURN_ON_HEADSET) is True, twilight_app_seletors.TURN_ON_HEADSET + " text not found"
            logging.info("Asserting for %s", twilight_app_seletors.NEXT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.NEXT) is True, twilight_app_seletors.NEXT + " text not found"

            logging.info("Clicking on %s", twilight_app_seletors.NEXT)
            self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)
            logging.info("Asserting for %s", twilight_app_seletors.ENABLE_BLUETOOTH)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.ENABLE_BLUETOOTH) is True, twilight_app_seletors.ENABLE_BLUETOOTH + " text not found"
        finally:
            logging.info("Pressing Back")
            self._press_back(8)

    def test_Oculus_Prcd_Post_Enable_Bluetooth(self):
        """
        TC[T2057894911]: Verify user can proceed past prompt after enabling Bluetooth
        :return: None
        """
        try:
            logging.info("Executing : 'Verify user can proceed past prompt after enabling Bluetooth'")

            self._unlock_screen()
            self._clear_app_storage_cache()
            self._disable_bluetooth()
            self._turn_ON_location_services()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()
            logging.info("Asserting for '%s'", twilight_app_seletors.OCULUS_QUEST)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_QUEST) is True, twilight_app_seletors.OCULUS_QUEST + " Text not found on screen"
            logging.info("Clicking On %s", twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)
            logging.info("Asserting for %s", twilight_app_seletors.START)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.START) is True, twilight_app_seletors.START + "text not found on screen"

            logging.info("Asserting for %s", twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT) is True, twilight_app_seletors.WELCOME_TO_OCULUS_QUEST + "text not found on screen"
            logging.info("Clicking on %s", twilight_app_seletors.START)
            self.dut.mbs.clickOnText(twilight_app_seletors.START)
            logging.info("Asserting for %s", twilight_app_seletors.POWER)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.POWER) is True, twilight_app_seletors.POWER + " text not found"

            logging.info("Asserting for %s", twilight_app_seletors.PLUGIN)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.PLUGIN) is True, twilight_app_seletors.PLUGIN + " text not found"
            logging.info("Asserting for %s", twilight_app_seletors.CONTINUE)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.CONTINUE) is True, twilight_app_seletors.CONTINUE + "text not found"

            logging.info("Clicking On %s", twilight_app_seletors.CONTINUE)
            self.dut.mbs.clickOnText(twilight_app_seletors.CONTINUE)
            logging.info("Asserting for %s", twilight_app_seletors.TURN_ON_HEADSET)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.TURN_ON_HEADSET) is True, twilight_app_seletors.TURN_ON_HEADSET + " text not found"

            logging.info("Asserting for %s", twilight_app_seletors.NEXT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.NEXT) is True, twilight_app_seletors.NEXT + " text not found"
            logging.info("Clicking on %s", twilight_app_seletors.NEXT)
            self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)
            logging.info("Asserting for %s", twilight_app_seletors.ENABLE_BLUETOOTH)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.ENABLE_BLUETOOTH) is True, twilight_app_seletors.ENABLE_BLUETOOTH + " text not found"

            logging.info("Clicking on %s",twilight_app_seletors.ENABLE_BLUETOOTH)
            self.dut.mbs.waitAndClickUsingClass(twilight_app_seletors.BUTTON_CLASS)
            logging.info("Asserting for %s", twilight_app_seletors.NEXT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.NEXT) is True, twilight_app_seletors.NEXT + " text not found"
            logging.info("Clicking on %s",twilight_app_seletors.NEXT)
            self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)

            logging.info("Asserting for %s",twilight_app_seletors.ALLOW)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.ALLOW) is True, twilight_app_seletors.ALLOW + "text not found"
            logging.info("Clicking on %s",twilight_app_seletors.ALLOW)
            self.dut.mbs.clickOnText(twilight_app_seletors.ALLOW)
            logging.info("Asserting for %s", twilight_app_seletors.LOOKING_FOR_HEADSET)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.LOOKING_FOR_HEADSET) is True, twilight_app_seletors.LOOKING_FOR_HEADSET + "text not found"
        finally:
            logging.info("Pressing Back")
            self._press_back(6)

    def test_Oculus_Bluetooth_Prompt(self):
        """
        TC[T2057894908]: Verify enable Bluetooth prompt appears when Bluetooth is disabled on phone
        :return: None
        """
        try:
            logging.info("Executing : 'Verify enable Bluetooth prompt appears when Bluetooth is disabled on phone'")
            self._unlock_screen()
            self._clear_app_storage_cache()
            self._disable_bluetooth()
            self._turn_ON_location_services()

            if self._is_twilight_app_logged_in() is not True:
                logging.info("Logging In to Oculus")
                self._twilight_app_login()

            logging.info("Asserting for '%s'", twilight_app_seletors.OCULUS_QUEST)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_QUEST) is True, twilight_app_seletors.OCULUS_QUEST + " Text not found on screen"
            logging.info("Clicking On %s", twilight_app_seletors.OCULUS_QUEST)
            self.dut.mbs.clickOnText(twilight_app_seletors.OCULUS_QUEST)
            logging.info("Asserting for %s", twilight_app_seletors.START)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.START) is True, twilight_app_seletors.START + "text not found on screen"

            logging.info("Asserting for %s", twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.OCULUS_QUEST_WELCOME_TEXT) is True, twilight_app_seletors.WELCOME_TO_OCULUS_QUEST + "text not found on screen"
            logging.info("Clicking on %s", twilight_app_seletors.START)
            self.dut.mbs.clickOnText(twilight_app_seletors.START)

            logging.info("Asserting for %s", twilight_app_seletors.POWER)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.POWER) is True, twilight_app_seletors.POWER + " text not found"
            logging.info("Asserting for %s", twilight_app_seletors.PLUGIN)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.PLUGIN) is True, twilight_app_seletors.PLUGIN + " text not found"
            logging.info("Asserting for %s", twilight_app_seletors.CONTINUE)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.CONTINUE) is True, twilight_app_seletors.CONTINUE + "text not found"

            logging.info("Clicking On %s", twilight_app_seletors.CONTINUE)
            self.dut.mbs.clickOnText(twilight_app_seletors.CONTINUE)
            logging.info("Asserting for %s", twilight_app_seletors.TURN_ON_HEADSET)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.TURN_ON_HEADSET) is True, twilight_app_seletors.TURN_ON_HEADSET + " text not found"

            logging.info("Asserting for %s", twilight_app_seletors.NEXT)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.NEXT) is True, twilight_app_seletors.NEXT + " text not found"
            logging.info("Clicking on %s", twilight_app_seletors.NEXT)
            self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)

            logging.info("Asserting for %s", twilight_app_seletors.ENABLE_BLUETOOTH)
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                twilight_app_seletors.ENABLE_BLUETOOTH) is True, twilight_app_seletors.ENABLE_BLUETOOTH + " text not found"
        finally:
            logging.info("Pressing Back")
            self._press_back(6)

    def test_fb(self):

        logging.info("Launching FB")
        a = False
        assert a is True, self._captureScreenShot_IfassertFail("a is not found True", "arvind.png")
        print("--------------")
        time.sleep(1000)
        self.dut.mbs.launchApp(twilight_app_seletors.FACEBOOK_APP_LAUNCHER_ACTIVITY)
        logging.info("Launched FB")
        forgot_pwd = self.dut.mbs.waitUntillDisplayElementWithContentDesc("Forgotten password?")
        create_new = self.dut.mbs.waitUntillDisplayElementWithContentDesc("Create New Facebook Account")
        login_btn = self.dut.mbs.waitUntillDisplayElementWithContentDesc("Log In")

        if forgot_pwd is True and create_new is True and login_btn:
            logging.info("Facebook not logged In.")
        else:
            logging.info("Facebook logged In.")
        time.sleep(3)
        self._press_back(3)
        time.sleep(3)

        self.dut.mbs.launchApp(twilight_app_seletors.TWILIGHT_APP_LAUNCHER_ACTIVITY)
        self.dut.mbs.waitUntillDisplayElementWithText("Continue Using Facebook")
        self.dut.mbs.clickOnText("Continue Using Facebook")

    def _captureScreenShot_IfassertFail(self, fail_str, image_name):
        logging.info("Assert failed '%s' , capturing screen-shot %s", fail_str, image_name)
        self._capture_screenshot(image_name)


    def _disable_bluetooth(self):
        self.dut.mbs.executeCommandOnDevice("am start -a " + twilight_app_seletors.BLUETOOTH_DISABLE_ACTIVITY)
        logging.info("Checking for Bluetooth..")
        if self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.ALLOW):
            logging.info("Disabling Bluetooth")
            self.dut.mbs.clickOnText("Allow")
            time.sleep(2)
        else:
            logging.info("Bluetooth already disabled")
        time.sleep(3)

    def _enable_bluetooth(self):
        self.dut.mbs.executeCommandOnDevice("am start -a " + twilight_app_seletors.BLUETOOTH_ENABLE_ACTIVITY)
        logging.info("Checking for Bluetooth..")
        if self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.ALLOW):
            logging.info("Enabling Bluetooth")
            self.dut.mbs.clickOnText("Allow")
            time.sleep(2)
        else:
            logging.info("Bluetooth already enabled")
        time.sleep(3)

    def _clear_app_storage_cache(self):
        """
        To clear storage/cache of Oculus application.
        :return: None
        """
        clear_cache_cmd = "adb -s " + config_parser.dev_li[0] + " shell pm clear " + \
                          twilight_app_seletors.TWILIGHT_APP_PACKAGE
        #logging.info("Clearing storage/cache...")
        os.system(clear_cache_cmd)

    def _is_twilight_app_logged_in(self):
        """
        To check if user logged in on twilight app in device
        :return: True/False
        """

        # Launch twilight app and check for login
        logging.info("Checking if already logged In")
        self.dut.mbs.launchApp(twilight_app_seletors.TWILIGHT_APP_LAUNCHER_ACTIVITY)
        fb_text = self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.FACEBOOK_CONTINUE_TEXT)
        terms_login_screen = self.dut.mbs.assertTextDisplayed(twilight_app_seletors.TERMS_OF_SERVICES)
        privacy_policy_text = self.dut.mbs.assertTextDisplayed(twilight_app_seletors.PRIVACY_POLICY_LOGIN_SCREEN)
        logging.info(fb_text)
        logging.info(terms_login_screen)
        logging.info(privacy_policy_text)
        if fb_text is True and terms_login_screen is True and privacy_policy_text is True:
            logging.info("User not logged in on Oculus")
            return False
        else:
            logging.info("User already logged in on Oculus app")
            return True

    def _twilight_app_login(self):
        """Twilight app login. """

        self.dut.mbs.clickOnText(twilight_app_seletors.SIGN_IN)
        self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.FORGOT_PASSWORD)
        logging.info("Click to enter email")
        self.dut.mbs.clickOnText(twilight_app_seletors.UNAME_SELECTOR_TEXT)
        logging.info("Entering email")
        self.dut.mbs.inputText(twilight_app_seletors.USERNAME)
        logging.info("Pressing Enter")
        self.dut.mbs.inputKeyEvent(66)
        logging.info("Entering Password")
        self.dut.mbs.inputText(twilight_app_seletors.PASSWORD)
        logging.info("Clicking on NEXT")
        self.dut.mbs.clickOnText(twilight_app_seletors.NEXT)
        logging.info("Clicked on NEXT")

        # Assert whether logged in screen found or not
        select_headset = self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.SELECT_HEADSET)
        oculus_go = self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_GO)
        oculus_quest = self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_QUEST)
        oculus_rift_s = self.dut.mbs.waitUntillDisplayElementWithText(twilight_app_seletors.OCULUS_RIFT_S)

        logging.info(select_headset)
        logging.info(oculus_go)
        logging.info(oculus_quest)
        logging.info(oculus_rift_s)

        if select_headset is True and oculus_go is True and oculus_quest is True and \
                oculus_rift_s is True:
            logging.info("Logged in successfully..")
            return True
        else:
            logging.info("Not logged in successfully..")
            return False

    def _is_gps_enabled(self):
        logging.info("Checking if gps location services are enabled or not")
        self.dut.mbs.launchSettings()
        self.dut.mbs.clickOnTextScrollDown(map_selectors.SECURITY_AND_LOCATION)
        self.dut.mbs.clickOnTextScrollDown(map_selectors.LOCATION)
        LOCATION_STATUS = self.dut.mbs.getTextByResourceId(map_selectors.TOGGLE_BUTTON)
        if 'OFF' in LOCATION_STATUS:
            logging.info("Location services are disabled")
            return False
        else:
            logging.info("Location services are enabled")
            return True
        time.sleep(3)
        self._press_back()

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
        self._press_back(3)

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
        self._press_back(3)

    def _verify_text_on_screen(self, image=None, txt=None):

      if image is not None and txt is not None:
        is_image_exist = os.path.isfile(image)
        if is_image_exist:
          os.system("rm " + image)
        self._capture_screenshot(image)

        # Suggestion message text verification
        is_new_image_exist = os.path.isfile(image)

        if is_new_image_exist:
          logging.info("Screen-shot found")
          image = cv2.imread(image)
          gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
          filename = "{}.png".format(os.getpid())
          cv2.imwrite(filename, gray)
          img_text = pytesseract.image_to_string(Image.open(filename))
          os.remove(filename)
          logging.info("Image text found %s : ", img_text)
          if txt in img_text:
            logging.info("Correct text found on screen")
            return True
          else:
            logging.info("Incorrect text found on screen")
            return False
        else:
          logging.info("Screenshot not found")
          return False
      else:
        logging.info("Please give valid input parameters")
        return False

    def _get_screen_text(self, image=None):

      if image is not None:
        is_image_exist = os.path.isfile(image)
        if is_image_exist:
          os.system("rm " + image)
        self._capture_screenshot(image)

        # Suggestion message text verification
        is_new_image_exist = os.path.isfile(image)

        if is_new_image_exist:
          logging.info("Screenshot found")
          image = cv2.imread(image)
          gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
          filename = "{}.png".format(os.getpid())
          cv2.imwrite(filename, gray)
          img_text = pytesseract.image_to_string(Image.open(filename))
          os.remove(filename)
          logging.info("Image text found %s : ", img_text)
          return img_text
        else:
          logging.info("Screenshot not found")
      else:
        logging.info("Please give valid input parameters")

    def _unlock_screen(self):
      self.dut.mbs.inputKeyEvent(224)
      self.dut.mbs.inputKeyEvent(82)

    def _assert_pop_up_text(self, contact_name):
      assert self.dut.mbs.assertTextDisplayed("Delete this contact?") is True, "Expected text not found on 'Delete' popup"
      txt = contact_name + " " + "will be removed from Google Contacts and all your synced devices"
      assert self.dut.mbs.assertTextDisplayed(txt) is True, "Expected text not found on 'Delete' popup"
      assert self.dut.mbs.assertTextDisplayed("Cancel") is True, "Expected text not found on 'Delete' popup"
      assert self.dut.mbs.assertTextDisplayed("Delete") is True, "Expected text not found on 'Delete' popup"

    def _press_input_key(self, key_event=None, count=None):
      if key_event is not None and count is not None:
        for c in range(count):
          self.dut.mbs.inputKeyEvent(key_event)
      else:
        logging.info("Please provide valid key event key and count")

    def _capture_screenshot(self, image_name):
      logging.info("Capturing screenshot : %s", image_name)

      if os.path.exists(gTAF_config.gTAF_home + image_name):
          os.system("rm " + image_name)

      self.dut.mbs.executeCommandOnDevice(" screencap -p /sdcard/" + image_name)
      cmd = "adb -s " + config_parser.dev_li[0] + " pull /sdcard/" + image_name + " ."

      logging.info(cmd)
      os.system(cmd)
      self.dut.mbs.executeCommandOnDevice(" rm /sdcard/" + image_name)

    def _press_back(self, count):
      for c in range(count):
        self.dut.mbs.pressBack()

if __name__ == '__main__':
    test_runner.main()
