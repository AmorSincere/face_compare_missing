import os
import sqlite3
from os.path import join as join_path
from pathlib import Path
from aiogram import types
from uuid import uuid4

BASE_URL = Path(__file__).parent.parent


def gen_code(filename):
    filename = filename.split('.')[-1]
    kode = str(uuid4())
    kode = kode.replace('-', '')
    kode = kode + '.' + filename
    return kode


async def add_image_to_user(message: types.Message, folder):
    full_name = message.from_user.full_name
    user_id = str(message.from_user.id)
    phone = 'aniqlanmagan'
    username = message.from_user.username
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute('SELECT Name FROM Users WHERE Name=(?);', [user_id, ])
    cur_res = cursor.fetchall()
    has_user = False
    for i in cur_res:
        if i[0] == user_id:
            has_user = True
    if not has_user:
        print('if ga tushdi!')
        cursor.execute("""INSERT INTO Users(Name,PhoneNumber,fullname,username) VALUES(?,?,?,?)""",
                       [user_id, phone, full_name, username])
        connect.commit()
    cursor.execute('SELECT UserID FROM Users WHERE Name=(?);', [user_id, ])
    ImageId = int(cursor.fetchone()[0])
    cursor.execute("""INSERT INTO Pictures(ImageId,ImagePath) VALUES(?,?)""", [ImageId, folder])
    connect.commit()
    connect.close()


def found_person(user_id, is_lost: bool):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT UserId FROM Users WHERE Name=(?)", [user_id, ])
    cur_res = cursor.fetchall()
    if cur_res:
        ImageId = cur_res[0][0]
    else:
        ImageId = 0
    cursor.execute("SELECT ImagePath FROM Pictures WHERE ImageId=(?)", [ImageId, ])
    cur_res = cursor.fetchall()
    connect.close()
    pictures_list = []
    print('it gathered user pics')
    if cur_res:
        for i in cur_res:
            pictures_list.append(i[0])
    return [pictures_list, user_id, is_lost]


def clear_images_of_user(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT UserId FROM Users WHERE Name=(?)", [user_id, ])
    cur_res = cursor.fetchall()
    print(cur_res)
    if cur_res:
        ImageId = cur_res[0][0]
    else:
        ImageId = 0
    cursor.execute("SELECT ImagePath FROM Pictures WHERE ImageId==(?)", [ImageId, ])
    cur_res = cursor.fetchall()
    if cur_res:
        for i in cur_res:
            os.remove(join_path(BASE_URL, i[0]))
    cursor.execute("""DELETE FROM Pictures WHERE ImageId==(?)""", (ImageId,))
    connect.commit()
    connect.close()
    print('deleted')
