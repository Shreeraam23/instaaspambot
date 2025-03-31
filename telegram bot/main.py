import logging
import json
import os
import telebot
from instagrapi import Client
from telebot.types import Message
import time
from threading import Thread
from queue import Queue
import random

# Configuration
TELEGRAM_BOT_TOKEN = "7764836417:AAHBfEZC5_mij_lq2jcaaCAOVOW9kamBSCA"
OWNER_IDS = [7369976226, 123456]  # Authorized users's user id
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Logging setup with detailed debugging
logging.basicConfig(
    filename="instagrapi_bot.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
)

# Store multiple Instagram clients per Telegram user
user_clients = {}  # {telegram_id: {account_name: Client}}
message_queue = Queue()  # Queue to manage API requests

# Welcome and Help Messages
WELCOME_MESSAGE = "👋 Welcome to the Instagram Spam Bot! This bot lets you manage Instagram accounts and send messages like a pro!"
HELP_MESSAGE = """
📋 **Commands Available:**
/start - Start the bot and see this message
/login - Add an Instagram account
/list - View logged-in accounts and send random messages
/send - Send messages (single or random)
/credits - See who made this awesome bot
/logout - Log out from all accounts
/help - Show this help message
"""

# Credits Text (customize this as you like)
CREDITS_TEXT = "Bot created by Ahmed Bhai (@tipsandgamer) - The mastermind behind this spam machine!"

def save_session(telegram_id, account_name):
    session_file = f"session_{telegram_id}_{account_name}.json"
    client = user_clients[telegram_id][account_name]
    with open(session_file, "w") as f:
        json.dump(client.get_settings(), f)
    logging.info(f"Session saved for {account_name} (User: {telegram_id}).")

def load_session(telegram_id, account_name):
    session_file = f"session_{telegram_id}_{account_name}.json"
    if os.path.exists(session_file):
        with open(session_file, "r") as f:
            settings = json.load(f)
        cl = Client()
        cl.set_settings(settings)
        try:
            cl.login(cl.username, cl.password)
            user_clients.setdefault(telegram_id, {})[account_name] = cl
            logging.info(f"Session restored for {account_name} (User: {telegram_id}).")
            return True
        except Exception as e:
            logging.warning(f"Session restore failed for {account_name}: {e}")
            return False
    return False

# API limit bypass with delay and queue
def process_queue():
    while True:
        if not message_queue.empty():
            client, text, target_ids, is_group = message_queue.get()
            try:
                client.direct_send(text, target_ids)
                logging.debug(f"Message sent: {text} to {target_ids}")
            except Exception as e:
                logging.error(f"Queue processing error: {e}")
            time.sleep(random.uniform(1, 3))  # Random delay to avoid rate limits
        time.sleep(0.1)

Thread(target=process_queue, daemon=True).start()

@bot.message_handler(commands=['start'])
def start(message: Message):
    if message.chat.id not in OWNER_IDS:
        bot.reply_to(message, "🚫 Unauthorized user! Only approved users can use this bot.")
        return
    bot.reply_to(message, f"{WELCOME_MESSAGE}\n\n{HELP_MESSAGE}")

@bot.message_handler(commands=['help'])
def help_command(message: Message):
    if message.chat.id not in OWNER_IDS:
        bot.reply_to(message, "🚫 Unauthorized user!")
        return
    bot.reply_to(message, HELP_MESSAGE)

@bot.message_handler(commands=['login'])
def login(message: Message):
    if message.chat.id not in OWNER_IDS:
        bot.reply_to(message, "🚫 Unauthorized user!")
        return
    bot.reply_to(message, "📱 Send your Instagram username.")
    bot.register_next_step_handler(message, get_username)

def get_username(message: Message):
    username = message.text
    bot.reply_to(message, "🔑 Send your Instagram password (this won't be saved).")
    bot.register_next_step_handler(message, lambda msg: get_password(message.chat.id, username, msg))

def get_password(telegram_id, username, message: Message):
    password = message.text
    cl = Client()
    try:
        cl.login(username, password)
        user_clients.setdefault(telegram_id, {})[username] = cl
        save_session(telegram_id, username)
        bot.reply_to(message, f"✅ Login successful for {username}!")
    except Exception as e:
        if "challenge_required" in str(e):  # Handle 2FA
            bot.reply_to(message, "🔐 2FA required! Enter the OTP code sent to your device.")
            bot.register_next_step_handler(message, lambda msg: verify_otp(telegram_id, username, password, msg))
        else:
            logging.error(f"Login failed for {username}: {e}")
            bot.reply_to(message, f"❌ Login failed: {e}")

def verify_otp(telegram_id, username, password, message: Message):
    otp = message.text
    cl = Client()
    try:
        cl.login(username, password, verification_code=otp)
        user_clients.setdefault(telegram_id, {})[username] = cl
        save_session(telegram_id, username)
        bot.reply_to(message, f"✅ Login successful for {username} with OTP!")
    except Exception as e:
        logging.error(f"OTP verification failed for {username}: {e}")
        bot.reply_to(message, f"❌ OTP verification failed: {e}")

@bot.message_handler(commands=['list'])
def list_accounts(message: Message):
    telegram_id = message.chat.id
    if telegram_id not in OWNER_IDS or telegram_id not in user_clients:
        bot.reply_to(message, "⚠️ No accounts logged in! Use /login first.")
        return
    accounts = list(user_clients[telegram_id].keys())
    bot.reply_to(message, f"📋 Logged-in accounts: {', '.join(accounts)}\n"
                         "Would you like to send multiple random messages? (yes/no)")
    bot.register_next_step_handler(message, handle_random_messages)

def handle_random_messages(message: Message):
    if message.text.lower() == "yes":
        bot.reply_to(message, "✍️ Enter messages separated by '|' (e.g., msg1|msg2|msg3).")
        bot.register_next_step_handler(message, get_random_messages)
    else:
        bot.register_next_step_handler(message, single_spam)

def get_random_messages(message: Message):
    messages = message.text.split("|")
    if not messages or len(messages) < 1:
        bot.reply_to(message, "⚠️ Please provide at least one message!")
        return
    message_dict = {i: msg.strip() for i, msg in enumerate(messages)}
    bot.reply_to(message, "🎯 Choose an option:\n1. Spam a user\n2. Spam a group")
    bot.register_next_step_handler(message, lambda msg: choose_spam_type(message.chat.id, message_dict, msg))

@bot.message_handler(commands=['send'])
def send_message_start(message: Message):
    if message.chat.id not in OWNER_IDS or message.chat.id not in user_clients:
        bot.reply_to(message, "⚠️ Login first with /login!")
        return
    bot.reply_to(message, "✨ Would you like to send multiple random messages? (yes/no)")
    bot.register_next_step_handler(message, handle_random_messages)

@bot.message_handler(commands=['single_spam'])
def single_spam(message: Message):
    bot.reply_to(message, "🎯 Choose an option:\n1. Spam a user\n2. Spam a group")
    bot.register_next_step_handler(message, lambda msg: choose_spam_type(message.chat.id, None, msg))

def choose_spam_type(telegram_id, message_dict, message: Message):
    choice = message.text.strip()
    if choice == "1":
        bot.reply_to(message, "👤 Enter recipient's Instagram username.")
        bot.register_next_step_handler(message, lambda msg: get_recipient(telegram_id, message_dict, msg))
    elif choice == "2":
        bot.reply_to(message, "👥 Enter group chat name or ID.")
        bot.register_next_step_handler(message, lambda msg: get_group(telegram_id, message_dict, msg))
    else:
        bot.reply_to(message, "❌ Invalid choice! Use 1 or 2.")

def get_recipient(telegram_id, message_dict, message: Message):
    username = message.text.strip()
    try:
        user_id = list(user_clients[telegram_id].values())[0].user_id_from_username(username)
        if message_dict:
            bot.reply_to(message, "🔢 Enter the number of times to send random messages.")
            bot.register_next_step_handler(message, lambda msg: send_dm_loop(telegram_id, [user_id], message_dict, msg, False))
        else:
            bot.reply_to(message, "✍️ Enter your message.")
            bot.register_next_step_handler(message, lambda msg: send_dm(telegram_id, [user_id], msg.text, msg, False))
    except Exception as e:
        logging.error(f"Error fetching user {username}: {e}")
        bot.reply_to(message, f"❌ Error fetching user: {e}")

def get_group(telegram_id, message_dict, message: Message):
    group_id = message.text.strip()
    if message_dict:
        bot.reply_to(message, "🔢 Enter the number of times to send random messages.")
        bot.register_next_step_handler(message, lambda msg: send_dm_loop(telegram_id, [group_id], message_dict, msg, True))
    else:
        bot.reply_to(message, "✍️ Enter your message.")
        bot.register_next_step_handler(message, lambda msg: send_dm(telegram_id, [group_id], msg.text, msg, True))

def send_dm(telegram_id, target_ids, text, message: Message, is_group):
    bot.reply_to(message, "🔢 Enter the number of times to send the message.")
    bot.register_next_step_handler(message, lambda msg: send_dm_loop(telegram_id, target_ids, {0: text}, msg, is_group))

def send_dm_loop(telegram_id, target_ids, message_dict, message: Message, is_group):
    try:
        count = int(message.text)
        bot.reply_to(message, f"🚀 Queuing {count} messages using {len(user_clients[telegram_id])} accounts...")
        clients = list(user_clients[telegram_id].values())
        for _ in range(count):
            for client in clients:
                text = random.choice(list(message_dict.values()))  # Randomly pick from dictionary
                message_queue.put((client, text, target_ids, is_group))
        bot.reply_to(message, "✅ Messages queued for sending!")
    except Exception as e:
        logging.error(f"Failed to queue messages: {e}")
        bot.reply_to(message, f"❌ Failed to send message: {e}")

@bot.message_handler(commands=['logout'])
def logout(message: Message):
    if message.chat.id not in OWNER_IDS or message.chat.id not in user_clients:
        bot.reply_to(message, "⚠️ No accounts to log out from!")
        return
    telegram_id = message.chat.id
    for account_name in user_clients[telegram_id]:
        user_clients[telegram_id][account_name].logout()
        os.remove(f"session_{telegram_id}_{account_name}.json")
    del user_clients[telegram_id]
    bot.reply_to(message, "👋 Logged out from all accounts and sessions deleted!")

@bot.message_handler(commands=['credits'])
def credits(message: Message):
    if message.chat.id not in OWNER_IDS:
        bot.reply_to(message, "🚫 Unauthorized user!")
        return
    bot.reply_to(message, CREDITS_TEXT)

# Additional Telegram Feature: Echo for Fun (only for authorized users)
@bot.message_handler(func=lambda message: message.chat.id in OWNER_IDS and message.text not in ['/start', '/help', '/login', '/list', '/send', '/single_spam', '/logout', '/credits'])
def echo(message: Message):
    bot.reply_to(message, f"🤖 You said: {message.text}\nUse /help for commands!")

if __name__ == "__main__":
    for user_id in OWNER_IDS:
        for file in os.listdir():
            if file.startswith(f"session_{user_id}_"):
                account_name = file.split("_")[2].split(".")[0]
                load_session(user_id, account_name)
    bot.polling(non_stop=True)
