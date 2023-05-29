from pyrogram import Client
from pyrogram.errors import MessageDeleteForbidden
from pyrogram.types import Message

from db import filters as db_filters


def delete_message(c, msg):

    if msg[0].chat is not None:  # check if msg delete in chat user or group
        group = msg[0].chat.id

        if db_filters.is_group_exists(group_id=group):

            del_ids = [i.id for i in msg]  # list of id to msg delete
            msg_ids = [db_filters.get_user_by_topic_msg_id2(i) for i in del_ids]  # list of Message (DB)

            my_dict = {}
            for msg in msg_ids:  # create dict{tg_id: [msg_id]}
                if msg is not None:
                    if my_dict.get(int(msg.tg_id.id)) is None:
                        my_dict[int(msg.tg_id.id)] = [msg.user_msg_id]
                    else:
                        my_dict[int(msg.tg_id.id)].append(msg.user_msg_id)
                else:
                    continue

            for user in my_dict.keys():
                c.delete_messages(chat_id=user, message_ids=my_dict[user])


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
        try:
            if reply:
                topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
                tg_id = db_filters.get_tg_id_by_topic(topic_id=topic_id)
                c.delete_messages(chat_id=tg_id, message_ids=reply)
                c.delete_messages(chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
                c.delete_messages(chat_id=msg.chat.id, message_ids=msg.id)
            else:
                c.delete_messages(chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
                c.delete_messages(chat_id=msg.chat.id, message_ids=msg.id)
        except MessageDeleteForbidden as e:
            print(e)


