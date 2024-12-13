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
            "schedule": [{"event_id": 0, "date": "01.01.2022", "time": "11:00", "dealer": "John Doe", "desc": "meet"},
                         {"event_id": 1, "date": "01.01.2022", "time": "12:00", "dealer": "Spar", "desc": "buy"},
                         {"event_id": 2, "date": "01.01.2022", "time": "13:00", "dealer": "Bank", "desc": "pay"},
                        ]
            }

    while True:
        print("main process...")
        try:
            event_query = _from_telegram_queue.get(timeout=1)
          
            print(f"\n main(): {event_query}")

            if event_query[1]["pack"] == "read":
                _to_telegram_queue.put(_data)
                print(f"Main(): send schedule {_data}")

        except Empty:
            time.sleep(5)

    








 
