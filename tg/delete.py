from pyrogram import Client
from pyrogram.errors import MessageDeleteForbidden
from pyrogram.types import Message

from db import repository


def delete_message(c, msg):
    #  just if msg to delete send with the bot !

    if msg[0].chat is not None:  # check if msg delete in chat user or group
        group = msg[0].chat.id

        if repository.is_group_exists(group_id=group):

            and_messages = msg[-1].id  # check if delete topic or some messages
            if repository.is_topic_id_exists(topic_id=and_messages):
                repository.del_topic(topic_id=and_messages)
                return

            del_ids = [i.id for i in msg]  # list of id to msg delete
            msg_ids = [repository.get_user_by_topic_msg_id(msg_id=i) for i in del_ids]  # list of Message (DB)

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
    if msg.reply_to_message:
        is_reply = repository.get_user_by_topic_msg_id(msg_id=msg.reply_to_message.id)
        if is_reply is not None:
            reply = is_reply.user_msg_id
        else:
            reply = None
    else:
        reply = None
    return reply


def delete(c: Client, msg: Message):
    if repository.is_group_exists(group_id=msg.chat.id):
        reply = get_reply_to_message_by_topic(msg)
        try:
            if reply:
                topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
                tg_id = int(repository.get_user_by_topic_id(topic_id=topic_id).id)
                c.delete_messages(chat_id=tg_id, message_ids=reply)
                c.delete_messages(chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
                c.delete_messages(chat_id=msg.chat.id, message_ids=msg.id)
            else:
                c.delete_messages(chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
                c.delete_messages(chat_id=msg.chat.id, message_ids=msg.id)
        except MessageDeleteForbidden as e:
            print(e)


