from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import scanner
from telegram import Telegram

tg = Telegram()


options = webdriver.FirefoxOptions()
# options = webdriver.ChromeOptions()
# options.binary_location = './geckodriver'
# options.add_argument('--incognito')
# options.add_argument("disable-infobars")
options.add_argument('--headless') #Oculto
# options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# prefs = {"profile.managed_default_content_settings.images":2}
# options.headless = True
# options.add_experimental_option("prefs", prefs)

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

scanner.run(driver)