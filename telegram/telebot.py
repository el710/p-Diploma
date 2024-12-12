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

"""
    kostyl
"""
event_list = [{"description": "sdgdsg", "time": "11:00"}, {"description": "cvbnvj", "time": "13:00"}]



class DealEvent():
    event_list = []

    def __init__(self, **data):
        self.date = data["event_date"]
        self.time = data["event_time"]
        self.dealer = data["dealer"]
        self.description = data["event_description"]

        DealEvent.event_list.append(self)

posts_query = CallbackData('button', 'button_id', 'action')

def init_schedule(list):
    schedule = InlineKeyboardMarkup(row_width=1)

    for i, ev in enumerate(list):
        button = InlineKeyboardButton(f'{ev["time"]} - {ev["description"]}', callback_data=posts_query.new(str(i), action='push'))
        schedule.insert(button)
    
    return schedule



 



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

        
"""
    Handler for commands... </comm>
"""
@dp.message_handler(commands=['start'])
async def get_command(message):
    t_user = TelegramUser.get_user(message)
    if not t_user.login:
        await message.answer(f"Hello {t_user.nickname}! Nice to see you", reply_markup=out_main_keyboard)
        t_user.activate()
        """
            send new user to the UserBase
            queue
        """
    else:
        await message.answer(f"", reply_markup=out_main_keyboard)

"""
    Main menu
"""
@dp.message_handler(text=text_button_sched)
async def show_schedule(message):
    t_user = TelegramUser.get_user(message)
    if t_user.login:
        """
           send queary for schedule...
           wait for answer
           
           
           show inline shedule
        """
        """
            make inline menu
        """
        schedule_menu = init_schedule(event_list)

        """
           show inline shedule
        """
        await message.answer(f"Сегодня:", reply_markup=schedule_menu)
    else:
        await message.answer(f"try /start...")


@dp.callback_query_handler(posts_query.filter(action='push'))
async def open_event(call):
    # for i in call:
    #     print(i)
    await call.message.answer(f"event: {call.data}")
    await call.answer()
    



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
async def get_event_description(message, state):
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
async def get_event_description(message, state):
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
            """
                    send data to UserEventBase
            """
            data = await state.get_data()

            new_event = DealEvent(**data)
           
            await message.answer(f'''Добавлям событие:
                        дата: {new_event.date}
                        время: {new_event.time}
                        контакт: {new_event.dealer}
                        событие: {new_event.description}
                             ''', reply_markup=out_main_keyboard)
            await state.finish() 
    else:
        await message.answer(f"try /start...")



"""
    handler for every message
"""
@dp.message_handler()
async def all_message(message):
    await message.answer(f"try /start...")


async def botloop_routine():
    while True:
        await dp.start_polling()

def telebot_start():
    try:
        asyncio.run(botloop_routine())
    except Exception as e:
        print(f"Error: {e}")
    

    
    
    
    