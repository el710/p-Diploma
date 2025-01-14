"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

import os
import sys

import asyncio
from threading import Thread
import time
import queue
from queue import Empty

import logging

# from database.db import make_slug
from database.db import (create_base_user, read_base_user,
                         create_base_event, read_users_events,
                         update_base_event, delete_base_event)

from web.data_schemas import CreateUser, CreateEvent


os.system('cls')
logging.basicConfig(level=logging.INFO, 
                    format="%(levelname)s: | %(module)s     %(message)s")
print("Vivat Academia")


from telegram.telebot import telebot_start
from web.webapi import webapi_start


def run_thread_agent(func):
    """
        Run <func> as thread with 
        conection by two queues: "in" thread & "out" thread
        Return: in/out queues
    """
    in_queue = queue.Queue()
    out_queue = queue.Queue()
    thread = Thread(target=func,
                    args=[in_queue, out_queue],
                    daemon=True
                   )
    try:
        thread.start()
    except Exception as exc:
        print(f"run_thread_agent: exception {exc}")
        raise Exception
    
    return {"in": in_queue, "out": out_queue}


class TMessage():
    def __init__(self, args):
        self.user = args[0]["user"]
        self.message_type = args[1]["pack"]

        if self.message_type == 'create_event':
            self.task = args[1]["description"]
            self.date = args[1]["date"]
            self.time = args[1]["time"]
            self.dealer = args[1]["dealer"]
        elif self.message_type == 'read_event':
             self.username = args[1]["username"]
             self.firstname = args[1]["firstname"]
             self.lastname = args[1]["lastname"]
             self.language = args[1]["language"]
             self.is_human = args[1]["is_human"]
             self.telegram_id = args[1]["telegram_id"]
        elif self.message_type == 'update_event':
            self.event_id = args[1]["event_id"]
            self.task = args[1]["description"]
            self.date = args[1]["date"]
            self.time = args[1]["time"]
            self.dealer = args[1]["dealer"]
        else:
            self.event_id = args[1]["event_id"]
    
    def __str__(self):
        return (str(self.__dir__()))
    
    def __del__(self):
        pass

    def set_user(self, user=None): self.user = user
    def get_user(self): return self.user
    def get_message_type(self): return self.message_type


def pack_schedule(user_id=None, events_list = []):
    '''
        Make message to telegram bot
        Return: dictionary {}
    '''
    if events_list: 
        volume = len(events_list)
    else:
        volume = 0
    if events_list: 
        return {"user": user_id,
                "events_count": volume,
                "schedule": events_list}


def make_telegram_data(user_id=None, events=None):
    if user_id is None or events is None:
        ## no user - send empty messaage
        ## user have no events - send empty message
        return pack_schedule(user_id, events)
    else:
        events_list = []
        for item in events:
            events_list.append({"event_id": item.id,
                                "date": item.date,
                                "time": item.time,
                                "dealer": item.dealer,
                                "description": item.task}
            )
        return pack_schedule(user_id, events_list=events_list)    

def get_user_events(user_id):
    if user_id:
       events = read_users_events(user_id) ## list of EventModel
       logging.info(f"get_user_events(): {user_id} - events -{len(events)}")    
    else: 
        events = None
        logging.info(f"get_user_events(): {user_id} - events -{events}")    

    

    return make_telegram_data(user_id, events)


if __name__ == "__main__":
    dir, file = os.path.split(sys.argv[0])
    print(dir, file)
    os.chdir(dir)

    logging.info("Main(): start...")

    # start thread with telegram bot
    telegram_link = run_thread_agent(telebot_start)

    # start thread with webapi
    webapi_link = run_thread_agent(webapi_start)

    user_schedule = {}
        
    # main work cycle
    while True:
        # print("Main(): wait...")
        try:
            event_query = telegram_link["out"].get(timeout=1)
            # print(f"\nMain() get: {event_query}")

            ## parse message
            mess = TMessage(event_query)
            
            logging.info(f"get message: {mess.get_message_type()}")

            match mess.get_message_type():
                case "create_event":
                    logging.info("add event")
                    tmp_user = read_base_user(mess.get_user())
                    logging.info(f"{tmp_user.__str__()}")

                    if tmp_user:
                        new_event = CreateEvent(task = mess.task,
                                                date = mess.date,
                                                time = mess.time,
                                                owner_id = tmp_user.id,
                                                dealer = mess.dealer
                                            )
                        create_base_event(new_event)

                case "read_event":
                    logging.info("read & login user")
                    
                    tmp_user = read_base_user(mess.get_user())
                    logging.info(f"user: {tmp_user}")

                    if tmp_user is None:
                        tmp_user = CreateUser(username = mess.username,
                                              firstname = mess.firstname,
                                              lastname = mess.lastname,
                                              email = 'user@mail',
                                              language = mess.language,
                                              is_human = mess.is_human,
                                              telegram_id = mess.telegram_id
                                             )
                        
                        logging.info(f"create user: {tmp_user}")    
                        create_base_user(tmp_user)

                case "update_event":
                    logging.info("update event")
                    tmp_user = read_base_user(mess.get_user())
                    
                    if tmp_user:
                        new_event = CreateEvent(task = mess.task,
                                                date = mess.date,
                                                time = mess.time,
                                                owner_id = tmp_user.id,
                                                dealer = mess.dealer)
                        # logging.info(f"{mess.get_user()} update event {mess.event_id}:  {new_event}")
                        update_base_event(mess.event_id, new_event)


                case "delete_event":
                    logging.info("delete event")

                    delete_base_event(mess.event_id)
                
                case _:
                    ## wrong message - set None user
                    mess.set_user()

            ## send user schedule as answer
            user_schedule = get_user_events(mess.get_user())
            
            telegram_link["in"].put(user_schedule)
            ##print(f"\nMain() put: send schedule {user_schedule}")

        except Empty:
            ## in case no message from telegram
            ## free proccess time
            time.sleep(3)
