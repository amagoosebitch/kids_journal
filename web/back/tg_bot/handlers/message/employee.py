from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from tg_bot.api_utils import get_employee_by_tg_id, get_group_by_id
from tg_bot.message_replies import CHOOSE_GROUP, GROUP_INFO, NEXT
from tg_bot.states import EmployeeState


async def handle_single_child_report(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if "group_page" not in context.chat_data:
        context.chat_data["group_page"] = 0
    group_ids = get_employee_by_tg_id(
        tg_id=update.callback_query.from_user.id
    ).group_ids
    group_page = context.chat_data["group_page"]
    if group_page > len(group_ids):
        context.chat_data["group_page"] = 0
        group_page = 0

    group_info_buttons: list[list[InlineKeyboardButton]] = [[]]
    for group_id in group_ids[group_page : group_page + 3]:
        group = get_group_by_id(group_id=str(group_id))
        msg = GROUP_INFO.format(group_name=group.name, group_age_range=group.age_range)
        group_info_buttons.append([InlineKeyboardButton(msg, callback_data=group_id)])
    group_info_buttons.append([InlineKeyboardButton(NEXT, callback_data=NEXT)])

    await update.callback_query.edit_message_text(
        CHOOSE_GROUP,
        reply_markup=InlineKeyboardMarkup(group_info_buttons),
    )
    return EmployeeState.CHOOSE_GROUP.value


async def handle_choose_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query.data == NEXT:
        context.chat_data["group_page"] += 3
        return await handle_single_child_report(update=update, context=context)

    group_id = update.callback_query.data

    return EmployeeState.CHOOSE_CHILD


async def handle_choose_child(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def handle_write_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass
