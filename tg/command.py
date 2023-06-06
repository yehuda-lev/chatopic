from pyrogram import Client
from pyrogram.errors import Forbidden, SlowmodeWait
from pyrogram.raw import functions
from pyrogram.raw import types as raw_types
from pyrogram.raw.types import MessageActionTopicEdit, MessageActionRequestedPeer
from pyrogram.types import (Message, ReplyKeyboardRemove, InlineKeyboardMarkup,
                            InlineKeyboardButton, CallbackQuery, BotCommand, BotCommandScopeChat)

from db import repository
from tg.strings import resolve_msg
from dotenv import load_dotenv
import os

load_dotenv()


def send_welcome(_, msg: Message):
    """
    send 'hello' in the user sent command '/start' to the bot
    """

    msg.reply(text=os.environ['WELCOME'])


def get_info_command(_, msg: Message):
    """
    send information what the user can do in topic.
    """
    try:
        msg.reply(text=resolve_msg(key='INFO'))
    except (Forbidden, SlowmodeWait) as e:
        print(e)


def protect(_, msg: Message):
    """
    in the admin want to protect/unprotect the messages to send the users
    """

    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    tg_id = repository.get_user_by_topic_id(topic_id=topic_id).id

    try:
        if msg.command[0] == "protect":
            is_protect = True
            msg.reply(resolve_msg('PROTECT'))
        else:
            is_protect = False
            msg.reply(resolve_msg('UNPROTECT'))

        repository.change_protect(tg_id=tg_id, is_protect=is_protect)

    except (Forbidden, SlowmodeWait) as e:
        print(e)


async def request_group(c: Client, msg: Message):
    """
    in the admin want to add group (sent command '/add_group') for the bot
    """
    if msg.chat.id != msg.from_user.id:
        await msg.reply(text=resolve_msg(key='REQUEST_IN_GROUP'))
        return
    peer = await c.resolve_peer(msg.chat.id)
    await c.invoke(
        functions.messages.SendMessage(peer=peer,
                                       message=resolve_msg(key='REQUEST'),
                                       random_id=c.rnd_id(),
                                       reply_markup=reply_markup(msg)
                                       )
    )


def reply_markup(msg):
    """
    :return raw keyboard
    """

    return raw_types.ReplyKeyboardMarkup(rows=[
        raw_types.KeyboardButtonRow(
            buttons=[
                raw_types.KeyboardButtonRequestPeer(
                    text=resolve_msg(key='REQUEST_BUTTON'), button_id=1,
                    peer_type=raw_types.RequestPeerTypeChat(
                        forum=True, bot_participant=True,
                        user_admin_rights=raw_types.ChatAdminRights(
                            add_admins=True, delete_messages=True,
                            manage_topics=True, change_info=True,
                            pin_messages=True
                        ),
                        bot_admin_rights=raw_types.ChatAdminRights(
                            change_info=True,
                            delete_messages=True,
                            manage_topics=True,
                            pin_messages=True
                        )
                    )
                )
            ]
        )
    ], resize=True)


# raw_update
async def create_group(c: Client, update: raw_types.UpdateNewMessage, users, chats):
    """
    in the bot a receives a message 'RequestPeerTypeChat'
    """

    try:
        if not update.message:
            return
        if not update.message.action:
            return

        if isinstance(update.message.action, MessageActionRequestedPeer):  # add group
            if repository.check_if_have_a_group():  # is have a group
                return
            tg_id = update.message.peer_id.user_id
            if repository.is_admin_exists(tg_id=tg_id):  # is admin

                first_group_id = update.message.action.peer.channel_id
                group_id = int(f"-100{first_group_id}")
                info = await c.get_chat(chat_id=group_id)
                group_name = info.title

                repository.create_group(group_id=group_id, name=group_name)  # create group in db

                text = resolve_msg(key='GROUP_ADD') \
                    .format(f"[{group_name}](t.me/c/{first_group_id})")

                await c.send_message(chat_id=tg_id, reply_to_message_id=update.message.id,
                                     text=text,
                                     reply_markup=ReplyKeyboardRemove(selective=True))
                await set_commands_for_group(c, group_id)

        # close/open topic > ban/unban user from the bot
        elif isinstance(update.message.action, MessageActionTopicEdit):
            # check if topic closed or just edited
            if update.message.action.closed is not None:
                await baned_user_by_closed_topic(c, update)

    except AttributeError:
        return


async def set_commands_for_group(c: Client, group_id: int):
    await c.set_bot_commands(
        commands=[
            BotCommand(command='info', description=resolve_msg('COMMAND_INFO')),
            BotCommand(command='delete', description=resolve_msg('COMMAND_DELETE')),
            BotCommand(command='protect', description=resolve_msg('COMMAND_PROTECT')),
            BotCommand(command='unprotect', description=resolve_msg('COMMAND_UNPROTECT')),
        ],
        scope=BotCommandScopeChat(chat_id=group_id)
    )


async def baned_user_by_closed_topic(c: Client, update: raw_types.UpdateNewMessage):
    """
    if topic is closed or opened > ban or unban the user
    """

    tg_id = repository.get_user_by_topic_id(update.message.reply_to.reply_to_msg_id).id
    banned = update.message.action.closed
    repository.change_banned(tg_id=tg_id, is_banned=banned)

    if banned:
        text = resolve_msg(key='BAN')
    else:
        text = resolve_msg(key='UNBAN')

    await c.send_message(chat_id=int(f'-100{update.message.peer_id.channel_id}'),
                         reply_to_message_id=update.message.id, text=text)


def ask_delete_group(_, msg: Message):
    """
    when the admin want to delete the group
    """
    if repository.get_my_group() is not None:
        msg.reply(text=resolve_msg('ASK_DEL_GROUP'), reply_to_message_id=msg.id,
                  reply_markup=InlineKeyboardMarkup([
                      [InlineKeyboardButton(text=resolve_msg('YES_DELETE'), callback_data='delete:yes')],
                      [InlineKeyboardButton(text=resolve_msg('NO_DELETE'), callback_data='delete:no')]
                  ]))
    else:
        msg.reply(text=resolve_msg('GROUP_NOT_EXISTS'))


def delete_group(c: Client, cbd: CallbackQuery):
    """
    when the admin want to delete the group
    """

    data = cbd.data.split(':')[1]

    if data == 'no':
        cbd.answer(text=resolve_msg('NOT_DEL_GROUP'), show_alert=True)
        c.delete_messages(chat_id=cbd.from_user.id, message_ids=cbd.message.id)
        c.delete_messages(chat_id=cbd.from_user.id, message_ids=cbd.message.reply_to_message.id)
        return

    else:
        cbd.answer(text=resolve_msg('DEL_GROUP'), show_alert=True)
        group = int(repository.get_my_group())
        c.leave_chat(chat_id=group)
        c.delete_messages(chat_id=cbd.from_user.id, message_ids=cbd.message.id)
        c.delete_messages(chat_id=cbd.from_user.id, message_ids=cbd.message.reply_to_message.id)

    # delete the group and all message
    repository.del_all()
