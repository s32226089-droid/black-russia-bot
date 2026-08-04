import os

# Telegram Bot Token (получить у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "BOT_TOKEN = "8944459806:AAE1576thEANwW1RP6jQxJ90EKrV4k0hfgc"
")

# Настройки базы данных
DB_PATH = "black_russia.db"

# Начальные параметры игрока
START_MONEY = 10000
START_EXP = 0
START_LEVEL = 1

# Экономика и настройки работ
JOBS = {
    "mine": {"title": "⛏️ Шахта", "req_level": 1, "min_pay": 1500, "max_pay": 3500, "exp": 2, "cooldown": 30},
    "factory": {"title": "🏭 Завод", "req_level": 2, "min_pay": 4000, "max_pay": 7000, "exp": 3, "cooldown": 60},
    "courier": {"title": "🛵 Курьер", "req_level": 3, "min_pay": 8000, "max_pay": 12000, "exp": 5, "cooldown": 120},
    "trucker": {"title": "🚛 Дальнобойщик", "req_level": 5, "min_pay": 25000, "max_pay": 45000, "exp": 10, "cooldown": 300},
}

# Автосалон (Автомобили)
CARS = {
    "vaz2107": {"title": "ВАЗ 2107", "price": 120000, "class": "Низкий"},
    "bmw_e30": {"title": "BMW E30", "price": 350000, "class": "Низкий"},
    "bmw_m5_e39": {"title": "BMW M5 E39", "price": 850000, "class": "Средний"},
    "skyline_r34": {"title": "Nissan Skyline R34", "price": 1800000, "class": "Средний"},
    "mercedes_amg_gt": {"title": "Mercedes-AMG GT", "price": 6500000, "class": "Высокий"},
    "bugatti_chiron": {"title": "Bugatti Chiron", "price": 25000000, "class": "Высокий"},
}

# Фракции
FACTIONS = {
    "gov": {"title": "🏛️ Правительство", "req_level": 3, "salary": 8000},
    "gibdd": {"title": "🚔 ГИБДД", "req_level": 4, "salary": 12000},
    "umvd": {"title": "🚔 УМВД", "req_level": 4, "salary": 12000},
    "opg_arz": {"title": "🗡️ ОПГ Арзамас", "req_level": 2, "salary": 10000},
    "opg_bat": {"title": "🗡️ ОПГ Батырево", "req_level": 2, "salary": 10000},
}
