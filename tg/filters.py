from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.raw import types as raw_types
from pyrogram.types import Message

from db import filters as db_filters
from tg.strings import resolve_msg


def is_banned(_, __, msg: Message):
    tg_id = msg.from_user.id
    if msg.chat.id == tg_id:
        if db_filters.get_is_banned_by_tg_id(tg_id=tg_id):
            return False
    else:
        topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
        if db_filters.get_is_banned_by_topic_id(topic_id=topic_id):
            msg.reply(resolve_msg(key='USER_IS_BANNED', msg_or_user=msg))
            return False
    return True


async def is_user_exists(_, c: Client, msg: Message):
    tg_id = msg.from_user.id
    if db_filters.is_tg_id_exists(tg_id=tg_id):
        if db_filters.is_user_active(tg_id):
            return True
        else:
            db_filters.change_active(tg_id=tg_id, active=True)
    else:
        name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
        create = await create_topic(cli=c, msg=msg)
        group_id, topic_id = int("-100" + str(create.peer_id.channel_id)), create.id
        db_filters.create_user(tg_id=tg_id, group_id=group_id, topic_id=topic_id, name=name)
        return True


async def create_topic(cli: Client, msg: Message):
    name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
    username = "@" + str(username) if (username := msg.from_user.username) else "❌"
    peer = await cli.resolve_peer(int(db_filters.get_my_group()))
    create = await cli.invoke(functions.channels.CreateForumTopic(
        channel=raw_types.InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
        title=name,
        random_id=1000000,
        icon_color=None,
        icon_emoji_id=5312016608254762256,
        send_as=None
    )
    )
    text = resolve_msg(key='INFO_TOPIC', msg_or_user=msg).\
        format(f"[{name}](tg://user?id={msg.from_user.id})", f"{username}", f"{msg.from_user.id}")
    photo = photo if (photo := msg.from_user.photo) else None
    chat_id = int("-100" + str(create.updates[1].message.peer_id.channel_id))
    if photo is None:
        await cli.send_message(chat_id=chat_id, text=text,
                               reply_to_message_id=create.updates[1].message.id)
    else:
        async for photo in cli.get_chat_photos(msg.from_user.id, limit=1):
            await cli.send_photo(chat_id=chat_id, photo=photo.file_id,
                                 caption=text, reply_to_message_id=create.updates[1].message.id)
    return create.updates[1].message


def is_topic(_, __, msg: Message):
    tg_id = msg.from_user.id
    if not msg.chat.id == tg_id:
        if not (msg.reply_to_top_message_id or msg.reply_to_message_id):
            return False
        topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
        if not db_filters.is_topic_id_exists(topic_id=topic_id):
            return False
        return True
    return True


def is_not_raw(_, __, msg: Message) -> bool:
    if msg.text or msg.game or msg.command or msg.photo or msg.document or msg.voice \
            or msg.service or msg.media or msg.audio or msg.video or msg.contact \
            or msg.location or msg.sticker or msg.poll or msg.animation:
        return True
    return False


def is_admin(_, __, msg: Message) -> bool:
    if not db_filters.is_admin_exists(tg_id=msg.from_user.id):
        msg.reply(resolve_msg(key='IS_ADMIN', msg_or_user=msg))
        return False
    return True


def is_have_a_group(_, __, msg: Message):
    if not db_filters.check_if_have_a_group():
        if db_filters.is_admin_exists(tg_id=msg.from_user.id):
            if not (msg.command[0] == 'add_group') and not msg.service:
                msg.reply(resolve_msg(key='GROUP_NOT_EXISTS', msg_or_user=msg))
        else:
            msg.reply(resolve_msg(key='BOT_NOT_WORKING', msg_or_user=msg))
        return False
    return True
