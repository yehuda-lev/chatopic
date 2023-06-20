import logging
import os
from logging import handlers
from pyrogram import Client
from dotenv import load_dotenv
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import BotCommand, BotCommandScopeChat

from db import repository
from tg import handlers
from tg.strings import resolve_msg

load_dotenv()


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

# max bytes file 5 MB
file_handler = logging.handlers.RotatingFileHandler(
    filename='my_log.log', maxBytes=5 * 1024 * 1024, backupCount=1, mode='D'
)
# file_handler = logging.FileHandler('your_log_file.log')
file_handler.setLevel(logging.DEBUG)

logging.basicConfig(
    format='Time> %(asctime)s | Module> %(module)s | LevelName> %(levelname)s | '
           'Message> %(message)s | Name> %(name)s | FuncName> %(funcName)s | Line > %(lineno)d',
    level=logging.INFO,
    handlers=[
        file_handler,
        console_handler
    ]
)

logger = logging.getLogger(__name__)


def main():
    app = Client(name=os.environ['PYROGRAM_NAME_SESSION'], api_id=os.environ['TELEGRAM_API_ID'],
                 api_hash=os.environ['TELEGRAM_API_HASH'], bot_token=os.environ['TELEGRAM_BOT_TOKEN'])

    for admin in os.environ['ADMINS'].split(','):
        if not repository.is_admin_exists(tg_id=int(admin)):
            repository.create_admin(tg_id=int(admin))

            set_commands_for_admin(c=app, admin_id=int(admin))

    logger.debug(f"Bot {app.name} is up and running!")

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
                BotCommand(command='unban', description=resolve_msg('COMMAND_UNBAN')),
                BotCommand(command='send', description=resolve_msg('COMMAND_SEND'))
            ],
            scope=BotCommandScopeChat(chat_id=admin_id)
        )
    except PeerIdInvalid as e:
        logger.error(e)
    c.stop()


if __name__ == '__main__':
    main()
