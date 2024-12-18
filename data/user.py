"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""
import queue
from queue import Empty
import time


class UUser():
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.username = None
        self.language = None
        self.is_human = None

    def set_human_state(self, is_human):
        if is_human != None: self.is_human = bool(is_human)


class IOUser(UUser):
    users = []

    def __init__(self):
        super().__init__()
        self.login = None ## is user login/logout
        self.interface = {"app": False, "web": False, "telegram": False} ## User interface

    
    def user_log(self):
        pass