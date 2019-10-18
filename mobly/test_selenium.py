from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import web_page_selectors
from selenium.webdriver.chrome.options import Options
from mobly import base_test
from mobly import test_runner
from mobly.controllers import android_device
import time
from collections import OrderedDict
import logging

class Browser(base_test.BaseTestClass):

    def setup_class(self):
        logging.info("Gmail login test execution ")
        # Registering android_device controller module declares the test's
        # dependency on Android device hardware. By default, we expect at
        # least one object is created from this.
        #self.ads = self.register_controller(android_device)
        #self.dut = self.ads[0]
        # Start Mobly Bundled Snippets (MBS).
        # self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.bundled')
        #self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.example4')

    def test_gmail_login(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(executable_path=r'/usr/local/bin/chromedriver',chrome_options=chrome_options)
        logging.info("Initializing drivers.")
        driver.maximize_window()
        time.sleep(5)
        logging.info("Launching gmail web page")
        driver.get(web_page_selectors.GMAIL_URL)
        logging.info("Web page launched %s", web_page_selectors.GMAIL_URL)
        time.sleep(10)
        logging.info("Entering login details")
        try:
            element = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, web_page_selectors.GMAIL_USERNAME_CSS_SELECTOR)))
        except:
            logging.info("Quit")
        driver.find_element_by_css_selector(web_page_selectors.GMAIL_USERNAME_CSS_SELECTOR).send_keys(web_page_selectors.GMAIL_ID)
        time.sleep(2)
        driver.find_element_by_css_selector(web_page_selectors.UNAME_NEXT_BUTTON_CSS_SELECTOR).click()
        time.sleep(2)
        driver.find_element_by_xpath(web_page_selectors.GMAIL_PASSWORD_XPATH).send_keys(web_page_selectors.GMAIL_PASSWORD)
        time.sleep(2)
        logging.info("Click on login")
        driver.find_element_by_css_selector(web_page_selectors.PASSWORD_NEXT_BUTTON_CSS_SELECTOR).click()
        time.sleep(5)
        url = driver.current_url
        title = driver.title
        logging.info("Current web page url %s", url)
        logging.info("Current web page title %s", title)
        assert "https://mail.google.com/mail/#inbox" in url , "Failed, invalid url found"
        assert "Gmail" in title, "Failed, invalid web page title found"
        logging.info("Closing web page")
        driver.close()

if __name__ == '__main__':
    test_runner.main()
