from aiogram import Bot
from aiogram.utils import executor
from aiogram.utils.exceptions import WrongFileIdentifier
from aiogram.types import ContentType, CallbackQuery, Message, InputFile
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from callback_data import state_callback, done_callback, scanning_callback
from config import token
from buttons import button_start
from models import Meme, User
from manager import text_scanning, check_photo, comparison_database
from scenario import mem_scene, DEFAULT_ANSWER
from states import DarkState

bot = Bot(token=token)
dpb = Dispatcher(bot, storage=MemoryStorage())

# -------------------------------------------------------------- Команды


@dpb.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.answer('Привет! Это бот по поиску мемов.\n'
                         'Так же ты можешь помочь нам и добавить новые мемы и их описание', reply_markup=button_start)
    User.user_update(message)
    await DarkState.STATE_OF_REST.set()


@dpb.message_handler(commands=['start'], state=DarkState)
async def start_command(message: Message, state: FSMContext):
    await message.answer('Привет! Это бот по поиску мемов.\n'
                         'Так же ты можешь помочь нам и добавить новые мемы и их описание', reply_markup=button_start)
    data = await state.get_data()
    if data:
        comparison_database(data)
    User.user_update(message)
    await state.finish()


@dpb.message_handler(commands=['count'], state=DarkState)
async def start_command(message: Message):
    count_mem = Meme.mem_count()
    count_u = User.user_count()
    await message.answer(f'количество мемов в боте на данный момент - {count_mem}.')
    await message.answer(f'количество пользователей, нажавших кнопку "/statr" - {count_u}.', reply_markup=button_start)


@dpb.message_handler(commands=['help'], state=DarkState)
async def help_command(message: Message):
    await message.answer('Я умею искать мемы, пока не очень хорошо.')

# -------------------------------------------------------------- Обработчики колбеков


@dpb.callback_query_handler(done_callback.filter(readily='ok'), state=DarkState)
async def done_state(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    Meme.insert_mem(data['file_id'], data['content'].lower())
    await call.answer(cache_time=60)
    await call.message.answer('Мем добавлен, спасибо за пополнение!', reply_markup=button_start)
    await DarkState.STATE_OF_REST.set()


@dpb.callback_query_handler(scanning_callback.filter(key_name='Сканировать'), state=DarkState)
async def determining_state(call: CallbackQuery, callback_data: dict, state: FSMContext):
    state_data = mem_scene[callback_data.get('key_name')]
    data = await state.get_data()
    text = text_scanning(data.get('file_id'))
    await call.answer(cache_time=60)
    if text.replace(' ', ''):
        await call.message.answer(f'Текст на фото:\n\n{text}')
        await call.message.answer(state_data['text_before'])
        await state_data['state'].set()
    else:
        await call.message.answer('Сканирование не дало результатов, введите текст с картинки')
        await state_data['state'].set()


@dpb.callback_query_handler(state_callback.filter(), state=DarkState)
async def determining_state(call: CallbackQuery, callback_data: dict):
    state_data = mem_scene[callback_data.get('key_name')]
    await call.answer(cache_time=60)
    await call.message.answer(state_data['text_before'])
    await state_data['state'].set()


@dpb.callback_query_handler(state_callback.filter())
async def determining_state(call: CallbackQuery, callback_data: dict):
    state_data = mem_scene[callback_data.get('key_name')]
    await call.answer(cache_time=60)
    await call.message.answer(state_data['text_before'])
    await state_data['state'].set()

# -------------------------------------------------------------- Обработчики состояний DarkState


@dpb.message_handler(state=DarkState.STATE_OF_REST, content_types=ContentType.PHOTO)
async def get_photo(message: Message, state: FSMContext):
    await message.photo[-1].download(f'MemeLibrary/{message.photo[-1]["file_id"]}.jpg')
    file_id = message.photo[-1]["file_id"]
    if check_photo(f'{file_id}.jpg'):
        await state.update_data(file_id=file_id)
        await message.answer(mem_scene['Добавить_мем']['text_after'], reply_markup=mem_scene['Добавить_мем']['button'])
    else:
        await message.answer('Такой мем уже есть, загрузите другой.')


@dpb.message_handler(state=DarkState.DESCRIPTION_STATE)
async def get_content(message: Message, state: FSMContext):
    content = message.text
    await state.update_data(content=content)
    await message.answer(mem_scene['Написать']['text_after'], reply_markup=mem_scene['Написать']['button'])


@dpb.message_handler(state=DarkState.SEARCH_STATE)
async def get_description(message: Message, state: FSMContext):
    res = Meme.get_mem_or_none(message.text)
    if res:
        for i in res:
            try:
                await message.answer_photo((i[0]))
            except WrongFileIdentifier:
                photo = InputFile(f'MemeLibrary/{i[0]}.jpg')
                await message.answer_photo(photo)
        await message.answer('поиск выполнен!', reply_markup=button_start)
    else:
        await message.answer('По вашему запросу нет результатов.', reply_markup=button_start)
    await state.finish()


@dpb.message_handler(state=DarkState.STATE_OF_REST)
async def everything_else(massage: Message):
    await massage.answer(DEFAULT_ANSWER['text'], reply_markup=DEFAULT_ANSWER['button'])


if __name__ == '__main__':
    executor.start_polling(dpb)
