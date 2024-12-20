from fastapi import FastAPI
import uvicorn
from data.webuser import WebUser
from .user_router import user_router
from .event_router import event_router


webapi = FastAPI()
webapi.include_router(user_router)
webapi.include_router(event_router)


def webapi_start(*args):
    """
        Web thread
    """
    WebUser.set_queue(args[0], args[1])
    
    try:
        uvicorn.run(webapi, host='127.0.0.1', port=8000)
    except Exception as e:
        print(f"Error: {e}")

