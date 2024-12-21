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


if __name__ == "__main__":
    dir, file = os.path.split(sys.argv[0])
    print(dir, file)
    os.chdir(dir)

    print(f"\nMain(): start...")

    _from_telegram_queue = queue.Queue()
    _to_telegram_queue = queue.Queue()
    telegram_bot = Thread(target=telebot_start, args=[_to_telegram_queue, _from_telegram_queue], daemon=True)
    telegram_bot.start()

    _to_webapi_queue = queue.Queue()
    _from_webapi_queue = queue.Queue()
    webapi_app = Thread(target=webapi_start, args=[_to_webapi_queue, _from_webapi_queue], daemon=True)
    webapi_app.start()

    """
        INIT:
        - get all users with telegram_id
        - get events for each user for today - make schedule
    """
    send_data = {}
        
    while True:
        # print("Main(): wait...")
        try:
            event_query = _from_telegram_queue.get(timeout=1)
          
            print(f"\nMain() get: {event_query}")

            telegram_user = event_query[0]["user"]
            message = event_query[1]

            match message["pack"]:
                case "create_event":
                    print(f"Main() add event & make schedule")

                    db = local_session()
                    tmp_user = read_base_user(db, telegram_id=telegram_user)
                    if tmp_user:
                        new_event = CreateEvent(task = message["description"],
                                                date = message["date"],
                                                time = message["time"],
                                                owner_id = tmp_user.id,
                                                dealer = message["dealer"]
                                            )
                        create_base_event(db, new_event)

                        events = read_users_events(db, tmp_user.id) ## list of EventModel
                        if events is None:
                            send_data = {"user": message["telegram_id"],
                                         "events_count": 0,
                                         "schedule": []
                                        }
                        else:
                            events_list = []
                            for idx, item in enumerate(events):
                                events_list.append({"event_id": idx,
                                                    "date": item.date,
                                                    "time": item.time,
                                                    "dealer": item.dealer,
                                                    "description": item.task}
                                                   )
                            
                            send_data = {"user": tmp_user.telegram_id,
                                         "events_count": len(events),
                                         "schedule": events_list
                                        }
                                        
                    db.close()
            
                case "read_event":
                    print(f"Main() login user & make schedule")

                    db = local_session()
                    tmp_user = read_base_user(db, slug=make_slug(message["username"], message["firstname"], message["lastname"]))
                    if  tmp_user is None:
                        tmp_user = CreateUser(username = message["username"],
                                              firstname = message["firstname"],
                                              lastname = message["lastname"],
                                              email = 'user@mail',
                                              language = message["language"],
                                              is_human = message["is_human"],
                                              telegram_id = message["telegram_id"]
                                            )
                        
                        create_base_user(db, tmp_user)

                        tmp_user = read_base_user(db, telegram_id=telegram_user)
                        if tmp_user:
                            events = read_users_events(db, tmp_user.id) ## list of EventModel
                            if events is None:
                                send_data = {"user": message["telegram_id"],
                                             "events_count": 0,
                                             "schedule": []
                                            }
                            else:
                                events_list = []
                                for idx, item in enumerate(events):
                                    events_list.append({"event_id": idx,
                                                        "date": item.date,
                                                        "time": item.time,
                                                        "dealer": item.dealer,
                                                        "description": item.task}
                                                      )
                                send_data = {"user": tmp_user.telegram_id,
                                             "events_count": len(events),
                                             "schedule": events_list
                                            }

                    elif tmp_user.telegram_id == 0:
                        """
                            - update user &  Get user's events
                        """
                    else:
                        # print(tmp_user)
                        """
                            - Get user's events
                        """
                        events = read_users_events(db, tmp_user.id) ## list of EventModel
                        if events is None:
                            send_data = {"user": message["telegram_id"],
                                         "events_count": 0,
                                         "schedule": []
                                        }
                        else:
                            events_list = []
                            for idx, item in enumerate(events):
                                events_list.append({"event_id": idx,
                                                    "date": item.date,
                                                    "time": item.time,
                                                    "dealer": item.dealer,
                                                    "description": item.task}
                                                )
                            send_data = {"user": tmp_user.telegram_id,
                                         "events_count": len(events),
                                         "schedule": events_list
                                        }
                    
                    db.close()

                case "udpate_event":
                    print(f"Main() change event & make schedule")

                case "delete_event":
                    print(f"Main() delete event & make schedule")
                
                case _:
                    send_data = {"user": None,
                                 "events_count": 0,
                                 "schedule": []
                                }

            _to_telegram_queue.put(send_data)
            print(f"\nMain() put: send schedule {send_data}")

        except Empty:
            time.sleep(3)

    








 
