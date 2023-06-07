import logging
import requests
from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
from config import *
from filters import *
from keyboards import *


logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)

dp = Dispatcher(bot)


@dp.message_handler(IsAdmin(), commands='start')
async def start(message: Message):
    await message.answer("You can get movie in one click!", reply_markup=MainMenu())


@dp.callback_query_handler(text='random')
async def get_random(call: CallbackQuery):
    await call.answer()
    r = requests.get(url=url+'v1/movie/random', headers=header)
    print(r.json())
    if r.status_code == 200:
        title = r.json()['name']
        description = r.json()['description']
        year = r.json()['year']
        rating_kp = r.json()['rating']['kp']
        rating_imbd = r.json()['rating']['imdb']
        poster = r.json()["poster"]["url"]
        await call.message.answer_photo(poster, caption=f'Here is your random film!\n'
                                  f'Название: {title}\n'
                                  f'Описание: {description}\n'
                                  f'Год выпуска: {year}\n'
                                  f'Оценка на КП: {rating_kp}\n'
                                  f'Оценка на IMDB: {rating_imbd}', reply_markup=MovieMenu())

''' WORK IN PROGRESS
@dp.callback_query_handler(text='reviews')
async def get_reviews(call: CallbackQuery):
    await call.answer()
    r = requests.get(url=url + 'v1/review?page=1&limit=5', headers=header)
    if r.status_code == 200:
        r = r.json()['docs']
        for rw in r:
            id = rw['movieId']
            r_film = requests.get(url=url + 'v1.3/movie/' + str(id), headers=header)
            title_film = r_film.json()['name']
            title = rw['title']
            author = rw['author']
            review = rw['review']
            await call.message.answer(f'Фильм: {title_film}\n'
                                      f'Заголовок: {title}\n'
                                      f'Автор: {author}\n'
                                      f'Отзыв: {review}')
'''

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)