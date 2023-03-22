import os

from pyrogram import (Client, types, filters)
from pyrogram.errors import BadRequest
from pyrogram.raw import functions
from pyrogram.raw.functions.channels import create_forum_topic, EditForumTopic
from pyrogram.types import InlineKeyboardButton, KeyboardButton, Message, InputMedia, InputMediaPhoto, InputMediaVideo, \
    InputMediaDocument, InputMediaAudio, InputMediaAnimation, Update
from db import filters

import pyrogram.raw
from pyrogram.raw.types import (KeyboardButtonRequestPeer, RequestPeerTypeUser, ReplyKeyboardMarkup,
                                KeyboardButtonRow, UpdateNewMessage, RequestPeerTypeChat, RequestPeerTypeBroadcast,
                                ChatAdminRights, UpdateChannelUserTyping, UpdateChatParticipantAdd,
                                UpdateNewChannelMessage, InputChannel, Channel, MessageActionTopicEdit)
from pyrogram.raw.functions.messages import SendMessage
from pyrogram.raw.base import ChatAdminRights as Base_ChatAdminRights, KeyboardButton, InputPeer

from db.filters import is_tg_id_exists, get_topic_id_by_tg_id, get_group_by_tg_id, get_my_group, create_message, \
    get_tg_id_by_topic, is_topic_id_exists, get_topic_msg_id_by_user_msg_id, get_user_msg_id_by_topic_msg_id, \
    get_is_protect, change_protect, change_banned, get_is_banned, create_group, is_admin_exists, check_if_have_a_group
from tg.filters import is_admin, is_not_raw, is_have_a_group

# import pyrogram.raw.functions.channels.create_forum_topic
bot = Client("my_bot")


async def create_topic(cli: Client, msg: Message):
    name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
    username = "@" + str(username) if (username:= msg.from_user.username) else "אין"
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
    text = f"**פרטים על המשתמש**\n"\
    f"**שם:** [{name}](tg://user?id={msg.from_user.id})" \
    f"\n**שם משתמש:** {username}\n"\
    f"‏**ID:**`{msg.from_user.id}`"
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


@bot.on_message(pyrogram.filters.command(["protect", "unprotect"]) & pyrogram.filters.group)
def protect(c: Client, msg: Message):
    topic_id = is_topic(msg)
    if topic_id is False:
        return
    tg_id = get_tg_id_by_topic(topic_id=topic_id)
    if msg.command[0] == "protect":
        is_protect = True
    else:
        is_protect = False
    change_protect(tg_id=tg_id, is_protect=is_protect)
    msg.reply("Done")


@bot.on_message(pyrogram.filters.command(["ban", "unban"]) & pyrogram.filters.group)
def ban_users(c: Client, msg: Message):
    topic_id = is_topic(msg)
    if topic_id is False:
        return
    tg_id = get_tg_id_by_topic(topic_id=topic_id)
    try:
        if msg.command[0] == "ban":
            change_banned(tg_id=tg_id, is_banned=True)
            msg.reply("banned \nYou can unban him by sending the /unban command")
            closed = True
        else:
            change_banned(tg_id=tg_id, is_banned=False)
            msg.reply("unbanned \nYou can block it again by sending the /ban command")
            closed = False
        peer = c.resolve_peer(msg.chat.id)
        c.invoke(EditForumTopic(
            channel=InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
            topic_id=topic_id, closed=closed
            )
        )
    except BadRequest as e:
        print(e)


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


@bot.on_message(pyrogram.filters.create(is_not_raw) & pyrogram.filters.create(is_have_a_group))
async def forward_message(cli: Client, msg: Message):
    if msg.service or msg.game:
        print("service")
        return
    tg_id = msg.from_user.id
    if msg.chat.id == tg_id:
        await forward_message_from_user(cli=cli, msg=msg)
    elif msg.chat.id == -1001558142106:
        await forward_message_from_topic(cli=cli, msg=msg)
    else:
        print("other")


async def edit_message(cli: Client, msg: Message, chat_id, msg_id):
    if msg.text:
        await cli.edit_message_text(chat_id=chat_id, message_id=msg_id,text=msg.text)
        return
    caption = text if (text := msg.caption) else None
    if msg.photo:
        media = InputMediaPhoto(media=msg.photo.file_id, caption=caption)
    elif msg.video:
        media = InputMediaVideo(media=msg.video.file_id, caption=caption)
    elif msg.document:
        media = InputMediaDocument(media=msg.document.file_id, caption=caption)
    elif msg.audio:
        media = InputMediaAudio(media=msg.audio.file_id, caption=caption)
    elif msg.animation:
        media = InputMediaAnimation(media=msg.animation.file_id)
    else:
        print(msg)
        return
    await cli.edit_message_media(chat_id=chat_id, message_id=msg_id, media=media)


async def edit_message_by_user(cli: Client, msg: Message):
    tg_id = msg.from_user.id
    if not is_tg_id_exists(tg_id=tg_id):
        return
    if is_banned(tg_id):
        return
    chat_id = get_group_by_tg_id(tg_id=tg_id)
    msg_id = get_topic_msg_id_by_user_msg_id(tg_id=tg_id, msg_id=msg.id)
    await edit_message(cli, msg, chat_id, msg_id)


async def edit_message_by_topic(cli: Client, msg: Message):
    topic_id = is_topic(msg)
    if topic_id is False:
        return
    chat_id = get_tg_id_by_topic(topic_id=topic_id)
    if is_banned(tg_id=chat_id):
        await msg.reply("the user is ban\nYou can unban him by sending the /unban command")
        return
    msg_id = get_user_msg_id_by_topic_msg_id(topic_id, msg_id=msg.id)
    await edit_message(cli, msg, chat_id, msg_id)


@bot.on_edited_message(pyrogram.filters.create(is_have_a_group))
async def edited_message(cli: Client, msg: Message):
    tg_id = msg.from_user.id
    if msg.chat.id == tg_id:
        await edit_message_by_user(cli=cli, msg=msg)
    elif msg.chat.id == -1001558142106:
        await edit_message_by_topic(cli, msg)
    else:
        print("not edited")
        print(msg)
        return


@bot.on_message(pyrogram.filters.command("add_group") & pyrogram.filters.create(is_admin))
async def request_group(c: Client, msg: Message):
    peer = await bot.resolve_peer(msg.chat.id)
    await bot.invoke(
        SendMessage(peer=peer, message="אנא לחץ על הכפתור למטה כדי להוסיף את הבוט לקבוצה עם נושאים",
                    random_id=bot.rnd_id(),
                    reply_markup=ReplyKeyboardMarkup(rows=[
                        KeyboardButtonRow(
                            buttons=[
                                KeyboardButtonRequestPeer(
                                    text='הוסף אותי לקבוצה עם נושאים', button_id=1,
                                    peer_type=RequestPeerTypeChat(
                                        forum=True, bot_participant=True,
                                        user_admin_rights=ChatAdminRights(
                                            add_admins=True, delete_messages=True,
                                            manage_topics=True, change_info=True
                                            ),
                                        bot_admin_rights=ChatAdminRights(
                                            change_info=True,
                                            delete_messages=True,
                                            manage_topics=True,
                                            )
                                    )
                                )
                            ]
                        )
                    ], resize=True))
    )

@bot.on_raw_update()
async def create_group(client, update: UpdateNewMessage, users, chats):
    print(update)
    tg_id = update.message.peer_id.user_id
    try:
        if is_admin_exists(tg_id=tg_id):
            if not check_if_have_a_group():
                first_group_id = update.message.action.peer.channel_id
                group_id = int(f"-100{first_group_id}")
                info = await bot.get_chat(chat_id=group_id)
                print(info)
                group_name = info.title
                filters.create_group(group_id=group_id, name=group_name)
                text = f"הקבוצה [{group_name}](t.me/c/{first_group_id}) נוספה בהצלחה"
                await bot.send_message(chat_id=tg_id, reply_to_message_id=update.message.id,
                                       text=text, reply_markup=pyrogram.types.ReplyKeyboardRemove(selective=True))

    except AttributeError:
        await bot.send_message(chat_id=tg_id, reply_to_message_id=update.message.id,
                               text="הבוט בתחזוקה אנא חזור שנית בהמשך היום")
        return


bot.run()
