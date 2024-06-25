from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import undetected_chromedriver
from bs4 import BeautifulSoup
import requests

def parse_gr_id(gr_name):
   option=Options()
   option.add_argument('--headless')
   browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

   browser.get('https://sibsutis.ru/students/schedule/?type=student')

   browser.find_element(by=By.ID, value='group_select').click()
   browser.find_element(by=By.CLASS_NAME, value='select2-search__field').send_keys(gr_name)

   browser.implicitly_wait(2)
   check_res = browser.find_element(by=By.CLASS_NAME, value='select2-results__options')
   if check_res.text == "": #проверяем что результаты поиска существуют
      print("сайт не выдал результаты поиска")
   else:
      #print("not null")
      group = browser.find_element(by=By.CLASS_NAME, value='select2-results__option--highlighted')
      if group.text.lower() == gr_name:
         #print("группа " + group.text + " найдена")
         group.click()
         current_url = browser.current_url
         print("id_gr = "+ current_url[current_url.find("group=")+6:])
      else:
         print("группа: "+ gr_name + "  не найдена на сате sibsutis")
   browser.quit()
   return current_url[current_url.find("group=")+6:]

def parse_tb_gr(gr_id):
   option=Options()
   option.add_argument('--headless')
   browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

   #url="https://sibsutis.ru/students/schedule/?type=student&group="+gr_id
   browser.get('https://sibsutis.ru/students/schedule/?type=student&group='+gr_id)

   browser.implicitly_wait(2)
   time_class = browser.find_element(by=By.CLASS_NAME, value='schedule__item')
   str = time_class.text
   return str

def parse_tb_bs4(gr_id):
   page = requests.get('https://sibsutis.ru/students/schedule/?type=student&group=2330310')
   soup = BeautifulSoup(page.text)
   tb = soup.find("div", class_="schedule__item")
   print(tb)


# start_time = time.time()
# parse_tb_bs4("2330310")
# print("--- %s seconds ---" % (time.time() - start_time))
'''   
start_time = time.time()

option=Options()
#option.headless = True
option.add_argument('--headless')
#option.add_argument(f"user-agent={UserAgent().random}")
#option.add_argument('--disable-blink-features=AutomationControlled')

#browser = undetected_chromedriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

browser.get('https://sibsutis.ru/students/schedule/?type=student')

search_group = 'ип-012'

browser.find_element(by=By.ID, value='group_select').click()
browser.find_element(by=By.CLASS_NAME, value='select2-search__field').send_keys(search_group)

#browser.find_element("xpath", '/html/body/div[3]/div[1]/div[2]/span/span[1]/span/span[1]/span').click()
#browser.find_element("xpath", '/html/body/span/span/span[1]/input').send_keys(search_group)
#time.sleep(2)
browser.implicitly_wait(2)
check_res = browser.find_element(by=By.CLASS_NAME, value='select2-results__options')
if check_res.text == "": #проверяем что результаты поиска существуют
    print("сайт не выдал результаты поиска")
else:
   #print("not null")
   group = browser.find_element(by=By.CLASS_NAME, value='select2-results__option--highlighted')
   if group.text.lower() == search_group:
      print("группа " + group.text + " найдена")
      group.click()
      current_url = browser.current_url
      #print(browser.current_url
      #тут нужен парсинг расписания
      
      # browser.get(current_url)
      # browser.implicitly_wait(2)
      # time_class = browser.find_element(by=By.CLASS_NAME, value='schedule__item')
      # str = time_class.text
      # print(str)
      
   else:
      print("группа: "+ search_group + "  не найдена на сате sibsutis")

browser.quit()
print("--- %s seconds ---" % (time.time() - start_time))
'''