import os
import time
import random
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN, JOBS, CARS, FACTIONS
from database import init_db, get_player, register_player, update_player
from keyboards import main_menu_keyboard, jobs_keyboard, dealership_keyboard, factions_keyboard

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class RegistrationState(StatesGroup):
    waiting_for_rp_name = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    player = get_player(message.from_user.id)
    if player:
        await message.answer(
            f"🚘 **Добро пожаловать в BLACK RUSSIA RP!**

С возвращением, **{player['rp_name']}**!",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )
    else:
        await message.answer(
            "🚘 **Добро пожаловать в проект BLACK RUSSIA RP (Telegram Edition)!**

"
            "Для начала создайте своего персонажа.
"
            "Введите ваш RP Никнейм в формате: `Имя_Фамилия` (например, `Ivan_Ivanov`):",
            parse_mode="Markdown"
        )
        await RegistrationState.waiting_for_rp_name.set()

@dp.message_handler(state=RegistrationState.waiting_for_rp_name)
async def process_rp_name(message: types.Message, state: FSMContext):
    rp_name = message.text.strip()
    if "_" not in rp_name or len(rp_name.split("_")) != 2:
        await message.answer("❌ Неверный формат! Введите никнейм в формате `Имя_Фамилия` (например, `Sasha_White`):", parse_mode="Markdown")
        return
    
    register_player(message.from_user.id, message.from_user.username or "Player", rp_name)
    await state.finish()
    await message.answer(
        f"✅ **Персонаж {rp_name} успешно создан!**
"
        f"Вам зачислен стартовый бонус: **10 000 руб.**

"
        "Используйте меню ниже для игры:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

@dp.message_handler(lambda msg: msg.text == "👤 Профиль / Статистика")
async def show_profile(message: types.Message):
    player = get_player(message.from_user.id)
    if not player:
        return await message.answer("Зарегистрируйтесь через /start")
    
    req_exp = player['level'] * 5
    profile_text = (
        f"📊 **ПАСПОРТ ИГРОКА | BLACK RUSSIA**
"
        f"➖➖➖➖➖➖➖➖➖➖
"
        f"👤 **Никнейм:** `{player['rp_name']}`
"
        f"⭐ **Уровень:** `{player['level']}` [{player['exp']}/{req_exp} EXP]
"
        f"💵 **Наличные:** `{player['money']:,} руб.`
"
        f"🏦 **Банковский счет:** `{player['bank_money']:,} руб.`
"
        f"🚘 **Автомобиль:** `{player['car']}`
"
        f"🏛️ **Организация:** `{player['faction']}`
"
        f"➖➖➖➖➖➖➖➖➖➖"
    )
    await message.answer(profile_text, parse_mode="Markdown")

@dp.message_handler(lambda msg: msg.text == "💼 Работы")
async def show_jobs(message: types.Message):
    await message.answer("💼 **Выберите доступную работу:**", parse_mode="Markdown", reply_markup=jobs_keyboard())

@dp.callback_query_handler(lambda c: c.data.startswith('job_'))
async def process_job_work(callback: types.CallbackQuery):
    job_id = callback.data.split('_')[1]
    job = JOBS.get(job_id)
    player = get_player(callback.from_user.id)

    if not player:
        return await callback.answer("Ошибка доступа.", show_alert=True)

    if player['level'] < job['req_level']:
        return await callback.answer(f"❌ Для этой работы нужен {job['req_level']} уровень!", show_alert=True)

    now = int(time.time())
    cooldown = job['cooldown']
    if now - player['last_work_time'] < cooldown:
        rem = cooldown - (now - player['last_work_time'])
        return await callback.answer(f"⏳ Вы устали! Отдохните еще {rem} секунд.", show_alert=True)

    pay = random.randint(job['min_pay'], job['max_pay'])
    new_money = player['money'] + pay
    new_exp = player['exp'] + job['exp']
    req_exp = player['level'] * 5

    new_level = player['level']
    if new_exp >= req_exp:
        new_level += 1
        new_exp = 0
        await bot.send_message(callback.from_user.id, f"🎉 **ПОЗДРАВЛЯЕМ!** Вы получили `{new_level}` уровень!", parse_mode="Markdown")

    update_player(callback.from_user.id, money=new_money, exp=new_exp, level=new_level, last_work_time=now)
    await callback.answer(f"✅ Вы отработали смену на {job['title']}!
+ Заработано: {pay:,} руб.
+ Опыт: {job['exp']} EXP", show_alert=True)

@dp.message_handler(lambda msg: msg.text == "🚗 Автосалон")
async def show_dealership(message: types.Message):
    await message.answer("🚗 **Автосалон области:**", parse_mode="Markdown", reply_markup=dealership_keyboard())

@dp.callback_query_handler(lambda c: c.data.startswith('buycar_'))
async def process_buy_car(callback: types.CallbackQuery):
    car_id = callback.data.split('_')[1]
    car = CARS.get(car_id)
    player = get_player(callback.from_user.id)

    if player['money'] < car['price']:
        return await callback.answer("❌ У вас недостаточно денег!", show_alert=True)

    new_money = player['money'] - car['price']
    update_player(callback.from_user.id, money=new_money, car=car['title'])
    await callback.answer(f"🎉 Поздравляем! Вы купили {car['title']}!", show_alert=True)
    await bot.send_message(callback.from_user.id, f"🚘 **Вы успешно приобрели автомобиль:** {car['title']} за `{car['price']:,} руб.`", parse_mode="Markdown")

@dp.message_handler(lambda msg: msg.text == "🏛️ Фракции")
async def show_factions_menu(message: types.Message):
    await message.answer("🏛️ **Государственные и нелегальные организации:**", parse_mode="Markdown", reply_markup=factions_keyboard())

@dp.callback_query_handler(lambda c: c.data.startswith('joinfaction_'))
async def process_join_faction(callback: types.CallbackQuery):
    faction_id = callback.data.split('_')[1]
    faction = FACTIONS.get(faction_id)
    player = get_player(callback.from_user.id)

    if player['level'] < faction['req_level']:
        return await callback.answer(f"❌ Требуется {faction['req_level']} уровень!", show_alert=True)

    update_player(callback.from_user.id, faction=faction['title'])
    await callback.answer(f"✅ Вы вступили в фракцию {faction['title']}!", show_alert=True)

@dp.message_handler(lambda msg: msg.text == "💬 RP Команды")
async def show_rp_help(message: types.Message):
    text = (
        "💬 **RP Команды игрового процесса:**

"
        "1️⃣ `/me [действие]` — совершить действие от 1-го лица.
"
        "   *Пример:* `/me достал документы из кармана`

"
        "2️⃣ `/do [описание]` — описание состояния окружающей среды.
"
        "   *Пример:* `/do Паспорт находится в правой руке.`

"
        "3️⃣ `/try [действие]` — попытаться совершить действие (Успешно/Неуспешно).
"
        "   *Пример:* `/try завел двигатель ВАЗ 2107`"
    )
    await message.answer(text, parse_mode="Markdown")

@dp.message_handler(commands=['me', 'do', 'try'])
async def handle_rp_commands(message: types.Message):
    player = get_player(message.from_user.id)
    if not player:
        return
    
    cmd = message.get_command()
    args = message.get_args()
    if not args:
        return await message.answer(f"Использование: `{cmd} [текст]`", parse_mode="Markdown")

    if cmd == "/me":
        await message.answer(f"🟣 *{player['rp_name']}* {args}", parse_mode="Markdown")
    elif cmd == "/do":
        await message.answer(f"🔹 {args} (( *{player['rp_name']}* ))", parse_mode="Markdown")
    elif cmd == "/try":
        res = random.choice(["✅ УСПЕШНО", "❌ НЕУСПЕШНО"])
        await message.answer(f"🎲 *{player['rp_name']}* {args} | [{res}]", parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data == "back_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, "Главное меню:", reply_markup=main_menu_keyboard())

if __name__ == "__main__":
    init_db()
    print("🚀 Сервер Black Russia Bot успешно запущен!")
    executor.start_polling(dp, skip_updates=True)
