import time
import os
from datetime import datetime
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from telegram import TelegramBot
from database import Database
import logging

logging.getLogger()
db = Database()
tg = TelegramBot()
load_dotenv()
user = os.getenv('LOGIN')
senha = os.getenv('SENHA')
token = os.getenv('TOKEN')
timer = int(os.getenv('TIMER_SECONDS'))
id_chat = int(os.getenv('ID_CHAT'))
country = os.getenv('COUNTRY').lower()

def login(driver) -> bool:
    driver.get(f'https://www.mql5.com/{country}/auth_login')
    logging.info('Fazendo login...')
    time.sleep(3)
    try:
        username = driver.find_element(By.XPATH, '//*[@id="Login"]')
        username.send_keys(user)
    except Exception as erro:
        logging.error('Input login não encontrado - ', erro)
        return False
    try:
        password = driver.find_element(By.XPATH, '//*[@id="Password"]')
        password.send_keys(senha)
    except Exception as erro:
        logging.error('Input senha não encontrado - ', erro)
        return False
    password.send_keys(Keys.ENTER)
    time.sleep(3)
    return True

def isLogged(driver) -> bool:
    try:
        driver.get(f'https://www.mql5.com/{country}/job')
        time.sleep(3)
        user = driver.find_element(By.XPATH, '/html/body/div/header/div/div[1]/div[3]/div[1]/nav/ul/li/a').get_attribute('href')
        logging.info('Usuario logado!')
        return True
    except:
        logging.error('Não logado!')
        return False

def isMsg(driver, telegram) -> bool:
    # Notificação
    try:
        msg = driver.find_element(By.XPATH, '//*[@id="notify_jobs"]')
        link_msg = msg.get_attribute('href')
        telegram.send_message(f'*VOCÊ POSSUI UMA NOVA MENSAGEM*\n[Clique para visualizar]({link_msg})')
        logging.info(f'Nova mensagem!\n{link_msg}')
        return True
    except Exception as erro:
        logging.info('Sem novas mensagens')
        return False

def get_element_title_job(number: int):
    return f'/html/body/div[1]/main/article/div/div[2]/div[1]/div[4]/div[3]/div[{number}]/div[1]/a'

def get_element_desc_job(number: int):
    return f'/html/body/div[1]/main/article/div/div[2]/div[1]/div[4]/div[3]/div[{number}]/div[2]/div[1]/div[2]/div'

def jobs(driver):
    driver.get(f'https://www.mql5.com/{country}/job')
    time.sleep(3)
    job1 = None
    desc1 = None

    try:
        job1 = driver.find_element(By.XPATH, get_element_title_job(1))
        id1 = job1.get_attribute('href').replace(f'https://www.mql5.com/{country}/job/', '')
        job1 = job1.text
        desc1 = driver.find_element(By.XPATH, get_element_desc_job(1)).text
    except Exception as erro:
        id1 = None
        logging.error('Objeto job não encontrado -', str(erro))
    job2 = None
    desc2 = None
    try:
        job2 = driver.find_element(By.XPATH, get_element_title_job(2))
        id2 = job2.get_attribute('href').replace(f'https://www.mql5.com/{country}/job/', '')
        job2 = job2.text
        desc2 = driver.find_element(By.XPATH, get_element_desc_job(2)).text
    except Exception as erro:
        id2 = None
        logging.error('Objeto job não encontrado')
    job3 = None
    desc3 = None
    try:
        job3 = driver.find_element(By.XPATH, get_element_title_job(3))
        id3 = job3.get_attribute('href').replace(f'https://www.mql5.com/{country}/job/', '')
        job3 = job3.text
        desc3 = driver.find_element(By.XPATH, get_element_desc_job(3)).text
    except Exception as erro:
        id3 = None
        logging.error('Objeto job não encontrado')
    return [(id1, job1, desc1), (id2, job2, desc2), (id3, job3, desc3)]

def routing(driver, db, tg):
    isMsg(driver, tg)
    logging.info(datetime.now())
    id_jobs = db.get_all_id_jobs()
    consult_jobs = jobs(driver)
    if not consult_jobs:
        pass
    for i in range(len(consult_jobs)):
        if consult_jobs[i][0] != None and consult_jobs[i][1] != None and consult_jobs[i][2] != None:
            id = int(consult_jobs[i][0])
            if id in id_jobs:
                logging.info(f'Job {id} já cadastrado')
                pass
            else:
                logging.info(f'Novo job encontrado - {id}')
                title = consult_jobs[i][1]
                desc = consult_jobs[i][2]
                db.set_job(id, title, desc)
                tg.send_message(f'*{title}*\n\n{desc}\n[Clique para acessar](https://www.mql5.com/{country}/job/{id})')
        else:
            # Valor vazio
            logging.info(consult_jobs[i][0])
            logging.info(consult_jobs[i][1])
            logging.info(consult_jobs[i][2])
            pass

def run(driver):
    logging.info("Start script")
    ltime = datetime.now()
    ltime =  ltime.timestamp()
    while True:
        try:
            if datetime.now().timestamp() >= ltime:
                if isLogged(driver):
                    routing(driver, db, tg)
                else:
                    login(driver)
                    routing(driver, db, tg)
                ltime = datetime.now() + relativedelta(seconds=timer)
                ltime =  ltime.timestamp()
        except KeyboardInterrupt:
            break