from io import BytesIO

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from tg_bot.api_utils import (
    get_children_by_group_id,
    get_employee_by_tg_id,
    get_group_by_id, get_parents_by_child_id,
)
from tg_bot.message_replies import (
    BACK,
    CHOOSE_CHILD,
    CHOOSE_GROUP,
    GROUP_INFO,
    NEXT,
    SEND_PICTURE,
    WRITE_REPORT,
)
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
        group_info_buttons.append(
            [InlineKeyboardButton(msg, callback_data=str(group_id))]
        )
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
    children = get_children_by_group_id(group_id=group_id)

    keyboard = [
        [
            InlineKeyboardButton(
                children[i - 1].name, callback_data=str(children[i - 1].child_id)
            ),
            InlineKeyboardButton(
                children[i].name, callback_data=str(children[i].child_id)
            ),
        ]
        for i in range(1, len(children), 2)
    ]
    if len(children) % 2 == 1:
        keyboard.append(
            [
                InlineKeyboardButton(
                    children[-1].name, callback_data=str(children[-1].child_id)
                )
            ]
        )
    keyboard.append([InlineKeyboardButton(BACK, callback_data=BACK)])

    await update.callback_query.edit_message_text(
        CHOOSE_CHILD, reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return EmployeeState.CHOOSE_CHILD.value


async def handle_choose_child(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["child_id"] = update.callback_query.data

    await update.callback_query.edit_message_text(WRITE_REPORT)
    return EmployeeState.WRITE_REPORT.value


async def handle_write_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["report_text"] = update.message.text

    await update.message.reply_text(SEND_PICTURE)
    return EmployeeState.SEND_PICTURE.value


async def handle_send_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parent_1, parent_2 = get_parents_by_child_id(context.chat_data["child_id"])

    file = await update.message.photo[-1].get_file()
    picture = await file.download_as_bytearray()

    await context.bot.send_photo(parent_1.tg_user_id, BytesIO(picture))
    await context.bot.send_message(chat_id=parent_1.tg_user_id, text=context.chat_data["report_text"])

    await context.bot.send_photo(parent_2.tg_user_id, BytesIO(picture))
    await context.bot.send_message(chat_id=parent_2.tg_user_id, text=context.chat_data["report_text"])
