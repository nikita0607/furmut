#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import choice


class GoodWords:
    good_phrases = ["Du bist Susse", 
                    "Du bist beste Mutter!",
                    "Alles wird gut",
                    "Du bist die beste"]

    @staticmethod
    def get_good_phrase():
        return choice(GoodWords.good_phrases)
