import config
import logging
import asyncio
from datetime import datetime
from print_task10 import Db_insert
from aiogram import Bot, Dispatcher, executor, types
from aiogram import types
from config import api_token

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.api_token)
dp = Dispatcher(bot)

#Эхо
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)#resize_keyboard=True
    item1=types.KeyboardButton(text="Рандомное задание")
    
    markup.add(item1)
    await message.answer('Добро пожаловать', reply_markup=markup)

@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    await message.answer('Ща пришлю')
    new_get_insert_from_db=Db_insert()
    new_str=new_get_insert_from_db.get_element_bot()
    print(new_str)
    if message.chat.type=='private':
        if message.text=="Рандомное задание":
            await message.answer('Номер задачи:     '+new_str[0][1]+'      . Название задачи:     '+new_str[0][3] )
            await message.answer('https://codeforces.com'+new_str[0][4])
            await message.answer('Сложность: '+new_str[0][5]+' . Тип задачи: ')
            await message.answer(new_str[0][6])
            await message.answer('Кол-во решений   ' +new_str[0][7]+'     и ссылка на них ')
            await message.answer('https://codeforces.com'+new_str[0][8])
            await message.answer('Это пока что все что я умею :( ')
            
    
   
    
    # for i in new_str:
    #     for j in i:
    #         await message.answer(j)



# async def scheduled(wait_for):
# 	while True:
# 		await asyncio.sleep(wait_for)


if __name__=='__main__':
    executor.start_polling(dp,skip_updates=True)
    #asyncio.run(scheduled(10))
   