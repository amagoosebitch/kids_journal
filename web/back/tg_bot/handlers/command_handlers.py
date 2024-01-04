import logging

from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.message_replies import START_COMMAND_REPLY, STOP_COMMAND_REPLY

logger = logging.getLogger(__name__)


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s started a conversation", update.message.from_user.username)
    await update.message.reply_text(START_COMMAND_REPLY)
    return 0


async def stop_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s stopped a conversation", update.message.from_user.username)
    await update.message.reply_text(STOP_COMMAND_REPLY)
