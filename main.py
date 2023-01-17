from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import scanner

options = webdriver.FirefoxOptions()
options.add_argument('--incognito')
options.add_argument("disable-infobars")
options.add_argument('--headless') #Oculto
options.add_argument("--disable-extensions")
options.add_argument('--disable-gpu')

driver = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
scanner.run(driver)