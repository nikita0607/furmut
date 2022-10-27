import schedule

import helper

from telebot import types

from typing import List, Dict, Callable, Type

from bot import Bot


class Task:
    def __init__(self, user: 'User', schedule, text, keys, carusel = None, schedule_timer=-1):
        self.schedule = schedule

        self.schedule_timer = schedule_timer
        self.timed_schedule = None
        
        self.keys: list = keys
        self.text: str = text
        self.user: User = user
        self.carusel = carusel

    def cancel(self):
        schedule.cancel_job(self.schedule)
        if self.timed_schedule:
            schedule.cancel_job(self.timed_schedule)
        del self

    def handle(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for key_text in self.keys:
            markup.add(types.KeyboardButton(key_text))
        self.user.bot.send_message(self.user.chat_id, self.text, reply_markup=markup)

        if self.carusel:
             self.user.bot.carusels[self.user.chat_id] = self.carusel(self.user.bot, self.user)
             if self.schedule_timer > -1:
                self.timed_schedule = schedule.every(5).minutes.do(self.t_schedule_check)

    def t_schedule_check(self):
        if self.user.chat_id in self.user.bot.carusels and \
                isinstance(self.user.bot.carusels[self.user.chat_id], self.carusel):
            self.user.bot.send_message(self.user.chat_id, "Du hast mich vergessen...")
        else:
            schedule.cancel_job(self.timed_schedule)
                 

class User:
    def __init__(self, bot, chat_id: int):
        self.bot: Bot = bot
        self.chat_id = chat_id
        self.timer_schedule: Dict[int, Task] = {}

    def add_timer(self, _time, msg: str, keys: list, carusel):
        schd = schedule.every().day.at(helper.Time.minuts_to_str(_time)).do(lambda: self.sched_handle(_time))
        task = Task(self, schd, msg, keys, carusel, 5)
        self.timer_schedule[_time] = task

    def get_timers(self) -> List[int]:
        return [i for i in self.timer_schedule]
    
    def has_timer(self, time: int) -> bool:
        return time in self.timer_schedule

    def delete_timer(self, time: int):
        self.timer_schedule[time].cancel()
        del self.timer_schedule[time]

    def sched_handle(self, _time):
        self.timer_schedule[_time].handle()
        
