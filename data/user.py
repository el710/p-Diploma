"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

class UUser():
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.nickname = None
        self.email = None
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


telegram_keys = ["first_name", "last_name", "username", "language_code", "is_bot", "id"]


class TelegramUser(IOUser):

    def __init__(self, user_data):
        super().__init__()
        self.first_name = user_data["first_name"]
        self.last_name = user_data["last_name"]
        self.nickname = user_data["username"]
        self.language = user_data["language_code"]
        self.set_human_state(not user_data["is_bot"])
        self.user_id = user_data["id"]
        self.login = False
        self.interface["telegram"] = True

    def activate(self):
        self.login = True
    
    def parse_message(bot_message):
        user_data = {}
        for key, value in bot_message:
            if isinstance(value, dict):
                for i in telegram_keys:
                    if user_data.get(i) == None:
                        user_data[i] = value.get(i)
        return user_data       

    def auth(self, bot_message):
        for key, value in bot_message:
            # print(key, type(value))
            if isinstance(value, dict):
                if self.first_name == None: self.first_name = value.get(TelegramUser._FIRST_NAME, None)
                if self.last_name == None: self.last_name = value.get(TelegramUser._LAST_NAME, None)
                if self.nickname == None: self.user_name = value.get(TelegramUser._NICK_NAME, None)
                if self.language == None: self.language = value.get(TelegramUser._LANG_ID, None)
                if self.bot == None: self.bot = value.get(TelegramUser._NOT_HUMAN, None)
                if self.telegram_id == None: self.telegram_id = value.get(TelegramUser._TELEGRAM_ID, None)
        self.set_human_state(not self.bot)
    
    
    def get_user(bot_message):
        user_data = TelegramUser.parse_message(bot_message)
        
        for item in TelegramUser.users:
            if item["id"] == user_data["id"]:
                return item["address"]
        
        new_user = TelegramUser(user_data)
        TelegramUser.users.append({"id": user_data["id"], "address": new_user})
        return new_user

        

        


                            

        
        
    


