
import telebot

bot = telebot.TeleBot("8025355595:AAGK1QblfiZUCDOg5bDWeay9Pe-p-Q7_Kmw")

users = {}
referrals = {}

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) > 1:
        ref = args[1]
        if ref != str(user_id) and ref not in referrals:
            referrals[ref] = referrals.get(ref, []) + [user_id]
    users[user_id] = users.get(user_id, 0.0)
    bot.send_message(user_id, "Добро пожаловать в WaltrosBet!")

@bot.message_handler(func=lambda m: m.text == "💰 Пополнить")
def deposit(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите сумму и адрес:
Пример:
5.0 @username")

@bot.message_handler(func=lambda m: m.text == "📤 Вывести")
def withdraw(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите сумму и адрес для вывода.")

@bot.message_handler(func=lambda m: m.text == "💰 Баланс")
def balance(message):
    user_id = message.from_user.id
    balance = users.get(user_id, 0.0)
    bot.send_message(user_id, f"Ваш баланс: {balance:.2f} USDT")

@bot.message_handler(func=lambda m: m.text == "👥 Рефералка")
def referral(message):
    user_id = message.from_user.id
    ref_link = f"https://t.me/Waltrosbetbot?start={user_id}"
    bot.send_message(user_id, f"Ваша реферальная ссылка:
{ref_link}")

@bot.message_handler(func=lambda m: m.text == "🎮 Играть")
def play_menu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🏀 Баскетбол", "⚽ Футбол")
    keyboard.row("✊ Камень", "✋ Бумага", "✌️ Ножницы")
    bot.send_message(message.chat.id, "Выберите игру:", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text in ["🏀 Баскетбол", "⚽ Футбол", "✊ Камень", "✋ Бумага", "✌️ Ножницы"])
def play_game(message):
    user_id = message.from_user.id
    bot.send_message(user_id, f"Игра '{message.text}' скоро будет доступна!")

bot.polling()
