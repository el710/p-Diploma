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





    _data = {"user": 6837972319,
             "count": 3,
             "schedule": [{"event_id": 0, "date": "01.01.2022", "time": "11:00", "dealer": "John Doe", "description": "meet"},
                         {"event_id": 1, "date": "01.01.2022", "time": "12:00", "dealer": "Spar", "description": "buy"},
                         {"event_id": 2, "date": "01.01.2022", "time": "13:00", "dealer": "Bank", "description": "pay"},
                        ]
            }

    while True:
        # print("Main(): wait...")
        try:
            event_query = _from_telegram_queue.get(timeout=1)
          
            print(f"\nMain() get: {event_query}")

            if event_query[1]["pack"] == "create_event":
                print(f"Main() add event & make schedule")

            elif event_query[1]["pack"] == "read_event":
                print(f"Main() login user & make schedule")

            elif event_query[1]["pack"] == "udpate_event":
                print(f"Main() change event & make schedule")
            
            elif event_query[1]["pack"] == "delete_event":
                print(f"Main() delete event & make schedule")

            _to_telegram_queue.put(_data)
            print(f"\nMain() put: send schedule")

        except Empty:
            time.sleep(3)

    








 
