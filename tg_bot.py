from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from pyexpat.errors import messages

api_key = '8035950847:AAFtrprDtZnv7n_ihZWLQ4SuzVqMjQ7iTPk'
bot = Bot(token=api_key)
dsp = Dispatcher(bot=bot, storage=MemoryStorage())

kb2 = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data='formulas')
kb2.add(button3)
kb2.add(button4)

kb3 = InlineKeyboardMarkup()
button6 = InlineKeyboardButton(text = 'Product1', callback_data='product_buying')
button7 = InlineKeyboardButton(text = 'Product2', callback_data='product_buying')
button8 = InlineKeyboardButton(text = 'Product3', callback_data='product_buying')
button9 = InlineKeyboardButton(text = 'Product4', callback_data='product_buying')
kb3.add(button6)
kb3.add(button7)
kb3.add(button8)
kb3.add(button9)

kb = ReplyKeyboardMarkup(resize_keyboard = True)
button = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
button5 = KeyboardButton(text = 'Купить')
kb.add(button5)
kb.add(button)
kb.add(button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dsp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = kb2)

@dsp.message_handler(text="Купить")
async def get_buying_list(message):
    with open('files/1.png', 'rb') as img:
        await message.answer_photo(img, 'Product1 - беспроигрышный выбор, замечателный аппарат для постоянного отслеживаня состояния вашего здоровья. \n Цена: 1000.')
    with open('files/2.png', 'rb') as img2:
        await message.answer_photo(img2, 'Product2 - приятные помошники для вашего иммунитета. \n Цена: 3500.')
    with open( 'files/3.png','rb') as img3:
        await message.answer_photo(img3, 'Product3 - великолепный уход для вашей кожи. \n Цена: 1200.')
    with open('files/4.png', 'rb') as img4:
        await message.answer_photo(img4, 'Product4 - о своем здоровье нужно заботиться не только физически, но и морально) \n Цена: 15600.')
    await message.answer('Выберите продукт для покупки:', reply_markup = kb3)

@dsp.callback_query_handler(text= ['product_buying'])
async def send_confirm_message(call):
    await  call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dsp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора: \n - для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5; \n - для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()

@dsp.callback_query_handler(text = 'calories')
async def set_age(call):
    print('Началась команда "Calories"')
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dsp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dsp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dsp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    weight = float(data['weight'])
    growth = float(data['growth'])
    age = float(data['age'])
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша норма калорий: {calories} ккал в сутки.')
    await state.finish()
    print('Выведено сообщение: Ваша норма калорий: {calories} ккал в сутки.')

@dsp.message_handler(commands=['start'])
async def start(message):
    print('Выведено сообщение: Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dsp.message_handler()
async def all_messages(message):
    print('Выведено сообщение: Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dsp, skip_updates=True)