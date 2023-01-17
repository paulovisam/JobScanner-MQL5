from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import scanner

options = webdriver.FirefoxOptions()
options.add_argument('--incognito')
options.add_argument("disable-infobars")
options.add_argument('--headless') #Oculto
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
scanner.run(driver)