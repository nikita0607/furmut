import telebot

import schedule
import threading
import helper

from threading import Thread
from time import sleep
from abc import ABC, abstractmethod

from telebot import types

from typing import Dict, Tuple

from carusel import *
from bot import Bot
from good_words import GoodWords
from user import User


bot = Bot("5709047064:AAE9QPGMacQ_nlMXVvqq2KICcz0XIJpNWNs", threaded=True)


def schedule_checker():  # рассылка
    while True:
        schedule.run_pending()
        sleep(1)


def eq_msg(text):
    def f(msg):
        return text == msg.text
    return f


@bot.message_handler(commands=['start'])
def welcome(message: types.Message):
    markup = helper.MessageHelper.start_markup()

    bot.users[message.from_user.id] = User(bot, message.from_user.id)
    bot.send_message(message.from_user.id, "Hallo", reply_markup=markup)


@bot.message_handler(func=eq_msg("Einen Timer hinzufugen"))
def add_timer(msg: types.Message):
    bot.send_message(msg.from_user.id, "Eintreten die Zeit", 
                     reply_markup=helper.MessageHelper.clear_murkup)
    bot.carusels[msg.from_user.id] = HealTimerCarusel(bot, bot.users[msg.from_user.id])


@bot.message_handler(func=eq_msg("Timer loschen"))
def delete_timer(msg: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user: User = bot.users[msg.from_user.id]
    timers = user.get_timers()
    
    if not timers:
        bot.reply_to(msg, "Keine Timer!")
        return
    for time in timers:
        item = types.KeyboardButton(Time.minuts_to_str(time))
        markup.add(item)


    bot.carusels[msg.from_user.id] = TimerDeleteCarusel(bot, bot.users[msg.from_user.id])
    bot.reply_to(msg, "Timer auswahlen", reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.from_user.id in bot.carusels)
def handle_carusel(msg: types.Message):
    bot.carusels[msg.from_user.id].step(msg)
    if bot.carusels[msg.from_user.id].is_ready:
        bot.carusels[msg.from_user.id].delete()
        bot.reply_to(msg, GoodWords.get_good_phrase(), 
                     reply_markup=helper.MessageHelper.start_markup())


Thread(target=schedule_checker).start()
bot.polling(none_stop=True)
