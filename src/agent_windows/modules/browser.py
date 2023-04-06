import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

class Browser():
    """ Main class for browsing websites using chrome """
    def __init__(self):
        print('Class:Browser Initialized')
        # Set custom flags to ignore SSL errors if timestamp is wrong
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--ignore-ssl-errors")
        self.options.add_argument("--ignore-certificate-errors-spki-list")
        
        # Disable popups, notifications and hwaccel
        self.options.add_argument("disable-popup-blocking")
        self.options.add_argument('--disable-blink-features=AutomationControlled') # helps mitigate bot detection 
        self.options.add_argument("disable-notifications")
        self.options.add_argument("disable-gpu")  # disable hw acceleration

        # Supress logging of various I/O units in Chrome
        self.options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])

        # Create driver for Chrome (can be created for Firefox if desired )

    
    def browse_url(self, url):
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=self.options)
        """ Function for browsing a specific webpage """
        self.driver.get(url)
        time.sleep(7)
        driver.close()

    def search_google(self, query):
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=self.options)
        
        """ Function for searching google """
        print("Searching google for: " + query)
        driver.get("https://www.google.no")

        # New browser, have to accept ToC
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "L2AGLb")))
        except:
            print('No ToC found')
            driver.close()
        else:
          driver.find_element(By.ID, "L2AGLb").click()

          # REALISM: Sleep for a random time before typing and searching
          time.sleep(random.randint(1, 5))

          # Find search box, type in query and enter.
          search = driver.find_element(by=By.NAME, value="q")
          search.send_keys(query)
          search.send_keys(Keys.RETURN)
          time.sleep(2)
          
          # REALISM: Consider moving to one of the next 2 pages
          page = random.randint(1, 3)
          current_page = 1
          print("Getting page: " + str(page))
          # Click next page until we reach the page we want to be on
          while current_page < page:
              try:
                next_button = driver.find_element(
                    by=By.XPATH, value="//*[contains(local-name(), 'span') and \ncontains(text(), 'Neste')]")
              except:
                print('failed, move on')
                current_page = current_page+1
              else:
                current_page = current_page+1
                next_button.click()
              
          
          # Wait until results are visible and gather the resutls on the page
          # error thrown here on dragon once
          try:
              WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='yuRUbf']/a")))  
          except:
              print('No results found')
              time.sleep(2)#
              driver.close()
          else:
            results = driver.find_elements(by=By.XPATH, value="//div[@class='yuRUbf']/a")  # finds webresults  
                    
            # REALISM: Sleep for a random time before clicking on a link
            time.sleep(random.randint(1, 5))
            
            # REALISM: 80% chance of clicking a link
            if random.randint(1, 10) <= 8:
                print("Link clicked")
                # clicks on a random result
                res_click = random.randint(0,len(results)-1)
                try:
                  results[res_click].click()
                except:
                  print('failed to click link, move on')
            else:
                print("No link clicked")
                
            time.sleep(2)#
            driver.close()


if __name__ == '__main__':
    browser = Browser()
    browser.search_google("how to slay a dragon")