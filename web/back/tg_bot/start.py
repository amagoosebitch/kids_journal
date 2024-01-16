import json

from telegram import Update

from tg_bot.bot import app


async def start(event, context):
    print(event)
    print(app._initialized)
    try:
        await app.initialize()
        message = Update.de_json(json.loads(event["body"]), app.bot)
        await app.process_update(message)
        await app.shutdown()
    except Exception as e:
        print(e)
        return {"statusCode": 500}
    return {"statusCode": 200}
