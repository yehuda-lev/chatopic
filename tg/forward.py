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


async def is_user_exists(c: Client, msg: Message):
    name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
    tg_id = msg.from_user.id
    if filters.is_tg_id_exists(tg_id=tg_id):
        return
    else:
        create = await create_topic(cli=c, msg=msg)
        group_id, topic_id = int("-100" + str(create.peer_id.channel_id)), create.id
        filters.create_user(tg_id=tg_id, group_id=group_id, topic_id=topic_id, name=name)


def is_topic(msg: Message):
    if not (msg.reply_to_top_message_id or msg.reply_to_message_id):
        return False
    topic_id = topic if (topic:= msg.reply_to_top_message_id) else msg.reply_to_message_id
    if not is_topic_id_exists(topic_id=topic_id):
        return False
    return topic_id

def is_banned(tg_id: int):
    return get_is_banned(tg_id=tg_id)

async def create_topic(cli: Client, msg: Message):
    name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
    username = "@" + str(username) if (username:= msg.from_user.username) else "אין"
    peer = await cli.resolve_peer(int(get_my_group()))
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
    topic_id = topic if (topic:= msg.reply_to_top_message_id) else msg.reply_to_message_id
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
    await is_user_exists(c=cli, msg=msg)
    if is_banned(tg_id=tg_id):
        return
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
    topic_id = is_topic(msg)
    if topic_id is False:
        return
    print(topic_id)
    tg_id = get_tg_id_by_topic(topic_id=topic_id)
    if is_banned(tg_id):
        await msg.reply("the user is ban\nYou can unban him by sending the /unban command")
        return
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
