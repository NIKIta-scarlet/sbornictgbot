import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

# Вставьте ваш токен сюда
API_TOKEN = '8430807966:AAEDzl2NZ1GCkL426tXo2Ii9NazxVODpDZ4'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Список задач (вопрос и ответ)
TASKS = [
    {"q": "Когда сломался компьютер, его Хозяин сказал: «Память не могла выйти из строя». Его сын предположил, что сгорел процессор, а винчестер исправен. Мастер по ремонту сказал, что с процессором все в порядке, а память неисправна. В результате оказалось, что двое из них сказали все верно, а третий – все неверно. Что же сломалось?", "a": "Память"},
    {"q": "В некотором месте есть только три деревни: Правдино, Кривдино и Серединка Наполовинку. Соответственно, жители первой всегда говорят правду, жители второй – всегда лгут, а в Серединке-Наполовинку часть жителей всегда честные, часть – всегда лгуны. Вы – пожарный, который сидит в пожарном участке, откуда этих трех деревень не видно. Раздается телефонный звонок, вы берете трубку. У нас в деревне пожар. – А где вы живете? – В Серединке-Наполовинку. В какую деревню необходимо ехать пожарному? Кто звонил?", "a": "Серединку-Наполовинку"},
    {"q": "Семеро друзей – Антонов, Борисов, Васильев, Глебов, Дмитриев, Егоров и Иванов –- по странному стечению обстоятельств имеют совпадающие имена, причем ни один из них не является тезкой своей фамилии. Кроме того, о них известно следующее: – Все, кроме Антонова и Глебова, уже женаты. – Невесте Егора очень не нравится фамилия ее жениха. – Фамилия Глеба совпадает с именем Иванова. – Жены Дмитриева и Ивана – родные сестры. – Тот, чье имя совпадает с фамилией Бориса, женат, и его фамилия совпадает с именем Егорова. – Иван, Егор и Василий – брюнеты. – Остальные четверо, в числе которых Иванов, Егоров и Васильев, – блондины. Как фамилия Василия?", "a": "Дмитриев"},
    {"q": "На острове Контрастов живут рыцари и лжецы. Рыцари всегда говорят правду, лжецы всегда лгут. Некоторые жители заявили, что на острове чётное число рыцарей, а остальные заявили, что на острове нечётное число лжецов. Может ли число жителей острова быть нечётным", "a": "Нет"},
    {"q": "В семье четверо детей, причем все мальчики в ней (если таковые есть) лгут, а все девочки (если таковые есть) говорят правду. 1-й ребенок сказал: «У меня сестер и братьев поровну»; 2-й: «У меня ровно один брат»; 3-й: «У меня ровно два брата»; 4-й: «У меня ровно две сестры». Определите, сколько в этой семье мальчиков", "a": "2 мальчика и 2 девочки"}
]

# Хранилище прогресса (в памяти)
user_data = {}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    # Сброс прогресса при старте
    user_data[user_id] = {"finished": [], "current_task": None}
    
    first_name = message.from_user.first_name
    
    photo_url = 'https://vk.com/club237429724?z=photo-237429724_457239018%2F7f6b50b77953b75d13'

    await message.answer_photo(
        photo=photo_url,)
    
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
    
    # Инициализация данных пользователя, если их нет
    if user_id not in user_data:
        user_data[user_id] = {"finished": [], "current_task": None}
    
    # Список доступных индексов задач
    available_indices = [i for i in range(len(TASKS)) if i not in user_data[user_id]["finished"]]
    
    if not available_indices:
        await message.answer("Поздравляем, ты решил весь список доступных задач, если тебе мало, "
                             "то можешь поискать себе задачи по душе в нашем сборнике: https://vk.com/club237429724")
        return

    # Выбираем случайную новую задачу
    task_index = random.choice(available_indices)
    user_data[user_id]["current_task"] = task_index
    
    await message.answer(f"Задача: {TASKS[task_index]['q']}")

@dp.message()
async def handle_answer(message: Message):
    user_id = message.from_user.id
    
    # Проверяем, есть ли активная задача
    if user_id not in user_data or user_data[user_id]["current_task"] is None:
        return

    task_idx = user_data[user_id]["current_task"]
    correct_answer = TASKS[task_idx]["a"].lower()
    user_answer = message.text.strip().lower()

    if user_answer == correct_answer:
        await message.answer("Молодчина! ✅")
    else:
        await message.answer(f"Тебе надо больше тренироваться... ❌\nПравильный ответ: {TASKS[task_idx]['a']}")

    # Помечаем задачу как решенную
    user_data[user_id]["finished"].append(task_idx)
    user_data[user_id]["current_task"] = None

    # Автоматически предлагаем следующую задачу
    await cmd_get(message)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
