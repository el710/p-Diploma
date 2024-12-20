"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""
import queue
from queue import Empty
import time


class UUser():
    def __init__(self):
        self.firstname = None
        self.lastname = None
        self.username = None
        self.language = None
        self.is_human = None

    def set_human_state(self, is_human):
        if is_human != None: self.is_human = bool(is_human)


class IOUser(UUser):
    users = []

    def __init__(self):
        super().__init__()
        self.login = False ## is user login/logout

    
    def user_log(self):
        pass