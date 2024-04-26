import asyncio

import aiosqlite
import telebot.apihelper
from telebot.async_telebot import AsyncTeleBot


bot = AsyncTeleBot()


async def setup():
    async with aiosqlite.connect("database_for_tg.db") as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS tg_ids (id INTEGER PRIMARY KEY UNIQUE NOT NULL)"
        )


async def create_id(message_id):
    async with aiosqlite.connect("database_for_tg.db") as db:
        await db.execute("INSERT INTO tg_ids (id) VALUES (?)", (message_id,))
        await db.commit()


async def all_tg_ids():
    async with aiosqlite.connect("database_for_tg.db") as db:
        async with db.execute("SELECT id FROM tg_ids") as cursor:
            res = []
            async for row in cursor:
                res.append(row[0])
            return res


@bot.message_handler(commands=["start"])
async def start(message):
    await create_id(message_id=message.chat.id)
    await bot.send_message(
        message.chat.id,
        f"""Привет {message.from_user.first_name}! Я отправлю вам заявку при поступлений!""",
    )


async def get_application(application: str):
    ids = await all_tg_ids()
    try:
        for idx in ids:
            print(idx)
            await bot.send_message(chat_id=idx, text=application, parse_mode="html")
    except telebot.apihelper.ApiTelegramException as e:
        print(e, idx)
    # try:
    #     await bot.send_message(chat_id=883371538, text=application, parse_mode="html")
    # except telebot.apihelper.ApiTelegramException as e:
    #     print(e)


if __name__ == "__main__":
    asyncio.run(bot.polling())
    # asyncio.run(setup())
    # asyncio.run(all_tg_ids())
