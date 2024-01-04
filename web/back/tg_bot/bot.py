import ydb
from telegram.ext import Application, CommandHandler, ConversationHandler

from db.services.parent import ParentService
from db.settings import YDBSettings
from tg_bot.handlers.command_handlers import start_command_handler, stop_command_handler
from tg_bot.settings import BotSettings


def start() -> None:
    settings = BotSettings()
    application: Application = Application.builder().token(settings.token).build()

    start_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command_handler)],
        states={},
        fallbacks=[CommandHandler("stop", stop_command_handler)],
    )
    application.add_handler(start_conv_handler)
    application.run_polling()


if __name__ == "__main__":
    settings = YDBSettings()
    driver = ydb.Driver(
        endpoint=settings.endpoint,
        database=settings.database,
        credentials=ydb.credentials_from_env_variables(),
    )
    session_pool = ydb.SessionPool(driver)

    parent_service = ParentService(session_pool, settings.database)

    start()
