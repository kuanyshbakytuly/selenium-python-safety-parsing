import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from fake_useragent import UserAgent
import pymssql
import sqlalchemy as sql
import urllib3
import warnings
from time import sleep

warnings.filterwarnings('ignore')
urllib3.disable_warnings()
pool_timeout = 30

def pd_show():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)


headers = '{...}'. #too privacy

user = 'SA'
password = 'reallyStrongPwd123'
server = '127.0.0.1'
port = 1433
database = 'AZURE'
conn = sql.create_engine(url=f"mssql+pymssql://{user}:{password}@{server}:{port}/{database}", encoding='utf-8')


ua = UserAgent(verify_ssl=False)
a = ua.random
user_agent = ua.random
ser = Service("chromedriver")
chrome_options = Options()
chrome_options.add_experimental_option('w3c', True)
chrome_options.add_argument(f'user-agent={user_agent}')
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'performance':'ALL' }
driver = webdriver.Chrome(service=ser, options=chrome_options, desired_capabilities=d)



url = f'https://krisha.kz/map/prodazha/kvartiry/astana-almatinskij/?lat=51.096377&lon=71.594986&zoom=19'
driver.get(url)
print(url)
driver.maximize_window()
driver.implicitly_wait(5)
yandex = '/html/body/main/div/div[1]/ymaps/ymaps/ymaps/ymaps[4]/ymaps[2]/ymaps[2]/div/a[2]'
el = driver.find_element(By.XPATH, yandex)
el.click()





def getting_site():
    data = driver.get_log('performance')
    for i in data:
        if isinstance(i, dict):
            if "https://krisha.kz/ms/views/krisha/live/" in i['message']:
                ID = i['message'].split('https://krisha.kz/ms/views/krisha/live/')[1].split('/"}')[0].split(',')
                print(ID)
                df = pd.DataFrame(ID)
                df.to_sql('krisha_id', con=conn, if_exists='append')
    driver.get_log('browser')



d = {'size_y': (51.115680, 51.225042), 'size_x': (71.389659, 71.594986)}
range_y = int((d['size_y'][1] - d['size_y'][0]) // 0.001091)
range_x = int((d['size_x'][1] - d['size_x'][0]) // 0.002219)

element = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/ymaps/ymaps/ymaps/ymaps[1]')

c = 0

for i in range(range_y):
    for j in range(range_x):
        c += 1
        print(f'{c} ---- {getting_site()}')
        ActionChains(driver).drag_and_drop_by_offset(element, 833, 0).perform()
        sleep(3)
    ActionChains(driver).drag_and_drop_by_offset(element, 0, -213).perform()
    ActionChains(driver).drag_and_drop_by_offset(element, 0, -213).perform()
    ActionChains(driver).drag_and_drop_by_offset(element, 0, -213).perform()


