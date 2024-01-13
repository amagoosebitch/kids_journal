import json
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from tg_bot.callbacks import ReportTypeCallback
from tg_bot.handlers.command_handlers import start_command_handler, stop_command_handler
from tg_bot.handlers.message.employee import (
    handle_choose_child,
    handle_choose_group,
    handle_employee_start,
    handle_send_picture,
    handle_single_child_report,
    handle_write_report,
)
from tg_bot.handlers.message.parent import handle_subscribe
from tg_bot.message_replies import BACK
from tg_bot.settings import BotSettings
from tg_bot.states import EmployeeState, ParentState

logger = logging.getLogger(__name__)


def get_application() -> Application:
    settings = BotSettings()
    application: Application = Application.builder().token(settings.token).build()

    start_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command_handler)],
        states={
            EmployeeState.CHOOSE_REPORT_TYPE.value: [
                CallbackQueryHandler(
                    handle_single_child_report,
                    pattern=f"^{ReportTypeCallback.SINGLE_CHILD}$",
                )
                #  ToDo: Другие ветки работника
            ],
            EmployeeState.CHOOSE_GROUP.value: [
                CallbackQueryHandler(handle_employee_start, pattern=f"^{BACK}$"),
                CallbackQueryHandler(handle_choose_group, pattern="^.*$"),
            ],
            EmployeeState.CHOOSE_CHILD.value: [
                CallbackQueryHandler(handle_single_child_report, pattern=f"^{BACK}$"),
                CallbackQueryHandler(handle_choose_child, pattern="^.*$"),
            ],
            EmployeeState.WRITE_REPORT.value: [
                MessageHandler(filters.TEXT, handle_write_report)
            ],
            EmployeeState.SEND_PICTURE.value: [
                MessageHandler(
                    filters.ATTACHMENT | filters.Document.IMAGE, handle_send_picture
                )
            ],
            ParentState.SUBSCRIBE.value: [
                CallbackQueryHandler(handle_subscribe, pattern="^.*$")
            ],
        },
        fallbacks=[CommandHandler("stop", stop_command_handler)],
    )

    application.add_handler(start_conv_handler)
    return application


async def start(event, context):
    print(event)
    print(app._initialized)
    await app.initialize()
    message = Update.de_json(json.loads(event["body"]), app.bot)
    await app.process_update(message)


app = get_application()

if __name__ == "__main__":
    app.run_polling()
