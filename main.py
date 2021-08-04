from aiogram import Bot
from aiogram.utils import executor
from aiogram.types import ContentType, CallbackQuery, Message
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from callback_data import state_callback, done_callback, scanning_callback
from config import TOKEN
from buttons import button_start
from models import Meme
from manager import text_scanning, check_photo
from scenario import add_mem, search_mem, DEFAULT_ANSWER
from states import AddMem, SearchMem

bot = Bot(token=TOKEN)
dpb = Dispatcher(bot, storage=MemoryStorage())

# -------------------------------------------------------------- Команды


@dpb.message_handler(commands=['start'])
async def start_command(message: Message, state: FSMContext):
    await message.answer('Привет! Это бот по поиску мемов.\n'
                         'Так же ты можешь помочь нам и добавить новые мемы и их описание', reply_markup=button_start)
    await state.finish()


@dpb.message_handler(commands=['help'])
async def help_command(message: Message):
    await message.answer('Я умею искать мемы, пока не очень хорошо.')

# -------------------------------------------------------------- Обработчики колбеков


@dpb.callback_query_handler(done_callback.filter(readily='ok'), state=AddMem)
async def done_state(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    Meme.insert_mem(data['file_id'], data['content'].lower())
    await call.answer(cache_time=60)
    await call.message.answer('Мем добавлен, спасибо за пополнение!')
    await state.finish()


@dpb.callback_query_handler(scanning_callback.filter(key_name='Сканировать'), state=AddMem)
async def determining_state(call: CallbackQuery, callback_data: dict, state: FSMContext):
    state_data = add_mem[callback_data.get('key_name')]
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


@dpb.callback_query_handler(state_callback.filter(), state=AddMem)
async def determining_state(call: CallbackQuery, callback_data: dict):
    state_data = add_mem[callback_data.get('key_name')]
    await call.answer(cache_time=60)
    await call.message.answer(state_data['text_before'])
    await state_data['state'].set()


@dpb.callback_query_handler(state_callback.filter())
async def determining_state(call: CallbackQuery, callback_data: dict):
    if callback_data.get('key_name') in add_mem:
        state_data = add_mem[callback_data.get('key_name')]
    else:
        state_data = search_mem[callback_data.get('key_name')]
    await call.answer(cache_time=60)
    await call.message.answer(state_data['text_before'])
    await state_data['state'].set()

# -------------------------------------------------------------- Обработчики состояний AddMem


@dpb.message_handler(state=AddMem.STATE_1, content_types=ContentType.PHOTO)
async def get_photo(message: Message, state: FSMContext):
    await message.photo[-1].download(f'MemeLibrary/{message.photo[-1]["file_id"]}.jpg')
    file_id = message.photo[-1]["file_id"]
    if check_photo(f'MemeLibrary/{file_id}.jpg'):
        await state.update_data(file_id=file_id)
        await message.answer(add_mem['Добавить_мем']['text_after'], reply_markup=add_mem['Добавить_мем']['button'])
    else:
        await message.answer('Такой мем уже есть, загрузите другой.')


@dpb.message_handler(state=AddMem.STATE_2)
async def get_content(message: Message, state: FSMContext):
    content = message.text
    await state.update_data(content=content)
    await message.answer(add_mem['Написать']['text_after'], reply_markup=add_mem['Написать']['button'])

# -------------------------------------------------------------- Обработчики состояний SearchMem


@dpb.message_handler(state=SearchMem.STATE_1)
async def get_description(message: Message, state: FSMContext):
    res = Meme.get_mem_or_none(message.text)
    if res:
        for i in res:
            await message.answer_photo(i[0])
        await message.answer('поиск выполнен!')
    else:
        await message.answer('По вашему запросу нет результатов.')
    await state.finish()

# -------------------------------------------------------------- Все остальные сообщения


@dpb.message_handler()
async def everything_else(massage: Message):
    await massage.answer(DEFAULT_ANSWER['text'], reply_markup=DEFAULT_ANSWER['button'])


if __name__ == '__main__':
    executor.start_polling(dpb)
