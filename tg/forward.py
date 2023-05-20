import pyrogram
from pyrogram import Client
from pyrogram.errors import BadRequest, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.types import Message

from db import filters as db_filters


def get_reply_to_message_by_user(msg: Message):
    tg_id = msg.from_user.id
    if msg.reply_to_message:
        is_reply = db_filters.get_topic_msg_id_by_user_msg_id(tg_id=tg_id, msg_id=msg.reply_to_message.id)
        if is_reply is not None:
            reply = is_reply
        else:
            reply = db_filters.get_topic_id_by_tg_id(tg_id=tg_id)
    else:
        reply = db_filters.get_topic_id_by_tg_id(tg_id=tg_id)
    return reply


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


async def forward_message_from_user(cli: Client, msg: Message):
    tg_id = msg.from_user.id
    group = db_filters.get_group_by_tg_id(tg_id=tg_id)
    reply = get_reply_to_message_by_user(msg=msg)
    try:
        forward = await msg.copy(chat_id=int(group), reply_to_message_id=reply)
        db_filters.create_message(tg_id_or_topic_id=tg_id, is_topic_id=False,
                                  user_msg_id=msg.id, topic_msg_id=forward.id)
    except BadRequest as e:
        print("forward_message_from_user", e)
        return


async def forward_message_from_topic(cli: Client, msg: Message):
    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    tg_id = db_filters.get_tg_id_by_topic(topic_id=topic_id)
    is_protect = db_filters.get_is_protect_by_topic_id(topic_id=topic_id)
    reply = get_reply_to_message_by_topic(msg=msg)
    try:
        forward = await msg.copy(chat_id=tg_id, reply_to_message_id=reply, protect_content=is_protect)
        db_filters.create_message(tg_id_or_topic_id=topic_id, is_topic_id=True,
                                  user_msg_id=forward.id, topic_msg_id=msg.id)

    except InputUserDeactivated:
        db_filters.change_active(tg_id=tg_id, active=False)

    except UserIsBlocked:
        db_filters.change_active(tg_id=tg_id, active=False)

    except PeerIdInvalid:
        db_filters.change_active(tg_id=tg_id, active=False)

    except BadRequest as e:
        db_filters.change_active(tg_id=tg_id, active=False)
        print(e)


# @app.on_message(pyrogram.filters.create(is_not_raw) & pyrogram.filters.create(is_have_a_group))
async def forward_message(cli: Client, msg: Message):
    if msg.service or msg.game:
        print("service")
        return
    tg_id = msg.from_user.id
    if msg.chat.id == tg_id:
        await forward_message_from_user(cli=cli, msg=msg)
    elif db_filters.is_group_exists(group_id=msg.chat.id):
        await forward_message_from_topic(cli=cli, msg=msg)
    else:
        print("other")
        return
