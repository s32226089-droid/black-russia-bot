from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import JOBS, CARS, FACTIONS

def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("👤 Профиль / Статистика"), KeyboardButton("💼 Работы"))
    keyboard.add(KeyboardButton("🚗 Автосалон"), KeyboardButton("🏛️ Фракции"))
    keyboard.add(KeyboardButton("💬 RP Команды"), KeyboardButton("🏆 Топ Игроков"))
    return keyboard

def jobs_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for job_id, job in JOBS.items():
        text = f"{job['title']} (с {job['req_level']} lvl) — [{job['min_pay']}-{job['max_pay']} руб.]"
        keyboard.add(InlineKeyboardButton(text=text, callback_data=f"job_{job_id}"))
    keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main"))
    return keyboard

def dealership_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for car_id, car in CARS.items():
        text = f"🚘 {car['title']} | {car['price']:,} руб. ({car['class']} класс)"
        keyboard.add(InlineKeyboardButton(text=text, callback_data=f"buycar_{car_id}"))
    keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main"))
    return keyboard

def factions_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for faction_id, faction in FACTIONS.items():
        text = f"{faction['title']} (с {faction['req_level']} lvl) — ЗП: {faction['salary']} руб."
        keyboard.add(InlineKeyboardButton(text=text, callback_data=f"joinfaction_{faction_id}"))
    keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main"))
    return keyboard
