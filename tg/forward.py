import pyrogram
from pyrogram import Client
from pyrogram.errors import (BadRequest, InputUserDeactivated, UserIsBlocked, PeerIdInvalid)
from pyrogram.types import Message

from db import filters as db_filters


async def forward_message(cli: Client, msg: Message):
    """
    Forwarding a message sent from a user to a group
    or from a group to a user
    """

    if msg.service or msg.game:  # you cant copy this message
        return

    tg_id = msg.from_user.id

    if msg.chat.id == tg_id:  # the message sent by user
        await forward_message_from_user(c=cli, msg=msg)

    elif db_filters.is_group_exists(group_id=msg.chat.id):  # the message sent by topic
        await forward_message_from_topic(msg=msg)

    else:
        return


def get_reply_to_message_by_user(msg: Message) -> int:
    """
    get reply to message by user,
    if not reply: return topic id
    """

    tg_id = msg.from_user.id
    if msg.reply_to_message:
        is_reply = db_filters.get_topic_msg_id_by_user_msg_id(
            tg_id=tg_id, msg_id=msg.reply_to_message.id)

        if is_reply is not None:
            reply = is_reply
        else:
            reply = db_filters.get_topic_id_by_tg_id(tg_id=tg_id)
    else:
        reply = db_filters.get_topic_id_by_tg_id(tg_id=tg_id)
    return reply


async def forward_message_from_user(c: Client, msg: Message):
    """
    the message sent by user > forward message to topic
    """

    tg_id = msg.from_user.id
    group = db_filters.get_group_by_tg_id(tg_id=tg_id)
    reply = get_reply_to_message_by_user(msg=msg)

    try:
        if msg.poll is not None or msg.venue is not None \
                or msg.contact is not None or msg.location is not None:

            await send_contact_or_poll_or_location(c, msg, int(group), reply)
            return

        forward = await msg.copy(chat_id=int(group), reply_to_message_id=reply)
        db_filters.create_message(tg_id_or_topic_id=tg_id, is_topic_id=False,
                                  user_msg_id=msg.id, topic_msg_id=forward.id)
    except BadRequest as e:
        print("forward_message_from_user", e)
        return


def get_reply_to_message_by_topic(msg: Message) -> int | None:
    """
    get reply to message by topic,
    if not reply: return None
    """

    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    if msg.reply_to_message:
        is_reply = db_filters.get_user_msg_id_by_topic_msg_id(
            topic_id=topic_id, msg_id=msg.reply_to_message.id)

        if is_reply is not None:
            reply = is_reply
        else:
            reply = None
    else:
        reply = None

    return reply


async def forward_message_from_topic(msg: Message):
    """the message sent in topic > forward message to user"""

    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    tg_id = db_filters.get_tg_id_by_topic(topic_id=topic_id)
    is_protect = db_filters.get_is_protect_by_topic_id(topic_id=topic_id)
    reply = get_reply_to_message_by_topic(msg=msg)

    try:
        forward = await msg.copy(chat_id=tg_id, reply_to_message_id=reply,
                                 protect_content=is_protect)
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


async def send_contact_or_poll_or_location(c: Client, msg: Message, group: int, reply: int | None):
    try:
        if msg.contact is not None:
            # Handle contact message
            await c.send_contact(
                chat_id=group,
                phone_number=msg.contact.phone_number,
                first_name=msg.contact.first_name,
                last_name=msg.contact.last_name,
                reply_to_message_id=reply
            )

        elif msg.location is not None:
            # Handle location message
            await c.send_location(
                chat_id=group,
                latitude=msg.location.latitude,
                longitude=msg.location.longitude,
                reply_to_message_id=reply
            )

        elif msg.poll is not None:
            print('poll')
            # Handle quiz message
            await c.send_poll(
                chat_id=group,
                question=msg.poll.question,
                options=[o.text for o in msg.poll.options],
                reply_to_message_id=reply
            )

        elif msg.venue is not None:
            print('venue')
            # Handle location message
            await c.send_location(
                chat_id=group,
                latitude=msg.venue.location.latitude,
                longitude=msg.venue.location.longitude,
                reply_to_message_id=reply
            )

    except BadRequest as e:
        print("forward_message_from_user", e)
        return
