import sqlite3 as sq
from create_bot import bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import logging
import pytz
from create_bot import scheduler
from apscheduler.triggers.cron import CronTrigger
from handlers import my_schedulers

timezone = pytz.timezone('Asia/Bangkok')  # UTC+7

def sql_start():
   global base, cur
   base = sq.connect('timetable.db')
   cur = base.cursor()
   if base:
      print('Data base connected OK!')
   base.execute('CREATE TABLE IF NOT EXISTS timetable'+
         '(id TEXT UNIQUE, gr_name TEXT, time_notif TEXT)')
   base.commit()

def get_user(user_id):
    cur.execute('SELECT id, time_notif FROM timetable WHERE id = ? AND time_notif != "-"', (user_id,))
    return cur.fetchone()

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
        scheduler.add_job(my_schedulers.send_message, trigger, args=[user_id], id=f"user_{user_id}")
        logging.info(f"Scheduled job for user {user_id} at {time_notif} UTC+7")

async def sql_add_command(message: Message):
   data = {}
   data['id_user'] = message.from_user.id
   data['gr_name'] = message.text.lower()
   # Удаление существующей задачи, если она есть
   try:
      scheduler.remove_job(f"user_{data['id_user']}")
   except Exception as e:
      logging.warning(f"No existing job to remove for user {data['id_user']}: {e}")
   #replace используется чтобы пользователь смог сменить группу
   cur.execute('REPLACE INTO timetable (id, gr_name, time_notif) VALUES (?, ?, ?)', tuple(data.values()) + ('19:00', ))#tuple(data.values()))
   base.commit()
   user_data = get_user(data['id_user'])
   if user_data:
      user_id, time_notif = user_data
      hours, minutes = map(int, time_notif.split(':'))
      trigger = CronTrigger(hour=hours, minute=minutes, timezone=timezone)
      scheduler.add_job(my_schedulers.send_message, trigger, args=[user_id], id=f"user_{user_id}")
      logging.info(f"Scheduled job for user {user_id} at {time_notif} UTC+7")

async def sql_add_notif(message: Message):
   data = {}
   data['time'] = message.text
   data['id_user'] = message.from_user.id
   
   # Удаление существующей задачи, если она есть
   try:
      scheduler.remove_job(f"user_{data['id_user']}")
   except Exception as e:
      logging.warning(f"No existing job to remove for user {data['id_user']}: {e}")
   #replace используется чтобы пользователь смог сменить группу
   cur.execute('UPDATE timetable SET time_notif = ? WHERE id = ?', tuple(data.values()))#tuple(data.values()))
   base.commit()
   user_data = get_user(data['id_user'])
   if user_data:
      user_id, time_notif = user_data
      hours, minutes = map(int, time_notif.split(':'))
      trigger = CronTrigger(hour=hours, minute=minutes, timezone=timezone)
      scheduler.add_job(my_schedulers.send_message, trigger, args=[user_id], id=f"user_{user_id}")
      logging.info(f"Scheduled job for user {user_id} at {time_notif} UTC+7")

async def sql_find_gr_name(message):
   search_query = str(message.from_user.id)
   for ret in cur.execute('SELECT gr_name FROM timetable WHERE id LIKE ?', ('%'+search_query+'%',)).fetchall():
      return(ret[0])
      