import os
import telebot
from flask import Flask, request

# Получаем переменные окружения
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not TOKEN or not ADMIN_ID:
    print("❌ BOT_TOKEN или ADMIN_ID не заданы. Проверь переменные окружения.")
    exit(1)

try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    print("❌ ADMIN_ID должен быть числом.")
    exit(2)

print("✅ Бот запускается...")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/")
def index():
    return "Бот работает!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "👋 Привет! Напиши своё сообщение, и мы обязательно свяжемся с тобой.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user = message.from_user
    text = f"📩 Новое сообщение от @{user.username or user.first_name} (ID: {user.id}):\n\n{message.text}"
    bot.send_message(ADMIN_ID, text)
    bot.reply_to(message, "✅ Спасибо! Ваше сообщение отправлено. Мы скоро свяжемся с вами.")

if __name__ == "__main__":
    print("📡 Устанавливаем Webhook...")
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.getenv('RENDER_EXTERNAL_URL')}/{TOKEN}")
if __name__ == "__main__":
    print("✅ Бот запускается...")
    print("📡 Устанавливаем Webhook...")
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.getenv('RENDER_EXTERNAL_URL')}/{TOKEN}")

    # Запускаем Flask, чтобы Render видел открытый порт
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
