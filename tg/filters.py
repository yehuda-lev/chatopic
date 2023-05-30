import time

from pyrogram import Client
from pyrogram.enums import MessageEntityType
from pyrogram.errors import ButtonUserPrivacyRestricted, ChatWriteForbidden, Forbidden, ChatAdminRequired, FloodWait
from pyrogram.raw import functions
from pyrogram.types import Message, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton

from db import filters as db_filters
from tg.strings import resolve_msg


def is_banned(_, __, msg: Message):
    """
    filter to check if user is banned or not
    """
    try:
        tg_id = msg.from_user.id
    except AttributeError:
        return False

    if msg.chat.id == tg_id:
        if db_filters.get_user_by_tg_id(tg_id=tg_id).ban:
            return False
    else:
        topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
        if db_filters.get_user_by_topic_id(topic_id=topic_id).ban:
            msg.reply(resolve_msg(key='USER_IS_BANNED'))
            return False
    return True


async def is_user_exists(_, c: Client, msg: Message):
    """
    filter to check if user exists. if not exists >
    create topic for user and create topic in the DB
    """
    try:
        tg_id = msg.from_user.id
    except AttributeError:
        return True

    if db_filters.is_tg_id_exists(tg_id=tg_id):
        if db_filters.is_user_active(tg_id):
            return True
        else:
            db_filters.change_active(tg_id=tg_id, active=True)
    else:
        name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
        create = await create_topic(cli=c, msg=msg)
        if create is False:
            return False

        group_id, topic_id = int("-100" + str(create.peer_id.channel_id)), create.id
        db_filters.create_user(tg_id=tg_id, group_id=group_id, topic_id=topic_id, name=name)
        return True


async def create_topic(cli: Client, msg: Message):
    """
    func to create topic in group for the user
    """

    name = msg.from_user.first_name + (" " + last if (last := msg.from_user.last_name) else "")
    username = "@" + str(username) if (username := msg.from_user.username) else "❌"

    try:
        # create topic
        peer = await cli.resolve_peer(int(db_filters.get_my_group()))
        create = await cli.invoke(functions.channels.CreateForumTopic(
            channel=peer,
            title=name,
            random_id=1000000,
            icon_color=None,
            icon_emoji_id=5312016608254762256,
            send_as=None
            )
        )

    except (ChatWriteForbidden, Forbidden) as e:
        print(e)
        return False

    # time.sleep(0.3)

    text = resolve_msg(key='INFO_TOPIC'). \
        format(f"[{name}](tg://user?id={msg.from_user.id})", f"{username}", f"{msg.from_user.id}",
               f"{msg.from_user.id}", f"{msg.from_user.id}")

    # check if user have a photo
    photo = photo if (photo := msg.from_user.photo) else None

    chat_id = int("-100" + str(create.updates[1].message.peer_id.channel_id))

    try:
        try:
            if photo is None:  # if not have a photo > send text
                send = await cli.send_message(chat_id=chat_id, text=text,
                                              reply_to_message_id=create.updates[1].message.id,
                                              reply_markup=InlineKeyboardMarkup([[
                                                  InlineKeyboardButton(text=name, user_id=msg.from_user.id)]]))

            else:  # if user have a photo > send photo + text
                async for photo in cli.get_chat_photos(msg.from_user.id, limit=1):
                    send = await cli.send_photo(chat_id=chat_id, photo=photo.file_id,
                                                caption=text, reply_to_message_id=create.updates[1].message.id,
                                                reply_markup=InlineKeyboardMarkup([[
                                                    InlineKeyboardButton(text=name, user_id=msg.from_user.id)]]))
        except ButtonUserPrivacyRestricted:
            if photo is None:  # if not have a photo > send text
                send = await cli.send_message(chat_id=chat_id, text=text,
                                              reply_to_message_id=create.updates[1].message.id)

            else:  # if user have a photo > send photo + text
                async for photo in cli.get_chat_photos(msg.from_user.id, limit=1):
                    send = await cli.send_photo(chat_id=chat_id, photo=photo.file_id,
                                                caption=text,
                                                reply_to_message_id=create.updates[1].message.id)

        # pinned the message
        try:
            await cli.unpin_chat_message(chat_id=chat_id, message_id=send.id)
            await cli.pin_chat_message(chat_id=chat_id, message_id=send.id)
        except ChatAdminRequired:
            return False

    except FloodWait as e:
        time.sleep(e.value)

    return create.updates[1].message


def is_topic_or_is_user(_, __, msg: Message) -> bool:
    """
    check if msg send by user or sent in topic (and topic exists) or of topic
    """
    try:
        tg_id = msg.from_user.id
        if msg.chat.id == tg_id:  # chat_id is user
            return True

    except AttributeError:  # when the user send message from channel
        pass

    if db_filters.is_group_exists(group_id=msg.chat.id):  # is my_group
        if not (msg.reply_to_top_message_id or msg.reply_to_message_id):  # not in topic
            return False

        topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id

        if db_filters.is_topic_id_exists(topic_id=topic_id):  # topic exists
            return True

    return False


def is_not_raw(_, __, msg: Message) -> bool:
    """
    check is msg not raw.
    When sharing a group to a bot;
    A message is received that is only supported in 'raw message'
    """

    if msg.text or msg.game or msg.command or msg.photo or msg.document or msg.voice \
            or msg.service or msg.media or msg.audio or msg.video or msg.contact \
            or msg.location or msg.sticker or msg.poll or msg.animation or msg.venue:
        return True

    return False


def is_admin(_, __, msg: Message) -> bool:
    """
    check if msg sent by admin or not.
    """

    if not db_filters.is_admin_exists(tg_id=msg.from_user.id):
        msg.reply(resolve_msg(key='IS_ADMIN'))
        return False
    return True


def is_have_a_group(_, __, msg: Message):
    """
    check if you have a group.
    """

    if not db_filters.check_if_have_a_group():

        if db_filters.is_admin_exists(tg_id=msg.from_user.id):

            if not msg.service:
                if msg.command:
                    if msg.command[0] == 'add_group':
                        return False

                msg.reply(resolve_msg(key='GROUP_NOT_EXISTS'))

        else:
            msg.reply(resolve_msg(key='BOT_NOT_WORKING'))

        return False

    return True


def is_force_reply(_, __, msg: Message) -> bool:
    """
    check if msg force reply.
    in the admin send message for everyone
    """

    try:
        if isinstance(msg.reply_to_message.reply_markup, ForceReply):
            return True
    except AttributeError:
        return False
    return False


def is_command(_, __, msg: Message) -> bool:
    """
    check if the message is command or not.
    """

    if msg.command:
        return False
    else:
        if msg.entities:
            if msg.entities[0].type == MessageEntityType.BOT_COMMAND:
                return False
    return True
