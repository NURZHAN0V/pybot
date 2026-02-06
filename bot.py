import telebot as t
import dotenv
import os
from database import *
from openrouter import *

dotenv.load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN_API')
TELEGRAM_ADMIN_ID = os.getenv('TELEGRAM_ADMIN')
OPENROUTER_KEY = os.getenv('OPENROUTER_API_KEY')

bot = t.TeleBot(TELEGRAM_TOKEN)


# обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    save_user(message.from_user)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        message.chat.id,
        "Привет! Я - асситент Олег. Чем могу помочь?"
    )

# обработчик команд /me
@bot.message_handler(commands=['me'])
def id_message(message):
    # возвращаем информацию о пользователе: id, first_name, username, language_code
    from_user = (
        f"Ваш ID: `{message.from_user.id}`\n"
        f"Ваше имя: `{message.from_user.first_name}`\n"
        f"Ваш username: `{message.from_user.username or 'не указан'}`\n"
        f"Язык: `{message.from_user.language_code}`"
    )

    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, from_user, parse_mode="Markdown")


# выдать права администратора
@bot.message_handler(commands=['admin'])
def admin_message(message):
    if message.from_user.id == int(TELEGRAM_ADMIN_ID):
        user_id = message.text[6:].strip()
        if admin_add(user_id):
            bot.send_message(message.chat.id, "Права администратора назначены")
        else:
            bot.send_message(message.chat.id, "У пользователя уже есть права администратора или пользователь не найден")
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "У тебя нет прав администратора")


# обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if not is_chat_accessible(message.chat.id):
        bot.reply_to(message, "У тебя нет подписки, обратись к администратору @olegnastyle.")
        return

    bot.send_chat_action(message.chat.id, 'typing')

    # Получаем историю и формируем контекст
    # из последних 5 сообщений + новое
    history = get_messages(message.from_user.id)
    prompt = "".join([f"Пользователь: {m[2]}\nБот: {m[3]}\n" for m in history[-5:]])
    prompt += f"\nПользователь пишет: {message.text}"

    # Отправляем в API
    response = fetch_openrouter_api_key(OPENROUTER_KEY, prompt)

    # Сохраняем
    save_message(message.from_user.id, message.text, response)

    bot.send_message(message.chat.id, response, parse_mode="Markdown")

if __name__ == '__main__':
    init_db()
    print("Бот запущен и готов к работе!")
    bot.infinity_polling()