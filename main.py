"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""
import os
import sys

import asyncio
from threading import Thread
import time

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


if __name__ == "__main__":
    dir, file = os.path.split(sys.argv[0])
    print(dir, file)
    os.chdir(dir)

    telegram_bot = Thread(target=telebot_start, daemon=True)
    telegram_bot.start()

    while True:
        print("main process...")
        
        
        
        
        
        
        
        
        
        
        
        time.sleep(10)

    








 
