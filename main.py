import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import json
import os

# Инициализация бота
bot = telebot.TeleBot('7697775529:AAEyllbCOd1gNVLoOeM7wCu5eLpkrOfxH00')

complexes = ["ЖК Астана", "ЖК Байтерек", "ЖК Керемет", "ЖК Орда"]
rooms = ["1 комната", "2 комнаты", "3 комнаты", "4 комнаты"]
furniture_options = ["С мебелью", "Без мебели"]
user_selection = {}


# Функция для сохранения данных в JSON файл
def save_data_to_json(chat_id, complex_name, room, furniture, phone):
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = []

    # Ищем и обновляем данные пользователя
    for user_data in data:
        if user_data['chat_id'] == chat_id:
            user_data.update({
                "complex_name": complex_name,
                "room": room,
                "furniture": furniture,
                "phone": phone
            })
            break
    else:
        # Если данных нет, добавляем новые
        data.append({
            "chat_id": chat_id,
            "complex_name": complex_name,
            "room": room,
            "furniture": furniture,
            "phone": phone
        })

    # Сохраняем данные обратно в JSON файл
    with open("user_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("Данные успешно сохранены в JSON файл.")


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in user_selection:
        user_selection[message.chat.id] = {}

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for complex_name in complexes:
        keyboard.add(KeyboardButton(complex_name))
    keyboard.add(KeyboardButton("Изменить данные"))

    bot.send_message(message.chat.id, "Выберите жилой комплекс или нажмите 'Изменить данные' для редактирования.",
                     reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Изменить данные")
def edit(message):
    if message.chat.id not in user_selection or 'complex' not in user_selection[message.chat.id]:
        bot.send_message(message.chat.id, "Ваши данные не найдены. Пожалуйста, завершите процесс выбора.")
        return

    selected = user_selection[message.chat.id]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Выбрать комплекс"))
    keyboard.add(KeyboardButton("Выбрать количество комнат"))
    keyboard.add(KeyboardButton("Выбрать мебель"))
    keyboard.add(KeyboardButton("Выбрать номер телефона"))

    bot.send_message(message.chat.id, "Что вы хотите изменить?", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Выбрать комплекс")
def edit_complex(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for complex_name in complexes:
        keyboard.add(KeyboardButton(complex_name))
    keyboard.add(KeyboardButton("Назад"))
    bot.send_message(message.chat.id, "Выберите новый жилой комплекс:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in complexes)
def update_complex(message):
    if message.chat.id not in user_selection:
        user_selection[message.chat.id] = {}

    user_selection[message.chat.id]['complex'] = message.text

    # Предложить изменить выбор
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Выбрать количество комнат"))
    keyboard.add(KeyboardButton("Выбрать мебель"))
    keyboard.add(KeyboardButton("Выбрать номер телефона"))
    keyboard.add(KeyboardButton("Завершить выбор"))

    bot.send_message(message.chat.id, f"Жилой комплекс выбран: {message.text}. Хотите изменить что-то?",
                     reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Выбрать количество комнат")
def edit_rooms(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for room in rooms:
        keyboard.add(KeyboardButton(room))
    keyboard.add(KeyboardButton("Назад"))
    bot.send_message(message.chat.id, "Выберите количество комнат:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in rooms)
def update_rooms(message):
    if message.chat.id in user_selection:
        user_selection[message.chat.id]['rooms'] = message.text
        # Предложить изменить мебель и телефон
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("Выбрать мебель"))
        keyboard.add(KeyboardButton("Выбрать номер телефона"))
        keyboard.add(KeyboardButton("Завершить выбор"))

        bot.send_message(message.chat.id, f"Количество комнат: {message.text}. Хотите изменить что-то?",
                         reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Выбрать мебель")
def edit_furniture(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for furniture in furniture_options:
        keyboard.add(KeyboardButton(furniture))
    keyboard.add(KeyboardButton("Назад"))
    bot.send_message(message.chat.id, "Выберите мебель:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in furniture_options)
def update_furniture(message):
    if message.chat.id in user_selection:
        user_selection[message.chat.id]['furniture'] = message.text
        # Предложить изменить номер телефона
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("Выбрать номер телефона"))
        keyboard.add(KeyboardButton("Завершить выбор"))

        bot.send_message(message.chat.id, f"Мебель: {message.text}. Хотите изменить что-то?",
                         reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Выбрать номер телефона")
def edit_phone(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте новый номер телефона.", reply_markup=ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton("Отправить мой номер", request_contact=True)))


@bot.message_handler(content_types=['contact'])
def update_phone(message):
    if message.chat.id in user_selection:
        # Проверяем, что все данные есть перед обновлением телефона
        if 'complex' not in user_selection[message.chat.id] or 'rooms' not in user_selection[message.chat.id] or 'furniture' not in user_selection[message.chat.id]:
            bot.send_message(message.chat.id, "Ошибка: вы не выбрали все необходимые параметры. Пожалуйста, завершите выбор.")
            return

        user_selection[message.chat.id]['phone'] = message.contact.phone_number
        save_data_to_json(message.chat.id, user_selection[message.chat.id].get('complex', ''),
                          user_selection[message.chat.id].get('rooms', ''), user_selection[message.chat.id].get('furniture', ''),
                          user_selection[message.chat.id]['phone'])
        bot.send_message(message.chat.id, f"Номер телефона обнавлен на {message.contact.phone_number}")


@bot.message_handler(func=lambda message: message.text == "Завершить выбор")
def finish(message):
    if message.chat.id in user_selection:
        selected = user_selection[message.chat.id]

        # Проверяем, что все данные присутствуют
        if 'complex' in selected and 'rooms' in selected and 'furniture' in selected and 'phone' in selected:
            save_data_to_json(message.chat.id, selected['complex'], selected['rooms'], selected['furniture'], selected['phone'])
            bot.send_message(message.chat.id, "Выбор завершен. Ваши данные сохранены.")
        else:
            # Если чего-то не хватает, сообщаем об этом
            missing = []
            if 'complex' not in selected:
                missing.append("Жилой комплекс")
            if 'rooms' not in selected:
                missing.append("Количество комнат")
            if 'furniture' not in selected:
                missing.append("Мебель")
            if 'phone' not in selected:
                missing.append("Номер телефона")

            bot.send_message(message.chat.id, f"Не все параметры выбраны. Пожалуйста, выберите: {', '.join(missing)}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, завершите выбор всех параметров.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
