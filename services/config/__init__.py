from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import md
from buttons.markup import teach_me
from dispatch import dp, bot


@dp.message_handler(commands="start")
async def start(message: types.Message, state: FSMContext):
    message_body = f"""Hi <a href="tg://user?id={message.from_user.id}">{md.quote_html(message.from_user.full_name)}</a>\nchoose"""
    await bot.send_message(text=message_body, chat_id=message.chat.id
                           , reply_markup=teach_me(), parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands="help")
async def help(message: types.Message):
    # some text in uzbek language
    message_body = "botga rasmlarni yuklagan topdim/yo'qotdim buyruqlarini qayta bosmang.  Aks holda avvalgi yuklagan rasmlaringiz o'chadi. Agar xato rasm yuklagan bo'lsangiz topdim/yo'qotdim buyrug'ini bosib qayta yuklashingiz mumkin. Topgan/yo'qotgan odam rasmlarni yuklagan bo'lsa sizga natijalarni dastur ko'rsatadi. Agar yuklamagan bo'lsa , yuklagan payti siz yuklagan rasmlarni u kishiga ko'rsatib sizga bo'glanish uchun malumotlaringiz beriladi.Topdim/yo'qotdim buyrug'ini bosib birdan ko'p rasmlar yuklashingiz mumkin. Admin:@amorsincere Birinchi rasm qo'shing bo'lmasa raqamingiz yozib olinmaydi!"
    await message.reply(message_body)
    url = r'https://images.unsplash.com/photo-1507027682794-35e6c12ad5b4?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1887&q=80'
    await bot.send_photo(chat_id=message.chat.id, photo=url)
