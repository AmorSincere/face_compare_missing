import os
from pathlib import Path
from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from os.path import join as join_path

BTN_I_LOST = "I lost"
BTN_I_FOUND = "I found"
GUIDE_TEXT = "Upload pictures and press that is all button and wait"
BTN_THAT_IS_ALL = "that is all"
PHONE = '☎️'
PHONE_NUMBER_BUTTON_TEXT = F'{PHONE} share your number'
PHONE_NUMBER_BUTTON = KeyboardButton(text=PHONE_NUMBER_BUTTON_TEXT, request_contact=True)
BTN_STATE_PHONE = "add your number"


def teach_me():
    row1: List = [BTN_I_LOST]
    row2: List = [BTN_I_FOUND]
    row3: List = [BTN_STATE_PHONE]
    keyboard: List = [row1, row2, row3]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)
    return markup


def phone_number_markup():
    row1: List = [PHONE_NUMBER_BUTTON]
    row2: List = [BTN_THAT_IS_ALL]
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[row1, row2])
