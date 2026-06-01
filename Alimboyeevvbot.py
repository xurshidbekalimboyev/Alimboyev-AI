import logging
import os
from groq import Groq
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = os.environ.get("8562499987:AAH1D2yZD9Qjym3YSM7Jmf02peYHraoJMDw")
GROQ_API_KEY = os.environ.get("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")

client = Groq(api_key=GROQ_API_KEY)

chat_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Salom {user_name}! 👋\n"
        f"Men AI yordamchiman. Istalgan savolingizni bering!\n\n"
        f"📌 /reset — suhbatni tozalash"
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in chat_histories:
        del chat_histories[user_id]
    await update.message.reply_text("✅ Suhbat tarixi tozalandi!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    if user_id not in chat_histories:
        chat_histories[user_id] = [
            {"role": "system", "content": "Sen yordamchi AI botsan. O'zbek tilida qisqa va aniq javob ber."}
        ]

    chat_histories[user_id].append({"role": "user", "content": user_text})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_histories[user_id],
            max_tokens=1000
        )
        bot_reply = response.choices[0].message.content
        chat_histories[user_id].append({"role": "assistant", "content": bot_reply})
        await update.message.reply_text(bot_reply)
    except Exception as e:
        logging.error(f"Xato: {e}")
        await update.message.reply_text(f"❌ Xato: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot ishlamoqda...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
