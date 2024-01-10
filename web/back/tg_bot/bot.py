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
    handle_single_child_report,
    handle_write_report,
)
from tg_bot.settings import BotSettings
from tg_bot.states import EmployeeState


def start() -> None:
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
                CallbackQueryHandler(handle_choose_group, pattern="^.*$")
            ],
            EmployeeState.CHOOSE_CHILD.value: [
                MessageHandler(filters.TEXT, handle_choose_child)
            ],
            EmployeeState.WRITE_REPORT.value: [
                MessageHandler(filters.TEXT, handle_write_report)
            ],
        },
        fallbacks=[CommandHandler("stop", stop_command_handler)],
    )
    application.add_handler(start_conv_handler)
    application.run_polling()


if __name__ == "__main__":
    start()
