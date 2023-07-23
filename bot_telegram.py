import os
import re

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class WaitingForPattern(StatesGroup):
    pattern = State()


storage = MemoryStorage()
waiting_for_pattern = WaitingForPattern.pattern
#Для работы с тестами, необходимо задать токен напрямую, чтобы это выглядело так: bot = Bot(token='ваш токен')
bot = Bot(token=os.environ.get('TOKEN'))
dp = Dispatcher(bot, storage=storage)
# Получаем id админа
with open('admin_id.txt', encoding='utf-8') as file:
    admin_chat_id = int(file.read())


# Метод, проверящий, является ли пользователь админом
async def check_admin(chat_id: int, user_id: int, admin_chat_id: int) -> bool:
    user = await bot.get_chat_member(chat_id, user_id)
    return str(user.user.id) == str(admin_chat_id)


@dp.message_handler(commands=['start'], chat_type=types.ChatType.PRIVATE)
async def start(msg: types.Message):
    # Проверяем, является ли пользователь админом
    if not await check_admin(msg.chat.id, msg.from_user.id, admin_chat_id):
        await bot.send_message(msg.chat.id, "Команда доступна только администратору.")
        return
    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    # Добавляем кнопку "/addpattern"
    add_pattern_button = KeyboardButton('/add_pattern')
    keyboard.add(add_pattern_button)

    # Добавляем кнопку "/removepattern"
    remove_pattern_button = KeyboardButton('/remove_pattern')
    keyboard.add(remove_pattern_button)

    # Отправляем клавиатуру пользователю
    await bot.send_message(chat_id=admin_chat_id, text="Выберите команду:", reply_markup=keyboard)


# Загрузка шаблонов регулярных выражений
def load_regex_patterns():
    regex_list = []
    with open('conf_data_templates.txt', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # Удаляем начальные и конечные пробелы и символы новой строки
            if line and not line.startswith('#'):  # Если строка не пустая и не начинается с '#'
                pattern = line.split('#', 1)[0].strip()  # Удаляем комментарии после символа '#'
                regex_list.append(pattern)
    return regex_list


# Сохранение шаблонов регулярных выражений
def save_regex_patterns(regex_list):
    with open('conf_data_templates.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(regex_list))


# Обработчик команды /addpattern
@dp.message_handler(commands=['add_pattern'], chat_type=types.ChatType.PRIVATE)
async def add_pattern(msg: types.Message):
    # Проверяем, является ли пользователь админом
    if not await check_admin(msg.chat.id, msg.from_user.id, admin_chat_id):
        await bot.send_message(msg.chat.id, "Команда доступна только администратору.")
        return

    # Устанавливаем состояние для ожидания нового шаблона
    await msg.answer('Введите новый шаблон регулярного выражения:')
    await waiting_for_pattern.set()


# Обработчик текстового сообщения после команды /addpattern
@dp.message_handler(state=waiting_for_pattern)
async def process_pattern(msg: types.Message, state: FSMContext):
    pattern = msg.text
    try:
        re.compile(pattern)  # Проверяем, что шаблон является действительным регулярным выражением
    except re.error:
        await msg.reply('Введенное значение не является действительным регулярным выражением. Попробуйте еще раз.')
        return
    # Проверяем, что шаблон регулярного выражения еще не существует
    regex_list = load_regex_patterns()
    if pattern in regex_list:
        await msg.reply(f'Шаблон "{pattern}" уже существует. Введите другой шаблон')
        return
    # Добавляем новый шаблон в список
    regex_list.append(pattern)
    save_regex_patterns(regex_list)
    await state.finish()
    await msg.reply(f'Шаблон "{pattern}" успешно добавлен.')


# Обработчик команды /remove_pattern
@dp.message_handler(commands=['remove_pattern'], chat_type=types.ChatType.PRIVATE)
async def remove_pattern(msg: types.Message):
    # Проверяем, является ли пользователь админом
    if not await check_admin(msg.chat.id, msg.from_user.id, admin_chat_id):
        await bot.send_message(msg.chat.id, "Команда доступна только администратору.")
        return
    # Загружаем текущие шаблоны
    regex_list = load_regex_patterns()

    # Создаем инлайн-клавиатуру с кнопками для удаления шаблонов
    keyboard = InlineKeyboardMarkup()
    for pattern in regex_list:
        button = InlineKeyboardButton(text=f"Удалить: {pattern}", callback_data=f"remove_pattern:{pattern}")
        keyboard.add(button)
    await msg.reply("Выберите шаблон, который необходимо удалить:", reply_markup=keyboard)



# Обработчик нажатия на кнопку удаления шаблона
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('remove_pattern:'))
async def process_remove_pattern(callback_query: types.CallbackQuery):
    pattern = callback_query.data.split(':')[1]

    # Проверяем, что шаблон существует
    regex_list = load_regex_patterns()
    if pattern not in regex_list:
        await callback_query.message.reply(f'Шаблон "{pattern}" не найден.')
        return

    # Удаляем шаблон из списка
    regex_list.remove(pattern)
    save_regex_patterns(regex_list)
    await callback_query.message.reply(f'Шаблон "{pattern}" успешно удален.')


# Обработчик всех остальных сообщений
@dp.message_handler()
async def echo_send(msg: types.Message) -> None:
    regex_list = load_regex_patterns()

    text = msg.text
    for pattern in regex_list:
        if re.search(pattern, text):
            await msg.reply(f'Текст сообщения от {msg.from_user.username} содержал потенциально важные данные')
            caption = f'Сообщение: "{msg.text}" от пользователя {msg.from_user.username} было удалено с помощью шаблона {pattern}'
            await bot.send_message(chat_id=admin_chat_id, text=caption)
            await msg.delete()
            return

    return


executor.start_polling(dp, skip_updates=True)

