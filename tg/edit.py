from pyrogram import Client
from pyrogram import types
from pyrogram.errors import MessageIdInvalid, MessageNotModified, ChannelPrivate, BadRequest
from pyrogram.types import CallbackQuery

from db import repository
from tg.strings import resolve_msg


async def edited_message(cli: Client, msg: types.Message):
    """
    edit message in user if edited by topic
    or edit message in topic if edited by user
    """

    tg_id = msg.from_user.id
    if msg.chat.id == tg_id:  # edited by user
        await edit_message_by_user(cli=cli, msg=msg)

    elif repository.is_group_exists(group_id=msg.chat.id):  # edited by topic
        await edit_message_by_topic(cli, msg)

    else:
        print("not edited")
        return


async def edit_message_by_user(cli: Client, msg: types.Message):
    """
    the user edit message > edit message in topic
    """

    tg_id = msg.from_user.id
    chat_id = repository.get_user_by_tg_id(tg_id=tg_id).group.id

    msg_id = repository.get_topic_msg_id_by_user_msg_id(tg_id=tg_id, msg_id=msg.id)
    if msg_id is None:
        return
    await edit_message(cli, msg, chat_id, msg_id, is_topic=True)


async def edit_message(cli: Client, msg: types.Message, chat_id, msg_id, is_topic: bool):
    """edit message in chat_id"""

    if msg.text:  # not caption
        try:
            await cli.edit_message_text(
                chat_id=chat_id, message_id=msg_id, text=msg.text, entities=msg.entities,
                reply_markup=get_reply_markup(msg, is_topic)
            )

        except (MessageIdInvalid, MessageNotModified):
            pass
        except (ChannelPrivate, BadRequest):
            pass
        return

    caption = text if (text := msg.caption.markdown) else None
    if msg.photo:
        media = types.InputMediaPhoto(media=msg.photo.file_id, caption=caption)
    elif msg.video:
        media = types.InputMediaVideo(media=msg.video.file_id, caption=caption)
    elif msg.document:
        media = types.InputMediaDocument(media=msg.document.file_id, caption=caption)
    elif msg.audio:
        media = types.InputMediaAudio(media=msg.audio.file_id, caption=caption)
    elif msg.animation:
        media = types.InputMediaAnimation(media=msg.animation.file_id)
    elif msg.voice:
        # TODO check if you can edit the message
        return
    else:
        return

    try:
        await cli.edit_message_media(
            chat_id=chat_id, message_id=msg_id, media=media,
            reply_markup=get_reply_markup(msg, is_topic))

    except (MessageIdInvalid, MessageNotModified):
        pass
    except (ChannelPrivate, BadRequest):
        pass


def get_reply_markup(msg: types.Message, is_topic: bool) -> types.InlineKeyboardMarkup | None:
    """
    return InlineKeyboardButton URL (and EDIT if is_topic)
    if msg is instance InlineKeyboardButton URL else return None
    (or EDIT if is_topic)
    """

    if isinstance(msg.reply_markup, types.InlineKeyboardMarkup):

        if any(True if b.url is not None else False for a in msg.reply_markup.inline_keyboard for b in a):
            #  if InlineKeyboardButton is url
            reply_markup = [[types.InlineKeyboardButton(text=b.text, url=b.url)]
                            for a in msg.reply_markup.inline_keyboard for b in a if b.url is not None]
        else:
            reply_markup = None
    else:
        reply_markup = None

    if is_topic:
        if reply_markup is None:
            reply_markup = [[types.InlineKeyboardButton(
                text=resolve_msg(key='EDIT'), callback_data='edit')]]

        else:
            reply_markup.append([types.InlineKeyboardButton(
                text=resolve_msg(key='EDIT'), callback_data='edit')])

    if reply_markup is not None:
        reply_markup = types.InlineKeyboardMarkup(reply_markup)

    return reply_markup


def answer_the_message_is_edited(_, cbd: CallbackQuery):
    cbd.answer(text=resolve_msg(key='EDIT_CBD'), show_alert=True)


async def edit_message_by_topic(cli: Client, msg: types.Message):
    """
    the message edit in topic > edit message in the user
    """

    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    tg_user = repository.get_user_by_topic_msg_id(topic_id=topic_id, msg_id=msg.id)

    try:
        chat_id = int(tg_user.tg_id.id)
        msg_id = tg_user.user_msg_id
    except AttributeError:
        return

    if msg_id is None:
        return

    await edit_message(cli, msg, chat_id, msg_id, is_topic=False)
