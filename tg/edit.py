import pyrogram
from pyrogram import Client
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio, \
    InputMediaAnimation

from db.filters import is_tg_id_exists, get_group_by_tg_id, get_topic_msg_id_by_user_msg_id, get_tg_id_by_topic, \
    get_user_msg_id_by_topic_msg_id, is_group_exists
from tg.filters import is_have_a_group


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
    chat_id = get_group_by_tg_id(tg_id=tg_id)
    msg_id = get_topic_msg_id_by_user_msg_id(tg_id=tg_id, msg_id=msg.id)
    if msg_id is None:
        return
    await edit_message(cli, msg, chat_id, msg_id)


async def edit_message_by_topic(cli: Client, msg: Message):
    topic_id = topic if (topic:= msg.reply_to_top_message_id) else msg.reply_to_message_id
    chat_id = get_tg_id_by_topic(topic_id=topic_id)
    msg_id = get_user_msg_id_by_topic_msg_id(topic_id, msg_id=msg.id)
    if msg_id is None:
        return
    await edit_message(cli, msg, chat_id, msg_id)


@bot.on_edited_message(pyrogram.filters.create(is_have_a_group))
async def edited_message(cli: Client, msg: Message):
    tg_id = msg.from_user.id
    if msg.chat.id == tg_id:
        await edit_message_by_user(cli=cli, msg=msg)
    elif is_group_exists(group_id=msg.chat.id):
        await edit_message_by_topic(cli, msg)
    else:
        print("not edited")
        return