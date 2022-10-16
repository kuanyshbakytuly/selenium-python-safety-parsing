import pymssql
import requests
import sqlalchemy as sql
import urllib3
import warnings
from time import sleep
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from fake_useragent import UserAgent
import re
import prediction

warnings.filterwarnings('ignore')
urllib3.disable_warnings()
pool_timeout = 30

headers = {}

user = ''
password = ''
server = ''
port = 1433
database = 'AZURE'
conn = sql.create_engine(url=f"mssql+pymssql://{user}:{password}@{server}:{port}/{database}", encoding='utf-8')


def recieveing_data_fromsql():
    quore = conn.execute(
        "select a.id from krisha_id as a left join krishaaa as b on a.id = b.id where b.id is NULL order by 1;")
    id_areas = []
    for i in quore:
        id_areas.append(str(i)[2:-3])
    return id_areas


def getting_meta_data():
    d = {}
    pattern_dtype = {
        'ID': sql.types.INTEGER,
        'Санузел': sql.types.NVARCHAR,
        'Интернет': sql.types.NVARCHAR,
        'Телефон': sql.types.NVARCHAR,
        'Балкон': sql.types.NVARCHAR,
        'Дверь': sql.types.NVARCHAR,
        'Парковка': sql.types.NVARCHAR,
        'Пол': sql.types.NVARCHAR,
        'Безопасность': sql.types.NVARCHAR,
        'Разное': sql.types.NVARCHAR,
        'ФИО': sql.types.NVARCHAR,
        'Контакты': sql.types.NVARCHAR,
        'Описание': sql.types.NVARCHAR,
        'Жилой комплекс': sql.types.NVARCHAR,
        'Плошадь': sql.types.NVARCHAR,
        'Количество комнат': sql.types.INTEGER,
        'Этаж': sql.types.NVARCHAR,
        'Состояние квартиры': sql.types.NVARCHAR,
        'Год постройки': sql.types.NVARCHAR,
        'Тип строение': sql.types.NVARCHAR,
        'Бывшее общежитие': sql.types.NVARCHAR,
        'Высота потолоков': sql.types.NVARCHAR,
        'Площадь, м²': sql.types.NVARCHAR,
        'Город': sql.types.NVARCHAR,
        'Состояние': sql.types.NVARCHAR,
        'Тип дома': sql.types.NVARCHAR,
        'Потолки': sql.types.NVARCHAR,
        'Возможен обмен': sql.types.NVARCHAR,
        'Балкон остеклён': sql.types.NVARCHAR
    }

    return pattern_dtype


dtype = getting_meta_data()

data_id = recieveing_data_fromsql()

ua = UserAgent(verify_ssl=False)
a = ua.random
user_agent = ua.random
ser = Service("/Users/kuanyshbakytuly/PycharmProjects/pythonProject4/chromedriver")
chrome_options = Options()
chrome_options.add_experimental_option('w3c', True)
'''chrome_options.add_argument(f'user-agent={user_agent}')'''
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(service=ser, options=chrome_options, desired_capabilities=d)


def checking(url):
    if requests.get(url).status_code == 404:
        return False


def getting_info(ID):
    d = {}
    info = element_info.split("\n")[2:]
    info.remove('показать на карте')
    for i in range(0, len(info), 2):
        d[info[i]] = info[i + 1]

    if element_name:
        pass
    else:
        d['ФИО'] = element_name

    if element_number:
        d['Контакты'] = ", ".join(element_number.split('\n'))

    if element_parameters:
        for i in range(len(element_parameters), 2):
            d[element_parameters[i]] = element_parameters[i + 1]

    if element_text:
        d['Описание'] = element_text.replace('\n', ' ')
    d['ID'] = ID
    return d

driver.get('https://krisha.kz')

try:
    driver.find_element(By.CLASS_NAME, 'popup-update-browser__close-icon').click()
except:
    pass

driver.maximize_window()
driver.implicitly_wait(5)
dtypee = getting_meta_data()

c = 0

for i in data_id:
    url = f'https://krisha.kz/a/show/{i}'
    print(checking(url))
    # checking our id have been activated yet
    if not checking(url) and len(i) == 8:

        driver.get(url)

        if not c:
            try:

                driver.find_element(By.XPATH,
                                    '/html/body/main/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/button').click()
                c += 1
            except:
                pass

            '''getting author's phone number'''
            try:
                driver.find_element(By.XPATH,
                                    '/html/body/main/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[3]/div/div/button').click()
                '''bypassing captcha with images or squares'''
                try:
                    driver.find_element((By.XPATH, '/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]')).click()
                    try:
                        captcha_condition = driver.find_element(By.XPATH,
                                                                 '/html/body/div/div/div[2]/div[1]/div[1]/div').text
                        if bool(re.match('Select all images with...', captcha_condition)):
                            captcha = prediction.Prediction_Images(driver)
                            captcha.resulta()
                        elif bool(re.match('Select all squares with...', captcha_condition)):
                            captcha = prediction.Prediction_speech(driver)
                            captcha.predicting()
                    except:
                        pass

                except:
                    pass
                sleep(1)
                element_number = driver.find_element(By.CLASS_NAME, "offer__contacts-phones").text
            except:
                element_number = None
                pass

            #getting the author's name
            try:
                element_name = driver.find_element(By.XPATH,
                                                   "/html/body/main/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[2]").text
            except:
                element_name = None
                pass

            element_title = driver.find_element(By.CLASS_NAME, "offer__advert-title").text
            element_info = driver.find_element(By.CLASS_NAME, "offer__advert-info").text
            element_parameters = driver.find_element(By.CLASS_NAME, "offer__parameters").text
            element_text = driver.find_element(By.CLASS_NAME, "text").text

            df = pd.DataFrame(columns=list(dtypee.keys()))
            dada = getting_info(ID=i)

            k = df.append(dada, ignore_index=True)
            k.to_sql('krishaaaa', con=conn, if_exists='append')

            print(a)
            print([i for i in dada.keys() if i not in dtypee.keys()])

            print(k)
            print(dtype.keys())

            print(f'success ---- {i}')
