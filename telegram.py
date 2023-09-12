import os
from dotenv import load_dotenv
import telebot


class TelegramBot:
    def __init__(self, demo: bool = False):
        load_dotenv()
        self.demo = demo
        self.token = os.getenv("TOKEN")
        self.chat_id = os.getenv("ID_CHAT")
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.id_last_msg = 0
        self.id_gale = 0
        self.bot = telebot.TeleBot(self.token, parse_mode='Markdown', disable_web_page_preview=True)


    def send_message(self, text: str, reply: int = None):
        try:
            print(text, self.chat_id)
            if not self.demo:
                return self.bot.send_message(self.chat_id, text, reply_to_message_id=reply)
            return
        except:
            pass

    def send_message_by_id(self, chat_id, text):
        try:
            if not self.demo:
                return self.bot.send_message(chat_id, text)
            self.log.debug(text)
        except:
            pass
    
    def send_photo(self, chat_id, photo: str):
        with open(photo, 'rb') as photo_rb:
            self.bot.send_photo(chat_id, photo_rb)
        return True

    def delete_menssage(self, message_id):
        try:
            if not self.demo:
                self.bot.delete_message(chat_id=self.chat_id, message_id=message_id)
            return
        except:
            pass
