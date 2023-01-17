from dotenv import load_dotenv
import requests
import os

class Telegram():
    def __init__(self) -> None:
        load_dotenv()
        self.token = os.getenv('TOKEN')
    
    def sender(self, msg: str, id: int):
        method = '/sendMessage'
        url = 'https://api.telegram.org/bot'
        data = {
            'chat_id':id,
            'text':msg,
            'parse_mode':'markdown'
        }
        return requests.post(url+self.token+method, data=data).json()


    def get_chat_id(self):
        url = 'https://api.telegram.org/bot'
        method = '/getUpdates'
        res = requests.post(url+self.token+method).json()
        print(res)

    def set_chat_id():
        pass