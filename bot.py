import os
import threading
import telebot as t
from database import *
from openrouter import *
from mitup import *
from config import *
from audio import *

bot = t.TeleBot(TELEGRAM_TOKEN)

# создаем папку temp
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


def _chat_action_until(chat_id, action, stop_event):
    """Показывает action в чате каждые 4 сек, пока не установлен stop_event."""
    while True:
        bot.send_chat_action(chat_id, action)
        if stop_event.wait(4):
            break


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


# обработчик команды /admin
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


def _reply_ai(user_id, chat_id, text):
    """Контекст + запрос в ИИ, сохранение, ответ."""
    history = get_messages(user_id)
    prompt = "".join([f"Пользователь: {m[2]}\nБот: {m[3]}\n" for m in history[-5:]])
    prompt += f"\nПользователь пишет: {text}"
    response = fetch_openrouter_api_key(OPENROUTER_KEY, prompt)
    save_message(user_id, text, response)
    bot.send_message(chat_id, response, parse_mode="Markdown")

    
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    stop = threading.Event()
    threading.Thread(target=_chat_action_until, args=(message.chat.id, 'typing', stop), daemon=True).start()
    file_info = bot.get_file(message.voice.file_id)
    ogg_path = f"{TEMP_DIR}/voice_{message.message_id}.ogg"
    wav_path = f"{TEMP_DIR}/voice_{message.message_id}.wav"
    with open(ogg_path, 'wb') as f:
        f.write(bot.download_file(file_info.file_path))
    convert_ogg_to_wav(ogg_path, wav_path)
    text = wav_to_text(wav_path)
    if not text:
        stop.set()
        bot.reply_to(message, "(не удалось распознать)")
        return
    if not is_chat_accessible(message.chat.id):
        stop.set()
        bot.reply_to(message, "У тебя нет подписки, обратись к администратору @olegnastyle ☺️")
        return
    _reply_ai(message.from_user.id, message.chat.id, text)
    stop.set()

# обработчик сообщений для генерации изабражения
@bot.message_handler(func=lambda message: "нарис" in message.text.lower())
def draft_message(message):
    if not is_chat_accessible(message.chat.id):
        bot.reply_to(message, "У тебя нет подписки, обратись к администратору @olegnastyle ☺️")
        return
    prompt = message.text
    stop = threading.Event()
    threading.Thread(target=_chat_action_until, args=(message.chat.id, 'upload_photo', stop), daemon=True).start()
    image_url = fetch_draft(prompt, MITUP_KEY, MITU_URL)
    stop.set()
    bot.send_photo(message.chat.id, image_url)


# обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if not is_chat_accessible(message.chat.id):
        bot.reply_to(message, "У тебя нет подписки, обратись к администратору @olegnastyle ☺️")
        return
    stop = threading.Event()
    threading.Thread(target=_chat_action_until, args=(message.chat.id, 'typing', stop), daemon=True).start()
    _reply_ai(message.from_user.id, message.chat.id, message.text)
    stop.set()

if __name__ == '__main__':
    init_db()
    print("Бот запущен и готов к работе!")
    bot.infinity_polling()