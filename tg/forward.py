import pyrogram
from pyrogram import Client
from pyrogram.errors import BadRequest
from pyrogram.raw import functions
from pyrogram.raw.types import InputChannel
from pyrogram.types import Message

from db import filters
from db.filters import get_my_group, get_topic_msg_id_by_user_msg_id, get_topic_id_by_tg_id, \
    get_user_msg_id_by_topic_msg_id, is_topic_id_exists, get_is_banned, get_group_by_tg_id, create_message, \
    get_tg_id_by_topic, get_is_protect, is_group_exists
from tg.filters import is_not_raw, is_have_a_group


def get_reply_to_message_by_user(msg: Message):
    tg_id = msg.from_user.id
    if msg.reply_to_message:
        is_reply = get_topic_msg_id_by_user_msg_id(tg_id=tg_id, msg_id=msg.reply_to_message.id)
        if is_reply is not None:
            reply = is_reply
        else:
            reply = get_topic_id_by_tg_id(tg_id=tg_id)
    else:
        reply = get_topic_id_by_tg_id(tg_id=tg_id)
    return reply


def get_reply_to_message_by_topic(msg: Message):
    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    if msg.reply_to_message:
        is_reply = get_user_msg_id_by_topic_msg_id(topic_id=topic_id, msg_id=msg.reply_to_message.id)
        if is_reply is not None:
            reply = is_reply
        else:
            reply = None
    else:
        reply = None
    return reply


async def forward_message_from_user(cli: Client, msg: Message):
    tg_id = msg.from_user.id
    group = get_group_by_tg_id(tg_id=tg_id)
    reply = get_reply_to_message_by_user(msg=msg)
    try:
        forward = await msg.copy(chat_id=int(group), reply_to_message_id=reply)
        create_message(tg_id_or_topic_id=tg_id, is_topic_id=False,
                       user_msg_id=msg.id, topic_msg_id=forward.id)
    except BadRequest as e:
        print("forward_message_from_user", e)
        return


async def forward_message_from_topic(cli: Client, msg: Message):
    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    tg_id = get_tg_id_by_topic(topic_id=topic_id)
    is_protect = get_is_protect(tg_id=tg_id)
    reply = get_reply_to_message_by_topic(msg=msg)
    try:
        forward = await msg.copy(chat_id=tg_id, reply_to_message_id=reply, protect_content=is_protect)
        create_message(tg_id_or_topic_id=topic_id, is_topic_id=True,
                       user_msg_id=forward.id, topic_msg_id=msg.id)
    except BadRequest as e:
        print("forward_message_from_topic", e)
        return


@app.on_message(pyrogram.filters.create(is_not_raw) & pyrogram.filters.create(is_have_a_group))
async def forward_message(cli: Client, msg: Message):
    if msg.service or msg.game:
        print("service")
        return
    tg_id = msg.from_user.id
    if msg.chat.id == tg_id:
        await forward_message_from_user(cli=cli, msg=msg)
    elif is_group_exists(group_id=msg.chat.id):
        await forward_message_from_topic(cli=cli, msg=msg)
    else:
        print("other")
        return
