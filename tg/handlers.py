from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from db import filters
from db.filters import is_tg_id_exists


async def create_topic(cli: Client, msg: Message):
    name = msg.from_user.first_name + (" " + msg.from_user.last_name if msg.from_user.last_name else "")
    peer = await cli.resolve_peer(msg.chat.id)
    from pyrogram.raw.types import InputChannel
    create = await cli.invoke(functions.channels.CreateForumTopic(
        channel=InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
        title=name,
        random_id=1000,
        icon_color=None,
        icon_emoji_id=5312016608254762256,
        send_as=None
        )
    )
    return create.updates[1].message


async def is_user_exists(c: Client, msg: Message):
    name = msg.from_user.first_name + (" " + msg.from_user.last_name if msg.from_user.last_name else "")
    tg_id = msg.from_user.id
    print(filters.is_tg_id_exists(tg_id=tg_id))
    if filters.is_tg_id_exists(tg_id=tg_id):
        return
    else:
        create = await create_topic(cli=c, msg=msg)
        group_id = int("-100" + str(create.peer_id.channel_id))
        topic_id = create.id
        print(group_id, topic_id, tg_id, msg.chat.id)
        filters.create_user(tg_id=tg_id, group_id=group_id, topic_id=topic_id, name=name)
