import logging
import os
import requests
import tempfile
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
)
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)

# Dictionnaire pour stocker l'état utilisateur (optionnel)
user_state = {}

def menu(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Send a text", callback_data="send_text"),
            InlineKeyboardButton("Set Position", callback_data="set_position"),
            InlineKeyboardButton("Google 🌐", url="https://www.google.fr")
        ]
    ]
    update.message.reply_text(
        f"Welcome to EIAM Bot.\nLattitude : 48.8566\nLongitude : 2.3522\n",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    if query.data == "send_text":
        query.edit_message_text("✍️ Please send me your text in the chat.")
        user_state[user_id] = {"awaiting_text": True}
    elif query.data == "set_position":
        query.edit_message_text("🌍 Enter your latitude:")
        user_state[user_id] = {"awaiting_latitude": True}

def handle_text(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    state = user_state.get(user_id, {})
    text = update.message.text.strip()
    if state.get("awaiting_text"):
        # Save text to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmpfile:
            tmpfile.write(text)
            tmpfile_path = tmpfile.name
        # Prepare data for the server
        url = "http://localhost:8000/textfile_to_emo"
        files = {"file": open(tmpfile_path, "rb")}
        data = {}
        lat = state.get("latitude")
        lon = state.get("longitude")
        if lat is not None and lon is not None:
            data["latitude"] = str(lat)
            data["longitude"] = str(lon)
        try:
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
            result = response.json()
            update.message.reply_text(f"✅ Text sent and processed!\nServer response:\n{result}\n\nType /menu to start again.")
        except Exception as e:
            update.message.reply_text(f"❌ Error sending to server: {e}\n\nType /menu to try again.")
        finally:
            files["file"].close()
        user_state.pop(user_id, None)
    elif state.get("awaiting_latitude"):
        try:
            latitude = float(text)
            user_state[user_id] = {"latitude": latitude, "awaiting_longitude": True}
            update.message.reply_text("🌍 Enter your longitude:")
        except ValueError:
            update.message.reply_text("❌ Please enter a valid number for latitude.")
    elif state.get("awaiting_longitude"):
        try:
            longitude = float(text)
            latitude = user_state[user_id].get("latitude")
            user_state[user_id] = {"latitude": latitude, "longitude": longitude}
            update.message.reply_text(
                f"📍 Position set!\nLatitude: {latitude}\nLongitude: {longitude}\n\nType /menu to start again."
            )
        except ValueError:
            update.message.reply_text("❌ Please enter a valid number for longitude.")
    else:
        update.message.reply_text("Type /menu to show the available actions.")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", menu))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()