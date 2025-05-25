# WaltrosBet Casino Bot — Финальная версия
from telebot import TeleBot, types
import random

BOT_TOKEN = "8025355595:AAGK1QblfiZUCDOg5bDWeay9Pe-p-Q7_Kmw"
CRYPTO_TOKEN = "403892:AAM7xRf5QnFScaTX4v4Kn98z2gzCBWPNlWj"
ADMIN_ID = 152281500
CHANNEL_ID = -1002652557681

bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🚀 ИГРАТЬ"))
    markup.add(types.KeyboardButton("⚡ Профиль"))
    markup.add(types.KeyboardButton("💰 Пополнить баланс"))
    markup.add(types.KeyboardButton("📎 Реферальная система"))
    
    text = (
        f"👋 Добро пожаловать, {message.from_user.first_name}!

"
        "🚀 [Канал где публикуются ставки, акции, новости — тык](https://t.me/+I0EEvCfIQIUxZTg1)

"
        "Ты можешь оставить всё как есть. Или рискнуть!"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['bal'])
def bal(message):
    bot.send_message(message.chat.id, (
        "Для пополнения баланса используйте @CryptoBot:

"
        "1. Перейдите в @CryptoBot
"
        "2. Отправьте USDT
"
        "3. Баланс обновится автоматически."
    ))

@bot.message_handler(commands=['profile'])
def profile(message):
    bot.send_message(message.chat.id, f"Ваш профиль, {message.from_user.first_name}")

@bot.message_handler(commands=['send'])
def send(message):
    bot.send_message(message.chat.id, "Введите адрес и сумму для вывода.")

@bot.message_handler(commands=['menu'])
def menu(message):
    start(message)

@bot.message_handler(commands=['ref'])
def ref(message):
    ref_link = f"https://t.me/WaltrosBetBot?start={message.from_user.id}"
    bot.send_message(message.chat.id, f"Ваша реферальная ссылка:
{ref_link}")

@bot.message_handler(func=lambda m: True)
def handle_buttons(message):
    if message.text == "🚀 ИГРАТЬ":
        # Игровая логика с шансом 35% победы
        outcome = random.choices(["win", "lose"], weights=[35, 65])[0]
        if outcome == "win":
            bot.send_message(message.chat.id, "⚡ Победа! Вы сорвали куш!")
        else:
            bot.send_message(message.chat.id, "⚡ Поражение — но Вальтрос всегда возвращается!")
    elif message.text == "⚡ Профиль":
        profile(message)
    elif message.text == "💰 Пополнить баланс":
        bal(message)
    elif message.text == "📎 Реферальная система":
        ref(message)

bot.polling()
