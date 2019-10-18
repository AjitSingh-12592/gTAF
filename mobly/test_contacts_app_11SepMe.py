import logging
import os
import random
import time
from collections import OrderedDict
import cv2
import pytesseract
import subprocess
from PIL import Image
from mobly.config_parser import dev_li as device_list
import gTAF_config
import contacts_selectors
from mobly import base_test
from mobly import config_parser
from mobly import test_runner
from mobly.controllers import android_device


class Contacts(base_test.BaseTestClass):

    feedback_selector = ["Contacts", "", "More options", "Help & feedback",
                          "Send feedback", "Write your feedback", "dial"]
    _revoke_contact_permission = ["Advanced", "App permissions", "Contacts", "Gmail"]
    strong_match_contact = [{'First name': 'Tesse', 'Email': 'test-c@hcl.com'},
                             {'First name': 'Tessei', 'Email': 'test-c@hcl.com'},
                             {'First name': 'Test', 'Company': 'Hcl'},
                             {'First name': 'Test', 'Company': 'Hcl'}]

    def setup_class(self):

        global surname
        global phonetic_last_name
        global pop_up_deny
        global pop_up_cancel
        global save_btn
        global android_version
        global uiElement
        global _create_all_contacts
        global contact_details_revoke_permission
        global _search_fav_contact_top
        global _fav_all_contacts_view

        android_version_cmd = "adb -s " + device_list[0] +\
                              " shell getprop ro.build.version.release"
        android_version = subprocess.check_output(android_version_cmd, shell=True)
        android_version = android_version.strip()
        logging.info("android_version : %s", android_version)

        device_model_cmd = "adb  -s " + device_list[0] + " shell getprop ro.product.model"
        device_model = subprocess.check_output(device_model_cmd, shell=True)
        device_model = device_model.strip()
        logging.info("device_model : %s", device_model)
        logging.info("Loading device configuration for %s device[Android version-%s]",
                     device_model, android_version)
        gTAF_config.load_device_config(dev_model=device_model,
                                       android_version=android_version)
        uiElement = gTAF_config.uiElement
        surname = uiElement['DEVICE_DETAIL']
        surname = uiElement['CONTACT_SURNAME_TEXT']
        phonetic_last_name = uiElement['PHONETIC_LAST_NAME']
        pop_up_deny = uiElement['POP_UP_DENY']
        pop_up_cancel = uiElement['POP_UP_CANCEL']
        save_btn = uiElement['SAVE_BTN']

        _create_all_contacts = OrderedDict([("Name prefix", "test"), ("First name", "testx"),
                                            ("Middle name", "testy"), (surname, "test1"), ("Name suffix", "test2"),
                                            (phonetic_last_name, "test3"), ("Phonetic middle name", "test4"),
                                            ("Phonetic first name", "test5"), ("Nickname", "test6"),
                                            ("File as", "test7"),
                                            ("Company", "HCL"), ("Title", "Service"), ("Phone", "1234567891"),
                                            ("Email", "testmail@gmail.com"),
                                            ("Website", "www.hcl.com"), ("Relationship", "test8"), ("SIP", "158998"),
                                            ("Custom field", "test9"), ("Custom label", "test10")])

        contact_details_revoke_permission = OrderedDict(
            [("First name", "Tesla"), (surname, "Jordan"), ("Email", "testmail-s@hcl.com")])

        _search_fav_contact_top = [
            {'First name': 'Test', surname: 'Case', 'Phone': '9998989', 'Email': 'test-c@hcl.com',
             'Address': 'Noida'},
            {'First name': 'Tesian', surname: 'Salvatore', 'Phone': '9992929',
             'Email': 'tesian-s@hcl.com',
             'Address': 'Delhi'},
            {'First name': 'Tesla', surname: 'Jordan', 'Phone': '9993939',
             'Email': 'tesla-j@hcl.com',
             'Address': 'Mumbai'},
            {'First name': 'Teshmie', surname: 'Mathews', 'Phone': '9994949',
             'Email': 'teshmie-m@hcl.com',
             'Address': 'Banglore'},
            {'First name': 'Tessa', surname: 'Cruise', 'Phone': '9995959',
             'Email': 'tessa-c@hcl.com',
             'Address': 'Chennai'},
            {'First name': 'Tessie', surname: 'William', 'Phone': '9996969',
             'Email': 'tessie-w@hcl.com',
             'Address': 'Gurgaon'},
            {'First name': 'Tesca', surname: 'Lockwood', 'Phone': '9997979',
             'Email': 'tesca-l@hcl.com',
             'Address': 'Chandigarh'},
            {'First name': 'Tesni', surname: 'Shied', 'Phone': '9991919', 'Email': 'tesni-s@hcl.com',
             'Address': 'Faridabad'}]

        _fav_all_contacts_view = [{'First name': 'Test', surname: 'Case', 'Company': 'HCL'},
                                  {'First name': 'Test', surname: 'Case', 'Company': 'HCL'}]

        self.ads = self.register_controller(android_device)
        self.dut = self.ads[0]
        logging.info("List of device found in test bed : %s", config_parser.dev_li)
        self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.example4')
        logging.info("Launching contact app on device with device id :%s ", device_list[0])

    def test_create_contact_name(self):
        """
        TC_CONTACT_001: Create contact, test name field filling
        :return: None
        """
        try:
            image_name = 'contacts.png'
            contact_details = OrderedDict([("First name", "Tesian"), (surname, "Salvatore")])
            expected_toast_text = contact_details["First name"] + ' ' +\
                                  contact_details[surname] + ' ' + "saved"
            logging.info("Expected toast message text : '%s'", expected_toast_text)

            self.unlock_screen()
            self.dut.mbs.pressHome()
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            no_contacts = self.dut.mbs.assertTextDisplayed("No contacts yet")
            if no_contacts is False:
                logging.info("Deleting existing contacts")
                self.delete_all_contacts()
            logging.info("Creating new contact ")
            self.dut.mbs.waitAndClickUsingResourceId(contacts_selectors.FLOATING_ACTION_BUTTON)
            for key in contact_details:
                logging.info("Adding detail for : %s", key)
                self.dut.mbs.clickOnText(key)
                logging.info("Input text : %s", contact_details[key])
                self.dut.mbs.inputText(contact_details[key])
                self.dut.mbs.pressBack()
                time.sleep(1)
            logging.info("Click on Save button")
            self.dut.mbs.clickOnText("Save")
            self.press_back(2)
            time.sleep(.5)

            logging.info("Verifying toast message on screen")
            # Verifying toast message
            toast_result = self.verify_text_on_screen(image=image_name, txt=expected_toast_text)
            assert toast_result is True, "Incorrect toast message found"
        finally:
            self.press_back(4)

    def test_create_contact_all_fields(self):
        """
        TC_CONTACT_002: Create new contact with ALL fields filled in
        :return: None
        """
        try:

            name = _create_all_contacts["Name prefix"] + ' ' + \
                   _create_all_contacts["First name"] + ' ' + \
                   _create_all_contacts[
                       "Middle name"] + ' ' + _create_all_contacts[surname] + ', ' + \
                   _create_all_contacts["Name suffix"]

            logging.info(name)
            phonetic = _create_all_contacts[phonetic_last_name] + ' ' + _create_all_contacts[
                "Phonetic middle name"] + ' ' + _create_all_contacts["Phonetic first name"]
            mobile = _create_all_contacts["Phone"]
            sip = _create_all_contacts["SIP"]
            email = _create_all_contacts["Email"]
            nickname = _create_all_contacts["Nickname"]
            file_as = _create_all_contacts["File as"]
            website = _create_all_contacts["Website"]
            compony_title = _create_all_contacts["Title"] + ', ' + _create_all_contacts["Company"]
            relationship = _create_all_contacts["Relationship"]
            custom_field = _create_all_contacts["Custom field"]
            custom_label = _create_all_contacts["Custom label"]

            self.unlock_screen()
            self.press_back(3)
            self.dut.mbs.pressHome()
            logging.info("Launching contacts")
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()

            logging.info("Asserting for any existing contacts")
            no_contacts = self.dut.mbs.assertTextDisplayed("No contacts yet")
            if no_contacts is False:
                logging.info("Deleting existing contacts")
                self.delete_all_contacts()
            logging.info("Creating new contact ")
            self.dut.mbs.waitAndClickUsingResourceId(contacts_selectors.FLOATING_ACTION_BUTTON)
            logging.info("Click on More fields")
            self.dut.mbs.clickOnText("More fields")
            self.set_contact_photo()

            self.dut.mbs.waitAndClickUsingContentDesc("Show more name fields")

            for key in _create_all_contacts:
                logging.info("Adding detail %s for : %s", _create_all_contacts[key], key)
                self.dut.mbs.scrollClickOnText(key)
                logging.info("Entering text : %s", _create_all_contacts[key])
                self.dut.mbs.inputText(_create_all_contacts[key])
                self.dut.mbs.pressBack()
                time.sleep(1)
                if key == 'SIP':
                    logging.info("Click on Add custom field")
                    self.dut.mbs.clickOnText("Add custom field")

            # self.create_contact_label()
            logging.info("Save contact")
            self.dut.mbs.clickOnText("Save")
            time.sleep(1)
            self.dut.mbs.pressBack()
            time.sleep(1)
            logging.info(name)
            assert self.dut.mbs.assertTextDisplayed(name), "Contact not found"
            logging.info("Click on name")
            self.dut.mbs.clickOnText(name)

            _contact_img = self.dut.mbs.isDisplayed(contacts_selectors.CONTACT_IMAGE_ICON_RES_ID)
            _name = self.dut.mbs.getTextContactFrame(0, 1, 0)
            _phonetic = self.dut.mbs.getTextContactFrame(0, 1, 1)
            _mobile = self.dut.mbs.getTextContactRFrame(0, 0, 0)
            _sip = self.dut.mbs.getTextContactRFrame(0, 2, 0)

            self.dut.mbs.scrollDown()

            _email = self.dut.mbs.getTextContactRFrame(0, 4, 0)
            _nickname = self.dut.mbs.getTextContactRFrame(1, 0, 0)
            _phonetic_name = self.dut.mbs.getTextContactRFrame(1, 2, 0)
            _file_as = self.dut.mbs.getTextContactRFrame(1, 4, 0)
            _website = self.dut.mbs.getTextContactRFrame(1, 6, 0)

            self.dut.mbs.scrollDown()

            _compony_title = self.dut.mbs.getTextContactRFrame(1, 8, 0)
            _relationship = self.dut.mbs.getTextContactRFrame(1, 10, 0)
            _custom_field = self.dut.mbs.getTextContactRFrame(1, 12, 0)
            _custom_label = self.dut.mbs.getTextContactRFrame(1, 12, 1)

            logging.info("Verifying created contact details")

            assert _contact_img is True, "Contact image not found"
            assert _name[0] == name, "Incorrect name found"
            assert _phonetic[0] == phonetic, "Incorrect phonetic name found"
            for digit in mobile:
                assert digit in _mobile[0], "Incorrect mobile number found"
            assert _sip[0] == sip, "Incorrect SIP number found"
            assert _email[0] == email, "Incorrect email found"
            assert _nickname[0] == nickname, "Incorrect nickname found"
            assert _phonetic_name[0] == phonetic, "Incorrect phonetic nick name found"
            assert _file_as[0] == file_as, "Incorrect file as name found"
            assert _website[0] == website, "Incorrect website name found"

            logging.info(_compony_title[0])
            logging.info(compony_title)

            assert _compony_title[0] == compony_title, "Incorrect company title found"
            assert _relationship[0] == relationship, "Incorrect relationship value found"
            assert _custom_field[0] == custom_field, "Incorrect custom_field value found"
            assert _custom_label[0] == custom_label, "Incorrect custom_label value found"
        finally:
            self.press_back(4)

    def test_remove_favorite_contact(self):
        """
        TC_CONTACT_013: Remove a contact from Favorites
        :return:None
        """
        self.unlock_screen()
        self.dut.mbs.pressHome()
        self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
        self.allow_contact_permission()
        self.skip_sign_in()
        self.account_sync_msg_check()
        no_contacts = self.dut.mbs.assertTextDisplayed("No contacts yet")
        if no_contacts is False:
            logging.info("Deleting existing contacts")
            self.delete_all_contacts()
        logging.info("Creating new contact ")
        self.dut.mbs.waitAndClickUsingResourceId(contacts_selectors.FLOATING_ACTION_BUTTON)
        self.dut.mbs.clickOnText("First name")
        self.dut.mbs.inputText("Test")
        self.dut.mbs.clickOnText(surname)
        self.dut.mbs.inputText("name")
        self.dut.mbs.clickOnText("Save")
        time.sleep(1)
        logging.info("Adding created contact to favourites list")
        self.dut.mbs.waitAndClickUsingContentDesc(uiElement['ADD_TO_FAV'])
        self.dut.mbs.pressBack()

        fav_content_desc = self.dut.mbs.getFavContactDesc()
        fav_content_desc = fav_content_desc.encode("ascii")
        logging.info("Fetched content desc %s ", fav_content_desc)
        assert uiElement['FAV'] in fav_content_desc, 'Favourites contact not found'
        self.dut.mbs.clickOnText("Test name")
        logging.info("Removing created contact from favourites list")

        self.dut.mbs.waitAndClickUsingContentDesc("Remove from favorites")
        self.dut.mbs.pressBack()
        logging.info("Verifying if favourites contact found..")
        fav_content_desc = self.dut.mbs.getFavContactDesc()
        assert fav_content_desc is None, 'Favourites contact not found, removed from list'
        created_contact = self.dut.mbs.assertTextDisplayed("Test name")
        assert created_contact is True, 'Created contact does not found in default contact view'
        self.dut.mbs.pressBack()

    def test_contact_permission_revoke_from_gmail(self):
        """
        TC_CONTACT_007: Test Contacts permission revoke from Gmail
        :return: None
        """
        try:
            expected_toast_text = "Allow contacts suggestions"
            image_name = "contact_suggestion.png"
            _compose = "Compose"
            _to = "To"
            input_name = contact_details_revoke_permission["First name"]

            logging.info("Current android version : %s", android_version)
            self.unlock_screen()
            self.dut.mbs.pressHome()
            self.create_contact_revoke_permissions(contact_details_revoke_permission)

            logging.info("Current android version : %s", android_version)
            self.disable_contact_permission_for_gmail()
            time.sleep(2)
            self.dut.mbs.launchGmail()
            time.sleep(2)
            self.get_screen_text(image='gmail_revoke.png')
            self.dut.mbs.waitAndClickUsingContentDesc(_compose)
            self.dut.mbs.clickOnText(_to)
            self.dut.mbs.inputText(input_name)
            time.sleep(2)
            self.press_input_key(key_event=67, count=len(input_name))
            self.dut.mbs.inputText(input_name)
            time.sleep(2)
            # Verifying toast message
            toast_result = self.verify_text_on_screen(image=image_name, txt=expected_toast_text)
            assert toast_result is True, "Incorrect toast message found"

            # To filed text verification
            to_field_text = self.dut.mbs.getTextByResourceId(contacts_selectors.CONTACT_TO_RES_ID)
            to_field_text = to_field_text.encode("ascii")
            logging.info("To filed text : %s ", to_field_text)
            assert to_field_text.decode("utf-8") == input_name, "Invalid text found in To field"

        finally:
            self.press_input_key(key_event=67, count=len(input_name))
            self.press_back(5)
            logging.info("Enable Gmail permission for contacts")
            self.enable_contact_permission_for_gmail()

    def test_delete_contact(self):
        """
        TC_CONTACT_015: Delete contact test
        :return: None
        """
        try:
            contact_name = contact_details_revoke_permission["First name"] + " " + \
                           contact_details_revoke_permission[surname]
            expected_toast_text = contact_name + " deleted"
            image_name = "delete_contact.png"
            logging.info("Delete contact toast message to be verify : '%s' ", expected_toast_text)

            self.unlock_screen()
            self.dut.mbs.pressHome()
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            no_contacts = self.dut.mbs.assertTextDisplayed("No contacts yet")
            if no_contacts is False:
                logging.info("Deleting existing contacts")
                self.delete_all_contacts()
            logging.info("Creating new contact ")
            self.create_contact_revoke_permissions(contact_details_revoke_permission)
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            self.delete_contact(contact_name)

            # Verifying toast message
            toast_result = self.verify_text_on_screen(image=image_name, txt=expected_toast_text)
            assert toast_result is True, "Incorrect toast message found"
        finally:
            self.press_back(4)

    def test_contact_permission_grant_from_gmail(self):
        """
        TC_CONTACT_008: Test contact name auto complete in Gmail after granting Contacts permission
        :return: None
        """
        try:
            expected_toast_text = contact_details_revoke_permission["First name"] + " " \
                                  + contact_details_revoke_permission[surname]
            image_name = "contact_suggestion_grant.png"
            _compose = "Compose"
            _to = "To"
            input_name = contact_details_revoke_permission["First name"]

            self.unlock_screen()
            self.dut.mbs.pressHome()
            self.create_contact_revoke_permissions(contact_details_revoke_permission)

            self.enable_contact_permission_for_gmail()
            time.sleep(2)
            self.dut.mbs.launchGmail()
            time.sleep(2)
            self.get_screen_text(image='gmail_grant.png')
            assert self.dut.mbs.waitUntillDisplayElementWithContentDesc(_compose) is True, "Compose not found"
            self.dut.mbs.waitAndClickUsingContentDesc(_compose)
            assert self.dut.mbs.waitUntillDisplayElementWithText(_to) is True, "To not found"
            self.dut.mbs.clickOnText(_to)
            self.dut.mbs.inputText(input_name)
            logging.info("Expected toast message %s", expected_toast_text)
            time.sleep(2)

            # Verifying toast message
            logging.info("Expected toast message : %s ", expected_toast_text)
            toast_result = self.verify_text_on_screen(image=image_name, txt=expected_toast_text)
            assert toast_result is True, "Incorrect toast message found"
        finally:
            self.press_input_key(key_event=67, count=len(input_name))
            self.press_back(5)

    def test_strong_match_for_duplicates(self):
        """
        TC_CONTACT_003: Strong match duplicates
        :return: None
        """
        try:
            _merge_duplicate_msg = '2 people with duplicate listings'
            logging.info("Executing TC_CONTACT_003: Strong match duplicates")

            self.unlock_screen()
            self.dut.mbs.pressHome()

            # To launch contacts app and delete all existing contacts
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            if self.dut.mbs.assertTextNotDisplayed("No contacts yet"):
                self.delete_all_contacts()
            logging.info("Creating Contacts")
            self.create_strong_match_contacts(_contact=self.strong_match_contact)

            self.clear_cache()

            count = 0

            # To launch contacts app
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            time.sleep(3)

            while self.dut.mbs.assertTextDisplayed('Getting contacts'):
                logging.info("Getting Contacts progress bar found, waiting to disappear..")
                time.sleep(0.5)
                count = count + 1
                if count > 150:
                    logging.info("Getting contacts sync message not dismissed")
                    break
                continue
            self.dut.mbs.waitAndClickUsingContentDesc('Open navigation drawer')
            logging.info("Click on Suggestions")
            self.dut.mbs.clickOnText('Suggestions')
            logging.info("Refreshing suggestion screen")
            time.sleep(2)
            self.dut.mbs.refresh()
            time.sleep(4)
            assert self.dut.mbs.assertTextDisplayed(_merge_duplicate_msg), "Merge duplicates pop up not found"
            self.dut.mbs.clickOnText('Merge duplicates')
            self.dut.mbs.waitUntillDisplayElementWithText("Merge all")
            self.dut.mbs.clickOnText("Merge all")
            assert self.dut.mbs.waitUntillDisplayElementWithText(
                "Merge 2 duplicates?") is True, "Merge all pop up not found"
        finally:
            self.press_back(5)

    def test_suggestion_welcome_card(self):
        """
        TC_CONTACT_004: Suggestions > Welcome Card verification
        :return: None
        """
        try:
            _suggestion_welcome_header = "Welcome to your suggestions"
            _got_it_text = "Got it"
            _apps_notification = "Apps & notifications"

            self.unlock_screen()
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            self.press_back(3)
            self.dut.mbs.pressHome()

            self.clear_cache()

            logging.info("Launching contacts")
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            logging.info("Open navigation drawer")
            self.dut.mbs.waitUntillDisplayElementWithContentDesc(contacts_selectors.NAVIGATION_DRAWER)
            self.dut.mbs.waitAndClickUsingContentDesc(contacts_selectors.NAVIGATION_DRAWER)

            logging.info("Click on Suggestions")
            assert self.dut.mbs.waitUntillDisplayElementWithText("Suggestions") is True, "Suggestions not displayed"
            self.dut.mbs.clickOnText("Suggestions")

            logging.info("Refreshing suggestion screen")
            time.sleep(2)
            self.dut.mbs.refresh()
            time.sleep(2)

            logging.info("Verifying suggestion welcome screen messages")
            self.dut.mbs.waitUntillDisplayElementWithText(_suggestion_welcome_header)
            self.dut.mbs.assertTextDisplayed(_suggestion_welcome_header)
            self.dut.mbs.assertTextDisplayed(_got_it_text)
            _header = self.dut.mbs.getTextByResourceId(contacts_selectors.SUGGESTIONS_WELCOME_HEADER)
            _got_it = self.dut.mbs.getTextByResourceId(contacts_selectors.SUGGESTIONS_WELCOME_GOT_IT)

            logging.info(_header)
            logging.info(_got_it)
            _header = _header.encode("utf-8")
            _got_it = _got_it.encode("utf-8")

            self.dut.mbs.clickOnText(_got_it_text)
            time.sleep(2)
            assert self.dut.mbs.assertTextNotDisplayed(
                _suggestion_welcome_header) is True, "Welcome suggestions popup not dismissed"
            assert self.dut.mbs.assertTextNotDisplayed(_got_it_text) is True, "Got it not dismissed"

            assert _header == _suggestion_welcome_header, " 'Welcome to your suggestions' not found"
            assert _got_it == _got_it_text, " 'Got it' text not found"
        finally:
            self.press_back(4)

    def test_merge_duplicates(self):
        """
        TC_CONTACT_005 :Suggestions  Merge Duplicates
        :return: None
        """
        try:
            _contact = [{'First name': 'Test', surname: 'Case', 'Company': 'HCL'},
                        {'First name': 'Test', surname: 'Case', 'Company': 'HCL'}]
            _duplicates = [_contact[0]['First name'] + " " + _contact[0][surname],
                           _contact[1]['First name'] + " " + _contact[1][surname]]

            merge_verify_image = "merge_verification.png"
            merge_text = "Contacts merged"
            suggestion_text = "Welcome to your suggestions"

            self.unlock_screen()
            self.press_back(4)
            self.dut.mbs.pressHome()

            # To launch contacts app
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            # Delete previous contacts if exists
            if self.dut.mbs.assertTextNotDisplayed("No contacts yet"):
                self.delete_all_contacts()

            # Create new contacts
            self.create_duplicate_contacts(_contacts=_contact)
            self.clear_cache()

            # To launch contacts app
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            logging.info('Getting contacts')
            while (self.dut.mbs.assertTextDisplayed('Getting contacts')):
                logging.info("Getting Contacts progress bar found, waiting to disappear..")
                time.sleep(0.5)
                continue
            self.dut.mbs.waitAndClickUsingContentDesc('Open navigation drawer')
            self.dut.mbs.clickOnText('Suggestions')

            logging.info("Refreshing suggestion screen")
            time.sleep(2)
            self.dut.mbs.refresh()
            time.sleep(4)

            assert self.dut.mbs.waitUntillDisplayElementWithText(
                'Merge duplicates') is True, "Merge duplicates not found"
            self.dut.mbs.clickOnText('Merge duplicates')

            logging.info("assert '%s' ", _duplicates[0])
            time.sleep(5)
            # Verification 2: On clicking "Merge duplicates" duplicates are shown.
            assert self.dut.mbs.assertTextDisplayed(_duplicates[0]) is True, "Duplicates are not shown."
            logging.info("asserted")
            logging.info("assert '%s' ", _duplicates[1])
            assert self.dut.mbs.assertTextDisplayed(_duplicates[1]) is True, "Duplicates are not shown."

            self.dut.mbs.clickOnText("Merge")
            time.sleep(2)

            # Verification 3: The duplicates were merged.
            assert self.verify_text_on_screen(image=merge_verify_image,
                                               txt=merge_text) is True, "Duplicates didn't merge."

            # Verification 4: On clicking back arrow, verify that Suggestions view loads.
            self.dut.mbs.pressBack()
            time.sleep(1)
            assert self.dut.mbs.assertTextDisplayed(
                suggestion_text) is True, "Suggestions view loads verification failed."

        finally:
            self.press_back(5)

    def test_create_label(self):
        """
        TC_CONTACT_006: Create new Label for single account
        :return: None
        """
        try:
            expected_toast_message = "Label created"
            label_name = "test_label"
            image_name = "label_toast.png"
            gmail_account_image = "google_account_count.png"
            self.unlock_screen()
            self.press_back(4)
            self.dut.mbs.pressHome()
            self.dut.mbs.launchGmail()
            self.dut.mbs.waitAndClickUsingContentDesc(contacts_selectors.NAVIGATION_DRAWER)
            time.sleep(2)
            self.dut.mbs.scrollDown()
            time.sleep(2)
            self.dut.mbs.clickOnText("Settings")
            time.sleep(2)
            logging.info("Capturing screenshot to check the configured google account in devices")
            gmail_account_text = self.get_screen_text(image=gmail_account_image)
            gmail_account_text = gmail_account_text.encode("utf-8")
            gmail_account_text = gmail_account_text.replace("\n", " ")

            if gmail_account_text.count("@gmail.com") == 1:
                logging.info("Only one google account configured currently in device")
                self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
                self.allow_contact_permission()
                self.skip_sign_in()
                self.account_sync_msg_check()
                self.dut.mbs.waitAndClickUsingContentDesc("Open navigation drawer")
                self.dut.mbs.clickOnText("Create label")
                self.dut.mbs.clickOnText("Label name")
                self.dut.mbs.inputText(label_name)
                self.dut.mbs.clickOnText("OK")
                time.sleep(1)
                # Verifying label name
                label_displayed = self.dut.mbs.assertTextDisplayed(label_name)
                assert label_displayed is True, "Created label name not displayed on device screen"

                # Verifying toast message
                toast_result = self.verify_text_on_screen(image=image_name, txt=expected_toast_message)
                assert toast_result is True, "Incorrect create label toast text found"
            else:
                logging.info("More then one google account configured currently in device")
        finally:
            logging.info("Deleting created label")
            self.dut.mbs.waitAndClickUsingContentDesc("More options")
            self.dut.mbs.clickOnText("Delete label")
            self.press_back(3)

    def test_contact_help_feedback(self):
        """
        TC_CONTACT_014 To test help & feedback
        :return: None
        """
        try:
            # list of data to be verified
            verification_data = ["Browse all articles", "Contact us", "Send feedback"]
            image_name = "feedback_image.png"
            flag = False
            contact_name = contact_details_revoke_permission["First name"] + " " + \
                           contact_details_revoke_permission[surname]

            self.unlock_screen()
            self.dut.mbs.pressHome()
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            no_contacts = self.dut.mbs.assertTextDisplayed("No contacts yet")
            if no_contacts is False:
                logging.info("Deleting existing contacts")
                self.delete_all_contacts()
            logging.info("Creating new contact ")
            self.create_contact_revoke_permissions(contact_details_revoke_permission)

            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)

            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            self.dut.mbs.clickOnText(contact_name)

            # Click on the Overflow Menu
            self.dut.mbs.waitAndClickUsingContentDesc(self.feedback_selector[2])

            # Click on Help & Feedback option
            self.dut.mbs.clickOnText(self.feedback_selector[3])
            time.sleep(3)

            self.dut.mbs.waitUntillDisplayElementWithText("Popular articles")
            # Get available popular articles list
            popular_articles = self.get_help_feedback_popular_articles(self.get_screen_text(image=image_name))

            logging.info("Popular articles are %s ", popular_articles)
            print(len(popular_articles))
            # Check whether the  device is online or not
            if self.dut.mbs.isOnline():
                logging.info("Internet is up in device")
                for article in range(0, len(popular_articles)):
                    logging.info("Clicking on  '%s'", popular_articles[article])
                    self.dut.mbs.clickOnText(popular_articles[article])
                    time.sleep(2)

                    # Verify text not expected text on respective article's screen
                    for assert_text in range(0, len(verification_data)):
                        assert self.dut.mbs.assertTextDisplayed(
                            verification_data[assert_text]) is False, "Expected text not found"
                    self.press_back(1)

                # Verify feedback sent option
                self.dut.mbs.clickOnText(self.feedback_selector[4])
                time.sleep(1)
                self.dut.mbs.clickUsingResourceId("com.google.android.gms:id/gf_issue_description")
                self.dut.mbs.inputText("Good")
                self.dut.mbs.waitAndClickUsingContentDesc("Send")
                time.sleep(2)
                for i in range(1, 40):
                    if self.verify_text_on_screen(
                            image=image_name, txt="Thank you for the feedback"):
                        flag = True
                        break
                    else:
                        logging.info(self.feedback_selector[5] + " Edit text not found")
                logging.info("flag is: %s ", flag)
                assert flag is True, "Feedback confirmation could not get successfully"
            else:
                logging.info("flag is:: %s ", flag)
                logging.info("Test Failed, Device is Offline")
                assert False

        finally:
            self.press_back(4)
            self.dut.mbs.pressHome()

    def test_google_play_service_permission_revoke(self):
        """
        TC_CONTACT_009: To revoke the Google play service and check the sync with google account, app should not crash
        :return: None
        """
        try:
            _case_select = ["Open navigation drawer", "Settings", "Accounts", "Google", "Account sync", "Contacts",
                            "Sync failed"]
            _pop_up_deny = pop_up_deny
            _pop_up_cancel = pop_up_cancel
            _image_name = "app_notification.png"

            self.unlock_screen()
            self.dut.mbs.pressHome()
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            self.revoke_google_play_services()

            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()

            assert self.dut.mbs.waitUntillDisplayElementWithContentDesc(_case_select[0]) is True, \
                "Navigation drawer not displayed"

            self.dut.mbs.waitAndClickUsingContentDesc(_case_select[0])  # TO open NAVIGATION DRAWER
            self.dut.mbs.clickOnText(_case_select[1])  # To click on  SETTINGS
            time.sleep(1)
            self.dut.mbs.clickOnText(_case_select[2])  # To click on ACCOUNTS
            time.sleep(2)
            if self.dut.mbs.assertTextDisplayed(_case_select[3]):
                self.dut.mbs.clickOnText(_case_select[3])
            else:
                logging.info("Test Failed, Add Google Account")
                assert False

            time.sleep(1)
            logging.info("Verifying if any crash is there")
            assert self.dut.mbs.uiWatcherTextContains("isn't responding") is False, "Crash found"
            logging.info("No crash observed")
            self.dut.mbs.clickOnText(_case_select[4])  # To click on ACCOUNT SYNC

            for index in range(5):
                logging.info("Toggling Contact's sync")
                self.dut.mbs.clickOnText(_case_select[5])  # To click on CONTACTS
                time.sleep(2)
                logging.info("Verifying if any crash is there")
                assert self.dut.mbs.uiWatcherTextContains("isn't responding") is False, "Crash found"
                logging.info("No crash observed")

            # Enable Contact sync
            if self.dut.mbs.isContentThere(_case_select[6]):
                logging.info("Contact's sync is ON")
            else:
                logging.info("Enabling Contact's sync")
                self.dut.mbs.clickOnText(_case_select[5])
                time.sleep(1)
            self.press_back(5)

        finally:
            logging.info("Enabling Google play services")
            self.enable_google_play_services()

    def test_search_favourite_on_top(self):
        """
        TC_CONTACT_010 Favorite search results on top test
        :return: None
        """
        try:

            # List of all the names of favourite contacts from _contact
            _fav = [_search_fav_contact_top[3]['First name'] + " " + _search_fav_contact_top[3][surname],
                    _search_fav_contact_top[1]['First name'] + " " + _search_fav_contact_top[1][surname],
                    _search_fav_contact_top[7]['First name'] + " " + _search_fav_contact_top[7][surname],
                    _search_fav_contact_top[5]['First name'] + " " + _search_fav_contact_top[5][surname]]

            self.unlock_screen()
            self.dut.mbs.pressHome()
            logging.info("favourates contacts : %s ", _fav)
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            # Delete previous contacts if exists
            if self.dut.mbs.assertTextNotDisplayed("No contacts yet"):
                logging.info("Delete all contacts")
                self.delete_all_contacts()
            self.create_multiple_contacts(_contact=_search_fav_contact_top)

            # To search the contact and retrieve the search result into a list

            self.dut.mbs.waitUntillDisplayElementWithResID(contacts_selectors.CONTACT_SEARCH_BAR_RES_ID)

            self.dut.mbs.clickUsingResourceId(contacts_selectors.CONTACT_SEARCH_BAR_RES_ID)
            time.sleep(1)
            self.dut.mbs.clickUsingResourceId(contacts_selectors.CONTACT_SEARCH_BAR_RES_ID)
            time.sleep(1)
            self.dut.mbs.inputText("Tes")
            time.sleep(1)
            self.dut.mbs.pressBack()
            _item_list = self.dut.mbs.getAllItemsOfListView(7)
            logging.info("Fetched contacts after create contact : %s ", _item_list)

            # Verifying that all the favourites are at the top of the search result
            for i in range(0, 4):
                logging.info("Searching '%s' in fav contact list", _item_list[i])
                if str(_item_list[i]).encode("ascii") in _fav:
                    logging.info("'%s' found in fav contacts list", _item_list[i])
                    assert True
                else:
                    logging.info("'%s' not found in fav contacts list", _item_list[i])
                    assert False
        finally:
            self.press_back(3)
            self.dut.mbs.pressHome()

    def test_favourite_in_all_contact(self):
        """
        TC_CONTACT_012: Test favorites in 'All Contacts' view
        :return: None
        """
        try:
            _dict_keys = ['First name', surname, 'Company']
            _selector = ["Create contact", "Save", uiElement['ADD_TO_FAV'], "1 selected"]
            _fav = _fav_all_contacts_view[1]['First name'] + " " + _fav_all_contacts_view[1][surname]

            self.unlock_screen()

            # To launch contacts app and delete all existing contacts
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            # Delete previous contacts if exists
            if self.dut.mbs.assertTextNotDisplayed("No contacts yet"):
                self.delete_all_contacts()

            # Creating 2 contacts and marking one of them as favourite.
            logging.info("Creating 2 contacts and marking one of them as favourite.")
            flag = 1
            for contact_dict in _fav_all_contacts_view:
                self.dut.mbs.waitAndClickUsingContentDesc(_selector[0])
                time.sleep(1)
                self.dut.mbs.clickOnText(_selector[0])
                time.sleep(1)
                for index in range(0, 3):
                    time.sleep(1)
                    self.dut.mbs.clickOnText(_dict_keys[index])
                    self.dut.mbs.inputText(contact_dict[_dict_keys[index]])
                self.dut.mbs.clickOnText(_selector[1])
                time.sleep(2)
                if flag % 2 == 0:
                    self.dut.mbs.waitAndClickUsingContentDesc(_selector[2])
                self.dut.mbs.pressBack()
                flag += 1
            self.press_back(3)

            # Changing the orientation.
            logging.info("Changing screen orientation")
            self.dut.mbs.setOrientation("left")
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            self.allow_contact_permission()
            self.skip_sign_in()
            self.account_sync_msg_check()
            time.sleep(1)
            self.dut.mbs.assertTextDisplayed(_fav)
            self.dut.mbs.longPressText(_fav)
            time.sleep(1)
            assert self.dut.mbs.assertTextDisplayed(_selector[-1]) is True, "1 Selected text not found"
        finally:
            logging.info("Changing screen orientation")
            self.dut.mbs.setOrientation("natural")
            self.press_back(4)

    def test_share_contacts(self):
        """
        TC_CONTACT_011: Test multiple contacts Share via Gmail
        :return: None
        """
        _contact = [{'First name': 'Test', surname: 'Case', 'Phone': '9998989', 'Email': 'test-c@hcl.com',
                     'Address': 'Noida'},
                    {'First name': 'Tesian', surname: 'Salvatore', 'Phone': '9992929', 'Email': 'tesian-s@hcl.com',
                     'Address': 'Delhi'},
                    {'First name': 'Tesla', surname: 'Jordan', 'Phone': '9993939', 'Email': 'tesla-j@hcl.com',
                     'Address': 'Mumbai'}]
        _deny = uiElement['DENY']
        _allow = uiElement['ALLOW']
        _subject = "Test_Case_" + str(random.randint(0, 99)) + "_" + str(random.randint(99, 999))
        _selector = ["Share", "Gmail", "To", "Subject", "Send", "Save to Drive", save_btn,
                     "Your 1 file is being uploaded to:", "Unread me, " + _subject]
        _image_drive = "driveVerification.png"
        _gmail_image = "gmail_home.png"


        # To Unlock screen, launch contact and create multiple contacts
        self.unlock_screen()
        self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
        self.allow_contact_permission()
        self.skip_sign_in()
        self.account_sync_msg_check()
        # Delete previous contacts if exists
        if self.dut.mbs.assertTextNotDisplayed("No contacts yet"):
            self.delete_all_contacts()

        self.create_multiple_contacts(_contact=_contact)
        time.sleep(1)

        # Select the contact using long press and click on share
        self.dut.mbs.longPressText(_contact[0]['First name'] + " " + _contact[0][surname])
        self.dut.mbs.clickOnText(_contact[1]['First name'] + " " + _contact[1][surname])
        self.dut.mbs.clickOnText(_contact[2]['First name'] + " " + _contact[2][surname])
        logging.info("Click on %s:", _selector[0])
        self.dut.mbs.waitAndClickUsingContentDesc(_selector[0])
        time.sleep(1)

        # Check for permission pop up and act accordingly
        if self.dut.mbs.assertTextDisplayed(_allow) and self.dut.mbs.assertTextDisplayed(_deny):
            logging.info("Click on %s:", _allow)
            self.dut.mbs.clickOnText(_allow)
        time.sleep(3)

        # Check if device is online or not
        assert self.dut.mbs.isOnline() is True, "Device is Offline"

        # Check for Gmail option and click on it
        if self.dut.mbs.assertTextDisplayed(_selector[1]):
            logging.info("Click on %s:", _selector[1])
            self.dut.mbs.clickOnText(_selector[1])
        time.sleep(3)
        logging.info("Click on %s:", _selector[2])
        # Add email in To, enter subject and send the mail
        self.dut.mbs.clickOnText(_selector[2])
        self.dut.mbs.inputText(self.dut.mbs.getFromGmailID())
        self.press_back(1)
        time.sleep(1)
        logging.info("Click on %s:", _selector[3])
        self.dut.mbs.clickOnText(_selector[3])
        time.sleep(1)
        logging.info(_subject)
        self.dut.mbs.inputText(_subject)
        time.sleep(1)
        logging.info("Click on %s:", _selector[4])
        self.dut.mbs.waitAndClickUsingContentDesc(_selector[4])
        time.sleep(2)
        self.press_back(3)

        # Launch Gmail to verify the sent email
        time.sleep(1)
        self.dut.mbs.launchGmail()
        time.sleep(1)
        logging.info(_selector[-1])
        time.sleep(1)
        self.dut.mbs.refresh()
        time.sleep(8)
        assert self.verify_text_on_screen(image=_gmail_image, txt=_subject) is True, "Sent mail not found in inbox"

        # Press Back and open contacts again select few contacts and save on drive and verify toast
        self.dut.mbs.pressBack()
        self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
        self.allow_contact_permission()
        self.skip_sign_in()
        self.account_sync_msg_check()
        time.sleep(3)

        self.dut.mbs.longPressText(_contact[0]['First name'] + " " + _contact[0][surname])
        time.sleep(.5)
        self.dut.mbs.clickOnText(_contact[1]['First name'] + " " + _contact[1][surname])
        time.sleep(.5)
        self.dut.mbs.clickOnText(_contact[2]['First name'] + " " + _contact[2][surname])
        time.sleep(.5)
        logging.info("Click on share button")
        self.dut.mbs.waitAndClickUsingContentDesc("Share")
        time.sleep(1)

        assert self.dut.mbs.isOnline() is True, "Device is Offline"
        assert self.dut.mbs.waitUntillDisplayElementWithText("Save to Drive") is True, \
            "Save to Drive option not found"
        if self.dut.mbs.assertTextDisplayed("Save to Drive"):
            logging.info("Click on Save to drive option")
            self.dut.mbs.clickOnText("Save to Drive")
        time.sleep(1)
        if self.dut.mbs.assertTextDisplayed(_allow):
            logging.info("Deny/Allow Drive access popup found, giving access")
            self.dut.mbs.clickOnText(_allow)

        self.dut.mbs.waitUntillDisplayElementWithText(uiElement['SAVE_BTN_SHARE'])
        logging.info("Click on '%s' button to save contacts on drive", uiElement['SAVE_BTN_SHARE'])
        time.sleep(1)
        self.dut.mbs.clickOnText(uiElement['SAVE_BTN_SHARE'])
        time.sleep(.5)
        logging.info("Expected toast text '%s' ", _selector[7])
        assert self.verify_text_on_screen(image=_image_drive, txt=_selector[7]) is True, "Drive Verification Failed"
        logging.info("Drive Verified")
        logging.info("Test Successfully Completed")
        self.press_back(4)

    def multiple_contacts(self, _contact):
        _dict_keys = ['First name', 'Last name', 'Phone', 'Email']
        _selector = ["Create contact", "More fields", "Save", "Add to favorites"]

        flag = 1
        for contact_dict in _contact:
            self.dut.mbs.waitAndClickUsingContentDesc(_selector[0])
            # self.dut.mbs.clickOnText(_selector[1])
            time.sleep(1)
            for index in range(0, 5):
                time.sleep(1)
                print(_dict_keys[index])
                # if self.dut.mbs.assertTextNotDisplayed(_dict_keys[index]):
                #    self.dut.mbs.pressBack()
                self.dut.mbs.clickOnTextScrollDown(_dict_keys[index])
                # self.dut.mbs.clickOnText(_dict_keys[index])
                print(contact_dict[_dict_keys[index]])
                self.dut.mbs.inputText(contact_dict[_dict_keys[index]])
            self.dut.mbs.clickOnText(_selector[2])
            time.sleep(1)
            if flag % 2 == 0:
                self.dut.mbs.waitAndClickUsingContentDesc(_selector[3])
            self.dut.mbs.pressBack()
            flag += 1

    def create_strong_match_contacts(self, _contact):
        """
        Create strong match contact names
        :param _contact:
        :return: None
        """
        _dict_keys = ['First name', 'Email', 'Company']
        _selector = ["Create contact", "Save"]

        for ind in range(0, 4):
            self.dut.mbs.waitAndClickUsingContentDesc(_selector[0])
            if ind < 2:
                for index in range(0, 2):
                    time.sleep(1)
                    logging.info("%s: %s", _dict_keys[index], _contact[ind][_dict_keys[index]])
                    self.dut.mbs.clickOnText(_dict_keys[index])
                    self.dut.mbs.inputText(_contact[ind][_dict_keys[index]])
                    self.dut.mbs.pressBack()
                self.dut.mbs.clickOnText(_selector[1])
                time.sleep(1)
                self.dut.mbs.pressBack()
            else:
                time.sleep(1)
                logging.info("%s :%s", _dict_keys[0], _contact[ind][_dict_keys[0]])
                self.dut.mbs.clickOnText(_dict_keys[0])
                self.dut.mbs.inputText(_contact[ind][_dict_keys[0]])
                logging.info("%s :%s", _dict_keys[2], _contact[ind][_dict_keys[2]])
                self.dut.mbs.clickOnText(_dict_keys[2])
                self.dut.mbs.inputText(_contact[ind][_dict_keys[2]])
                self.dut.mbs.clickOnText(_selector[1])
                time.sleep(1)
                self.dut.mbs.pressBack()

    def navigate_to_all_app_info(self):
        _image_name = "all_app.png"
        self.dut.mbs.launchSettings()
        assert self.dut.mbs.waitUntillDisplayElementWithText("Apps & notifications") is True, \
            "Apps & notifications option not displayed in settings"
        self.dut.mbs.clickOnText("Apps & notifications")
        time.sleep(1)
        # Click to expand all app in Apps & Notifications
        _app_notification_text = self.get_screen_text(image=_image_name)
        _app_notification_text = _app_notification_text.split("\n")
        for line in range(0, len(_app_notification_text)):
            logging.info("Searching 'See all' in %s :", _app_notification_text[line])
            if "See all" in _app_notification_text[line]:
                _txt_to_click = _app_notification_text[line].encode("utf-8")
                _txt_to_click = _txt_to_click.replace('>', '')
                _txt_to_click = _txt_to_click.lstrip()
                break
        if _txt_to_click is not None:
            self.dut.mbs.clickOnText(_txt_to_click)
            return True
        else:
            logging.info("No text found to click to see all apps, failed")
            return False

    def create_duplicate_contacts(self, _contacts):
        _dict_keys = ['First name', surname, 'Company']
        _selector = ["Create contact", save_btn]
        for contact_dict in _contacts:
            time.sleep(.5)
            self.dut.mbs.waitAndClickUsingContentDesc(_selector[0])
            time.sleep(1)
            for index in range(0, 3):
                time.sleep(1)
                logging.info("%s: %s", _dict_keys[index], contact_dict[_dict_keys[index]])
                self.dut.mbs.clickOnText(_dict_keys[index])
                self.dut.mbs.inputText(contact_dict[_dict_keys[index]])
            self.dut.mbs.clickOnText(_selector[1])
            time.sleep(1)
            self.dut.mbs.pressBack()
        self.press_back(3)

    def create_multiple_contacts(self, _contact):
        # Making contacts as favourites of odd index
        _dict_keys = ['First name', surname, 'Phone', 'Email', 'Address']
        _selector = ["Create contact", "More fields", "Save", uiElement['ADD_TO_FAV']]
        flag = 1
        for contact_dict in _contact:
            self.dut.mbs.waitAndClickUsingContentDesc(_selector[0])
            self.dut.mbs.clickOnText(_selector[1])
            time.sleep(1)
            for index in range(0, 5):
                time.sleep(0.4)
                logging.info(_dict_keys[index])
                if self.dut.mbs.assertTextNotDisplayed(_dict_keys[index]):
                    self.dut.mbs.pressBack()
                    self.dut.mbs.clickOnTextScrollDown(_dict_keys[index])
                self.dut.mbs.clickOnText(_dict_keys[index])
                logging.info(contact_dict[_dict_keys[index]])
                self.dut.mbs.inputText(contact_dict[_dict_keys[index]])
            self.dut.mbs.clickOnText(_selector[2])
            time.sleep(2)
            if flag % 2 == 0:
                self.dut.mbs.waitAndClickUsingContentDesc(_selector[3])
            self.dut.mbs.pressBack()
            flag += 1

    def get_help_feedback_popular_articles(self, _help_feedback_text):
        """"
        Return list of popular articles of Help & Feedback contact screen
        """
        logging.info("help & feedback screen text: %s", _help_feedback_text)
        _help_feedback_text = _help_feedback_text.split("\n")
        _lines, _popular_articles, _flag = [], [], 0
        _articles = []
        for i in range(0, len(_help_feedback_text)):
            if _help_feedback_text[i] != '':
                _help_feedback_text[i] = _help_feedback_text[i].encode("utf-8")
                _lines.append(_help_feedback_text[i])

        for i in range(0, len(_lines)):
            if _lines[i] == "Browse all articles":
                _flag = 0
                break
            if _flag == 1:
                _popular_articles.append(_lines[i])
            if _lines[i] == "Popular articles":
                _flag = 1

        for i in range(0, len(_popular_articles)):
            logging.info("Checking popular articles for any extra char in starting")
            if _popular_articles[i][1] == " " and _popular_articles[i][0] == "a":
                logging.info("Extra character found in article %s ", _popular_articles[i])
                _articles.append(_popular_articles[i][2:])
            else:
                logging.info("Extra character not found in article %s ", _popular_articles[i])
                _articles.append(_popular_articles[i])

        for i in range(0, len(_articles)):
            logging.info("Asserting Popular articles link text on screen : '%s' ", _articles[i])
            assert self.dut.mbs.assertTextDisplayed(_articles[i]) is True, "Text not found"

        logging.info(_articles)
        return _articles

    def verify_text_on_screen(self, image=None, txt=None):

        if image is not None and txt is not None:
            is_image_exist = os.path.isfile(image)
            if is_image_exist:
                os.system("rm " + image)
            self.capture_screen_shot(image)

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

    def test_assertfail(self):
        logging.info("test_assertfail")
        a = 1
        assert a == 0, self.get_screen_text_if_assert_fail(fail_str='Failed!!!!!!!!!!!', image_name='test_assertfail.png')

    def get_screen_text_if_assert_fail(self, fail_str=None, image_name=None):
        logging.info("In get_screen_text_if_assert_fail()")
        logging.info("Assert failed for '%s' , capturing screen-shot %s", fail_str, image_name)
        logging.info("Capturing screen text")
        self.get_screen_text(image=image_name)

    def get_screen_text(self, image=None):

        if image is not None:
            is_image_exist = os.path.isfile(image)
            if is_image_exist:
                os.system("rm " + image)
            self.capture_screen_shot(image)

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

    def create_contact_revoke_permissions(self, contact_details):

        self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
        self.allow_contact_permission()
        self.skip_sign_in()
        self.account_sync_msg_check()
        no_contacts = self.dut.mbs.assertTextDisplayed("No contacts yet")
        if no_contacts is False:
            logging.info("Deleting existing contacts")
            self.delete_all_contacts()
        logging.info("Creating new contact ")
        self.dut.mbs.waitAndClickUsingResourceId(contacts_selectors.FLOATING_ACTION_BUTTON)
        for key in contact_details:
            logging.info("Adding detail for : %s", key)
            self.dut.mbs.clickOnText(key)
            self.dut.mbs.inputText(contact_details[key])
            self.dut.mbs.pressBack()
            time.sleep(1)

        self.dut.mbs.clickOnText("Save")
        time.sleep(1)
        self.dut.mbs.pressBack()
        self.dut.mbs.pressBack()

    def create_contact(self, contact_details):

        self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
        self.allow_contact_permission()
        self.skip_sign_in()
        self.account_sync_msg_check()
        no_contacts = self.dut.mbs.assertTextDisplayed("No contacts yet")
        if no_contacts is False:
            logging.info("Deleting existing contacts")
            self.delete_all_contacts()
        logging.info("Creating new contact ")
        self.dut.mbs.waitAndClickUsingResourceId(contacts_selectors.FLOATING_ACTION_BUTTON)
        self.dut.mbs.clickOnText("More fields")
        self.set_contact_photo()
        self.dut.mbs.waitAndClickUsingContentDesc("Show more name fields")
        for key in contact_details:
            logging.info("Adding detail for : %s", key)
            self.dut.mbs.scrollClickOnText(key)
            self.dut.mbs.inputText(contact_details[key])
            self.dut.mbs.pressBack()
            time.sleep(1)
            if key == 'SIP':
                # self.dut.mbs.clickOnText("Add customised field")
                self.dut.mbs.clickOnText("Add custom field")
            time.sleep(1)
            self.dut.mbs.clickOnText(save_btn)
            time.sleep(1)
            self.dut.mbs.pressBack()

    def unlock_screen(self):
        time.sleep(5)
        self.dut.mbs.inputKeyEvent(224)
        self.dut.mbs.inputKeyEvent(82)
        contact_reset_cmd = "adb -s " + config_parser.dev_li[0] + \
                            " shell pm clear " + contacts_selectors.CONTACTS_PKG
        os.system(contact_reset_cmd)

    def skip_sign_in(self):
        time.sleep(1)
        logging.info("Checking skip sign in screen")
        skip = self.dut.mbs.assertTextDisplayed("Skip")
        sign = self.dut.mbs.assertTextDisplayed("Sign in")
        if skip and sign:
            logging.info("Skip and Sign in screen found, skipping it")
            self.dut.mbs.clickOnText("Skip")

    def create_contact_label(self):

        self.dut.mbs.waitAndClickUsingResourceId("com.google.android.contacts:id/group_list")
        is_label_present = self.dut.mbs.assertElementByResID("com.google.android.contacts:id/checkbox")
        is_label_checked = self.dut.mbs.isCheckboxChecked("com.google.android.contacts:id/checkbox")
        logging.info(is_label_present)
        logging.info(is_label_checked)
        if is_label_present:
            logging.info("Label found")
            if is_label_checked:
                logging.info("Label selected already")
                self.dut.mbs.clickOnText(pop_up_cancel)
            else:
                logging.info("Checking label's checkbox")
                self.dut.mbs.waitAndClickUsingResourceId("com.google.android.contacts:id/checkbox")
        else:
            logging.info("Label not exists, creating new label")
            self.dut.mbs.waitAndClickUsingResourceId("android:id/text1")
            self.dut.mbs.inputText("testlabel")
            self.dut.mbs.clickOnText("OK")
            time.sleep(2)
            self.dut.mbs.clickOnText("OK")

    def delete_contact(self, contact_name):
        time.sleep(1)
        self.dut.mbs.clickOnText(contact_name)
        self.dut.mbs.clickOnText("Edit contact")
        time.sleep(1)
        self.dut.mbs.waitAndClickUsingContentDesc("More options")
        self.dut.mbs.clickOnText("Delete")
        self.assert_pop_up_text(contact_name)
        self.dut.mbs.clickOnText("Delete")
        time.sleep(.5)

    def assert_pop_up_text(self, contact_name):
        assert self.dut.mbs.assertTextDisplayed(
            "Delete this contact?") is True, "Expected text not found on 'Delete' popup"
        txt = contact_name + " " + "will be removed from Google Contacts and all your synced devices"
        assert self.dut.mbs.assertTextDisplayed(txt) is True, "Expected text not found on 'Delete' popup"
        assert self.dut.mbs.assertTextDisplayed("Cancel") is True, "Expected text not found on 'Delete' popup"
        assert self.dut.mbs.assertTextDisplayed("Delete") is True, "Expected text not found on 'Delete' popup"

    def delete_all_contacts(self):
        time.sleep(2)
        logging.info("Delete all contacts")
        logging.info("Waiting to display three dot menu options")
        assert self.dut.mbs.waitUntillDisplayElementWithContentDesc("More options") is True, \
            "Three dot menu option not displayed"
        logging.info("Three dot menu options displayed")
        self.dut.mbs.waitAndClickUsingContentDesc("More options")
        logging.info("Click on more options")
        self.dut.mbs.clickOnText("Select all")
        logging.info("Click on more select all")
        self.dut.mbs.waitAndClickUsingResourceId("com.google.android.contacts:id/menu_delete")
        logging.info("Click on menu option")
        self.dut.mbs.waitUntillDisplayElementWithText("Delete")
        self.dut.mbs.clickOnText("Delete")
        logging.info("Click on delete")

    def set_contact_photo(self):
        logging.info("Adding contact photo")
        assert self.dut.mbs.waitUntillDisplayElementWithContentDesc("Add contact photo") is True, \
            "Camera button not found on create contact screen"
        self.dut.mbs.waitAndClickUsingContentDesc("Add contact photo")
        assert self.dut.mbs.waitUntillDisplayElementWithText("Take photo") is True, "Take photo popup not found"
        logging.info("Click on Take photo text")
        self.dut.mbs.clickOnText("Take photo")

        if self.dut.mbs.assertTextDisplayed("GOT IT"):
            logging.info("Entering camera mode got it popup found")
            self.dut.mbs.clickOnText("GOT IT")

        if self.dut.mbs.assertTextDisplayed(uiElement['POPUP_ALLOW']):
            logging.info("Camera permission access popup found, allowing permission for Camera")
            self.dut.mbs.clickOnText(uiElement['POPUP_ALLOW'])
        else:
            logging.info("Camera permission access popup not found")

        assert self.dut.mbs.waitUntillDisplayElementWithContentDesc(
            uiElement['CAMERA_TAKE_PHOTO']) is True, "Camera capture button not found"
        logging.info("Click on Take photo desc")
        self.dut.mbs.waitAndClickUsingContentDesc(uiElement['CAMERA_TAKE_PHOTO'])
        time.sleep(1)
        assert self.dut.mbs.waitUntillDisplayElementWithContentDesc("Done") is True, \
            "Correct check mark button not found after click"
        logging.info("Click on Done desc")
        self.dut.mbs.waitAndClickUsingContentDesc("Done")
        assert self.dut.mbs.waitUntillDisplayElementWithText(uiElement['CAMERA_RESET_DONE']) is True, \
            "After click Reset Done screen not found"
        self.dut.mbs.clickOnText(uiElement['CAMERA_RESET_DONE'])
        logging.info("Clicked on Done text")
        assert self.dut.mbs.waitUntillDisplayElementWithText("Save") is True, \
            "Create contact screen not found after capturing contact picture"

    def press_input_key(self, key_event=None, count=None):
        if key_event is not None and count is not None:
            for c in range(count):
                self.dut.mbs.inputKeyEvent(key_event)
        else:
            logging.info("Please provide valid key event key and count")

    def capture_screen_shot(self, image_name):
        logging.info("Capturing screenshot...")
        self.dut.mbs.executeCommandOnDevice(" screencap -p /sdcard/" + image_name)
        cmd = "adb -s " + config_parser.dev_li[0] + " pull /sdcard/" + image_name + " ."
        logging.info(cmd)
        os.system(cmd)
        self.dut.mbs.executeCommandOnDevice(" rm /sdcard/" + image_name)

    def press_back(self, count):
        for c in range(count):
            self.dut.mbs.pressBack()

    def account_sync_msg_check(self):
        logging.info("In account_sync_msg_check()")
        if self.dut.mbs.assertTextDisplayed("Account sync is off. Tap to turn on."):
            logging.info("Account sync text found, enabling contact sync")
            self.dut.mbs.clickOnText("Account sync is off. Tap to turn on.")

    def allow_contact_permission(self):
        logging.info("In allow_contact_permission()")
        time.sleep(2)
        if self.dut.mbs.assertTextDisplayed("ALLOW"):
            logging.info("ALLOW/DENY popup found, clicking on ALLOW to contacts access")
            self.dut.mbs.clickOnText("ALLOW")
        time.sleep(2)
        if self.dut.mbs.assertTextDisplayed("ALLOW"):
            logging.info("ALLOW/DENY popup found, clicking on ALLOW to call access")
            self.dut.mbs.clickOnText("ALLOW")

    def disable_contact_permission_for_gmail(self):

        _pop_up_deny = pop_up_deny
        _pop_up_cancel = pop_up_cancel
        _apps_notification = "Apps & notifications"
        _revoke_contact_permission = ["Advanced", "App permissions", "Contacts", "Gmail"]
        _settings_navigation_android_10 = ["Apps & notifications", "Advanced", "Permission manager", "Contacts",
                                           "Gmail"]

        if android_version == '9':
            logging.info("Launching Settings of android 9")

            self.dut.mbs.launchSettings()
            logging.info("Click on notifications")
            self.dut.mbs.clickOnText(_apps_notification)
            logging.info("Revoke contact permission")
            for item in _revoke_contact_permission:
                logging.info("Click on %s", item)
                self.dut.mbs.clickOnTextScrollDown(item)
            time.sleep(1)

            _deny = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
            _cancel = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)

            logging.info(_deny)
            logging.info(_cancel)
            time.sleep(2)
            if _deny is False and _cancel is False:
                self.dut.mbs.clickOnText("Gmail")
                time.sleep(1)
                _deny1 = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
                _cancel1 = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)
                logging.info("Disabling contacts permissions for Gmail")
                time.sleep(2)
                logging.info("Clicked on Deny anyway.")
                self.dut.mbs.clickOnText(_pop_up_deny)
                time.sleep(2)

            if _deny is True and _cancel is True:
                logging.info("Contacts permissions for Gmail are enabled, disabling it ")
                self.dut.mbs.clickOnText(_pop_up_deny)
                logging.info("Clicked on Deny anyway..")
                time.sleep(2)
            self.press_back(5)

        if android_version == '10':
            logging.info("Launching Settings of android 10")
            self.dut.mbs.launchSettings()
            time.sleep(1)
            logging.info("Click on %s ", _settings_navigation_android_10[0])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[0])
            logging.info("Click on %s ", _settings_navigation_android_10[1])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[1])
            logging.info("Click on %s ", _settings_navigation_android_10[2])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[2])
            logging.info("Click on %s ", _settings_navigation_android_10[3])
            time.sleep(2)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[3])
            logging.info("Click on %s ", _settings_navigation_android_10[4])
            time.sleep(3)
            self.dut.mbs.scrollClickOnText(_settings_navigation_android_10[4])
            self.dut.mbs.clickOnText(_settings_navigation_android_10[4])
            time.sleep(1)
            self.dut.mbs.clickOnText(uiElement["DENY"])  # Disabling the Google Play Service
            time.sleep(1)
            _deny = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
            _cancel = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)

            logging.info(_deny)
            logging.info(_cancel)
            time.sleep(2)
            if _deny is True and _cancel is True:
                logging.info("Contacts permissions for Gmail are enabled, disabling it ")
                self.dut.mbs.clickOnText(_pop_up_deny)
                logging.info("Clicked on Deny anyway..")

            self.press_back(5)

    def enable_contact_permission_for_gmail(self):

        _pop_up_deny = pop_up_deny
        _pop_up_cancel = pop_up_cancel
        _apps_notification = "Apps & notifications"
        _revoke_contact_permission = ["Advanced", "App permissions", "Contacts", "Gmail"]
        _settings_navigation_android_10 = ["Apps & notifications", "Advanced", "Permission manager", "Contacts",
                                           "Gmail"]

        if android_version == '9':
            logging.info("Launching Settings of android 9")
            self.dut.mbs.launchSettings()
            logging.info("Click on notifications")
            self.dut.mbs.clickOnText(_apps_notification)
            logging.info("Enable contact permission")
            for item in _revoke_contact_permission:
                logging.info("Click on %s", item)
                self.dut.mbs.clickOnTextScrollDown(item)
            time.sleep(1)

            _deny = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
            _cancel = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)

            time.sleep(1)
            if _deny is True and _cancel is True:
                logging.info("Permission already enabled")
                logging.info("Click on %s ", _pop_up_cancel)
                self.dut.mbs.clickOnText(_pop_up_cancel)
                time.sleep(2)

            self.press_back(5)

        if android_version == '10':
            logging.info("Launching Settings of android 10")
            self.dut.mbs.launchSettings()
            time.sleep(1)
            logging.info("Click on %s ", _settings_navigation_android_10[0])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[0])
            logging.info("Click on %s ", _settings_navigation_android_10[1])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[1])
            logging.info("Click on %s ", _settings_navigation_android_10[2])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[2])
            logging.info("Click on %s ", _settings_navigation_android_10[3])
            time.sleep(2)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[3])
            logging.info("Click on %s ", _settings_navigation_android_10[4])
            time.sleep(3)
            self.dut.mbs.scrollClickOnText(_settings_navigation_android_10[4])
            self.dut.mbs.clickOnText(_settings_navigation_android_10[4])
            time.sleep(1)
            self.dut.mbs.clickOnText(uiElement["ALLOW"])  # Disabling the Google Play Service
            time.sleep(2)
            self.press_back(5)

    def clear_cache(self):
        logging.info("Clear cache")
        if android_version == '9':
            logging.info("Launching settings for android version 9")
            self.dut.mbs.launchSettings()
            time.sleep(2)
            logging.info("Click on Apps & notifications")
            self.dut.mbs.clickOnText("Apps & notifications")
            time.sleep(1)
            logging.info("Click on contacts")
            self.dut.mbs.clickOnText("Contacts")
            time.sleep(1)
            logging.info("Click on stotrage")
            self.dut.mbs.clickOnText("Storage")
            time.sleep(1)
            logging.info("Click on clear cache")
            self.dut.mbs.clickOnText(uiElement['CLEAR_CACHE'])
            time.sleep(1)
            logging.info("Click on clear storage")
            self.dut.mbs.clickOnText(uiElement['CLEAR_STORAGE'])
            time.sleep(1)
            self.dut.mbs.clickOnText(contacts_selectors.ok)
            time.sleep(2)
            self.press_back(4)
        if android_version == '10':
            logging.info("Launching settings for android version 10")
            self.dut.mbs.launchSettings()
            time.sleep(2)
            logging.info("Click on Apps & notifications")
            self.dut.mbs.clickOnText("Apps & notifications")
            logging.info("Click on contacts")
            self.dut.mbs.clickOnText("Contacts")
            logging.info("Click on Stotage & cache")
            self.dut.mbs.clickOnText("Storage & cache")
            logging.info("Click on clear cache")
            self.dut.mbs.clickOnText(uiElement['CLEAR_CACHE'])
            logging.info("Click on clear storage")
            self.dut.mbs.clickOnText(uiElement['CLEAR_STORAGE'])
            self.dut.mbs.clickOnText(contacts_selectors.ok)
            time.sleep(1)
            self.press_back(4)

    def revoke_google_play_services(self):

        _pop_up_deny = pop_up_deny
        _pop_up_cancel = pop_up_cancel
        _settings_navigation_android_9 = ["Apps & notifications", "Advanced", "App permissions", "Contacts",
                                          "Google Play services"]
        _settings_navigation_android_10 = ["Apps & notifications", "Advanced", "Permission manager", "Contacts",
                                           "Google Play Store"]

        if android_version == '9':
            logging.info("Launching settings for andrtoid 9")
            self.dut.mbs.launchSettings()
            for text in _settings_navigation_android_9:
                logging.info("Click on %s ", text)
                self.dut.mbs.clickOnTextScrollDown(text)
            time.sleep(1)
            # Checking if the dialog box is there
            _deny = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
            _cancel = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)

            logging.info(_deny)
            logging.info(_cancel)

            if _deny is False and _cancel is False:
                logging.info("Contacts permissions for Google Play Services are enabled, disabling it ")
                time.sleep(1)
                self.dut.mbs.clickOnText(_settings_navigation_android_9[-1])
                time.sleep(2)
                _deny1 = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
                _cancel1 = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)
                logging.info("Disabling contacts permissions for Google Play Service")
                self.dut.mbs.waitUntillDisplayElementWithText(_pop_up_deny)
                time.sleep(2)
                self.dut.mbs.clickOnText(_pop_up_deny)  # Click on Deny anyway option to disable the service
                time.sleep(2)
                logging.info("Clicked on %s ", _pop_up_deny)

            # If given options are there(pop up) it means service is disabled.
            if _deny is True and _cancel is True:
                self.dut.mbs.clickOnText(_pop_up_deny)
                logging.info("Clicked on %s ", _pop_up_deny)
                time.sleep(2)
            self.press_back(5)
            time.sleep(2)

        if android_version == '10':
            logging.info("Launching settings for android 10")
            self.dut.mbs.launchSettings()
            time.sleep(1)
            logging.info("Click on %s ", _settings_navigation_android_10[0])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[0])
            logging.info("Click on %s ", _settings_navigation_android_10[1])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[1])
            logging.info("Click on %s ", _settings_navigation_android_10[2])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[2])
            logging.info("Click on %s ", _settings_navigation_android_10[3])
            time.sleep(2)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[3])
            logging.info("Click on %s ", _settings_navigation_android_10[4])
            time.sleep(3)
            self.dut.mbs.scrollClickOnText(_settings_navigation_android_10[4])
            self.dut.mbs.clickOnText(_settings_navigation_android_10[4])
            time.sleep(1)
            self.dut.mbs.clickOnText(uiElement["DENY"])  # Disabling the Google Play Service
            time.sleep(1)
            _deny = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
            _cancel = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)

            logging.info(_deny)
            logging.info(_cancel)
            time.sleep(2)
            if _deny is True and _cancel is True:
                logging.info("Contacts permissions for Gmail are enabled, disabling it ")
                self.dut.mbs.clickOnText(_pop_up_deny)
                logging.info("Clicked on Deny anyway..")

            self.press_back(5)

    def enable_google_play_services(self):
        _pop_up_deny = pop_up_deny
        _pop_up_cancel = pop_up_cancel
        _settings_navigation_android_9 = ["Apps & notifications", "Advanced", "App permissions", "Contacts",
                                          "Google Play services"]
        _settings_navigation_android_10 = ["Apps & notifications", "Advanced", "Permission manager", "Contacts",
                                           "Google Play Store"]

        if android_version == '9':
            logging.info("Launching settings for andrtoid 9")
            self.dut.mbs.launchSettings()
            for text in _settings_navigation_android_9:
                logging.info("Click on %s ", text)
                self.dut.mbs.clickOnTextScrollDown(text)

            time.sleep(1)
            _deny = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
            _cancel = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)

            if _deny is False and _cancel is False:
                logging.info("Contacts permissions for Google Play Services are enabled")
            else:
                self.dut.mbs.clickOnText(_pop_up_cancel)  # Disabling the Google Play Service
            self.press_back(5)

        if android_version == '10':
            logging.info("Launching settings for android 10")
            self.dut.mbs.launchSettings()
            time.sleep(1)
            logging.info("Click on %s ", _settings_navigation_android_10[0])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[0])
            logging.info("Click on %s ", _settings_navigation_android_10[1])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[1])
            logging.info("Click on %s ", _settings_navigation_android_10[2])
            time.sleep(1)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[2])
            logging.info("Click on %s ", _settings_navigation_android_10[3])
            time.sleep(2)
            self.dut.mbs.clickOnText(_settings_navigation_android_10[3])
            logging.info("Click on %s ", _settings_navigation_android_10[4])
            time.sleep(3)
            self.dut.mbs.scrollClickOnText(_settings_navigation_android_10[4])
            self.dut.mbs.clickOnText(_settings_navigation_android_10[4])
            time.sleep(1)
            self.dut.mbs.clickOnText(uiElement["ALLOW"])  # Disabling the Google Play Service
            time.sleep(2)
            self.press_back(5)


if __name__ == '__main__':
    test_runner.main()
