from pyrogram import Client
from pyrogram import types
from pyrogram.errors import MessageIdInvalid, MessageNotModified
from pyrogram.types import CallbackQuery

from db import filters as filters_db
from tg.strings import resolve_msg


async def edited_message(cli: Client, msg: types.Message):
    """
    edit message in user if edited by topic
    or edit message in topic if edited by user
    """

    tg_id = msg.from_user.id
    if msg.chat.id == tg_id:  # edited by user
        await edit_message_by_user(cli=cli, msg=msg)

    elif filters_db.is_group_exists(group_id=msg.chat.id):  # edited by topic
        await edit_message_by_topic(cli, msg)

    else:
        print("not edited")
        return


async def edit_message_by_user(cli: Client, msg: types.Message):
    """
    the user edit message > edit message in topic
    """

    tg_id = msg.from_user.id
    chat_id = filters_db.get_group_by_tg_id(tg_id=tg_id)
    msg_id = filters_db.get_topic_msg_id_by_user_msg_id(tg_id=tg_id, msg_id=msg.id)
    if msg_id is None:
        return
    await edit_message(cli, msg, chat_id, msg_id, is_topic=True)


async def edit_message(cli: Client, msg: types.Message, chat_id, msg_id, is_topic: bool):
    """edit message in chat_id"""

    if msg.text:  # not caption
        try:
            await cli.edit_message_text(chat_id=chat_id, message_id=msg_id, text=msg.text,
                                        reply_markup=send_reply_markup_only_in_topic(is_topic)
                                        )
        except MessageIdInvalid:
            pass
        except MessageNotModified:
            pass
        return

    caption = text if (text := msg.caption) else None
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
        print(msg)
        return

    try:
        await cli.edit_message_media(chat_id=chat_id, message_id=msg_id, media=media,
                                     reply_markup=send_reply_markup_only_in_topic(is_topic)
                                     )
    except MessageIdInvalid:
        pass
    except MessageNotModified:
        pass


def send_reply_markup_only_in_topic(is_topic: bool):
    if is_topic:
        return types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton(
                text=resolve_msg(key='EDIT'), callback_data='edit')]]
        )
    return None


def answer_the_message_is_edited(_, cbd: CallbackQuery):
    cbd.answer(text=resolve_msg(key='EDIT_CBD'), show_alert=True)


async def edit_message_by_topic(cli: Client, msg: types.Message):
    """
    the message edit in topic > edit message in the user
    """

    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    chat_id = filters_db.get_tg_id_by_topic(topic_id=topic_id)

    msg_id = filters_db.get_user_msg_id_by_topic_msg_id(topic_id, msg_id=msg.id)

    if msg_id is None:
        return

    await edit_message(cli, msg, chat_id, msg_id, is_topic=False)

