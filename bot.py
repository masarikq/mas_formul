import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Сюда вставляй свой токен от BotFather
TOKEN = '7968435367:AAEC2UeLz7ldSn9-V7xoZ1HZUrzzlSsBj9I'

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
 
# Твоя база формул. 
# Слева системный ключ, а внутри — ["Надпись на кнопке", "Текст формулы"]
FORMULAS = {
    "lol1": ["Дискриминант", "🧮 Дискриминант квадратного уравнения: D = b**2 - 4*a*c"],
    "lol2": ["Виета", "лалала я её не помню"]
    # Когда пройдем новые темы, просто дописывай их сюда через запятую:
    # "integral": ["Интеграл", "∫ Интеграл по частям: ..."]
} 

# 1. Функция, которая срабатывает на команду /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    # Создаем список кнопок на основе нашего словаря
    buttons = []
    for key, (btn_text, formula_text) in FORMULAS.items():
        # Добавляем инлайн-кнопку с текстом и меткой (callback_data)
        buttons.append([InlineKeyboardButton(text=btn_text, callback_data=key)])
    
    # Собираем клавиатуру из кнопок
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    # Отправляем приветствие и прикрепляем клавиатуру
    await message.answer("Привет! Выбери нужную формулу из меню:", reply_markup=keyboard)

# 2. Функция, которая ловит нажатие на кнопку
@dp.callback_query()
async def button_handler(callback: CallbackQuery):
    # Узнаем, какой ключ был привязан к нажатой кнопке
    key = callback.data
    
    # Если такой ключ есть в нашей базе, отправляем формулу
    if key in FORMULAS:
        btn_text, formula_text = FORMULAS[key]
        await callback.message.answer(formula_text)
    
    # Обязательно "гасим" анимацию загрузки на кнопке в Telegram
    await callback.answer()

# 3. Главная функция запуска
async def main():
    await dp.start_polling(bot)

# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(main())