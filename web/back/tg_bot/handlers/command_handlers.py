import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes, ConversationHandler

from tg_bot.api_utils import (
    get_employee_by_tg_id,
    get_parent_by_tg_id,
    try_merge_user_by_phone,
)
from tg_bot.callbacks import ReportTypeCallback
from tg_bot.message_replies import (
    MERGE_SUCCESS,
    MERGE_USER_NOT_FOUND,
    MERGE_USER_UNEXPECTED_ERROR,
    START_EMPLOYEE,
    START_PARENT,
    START_TRY_MERGE,
    STOP_COMMAND_REPLY,
)
from tg_bot.states import EmployeeState, ParentState

logger = logging.getLogger(__name__)


async def start_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text("kek")
    employee = get_employee_by_tg_id(tg_id=update.message.from_user.id)
    if employee:
        context.chat_data["first_name"] = employee.first_name
        await update.message.reply_text(
            START_EMPLOYEE.format(first_name=employee.first_name),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        # InlineKeyboardButton(
                        #     ReportTypeCallback.OBSERVATION,
                        #     callback_data=ReportTypeCallback.OBSERVATION,
                        # ),
                        # InlineKeyboardButton(
                        #     ReportTypeCallback.COMMON,
                        #     callback_data=ReportTypeCallback.COMMON,
                        # ),
                        InlineKeyboardButton(
                            ReportTypeCallback.SINGLE_CHILD,
                            callback_data=ReportTypeCallback.SINGLE_CHILD,
                        ),
                        InlineKeyboardButton(
                            ReportTypeCallback.PRESENTATION,
                            callback_data=ReportTypeCallback.PRESENTATION,
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

    share_button = KeyboardButton(text="Поделиться номером", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[share_button]], one_time_keyboard=True)
    await update.message.reply_text(text=START_TRY_MERGE, reply_markup=reply_markup)

    return ConversationHandler.END


async def stop_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s stopped a conversation", update.message.from_user.id)
    await update.message.reply_text(STOP_COMMAND_REPLY)

    return ConversationHandler.END


async def merge_users_by_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message is None:
        await update.message.reply_text(MERGE_USER_UNEXPECTED_ERROR)
        return ConversationHandler.END
    phone_number = message.contact.phone_number
    tg_id = message.from_user.id
    user = try_merge_user_by_phone(phone_number, tg_id)
    if user is not None:
        await update.message.reply_text(MERGE_SUCCESS)
        return ConversationHandler.END
    await update.message.reply_text(MERGE_USER_NOT_FOUND)
    return ConversationHandler.END
