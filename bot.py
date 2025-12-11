from __future__ import annotations

import logging
import os
from typing import Dict

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# 管理员聊天中 message_id -> 用户 chat_id 的映射
message_owner_mapping: Dict[int, int] = {}

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )


def get_admin_id() -> int:
    admin_id = os.getenv("ADMIN_ID")
    if not admin_id:
        raise RuntimeError("ADMIN_ID is not configured.")
    return int(admin_id)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    admin_id = context.bot_data["admin_id"]

    if user_id == admin_id:
        text = (
            "👋 *管理员你好！*\n"
            "你可以通过“回复”用户发送来的消息来与对方通信。"
        )
    else:
        text = (
            "你好！这是留言机器人。\n\n"
            "你可以发送文字、图片等内容，我会自动转交给管理员。"
        )

    await update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    admin_id = context.bot_data["admin_id"]

    username = f"@{user.username}" if user.username else "(无用户名)"
    display_name = escape_markdown(user.full_name, version=2)
    content = escape_markdown(message.text or message.caption or "[无文本内容]", version=2)

    header = (
        "👤 *来自用户*\n"
        f"ID: `{user.id}`\n"
        f"用户名: {escape_markdown(username, 2)}\n"
        f"昵称: {display_name}\n"
        "消息内容：\n"
        f"{content}"
    )

    try:
        # 发送 header
        sent_header = await context.bot.send_message(
            chat_id=admin_id,
            text=header,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        message_owner_mapping[sent_header.message_id] = user.id

        # 再 Copy 原始媒体/消息
        if message.photo or message.document or message.sticker or message.voice:
            copied = await message.copy(chat_id=admin_id)
            message_owner_mapping[copied.message_id] = user.id

    except Exception as exc:
        logger.error("Forward failed: %s", exc)
        await message.reply_text("抱歉，暂时无法联系管理员。请稍后再试。")


async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    admin_id = context.bot_data["admin_id"]

    if message.from_user.id != admin_id:
        return

    if not message.reply_to_message:
        await message.reply_text("❗ 请直接 *回复* 某条用户消息。")
        return

    original_msg_id = message.reply_to_message.message_id
    target_user_id = message_owner_mapping.get(original_msg_id)

    if not target_user_id:
        await message.reply_text("找不到用户，请让对方重新发送一条消息。")
        return

    try:
        await message.copy(chat_id=target_user_id)
    except Exception as exc:
        logger.error("Deliver failed to %s: %s", target_user_id, exc)
        await message.reply_text("发送失败，请稍后重试。")


def main() -> None:
    load_dotenv()
    setup_logging()

    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is missing")

    admin_id = get_admin_id()

    application = ApplicationBuilder().token(bot_token).build()
    application.bot_data["admin_id"] = admin_id

    application.add_handler(CommandHandler("start", start_command))

    application.add_handler(MessageHandler(filters.Chat(admin_id) & ~filters.COMMAND, handle_admin_message))
    application.add_handler(MessageHandler(~filters.Chat(admin_id) & ~filters.COMMAND, handle_user_message))

    logger.info("Bot started.")
    application.run_polling()


if __name__ == "__main__":
    main()
