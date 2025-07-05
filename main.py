from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import os
from dotenv import load_dotenv

load_dotenv(".env")

TOKEN = os.getenv("BOT_TOKEN")
SUPPORT_GROUP_ID = int(os.getenv("CHAT_ID"))
BOT_VER = "0.2.19"
message_map = {}


async def user_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if update.message.text:
        msg = f"📨 Сообщение от @{user.username or user.first_name} (ID: {user_id}):\n\n{update.message.text}"
        support_msg = await context.bot.send_message(chat_id=SUPPORT_GROUP_ID, text=msg)
        message_map[support_msg.message_id] = user_id
        await update.message.reply_text(
            "✅ Ваше сообщение отправлено в службу поддержки. Ожидайте ответа."
        )

    elif update.message.photo:
        photo = update.message.photo[-1]
        msg = f"📨 Сообщение от @{user.username or user.first_name} (ID: {user_id}):\n\n(Фото)"
        support_msg = await context.bot.send_photo(
            chat_id=SUPPORT_GROUP_ID, photo=photo.file_id, caption=msg
        )
        message_map[support_msg.message_id] = user_id
        await update.message.reply_text(
            "✅ Ваше фото отправлено в службу поддержки. Ожидайте ответа."
        )

    elif update.message.video:
        video = update.message.video
        msg = f"📨 Сообщение от @{user.username or user.first_name} (ID: {user_id}):\n\n(Видео)"
        support_msg = await context.bot.send_video(
            chat_id=SUPPORT_GROUP_ID, video=video.file_id, caption=msg
        )
        message_map[support_msg.message_id] = user_id
        await update.message.reply_text(
            "✅ Ваше видео отправлено в службу поддержки. Ожидайте ответа."
        )


async def support_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != SUPPORT_GROUP_ID:
        return

    if update.message.reply_to_message:
        original_msg_id = update.message.reply_to_message.message_id
        if original_msg_id in message_map:
            user_id = message_map[original_msg_id]

            if update.message.text:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"👨‍💼 Ответ службы поддержки:\n\n{update.message.text}",
                )
            elif update.message.photo:
                photo = update.message.photo[-1]
                await context.bot.send_photo(
                    chat_id=user_id,
                    photo=photo.file_id,
                    caption=f"👨‍💼 Ответ службы поддержки: {update.message.caption}",
                )
            elif update.message.video:
                video = update.message.video
                await context.bot.send_video(
                    chat_id=user_id,
                    video=video.file_id,
                    caption=f"👨‍💼 Ответ службы поддержки: {update.message.caption}",
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
        MessageHandler(filters.ChatType.PRIVATE & filters.PHOTO, user_message_handler)
    )
    app.add_handler(
        MessageHandler(filters.ChatType.PRIVATE & filters.VIDEO, user_message_handler)
    )
    app.add_handler(
        MessageHandler(filters.ChatType.GROUPS & filters.TEXT, support_reply_handler)
    )
    app.add_handler(
        MessageHandler(filters.ChatType.GROUPS & filters.PHOTO, support_reply_handler)
    )
    app.add_handler(
        MessageHandler(filters.ChatType.GROUPS & filters.VIDEO, support_reply_handler)
    )

    print(f"GraphON Bot | v. {BOT_VER}")
    print("Бот запущен...")
    app.run_polling()
