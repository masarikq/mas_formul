import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TOKEN = '7968435367:AAEC2UeLz7ldSn9-V7xoZ1HZUrzzlSsBj9I'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ТВОИ НОВЫЕ БАЗЫ ДАННЫХ ---

# База для Ангема (добавил ту самую шпаргалку по плоскостям)
ANGEM_FORMULAS = {
    "angem_type1": ["Тип 1: Прямая к каноническому", "Направляющий вектор прямой q ищется через векторное произведение нормалей n1 и n2."],
    "angem_type2": ["Тип 2: Уравнение плоскости", "Вектор нормали ищется как векторное произведение двух векторов, лежащих в плоскости. Формула: A(x-x0) + B(y-y0) + C(z-z0) = 0"]
}

# База для Матана
MATAN_FORMULAS = {
    "matan_limits": ["Пределы", "Первый замечательный предел: sin(x)/x = 1 при x -> 0."],
    "matan_derivatives": ["Таблица производных", "Производная от x^2 равна 2x."]
}

# --- 1. ГЛАВНОЕ МЕНЮ (/start) ---
@dp.message(CommandStart())
async def start_handler(message: Message):
    # Создаем жестко заданные кнопки для предметов
    buttons = [
        [InlineKeyboardButton(text="📐 Ангем", callback_data="subj_angem")],
        [InlineKeyboardButton(text="📈 Мат. анализ", callback_data="subj_matan")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выбери предмет, чтобы открыть шпоры:", reply_markup=keyboard)

# --- 2. ОБРАБОТКА ВЫБОРА ПРЕДМЕТА ---
# F.data.startswith("subj_") означает, что функция сработает, только если callback_data начинается с "subj_"
@dp.callback_query(F.data.startswith("subj_"))
async def subject_handler(callback: CallbackQuery):
    subject = callback.data
    buttons = []
    
    # Собираем меню в зависимости от выбранного предмета
    if subject == "subj_angem":
        for key, data in ANGEM_FORMULAS.items():
            buttons.append([InlineKeyboardButton(text=data[0], callback_data=key)])
        text = "Выбери тему по Ангему:"
        
    elif subject == "subj_matan":
        for key, data in MATAN_FORMULAS.items():
            buttons.append([InlineKeyboardButton(text=data[0], callback_data=key)])
        text = "Выбери тему по Мат. анализу:"

    # Обязательно добавляем кнопку "Назад" в главное меню
    buttons.append([InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    # edit_text меняет текущее сообщение с кнопками, чтобы не спамить новыми сообщениями в чат
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

# --- 3. КНОПКА "НАЗАД" ---
@dp.callback_query(F.data == "back_to_main")
async def back_handler(callback: CallbackQuery):
    # Восстанавливаем главное меню
    buttons = [
        [InlineKeyboardButton(text="📐 Ангем", callback_data="subj_angem")],
        [InlineKeyboardButton(text="📈 Мат. анализ", callback_data="subj_matan")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text("Выбери предмет, чтобы открыть шпоры:", reply_markup=keyboard)
    await callback.answer()

# --- 4. ВЫДАЧА САМОЙ ФОРМУЛЫ ---
# Этот хэндлер ловит все остальные нажатия (темы)
@dp.callback_query()
async def formula_handler(callback: CallbackQuery):
    key = callback.data
    
    # Ищем, в каком словаре лежит наша формула
    if key in ANGEM_FORMULAS:
        formula_text = ANGEM_FORMULAS[key][1]
        await callback.message.answer(formula_text)
    elif key in MATAN_FORMULAS:
        formula_text = MATAN_FORMULAS[key][1]
        await callback.message.answer(formula_text)
        
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())