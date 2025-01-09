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

from slugify import slugify

from database.db import local_session, make_slug
from database.db import (create_base_user, read_base_user,
                         create_base_event, read_users_events
                        )

from web.data_schemas import CreateUser, CreateEvent


os.system('cls')
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

def pack_schedule(user_id, events_list = []):
    return {"user": user_id,
            "events_count": len(events_list),
            "schedule": events_list
           }

class TMessage():
    def __init__(self, args):
        self.user = args[0]["user"]
        self.type = args[1]["pack"]
        if self.type == 'read_event':
             self.username = args[1]["username"]
             self.firstname = args[1]["firstname"]
             self.lastname = args[1]["lastname"]
             self.language = args[1]["language"]
             self.is_human = args[1]["is_human"]
             self.telegram_id = args[1]["telegram_id"]            
        else:
            self.task = args[1]["description"]
            self.date = args[1]["date"]
            self.time = args[1]["time"]
            self.dealer = args[1]["dealer"]

    
    def __str__(self):
        return (str(self.__dir__()))
    
    def __del__(self):
        pass

    
    def get_user(self): return self.user
        


if __name__ == "__main__":
    dir, file = os.path.split(sys.argv[0])
    print(dir, file)
    os.chdir(dir)

    print(f"\nMain(): start...")

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
          
            print(f"\nMain() get: {event_query}")

            mess = TMessage(event_query)
            # print(mess)

            match mess.type:
                case "create_event":
                    print(f"Main() add event & make schedule")
                    db = local_session()
                    tmp_user = read_base_user(db, telegram_id=mess.get_user())
                    db.close()

                    if tmp_user:
                        new_event = CreateEvent(task = mess.task,
                                                date = mess.date,
                                                time = mess.time,
                                                owner_id = tmp_user.id,
                                                dealer = mess.dealer
                                            )
                        create_base_event(new_event)

                        db = local_session()
                        events = read_users_events(db, tmp_user.id) ## list of EventModel
                        db.close()

                        if events is None:
                            ## user have no events - send empty schedule
                            user_schedule = pack_schedule(mess.get_user())
                        else:
                            events_list = []
                            for idx, item in enumerate(events):
                                events_list.append({"event_id": idx,
                                                    "date": item.date,
                                                    "time": item.time,
                                                    "dealer": item.dealer,
                                                    "description": item.task}
                                                   )
                            pack_schedule(tmp_user.telegram_id, events_list=events_list)
                    
            
                case "read_event":
                    print(f"Main() login user & make schedule")
                    db = local_session()
                    tmp_user = read_base_user(db, telegram_id=mess.get_user())
                    if  tmp_user is None:
                        tmp_user = CreateUser(username = mess.username,
                                              firstname = mess.firstname,
                                              lastname = mess.lastname,
                                              email = 'user@mail',
                                              language = mess.language,
                                              is_human = mess.is_human,
                                              telegram_id = mess.telegram_id
                                            )
                        
                        create_base_user(db, tmp_user)

                        tmp_user = read_base_user(telegram_id=mess.get_user())
                        if tmp_user:
                            events = read_users_events(tmp_user.id) ## list of EventModel
                            if events is None:
                                ## user have no events - send empty schedule
                                user_schedule = pack_schedule(mess.get_user())
                            else:
                                events_list = []
                                for idx, item in enumerate(events):
                                    events_list.append({"event_id": idx,
                                                        "date": item.date,
                                                        "time": item.time,
                                                        "dealer": item.dealer,
                                                        "description": item.task}
                                                      )
                                user_schedule = pack_schedule(tmp_user.telegram_id, events_list)
                        db.close()

                    elif tmp_user.telegram_id == 0:
                        """
                            - update user &  Get user's events
                        """
                    else:
                        # print(tmp_user)
                        """
                            - Get user's events
                        """
                        db = local_session()
                        events = read_users_events(db, tmp_user.id) ## list of EventModel
                        if events is None:
                            ## user have no events - send empty schedule
                            user_schedule = pack_schedule(mess.get_user())
                        else:
                            events_list = []
                            for idx, item in enumerate(events):
                                events_list.append({"event_id": idx,
                                                    "date": item.date,
                                                    "time": item.time,
                                                    "dealer": item.dealer,
                                                    "description": item.task}
                                                )
                            user_schedule = pack_schedule(tmp_user.telegram_id, events_list)
                        db.close()

                case "udpate_event":
                    print(f"Main() change event & make schedule")

                case "delete_event":
                    print(f"Main() delete event & make schedule")
                
                case _:
                    ## wrong message - send None user & empty schedule
                    user_schedule = pack_schedule(None)

            telegram_link["in"].put(user_schedule)
            ##print(f"\nMain() put: send schedule {user_schedule}")

        except Empty:
            ## case if no message from telegram
            ## free proccess time
            time.sleep(3)

    








 
