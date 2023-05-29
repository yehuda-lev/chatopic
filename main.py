import os
from pyrogram import Client
from dotenv import load_dotenv
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import BotCommand, BotCommandScopeChat

from db import filters as db_filters
from tg import handlers
from tg.strings import resolve_msg

load_dotenv()


def main():
    app = Client(name=os.environ['PYROGRAM_NAME_SESSION'], api_id=os.environ['TELEGRAM_API_ID'],
                 api_hash=os.environ['TELEGRAM_API_HASH'], bot_token=os.environ['TELEGRAM_BOT_TOKEN'])

    for admin in os.environ['ADMINS'].split(','):
        if not db_filters.is_admin_exists(tg_id=int(admin)):
            db_filters.create_admin(tg_id=int(admin))

        set_commands_for_admin(c=app, admin_id=int(admin))

    print(f"Bot {app.name} is up and running!")

    for handler in handlers.HANDLERS:
        app.add_handler(handler)

    app.run()


def set_commands_for_admin(c: Client, admin_id: int):
    c.start()
    try:
        c.set_bot_commands(
            commands=[
                BotCommand(command='start', description='start'),
                BotCommand(command='add_group', description=resolve_msg('COMMAND_ADD_GROUP')),
                BotCommand(command='delete_group', description=resolve_msg('COMMAND_DELETE_GROUP')),
                BotCommand(command='send', description=resolve_msg('COMMAND_SEND'))
            ],
            scope=BotCommandScopeChat(chat_id=admin_id)
        )
    except PeerIdInvalid:
        pass
    c.stop()


if __name__ == '__main__':
    main()
