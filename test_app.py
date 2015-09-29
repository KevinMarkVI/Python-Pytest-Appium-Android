import os
import unittest
import sys
import new
from appium import webdriver
from sauceclient import SauceClient

browsers = [{
    'appiumVersion':    '1.4.11',
    'browserName':      '',
    'platformName':     'Android',
    'platformVersion':  '4.4',
    'deviceOrientation':'portrait',
    'deviceName':       'Samsung Galaxy S5 Device',
    'app':              'http://saucelabs.com/example_files/ContactManager.apk'
}]

username = os.environ['SAUCE_USERNAME']
access_key = os.environ['SAUCE_ACCESS_KEY']

# This decorator is required to iterate over browsers
def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)
    return decorator

@on_platforms(browsers)
class FirstSampleTest(unittest.TestCase):

    # setUp runs before each test case
    def setUp(self):
        self.desired_capabilities['name'] = self.id()
        self.driver = webdriver.Remote(
           command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (username, access_key),
           desired_capabilities=self.desired_capabilities)

    # click to make a new note in the app
    def test_note(self):
        addContactButton = self.driver.find_element_by_name("Add Contact")
        addContactButton.click()
        textFieldsList = self.driver.find_elements_by_class_name("android.widget.EditText")
        textFieldsList[0].send_keys("Some Name")
        textFieldsList[2].send_keys("Some@example.com")
        self.driver.find_element_by_name("Save").click()

    # tearDown runs after each test case
    def tearDown(self):
        self.driver.quit()
        sauce_client = SauceClient(username, access_key)
        status = (sys.exc_info() == (None, None, None))
        sauce_client.jobs.update_job(self.driver.session_id, passed=status)
