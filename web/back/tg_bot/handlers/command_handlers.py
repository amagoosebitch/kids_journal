import logging

import requests
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from tg_bot.api_client_settings import get_api_settings
from tg_bot.message_replies import (
    START_EMPLOYEE,
    START_NO_ONE,
    START_PARENT,
    STOP_COMMAND_REPLY,
)
from tg_bot.states import EmployeeState, ParentState

logger = logging.getLogger(__name__)


async def start_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    logger.info("User %s started a conversation", update.message.from_user.username)
    breakpoint()

    api_settings = get_api_settings()
    params = {"tg_id": update.message.from_user.username}  # Берем usernmame, а не id? Что, если меняется?

    employee_response = requests.get(
        api_settings.employee_url,
        params=params,
    ).json()
    if employee_response:
        await update.message.reply_text(START_EMPLOYEE)
        return EmployeeState.CHOOSE_REPORT_TYPE.value

    parent_response = requests.get(
        api_settings.parent_url,
        params=params,
    ).json()
    if parent_response:
        await update.message.reply_text(START_PARENT)
        return ParentState.SUBSCRIBE.value

    await update.message.reply_text(START_NO_ONE)
    return ConversationHandler.END


async def stop_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s stopped a conversation", update.message.from_user.username)
    await update.message.reply_text(STOP_COMMAND_REPLY)
