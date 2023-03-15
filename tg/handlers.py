from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.raw.types import InputChannel
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from db import filters
from db.filters import is_tg_id_exists, get_group_by_tg_id, get_topic_id_by_tg_id, get_my_group, create_message, \
    is_topic_id_exists, get_tg_id_by_topic


async def create_topic(cli: Client, msg: Message):
    name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
    try:
        peer = await cli.resolve_peer(-1001558142106)
        create = await cli.invoke(functions.channels.CreateForumTopic(
            channel=InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
            title=name,
            random_id=1000000,
            icon_color=None,
            icon_emoji_id=5312016608254762256,
            send_as=None
            )
        )
        return create.updates[1].message
    except Exception as e:
        print(e)

async def is_user_exists(c: Client, msg: Message):
    name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
    tg_id = msg.from_user.id
    print("tg_id exists:", filters.is_tg_id_exists(tg_id=tg_id))
    if filters.is_tg_id_exists(tg_id=tg_id):
        return
    else:
        create = await create_topic(cli=c, msg=msg)
        group_id = int("-100" + str(create.peer_id.channel_id))
        topic_id = create.id
        print(f"create topic; group: {group_id}, chat_id: {msg.chat.id}, topic: {topic_id}, tg_id: {tg_id}")
        filters.create_user(tg_id=tg_id, group_id=group_id, topic_id=topic_id, name=name)