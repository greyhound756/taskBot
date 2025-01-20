import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import text

TOKEN = "YOUR API KEY"

bot = Bot(token=TOKEN)
dp = Dispatcher()

tasks = []

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(text.WELCOME)

@dp.message(Command("add"))
async def add_task(message: Message):
    task_text = message.text[len("/add "):].strip()
    if not task_text:
        await message.answer(text.ERROR)
        return
    tasks.append(task_text)
    await message.answer(f"✅ Задача добавлена:\n{task_text}")

@dp.message(Command("list"))
async def list_task(message: Message):
    if not tasks:
        await message.answer(text.ERROR2)
        return
    task_list = "\n".join([f"{i + 1}. {task}" for i, task in enumerate(tasks)])
    await message.answer(task_list)

@dp.message(Command("done"))
async def done_task(message: Message):
    try:
        task_index = int(message.text[len("/done "):].strip()) - 1
        if 0 <= task_index < len(tasks):
            completed_task = tasks.pop(task_index)
            await message.answer(f"✅ Задача выполнена:\n{completed_task}")
        else:
            await message.answer("❗ Неверный номер задачи. Проверьте список задач с помощью команды /list.")
    except (ValueError, IndexError):
        await message.answer("❗ Укажите корректный номер задачи. Пример:\n/done 1")

async def main():
    try:
        print("Бот запущен...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
