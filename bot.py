import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message


API_TOKEN = '8430807966:AAEDzl2NZ1GCkL426tXo2Ii9NazxVODpDZ4'


bot = Bot(token=API_TOKEN)
dp = Dispatcher()


TASKS = [
    {"q": "У отца Мэри есть пять дочерей: Нана, Нене, Нини, Ноно. Как зовут пятую?", "a": "Мэри"},
    {"q": "Что можно увидеть с закрытыми глазами?", "a": "Сны"},
    {"q": "Чем больше из нее берешь, тем больше она становится. Что это?", "a": "Яма"},
    {"q": "Что всегда идет, но никогда не доходит?", "a": "Время"},
    {"q": "Шел муж с женой, брат с сестрой, да шурин с зятем. Сколько всего человек?", "a": "3"}
]


user_data = {}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    
    user_data[user_id] = {"finished": [], "current_task": None}
    
    first_name = message.from_user.first_name
    msg1 = (f"Привет, {first_name}! 👋\n"
            f"Я твой персональный учебный ассистент. Я помогу тебе закрепить знания "
            f"из нашего сборника задач на логику.\n"
            f"Надеемся, что ты готов начать обучение, удачи!🎓")
    
    msg2 = ("Вот что я могу:\n"
            "А) Выдать случайную задачку на логику\n"
            "Б) Проверить твой ответ и подобрать похожую задачку если ты ошибся\n"
            "Чтобы начать, нажми кнопочку /get или впиши ее вручную")
    
    await message.answer(msg1)
    await message.answer(msg2)

@dp.message(Command("get"))
async def cmd_get(message: Message):
    user_id = message.from_user.id
    
    
    if user_id not in user_data:
        user_data[user_id] = {"finished": [], "current_task": None}
    
    
    available_indices = [i for i in range(len(TASKS)) if i not in user_data[user_id]["finished"]]
    
    if not available_indices:
        await message.answer("Поздравляем, ты решил весь список доступных задач, если тебе мало, "
                             "то можешь поискать себе задачи по душе в нашем сборнике: PROстая логика")
        return

   
    task_index = random.choice(available_indices)
    user_data[user_id]["current_task"] = task_index
    
    await message.answer(f"Задача: {TASKS[task_index]['q']}")

@dp.message()
async def handle_answer(message: Message):
    user_id = message.from_user.id
    
    
    if user_id not in user_data or user_data[user_id]["current_task"] is None:
        return

    task_idx = user_data[user_id]["current_task"]
    correct_answer = TASKS[task_idx]["a"].lower()
    user_answer = message.text.strip().lower()

    if user_answer == correct_answer:
        await message.answer("Молодчина! ✅")
    else:
        await message.answer(f"Тебе надо больше тренироваться... ❌\nПравильный ответ: {TASKS[task_idx]['a']}")

    
    user_data[user_id]["finished"].append(task_idx)
    user_data[user_id]["current_task"] = None

    
    await cmd_get(message)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
