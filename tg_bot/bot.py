from telegram.ext import Application, ConversationHandler, CommandHandler

from tg_bot.handlers.command_handlers import start_command_handler, stop_command_handler
from tg_bot.settings import BotSettings


def start() -> None:
    settings = BotSettings()
    application: Application = Application.builder().token(settings.token).build()

    start_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command_handler)],
        states={},
        fallbacks=[CommandHandler("stop", stop_command_handler)]
    )
    application.add_handler(start_conv_handler)
    application.run_polling()


if __name__ == "__main__":
    start()
