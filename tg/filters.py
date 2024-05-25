import asyncio
import logging

from pyrogram import Client, filters, enums, errors, raw, types
from sqlalchemy.exc import NoResultFound

from db import repository
from tg.strings import resolve_msg
from data import config

logger = logging.getLogger(__name__)

settings = config.get_settings()


async def create_user() -> filters.Filter:
    """
    Create user and topic
    """

    async def func(_, client: Client, msg: types.Message) -> bool:

        tg_id = msg.from_user.id

        try:
            user = repository.get_user_by_tg_id(tg_id=tg_id)
            if not user.active:
                repository.update_user(user_tg_id=tg_id, active=True)
            if user.banned:
                return False
        except NoResultFound:
            return await create_topic(client, msg)

        return True

    return filters.create(func, "Create user")


async def create_topic(client: Client, msg: types.Message):
    """
    Create topic
    """

    name = msg.from_user.full_name
    tg_id = msg.from_user.id
    username = f"@{username}" if (username := msg.from_user.username) else "❌"
    group_id = settings.tg_group_topic_id

    try:
        # create topic
        topic = await client.create_forum_topic(
            chat_id=group_id,
            name=f"{name} | {tg_id}",
        )

    except (errors.ChatWriteForbidden, errors.Forbidden) as e:
        logger.error(e)
        return False

    repository.create_user_and_topic(tg_id=tg_id, name=name, topic_id=topic.id)

    await asyncio.sleep(0.3)

    text = resolve_msg(key='INFO_TOPIC'). \
        format(f"[{name}](tg://user?id={tg_id})", f"{username}", f"{tg_id}",
               f"{tg_id}", f"{tg_id}")

    # check if user have a photo
    photo = photo if (photo := msg.from_user.photo) else None

    reply_markup = types.InlineKeyboardMarkup(
                        [
                            [types.InlineKeyboardButton(text=name, user_id=tg_id)]
                        ]
                    )
    privacy = False
    send = None

    while True:
        try:
            if photo is None:  # if not have a photo > send text
                send = await client.send_message(
                    chat_id=group_id, text=text,
                    reply_parameters=types.ReplyParameters(message_id=topic.id),
                    reply_markup=reply_markup if not privacy else None
                )

            else:
                async for photo in client.get_chat_photos(tg_id, limit=1):
                    send = await client.send_photo(
                        chat_id=group_id, photo=await photo.download(in_memory=True),
                        caption=text, reply_parameters=types.ReplyParameters(message_id=topic.id),
                        reply_markup=reply_markup if not privacy else None
                    )
            break

        except errors.FloodWait as e:
            logger.debug(f"FloodWait when send message create_topic: {e.value}")
            await asyncio.sleep(e.value)
            continue

        except errors.ButtonUserPrivacyRestricted:
            privacy = True
            continue

    try:
        # pinned the message
        await client.unpin_chat_message(chat_id=group_id, message_id=send.id)
        await client.pin_chat_message(chat_id=group_id, message_id=send.id)
    except errors.FloodWait as e:
        logger.debug(e)
        await asyncio.sleep(e.value)

    return True


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

    if repository.is_group_exists(group_id=msg.chat.id):  # is my_group
        if not (msg.reply_to_top_message_id or msg.reply_to_message_id):  # not in topic
            return False

        topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id

        if repository.is_topic_id_exists(topic_id=topic_id):  # topic exists
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

    if not repository.is_admin_exists(tg_id=msg.from_user.id):
        msg.reply(resolve_msg(key='IS_ADMIN'))
        return False
    return True


def is_have_a_group(_, __, msg: Message):
    """
    check if you have a group.
    """

    if not repository.check_if_have_a_group():

        if repository.is_admin_exists(tg_id=msg.from_user.id):

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
