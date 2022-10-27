from abc import ABC, abstractmethod
from typing import Dict, Tuple, Union

from telebot import types

from bot import Bot
from helper import Time
from user import User


class Carusel(ABC):
    step_num = 0

    def __init__(self, bot, user):
        self.bot = bot
        self.user: User = user
        self.is_ready = False

    @abstractmethod
    def step(self, message: types.Message) -> Union[Tuple[str, types.ReplyKeyboardMarkup], None]:
        pass

    def delete(self):
        del self


class ScheduledCarusel(Carusel):
    def __init__(self, bot, user):
        self.shedules = []
        super().__init__(user, bot)


class HealTimerCarusel(Carusel):
    def step(self, msg: types.Message):
        text = msg.text

        time: int = Time.str_to_minuts(text)

        if time is None:
            self.bot.reply_to(msg, "Die Zeit ist unrichtig!")
            return

        self.bot.reply_to(msg, "Ja, das ist gut Zeit")
 
        self.user.add_timer(time, "Jetzt ist die Zeit!", ["Bereit"], HealAwakerCarusel)
        
        self.is_ready = True


class HealAwakerCarusel(Carusel):
    def step(self, msg: types.Message):
        if msg.text == "Bereit":
            self.is_ready = True
            self.bot.send_message(msg.from_user.id, "Gut!")
            self.is_ready = True
            return
        else:
            self.bot.send_message(msg.from_user.id, "Nicht gut...")


class TimerDeleteCarusel(Carusel):
    def step(self, msg: types.Message):
    
        time: int = Time.str_to_minuts(msg.text)

        if time is None:
            self.bot.reply_to(msg, "Die Zeit ist unrichtig!")
            return

        if not self.user.has_timer(time):
            self.bot.reply_to(msg, "Zeit nicht gefunden")
            return 

        self.bot.reply_to(msg, "Zeit entfert")
 
        self.user.delete_timer(time)
        self.is_ready = True

