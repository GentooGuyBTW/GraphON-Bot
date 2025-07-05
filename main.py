from telegram import Update, MessageEntity
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
SUPPORT_GROUP_ID = os.getenv("CHAT_ID")
BOT_VER = "0.2.5" # MODIFY VERSION AFTER COMMIT!
message_map = {}


async def user_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_message = update.message.text
    user_id = user.id
    msg = f"📨 Сообщение от @{user.username or user.first_name} (ID: {user_id}):\n\n{user_message}"
    support_msg = await context.bot.send_message(chat_id=SUPPORT_GROUP_ID, text=msg)
    message_map[support_msg.message_id] = user_id
    await update.message.reply_text(
        "✅ Ваше сообщение отправлено в службу поддержки. Ожидайте ответа."
    )


async def support_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != SUPPORT_GROUP_ID:
        return

    if update.message.reply_to_message:
        original_msg_id = update.message.reply_to_message.message_id
        if original_msg_id in message_map:
            user_id = message_map[original_msg_id]
            await context.bot.send_message(
                chat_id=user_id,
                text=f"👨‍💼 Ответ службы поддержки:\n\n{update.message.text}",
            )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Напишите ваш вопрос, и мы передадим его специалистам службы поддержки."
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, user_message_handler)
    )
    app.add_handler(
        MessageHandler(filters.ChatType.GROUPS & filters.TEXT, support_reply_handler)
    )
    print(f"GraphON Bot | v. {BOT_VER}")
    print("Бот запущен...")
    app.run_polling()
