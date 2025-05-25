
import telebot
from telebot import types

BOT_TOKEN = "8025355595:AAGK1QblfiZUCDOg5bDWeay9Pe-p-Q7_Kmw"
bot = telebot.TeleBot(BOT_TOKEN)

balances = {}

def get_balance(user_id):
    return balances.get(user_id, 0.0)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id not in balances:
        balances[user_id] = 0.0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Баланс", "🎰 Играть")
    markup.add("💵 Пополнить", "📤 Вывести")
    bot.send_message(user_id, "Добро пожаловать в WaltrosBet!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "💰 Баланс")
def check_balance(message):
    user_id = message.chat.id
    balance = get_balance(user_id)
    bot.send_message(user_id, f"Ваш баланс: {balance:.2f} USDT")

@bot.message_handler(func=lambda m: m.text == "💵 Пополнить")
def deposit(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Введите сумму и адрес:
Пример:
5.0 @username")

@bot.message_handler(func=lambda m: m.text == "📤 Вывести")
def withdraw(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Введите сумму и адрес:
Пример:
5.0 @username")

@bot.message_handler(func=lambda m: m.text == "🎰 Играть")
def play_game(message):
    user_id = message.chat.id
    if get_balance(user_id) < 1.0:
        bot.send_message(user_id, "Недостаточно средств для игры.")
        return
    import random
    result = random.choice(["win", "lose"])
    if result == "win":
        balances[user_id] += 2.0
        bot.send_message(user_id, "Поздравляем! Вы выиграли 2 USDT!")
    else:
        balances[user_id] -= 1.0
        bot.send_message(user_id, "Увы! Вы проиграли 1 USDT.")

bot.polling()
