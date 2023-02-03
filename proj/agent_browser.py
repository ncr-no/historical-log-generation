import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


# Set path for chromedriver
PATH = "C:\Program Files (x86)\chromedriver.exe"


class BrowseWebsite():
    """ Main class for browsing websites using chrome """

    def __init__(self, driver):
        # Set custom flags to ignore SSL errors if timestamp is wrong
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--ignore-certificate-errors-spki-list")

        # Disable popups, notifications and hwaccel
        options.add_argument("disable-popup-blocking")
        options.add_argument('--disable-blink-features=AutomationControlled') # helps mitigate bot detection 
        options.add_argument("disable-notifications")
        options.add_argument("disable-gpu")  # disable hw acceleration

        # Supress logging of various I/O units in Chrome
        options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])

        # Create driver for Chrome (can be created for Firefox if desired )
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        self.driver = driver

    # Function for browsing a website, and clicking random href after random delay
    def browse_url(self, url):
        """ Function for browsing a specific webpage """
        self.driver.get(url)

    def search_google(self, query):
        """ Function for searching google """
        print("Searching google for: " + query)
        
        self.driver.get("https://www.google.com")

        # New browser, have to accept ToC
        self.driver.find_element(By.ID, "L2AGLb").click()

        # REALISM: Sleep for a random time before typing and searching
        time.sleep(random.randint(1, 5))

        # Find search box, type in query and enter.
        search = self.driver.find_element(by=By.NAME, value="q")
        search.send_keys(query)
        search.send_keys(Keys.RETURN)
        time.sleep(2)
        
        # REALISM: Consider moving to one of the next 2 pages
        page = random.randint(1, 3)
        current_page = 1
        print("Getting page: " + str(page))
        # Click next page until we reach the page we want to be on
        while current_page < page:
            next_button = self.driver.find_element(
                by=By.XPATH, value="//*[contains(local-name(), 'span') and contains(text(), 'Neste')]")
            next_button.click()
            current_page = current_page+1
        
        # Wait until results are visible and gather them
        WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='yuRUbf']/a")))
        results = self.driver.find_elements(by=By.XPATH, value="//div[@class='yuRUbf']/a")  # finds webresults  
                
        # REALISM: Sleep for a random time before clicking on a link
        time.sleep(random.randint(1, 5))
        
        # REALISM: 80% chance of clicking a link
        if random.randint(1, 10) <= 8:
            print("Link clicked")
            # clicks on a random result
            res_click = random.randint(0,len(results)-1)
            results[res_click].click()
        else:
            print("No link clicked")
        time.sleep(2)
        self.driver.quit()


if __name__ == '__main__':
    browser = BrowseWebsite(driver=webdriver)
    browser.search_google("kakeoppskrift")
