from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.raw.types import InputChannel
from pyrogram.types import Message

import db
from db import filters
from db.filters import is_admin_exists, check_if_have_a_group

async def is_user_exists(_, c: Client, msg: Message):
    tg_id = msg.from_user.id
    if filters.is_tg_id_exists(tg_id=tg_id):
        return True
    else:
        name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
        create = await create_topic(cli=c, msg=msg)
        group_id, topic_id = int("-100" + str(create.peer_id.channel_id)), create.id
        filters.create_user(tg_id=tg_id, group_id=group_id, topic_id=topic_id, name=name)
        return True


async def create_topic(cli: Client, msg: Message):
    name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
    username = "@" + str(username) if (username:= msg.from_user.username) else "אין"
    peer = await cli.resolve_peer(int(filters.get_my_group()))
    create = await cli.invoke(functions.channels.CreateForumTopic(
        channel=InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
        title=name,
        random_id=1000000,
        icon_color=None,
        icon_emoji_id=5312016608254762256,
        send_as=None
        )
    )
    text = f"**פרטים על המשתמש**\n"\
    f"**שם:** [{name}](tg://user?id={msg.from_user.id})" \
    f"\n**שם משתמש:** {username}\n"\
    f"‏**ID:** `{msg.from_user.id}`\n\n"\
    f"לקבלת מידע על הפקודות הנתמכות בצאט אנא שלח את הפקודה /info"
    photo = photo if (photo:= msg.from_user.photo) else None
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
    if not (msg.reply_to_top_message_id or msg.reply_to_message_id):
        return False
    topic_id = topic if (topic:= msg.reply_to_top_message_id) else msg.reply_to_message_id
    if not filters.is_topic_id_exists(topic_id=topic_id):
        return False
    return True


def is_not_raw(_, __, msg: Message) -> bool:
    if msg.text or msg.game or msg.command or msg.photo or msg.document or msg.voice \
            or msg.service or msg.media or msg.audio or msg.video or msg.contact \
            or msg.location or msg.sticker or msg.poll or msg.animation:
        return True
    return False


def is_admin(_, __, msg: Message) -> bool:
    if not is_admin_exists(tg_id=msg.from_user.id):
        msg.reply("אינך מנהל")
        return False
    return True


def is_have_a_group(_, __, msg: Message):
    if not check_if_have_a_group():
        msg.reply("אין עדיין קבוצה, אני שלח את הפקודה /add_group")
        return False
    return True
