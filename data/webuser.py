"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""
import queue
from queue import Empty
import time

from .user import IOUser

class WebUser(IOUser):
    """
        Web client 
        - class's list of users
        - class's queues for excahnge with database dispatcher
        - object's user id data
        - object's user schedule - list of today's events


    """
    __users_list = []
    __in_queue = None
    __out_queue = None

    def __init__(self, user_data):
        super().__init__()
        self.first_name = user_data["first_name"]
        self.last_name = user_data["last_name"]
        self.username = user_data["username"]
        self.language = user_data["language_code"]
        self.human_state = True
        self.user_id = user_data["id"]
        
        self.login = False
        self.interface["web"] = True
        self.schedule = []
        self.event_new_req = {}
        self.event_get_req = {}
        self.event_chg_req = {}
        self.event_del_req = {}
    
    def get_user_info(self):
        """
            Make dict of user identification data
        """
        return {"user_id": self.user_id, 
                "first_name": self.first_name, 
                "last_name": self.last_name,
                "username": self.username, 
                "language": self.language,
                "is_human": self.is_human, 
                "interface": self.interface
                }
 
        

    def set_queue(in_queue, out_queue):
        """
            Set queues. Call when thread of bot has started
        """
        WebUser.__in_queue = in_queue
        WebUser.__out_queue = out_queue
