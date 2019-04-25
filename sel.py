from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import json
import csv

driver = webdriver.Firefox(executable_path='D:\selenium\geckodriver.exe')
driver.get("http://wishpost.wish.com/login")
elem = driver.find_element_by_name("username")
elem.send_keys("Account")
elem = driver.find_element_by_name("password")
elem.send_keys("passwor")
elem.send_keys(Keys.RETURN)
time.sleep(1)
cookies = driver.get_cookies()
driver.close()

cookie_s = ''
for i in cookies:
    cookie_s = cookie_s + i['name'] + '=' + i['value'] +';'
cookie_s = cookie_s[0:-1]

url = 'https://wishpost.wish.com/api/payment/get-cash-flow'
data = {}
data['endpoint'] = 'payment/get-cash-flow'
data['callback'] = 'renderCashFlowReport'
data['offset'] = '0'
data['count'] = '1000'
data['num_results'] = '0'
data['currency'] = 'CNY'
data['range'] = '30d'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
'Cookie':cookie_s}
rep = requests.post(url, data, headers = headers)
content = json.loads(rep.text)

data = content['data']
cash_flow_list = data['cash_flow_list']
with open('./transaction.csv', 'w') as f:
    writer = csv.writer(f)
    for i in cash_flow_list:
        writer.writerow(i.values())
