from pyrogram import Client
from pyrogram.types import Message

from db import filters as db_filters


def get_reply_to_message_by_topic(msg: Message):
    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    if msg.reply_to_message:
        is_reply = db_filters.get_user_msg_id_by_topic_msg_id(topic_id=topic_id, msg_id=msg.reply_to_message.id)
        if is_reply is not None:
            reply = is_reply
        else:
            reply = None
    else:
        reply = None
    return reply


def delete(c: Client, msg: Message):
    if db_filters.is_group_exists(group_id=msg.chat.id):
        reply = get_reply_to_message_by_topic(msg)
        if reply:
            topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
            tg_id = db_filters.get_tg_id_by_topic(topic_id=topic_id)
            c.delete_messages(chat_id=tg_id, message_ids=reply)
            c.delete_messages(chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
            c.delete_messages(chat_id=msg.chat.id, message_ids=msg.id)
        else:
            c.delete_messages(chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
            c.delete_messages(chat_id=msg.chat.id, message_ids=msg.id)



