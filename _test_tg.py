from pyrogram import Client, filters, types
from pyrogram.errors import BadRequest
from pyrogram.raw import functions
from pyrogram.raw.functions.channels import create_forum_topic
from pyrogram.types import InlineKeyboardButton, KeyboardButton, Message
from db import filters

import pyrogram.raw
from pyrogram.raw.types import (KeyboardButtonRequestPeer, RequestPeerTypeUser, ReplyKeyboardMarkup,
                                KeyboardButtonRow, UpdateNewMessage, RequestPeerTypeChat, RequestPeerTypeBroadcast,
                                ChatAdminRights, UpdateChannelUserTyping, UpdateChatParticipantAdd,
                                UpdateNewChannelMessage, InputChannel, Channel)
from pyrogram.raw.functions.messages import SendMessage
from pyrogram.raw.base import ChatAdminRights as Base_ChatAdminRights, KeyboardButton, InputPeer

from db.filters import is_tg_id_exists, get_topic_id_by_tg_id, get_group_by_tg_id, get_my_group, create_message, \
    get_tg_id_by_topic, is_topic_id_exists, get_topic_msg_id_by_user_msg_id, get_user_msg_id_by_topic_msg_id

# import pyrogram.raw.functions.channels.create_forum_topic
bot = Client("my_bot")


async def create_topic(cli: Client, msg: Message):
    name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
    username = username if (username:= msg.from_user.username) else "None"
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
    await cli.send_message(chat_id=int("-100" + str(create.updates[1].message.peer_id.channel_id)),
                           text=f"**INFO THE USER**\n"
                                f"**Name:** [{name}](tg://user?id={msg.from_user.id})" \
                                f"\n**Username:** @{username}\n"
                                f"**ID:** `{msg.from_user.id}`",
                           reply_to_message_id=create.updates[1].message.id)
    return create.updates[1].message

async def is_user_exists(c: Client, msg: Message):
    name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
    tg_id = msg.from_user.id
    if filters.is_tg_id_exists(tg_id=tg_id):
        return
    else:
        create = await create_topic(cli=c, msg=msg)
        group_id, topic_id = int("-100" + str(create.peer_id.channel_id)), create.id
        filters.create_user(tg_id=tg_id, group_id=group_id, topic_id=topic_id, name=name)


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
    topic_id = topic if(topic:= msg.reply_to_top_message_id) else msg.reply_to_message_id
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
    if not (msg.reply_to_top_message_id or msg.reply_to_message_id):
        return
    topic_id = topic if(topic:= msg.reply_to_top_message_id) else msg.reply_to_message_id
    if not is_topic_id_exists(topic_id=topic_id):
        return
    tg_id = get_tg_id_by_topic(topic_id=topic_id)
    reply = get_reply_to_message_by_topic(msg=msg)
    try:
        forward = await msg.copy(chat_id=tg_id, reply_to_message_id=reply)
        create_message(tg_id_or_topic_id=topic_id, is_topic_id=True,
                       user_msg_id=forward.id, topic_msg_id=msg.id)
    except BadRequest as e:
        print("forward_message_from_topic", e)
        return


@bot.on_message()
async def forward_message(cli: Client, msg: Message):
    tg_id = msg.from_user.id
    if msg.chat.id == tg_id:
        await forward_message_from_user(cli=cli, msg=msg)
    elif msg.chat.id == -1001558142106:
        await forward_message_from_topic(cli=cli, msg=msg)
    else:
        print("other")


async def edit_message_by_user(cli: Client, msg: Message):
    tg_id = msg.from_user.id
    msg_id = msg.id
    if not is_tg_id_exists(tg_id=tg_id):
        return
    chat_id = get_group_by_tg_id(tg_id=tg_id)
    msg_topic_id = get_topic_msg_id_by_user_msg_id(tg_id=tg_id, msg_id=msg_id)
    if msg.text:
        await cli.edit_message_text(chat_id=chat_id, message_id=msg_topic_id,
                                    text=msg.text)


async def edited_message(cli: Client, msg: Message):
    tg_id = msg.from_user.id
    if msg.chat.id == tg_id:
        await edit_message_by_user(cli=cli, msg=msg)

    # print(msg.reply(text="blaa"))
    # print(cli.edit_message_text(chat_id=5679878442, message_id=876, text="bla"))


sg_id = 687
g_id = 5679878442





# def is_exists(c: Client, msg: Message):
#     num = 0
#     for i in get_config().default_users_id:
#         if i == msg.chat.id:
#             num += 1
#     if num == 0:
#         msg.reply("אינך מורשה!")
#         c.block_user(msg.from_user.id)
#         return
#     text = ""
#     try:
#         if msg.text:
#             text = msg.text
#         elif msg.caption:
#             text = msg.caption
#         elif msg.video:
#             if msg.video.file_name:
#                 text = msg.video.file_name
#             else:
#                 text = msg.video.file_id
#         elif msg.document:
#             if msg.document.file_name:
#                 text = msg.document.file_name
#             else:
#                 text = msg.document.file_id
#         elif msg.audio:
#             if msg.audio.file_name:
#                 text = msg.audio.file_name
#             else:
#                 text = msg.audio.file_id
#         elif msg.photo:
#             text = msg.photo.file_id
#         if is_exists_db(msg=text):
#             c.delete_messages(chat_id=msg.chat.id, message_ids=msg.id)
#         else:
#             add_msg_db(msg=text, msg_id=msg.id)
#     except Exception as e:
#         c.send_message(chat_id="yehudalev", text=f"{e}")




bot.run()
