import pyrogram
from pyrogram import handlers

from tg import filters as tg_filters
from tg.command import get_info_command, protect, ban_users, request_group, create_group
from tg.edit import edited_message
from tg.forward import forward_message

HANDLERS = [
    handlers.MessageHandler(get_info_command, pyrogram.filters.command("info")
                            & pyrogram.filters.text & pyrogram.filters.group),
    handlers.MessageHandler(protect, pyrogram.filters.command(["protect", "unprotect"])
                            & pyrogram.filters.text & pyrogram.filters.group
                            & pyrogram.filters.create(tg_filters.is_banned)),
    handlers.MessageHandler(ban_users, pyrogram.filters.command(["ban", "unban"])
                            & pyrogram.filters.text & pyrogram.filters.group),
    handlers.MessageHandler(request_group, pyrogram.filters.command("add_group")
                            & pyrogram.filters.text & pyrogram.filters.create(tg_filters.is_admin)
                            & ~ pyrogram.filters.create(tg_filters.is_have_a_group)),
    handlers.MessageHandler(forward_message, ~ pyrogram.filters.command(
        ["start", "info", "protect", "unprotect", "ban", "unban", "add_group"])
                            & pyrogram.filters.create(tg_filters.is_not_raw)
                            & pyrogram.filters.create(tg_filters.is_have_a_group)
                            & pyrogram.filters.create(tg_filters.is_user_exists)),
    handlers.EditedMessageHandler(edited_message, pyrogram.filters.create(tg_filters.is_have_a_group)),
    handlers.RawUpdateHandler(create_group)
]
