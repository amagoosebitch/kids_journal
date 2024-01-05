import logging

import requests
from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.message_replies import START_COMMAND_REPLY, STOP_COMMAND_REPLY
from tg_bot.states import EmployeeState

logger = logging.getLogger(__name__)


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s started a conversation", update.message.from_user.username)
    employee_response = requests.get(
        "http://127.0.0.1:8000/employee/{tgId}",
        params={"tg_id": update.message.from_user.id},
    )
    parent_response = requests.get(
        "http://127.0.0.1:8000/employee/{tgId}",
        params={"tg_id": update.message.from_user.id},
    )
    await update.message.reply_text(START_COMMAND_REPLY)
    return EmployeeState.CHOOSE_REPORT_TYPE


async def stop_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s stopped a conversation", update.message.from_user.username)
    await update.message.reply_text(STOP_COMMAND_REPLY)
