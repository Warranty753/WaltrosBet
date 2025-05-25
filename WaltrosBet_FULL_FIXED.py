
import telebot
from telebot import types

BOT_TOKEN = "8025355595:AAGK1QblfiZUCDOg5bDWeay9Pe-p-Q7_Kmw"
CRYPTOBOT_TOKEN = "403892:AAM7xRf5QnFScaTX4v4Kn98z2gzCBWPNlWj"
OWNER_ID = 152281500
CHANNEL_ID = -1002652557681

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💰 Пополнить", "📤 Вывести")
    markup.row("🏛 Играть", "💰 Баланс")
    markup.row("👥 Рефералка")
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    uid = message.chat.id
    if uid not in user_data:
        user_data[uid] = {"balance": 0.0}
    ref = str(message.text[7:]) if len(message.text) > 7 else None
    if ref and ref.isdigit() and int(ref) != uid:
        inviter_id = int(ref)
        user_data[inviter_id]["balance"] += 1
        bot.send_message(inviter_id, "Вы получили 1 USDT за приглашение!")
    bot.send_message(uid, "Добро пожаловать в WaltrosBet!", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == "💰 Баланс")
def balance(message):
    uid = message.chat.id
    bal = user_data.get(uid, {}).get("balance", 0.0)
    bot.send_message(uid, f"Ваш баланс: {bal:.2f} USDT")

@bot.message_handler(func=lambda m: m.text == "💰 Пополнить")
def topup(message):
    uid = message.chat.id
    bot.send_message(uid, "Введите сумму и адрес:
Пример:
5.0 @username")
    bot.register_next_step_handler(message, process_topup)

def process_topup(message):
    try:
        uid = message.chat.id
        amount_str, address = message.text.strip().split()
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
        user_data[uid]["balance"] += amount
        bot.send_message(uid, f"Пополнено {amount:.2f} USDT")
    except:
        bot.send_message(message.chat.id, "Ошибка! Используйте формат: 5.0 @username")

@bot.message_handler(func=lambda m: m.text == "📤 Вывести")
def withdraw(message):
    uid = message.chat.id
    bot.send_message(uid, "Введите сумму и адрес:
Пример:
5.0 @username")
    bot.register_next_step_handler(message, process_withdraw)

def process_withdraw(message):
    try:
        uid = message.chat.id
        amount_str, address = message.text.strip().split()
        amount = float(amount_str)
        if amount <= 0 or amount > user_data[uid]["balance"]:
            raise ValueError
        user_data[uid]["balance"] -= amount
        bot.send_message(uid, f"Выведено {amount:.2f} USDT")
    except:
        bot.send_message(message.chat.id, "Ошибка! Убедитесь, что сумма корректна и хватает средств.")

@bot.message_handler(func=lambda m: m.text == "👥 Рефералка")
def referral(message):
    uid = message.chat.id
    link = f"https://t.me/Waltrosbetbot?start={uid}"
    bot.send_message(uid, f"Ваша реферальная ссылка:
{link}")

@bot.message_handler(func=lambda m: m.text == "🏛 Играть")
def play(message):
    uid = message.chat.id
    bal = user_data.get(uid, {}).get("balance", 0.0)
    if bal >= 1.0:
        import random
        win = random.choice([True, False])
        if win:
            user_data[uid]["balance"] += 1.0
            bot.send_message(uid, "Вы выиграли 1 USDT!")
        else:
            user_data[uid]["balance"] -= 1.0
            bot.send_message(uid, "Вы проиграли 1 USDT!")
    else:
        bot.send_message(uid, "Недостаточно средств для игры. Пополните баланс.")

bot.polling()
