import pytest
from pathlib import Path
import sys
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from lib.registerbot import registerbot

#URLs
url_lancerpoint = "https://lancerpoint.pasadena.edu/"
url_register = "https://beis.pasadena.edu/ssomanager/c/SSB?pkg=bwskfreg.P_AltPin"

#Credentials
username = os.environ.get("username")
password = os.environ.get("password")

@pytest.fixture(scope="class")
def driver_init(request):
    browser = registerbot(headless=True)
    request.cls.driver = browser
    yield
    browser.browser.close()

@pytest.mark.usefixtures("driver_init")
class Chrome_Test:
    pass
class TestRegisterbot(Chrome_Test):
    def testOpenChrome(self):
        self.driver.browser.get('https://www.google.com')
        assert 'https://www.google.com/' == self.driver.browser.current_url, 'Browser is not working'

    @pytest.mark.skipif(username==None or password==None, reason="Unable to get credential from travis ci")
    def testLoggingin(self):
        self.driver.logging_in(username, password) #Should visit login site if it is not now
        assert self.driver.logged_in(), "Failed to Login"

    @pytest.mark.skipif(username==None or password==None, reason="Unable to get credential from travis ci")
    def testVisiting(self):
        assert len(self.driver.get_term()) >= 1, 'Unable to retrieve term'
        self.driver.select_term(self.driver.get_term()[0])
        # assert self.driver.isRegisterpage(), 'not heading to registration page'
    
    @pytest.mark.skipif(username==None or password==None, reason="Unable to get credential from travis ci")
    def testRegistering(self):
        self.driver.crn_writer([1, 2, 3, 4, 5])