
import telebot
import requests
import time
import threading
import random
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup

BOT_TOKEN = "8025355595:AAGK1QblfiZUCDOg5bDWeay9Pe-p-Q7_Kmw"
CRYPTO_TOKEN = "403892:AAM7xRf5QnFScaTX4v4Kn98z2gzCBWPNlWj"
CHANNEL_ID = -1001234567890
ADMIN_ID = 123456789

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
balances = {}
referrals = {}
slots = ['🍒', '🍋', '🍊', '🍉', '⭐', '7️⃣']

def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("💵 Пополнить", "📤 Вывести")
    kb.add("🎰 Играть", "💰 Баланс")
    kb.add("👥 Рефералка")
    return kb

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    balances.setdefault(uid, 0)
    if len(message.text.split()) > 1:
        ref = int(message.text.split()[1])
        if ref != uid and uid not in referrals:
            referrals[uid] = ref
            bot.send_message(ref, f"@{message.from_user.username} — ваш реферал!")
    bot.send_message(uid, "Добро пожаловать в WaltrosBet", reply_markup=menu())

@bot.message_handler(func=lambda m: True)
def handle(message):
    uid = message.from_user.id
    text = message.text.strip()
    if text == "💵 Пополнить":
        create_invoice(uid)
    elif text == "📤 Вывести":
        bot.send_message(uid, "Введите сумму и адрес:\nПример:\n5.0 @username")
        bot.register_next_step_handler(message, withdraw)
    elif text == "🎰 Играть":
        play(uid)
    elif text == "💰 Баланс":
        bot.send_message(uid, f"Ваш баланс: {balances.get(uid, 0):.2f} USDT")
    elif text == "👥 Рефералка":
        link = f"https://t.me/{bot.get_me().username}?start={uid}"
        bot.send_message(uid, f"Ваша реферальная ссылка:
{link}")
    else:
        bot.send_message(uid, "Неизвестная команда. Используйте кнопки.")

def create_invoice(uid):
    headers = {"Crypto-Pay-API-Token": CRYPTO_TOKEN}
    payload = {
        "asset": "USDT", "amount": 5,
        "description": "Пополнение WaltrosBet",
        "payload": str(uid),
        "paid_btn_url": f"https://t.me/{bot.get_me().username}",
        "paid_btn_name": "open_bot"
    }
    r = requests.post("https://pay.crypt.bot/createInvoice", headers=headers, json=payload).json()
    url = r["result"]["pay_url"]
    bot.send_message(uid, f"Оплатите по ссылке:
{url}")

def withdraw(message):
    try:
        uid = message.from_user.id
        amt, addr = message.text.split()
        amt = float(amt)
        if balances.get(uid, 0) < amt:
            return bot.send_message(uid, "Недостаточно средств.")
        balances[uid] -= amt
        bot.send_message(ADMIN_ID, f"Вывод от @{message.from_user.username}: {amt} USDT → {addr}")
        bot.send_message(uid, "Заявка отправлена.")
    except:
        bot.send_message(uid, "Ошибка формата. Пример:
5.0 @username")

def play(uid):
    if balances.get(uid, 0) < 5:
        return bot.send_message(uid, "Недостаточно средств.")
    balances[uid] -= 5
    r = [random.choice(slots) for _ in range(3)]
    text = f"{r[0]} | {r[1]} | {r[2]}
"
    if r[0] == r[1] == r[2]:
        win = 15
    elif r[0] == r[1] or r[1] == r[2]:
        win = 7
    else:
        win = 0
    if win:
        balances[uid] += win
        text += f"Вы выиграли {win} USDT!"
    else:
        text += "Вы проиграли 5 USDT."
    bot.send_message(uid, text)

@app.route("/callback", methods=['POST'])
def callback():
    data = request.json
    if data.get("event") == "invoice_paid":
        uid = int(data["payload"])
        amt = float(data["amount"])
        balances[uid] = balances.get(uid, 0) + amt
        bot.send_message(uid, f"Зачислено {amt} USDT")
    return '', 200

def run_flask(): app.run(host="0.0.0.0", port=5000)
threading.Thread(target=run_flask).start()
bot.polling()
