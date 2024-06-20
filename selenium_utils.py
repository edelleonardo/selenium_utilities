from selenium import webdriver

import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class SeleniumUtils():
    def __init__(self, browser, output_location, headless_mode = False):
        self.driver = self.create_driver(browser, output_location, headless_mode)
        self.action_chains = self.create_action_chains(self.driver)

    def create_driver(self, browser, output_location, headless_mode):

        os.environ['WDM_LOG_LEVEL'] = '0'

        if browser == 'EDGE':
            edge_options = webdriver.EdgeOptions()
            edge_options.add_experimental_option("prefs", {
                "download.default_directory": f"{output_location}",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False,
            })
        
            if headless_mode == True:
                edge_options.add_argument("--headless=new")

            return webdriver.Edge(options=edge_options)
        
        elif browser == 'CHROME':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("prefs", {
                "download.default_directory": f"{output_location}",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False,
                
            })

            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--log-level=3")
            #chrome_options.add_argument("--no-sandbox")

            #chrome_options.add_experimental_option("debuggerAddress", "localhost:8989")
        
            if headless_mode == True:
                chrome_options.add_argument("--headless=new")

            return webdriver.Chrome(options=chrome_options)
        
    def create_action_chains(self, driver):
        return ActionChains(driver)
    
    def click_by_xpath(self, xpath_string, issingle, wait):
        driver = self.driver
        action_chains = self.action_chains

        if wait:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath_string)))

        button = driver.find_element(By.XPATH, xpath_string)

        if issingle == "single":
            action_chains.click(button).perform()
        else:
            action_chains.double_click(button).perform()

        time.sleep(2)

    def simulate_keystrokes(self, key, xpath):
        action_chains = self.action_chains
        action_chains.send_keys(key)

    def is_exist(self, xpath_string):
        driver = self.driver

        if len(driver.find_elements(By.XPATH, xpath_string)) == 1:
            return True
       
        return False
    
    def accept_alert(self):
        driver = self.driver

        WebDriverWait(driver, 20).until(EC.alert_is_present())
        
        driver.switch_to.alert.accept()

    def set_text(self, xpath_string, value, wait):
        driver = self.driver

        if wait:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,xpath_string)))
                                            
        input_element = driver.find_element(By.XPATH,xpath_string)
        input_element.clear()
        input_element.send_keys(value)
        input_element.send_keys(Keys.ENTER)

        time.sleep(2)

    def get_element(self, xpath_string):
        driver = self.driver
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,xpath_string)))
        element = driver.find_element(By.XPATH,xpath_string)
        return element


        
    