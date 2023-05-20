import pyrogram
from pyrogram import Client
from pyrogram.errors import BadRequest
from pyrogram.raw import functions
from pyrogram.raw import types as raw_types
from pyrogram.types import Message

from db import filters as filters_db
from tg.filters import is_admin
from tg.strings import resolve_msg
from dotenv import load_dotenv

load_dotenv()
import os


def send_welcome(c: Client, msg: Message):
    msg.reply(text=os.environ['WELCOME'])


# @app.on_message(pyrogram.filters.command("info") & pyrogram.filters.group)
def get_info_command(c: Client, msg: Message):
    msg.reply(text=resolve_msg(key='INFO', msg_or_user=msg))
    return


# @app.on_message(pyrogram.filters.command(["protect", "unprotect"]) & pyrogram.filters.group)
def protect(c: Client, msg: Message):
    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    tg_id = filters_db.get_tg_id_by_topic(topic_id=topic_id)
    if msg.command[0] == "protect":
        is_protect = True
        msg.reply(resolve_msg('PROTECT', msg))
    else:
        is_protect = False
        msg.reply(resolve_msg('UNPROTECT', msg))
    filters_db.change_protect(tg_id=tg_id, is_protect=is_protect)


# @app.on_message(pyrogram.filters.command(["ban", "unban"]) & pyrogram.filters.group)
def ban_users(c: Client, msg: Message):
    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    tg_id = filters_db.get_tg_id_by_topic(topic_id=topic_id)
    try:
        if msg.command[0] == "ban":
            filters_db.change_banned(tg_id=tg_id, is_banned=True)
            msg.reply(text=resolve_msg(key='BAN', msg_or_user=msg))
            closed = True
        else:
            filters_db.change_banned(tg_id=tg_id, is_banned=False)
            msg.reply(text=resolve_msg(key='UNBAN', msg_or_user=msg))
            closed = False
        peer = c.resolve_peer(msg.chat.id)
        c.invoke(functions.channels.EditForumTopic(
            channel=raw_types.InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
            topic_id=topic_id, closed=closed
        )
        )
    except BadRequest as e:
        print(e)


# @app.on_message(pyrogram.filters.command("add_group") & pyrogram.filters.create(is_admin))
async def request_group(c: Client, msg: Message):
    if msg.chat.id != msg.from_user.id:
        await msg.reply(text=resolve_msg(key='REQUEST_IN_GROUP', msg_or_user=msg))
        return
    peer = await c.resolve_peer(msg.chat.id)
    await c.invoke(
        functions.messages.SendMessage(peer=peer, message=resolve_msg(key='REQUEST', msg_or_user=msg),
                                       random_id=c.rnd_id(),
                                       reply_markup=reply_markup(msg))
    )


def reply_markup(msg):
    return raw_types.ReplyKeyboardMarkup(rows=[
        raw_types.KeyboardButtonRow(
            buttons=[
                raw_types.KeyboardButtonRequestPeer(
                    text=resolve_msg(key='REQUEST_BUTTON', msg_or_user=msg), button_id=1,
                    peer_type=raw_types.RequestPeerTypeChat(
                        forum=True, bot_participant=True,
                        user_admin_rights=raw_types.ChatAdminRights(
                            add_admins=True, delete_messages=True,
                            manage_topics=True, change_info=True
                        ),
                        bot_admin_rights=raw_types.ChatAdminRights(
                            change_info=True,
                            delete_messages=True,
                            manage_topics=True,
                        )
                    )
                )
            ]
        )
    ], resize=True)


# @app.on_raw_update()
async def create_group(c: Client, update: raw_types.UpdateNewMessage, users, chats):
    if filters_db.check_if_have_a_group():
        return
    try:
        if not update.message:
            return
        if not update.message.action:
            return
        tg_id = update.message.peer_id.user_id
        if filters_db.is_admin_exists(tg_id=tg_id):
            first_group_id = update.message.action.peer.channel_id
            group_id = int(f"-100{first_group_id}")
            info = await c.get_chat(chat_id=group_id)
            group_name = info.title
            filters_db.create_group(group_id=group_id, name=group_name)
            text = resolve_msg(key='GROUP_ADD', msg_or_user=users[tg_id], is_raw=True) \
                .format(f"[{group_name}](t.me/c/{first_group_id})")
            await c.send_message(chat_id=tg_id, reply_to_message_id=update.message.id, text=text,
                                 reply_markup=pyrogram.types.ReplyKeyboardRemove(selective=True))
    except AttributeError:
        return
