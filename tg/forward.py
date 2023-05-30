import time

from pyrogram import Client
from pyrogram.errors import (BadRequest, InputUserDeactivated, UserIsBlocked, PeerIdInvalid, FloodWait, ChannelPrivate,
                             ChatWriteForbidden, ChatAdminRequired, Forbidden, ChannelInvalid, SlowmodeWait)
from pyrogram.types import Message
from pyrogram.raw.functions import messages as raw_func

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
        await forward_message_from_topic(cli=cli, msg=msg)

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

    try:
        # if msg forward with credit > forward to topic with credit
        if msg.forward_from is not None or msg.forward_from_chat is not None or \
                msg.forward_sender_name is not None:

            topic = db_filters.get_topic_id_by_tg_id(tg_id=tg_id)
            peer_user = await c.resolve_peer(msg.from_user.id)
            peer_group = await c.resolve_peer(group)
            # forward message with credit
            await c.invoke(
                raw_func.ForwardMessages(from_peer=peer_user,
                                         random_id=[c.rnd_id()],
                                         drop_author=False,
                                         id=[msg.id],
                                         to_peer=peer_group,
                                         top_msg_id=topic
                                         )
            )

        else:
            reply = get_reply_to_message_by_user(msg=msg)

            if msg.poll is not None or msg.venue is not None \
                    or msg.contact is not None or msg.location is not None:
                await send_contact_or_poll_or_location(c, msg, int(group), reply, protect=None)
                return

            forward = await msg.copy(chat_id=int(group), reply_to_message_id=reply)
            db_filters.create_message(tg_id_or_topic_id=tg_id, is_topic_id=False,
                                      user_msg_id=msg.id, topic_msg_id=forward.id)

    except (FloodWait, SlowmodeWait) as e:
        time.sleep(e.value)

    except (ChannelPrivate, ChatWriteForbidden, ChatAdminRequired,
            ChannelInvalid, Forbidden, BadRequest) as e:
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


async def forward_message_from_topic(cli: Client, msg: Message):
    """the message sent in topic > forward message to user"""

    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    tg_user = db_filters.get_user_by_topic_id(topic_id=topic_id)
    tg_id = tg_user.id
    is_protect = tg_user.protect
    reply = get_reply_to_message_by_topic(msg=msg)

    try:
        if msg.poll is not None or msg.venue is not None \
                or msg.contact is not None or msg.location is not None:
            await send_contact_or_poll_or_location(c=cli, msg=msg, chat=tg_id,
                                                   reply=reply, protect=is_protect)
            return

        forward = await msg.copy(chat_id=tg_id, reply_to_message_id=reply,
                                 protect_content=is_protect)
        db_filters.create_message(tg_id_or_topic_id=topic_id, is_topic_id=True,
                                  user_msg_id=forward.id, topic_msg_id=msg.id)

    except (FloodWait, SlowmodeWait) as e:
        time.sleep(e.value)

    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid, BadRequest) as e:
        db_filters.change_active(tg_id=tg_id, active=False)
        print(f'forward_message_from_topic {e}')
        await msg.reply(text=e.MESSAGE)


async def send_contact_or_poll_or_location(c: Client, msg: Message, chat: int, reply: int | None, protect: bool | None):
    try:
        if msg.contact is not None:
            # Handle contact message
            forward = await c.send_contact(
                chat_id=chat,
                phone_number=msg.contact.phone_number,
                first_name=msg.contact.first_name,
                last_name=msg.contact.last_name,
                reply_to_message_id=reply,
                protect_content=protect
            )

        elif msg.location is not None:
            # Handle location message
            forward = await c.send_location(
                chat_id=chat,
                latitude=msg.location.latitude,
                longitude=msg.location.longitude,
                reply_to_message_id=reply,
                protect_content=protect
            )

        elif msg.poll is not None:
            # Handle quiz message
            forward = await c.send_poll(
                chat_id=chat,
                question=msg.poll.question,
                options=[o.text for o in msg.poll.options],
                reply_to_message_id=reply,
                protect_content=protect
            )

        else:  # venue
            # Handle location message
            forward = await c.send_location(
                chat_id=chat,
                latitude=msg.venue.location.latitude,
                longitude=msg.venue.location.longitude,
                reply_to_message_id=reply,
                protect_content=protect
            )

        db_filters.create_message(tg_id_or_topic_id=chat, is_topic_id=False,
                                  user_msg_id=msg.id, topic_msg_id=forward.id)

    except (FloodWait, SlowmodeWait) as e:
        time.sleep(e.value)

    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid) as e:
        db_filters.change_active(tg_id=chat, active=False)
        print(f'forward_message_from_topic {e}')
        await msg.reply(text=e.MESSAGE)

    except (ChannelPrivate, ChatWriteForbidden, ChatAdminRequired,
            ChannelInvalid, Forbidden, BadRequest) as e:
        print("forward_message_from_user", e)
        return
