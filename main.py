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


class UProject():
    """
        Class U-Project
        it defines:
         - main target
         - list of partners
         - list of clients (owners of project)
         - list of employers
         - plan & schedule
         - credit & debet
    """
    def __init__(self, target: str) -> None:
        self.main_target = target ## main target
        self.partners = []
        self.clients = []
        self.employers = []

from telegram.telebot import telebot_start

_from_telegram_queue = queue.Queue()
_to_telegram_queue = queue.Queue()

if __name__ == "__main__":
    dir, file = os.path.split(sys.argv[0])
    print(dir, file)
    os.chdir(dir)


    telegram_bot = Thread(target=telebot_start, args=[_to_telegram_queue, _from_telegram_queue], daemon=True)
    telegram_bot.start()


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

    








 
