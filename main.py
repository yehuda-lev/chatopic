import os
from pyrogram import Client
from dotenv import load_dotenv
from db import filters as db_filters
from tg import handlers


load_dotenv()


def main():
    app = Client(name=os.environ['PYROGRAM_NAME_SESSION'], api_id=os.environ['TELEGRAM_API_ID'],
                 api_hash=os.environ['TELEGRAM_API_HASH'], bot_token=os.environ['TELEGRAM_BOT_TOKEN'])

    for admin in os.environ['ADMINS'].split(','):
        if not db_filters.is_admin_exists(tg_id=int(admin)):
            db_filters.create_admin(tg_id=int(admin))

    print(f"Bot {app.name} is up and running!")

    for handler in handlers.HANDLERS:
        app.add_handler(handler)

    app.run()


if __name__ == '__main__':
    main()
