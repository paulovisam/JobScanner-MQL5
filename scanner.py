import time
import os
from datetime import datetime
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from telegram import Telegram
from database import Database

db = Database()
tg = Telegram()
load_dotenv()
user = os.getenv('LOGIN')
senha = os.getenv('SENHA')
token = os.getenv('TOKEN')
timer = int(os.getenv('TIMER_SECONDS'))
id_chat = int(os.getenv('ID_CHAT'))

def login(driver) -> bool:
    driver.get('https://www.mql5.com/pt/auth_login')
    print('Fazendo login...')
    time.sleep(3)
    try:
        username = driver.find_element(By.XPATH, '//*[@id="Login"]')
        username.send_keys(user)
    except Exception as erro:
        print('Input login não encontrado - ', erro)
        return False
    try:
        password = driver.find_element(By.XPATH, '//*[@id="Password"]')
        password.send_keys(senha)
    except Exception as erro:
        print('Input senha não encontrado - ', erro)
        return False
    password.send_keys(Keys.ENTER)
    time.sleep(3)
    return True

def isLogged(driver) -> bool:
    try:
        driver.get('https://www.mql5.com/pt/job')
        time.sleep(3)
        user = driver.find_element(By.XPATH, '/html/body/div/header/div/div[1]/div[3]/div[1]/nav/ul/li/a').get_attribute('href')
        print('Usuario logado!')
        return True
    except:
        print('Não logado!')
        return False

def isMsg(driver, telegram) -> bool:
    # Notificação
    try:
        msg = driver.find_element(By.XPATH, '//*[@id="notify_jobs"]')
        link_msg = msg.get_attribute('href')
        telegram.sender(f'*VOCÊ POSSUI UMA NOVA MENSAGEM*\n\n{link_msg}', id_chat)
        print(f'Nova mensagem!\n{link_msg}')
        return True
    except Exception as erro:
        print('Sem novas mensagens')
        return False

def jobs(driver):
    driver.get('https://www.mql5.com/pt/job')
    time.sleep(3)
    job1 = None
    desc1 = None
    try:
        job1 = driver.find_element(By.XPATH, '/html/body/div/main/article/div/div/div[2]/div[1]/div[4]/div[3]/div[1]/div[1]/a')
        id1 = job1.get_attribute('href').replace('https://www.mql5.com/pt/job/', '')
        job1 = job1.text
        desc1 = driver.find_element(By.XPATH, '/html/body/div[1]/main/article/div/div/div[2]/div[1]/div[4]/div[3]/div[1]/div[2]/div[1]/div[2]/div').text
    except Exception as erro:
        id1 = None
        print('Objeto job não encontrado')
    job2 = None
    desc2 = None
    try:
        job2 = driver.find_element(By.XPATH, '/html/body/div/main/article/div/div/div[2]/div[1]/div[4]/div[3]/div[2]/div[1]/a')
        id2 = job2.get_attribute('href').replace('https://www.mql5.com/pt/job/', '')
        job2 = job2.text
        desc2 = driver.find_element(By.XPATH, '/html/body/div[1]/main/article/div/div/div[2]/div[1]/div[4]/div[3]/div[2]/div[2]/div[1]/div[2]/div').text
    except Exception as erro:
        id2 = None
        print('Objeto job não encontrado')
    job3 = None
    desc3 = None
    try:
        job3 = driver.find_element(By.XPATH, '/html/body/div/main/article/div/div/div[2]/div[1]/div[4]/div[3]/div[3]/div[1]/a')
        id3 = job3.get_attribute('href').replace('https://www.mql5.com/pt/job/', '')
        job3 = job3.text
        desc3 = driver.find_element(By.XPATH, '/html/body/div[1]/main/article/div/div/div[2]/div[1]/div[4]/div[3]/div[3]/div[2]/div[1]/div[2]/div').text
    except Exception as erro:
        id3 = None
        print('Objeto job não encontrado')
    return [(id1, job1, desc1), (id2, job2, desc2), (id3, job3, desc3)]

def routing(driver, db, tg):
    isMsg(driver, tg)
    print(datetime.now())
    id_jobs = db.get_all_id_jobs()
    consult_jobs = jobs(driver)
    for i in range(len(consult_jobs)):
        if consult_jobs[i][0] != None and consult_jobs[i][1] != None and consult_jobs[i][2] != None:
            id = int(consult_jobs[i][0])
            if id in id_jobs:
                print(f'Job {id} já cadastrado')
                pass
            else:
                print(f'Novo job encontrado - {id}')
                title = consult_jobs[i][1]
                desc = consult_jobs[i][2]
                db.set_job(id, title, desc)
                tg.sender(f'*{title}*\n\nhttps://www.mql5.com/pt/job/{id}', id_chat)
        else:
            # Valor vazio
            print(consult_jobs[i][0])
            print(consult_jobs[i][1])
            print(consult_jobs[i][2])
            pass
    print('\n')

def run(driver):
    ltime = datetime.now()
    ltime =  ltime.timestamp()
    while True:
        if datetime.now().timestamp() >= ltime:
            if isLogged(driver):
                routing(driver, db, tg)
            else:
                login(driver)
                routing(driver, db, tg)
            ltime = datetime.now() + relativedelta(seconds=timer)
            ltime =  ltime.timestamp()