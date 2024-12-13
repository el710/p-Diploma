"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""
"""
    Telegram bot module
"""
import os, sys

## basic...
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

## for get <state>... to get, keep & use data of users
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

## outline menu buttons
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

## inline menu buttons
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

import asyncio
import queue
import json

from .id_bot import tel_token
from data.user import TelegramUser


text_button_sched = "Расписание"
text_button_add = "Добавить"
button_sched = KeyboardButton(text_button_sched)
button_add = KeyboardButton(text_button_add)
out_main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
out_main_keyboard.add(button_sched)
out_main_keyboard.add(button_add)

text_button_cancel = "Отменить"
button_cancel = KeyboardButton(text_button_cancel)
out_cancel_menu = ReplyKeyboardMarkup(resize_keyboard=True)
out_cancel_menu.add(button_cancel)


posts_query = CallbackData('button', 'button_id', 'action')

async def init_schedule_keyboard(events_list):
    schedule = InlineKeyboardMarkup(row_width=1)
    # print(f"init(): {events_list}")

    for i, event in enumerate(events_list):
        button = InlineKeyboardButton(f' {event["time"]} ({event["dealer"]}): {event["desc"]}', callback_data=posts_query.new(button_id=str(i), action='push'))
        schedule.insert(button)
    
    return schedule

text_button_edit = "Изменить"
text_button_delete = "Удалить"
button_edit = InlineKeyboardButton(text_button_edit, callback_data='edit')
button_delete = InlineKeyboardButton(text_button_delete, callback_data="delete")
event_callback = CallbackData('event', 'id', 'action')

async def init_event_keyboard(user_id, event_id):
    event_menu = InlineKeyboardMarkup()
    button_edit = InlineKeyboardButton(text_button_edit, callback_data=event_callback.new(id=f"{user_id}-{event_id}", action='edit'))
    button_delete = InlineKeyboardButton(text_button_delete, callback_data=event_callback.new(id=f"{user_id}-{event_id}", action='delete'))

    event_menu.insert(button_edit)
    event_menu.insert(button_delete)
    
    return event_menu

class MakeEvent(StatesGroup):
    event_date = State()
    event_time = State()
    dealer = State()
    event_description = State()

"""
    make bot & dispetcher
"""
bot = Bot(token=tel_token)
dp = Dispatcher(bot, storage=MemoryStorage())

_main_queue = None
        
"""
    Handler for commands... </comm>
"""
@dp.message_handler(commands=['start'])
async def get_command(message):
    """
        Login new user
    """
    t_user = TelegramUser.get_user(message)
    if not t_user.login:
        await message.answer(f"Hello {t_user.username}! Nice to see you", reply_markup=out_main_keyboard)
        # print("get_command(): call activate...")
        await t_user.activate()
    else:
        await message.answer(f"use menu...", reply_markup=out_main_keyboard)

"""
    Main menu
"""
@dp.message_handler(text=text_button_sched)
async def show_schedule(message):
    """
        Show user's schedule  in keyboard style
    """
    t_user = TelegramUser.get_user(message)
    if t_user.login:
        schedule_menu = await init_schedule_keyboard(t_user.schedule)

        await message.answer(f"Сегодня:", reply_markup=schedule_menu)
    else:
        await message.answer(f"try /start...")


"""
    Start new deal event State Machine
"""
@dp.message_handler(text=text_button_add)
async def start_new_event(message):
    t_user = TelegramUser.get_user(message)
    if t_user.login:
        """
           start StateMachine for new deal event
        """
        await message.answer(f"Укажите контакт: ", reply_markup = out_cancel_menu)
        await MakeEvent.dealer.set()
    else:
        await message.answer(f"try /start...")

@dp.message_handler(state=MakeEvent.dealer)
async def get_event_dealer(message, state):
    t_user = TelegramUser.get_user(message)
    if t_user.login:
        """
           set deal event - start description
        """
        if message.text == text_button_cancel:
           await message.answer(f"добавление отменено", reply_markup=out_main_keyboard)
           await state.finish()
        else:
            await state.update_data(dealer=message.text)
            await message.answer(f"Опишите событие: ", reply_markup = out_cancel_menu)
            await MakeEvent.event_description.set()
    else:
        await message.answer(f"try /start...")

@dp.message_handler(state=MakeEvent.event_description)
async def get_event_description(message, state):
    t_user = TelegramUser.get_user(message)
    if t_user.login:
        """
           set description - start data
        """
        if message.text == text_button_cancel:
           await message.answer(f"добавление отменено", reply_markup=out_main_keyboard)
           await state.finish()
        else:
            await state.update_data(event_description=message.text)
            await message.answer(f"Укажите дату: ", reply_markup = out_cancel_menu)
            await MakeEvent.event_date.set()
    else:
        await message.answer(f"try /start...")

@dp.message_handler(state=MakeEvent.event_date)
async def get_event_date(message, state):
    t_user = TelegramUser.get_user(message)
    if t_user.login:
        """
           set date - start time
        """
        if message.text == text_button_cancel:
           await message.answer(f"добавление отменено", reply_markup=out_main_keyboard)
           await state.finish()
        else:
            await state.update_data(event_date=message.text)
            await message.answer(f"Укажите время: ", reply_markup = out_cancel_menu)
            await MakeEvent.event_time.set()
    else:
        await message.answer(f"try /start...")

@dp.message_handler(state=MakeEvent.event_time)
async def get_event_time(message, state):
    t_user = TelegramUser.get_user(message)
    if t_user.login:
        """
           set time - end machine
        """
        if message.text == text_button_cancel:
           await message.answer(f"добавление отменено", reply_markup=out_main_keyboard)
           await state.finish()
        else:
            await state.update_data(event_time=message.text)
            data = await state.get_data()                       
            """
                CREATE: send new event to main
            """
            await t_user.create_event(**data)

            if t_user.send_request("create"):
                await message.answer("Новое событие: отправлено...", reply_markup=out_main_keyboard)
            else:
                await message.answer("Новое событие: не добавлено...", reply_markup=out_main_keyboard)

            await state.finish() 
    else:
        await message.answer(f"try /start...")

"""
    Events handler
"""

@dp.callback_query_handler(posts_query.filter(action='push'))
async def open_event(call):
    """
        Work with Event
    """
    user_id = call.from_user['id']
    t_user = TelegramUser.find_user(user_id)

    if t_user:
        event_id = int(call.data.split(":")[1])
        event_menu = await init_event_keyboard(user_id, event_id)

        await call.message.answer(f'''
        время: {t_user.schedule[event_id]["time"]}
        контакт: {t_user.schedule[event_id]["dealer"]}
        событие: {t_user.schedule[event_id]["desc"]}
                                   ''', reply_markup = event_menu)

    await call.answer()
    
@dp.callback_query_handler(event_callback.filter(action='edit'))
async def edit_event(call):
    """
        Edit Event
    """
    ids = call.data.split(":")[1]
    await call.message.answer(f"{ids}")
    await call.answer()

@dp.callback_query_handler(event_callback.filter(action='delete'))
async def delete_event(call):
    """
        Edit Event
    """
    ids = call.data.split(":")[1]
    await call.message.answer(f"{ids}")
    await call.answer()


@dp.message_handler()
async def all_message(message):
   """
        handler for unexpected messages
   """
   await get_command(message)


async def botloop_routine():
    """
        Main cycle for bot dispatcher
    """
    while True:
        await dp.start_polling()
        asyncio.sleep(0.1)

def telebot_start(*args):
    """
        Telegram bot thread
    """
    TelegramUser.set_queue(args[0], args[1])
    
    try:
        asyncio.run(botloop_routine())
    except Exception as e:
        print(f"Error: {e}")
    

    
    
    
    