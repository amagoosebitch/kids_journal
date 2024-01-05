from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.api_utils import get_employee_by_tg_id, get_group_by_id


async def handle_single_child_report(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    group_ids = get_employee_by_tg_id(tg_id=update.message.from_user.id)["group_ids"]
    for group_id in group_ids:
        group = get_group_by_id(group_id=group_id)


async def handle_choose_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def handle_choose_child(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def handle_write_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass
