from mobly import base_test
from mobly import test_runner
from mobly.controllers import android_device
import time
from collections import OrderedDict
import logging
import contacts_selectors
from PIL import Image
import pytesseract
import cv2
import os
import random
import gTAF_config

class Contacts(base_test.BaseTestClass):

    surname = "Last name"
    no_contacts_msg = "Your contacts list is empty"
    phonetic_last_name = "Phonetic last name"
    contact_save_btn = contacts_selectors.SAVE_BTN

    contact_details_revoke_permission = OrderedDict([("First name", "Tesla"), (surname, "Jordan"), ("Email", "testmail-s@hcl.com")])
    _selectors = ['Apps & notifications', 'Contacts', 'Storage', 'Clear cache',
                  'Clear storage', 'OK', 'Open navigation drawer', 'Suggestions',
                  'Merge duplicates', 'Merge', 'Getting contacts']
    _feedback_selector = ["Contacts", "", "More options", "Help & feedback", "Send feedback", "Write your feedback", "dial"]
    _create_all_contacts = OrderedDict([("Name prefix", "Mr."), ("First name", "testx"),
                                   ("Middle name", "testy"), (surname, "test1"), ("Name suffix", "test2"),
                                   (phonetic_last_name, "test3"), ("Phonetic middle name", "test4"),
                                   ("Phonetic first name", "test5"), ("Nickname", "test6"),
                                   ("Company", "HCL"), ("Title", "Service"), ("Phone", "1234567891"),
                                   ("Email", "testmail@gmail.com"),
                                   ("Website", "www.hcl.com"), ("Relationship", "test8"), ("SIP", "158998")])

    _revoke_contact_permission = ["Advanced", "App permissions", "Contacts", "Gmail"]

    _strong_match_contact = [{'First name': 'Tesse', 'Email': 'test-c@hcl.com'},
                {'First name': 'Tessei', 'Email': 'test-c@hcl.com'},
                {'First name': 'Test', 'Company': 'Hcl'},
                {'First name': 'Test', 'Company': 'Hcl'}]

    _strong_match_selector = ['Apps & notifications', 'Contacts', 'Storage', 'Clear cache', 'Clear storage', 'Getting contacts',
                 'Open navigation drawer', 'Suggestions', '2 people with duplicate listings', 'OK']

    # List of dict containing details of each contact
    _search_fav_contact_top = [{'First name': 'Test', 'Surname': 'Case', 'Phone': '9998989', 'Email': 'test-c@hcl.com',
                 'Address': 'Noida'},
                {'First name': 'Tesian', surname: 'Salvatore', 'Phone': '9992929', 'Email': 'tesian-s@hcl.com',
                 'Address': 'Delhi'},
                {'First name': 'Tesla', surname: 'Jordan', 'Phone': '9993939', 'Email': 'tesla-j@hcl.com',
                 'Address': 'Mumbai'},
                {'First name': 'Teshmie', surname: 'Mathews', 'Phone': '9994949', 'Email': 'teshmie-m@hcl.com',
                 'Address': 'Banglore'},
                {'First name': 'Tessa', surname: 'Cruise', 'Phone': '9995959', 'Email': 'tessa-c@hcl.com',
                 'Address': 'Chennai'},
                {'First name': 'Tessie', surname: 'William', 'Phone': '9996969', 'Email': 'tessie-w@hcl.com',
                 'Address': 'Gurgaun'},
                {'First name': 'Tesca', surname: 'Lockwood', 'Phone': '9997979', 'Email': 'tesca-l@hcl.com',
                 'Address': 'Chandigarh'},
                {'First name': 'Tesni', surname: 'Shied', 'Phone': '9991919', 'Email': 'tesni-s@hcl.com',
                 'Address': 'Faridabad'}]

    _fav_all_contacts_view = [{'First name': 'Test', surname: 'Case', 'Company': 'HCL'},
                              {'First name': 'Test', surname: 'Case', 'Company': 'HCL'}]


    def setup_class(self):

      # Registering android_device controller module declares the test's
      # dependency on Android device hardware. By default, we expect at least one object is created from this
      self.ads = self.register_controller(android_device)
      self.dut = self.ads[0]
      # Start Mobly Bundled Snippets (MBS).
      #self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.bundled')
      self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.example4')


    def test_CreateContact_Name(self):
      """
      TC_CONTACT_001: Create contact, test name field filling
      :return: None
      """
      try:
        image_name = 'contacts.png'
        contact_details = OrderedDict([("First name", "Tesian"), (self.surname, "Salvatore")])

        expected_toast_text = contact_details["First name"] + ' ' + contact_details[self.surname] + ' ' + "saved"
        logging.info("Expected toast message text : '%s'", expected_toast_text)

        self._unlock_screen()
        self.dut.mbs.pressHome()
        self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
        _noContacts = self.dut.mbs.assertTextDisplayed(self.no_contacts_msg)
        if _noContacts is False:
          logging.info("Deleting existing contacts")
          #self._deletAllContacts()
        logging.info("Creating new contact ")
        self.dut.mbs.waitAndClickUsingResourceId(contacts_selectors.FLOATING_ACTION_BUTTON)
        for key in contact_details:
            logging.info("Adding detail for : %s", key)
            self.dut.mbs.clickOnText(key)
            self.dut.mbs.inputText(contact_details[key])
            self.dut.mbs.pressBack()
            time.sleep(1)
        self.dut.mbs.clickOnText(self.contact_save_btn)
        time.sleep(2)

        # Verifying toast message
        toast_result = self._verify_text_on_screen(image=image_name, txt=expected_toast_text)
        assert toast_result is True, "Incorrect toast message found"
      finally:
        self._press_back(2)

    # Pending
    def test_CreateContact_AllFields(self):
      """
      TC_CONTACT_002: Create new contact with ALL fields filled in
      :return: None
      """

      name = self._create_all_contacts["Name prefix"] + ' ' + self._create_all_contacts["First name"] + ' ' + self._create_all_contacts[
        "Middle name"] + ' ' + self._create_all_contacts[self.surname] + ', ' + self._create_all_contacts["Name suffix"]

      phonetic = self._create_all_contacts[self.phonetic_last_name] + ' ' + self._create_all_contacts["Phonetic middle name"] + ' '+ self._create_all_contacts["Phonetic first name"]
      mobile = self._create_all_contacts["Phone"]
      sip = self._create_all_contacts["SIP"]
      email = self._create_all_contacts["Email"]
      nickname = self._create_all_contacts["Nickname"]
      #file_as = self._create_all_contacts["File as"]
      website = self._create_all_contacts["Website"]
      compony_title = self._create_all_contacts["Title"] + ' , ' + self._create_all_contacts["Company"]
      relationship = self._create_all_contacts["Relationship"]
      #custom_field = self._create_all_contacts["Custom field"]
      #custom_label = self._create_all_contacts["Custom label"]

      self._unlock_screen()
      self._press_back(3)
      self.dut.mbs.pressHome()
      self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
      _noContacts = self.dut.mbs.assertTextDisplayed(self.no_contacts_msg)
      if _noContacts is False:
        logging.info("Deleting existing contacts")
        #self._deletAllContacts()
      logging.info("Creating new contact ")
      self.dut.mbs.waitAndClickUsingResourceId(contacts_selectors.FLOATING_ACTION_BUTTON)
      self.dut.mbs.pressBack()
      time.sleep(1)
      self.dut.mbs.clickOnText("More fields")
      #self._setContactPhoto()

      self.dut.mbs.waitAndClickUsingContentDesc("Show more name fields")

      for key in self._create_all_contacts:
          logging.info("Adding detail for : %s", key)
          self.dut.mbs.scrollClickOnText(key)
          self.dut.mbs.inputText(self._create_all_contacts[key])
          self.dut.mbs.pressBack()
          time.sleep(1)
          if key == 'SIP':
              logging.info("Click on Add customised field")
              #self.dut.mbs.clickOnText("Add customised field")

      #self._createContactLabel()
      self.dut.mbs.clickOnText(self.contact_save_btn)
      time.sleep(1)
      self.dut.mbs.pressBack()
      assert self.dut.mbs.assertTextDisplayed(name), "Contact not found"
      self.dut.mbs.clickOnText(name)

      _contact_img = self.dut.mbs.isDisplayed(contacts_selectors.CONTACT_IMAGE_ICON_RES_ID)

      _txt = self._get_screen_text(image='cont.png')
      print(_txt)
      print("mobile,", mobile)
      assert name in _txt, "Name not found"
      assert phonetic in _txt, "Name not found"
      assert sip in _txt, "Name not found"

      self.dut.mbs.scrollDown()

      _txt = self._get_screen_text(image='cont.png')

      assert email in _txt, "Name not found"
      assert nickname in _txt, "Name not found"
      assert  phonetic in _txt, "Name not found"
      assert website in _txt, "Name not found"
      assert compony_title in _txt, "Name not found"
      assert relationship in _txt, "Name not found"

      '''

      _email = self.dut.mbs.getTextContactRFrame(0, 4, 0)
      _nickname = self.dut.mbs.getTextContactRFrame(1, 0, 0)
      _phonetic_name = self.dut.mbs.getTextContactRFrame(1, 2, 0)
      #_file_as = self.dut.mbs.getTextContactRFrame(1, 4, 0)
      _website = self.dut.mbs.getTextContactRFrame(1, 4, 0)

      self.dut.mbs.scrollDown()
      logging.info("Scroll down")
      time.sleep(1)
      _compony_title = self.dut.mbs.getTextContactRFrame(1, 4, 0)
      print("------------->",_compony_title, compony_title)
      _relationship = self.dut.mbs.getTextContactRFrame(1, 8, 0)
      print(_relationship)
      #_custom_field = self.dut.mbs.getTextContactRFrame(1, 12, 0)
      #_custom_label = self.dut.mbs.getTextContactRFrame(1, 12, 1)

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
      #assert _file_as[0] == file_as, "Incorrect file as name found"
      assert _website[0] == website, "Incorrect website name found"
      assert _compony_title[0] == compony_title, "Incorrect company title found"
      assert _relationship[0] == relationship, "Incorrect relationship value found"
      #assert _custom_field[0] == custom_field, "Incorrect custom_field value found"
      #assert _custom_label[0] == custom_label, "Incorrect custom_label value found"
      '''
      self._press_back(2)

    def test_remove_favorite_contact(self):
      """
      TC_CONTACT_013: Remove a contact from Favorites
      :return:None
      """

      self._unlock_screen()
      self.dut.mbs.pressHome()
      #self.dut.mbs.launchContacts()
      self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
      _noContacts = self.dut.mbs.assertTextDisplayed(self.no_contacts_msg)
      if _noContacts is False:
        logging.info("Deleting existing contacts")
        #self._deletAllContacts()
      logging.info("Creating new contact ")
      self.dut.mbs.waitAndClickUsingResourceId(contacts_selectors.FLOATING_ACTION_BUTTON)
      self.dut.mbs.clickOnText("First name")
      self.dut.mbs.inputText("Test")
      self.dut.mbs.clickOnText(self.surname)
      self.dut.mbs.inputText("name")
      self.dut.mbs.clickOnText(self.contact_save_btn)
      time.sleep(1)
      logging.info("Adding created contact to favourites list")
      self.dut.mbs.waitAndClickUsingContentDesc(contacts_selectors.ADD_TO_FAV_CONTENT_DESC)
      self.dut.mbs.pressBack()

      fav_content_desc = self.dut.mbs.getFavCntctDesc(0, 1, 0)
      logging.info(fav_content_desc)
      fav_content_desc = fav_content_desc.encode("ascii")
      logging.info(fav_content_desc)
      assert contacts_selectors.FAV in fav_content_desc, 'Favourites contact not found'
      self.dut.mbs.clickOnText("Test name")
      logging.info("Removing created contact from favourites list")

      self.dut.mbs.waitAndClickUsingContentDesc(contacts_selectors.REMOVE_FROM_FAV_CONTENT_DESC)
      self.dut.mbs.pressBack()
      logging.info("Verifying if favourites contact found..")
      fav_content_desc = self.dut.mbs.getFavCntctDesc(0, 1, 0)
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
        _pop_up_deny = "DENY ANYWAY"
        _pop_up_cancel = "CANCEL"
        _apps_notification = "Apps & notifications"
        _compose = "Compose"
        _to = "To"
        input_name = self.contact_details_revoke_permission["First name"]

        self._unlock_screen()
        self.dut.mbs.pressHome()
        self._create_contact_revoke_permissions(self.contact_details_revoke_permission)
        self.dut.mbs.launchSettings()
        self.dut.mbs.clickOnText(_apps_notification)
        for item in self._revoke_contact_permission:
          self.dut.mbs.clickOnTextScrollDown(item)
        time.sleep(1)

        _deny = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
        _cancel = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)

        if _deny is False and _cancel is False:
          self.dut.mbs.clickOnText(self._revoke_contact_permission[-1])
          time.sleep(1)
          _deny1 = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
          _cancel1 = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)
          logging.info("Disabling contacts permissions for Gmail")
          time.sleep(2)
          self.dut.mbs.clickOnText(_pop_up_deny)

        if _deny is True and _cancel is True:
          logging.info("Contacts permissions for Gmail are enabled, disabling it ")
          self.dut.mbs.clickOnText(_pop_up_deny)
          time.sleep(1)
          logging.info("Clicked on deny anyway on popup")

        self._press_back(4)
        self.dut.mbs.launchGmail()

        self.dut.mbs.waitAndClickUsingContentDesc(_compose)
        self.dut.mbs.clickOnText(_to)
        self.dut.mbs.inputText(input_name)
        time.sleep(2)
        self._press_input_key(key_event=67, count=len(input_name))
        self.dut.mbs.inputText(input_name)
        time.sleep(2)
        # Verifying toast message
        toast_result = self._verify_text_on_screen(image=image_name, txt=expected_toast_text)
        assert toast_result is True, "Incorrect toast message found"

        # To filed text verification
        to_field_text = self.dut.mbs.getTextByResourceId(contacts_selectors.CONTACT_TO_RES_ID)
        to_field_text = to_field_text.encode("ascii")
        logging.info("To filed text : %s ", to_field_text)
        assert to_field_text.decode("utf-8") == input_name, "Invalid text found in To field"

      finally:
        self._press_input_key(key_event=67, count=len(input_name))
        self._press_back(5)

    def test_delete_contact(self):
      """
      TC_CONTACT_015: Delete contact test
      :return: None
      """
      try:
        contact_name = self.contact_details_revoke_permission["First name"] + " " + \
                        self.contact_details_revoke_permission[self.surname]
        expected_toast_text = contact_name + " deleted"
        image_name = "delete_contact.png"
        logging.info("Delete contact toast message to be verify : '%s' ", expected_toast_text)

        self._unlock_screen()
        self.dut.mbs.pressHome()
        self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
        _noContacts = self.dut.mbs.assertTextDisplayed(self.no_contacts_msg)
        if _noContacts is False:
          logging.info("Deleting existing contacts")
          #self._deletAllContacts()
        logging.info("Creating new contact ")
        self._create_contact_revoke_permissions(self.contact_details_revoke_permission)
        self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
        self._deleteContact(contact_name)

        # Verifying toast message
        toast_result = self._verify_text_on_screen(image=image_name, txt=expected_toast_text)
        assert toast_result is True, "Incorrect toast message found"

      finally:
        self._press_back(2)

    def test_contact_permission_grant_from_gmail(self):
      """
      TC_CONTACT_008: Test contact name auto complete in Gmail after granting Contacts permission
      :return: None
      """
      try:
        expected_toast_text = self.contact_details_revoke_permission["First name"] + " " \
                              +  self.contact_details_revoke_permission[self.surname]
        image_name = "contact_suggestion_grant.png"
        #_contact_permission = ["Advanced", "App permissions", "Contacts", "Gmail"]
        _pop_up_deny = "DENY ANYWAY"
        _pop_up_cancel = "CANCEL"
        _apps_notification = "Apps & notifications"
        _compose = "Compose"
        _to = "To"
        input_name = self.contact_details_revoke_permission["First name"]

        self._unlock_screen()
        self.dut.mbs.pressHome()
        self._create_contact_revoke_permissions(self.contact_details_revoke_permission)
        self.dut.mbs.launchSettings()
        self.dut.mbs.clickOnText(_apps_notification)
        for item in self._revoke_contact_permission:
          self.dut.mbs.clickOnTextScrollDown(item)
        time.sleep(1)

        _deny = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
        _cancel = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)
        logging.info(_deny)
        logging.info(_cancel)
        if _deny is True and _cancel is True:
          logging.info("Contacts permissions for Gmail are enabled")
          self.dut.mbs.clickOnText(_pop_up_cancel)
          time.sleep(2)

        self._press_back(4)
        self.dut.mbs.launchGmail()

        self.dut.mbs.waitAndClickUsingContentDesc(_compose)
        self.dut.mbs.clickOnText(_to)
        self.dut.mbs.inputText(input_name)
        time.sleep(2)
        # Verifying toast message
        logging.info("Expected toast message : %s ", expected_toast_text)
        toast_result = self._verify_text_on_screen(image=image_name, txt=expected_toast_text)
        assert toast_result is True, "Incorrect toast message found"
      finally:
        self._press_input_key(key_event=67, count=len(input_name))
        self._press_back(5)

    #Pending
    def test_strong_match_for_duplicates(self):
        """
        TC_CONTACT_003: Strong match duplicates
        :return: None
        """
        try:
            logging.info("Executing TC_CONTACT_003: Strong match duplicates")
            #_contact = [{'First name': 'Tesse', 'Email': 'test-c@hcl.com'}, {'First name': 'Tessei', 'Email': 'test-c@hcl.com'}, {'First name': 'Test', 'Company': 'Hcl'}, {'First name': 'Test', 'Company': 'Hcl'}]
            #_selector = ['Apps & notifications', 'Contacts', 'Storage', 'Clear cache', 'Clear storage', 'Getting contacts', 'Open navigation drawer', 'Suggestions', '2 people with duplicate listings', 'OK']

            _expected_text_firstcluster = "Showing 2 duplicates for " + self._strong_match_contact[2]["First name"] + ". Swipe to dismiss"
            _expected_text_secondcluster = "Showing 2 duplicates for " + self._strong_match_contact[1]["First name"] + ". Swipe to dismiss"

            # To launch contacts app and delete all existing contacts
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            if self.dut.mbs.assertTextNotDisplayed(self.no_contacts_msg):
                logging.info("Deleting all contacts")
                #self._deletAllContacts()
            logging.info("Creating Contacts")
            self._create_strong_match_contacts(_contact=self._strong_match_contact)
            # To Launch Settings
            self.dut.mbs.launchSettings()

            for index in range(0, 3):
                logging.info("Click on %s : ", self._strong_match_selector[index])
                self.dut.mbs.clickOnText(self._strong_match_selector[index])

            logging.info("Click on clear cache")
            self.dut.mbs.clickOnText(contacts_selectors.CLEAR_CACHE)
            logging.info("Click on clear storage")
            self.dut.mbs.clickOnText(contacts_selectors.CLEAR_STORAGE)
            self.dut.mbs.clickOnText(contacts_selectors.ok_txt)
            self._press_back(4)

            # To launch contacts app
            self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
            time.sleep(3)
            while (self.dut.mbs.assertTextDisplayed(self._selectors[-1])):
                logging.info("Getting Contacts progress bar found, waiting to disappear..")
                time.sleep(0.5)
                continue
            self.dut.mbs.waitAndClickUsingContentDesc(self._selectors[6])
            self.dut.mbs.clickOnText(self._selectors[7])
            logging.info("Refreshing suggestion screen")
            time.sleep(2)
            self.dut.mbs.refresh()
            time.sleep(4)
            assert self.dut.mbs.assertTextDisplayed(self._strong_match_selector[8]), " Merge duplicates pop up not found"
            self.dut.mbs.clickOnText(self._selectors[8])

            logging.info("Verifying element with conetent description '%s' and '%s' ", _expected_text_firstcluster, _expected_text_secondcluster)
            assert self.dut.mbs.isContentDescExist(_expected_text_firstcluster) is True , "First cluster verification failed"
            assert self.dut.mbs.isContentDescExist(_expected_text_secondcluster) is True, "Second cluster verification failed"

        finally:
            #self._press_back(4)
            print("")

    # Pending
    def test_suggestion_welcome_card(self):
      """
      TC_CONTACT_004: Suggestions > Welcome Card verification
      :return: None
      """
      try:
        _suggestion_welcome_header = "Welcome to your suggestions"
        _got_it_text = "Got it"
        _apps_notification = "Apps & notifications"
        self._unlock_screen()
        self._press_back(3)
        self.dut.mbs.pressHome()

        # Open Contact's app info screen
        if self._navigate_to_all_app_info():
            time.sleep(2)
            for i in range(0, 5):
                if self.dut.mbs.assertTextDisplayed('Contacts'):
                    logging.info("Contact app name visible on screen")
                    self.dut.mbs.clickOnText('Contacts')
                    break
                else:
                    logging.info("Contact app name not visible on screen, scrolling down to search")
                    self.dut.mbs.scrollDown()
        else:
            logging.info("Not clicked on Seel all app to expand.")
        # To Launch Settings
        # self.dut.mbs.launchSettings()
        for index in range(2, 6):
            self.dut.mbs.clickOnText(self._selectors[index])

        self._press_back(5)

        self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
        logging.info("Click on 3 line to open side bar")
        self.dut.mbs.waitAndClickUsingContentDesc(contacts_selectors.CONTACT_DRAWER_DESC)
        time.sleep(1)
        self.dut.mbs.clickOnText("Suggestions")
        logging.info("Verifying suggestion welcome screen messages")
        self.dut.mbs.assertTextDisplayed(_suggestion_welcome_header)
        self.dut.mbs.assertTextDisplayed(_got_it_text)
        _header = self.dut.mbs.getTextByResourceId(contacts_selectors.SUGGESTIONS_WELCOME_HEADER)
        _got_it= self.dut.mbs.getTextByResourceId(contacts_selectors.SUGGESTIONS_WELCOME_GOT_IT)
        _header = _header.encode("utf-8")
        _got_it = _got_it.encode("utf-8")
        self.dut.mbs.clickOnText("Got it")
        self.dut.mbs.assertTextDisplayed(_suggestion_welcome_header)
        self.dut.mbs.assertTextDisplayed(_got_it_text)
        assert _header ==  _suggestion_welcome_header, " 'Welcome to your suggestions' not found"
        assert _got_it == _got_it_text , " 'Got it' text not found"
      finally:
        self._press_back(3)

    def test_merge_duplicates(self):
        """
        TC_CONTACT_005 :Suggestions  Merge Duplicates
        :return: None
        """
        try:
          _contact = [{'First name': 'Test', self.surname: 'Case', 'Company': 'HCL'},
                      {'First name': 'Test', self.surname: 'Case', 'Company': 'HCL'}]
          _duplicates = [_contact[0]['First name'] + " " + _contact[0][self.surname],
                         _contact[1]['First name'] + " " + _contact[1][self.surname]]
          merge_verify_image = "merge_verification.png"
          merge_text = "Contacts merged"
          suggestion_text = "Welcome to your suggestions"

          self._unlock_screen()
          self._press_back(4)
          self.dut.mbs.pressHome()

        # To launch contacts app
          self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)

        # Delete previous contacts if exists
          if self.dut.mbs.assertTextDisplayed(self.no_contacts_msg):
              #self._deletAllContacts()
              print("")

          # Create new contacts
          self._create_duplicate_contacts(_contacts=_contact)

          # Open Contact's app info screen
          self._navigate_to_all_app_info()
          time.sleep(2)
          for i in range(0, 5):
              if self.dut.mbs.assertTextDisplayed('Contacts'):
                  logging.info("Contact app name visible on screen")
                  self.dut.mbs.clickOnText('Contacts')
                  break
              else:
                  logging.info("Contact app name not visible on screen, scrolling down to search")
                  self.dut.mbs.scrollDown()

          # clear contact's cache and storage
          for index in range(2, 6):
              self.dut.mbs.clickOnText(self._selectors[index])
          self._press_back(4)

        # To launch contacts app
          self.dut.mbs.launchContacts()
          logging.info(self._selectors[-1])
          while(self.dut.mbs.assertTextDisplayed(self._selectors[-1])):
            logging.info("Getting Contacts progress bar found, waiting to disappear..")
            time.sleep(0.5)
            continue
          self.dut.mbs.waitAndClickUsingContentDesc(self._selectors[6])
          self.dut.mbs.clickOnText(self._selectors[7])

          logging.info("Refreshing suggestion screen")
          time.sleep(2)
          self.dut.mbs.refresh()
          time.sleep(4)

        # Verification 1: User sees duplicate suggestion card "Merge duplicates" if duplicates contacts are there.
          logging.info(self._selectors[8])
          logging.info(self.dut.mbs.assertTextDisplayed(self._selectors[8]))
          assert self.dut.mbs.assertTextDisplayed(self._selectors[8]) is True, "Suggestion Card \"Merge duplicates\" not found"
          self.dut.mbs.clickOnText(self._selectors[8])

          logging.info(_duplicates[0])
        # Verification 2: On clicking "Merge duplicates" duplicates are shown.
          assert self.dut.mbs.assertTextDisplayed(_duplicates[0]) is True and self.dut.mbs.assertTextDisplayed(_duplicates[0]) is True, "Duplicates are not shown."

          self.dut.mbs.clickOnText(self._selectors[9])
          time.sleep(2)

        # Verification 3: The duplicates were merged.
          assert self._verify_text_on_screen(image = merge_verify_image, txt = merge_text) is True, "Duplicates didn't merge."

        # Verification 4: On clicking back arrow, verify that Suggestions view loads.
          self.dut.mbs.pressBack()
          time.sleep(1)
          assert self.dut.mbs.assertTextDisplayed(suggestion_text) is True, "Suggestions view loads verification failed."

        finally:
          self._press_back(5)

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
        self._unlock_screen()
        self._press_back(4)
        self.dut.mbs.pressHome()
        self.dut.mbs.launchGmail()
        self.dut.mbs.waitAndClickUsingContentDesc("Open navigation drawer")
        time.sleep(2)
        self.dut.mbs.scrollDown()
        time.sleep(2)
        self.dut.mbs.clickOnText("Settings")
        time.sleep(2)
        logging.info("Capturing screenshot to check the configured google account in devices")
        gmail_account_text = self._get_screen_text(image=gmail_account_image)
        gmail_account_text = gmail_account_text.encode("utf-8")
        gmail_account_text = gmail_account_text.replace("\n", " ")

        if gmail_account_text.count("@gmail.com") == 1:
          logging.info("Only one google account configured currently in device")
          self.dut.mbs.launchContacts()
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
          toast_result = self._verify_text_on_screen(image=image_name, txt=expected_toast_message)
          assert toast_result is True, "Incorrect create label toast text found"
        else:
          logging.info("More then one google account configured currently in device")
      finally:
        logging.info("Deleting created label")
        self.dut.mbs.waitAndClickUsingContentDesc("More options")
        self.dut.mbs.clickOnText("Delete label")
        self._press_back(3)

    def test_contact_help_feedback(self):
      """
      TC_CONTACT_014 To test help & feedback
      :return: None
      """
      try:
        # list of data to be verified
        verification_data = ["Browse all articles", "Contact us", "Send feedback"]
        image_name = "feedback_image.png"

        contact_name = self.contact_details_revoke_permission["First name"] + " " + \
                       self.contact_details_revoke_permission[self.surname]

        self._unlock_screen()
        self.dut.mbs.pressHome()
        self.dut.mbs.launchContacts()
        _noContacts = self.dut.mbs.assertTextDisplayed("No contacts yet")
        if _noContacts is False:
          logging.info("Deleting existing contacts")
          self._deletAllContacts()
        logging.info("Creating new contact ")
        self._create_contact_revoke_permissions(self.contact_details_revoke_permission)
        self.dut.mbs.launchContacts()
        self.dut.mbs.clickOnText(contact_name)

        # Click on the Overflow Menu
        self.dut.mbs.waitAndClickUsingContentDesc(self._feedback_selector[2])

        # Click on Help & Feedback option
        self.dut.mbs.clickOnText(self._feedback_selector[3])
        time.sleep(1)

        # Get available popular articles list
        popular_articles = self._get_help_feedback_popular_articles(self._get_screen_text(image=image_name))

        logging.info("Popular articles are %s ", popular_articles)
        # Check whether the  device is online or not
        if self.dut.mbs.isOnline():
          for article in range(0, len(popular_articles)):
            logging.info("Clicking on  '%s'", popular_articles[article])
            self.dut.mbs.clickOnText(popular_articles[article])
            time.sleep(2)

            # Verify text not expected text on respective article's screen
            for assert_text in range(0, len(verification_data)):
              assert self.dut.mbs.assertTextDisplayed(verification_data[assert_text]) is False, "Expected text not found"
            self._press_back(1)

          # Verify feedback sent option
          self.dut.mbs.clickOnText(self._feedback_selector[4])
          time.sleep(1)
          self.dut.mbs.clickUsingResourceId("com.google.android.gms:id/gf_issue_description")
          self.dut.mbs.inputText("Good")
          self.dut.mbs.waitAndClickUsingContentDesc("Send")
          time.sleep(5)
          flag = False
          for i in range(1, 20):
            if self._verify_text_on_screen(image=image_name, txt="Thank you for the feedback"):
               flag = True
               break
            else:
              logging.info(self._feedback_selector[5] + " Edit text not found")

          assert flag is True, "Feedback confirmation could not get successfully"
        else:
          logging.info("Test Failed, Device is Offline")
          assert False

      finally:
        self._press_back(4)
        self.dut.mbs.pressHome()


    def test_google_play_service_permission_revoke(self):
      """
      TC_CONTACT_009: To revoke the Google play service and check the sync with google account, app should not crash
      :return: None
      """
      try:
          _select = ["Apps & notifications", "Advanced", "App permissions", "Contacts",
                     "Google Play services"]  # list to be used to open app permission in settings
          _case_select = ["Open navigation drawer", "Settings", "Accounts", "Google", "Account sync", "Contacts",
                          "Sync failed"]  # list to open contact and execute test case
          _pop_up_deny = "Deny anyway"  # To check deny anyway option
          _pop_up_cancel = "Cancel"
          _image_name = "app_notification.png"

          self._unlock_screen()  # TO unlock the screen
          self.dut.mbs.pressHome()  # To Press Home
          # self.dut.mbs.launchApp(contacts_selectors.SETTINGS_LAUNCHER_ACTIVITY)  # To Launch Settings
          self.dut.mbs.launchSettings()

          # Open App Permission
          for text in _select:
              self.dut.mbs.clickOnTextScrollDown(text)

          time.sleep(1)

          # Checking if the dialog box is there
          _deny = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
          _cancel = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)

          if _deny is False and _cancel is False:
              logging.info("Contacts permissions for Google Play Services are enabled, disabling it ")
              time.sleep(1)
              self.dut.mbs.clickOnText(_select[-1])  # Disabling the Google Play Service
              time.sleep(2)
              _deny1 = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
              _cancel1 = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)
              logging.info("Disabling contacts permissions for Google Play Service")
              self.dut.mbs.clickOnText(_pop_up_deny)  # Click on Deny anyway option to disable the service

          # If given options are there(pop up) it means service is disabled.
          if _deny is True and _cancel is True:
              self.dut.mbs.clickOnText(_pop_up_deny)  # Click on Deny anyway option to disable the service

          self._press_back(5)
          time.sleep(1)
          self.dut.mbs.launchContacts()  # Launch the Dialer App
          time.sleep(3)
          self.dut.mbs.waitAndClickUsingContentDesc(_case_select[0])  # TO open NAVIGATION DRAWER
          self.dut.mbs.clickOnText(_case_select[1])  # To click on  SETTINGS
          self.dut.mbs.clickOnText(_case_select[2])  # To click on ACCOUNTS
          time.sleep(2)
          if self.dut.mbs.assertTextDisplayed(_case_select[3]):  # To check existence of text GOOGLE
              self.dut.mbs.clickOnText(_case_select[3])  # To click on text GOOGLE
          else:
              logging.info("Test Failed, Add Google Account")
              assert False
          time.sleep(1)
          logging.info("Verifying if any crash is there")
          assert self.dut.mbs.uiWatcherTextContains("isn't responding") is False, "Crash found"
          logging.info("No crash observed")
          self.dut.mbs.clickOnText(_case_select[4])  # To click on ACCOUNT SYNC

          for index in range(4):
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
              self.dut.mbs.clickOnText(_case_select[5])  # To click on CONTACTS
          self._press_back(5)

      finally:
          # Enable Google play services
          logging.info("Enabling Google play services")
          self.dut.mbs.launchSettings()
          for text in _select:
              self.dut.mbs.clickOnTextScrollDown(text)
          time.sleep(1)
          _deny = self.dut.mbs.assertTextDisplayed(_pop_up_deny)
          _cancel = self.dut.mbs.assertTextDisplayed(_pop_up_cancel)

          if _deny is False and _cancel is False:
              logging.info("Contacts permissions for Google Play Services are enabled")
          else:
              self.dut.mbs.clickOnText(_select[-1])  # Disabling the Google Play Service
          self._press_back(4)

    def test_search_favourite_on_top(self):
      """
      TC_CONTACT_010 Favorite seach results on top test
      :return: None
      """
      try:

        # List of all the names of favourite contacts from _contact
        _fav = [self._search_fav_contact_top[3]['First name'] + " " + self._search_fav_contact_top[3][self.surname],
                self._search_fav_contact_top[1]['First name'] + " " + self._search_fav_contact_top[1][self.surname],
                self._search_fav_contact_top[7]['First name'] + " " + self._search_fav_contact_top[7][self.surname],
                self._search_fav_contact_top[5]['First name'] + " " + self._search_fav_contact_top[5][self.surname]]

        logging.info("favouratis contacts : %s ", _fav)
        self.dut.mbs.launchContacts()

        # Delete previous contacts if exists
        if self.dut.mbs.assertTextNotDisplayed("No contacts yet"):
          self._deletAllContacts()
        self._create_multiple_contacts(_contact=self._search_fav_contact_top)

        # To search the contact and retrieve the search result into a list
        self.dut.mbs.clickOnText("Search contacts")
        self.dut.mbs.inputText("Tes")
        self.dut.mbs.pressBack()
        _item_list = self.dut.mbs.getAllItemsOfListView(8)
        logging.info("Fetched contacts after create contact : %s ", _item_list)

        # Verifying that all the favourites are at the top of the search result
        for i in range(0, 4):
          if str(_item_list[i]).encode("ascii") in _fav:
            assert True
          else:
            assert False
      finally:
        self._press_back(3)
        self.dut.mbs.pressHome()

    def test_favourite_in_all_contact(self):
        """
        TC_CONTACT_012: Test favorites in 'All Contacts' view
        :return: None
        """
        try:
            _dict_keys = ['First name', self.surname, 'Company']
            _selector = ["Create contact", "Save", "Add to favourites", "1 selected"]
            _fav = self._fav_all_contacts_view[1]['First name'] + " " + self._fav_all_contacts_view[1][self.surname]

            self._unlock_screen()

            # To launch contacts app and delete all existing contacts
            self.dut.mbs.launchContacts()

            # Delete previous contacts if exists
            if self.dut.mbs.assertTextNotDisplayed("No contacts yet"):
                self._deletAllContacts()

            #Creating 2 contacts and marking one of them as favourite.
            flag = 1
            for contact_dict in self._fav_all_contacts_view:
                self.dut.mbs.waitAndClickUsingContentDesc(_selector[0])
                self.dut.mbs.clickOnText(_selector[0])
                time.sleep(1)
                for index in range(0, 3):
                    time.sleep(1)
                    #logging.info("%s: %s", _dict_keys[index], contact_dict[_dict_keys[index]])
                    self.dut.mbs.clickOnText(_dict_keys[index])
                    self.dut.mbs.inputText(contact_dict[_dict_keys[index]])
                self.dut.mbs.clickOnText(_selector[1])
                time.sleep(2)
                if flag % 2 == 0:
                    self.dut.mbs.waitAndClickUsingContentDesc(_selector[2])
                self.dut.mbs.pressBack()
                flag += 1
            self._press_back(3)

            #Changing the orientation.
            self.dut.mbs.setOrientation("left")
            self.dut.mbs.launchContacts()
            time.sleep(1)
            self.dut.mbs.assertTextDisplayed(_fav)
            self.dut.mbs.longPressText(_fav)
            time.sleep(1)
            assert self.dut.mbs.assertTextDisplayed(_selector[-1]) is True, "1 Selected text not found"
        finally:
            self.dut.mbs.setOrientation("natural")
            self._press_back(3)

    def test_share_contacts(self):
        """
        TC_CONTACT_011: Test multiple contacts Share via Gmail
        :return: None
        """
        _contact = [{'First name': 'Test', self.surname: 'Case', 'Phone': '9998989', 'Email': 'test-c@hcl.com',
                     'Address': 'Noida'},
                    {'First name': 'Tesian', self.surname: 'Salvatore', 'Phone': '9992929', 'Email': 'tesian-s@hcl.com',
                     'Address': 'Delhi'},
                    {'First name': 'Tesla', self.surname: 'Jordan', 'Phone': '9993939', 'Email': 'tesla-j@hcl.com',
                     'Address': 'Mumbai'}]
        _deny = "Deny"
        _allow = "Allow"
        _subject = "Test_Case_"+str(random.randint(0,99))+"_"+str(random.randint(99,999))
        _selector = ["Share", "Gmail", "To", "Subject", "Send","Save to Drive","Save", "Your 1 file is being uploaded to: My Drive","Unread me, " + _subject]
        _image_drive = "driveVerification.png"
        _gmail_image = "gmail_home.png"

        # To Unlock screen, launch contact and create multiple contacts
        self._unlock_screen()
        self.dut.mbs.launchContacts()

        # Delete previous contacts if exists
        if self.dut.mbs.assertTextNotDisplayed("No contacts yet"):
            self._deletAllContacts()

        self._create_multiple_contacts(_contact=_contact)
        time.sleep(1)

        # Select the contact using long press and click on share
        self.dut.mbs.longPressText(_contact[0]['First name'] + " " + _contact[0][self.surname])
        self.dut.mbs.clickOnText(_contact[1]['First name'] + " " + _contact[1][self.surname])
        self.dut.mbs.clickOnText(_contact[2]['First name'] + " " + _contact[2][self.surname])
        self.dut.mbs.waitAndClickUsingContentDesc(_selector[0])
        time.sleep(1)

        # Check for permission pop up and act accordingly
        if self.dut.mbs.assertTextDisplayed(_allow) and self.dut.mbs.assertTextDisplayed(_deny):
            self.dut.mbs.clickOnText(_allow)
        time.sleep(3)

        # Check if device is online or not
        assert self.dut.mbs.isOnline() is True, "Device is Offline"

        # Check for Gmail option and click on it
        if self.dut.mbs.assertTextDisplayed(_selector[1]):
            self.dut.mbs.clickOnText(_selector[1])
        time.sleep(3)

        # Add email in To, enter subject and send the mail
        self.dut.mbs.clickOnText(_selector[2])
        self.dut.mbs.inputText(self.dut.mbs.getFromGmailID())
        self._press_back(1)
        time.sleep(1)
        self.dut.mbs.clickOnText(_selector[3])
        time.sleep(1)
        logging.info(_subject)
        self.dut.mbs.inputText(_subject)
        time.sleep(1)
        self.dut.mbs.waitAndClickUsingContentDesc(_selector[4])
        self._press_back(3)

        # Launch Gmail to verify the sent email
        time.sleep(1)
        self.dut.mbs.launchGmail()

        logging.info(_selector[-1])
        time.sleep(1)
        self.dut.mbs.refresh()
        time.sleep(7)
        assert self._verify_text_on_screen(image=_gmail_image, txt=_subject) is True, "Sent mail not found in inbox"

        # Press Back and open contacts again select few contacts and save on drive and verify toast
        self.dut.mbs.pressBack()
        self.dut.mbs.launchContacts()
        time.sleep(1)

        self.dut.mbs.longPressText(_contact[0]['First name'] + " " + _contact[0][self.surname])
        self.dut.mbs.clickOnText(_contact[1]['First name'] + " " + _contact[1][self.surname])
        self.dut.mbs.clickOnText(_contact[2]['First name'] + " " + _contact[2][self.surname])
        self.dut.mbs.waitAndClickUsingContentDesc(_selector[0])
        time.sleep(1)

        if self.dut.mbs.assertTextDisplayed(_allow) and self.dut.mbs.assertTextDisplayed(_deny):
            self.dut.mbs.clickOnText(_allow)
        time.sleep(2)
        assert self.dut.mbs.isOnline() is True, "Device is Offline"
        if self.dut.mbs.assertTextDisplayed(_selector[5]):
            self.dut.mbs.clickOnText(_selector[5])
        time.sleep(3)
        self.dut.mbs.pressBack()
        time.sleep(1)
        self.dut.mbs.clickOnText(_selector[6])
        time.sleep(2)
        assert self._verify_text_on_screen(image=_image_drive, txt=_selector[7]) is True, "Drive Verification Failed"
        logging.info("Drive Verified")
        logging.info("Test Successfully Completed")
        self._press_back(2)

    def _create_multiple_contacts(self, _contact):
        _dict_keys = ['First name', 'Last name', 'Phone', 'Email', 'Address']
        _selector = ["Create contact", "More fields", "Save", "Add to favorites"]

        flag = 1
        for contact_dict in _contact:
            self.dut.mbs.waitAndClickUsingContentDesc(_selector[0])
            self.dut.mbs.clickOnText(_selector[1])
            time.sleep(1)
            for index in range(0, 5):
                time.sleep(1)
                print(_dict_keys[index])
                if self.dut.mbs.assertTextNotDisplayed(_dict_keys[index]):
                    self.dut.mbs.pressBack()
                    self.dut.mbs.scrollDown()
                self.dut.mbs.clickOnText(_dict_keys[index])
                print(contact_dict[_dict_keys[index]])
                self.dut.mbs.inputText(contact_dict[_dict_keys[index]])
            self.dut.mbs.clickOnText(_selector[2])
            time.sleep(1)
            if flag % 2 == 0:
                self.dut.mbs.waitAndClickUsingContentDesc(_selector[3])
            self.dut.mbs.pressBack()
            flag += 1

    def _create_strong_match_contacts(self, _contact):
        """
        Create strong match contact names
        :param _contact:
        :return: None
        """
        _dict_keys = ['First name', 'Email', 'Company']
        _selector = [contacts_selectors.CREATE_CONTACT_DESC, self.contact_save_btn]

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
                self.dut.mbs.pressBack()
                self.dut.mbs.clickOnText("More fields")
                logging.info("%s :%s", _dict_keys[2], _contact[ind][_dict_keys[2]])
                self.dut.mbs.clickOnText(_dict_keys[2])
                self.dut.mbs.inputText(_contact[ind][_dict_keys[2]])
                self.dut.mbs.clickOnText(_selector[1])
                time.sleep(1)
                self.dut.mbs.pressBack()

    def _navigate_to_all_app_info(self):
        _image_name = "all_app.png"
        self.dut.mbs.launchSettings()
        time.sleep(1)
        self.dut.mbs.clickOnText("Apps & notifications")
        time.sleep(1)
        # Click to expand all app in Apps & Notifications
        _app_notification_text = self._get_screen_text(image=_image_name)
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

    def _create_duplicate_contacts(self, _contacts):
      _dict_keys = ['First name', self.surname, 'Company']
      _selector = ["Create contact", "Save"]
      for contact_dict in _contacts:
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
      self._press_back(3)

    def _create_multiple_contacts(self,_contact):
      # Making contacts as favourites of odd index
        _dict_keys = ['First name', self.surname, 'Phone', 'Email', 'Address']
        _selector = ["Create contact", "More fields", "Save", "Add to favourites"]
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
                    self.dut.mbs.scrollDown()
                self.dut.mbs.clickOnText(_dict_keys[index])
                logging.info(contact_dict[_dict_keys[index]])
                self.dut.mbs.inputText(contact_dict[_dict_keys[index]])
            self.dut.mbs.clickOnText(_selector[2])
            time.sleep(2)
            if flag % 2 == 0:
              self.dut.mbs.waitAndClickUsingContentDesc(_selector[3])
            self.dut.mbs.pressBack()
            flag += 1

    def _get_help_feedback_popular_articles(self, _help_feedback_text):
      """"
      Return list of popular articles of Help & Feedback contact screen
      """
      logging.info("-----help feedback screen text----- : %s", _help_feedback_text)
      _help_feedback_text = _help_feedback_text.split("\n")
      _lines, _popular_articles, _flag = [], [], 0
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
        logging.info("Asserting Popular articles link text on screen : '%s' ", _popular_articles[i])
        assert self.dut.mbs.assertTextDisplayed(_popular_articles[i]) is True, "Text not found"
      return _popular_articles

    def _verify_text_on_screen(self, image=None, txt=None):

      if image is not None and txt is not None:
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
          logging.info("Screen-shot not found")
      else:
        logging.info("Please give valid input parameters")

    def _create_contact_revoke_permissions(self, contact_details):

      self.dut.mbs.launchApp(contacts_selectors.CONTACTS_LAUNCHER_ACTIVITY)
      _noContacts = self.dut.mbs.assertTextDisplayed(self.no_contacts_msg)
      if _noContacts is False:
        logging.info("Deleting existing contacts")
        #self._deletAllContacts()
      logging.info("Creating new contact ")
      self.dut.mbs.waitAndClickUsingResourceId(contacts_selectors.FLOATING_ACTION_BUTTON)
      for key in contact_details:
        logging.info("Adding detail for : %s", key)
        self.dut.mbs.clickOnText(key)
        self.dut.mbs.inputText(contact_details[key])
        self.dut.mbs.pressBack()
        time.sleep(1)

      self.dut.mbs.clickOnText(self.contact_save_btn)
      time.sleep(1)
      self.dut.mbs.pressBack()
      self.dut.mbs.pressBack()

    def _create_contact(self, contact_details):
      self.dut.mbs.launchContacts()
      _noContacts = self.dut.mbs.assertTextDisplayed("No contacts yet")
      if _noContacts is False:
        logging.info("Deleting existing contacts")
        self._deletAllContacts()
      logging.info("Creating new contact ")
      self.dut.mbs.waitAndClickUsingResourceId(contacts_selectors.FLOATING_ACTION_BUTTON)
      self.dut.mbs.clickOnText("More fields")
      self._setContactPhoto()
      self.dut.mbs.waitAndClickUsingContentDesc("Show more name fields")
      for key in contact_details:
        logging.info("Adding detail for : %s", key)
        self.dut.mbs.scrollClickOnText(key)
        self.dut.mbs.inputText(contact_details[key])
        self.dut.mbs.pressBack()
        time.sleep(1)
        if key == 'SIP':
          self.dut.mbs.clickOnText("Add customised field")
        time.sleep(1)
        self.dut.mbs.clickOnText("Save")
        time.sleep(1)
        self.dut.mbs.pressBack()

    def _unlock_screen(self):
      self.dut.mbs.inputKeyEvent(224)
      self.dut.mbs.inputKeyEvent(82)

    def _createContactLabel(self):

      self.dut.mbs.waitAndClickUsingResourceId("com.google.android.contacts:id/group_list")
      isLabelPresent = self.dut.mbs.assertElementByResID("com.google.android.contacts:id/checkbox")
      isLabelChecked = self.dut.mbs.isCheckboxChecked("com.google.android.contacts:id/checkbox")
      logging.info(isLabelPresent)
      logging.info(isLabelChecked)
      if isLabelPresent:
        logging.info("Label found")
        if isLabelChecked:
          logging.info("Label selected already")
          self.dut.mbs.clickOnText("Cancel")
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

    def _deleteContact(self, contact_name):
      time.sleep(1)
      self.dut.mbs.clickOnText(contact_name)
      #self.dut.mbs.waitAndClickUsingContentDesc(contacts_selectors.EDIT_BTN_DESC)
      time.sleep(1)
      self.dut.mbs.waitAndClickUsingContentDesc("More options")
      #self.dut.mbs.clickOnText("Delete")
      self.dut.mbs.clickOnText("Delete")
      self._assert_pop_up_text(contact_name)
      self.dut.mbs.clickOnText("DELETE")
      time.sleep(.5)

    def _assert_pop_up_text(self, contact_name):
      assert self.dut.mbs.assertTextDisplayed("Delete this contact?") is True, "Expected text not found on 'Delete' popup"
      txt = contact_name + " " + "will be removed from Google Contacts and all your synced devices"
      #assert self.dut.mbs.assertTextDisplayed(txt) is True, "Expected text not found on 'Delete' popup"
      assert self.dut.mbs.assertTextDisplayed("CANCEL") is True, "Expected text not found on 'Delete' popup"
      assert self.dut.mbs.assertTextDisplayed("DELETE") is True, "Expected text not found on 'Delete' popup"

    def _deletAllContacts(self):
      time.sleep(2)
      logging.info("Delete all contacts")
      self.dut.mbs.waitAndClickUsingContentDesc("More options")
      logging.info("Click on more options")
      self.dut.mbs.clickOnText("Select all")
      logging.info("Click on more select all")
      self.dut.mbs.waitAndClickUsingResourceId("com.google.android.contacts:id/menu_delete")
      logging.info("Click on menu option")
      self.dut.mbs.clickOnText("Delete")
      logging.info("Click on delete")

    def _setContactPhoto(self):
      time.sleep(1)
      logging.info("Adding contact photo")
      self.dut.mbs.waitAndClickUsingContentDesc("Add contact photo")
      self.dut.mbs.clickOnText("Take photo")
      time.sleep(2)
      self.dut.mbs.waitAndClickUsingContentDesc("Take photo")
      time.sleep(1)
      self.dut.mbs.waitAndClickUsingContentDesc("Done")
      self.dut.mbs.clickOnText("Done")
      time.sleep(1)

    def _press_input_key(self, key_event=None, count=None):
      if key_event is not None and count is not None:
        for c in range(count):
          self.dut.mbs.inputKeyEvent(key_event)
      else:
        logging.info("Please provide valid key event key and count")

    def _capture_screenshot(self, image_name):
      logging.info("Capturing screenshot...")
      self.dut.mbs.executeCommandOnDevice(" screencap -p /sdcard/" + image_name)
      cmd = "adb -s " + gTAF_config.CONTACT_APP_TEST_DEVICE_SERIAL + " pull /sdcard/" + image_name + " ."
      logging.info(cmd)
      os.system(cmd)
      self.dut.mbs.executeCommandOnDevice(" rm /sdcard/" + image_name)

    def _press_back(self, count):
      for c in range(count):
        self.dut.mbs.pressBack()

if __name__ == '__main__':
    test_runner.main()
