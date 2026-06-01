import logging
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = "8562499987:AAH1D2yZD9Qjym3YSM7Jmf02peYHraoJMDw"
GEMINI_API_KEY = "AQ.Ab8RN6IRnvdO4mYbYbuar_sO9MVT3vwhHVbTzJNpU2a2_4TKhA"

client = genai.Client(api_key=GEMINI_API_KEY)

chat_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Salom {user_name}! 👋\n"
        f"Men AI yordamchiman. Istalgan savolingizni bering!\n\n"
        f"📌 /reset — suhbatni tozalash"
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in chat_sessions:
        del chat_sessions[user_id]
    await update.message.reply_text("✅ Suhbat tarixi tozalandi!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    if user_id not in chat_sessions:
        chat_sessions[user_id] = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="Sen yordamchi AI botsan. O'zbek tilida qisqa va aniq javob ber."
            )
        )

try:
        response = chat_sessions[user_id].send_message(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:logging.error(f"Xato: {e}")              
        await update.message.reply_text(f"❌ Xato: {e}")  # xatoni ko'rsat
        
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot ishlamoqda...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
