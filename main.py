import random
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('ВАШ АЙДИ ОТ БОТА')

# Хранилище состояний пользователей
user_data = {}

# Генерация случайного числа
coolr = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)
coolb = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35)
chet = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36)
nechet = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35)

def randomus():
    return random.randint(0, 36)
    

# Функции создания клавиатуры
def create_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Казино"))
    keyboard.add(KeyboardButton("Баланс"))
    return keyboard

def create_balance_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Назад"), KeyboardButton("Пополнить"))
    return keyboard

def create_casino_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton('Ввести число'), KeyboardButton('Чет'), KeyboardButton('Зеро'))
    keyboard.row(KeyboardButton('Нечет'), KeyboardButton('Красное'), KeyboardButton('Черное'))
    keyboard.row(KeyboardButton('Назад'), KeyboardButton('Изменить ставку'))
    return keyboard

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    if user_id not in user_data:
        user_data[user_id] = {
            "balance": 0,
            "state": None,
            "random_card": randomus()
        }


    bot.send_message(user_id, "Привет! Нажми кнопку, чтобы начать.", reply_markup=create_main_menu())

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.chat.id
    text = message.text.lower()
    user = user_data.get(user_id, {})
    
    # Главные команды
    if text == "баланс":
        bot.send_message(user_id, f"Ваш баланс: {user.get('balance', 0)} р.", reply_markup=create_balance_menu())
        user['state'] = "balance"
    
    elif text == "пополнить" and user.get('state') == "balance":
        bot.send_message(user_id, "Введите сумму для пополнения:")
        user['state'] = "adding_balance"
    
    elif user.get('state') == "adding_balance":
        try:
            amount = int(message.text)
            if amount > 0:
                user['balance'] = user.get('balance', 0) + amount
                bot.send_message(user_id, f"Ваш баланс пополнен. Текущий баланс: {user['balance']} р.", reply_markup=create_balance_menu())
            else:
                bot.send_message(user_id, "Введите положительное число.")
        except ValueError:
            bot.send_message(user_id, "Введите корректное число.")
        user['state'] = "balance"
    
    elif text == 'изменить ставку':
        bot.send_message(user_id, "Введите ставку")
        user['state'] = "bet"

    elif text == "казино":
        user['random_card'] = randomus()
        bot.send_message(user_id, "Введите ставку")
        user['state'] = "bet"
        # bot.send_message(user_id, "Выберите действие:", reply_markup=create_casino_menu())
        # user['state'] = "casino"
    elif user.get('state') == "bet":
        try:
            global bet
            bet = int(message.text)
            if bet > -1:
                bot.send_message(user_id, "Выберите действие:", reply_markup=create_casino_menu())
                user['state'] = 'casino'
                return bet
        except ValueError:
            bot.send_message(user_id, "Введите корректное число.")

    elif text == "назад":
        bot.send_message(user_id, "Вы вернулись в главное меню.", reply_markup=create_main_menu())
        user['state'] = None

    # Логика казино

    elif text == "ввести число" and user.get('state') == "casino":
        print(user['random_card'])
        bot.send_message(user_id, "Введите число от 0 до 36:")
        user['state'] = "awaiting_number"

    elif user.get('state') == "awaiting_number":
        try:
            number = int(text)
            if 0 <= number <= 36:
                if number == user['random_card']:
                    bot.send_message(user_id, f"Поздравляю! Вы угадали число: {number}!")
                    bot.send_message(user_id, f"Ваш баланс увеличился на {bet*36}")
                    user["balance"] = user["balance"] + bet*36

                else:
                    bot.send_message(user_id, f"Вы не угадали. Выпало число: {user['random_card']}.")
                    user["balance"] = user["balance"] - bet
                    bot.send_message(user_id, f"Ваш баланс уменьшился на {bet}")
                user['state'] = "casino"
            else:
                bot.send_message(user_id, "Введите число в диапазоне от 0 до 36.")
        except ValueError:
            bot.send_message(user_id, "Введите корректное число.")

    elif text == "чет" and user.get('state') == "casino":
        if user['random_card'] in chet:
            bot.send_message(user_id, f"Вы выиграли! Выпало четное число: {user['random_card']}.")
            bot.send_message(user_id, f"Ваш баланс увеличился на {bet}")
            user["balance"] = user["balance"] + bet
        else:
            bot.send_message(user_id, f"Вы проиграли. Выпало нечетное число: {user['random_card']}.")
            user["balance"] = user["balance"] - bet
            bot.send_message(user_id, f"Ваш баланс уменьшился на {bet}")
    
    elif text == "нечет" and user.get('state') == "casino":
        if user['random_card'] in nechet:
            bot.send_message(user_id, f"Вы выиграли! Выпало нечетное число: {user['random_card']}.")
            bot.send_message(user_id, f"Ваш баланс увеличился на {bet}")
            user["balance"] = user["balance"] + bet

        else:
            bot.send_message(user_id, f"Вы проиграли. Выпало четное число: {user['random_card']}.")
            user["balance"] = user["balance"] - bet
            bot.send_message(user_id, f"Ваш баланс уменьшился на {bet}")

    elif text == "красное" and user.get('state') == "casino":
        if user['random_card'] in coolr:
            bot.send_message(user_id, f"Вы выиграли! Выпало красное число: {user['random_card']}.")
            bot.send_message(user_id, f"Ваш баланс увеличился на {bet}")
            user["balance"] = user["balance"] + bet

        else:
            bot.send_message(user_id, f"Вы проиграли. Выпало черное число: {user['random_card']}.")
            user["balance"] = user["balance"] - bet
            bot.send_message(user_id, f"Ваш баланс уменьшился на {bet}")

    elif text == "черное" and user.get('state') == "casino":
        if user['random_card'] in coolb:
            bot.send_message(user_id, f"Вы выиграли! Выпало черное число: {user['random_card']}.")
            bot.send_message(user_id, f"Ваш баланс увеличился на {bet}")
            user["balance"] = user["balance"] + bet

        else:
            bot.send_message(user_id, f"Вы проиграли. Выпало красное число: {user['random_card']}.")
            user["balance"] = user["balance"] - bet
            bot.send_message(user_id, f"Ваш баланс уменьшился на {bet}")

    elif text == "зеро" and user.get('state') == "casino":
        if user['random_card'] == 0:
            bot.send_message(user_id, "Поздравляю! Выпало зеро!")
            bot.send_message(user_id, f"Ваш баланс увеличился на {bet*36}")
            user["balance"] = user["balance"] + bet*36

        else:
            user["balance"] = user["balance"] - bet
            bot.send_message(user_id, f"Вы проиграли. Выпало число: {user['random_card']}.")
            bot.send_message(user_id, f"Ваш баланс уменьшился на {bet}")
    

    else:
        bot.send_message(user_id, "Неизвестная команда. Выберите действие из меню.")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен!")
    bot.polling(none_stop=True)

