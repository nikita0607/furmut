#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telebot import TeleBot


class Bot(TeleBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users: Dict[int, User] = {}
        self.carusels: Dict[int, Carusel] = {}
