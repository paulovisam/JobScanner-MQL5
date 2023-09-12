from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import scanner


options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument("disable-infobars")
options.add_argument('--headless') #Oculto
options.add_argument("--no-sandbox")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-dev-shm-usage")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
prefs = {"profile.managed_default_content_settings.images":2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=Service(), options=options)

scanner.run(driver)