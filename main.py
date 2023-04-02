from pyrogram import Client

from tg import handlers


def main():
    app = Client("my_bot")
    for handler in handlers.HANDLERS:
        app.add_handler(handler)
    app.run()


if __name__ == '__main__':
    main()
