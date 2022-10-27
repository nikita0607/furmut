import re

from telebot import types

from typing import Union


class Time:
    @staticmethod
    def minuts_to_str(mins: int) -> str:
        hours = mins//60
        minuts = mins%60

        if hours < 10:
            hours = f"0{hours}"
        else:
            hours = f"{hours}"

        if minuts < 10:
            minuts = f"0{minuts}"
        else:
            minuts = f"{minuts}"
        
        return f"{hours}:{minuts}"

    @staticmethod
    def str_to_minuts(t: str) -> Union[int, None]:
        ind = re.search("[0-9]{1,2}[:. ]", t)

        if ind is None:
            return None

        hours, minuts = t[:ind.end()-1], t[ind.end():]

        if not hours.isdecimal() or not minuts.isdecimal():
            return

        return int(hours)%24*60+int(minuts)%60


class MessageHelper:
    clear_murkup = types.ReplyKeyboardRemove()

    @staticmethod
    def start_markup():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Einen Timer hinzufugen")
        item2 = types.KeyboardButton("Timer loschen")
        markup.add(item1, item2)

        return markup

if __name__ == '__main__':
    assert 60 == Time.str_to_minuts("1:00")
    assert 125 == Time.str_to_minuts("2:5")
    assert 601 == Time.str_to_minuts("10 1")
    assert None == Time.str_to_minuts("10:asd")
    assert 0 == Time.str_to_minuts("24:0")
