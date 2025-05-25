import telebot

bot = telebot.TeleBot("8025355595:AAGK1QblfiZUCDOg5bDWeay9Pe-p-Q7_Kmw")

OWNER_ID = 152281500
CHANNEL_ID = -1002652557681

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в WaltrosBet!")

@bot.message_handler(commands=['пополнить'])
def deposit(message):
    bot.send_message(message.chat.id, "Введите сумму и адрес:\nПример:\n5.0 @username")

@bot.message_handler(commands=['баланс'])
def balance(message):
    bot.send_message(message.chat.id, "Ваш баланс: 0.00 USDT")

@bot.message_handler(commands=['рефералка'])
def referral(message):
    user_id = message.from_user.id
    ref_link = f"https://t.me/Waltrosbetbot?start={user_id}"
    bot.send_message(message.chat.id, f"Ваша реферальная ссылка: {ref_link}")

bot.polling()
