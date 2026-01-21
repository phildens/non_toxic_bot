import os
import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Получаем настройки из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Обращаемся к контейнеру модели по его имени в docker-compose (model_api)
MODEL_API_URL = "http://model_api:8000/predict"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


async def check_toxicity(text):
    try:
        response = requests.post(MODEL_API_URL, json={"text": text})
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logging.error(f"Ошибка соединения с моделью: {e}")
    return None


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я модератор. Я слежу за токсичностью в этом чате.")


# Обработка всех текстовых сообщений
@dp.message(F.text)
async def moderate_messages(message: types.Message):
    data = await check_toxicity(message.text)

    if data:
        prob = data['toxic_probability']
        is_toxic = data['is_toxic']

        # Если вероятность токсичности > 80% (настраивается в API)
        if is_toxic:
            warning_text = (
                f"🚨 <b>Обнаружена токсичность!</b>\n"
                f"Вероятность: {prob:.2%}\n"
                f"Пожалуйста, будьте вежливее."
            )
            # Отвечаем на сообщение (reply)
            await message.reply(warning_text, parse_mode="HTML")

            # Можно удалять сообщение (раскомментируй, если бот админ)
            # await message.delete()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())