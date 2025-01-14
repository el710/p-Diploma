"""
    Event model

    {"event_id": 0, "date": "01.01.2022", "time": "11:00", "dealer": "John Doe", "task": "meet"}
"""

"""
    FROM Telegram queue

    user message: 
    [{'user': xxx}, {'pack': 'read_event', 'telegram_id': xxx, 'firstname': 'xxx', 'lastname': 'xxx', 'username': 'xxx', 'language': 'xxx', 'is_human': xxx}]

    CRUD message:
    [{'user': xxx}, {'pack': 'create_event | update_event | delete_event', 'event_id': xxx, 'date': 'xx.xx.xxxx', 'time': 'xx:xx', 'dealer': 'xxx', 'description': 'xxx'}]
"""

"""
    TO Telegram queue

    schedule message:
    {"user": 6837972319,
             "events_count": 3,
             "schedule": [{"event_id": 5, "date": "01.01.2022", "time": "11:00", "dealer": "John Doe", "description": "meet"},
                         {"event_id": 7, "date": "01.01.2022", "time": "12:00", "dealer": "Spar", "description": "buy"},
                         {"event_id": 2, "date": "01.01.2022", "time": "13:00", "dealer": "Bank", "description": "pay"},
                        ]
            }
"""