import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from tg_bot.api_utils import get_employee_by_tg_id, get_parent_by_tg_id
from tg_bot.callbacks import ReportTypeCallback
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
    logger.info("User %s started a conversation", update.message.from_user.id)

    employee = get_employee_by_tg_id(tg_id=update.message.from_user.id)
    if employee:
        context.chat_data['first_name'] = employee.first_name
        await update.message.reply_text(
            START_EMPLOYEE.format(first_name=employee.first_name),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            ReportTypeCallback.OBSERVATION,
                            callback_data=ReportTypeCallback.OBSERVATION,
                        ),
                        InlineKeyboardButton(
                            ReportTypeCallback.COMMON,
                            callback_data=ReportTypeCallback.COMMON,
                        ),
                        InlineKeyboardButton(
                            ReportTypeCallback.SINGLE_CHILD,
                            callback_data=ReportTypeCallback.SINGLE_CHILD,
                        ),
                    ]
                ]
            ),
        )
        return EmployeeState.CHOOSE_REPORT_TYPE.value

    parent = get_parent_by_tg_id(tg_id=update.message.from_user.id)
    if parent:
        await update.message.reply_text(
            START_PARENT.format(first_name=parent["first_name"])
        )
        return ParentState.SUBSCRIBE.value

    await update.message.reply_text(START_NO_ONE)
    return ConversationHandler.END


async def stop_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s stopped a conversation", update.message.from_user.id)
    await update.message.reply_text(STOP_COMMAND_REPLY)

    return ConversationHandler.END
