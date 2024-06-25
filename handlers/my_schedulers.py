from create_bot import scheduler, dp, bot
from aiogram.methods import SendMessage
import logging
import sqlite3
import json
from datetime import datetime
from handlers import client

import sqlite3
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from create_bot import scheduler, dp, bot
from handlers import client
import json
import os
from dotenv import load_dotenv
from apscheduler.triggers.cron import CronTrigger
import pytz

load_dotenv()

logging.basicConfig(level=logging.INFO)

# Установка часового пояса
timezone = pytz.timezone('Asia/Bangkok')  # UTC+7

# Соединение с базой данных
conn = sqlite3.connect('timetable.db')
cursor = conn.cursor()

# Функция для получения всех пользователей и их времени уведомления
def get_all_users():
    cursor.execute('SELECT id, time_notif FROM timetable WHERE time_notif != "-"')
    return cursor.fetchall()

async def sql_find_gr_id(user_id):
    search_query = str(user_id)
    for ret in cursor.execute('SELECT gr_name FROM timetable WHERE id LIKE ?', ('%'+search_query+'%',)).fetchall():
        return ret[0]

async def find_tomorrow_json_notif(gr_name, json_name):
    with open(json_name, 'r') as file:
        data = json.load(file)
    today_data = datetime.today().date()
    list_tomorrow = []
    for tmp in data:
        if (tmp['Группа'].lower() == gr_name.lower() and int(tmp['ВремяНачала'].partition('.')[0]) == ((((today_data-client.first_odd_week).days)%14)+2)):
            list_tomorrow.append(tmp)

    list_tomorrow = sorted(list_tomorrow, key=lambda d: int(d['ВремяНачала'].partition(' ')[2].partition(':')[0])) 
    list_tomorrow = await client.edit_list(list_tomorrow)
    return list_tomorrow

async def tomorrow_tb_notif(user_id):
    gr_name = await sql_find_gr_id(user_id)
    list_classes = await find_tomorrow_json_notif(gr_name, client.name_json)
    if not list_classes:
        return 'Завтра нет пар!!!'
    str_out = ''
    str_out += list_classes[0]['ДеньНедели'] + '\n\n'
    for tmp in list_classes:
        str_out += tmp['Тип занятия'] + '\n' + tmp['ВремяНачала'].partition(' ')[2] + '\n' + tmp['Дисциплина'] + '\n' + tmp['ФизическоеЛицо'] + '\n' + tmp['Аудитория'] + '\n\n'
    return str(str_out)

async def send_message(user_id):
    try:
        message = await tomorrow_tb_notif(user_id)
        await bot.send_message(user_id,"Расписание на завтра:\n" + message)
    except Exception as e:
        logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

def schedule_jobs():
    user_data = get_all_users()
    for user_id, time_notif in user_data:
        hours, minutes = map(int, time_notif.split(':'))
        trigger = CronTrigger(hour=hours, minute=minutes, timezone=timezone)
        scheduler.add_job(send_message, trigger, args=[user_id], id = f"user_{user_id}")
        logging.info(f"Scheduled job for user {user_id} at {time_notif} UTC+7")
    scheduler.start()

def get_user(user_id):
    cursor.execute('SELECT id, time_notif FROM timetable WHERE id = ? AND time_notif != "-"', (user_id,))
    return cursor.fetchone()

def update_user_job(user_id):
    logging.info(f"Updating scheduled job for user {user_id}...")
    # Удаление существующей задачи, если она есть
    try:
        scheduler.remove_job(f"user_{user_id}")
    except Exception as e:
        logging.warning(f"No existing job to remove for user {user_id}: {e}")
    
    # Добавление новой задачи
    user_data = get_user(user_id)
    if user_data:
        user_id, time_notif = user_data
        hours, minutes = map(int, time_notif.split(':'))
        trigger = CronTrigger(hour=hours, minute=minutes, timezone=timezone)
        scheduler.add_job(send_message, trigger, args=[user_id], id=f"user_{user_id}")
        logging.info(f"Scheduled job for user {user_id} at {time_notif} UTC+7")

if __name__ == "__main__":
    schedule_jobs()


