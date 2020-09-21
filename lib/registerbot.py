from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pathlib import Path
import platform

class registerbot:
    '''
    Pasadena City College's Register Bot
    Made by Jaeyoung Cho / Travis Cho

    Attributes
    ----------
    headless: bool, optional


    Methods
    --------
    logging_in(*args)
        Logging in with credentials
    logged_in
        return whether user logged in or not
    crn_writer
        Automatically put crn and click submit
    get_term
        Get which term is available to apply
    select_term
        Select term in browser

    Note
    -----
    The program does not always detect the wrong crns.
    Do not change Dummy value in Json file
    '''
    def __init__(self, headless=False):
        '''Initializing

        Parameters
        -----------
        headless: bool, optional
            Open browser or work silently (Default: False)
        executable_path: string, optional
            File Location of ChromeDriver
        '''
        #PCC's URLs
        self._url_lancerpoint = "https://lancerpoint.pasadena.edu/"
        self._url_register = "https://beis.pasadena.edu/ssomanager/c/SSB?pkg=bwskfreg.P_AltPin"

        #Browser
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-gpu')
        if headless:
            chrome_options.add_argument('--headless')
        chrome_service = webdriver.chrome.service.Service(str(Path(__file__).parent) + '/driver/chromedriver')
        self._browser = webdriver.Chrome(options=chrome_options, service=chrome_service)


    @property
    def url_lancerpoint(self):return self._url_lancerpoint

    @property
    def url_register(self):
        return self._url_register

    @property
    def browser(self):
        return self._browser

    def logging_in(self, *args):
        '''Logging in with credentials

        Parameters
        ----------
        args: array, optional
            Username and Password
        '''
        if not self.logged_in():
            self.browser.get(self.url_lancerpoint)
        id_text = self.browser.find_element(By.ID, "username")
        pass_text = self.browser.find_element(By.ID, "password")
        try:
            id_text.send_keys(args[0])
            pass_text.send_keys(args[1])
            self.browser.find_element(By.XPATH, "//input[@value='Sign In']").click()
        except IndexError:
            print("Please Log in to your account and then press enter or provide credentials")
        except NoSuchElementException:
            raise("Unable to login\nCheck your network status or contact us")

    def logged_in(self):
        '''Check if user is logged in

        Returns bool
        ----------
        Whether User logged in or not
        '''
        return self.browser.current_url == self.url_lancerpoint
    
    def isRegisterpage(self):
        '''Check if user is in register page

        Returns bool
        ------------
        Whether User is in register page or not
        '''
        return self.browser.current_url == self.url_register 

    def crn_writer(self, crns):
        '''Write crns to the input field and click enter

        Parameters
        -----------
        CRNs: Array
            List of CRNs
        '''
        if not self.isRegisterpage():
            self.browser.get(self.url_register)

        self.browser.find_element(By.XPATH, "//input[@value='Submit']").click()
        xpath = ["//input[@ID='crn_id" + str(id) + "']" for id in range(1, 11)]
        count = 0

        for crn in crns:
            try:
                textbox = self.browser.find_element(By.XPATH, xpath[count])
                textbox.send_keys(str(crn))
                count += 1
            except NoSuchElementException:
                raise Exception("Unable to register")

        self.browser.find_element(By.XPATH, "//input[@value='Submit Changes']").click()


    def get_term(self):
        '''Get which terms are available to register

        Returns an array
        ----------
        Terms available to register
        '''
        if not self.isRegisterpage():
            self.browser.get(self.url_register)

        try:
            terms = self.browser.find_element(By.ID, "term_id")
            terms = terms.text.split('\n')
        except NoSuchElementException:
            raise Exception("Unable to retrive terms")

        return terms


    def select_term(self, term=None):
        '''Select terms and move to the next page

        Parameters
        ----------
        term: str
            Term to register
        '''
        if term is None:
            raise Exception("No term selected")
        if not self.isRegisterpage():
            self.browser.get(self.url_register)
        terms = self.browser.find_element(By.ID, "term_id")
        try:
            terms = terms.find_element(By.XPATH, "option[text()='"+term.lower().capitalize()+"']").click()
        except NoSuchElementException:
            raise Exception("Unable to find the following term")
