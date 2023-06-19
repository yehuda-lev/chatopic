import pyrogram
from pyrogram import handlers

from tg import filters as tg_filters
from tg.broadcast import send_message, get_message_for_subscribe
from tg.command import (get_info_command, protect, request_group,
                        raw_update, send_welcome, ask_delete_group, delete_group, unban_user)
from tg.delete import delete, delete_message
from tg.edit import edited_message, answer_the_message_is_edited
from tg.forward import forward_message

HANDLERS = [
    handlers.MessageHandler(get_info_command, pyrogram.filters.command("info")
                            & pyrogram.filters.text & pyrogram.filters.group
                            & pyrogram.filters.create(tg_filters.is_topic_or_is_user)),

    handlers.MessageHandler(unban_user, pyrogram.filters.command("unban")
                            & pyrogram.filters.text & pyrogram.filters.private
                            & pyrogram.filters.create(tg_filters.is_admin)
                            & pyrogram.filters.create(tg_filters.is_topic_or_is_user)),

    handlers.MessageHandler(delete, pyrogram.filters.command("delete")
                            & pyrogram.filters.text & pyrogram.filters.group
                            & pyrogram.filters.create(tg_filters.is_topic_or_is_user)),

    handlers.MessageHandler(send_welcome, pyrogram.filters.command("start")
                            & pyrogram.filters.text & pyrogram.filters.private
                            & pyrogram.filters.create(tg_filters.is_have_a_group)),

    handlers.MessageHandler(protect, pyrogram.filters.command(["protect", "unprotect"])
                            & pyrogram.filters.text & pyrogram.filters.group
                            & pyrogram.filters.create(tg_filters.is_topic_or_is_user)
                            & pyrogram.filters.create(tg_filters.is_banned)),

    handlers.MessageHandler(request_group, pyrogram.filters.command("add_group")
                            & pyrogram.filters.text & pyrogram.filters.create(tg_filters.is_admin)
                            & ~ pyrogram.filters.create(tg_filters.is_have_a_group)),

    handlers.MessageHandler(get_message_for_subscribe, pyrogram.filters.private
                            & pyrogram.filters.create(tg_filters.is_not_raw)
                            & pyrogram.filters.command("send")
                            & pyrogram.filters.create(tg_filters.is_admin)
                            | pyrogram.filters.create(tg_filters.is_force_reply)),

    handlers.MessageHandler(ask_delete_group, pyrogram.filters.private
                            & pyrogram.filters.create(tg_filters.is_not_raw)
                            & pyrogram.filters.command('delete_group')
                            & pyrogram.filters.create(tg_filters.is_admin)),

    handlers.CallbackQueryHandler(delete_group,
                                  pyrogram.filters.create(lambda _, __, cbd:
                                                          cbd.data.startswith('delete'))),

    handlers.CallbackQueryHandler(send_message,
                                  pyrogram.filters.create(lambda _, __, cbd:
                                                          cbd.data.endswith('send_message'))),

    handlers.CallbackQueryHandler(answer_the_message_is_edited,
                                  pyrogram.filters.create(lambda _, __, cbd:
                                                          cbd.data == 'edit')),

    handlers.MessageHandler(forward_message,
                            pyrogram.filters.create(tg_filters.is_command)
                            & pyrogram.filters.create(tg_filters.is_not_raw)
                            & pyrogram.filters.create(tg_filters.is_have_a_group)
                            & pyrogram.filters.create(tg_filters.is_topic_or_is_user)
                            & pyrogram.filters.create(tg_filters.is_user_exists)
                            & pyrogram.filters.create(tg_filters.is_banned)
                            & ~ pyrogram.filters.create(tg_filters.is_force_reply)),

    handlers.EditedMessageHandler(edited_message, pyrogram.filters.create(tg_filters.is_have_a_group)
                                  & pyrogram.filters.create(tg_filters.is_topic_or_is_user)
                                  & pyrogram.filters.create(tg_filters.is_banned)),

    handlers.DeletedMessagesHandler(delete_message),

    handlers.RawUpdateHandler(raw_update)
]
