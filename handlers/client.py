from keyboards import kb_client
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from data_base import sqlite_db
from datetime import datetime
import json
import datetime
from handlers import my_schedulers
from weather import get_weather
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

first_odd_week = datetime.date(2023,1,30) #первая нечетная неделя
name_json = 'timetable.json'

router = Router()

#класс для машины состояний
class FSMClient(StatesGroup):
   gr = State()
   notif = State()

@router.message(Command('start'))
async def command_start(message : Message,
                     state : FSMContext):
    await state.set_state(FSMClient.gr)

    await message.answer('Введите группу')
    my_schedulers.schedule_jobs()

#выход из состояний
@router.message(FSMClient.gr, Command(commands=["cancel"]))
@router.message(FSMClient.gr, F.text.lower() == "отмена")
async def cancel_handler(message: Message, state: FSMContext):
   current_state = await state.get_state()
   if current_state is None:
      return
   await state.clear()
   await message.reply('OK')

@router.message(FSMClient.gr, F.text)
async def load_gr(message: Message, state: FSMContext):
    data = {}
    data['id_user'] = message.from_user.id
    data['gr_name'] = message.text.lower()
    print(data)
    print("\n\n\n\n\n")
    await sqlite_db.sql_add_command(message)
    await message.answer('Выбери действие', reply_markup=kb_client)
    await state.clear()

@router.message(Command('help'))
async def command_help(message : Message):
    await message.answer("Данный бот создан для работы с расписанием в СИБГУТИ \n По вопросам пишите @alleksandr152", reply_markup=kb_client)

#Редактирование списка с расписанием для отправки сообщения
async def edit_list(old_list):
    new_list = []
    for old in old_list:
        if (old['ВремяНачала'].partition(' ')[2][:-3] == '8:00'):
            old['ВремяНачала'] = old['ВремяНачала'].replace('8:00:00', '🕰8:00 - 9:35') 
        elif (old['ВремяНачала'].partition(' ')[2][:-3] == '9:50'):
            old['ВремяНачала'] = old['ВремяНачала'].replace('9:50:00','🕰9:50 - 11:25')
        elif (old['ВремяНачала'].partition(' ')[2][:-3] == '11:40'):
            old['ВремяНачала'] = old['ВремяНачала'].replace('11:40:00','🕰11:40 - 13:15') 
        elif (old['ВремяНачала'].partition(' ')[2][:-3] == '13:45'):
            old['ВремяНачала'] = old['ВремяНачала'].replace('13:45:00','🕰13:45 - 15:20') 
        elif (old['ВремяНачала'].partition(' ')[2][:-3] == '15:35'):
            old['ВремяНачала'] = old['ВремяНачала'].replace('15:35:00','🕰15:35 - 17:10') 
        elif (old['ВремяНачала'].partition(' ')[2][:-3] == '17:25'):
            old['ВремяНачала'] = old['ВремяНачала'].replace('17:25:00', '🕰17:25 - 19:00') 
        elif (old['ВремяНачала'].partition(' ')[2][:-3] == '19:00'):
            old['ВремяНачала'] = old['ВремяНачала'].replace('19:00:00','🕰19:00 - 20:30') 
        
        old['Аудитория'] = '🚪'+old['Аудитория']
        old['ФизическоеЛицо'] = '🎓' + old['ФизическоеЛицо'] 
        old['Дисциплина'] = '✏️' + old['Дисциплина']

        if (old['Тип занятия'] == 'Практические занятия'):
            old['Тип занятия'] = 'Практическое занятие'
        elif (old['Тип занятия'] == 'Лекционные занятия'):
            old['Тип занятия'] = 'Лекционное занятие'
        elif (old['Тип занятия'] == 'Лекционные занятия'):
            old['Тип занятия'] = 'Лекционное занятие'
        new_list.append(old)
    return new_list

#функция для поиска рассписания на сегодня в json
async def find_today_json(gr_name, json_name):
    with open(json_name, 'r') as file:
        data = json.load(file)
    today_data = datetime.date.today()
    list_today = []
    for tmp in data:
        if (tmp['Группа'].lower() == gr_name.lower() and int(tmp['ВремяНачала'].partition('.')[0]) == ((((today_data-first_odd_week).days)%14)+1)):
            list_today.append(tmp)

    list_today = sorted(list_today, key=lambda d: int(d['ВремяНачала'].partition(' ')[2].partition(':')[0]))
    list_today = await edit_list(list_today)
    return list_today

@router.message(F.text.lower() == 'сегодня')
async def today_tb(message : Message):
    gr_name = await sqlite_db.sql_find_gr_name(message)
    list_classes = await find_today_json(gr_name,name_json)

    if list_classes == []:
        await message.answer('Нет пар!!!')
        return
    str_out = ''
    str_out += list_classes[0]['ДеньНедели']+'\n\n'
    for tmp in list_classes:
        str_out += tmp['Тип занятия']+'\n'+tmp['ВремяНачала'].partition(' ')[2]+'\n'+tmp['Дисциплина']+'\n'+tmp['ФизическоеЛицо']+'\n'+tmp['Аудитория']+'\n\n'
    
    await message.answer(str_out)
    

#функция для поиска рассписания на завтра в json
async def find_tomorrow_json(gr_name, json_name):
    with open(json_name, 'r') as file:
        data = json.load(file)
    today_data = datetime.date.today()
    list_tomorrow = []
    for tmp in data:
        if (tmp['Группа'].lower() == gr_name.lower() and int(tmp['ВремяНачала'].partition('.')[0]) == ((((today_data-first_odd_week).days)%14)+2)):
            list_tomorrow.append(tmp)

    list_tomorrow =sorted(list_tomorrow, key=lambda d: int(d['ВремяНачала'].partition(' ')[2].partition(':')[0])) 
    list_tomorrow = await edit_list(list_tomorrow)
    return list_tomorrow

@router.message(F.text.lower() == 'завтра')
async def tomorrow_tb(message : Message):
    gr_name = await sqlite_db.sql_find_gr_name(message)
    list_classes = await find_tomorrow_json(gr_name,name_json)
    if list_classes == []:
        await message.answer('Нет пар!!!')
        return
    str_out = ''
    str_out += list_classes[0]['ДеньНедели']+'\n\n'
    for tmp in list_classes:
        str_out += tmp['Тип занятия']+'\n'+tmp['ВремяНачала'].partition(' ')[2]+'\n'+tmp['Дисциплина']+'\n'+tmp['ФизическоеЛицо']+'\n'+tmp['Аудитория']+'\n\n'
    await message.answer(str_out)

#функция для поиска рассписания на неделю в json
async def find_week_json(gr_name, json_name):
    with open(json_name, 'r') as file:
        data = json.load(file)
    today_data = datetime.date.today()
    list_week = []

    if ((((today_data-first_odd_week).days)%14)+1) < 7 :
        for tmp_day in range(1, 7):
             list_today = []
             for tmp in data:
                if (tmp['Группа'].lower() == gr_name.lower() and int(tmp['ВремяНачала'].partition('.')[0]) == tmp_day):
                    list_today.append(tmp)
             list_today = sorted(list_today, key=lambda d: int(d['ВремяНачала'].partition(' ')[2].partition(':')[0]))
             list_today = await edit_list(list_today)
             list_week.append(list_today)
    else:
        for tmp_day in range(8, 14):
             list_today = []
             for tmp in data:
                if (tmp['Группа'].lower() == gr_name.lower() and int(tmp['ВремяНачала'].partition('.')[0]) == tmp_day):
                    list_today.append(tmp)
             list_today = sorted(list_today, key=lambda d: int(d['ВремяНачала'].partition(' ')[2].partition(':')[0]))
             list_today = await edit_list(list_today)
             list_week.append(list_today)
    return list_week

@router.message(F.text.lower() == 'неделя')
async def week_tb(message : Message):
    gr_name = await sqlite_db.sql_find_gr_name(message)
    list_classes = await find_week_json(gr_name,name_json)
    days_of_week = ['Понедельник','Вторник','Среда','Чеверг','Пятница','Суббота']
    for index, day in enumerate(list_classes):
        str_out = ''
        if day == []:
            await message.answer(days_of_week[index]+'\n\nНет пар!!!\n\n--------------------------')
            continue
        
        str_out += day[0]['ДеньНедели']+'\n\n'
        for tmp in day:
             str_out += tmp['Тип занятия']+'\n'+tmp['ВремяНачала'].partition(' ')[2]+'\n'+tmp['Дисциплина']+'\n'+tmp['ФизическоеЛицо']+'\n'+tmp['Аудитория']+'\n\n'
        await message.answer(str_out+'\n--------------------------')

#функция для отправки погоды
@router.message(F.text.lower() == 'погода')
async def weather_tb(message : Message):
    await message.answer(get_weather())

@router.message(Command('notification'))
async def change_notification(message : Message, state : FSMContext):
    await state.set_state(FSMClient.notif)
    await message.answer('Введите время для напоминания расписания в формате 19:00, для отключения уведомлений введите -')

#выход из состояний
@router.message(FSMClient.notif, Command(commands=["cancel"]))
@router.message(FSMClient.notif, F.text.lower() == "отмена")
async def cancel_handler(message: Message, state: FSMContext):
   current_state = await state.get_state()
   if current_state is None:
      return
   await state.clear()
   await message.reply('OK')

@router.message(FSMClient.notif, F.text)
async def load_notif(message: Message, state: FSMContext):
    data = {}
    data['id_user'] = message.from_user.id
    data['time'] = message.text
    print(data)
    print("\n\n\n\n\n")
    await sqlite_db.sql_add_notif(message)
    await state.clear()