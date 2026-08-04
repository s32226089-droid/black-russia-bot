import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import init_db, get_player, register_player
from keyboards import main_menu_keyboard

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class RegistrationState(StatesGroup):
    waiting_for_rp_name = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    player = get_player(message.from_user.id)
    if player:
        text = (
            f"🚘 **Добро пожаловать в BLACK RUSSIA RP!**\n\n"
            f"С возвращением, **{player['rp_name']}**!"
        )
        await message.answer(
            text,
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )
    else:
        text = (
            "🚘 **Добро пожаловать в проект BLACK RUSSIA RP**\n\n"
            "Для начала создайте своего персонажа.\n\n"
            "Введите ваш RP Никнейм в формате: `Имя_Фамилия`"
        )
        await message.answer(
            text,
            parse_mode="Markdown"
        )
        await RegistrationState.waiting_for_rp_name.set()

@dp.message_handler(state=RegistrationState.waiting_for_rp_name)
async def process_rp_name(message: types.Message, state: FSMContext):
    rp_name = message.text.strip()
    
    if "_" not in rp_name:
        await message.answer("❌ Неверный формат! Введите никнейм в формате: `Имя_Фамилия`", parse_mode="Markdown")
        return

    register_player(message.from_user.id, rp_name)
    await state.finish()
    
    text = (
        f"✅ **Персонаж {rp_name} успешно создан!**\n\n"
        f"Добро пожаловать в игру!"
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

if __name__ == '__main__':
    init_db()
    executor.start_polling(dp, skip_updates=True)
    
