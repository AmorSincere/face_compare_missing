import asyncio
import sqlite3
import time
import os
from aiogram import md
from pathlib import Path
from os.path import join as join_path
from pathlib import Path
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup
import requests

from buttons.markup import teach_me, BTN_I_LOST, GUIDE_TEXT, BTN_THAT_IS_ALL, BTN_I_FOUND, PHONE_NUMBER_BUTTON, \
    phone_number_markup, BTN_STATE_PHONE
from configs.constants import TOKEN

from dispatch import dp, bot
from finderMissingPeople import is_found
from services import gen_code, add_image_to_user, found_person, clear_images_of_user

from services.config import *
from states import StartStates

BASE_URL = Path(__file__).parent.parent


@dp.message_handler(content_types=['text'])
async def main_handler_function(message: types.Message):
    if message.text == BTN_I_LOST:
        clear_images_of_user(message.from_user.id)
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(BTN_THAT_IS_ALL)
        await message.answer(GUIDE_TEXT, reply_markup=markup)
        await StartStates.i_lost.set()
    elif message.text == BTN_I_FOUND:
        clear_images_of_user(message.from_user.id)
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(BTN_THAT_IS_ALL)
        await message.answer(GUIDE_TEXT, reply_markup=markup)
        await StartStates.i_found.set()
    elif message.text == BTN_STATE_PHONE:
        await message.answer("add your number so ones can connect to you easy",
                             reply_markup=phone_number_markup())
        await StartStates.number.set()
    else:
        await message.answer(message.text)


@dp.message_handler(state=StartStates.i_lost,
                    content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT, 'text'])
async def i_lost_handler(message: types.Message, state: FSMContext):
    if message.text != BTN_THAT_IS_ALL:
        if message.photo:
            file_id = message.photo[-1].file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info['file_path']
            kode = gen_code(file_path)
            folder = join_path(BASE_URL, 'db', 'pictures', 'lost_people', kode)
            file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
            r = requests.get(file_url, stream=True)
            with open(folder, "wb") as Pypdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        Pypdf.write(chunk)
            await add_image_to_user(message, join_path('db', 'pictures', 'lost_people', kode))
            await message.answer('sent successfully to the bot')

        if message.document:
            kode = gen_code(message.document.file_name)
            folder = join_path(BASE_URL, 'db', 'pictures', 'lost_people')
            file_id = message.document.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info['file_path']
            file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
            r = requests.get(file_url, stream=True)
            with open(join_path(folder, kode), "wb") as Pypdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        Pypdf.write(chunk)
            await add_image_to_user(message, join_path('db', 'pictures', 'lost_people', kode))
            await message.answer('sent successfully to the bot')

    else:
        my_list = found_person(message.from_user.id, is_lost=True)
        results = is_found(my_list)
        if results:
            await message.answer('some results there!')
            results = set(results)
            for i in results:
                with open(join_path(BASE_URL, i), 'rb') as file:
                    await message.answer_photo(photo=file, caption='is not this?')
                connect = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute('SELECT ImageId FROM Pictures WHERE ImagePath=(?);', [i, ])
                cur_res = cursor.fetchone()
                userId = cur_res[0]
                cursor.execute('SELECT Name,PhoneNumber,fullname,username FROM Users WHERE UserId=(?);', [userId, ])
                cur_res = cursor.fetchone()
                user_id = cur_res[0]
                phone_number = cur_res[1]
                fullname = cur_res[2]
                username = cur_res[3]
                connect.close()
                text = f'username: @{username}\nphone-number: {phone_number}\nfullname: {md.quote_html(fullname)}'
                text += f'\nid: <a href="tg://user?id={user_id}">{user_id}</a>'
                await bot.send_message(message.from_user.id, text=text, parse_mode="html")

        else:
            await message.answer('not found same ones')
        await state.finish()
        await message.answer('choose', reply_markup=teach_me())


@dp.message_handler(state=StartStates.i_found,
                    content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT, 'text'])
async def i_found_handler(message: types.Message, state: FSMContext):
    if message.text != BTN_THAT_IS_ALL:
        if message.photo:
            file_id = message.photo[-1].file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info['file_path']
            kode = gen_code(file_path)
            print(kode)
            folder = join_path(BASE_URL, 'db', 'pictures', 'found_people', kode)
            file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
            r = requests.get(file_url, stream=True)
            with open(folder, "wb") as Pypdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        Pypdf.write(chunk)
            await add_image_to_user(message, join_path('db', 'pictures', 'found_people', kode))
            await message.answer('sent successfully to the bot! ')

        if message.document:
            kode = gen_code(message.document.file_name)
            folder = join_path(BASE_URL, 'db', 'pictures', 'found_people')
            file_id = message.document.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info['file_path']
            file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
            r = requests.get(file_url, stream=True)
            print(join_path(folder, kode))
            with open(join_path(folder, kode), "wb") as Pypdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        Pypdf.write(chunk)
            await add_image_to_user(message, join_path('db', 'pictures', 'found_people', kode))
            await message.answer('sent successfully to the bot! ')

    else:
        await message.answer("now we check results do not press buttons until result(not found/found)",
                             reply_markup=teach_me())
        my_list = found_person(message.from_user.id, is_lost=False)
        results = is_found(my_list)
        if results:
            results = set(results)
            for i in results:
                connect = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute('SELECT ImageId FROM Pictures WHERE ImagePath=(?);', [i, ])
                cur_res = cursor.fetchone()
                userId = cur_res[0]
                cursor.execute('SELECT Name,PhoneNumber,fullname,username FROM Users WHERE UserId=(?);', [userId, ])
                cur_res = cursor.fetchone()
                user_id = cur_res[0]
                phone_number = cur_res[1]
                fullname = cur_res[2]
                username = cur_res[3]
                connect.close()
                text = f'username: @{username}\nphone-number: {phone_number}\nfullname:  {md.quote_html(fullname)}'
                text += f'\nid: <a href="tg://user?id={user_id}">{user_id}</a>'
                await bot.send_message(message.from_user.id, text=text, parse_mode="html")
                with open(join_path(BASE_URL, i), 'rb') as file:
                    await message.answer_photo(photo=file, caption="isn't it?")
        else:
            await message.answer('not found same ones')
        await state.finish()


# taking number

@dp.message_handler(content_types=[types.ContentType.CONTACT, 'text'], state=StartStates.number)
async def phone_number(message: types.Message, state: FSMContext):
    # todo do some checks
    if message.text == BTN_THAT_IS_ALL:
        await state.finish()
        await message.bot.send_message(text="choose:",
                                       chat_id=message.from_user.id,
                                       reply_markup=teach_me())
    elif message.contact:
        print("PHONE CONTACT: ", message.contact)
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET PhoneNumber=(?) WHERE Name=(?);',
                       [message.contact['phone_number'], message.contact['user_id'], ])
        connect.commit()
        connect.close()
        await state.finish()
        await message.bot.send_message(text="your number added!",
                                       chat_id=message.chat.id,
                                       reply_markup=teach_me())
