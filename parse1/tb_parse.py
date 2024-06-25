import json
import datetime
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

first_odd_week = datetime.date(2023,1,30)


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
      browser.quit()
      return -1
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
         return -1
   browser.quit()
   return current_url[current_url.find("group=")+6:]


def parse_tb_gr(gr_id, final_list):
   
   
   option=Options()
   option.add_argument('--headless')
   browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

   #url="https://sibsutis.ru/students/schedule/?type=student&group="+gr_id
   browser.get('https://sibsutis.ru/students/schedule/?type=student&group='+gr_id)

   browser.implicitly_wait(2)
   for i in range(10,23):#13,27

      str=''
      tmp = f'//*[@id="calendar"]/div[3]/a[{i}]'
      try:
         browser.find_element(by=By.XPATH, value=tmp).click()
      except:
         break
      browser.implicitly_wait(2)
      
      time_class = browser.find_element(by=By.CLASS_NAME, value='schedule__item')
      
      str = time_class.text
      i1 = str.find('08:00 - 09:35')+14
      i2 = str.find('09:50 - 11:25')+14
      i3 = str.find('11:40 - 13:15')+14
      i4 = str.find('13:45 - 15:20')+14
      i5 = str.find('15:35 - 17:10')+14
      i6 = str.find('17:25 - 19:00')+14
      i7 = str.find('19:00 - 20:35')+14
      #ii = str.find('\n', 14, i2)
      #print(str[i1:ii])
      #tmp_str = ''
      if(i2-i1 != 14):
         # словарь без типа занятия
         # tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': ''}
         
         # словарь с типа занятия
         tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': '', 'Тип занятия' : ''}
         
         tmp_dict['ВремяНачала']= f'{i-9}.01.0001 8:00:00'
         ii1 = str.find('\n', i1, i2-12)
         tmp_dict['Дисциплина']=str[i1:ii1]

         ii2 = str.find('\n', ii1+1, i2-12)
         tmp_dict['Тип занятия']=str[ii1+1:ii2]

         ii3 = str.find('\n', ii2+1, i2-12)
         tmp_dict['Группа']=str[ii2+1+7:ii3]

         ii4 = str.find('\n', ii3+1, i2-12)
         tmp_dict['ФизическоеЛицо']=str[ii3+1:ii4]

         ii5 = str.find('\n', ii4+1, i2-12)
         if(ii5 == -1):
            tmp_dict['Аудитория']='-'
         else:           
            tmp_dict['Аудитория']=str[ii4+1:ii5]
         final_list.append(tmp_dict)

      if(i3-i2 != 14):
         # словарь без типа занятия
         # tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': ''}
         
         # словарь с типа занятия
         tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': '', 'Тип занятия' : ''}

         tmp_dict['ВремяНачала']= f'{i-9}.01.0001 9:50:00'
         ii1 = str.find('\n',  i2, i3-12)
         tmp_dict['Дисциплина']=str[i2:ii1]

         ii2 = str.find('\n', ii1+1, i3-12)
         tmp_dict['Тип занятия']=str[ii1+1:ii2]

         ii3 = str.find('\n', ii2+1, i3-12)
         tmp_dict['Группа']=str[ii2+1+7:ii3]

         ii4 = str.find('\n', ii3+1, i3-12)
         tmp_dict['ФизическоеЛицо']=str[ii3+1:ii4]

         ii5 = str.find('\n', ii4+1, i3-12)
         if(ii5 == -1):
            tmp_dict['Аудитория']='-'
         else:           
            tmp_dict['Аудитория']=str[ii4+1:ii5]
         final_list.append(tmp_dict)
      

      if(i4-i3 != 14):
         # словарь без типа занятия
         # tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': ''}
         
         # словарь с типа занятия
         tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': '', 'Тип занятия' : ''}

         tmp_dict['ВремяНачала']= f'{i-9}.01.0001 11:40:00'
         ii1 = str.find('\n',  i3, i4-12)
         tmp_dict['Дисциплина']=str[i3:ii1]

         ii2 = str.find('\n', ii1+1, i4-12)
         tmp_dict['Тип занятия']=str[ii1+1:ii2]

         ii3 = str.find('\n', ii2+1, i4-12)
         tmp_dict['Группа']=str[ii2+1+7:ii3]

         ii4 = str.find('\n', ii3+1, i4-12)
         tmp_dict['ФизическоеЛицо']=str[ii3+1:ii4]

         ii5 = str.find('\n', ii4+1, i4-12)
         if(ii5 == -1):
            tmp_dict['Аудитория']='-'
         else:           
            tmp_dict['Аудитория']=str[ii4+1:ii5]
         final_list.append(tmp_dict)

      if(i5-i4 != 14):
         # словарь без типа занятия
         # tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': ''}
         
         # словарь с типа занятия
         tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': '', 'Тип занятия' : ''}

         tmp_dict['ВремяНачала']= f'{i-9}.01.0001 13:45:00'
         ii1 = str.find('\n',  i4, i5-12)
         tmp_dict['Дисциплина']=str[i4:ii1]

         ii2 = str.find('\n', ii1+1, i5-12)
         tmp_dict['Тип занятия']=str[ii1+1:ii2]

         ii3 = str.find('\n', ii2+1, i5-12)
         tmp_dict['Группа']=str[ii2+1+7:ii3]

         ii4 = str.find('\n', ii3+1, i5-12)
         tmp_dict['ФизическоеЛицо']=str[ii3+1:ii4]

         ii5 = str.find('\n', ii4+1, i5-12)
         if(ii5 == -1):
            tmp_dict['Аудитория']='-'
         else:           
            tmp_dict['Аудитория']=str[ii4+1:ii5]
         final_list.append(tmp_dict)

      if(i6-i5 != 14):
         # словарь без типа занятия
         # tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': ''}
         
         # словарь с типа занятия
         tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': '', 'Тип занятия' : ''}

         tmp_dict['ВремяНачала']= f'{i-9}.01.0001 15:35:00'
         ii1 = str.find('\n',  i5, i6-12)
         tmp_dict['Дисциплина']=str[i5:ii1]

         ii2 = str.find('\n', ii1+1, i6-12)
         tmp_dict['Тип занятия']=str[ii1+1:ii2]

         ii3 = str.find('\n', ii2+1, i6-12)
         tmp_dict['Группа']=str[ii2+1+7:ii3]

         ii4 = str.find('\n', ii3+1, i6-12)
         tmp_dict['ФизическоеЛицо']=str[ii3+1:ii4]

         ii5 = str.find('\n', ii4+1, i6-12)
         #tmp_dict['Аудитория']=str[ii4+1:ii5]
         if(ii5 == -1):
            tmp_dict['Аудитория']='-'
         else:           
            tmp_dict['Аудитория']=str[ii4+1:ii5]
         final_list.append(tmp_dict)

      if(i7-i6 != 14):
         # словарь без типа занятия
         # tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': ''}
         
         # словарь с типа занятия
         tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': '', 'Тип занятия' : ''}

         tmp_dict['ВремяНачала']= f'{i-9}.01.0001 17:25:00'
         ii1 = str.find('\n',  i6, i7-12)
         tmp_dict['Дисциплина']=str[i6:ii1]

         ii2 = str.find('\n', ii1+1, i7-12)
         tmp_dict['Тип занятия']=str[ii1+1:ii2]

         ii3 = str.find('\n', ii2+1, i7-12)
         tmp_dict['Группа']=str[ii2+1+7:ii3]

         ii4 = str.find('\n', ii3+1, i7-12)
         tmp_dict['ФизическоеЛицо']=str[ii3+1:ii4]

         ii5 = str.find('\n', ii4+1, i7-12)
         if(ii5 == -1):
            tmp_dict['Аудитория']='-'
         else:           
            tmp_dict['Аудитория']=str[ii4+1:ii5]
         final_list.append(tmp_dict)

      if(str.find('\n', i7) != -1):
         # словарь без типа занятия
         # tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': ''}
         
         # словарь с типа занятия
         tmp_dict = {'ВремяНачала': '', 'ДеньНедели': '', 'Неделя': '', 'Курс': '', 'Группа': '', 'ФизическоеЛицо': '', 'Аудитория': '', 'Дисциплина': '', 'Тип занятия' : ''}

         tmp_dict['ВремяНачала']= f'{i-9}.01.0001 19:00:00'
         ii1 = str.find('\n',  i7, len(str))
         tmp_dict['Дисциплина']=str[i7:ii1]

         ii2 = str.find('\n', ii1+1, len(str))
         tmp_dict['Тип занятия']=str[ii1+1:ii2]

         ii3 = str.find('\n', ii2+1, len(str))
         tmp_dict['Группа']=str[ii2+1+7:ii3]

         ii4 = str.find('\n', ii3+1, len(str))
         tmp_dict['ФизическоеЛицо']=str[ii3+1:ii4]
         ii5 = str.find('\n', ii4, len(str))
                 
         if(ii5 == -1):
            tmp_dict['Аудитория']='-'
         else:           
            tmp_dict['Аудитория']=str[ii4+1:len(str)]
         final_list.append(tmp_dict)
   
   return str


#поиск всех групп
def find_json(json_in):
   with open(json_in, 'r') as file:
      data = json.load(file)
   today_data = datetime.date.today()#datetime.date(2023,3,14)
   out_file =  open('out.txt', 'w') 
   list_gr = []
   for tmp in data:
      if tmp['Группа'].lower() in list_gr:
         continue
      list_gr.append(tmp['Группа'].lower())
   return list_gr

   out_file.close()

# final_list = []

# f= open("result_new2.json", 'a+')


# with open('result_new2.json') as json_file:
#     data = json.load(json_file)

# for d in data:
#    if(int(d['ВремяНачала'].partition('.')[0]) == 1 or int(d['ВремяНачала'].partition('.')[0]) == 8):
#       d['ДеньНедели']='Понедельник'
#    elif(int(d['ВремяНачала'].partition('.')[0]) == 2 or int(d['ВремяНачала'].partition('.')[0]) == 9):
#       d['ДеньНедели']='Вторник'
#    elif(int(d['ВремяНачала'].partition('.')[0]) == 3 or int(d['ВремяНачала'].partition('.')[0]) == 10):
#       d['ДеньНедели']='Вторник'
#    elif(int(d['ВремяНачала'].partition('.')[0]) == 4 or int(d['ВремяНачала'].partition('.')[0]) == 11):
#       d['ДеньНедели']='Вторник'
#    elif(int(d['ВремяНачала'].partition('.')[0]) == 5 or int(d['ВремяНачала'].partition('.')[0]) == 12):
#       d['ДеньНедели']='Вторник'
#    elif(int(d['ВремяНачала'].partition('.')[0]) == 6 or int(d['ВремяНачала'].partition('.')[0]) == 13):
#       d['ДеньНедели']='Вторник'

# data = json.dumps(data, ensure_ascii=False, indent=3)
# f.write(data)
# while True:
#    line = f.readline()
#    if not line:
#       break
#    parse_tb_gr(line, final_list)
#    print(line)



# js_list = json.dumps(final_list, ensure_ascii=False, indent=3)
# with open('result_new2.json', 'w') as res_file:
#    res_file.write(js_list)


# res_file.close()

# f.close()

# sss = '1.01.0001 8:00:00'
# sss = sss.replace('8:00:00', '8:00-9:35')
# print(sss)

import json

# Функция для определения дня недели на основе времени начала
def determine_weekday(time_start):
    # Извлекаем день месяца из времени начала
    day = int(time_start.split('.')[0])
    
    if day == 1 or day == 8:
        return "Понедельник"
    elif day == 2 or day == 9:
        return "Вторник"
    elif day == 3 or day == 10:
        return "Среда"
    elif day == 4 or day == 11:
        return "Четверг"
    elif day == 5 or day == 12:
        return "Пятница"
    elif day == 6 or day == 13:
        return "Суббота"
    else:
        return ""  # По умолчанию не определено


# Открываем JSON файл
json_file = 'result_new2.json'  # замените на путь к вашему JSON файлу

with open(json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Проходим по каждому элементу в списке
for item in data:
    # Получаем время начала
    time_start = item['ВремяНачала']
    # Определяем день недели
    weekday = determine_weekday(time_start)
    # Заменяем значение поля "ДеньНедели"
    item['ДеньНедели'] = weekday

# Перезаписываем файл с обновленными данными
with open(json_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Файл {json_file} успешно обновлен.")
