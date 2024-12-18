"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""
import queue
from queue import Empty
import time
from .user import IOUser

telegram_keys = ["first_name", "last_name", "username", "language_code", "is_bot", "id"]


class TelegramUser(IOUser):
    """
        Telegram client 
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
        self.set_human_state(not user_data["is_bot"])
        
        self.user_id = user_data["id"]
        self.login = False
        self.interface["telegram"] = True
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
        TelegramUser.__in_queue = in_queue
        TelegramUser.__out_queue = out_queue

    
    def parse_TG_message(bot_message):
        """
            Make user data from telegram message
        """
        user_data = {}
        for key, value in bot_message:
            if isinstance(value, dict):
                for i in telegram_keys:
                    if user_data.get(i) == None:
                        user_data[i] = value.get(i)
        return user_data       

    def find_user(user_id):
        for item in TelegramUser.users:
            if item["id"] == user_id:
                return item["address"]
        return None

    def get_user(bot_message):
        """
            Find user in list or make new one
            return: user
        """
        user_data = TelegramUser.parse_TG_message(bot_message)
        
        for item in TelegramUser.users:
            if item["id"] == user_data["id"]:
                return item["address"]
        
        new_user = TelegramUser(user_data)
        TelegramUser.users.append({"id": user_data["id"], "address": new_user})

        return new_user
    

    async def activate(self):
        """
            Request user & schedule from base
        """
        # print("activate(): call read_event...")
        self.login = await self.read_event()


    async def create_event(self, **data):
        """
            CRUD: make Create event
        """
        self.event_new_req = {"pack": "create_event",
                              "event_id": None,
                              "date": data["date"], 
                              "time": data["time"],
                              "dealer": data["dealer"], 
                              "description": data["description"]
                             }     
        # print(f"create_event(): {self.event_new_req}")
        return await self.send_request(request_type="create")
        

    async def read_event(self):
        """
            CRUD: make Read event 
        """
        self.event_get_req = {"pack": "read_event"}
        self.event_get_req.update(self.get_user_info())
        # print(f"read_event(): call send_request...")
        return await self.send_request(request_type="read")


    async def update_event(self, event_id, **data):
        """
            CRUD: make event update
        """
        self.event_chg_req = {"pack": "update_event",
                              "event_id": event_id,
                              "date": data["date"], 
                              "time": data["time"],
                              "dealer": data["dealer"], 
                              "description": data["description"]
                             }  
        return await self.send_request(request_type="update")


    async def delete_event(self, event_id):
        """
            CRUD: make event delete request
        """
        self.event_del_req = {"pack": "delete_event",
                              "event_id": event_id,
                              "date": None, 
                              "time": None,
                              "dealer": None, 
                              "description": None
                             } 
        return await self.send_request(request_type="delete")
      
    
    async def send_request(self, request_type="read"):
        """
            Send CRUD request to database dispatcher
        """
        _request = []

        _request.append({"user": self.user_id})

        if request_type == "create":
            _request.append(self.event_new_req)
        elif request_type == "read":
            _request.append(self.event_get_req)
        elif request_type == "update":
            _request.append(self.event_chg_req)
        elif request_type == "delete":
            _request.append(self.event_del_req)
        else:
            _request.clear()
        
        if _request:
            TelegramUser.__out_queue.put(_request)
            return self.get_schedule()
        
        return False
    

    def get_schedule(self):
        """
            Get & parce events list to schedule
        """
        # print("get_schedule(): ...")
        _try_count = 3
        while _try_count:
            try:
                 schedule = TelegramUser.__in_queue.get(timeout=1)
                 if schedule:
                    self.parse_schedule(schedule)
                    #  print(f"get_schedule(): {self.schedule}")
                    return True
            except Empty:
                # print(f"get_schedule(): empty queue ...")
                time.sleep(1)
                _try_count -= 1
            # finally:
            #     print(f"get_schedule(): wait...")
        return False


    def parse_schedule(self, package):
        if package["count"]:
            self.schedule = package["schedule"]
        else:
            self.schedule.clear()


        
                      


                            

        
        
    



